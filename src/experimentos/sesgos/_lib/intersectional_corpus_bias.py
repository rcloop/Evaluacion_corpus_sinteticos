"""
Métricas interseccionales sobre el corpus (solo datos).

- Género × Edad (sujeto de asistencia): tabla contingencia, χ².
- Género × Geografía (sujeto): tabla género × país/región (top-k), χ².
- Edad × Geografía: mismos bins gruesos y top geografías.

Entrada: entidades/*.json (por documento). Género sujeto: SEXO_SUJETO_ASISTENCIA o lexicón sobre
NOMBRE_SUJETO_ASISTENCIA. Edad: EDAD_SUJETO_ASISTENCIA / AGE_OF_SUBJECT en bins <60, 60–70, 70–80, ≥80.
Geografía: PAIS, TERRITORIO.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from name_gender_distribution import (
    iter_documents,
    iter_entities_from_annotation_obj,
    load_lexicon,
    normalize_sex_entity_value,
    extract_first_name,
    infer_gender,
    SUBJECT_NAME_LABELS,
    SEXO_SUJETO_ASISTENCIA_LABEL,
)
from age_distribution import parse_age

# Geografía: usar PAIS y TERRITORIO para "región" por doc
GEO_LABELS_PRIMARY = ["PAIS", "TERRITORIO"]
DEFAULT_AGE_LABELS = ["EDAD_SUJETO_ASISTENCIA", "AGE_OF_SUBJECT"]
# Bins gruesos para tablas χ² (evita celdas esperadas muy pequeñas frente a décadas).
INTERSECTIONAL_AGE_BIN_ORDER = ["<60", "60-70", "70-80", ">80"]
TOP_GEO_K = 15  # top regiones para tabla (resto "OTRO")


def coarse_age_bin_intersectional(age_years: int) -> str:
    """Map numeric age to reporting bins for gender×age and age×geography tests."""
    if age_years < 60:
        return "<60"
    if age_years < 70:
        return "60-70"
    if age_years < 80:
        return "70-80"
    return ">80"


def _get_first_value(pairs: List[Tuple[str, str]], label_set: set, normalizer=None):
    for lab, text in pairs:
        if lab.upper().strip() in label_set and text and str(text).strip():
            v = str(text).strip()
            if normalizer:
                v = normalizer(v)
            return v
    return None


def get_subject_gender_and_age_and_geo_per_doc(
    annotations_path: str,
    lexicon_path: Optional[str] = None,
    max_files: Optional[int] = None,
) -> List[Tuple[str, Optional[str], Optional[str], Optional[str]]]:
    """
    Por cada documento: (doc_id, gender, age_bin, geo).
    gender: SEXO_SUJETO_ASISTENCIA si existe; si no, lexicón sobre primer
    NOMBRE_SUJETO_ASISTENCIA.
    age_bin: uno de INTERSECTIONAL_AGE_BIN_ORDER a partir de la primera edad parseable.
    geo: primer PAIS o TERRITORIO normalizado.
    """
    lexicon = load_lexicon(lexicon_path)
    sexo_label = SEXO_SUJETO_ASISTENCIA_LABEL.upper().strip()
    subject_labels = {l.upper().strip() for l in SUBJECT_NAME_LABELS}
    age_labels = {l.upper().strip() for l in DEFAULT_AGE_LABELS}
    geo_labels = {l.upper().strip() for l in GEO_LABELS_PRIMARY}

    out: List[Tuple[str, Optional[str], Optional[str], Optional[str]]] = []
    for doc_id, pairs in iter_documents(annotations_path, max_files=max_files):
        subject_names = [text for lab, text in pairs if lab.upper().strip() in subject_labels and text]
        sex_values = [
            normalize_sex_entity_value(text)
            for lab, text in pairs
            if lab.upper().strip() == sexo_label and text
        ]
        parsed_ages: List[int] = []
        for lab, text in pairs:
            if lab.upper().strip() in age_labels and text:
                a = parse_age(text)
                if a is not None:
                    parsed_ages.append(a)
        geos = []
        for lab, text in pairs:
            if lab.upper().strip() in geo_labels and text:
                g = str(text).strip().upper()
                if g:
                    geos.append(g)

        gender = None
        if sex_values:
            gender = sex_values[0]
        elif subject_names:
            first = extract_first_name(subject_names[0])
            gender = infer_gender(first, lexicon, full_name=subject_names[0])
        age_bin = None
        if parsed_ages:
            # Per-document age: choose most frequent parsed age (mode).
            # Deterministic tie-break: choose the smallest age among tied modes.
            c = Counter(parsed_ages)
            max_count = max(c.values())
            modes = sorted([a for a, v in c.items() if v == max_count])
            age_bin = coarse_age_bin_intersectional(modes[0])
        geo = geos[0] if geos else None
        out.append((doc_id, gender, age_bin, geo))
    return out


def _chi2_independence_from_counts(
    row_keys: List[str], col_keys: List[str], counts: Dict[Tuple[str, str], int]
) -> Dict[str, Any]:
    table = [[counts.get((r, c), 0) for c in col_keys] for r in row_keys]
    r, c = len(table), len(table[0]) if table else 0
    if r == 0 or c == 0:
        return {"chi2": None, "p_value": None, "df": None}
    row_sums = [sum(table[i]) for i in range(r)]
    col_sums = [sum(table[i][j] for i in range(r)) for j in range(c)]
    total = sum(row_sums)
    if total == 0:
        return {"chi2": None, "p_value": None, "df": None}
    chi2 = 0.0
    for i in range(r):
        for j in range(c):
            exp = (row_sums[i] * col_sums[j]) / total
            if exp > 0:
                chi2 += ((table[i][j] - exp) ** 2) / exp
    df = (r - 1) * (c - 1)
    p_value = None
    try:
        from scipy.stats import chi2 as chi2_dist
        p_value = float(chi2_dist.sf(chi2, df=df))
    except Exception:
        pass
    df_min = min(r - 1, c - 1)
    cramers_v = (chi2 / (total * df_min)) ** 0.5 if total and df_min > 0 else None
    return {"chi2": float(chi2), "p_value": p_value, "df": float(df), "cramers_v": cramers_v}


def evaluate_intersectional_corpus_bias(
    annotations_path: str,
    lexicon_path: Optional[str] = None,
    max_files: Optional[int] = None,
    top_geo_k: int = TOP_GEO_K,
) -> Dict[str, Any]:
    rows = get_subject_gender_and_age_and_geo_per_doc(
        annotations_path, lexicon_path=lexicon_path, max_files=max_files
    )
    docs_with_gender = sum(1 for _, g, _, _ in rows if g is not None)
    docs_with_age = sum(1 for _, _, d, _ in rows if d is not None)
    docs_with_geo = sum(1 for _, _, _, geo in rows if geo is not None)
    docs_with_gender_age = sum(1 for _, g, d, _ in rows if g is not None and d is not None)
    docs_with_gender_geo = sum(1 for _, g, _, geo in rows if g is not None and geo is not None)
    docs_with_age_geo = sum(1 for _, _, d, geo in rows if d is not None and geo is not None)

    # Gender × Age
    ga_counts: Counter = Counter()
    for _, g, d, _ in rows:
        if g is not None and d is not None:
            ga_counts[(g, d)] += 1
    genders_sorted = ["fem", "masc", "other"]
    decades_sorted = [
        b for b in INTERSECTIONAL_AGE_BIN_ORDER if any(ga_counts.get((g, b), 0) > 0 for g in genders_sorted)
    ]
    if not decades_sorted:
        decades_sorted = list(INTERSECTIONAL_AGE_BIN_ORDER)
    ga_chi2 = _chi2_independence_from_counts(
        genders_sorted,
        decades_sorted,
        {k: v for k, v in ga_counts.items()},
    )
    ga_table = [[ga_counts.get((r, c), 0) for c in decades_sorted] for r in genders_sorted]

    # Gender × Geography: top_geo_k regiones, resto "OTRO"
    gg_counts: Counter = Counter()
    for _, g, _, geo in rows:
        if g is not None and geo is not None:
            gg_counts[(g, geo)] += 1
    # Deterministic ordering: break ties by geo label.
    all_geos = sorted({geo for (_, geo) in gg_counts.keys()})
    geo_totals = {geo: sum(gg_counts.get((gen, geo), 0) for gen in genders_sorted) for geo in all_geos}
    top_geos = sorted(all_geos, key=lambda geo: (-geo_totals.get(geo, 0), geo))[:top_geo_k]
    gg_table_counts: Counter = Counter()
    for (g, geo), v in gg_counts.items():
        col = geo if geo in top_geos else "_OTHER_"
        gg_table_counts[(g, col)] += v
    cols_geo = list(top_geos)
    if len(all_geos) > top_geo_k:
        cols_geo.append("_OTHER_")
    cols_geo = [c for c in cols_geo if any(gg_table_counts.get((r, c), 0) > 0 for r in genders_sorted)] or cols_geo
    gg_chi2 = _chi2_independence_from_counts(
        genders_sorted,
        cols_geo,
        dict(gg_table_counts),
    )
    gg_table = [[gg_table_counts.get((r, c), 0) for c in cols_geo] for r in genders_sorted]

    # Age × Geography: por cada top región, histograma de décadas (resumen: counts por (decade, geo))
    ag_counts: Counter = Counter()
    for _, _, d, geo in rows:
        if d is not None and geo is not None:
            col = geo if geo in top_geos else "_OTHER_"
            ag_counts[(d, col)] += 1
    decades_ag = [
        b for b in INTERSECTIONAL_AGE_BIN_ORDER if any(ag_counts.get((b, c), 0) > 0 for c in cols_geo)
    ]
    if not decades_ag:
        decades_ag = list(INTERSECTIONAL_AGE_BIN_ORDER)
    ag_chi2 = _chi2_independence_from_counts(
        decades_ag,
        cols_geo,
        dict(ag_counts),
    )
    ag_table = [[ag_counts.get((r, c), 0) for c in cols_geo] for r in decades_ag]

    return {
        "metric": "intersectional_corpus_bias",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_summary": {
            "annotations_path": str(annotations_path),
            "max_files": max_files,
            "docs_total": len(rows),
            "subject_gender_rule": "SEXO_SUJETO_ASISTENCIA if present; else lexicon on first subject name",
            "age_bins_intersectional": list(INTERSECTIONAL_AGE_BIN_ORDER),
            "docs_with_gender": docs_with_gender,
            "docs_with_age": docs_with_age,
            "docs_with_geo": docs_with_geo,
            "docs_with_gender_and_age": docs_with_gender_age,
            "docs_with_gender_and_geo": docs_with_gender_geo,
            "docs_with_age_and_geo": docs_with_age_geo,
            "top_geo_k": top_geo_k,
        },
        "n_tests_independence": 3,
        "gender_x_age": {
            "row_labels": genders_sorted,
            "col_labels": decades_sorted,
            "contingency_table": ga_table,
            "chi_square_independence": {
                **ga_chi2,
                "p_value_bonferroni": min(1.0, (ga_chi2.get("p_value") or 1.0) * 3),
            },
            "n": sum(ga_counts.values()),
        },
        "gender_x_geography": {
            "row_labels": genders_sorted,
            "col_labels": cols_geo,
            "contingency_table": gg_table,
            "chi_square_independence": {
                **gg_chi2,
                "p_value_bonferroni": min(1.0, (gg_chi2.get("p_value") or 1.0) * 3),
            },
            "n": sum(gg_table_counts.values()),
        },
        "age_x_geography": {
            "row_labels": decades_ag,
            "col_labels": cols_geo,
            "contingency_table": ag_table,
            "chi_square_independence": {
                **ag_chi2,
                "p_value_bonferroni": min(1.0, (ag_chi2.get("p_value") or 1.0) * 3),
            },
            "n": sum(ag_counts.values()),
        },
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Interseccionalidad: género×edad, género×geografía, edad×geografía")
    parser.add_argument("--annotations_path", required=True, help="Ruta a entidades/")
    parser.add_argument("--lexicon_path", default=None)
    parser.add_argument("--max_files", type=int, default=None)
    parser.add_argument("--top_geo_k", type=int, default=TOP_GEO_K)
    parser.add_argument("--output_path", default="bias_evaluation_results/intersectional_corpus_bias.json")
    args = parser.parse_args()
    result = evaluate_intersectional_corpus_bias(
        args.annotations_path,
        lexicon_path=args.lexicon_path,
        max_files=args.max_files,
        top_geo_k=args.top_geo_k,
    )
    out = Path(args.output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Output:", out)

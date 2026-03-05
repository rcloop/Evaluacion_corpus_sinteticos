"""
Diagnóstico × demografía (solo corpus).

Por documento: cruza género y edad del sujeto (entidades) con diagnósticos extraídos
del texto (documents/<doc_id>.txt). Tablas contingencia, χ², razones de prevalencia.

Entrada: corpus_root con entidades/ y documents/ (o paths separados).
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from name_gender_distribution import (
    iter_documents,
    load_lexicon,
    normalize_sex_entity_value,
    extract_first_name,
    infer_gender,
    SUBJECT_NAME_LABELS,
    SEXO_SUJETO_ASISTENCIA_LABEL,
)
from age_distribution import parse_age, decade_bin
from diagnosis_condition_bias import extract_diagnoses_from_text, normalize_dx

DEFAULT_AGE_LABELS = ["EDAD_SUJETO_ASISTENCIA", "AGE_OF_SUBJECT"]
DECADE_BINS = [f"{s}-{s+9}" for s in range(0, 120, 10)] + ["120+"]
TOP_DX_K = 25
TOP_AGE_BINS = 7  # e.g. 20-29..70-79 + 80+


def _get_doc_demographics(pairs: List[tuple], lexicon: Dict[str, str]) -> tuple:
    """Returns (gender, decade) for subject from entity pairs. gender in (fem,masc,other)."""
    sexo_label = SEXO_SUJETO_ASISTENCIA_LABEL.upper().strip()
    subject_labels = {l.upper().strip() for l in SUBJECT_NAME_LABELS}
    age_labels = {l.upper().strip() for l in DEFAULT_AGE_LABELS}
    subject_names = [text for lab, text in pairs if lab.upper().strip() in subject_labels and text]
    sex_values = [
        normalize_sex_entity_value(text)
        for lab, text in pairs
        if lab.upper().strip() == sexo_label and text
    ]
    ages = []
    for lab, text in pairs:
        if lab.upper().strip() in age_labels and text:
            a = parse_age(text)
            if a is not None:
                ages.append(decade_bin(a, max_decade=120))
    gender = None
    if subject_names:
        if sex_values:
            gender = sex_values[0]
        if gender is None:
            first = extract_first_name(subject_names[0])
            gender = infer_gender(first, lexicon)
    decade = ages[0] if ages else None
    return (gender, decade)


def _chi2_independence(table: List[List[int]]) -> Dict[str, Any]:
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
    return {"chi2": float(chi2), "p_value": p_value, "df": float(df)}


def evaluate_diagnosis_demography_bias(
    annotations_path: str,
    documents_path: str,
    lexicon_path: Optional[str] = None,
    max_files: Optional[int] = None,
    top_dx_k: int = TOP_DX_K,
    use_sections: bool = True,
    use_phrases: bool = True,
) -> Dict[str, Any]:
    """
    annotations_path: entidades/ dir
    documents_path: documents/ dir (same doc_id = same stem .json / .txt)
    """
    lexicon = load_lexicon(lexicon_path)
    ent_path = Path(annotations_path)
    doc_path = Path(documents_path)
    if not ent_path.exists() or not doc_path.exists():
        raise FileNotFoundError(f"Annotations: {ent_path}, Documents: {doc_path}")

    # (gender, dx) and (decade, dx) counts: each doc contributes for each dx in that doc
    g_dx: Counter = Counter()
    a_dx: Counter = Counter()
    docs_with_dx = 0
    docs_with_gender_dx = 0
    docs_with_age_dx = 0

    files = sorted(ent_path.glob("*.json"))
    if max_files is not None:
        files = files[:max_files]

    for fp in files:
        doc_id = fp.stem
        txt_file = doc_path / f"{doc_id}.txt"
        if not txt_file.exists():
            continue
        try:
            obj = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            continue
        from name_gender_distribution import iter_entities_from_annotation_obj
        pairs = list(iter_entities_from_annotation_obj(obj))
        gender, decade = _get_doc_demographics(pairs, lexicon)
        try:
            text = txt_file.read_text(encoding="utf-8")
        except Exception:
            continue
        dx_list = extract_diagnoses_from_text(text, use_sections=use_sections, use_phrases=use_phrases)
        dx_list = [normalize_dx(d) for d in dx_list if normalize_dx(d)]
        if not dx_list:
            continue
        docs_with_dx += 1
        for dx in dx_list:
            if gender is not None:
                g_dx[(gender, dx)] += 1
            if decade is not None:
                a_dx[(decade, dx)] += 1
        if gender is not None:
            docs_with_gender_dx += 1
        if decade is not None:
            docs_with_age_dx += 1

    genders = ["fem", "masc", "other"]
    # Top diagnósticos globalmente para columnas
    all_dx = set(dx for (_, dx) in g_dx.keys()) | set(dx for (_, dx) in a_dx.keys())
    top_dx = sorted(
        all_dx,
        key=lambda d: sum(g_dx.get((g, d), 0) for g in genders) + sum(a_dx.get((a, d), 0) for a in DECADE_BINS),
        reverse=True,
    )[:top_dx_k]

    # Gender × Diagnosis table (rows = genders, cols = top_dx)
    g_dx_table = [[g_dx.get((r, c), 0) for c in top_dx] for r in genders]
    g_dx_chi2 = _chi2_independence(g_dx_table)

    # Age × Diagnosis: use top age bins that have data
    age_bins_used = sorted(
        set(d for (d, _) in a_dx.keys()),
        key=lambda b: DECADE_BINS.index(b) if b in DECADE_BINS else 99,
    )[:TOP_AGE_BINS]
    if not age_bins_used:
        age_bins_used = [b for b in DECADE_BINS if any(a_dx.get((b, c), 0) > 0 for c in top_dx)] or DECADE_BINS[:5]
    a_dx_table = [[a_dx.get((r, c), 0) for c in top_dx] for r in age_bins_used]
    a_dx_chi2 = _chi2_independence(a_dx_table)

    return {
        "metric": "diagnosis_demography_bias",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_summary": {
            "annotations_path": str(annotations_path),
            "documents_path": str(documents_path),
            "max_files": max_files,
            "docs_with_diagnosis": docs_with_dx,
            "docs_with_gender_and_diagnosis": docs_with_gender_dx,
            "docs_with_age_and_diagnosis": docs_with_age_dx,
            "top_dx_k": top_dx_k,
        },
        "gender_x_diagnosis": {
            "row_labels": genders,
            "col_labels": top_dx,
            "contingency_table": g_dx_table,
            "chi_square_independence": g_dx_chi2,
            "n": sum(sum(row) for row in g_dx_table),
        },
        "age_x_diagnosis": {
            "row_labels": age_bins_used,
            "col_labels": top_dx,
            "contingency_table": a_dx_table,
            "chi_square_independence": a_dx_chi2,
            "n": sum(sum(row) for row in a_dx_table),
        },
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Diagnóstico × género y diagnóstico × edad (por documento)")
    parser.add_argument("--annotations_path", required=True, help="Ruta a entidades/")
    parser.add_argument("--documents_path", required=True, help="Ruta a documents/")
    parser.add_argument("--lexicon_path", default=None)
    parser.add_argument("--max_files", type=int, default=None)
    parser.add_argument("--output_path", default="bias_evaluation_results/diagnosis_demography_bias.json")
    args = parser.parse_args()
    result = evaluate_diagnosis_demography_bias(
        args.annotations_path,
        args.documents_path,
        lexicon_path=args.lexicon_path,
        max_files=args.max_files,
    )
    out = Path(args.output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Output:", out)

"""
Cobertura/completitud por documento: % de documentos con al menos un valor en cada dimensión.

Dimensiones: género (SEXO o nombre sujeto), edad (EDAD_SUJETO_ASISTENCIA), geografía (PAIS o TERRITORIO).
Opcional: % con las tres, matriz de co-ocurrencia de completitud.
"""

from __future__ import annotations

from collections import Counter
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
from age_distribution import parse_age

DEFAULT_AGE_LABELS = ["EDAD_SUJETO_ASISTENCIA", "AGE_OF_SUBJECT"]
GEO_LABELS = ["PAIS", "TERRITORIO"]


def evaluate_coverage_completeness(
    annotations_path: str,
    lexicon_path: Optional[str] = None,
    max_files: Optional[int] = None,
) -> Dict[str, Any]:
    lexicon = load_lexicon(lexicon_path)
    sexo_label = SEXO_SUJETO_ASISTENCIA_LABEL.upper().strip()
    subject_labels = {l.upper().strip() for l in SUBJECT_NAME_LABELS}
    age_labels = {l.upper().strip() for l in DEFAULT_AGE_LABELS}
    geo_labels = {l.upper().strip() for l in GEO_LABELS}

    total = 0
    has_gender = 0
    has_age = 0
    has_geo = 0
    has_gender_age = 0
    has_gender_geo = 0
    has_age_geo = 0
    has_all_three = 0
    # Co-occurrence of completeness: (has_gender, has_age, has_geo) -> count
    completeness_counts: Counter = Counter()

    for doc_id, pairs in iter_documents(annotations_path, max_files=max_files):
        total += 1
        g = False
        a = False
        geo = False
        subject_names = []
        sex_values = []
        for lab, text in pairs:
            lu = lab.upper().strip()
            if lu in subject_labels and text:
                subject_names.append(text)
            if lu == sexo_label and text:
                sex_values.append(normalize_sex_entity_value(text))
            if lu in age_labels and text and parse_age(text) is not None:
                a = True
            if lu in geo_labels and text and str(text).strip():
                geo = True
        g = bool(sex_values or subject_names)
        if g:
            has_gender += 1
        if a:
            has_age += 1
        if geo:
            has_geo += 1
        if g and a:
            has_gender_age += 1
        if g and geo:
            has_gender_geo += 1
        if a and geo:
            has_age_geo += 1
        if g and a and geo:
            has_all_three += 1
        key = (int(g), int(a), int(geo))
        completeness_counts[key] += 1

    pct = lambda x, t: (100.0 * x / t) if t else 0.0
    return {
        "metric": "coverage_completeness",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_summary": {
            "annotations_path": str(annotations_path),
            "max_files": max_files,
            "docs_total": total,
        },
        "by_dimension": {
            "has_gender": {"count": has_gender, "percent": pct(has_gender, total)},
            "has_age": {"count": has_age, "percent": pct(has_age, total)},
            "has_geography": {"count": has_geo, "percent": pct(has_geo, total)},
        },
        "by_combination": {
            "has_gender_and_age": {"count": has_gender_age, "percent": pct(has_gender_age, total)},
            "has_gender_and_geography": {"count": has_gender_geo, "percent": pct(has_gender_geo, total)},
            "has_age_and_geography": {"count": has_age_geo, "percent": pct(has_age_geo, total)},
            "has_all_three": {"count": has_all_three, "percent": pct(has_all_three, total)},
        },
        "completeness_cooccurrence": {
            "(gender, age, geo)": [{"key": list(k), "count": v} for k, v in sorted(completeness_counts.items())],
        },
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Cobertura/completitud por documento")
    parser.add_argument("--annotations_path", required=True)
    parser.add_argument("--lexicon_path", default=None)
    parser.add_argument("--max_files", type=int, default=None)
    parser.add_argument("--output_path", default="bias_evaluation_results/coverage_completeness.json")
    args = parser.parse_args()
    result = evaluate_coverage_completeness(
        args.annotations_path,
        lexicon_path=args.lexicon_path,
        max_files=args.max_files,
    )
    out = Path(args.output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(__import__("json").dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Output:", out)

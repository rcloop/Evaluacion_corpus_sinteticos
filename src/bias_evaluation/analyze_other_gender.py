"""
Análisis exhaustivo del origen de la categoría "other" en la métrica 1.1 (género).

Responde:
1. ¿Los "other" vienen de la anotación (SEXO_SUJETO_ASISTENCIA con valor no mapeado)?
2. ¿O los asigna el pipeline (falta SEXO o nombre no está en lexicón/heurística)?

Uso: desde src/bias_evaluation:
  python analyze_other_gender.py --annotations_path ../../corpus_repo/corpus_v1/entidades
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from name_gender_distribution import (
    SEXO_SUJETO_ASISTENCIA_LABEL,
    extract_first_name,
    iter_documents,
    load_lexicon,
    normalize_name,
    normalize_sex_entity_value,
    infer_gender,
    SUBJECT_NAME_LABELS,
)


def main():
    parser = argparse.ArgumentParser(description="Analyze why 'other' appears in gender distribution")
    parser.add_argument("--annotations_path", required=True, help="Path to entidades/ dir or JSON file")
    parser.add_argument("--max_files", type=int, default=None, help="Limit number of files (default: all)")
    parser.add_argument("--lexicon_path", default=None, help="Optional lexicon CSV/JSON")
    parser.add_argument("--output", default=None, help="Optional JSON output path")
    args = parser.parse_args()

    lexicon = load_lexicon(args.lexicon_path)
    sexo_label = SEXO_SUJETO_ASISTENCIA_LABEL.upper().strip()
    target_subject = {"NOMBRE_SUJETO_ASISTENCIA", "NAME_OF_ASSISTED_SUBJECT"}

    # Counts
    docs_with_subject_name = 0
    docs_with_sexo = 0
    subject_names_total = 0

    # When we HAVE SEXO in the doc: value -> (fem, masc, other)
    sex_value_to_gender: Counter[str] = Counter()
    sex_raw_to_normalized: dict[str, str] = {}  # raw text -> fem/masc/other

    # When we DON'T have SEXO: infer_gender result and reason
    inferred_fem = 0
    inferred_masc = 0
    inferred_other = 0
    # Reason for "other" when no SEXO: no_first_name | not_in_lexicon_and_heuristic_fails
    other_reason_no_first_name = 0
    other_reason_heuristic_fails = 0
    # Sample of first names that became "other" (no SEXO)
    sample_first_names_other: list[str] = []
    sample_full_names_other: list[str] = []
    # First names that became other (count)
    first_name_other_counter: Counter[str] = Counter()

    for doc_id, pairs in iter_documents(args.annotations_path, max_files=args.max_files):
        subject_names: list[str] = []
        sex_values: list[str] = []

        for label, text in pairs:
            lu = label.upper().strip()
            if lu == sexo_label:
                sex_values.append(text.strip())
            elif lu in target_subject:
                subject_names.append(text.strip())

        if not subject_names:
            continue

        docs_with_subject_name += 1
        subject_names_total += len(subject_names)
        if sex_values:
            docs_with_sexo += 1

        for i, name in enumerate(subject_names):
            if sex_values:
                raw = sex_values[i] if i < len(sex_values) else sex_values[0]
                sex_value_to_gender[raw] += 1
                norm = normalize_sex_entity_value(raw)
                sex_raw_to_normalized[raw] = norm
                continue

            # No SEXO: infer from name
            first = extract_first_name(name)
            g = infer_gender(first, lexicon, full_name=name)
            if g == "fem":
                inferred_fem += 1
            elif g == "masc":
                inferred_masc += 1
            else:
                inferred_other += 1
                if not first or not first.strip():
                    other_reason_no_first_name += 1
                else:
                    other_reason_heuristic_fails += 1
                    key = normalize_name(first)
                    first_name_other_counter[key] += 1
                    if len(sample_first_names_other) < 80:
                        sample_first_names_other.append(first or "(empty)")
                        sample_full_names_other.append(name[:60] if name else "(empty)")

    # Build report
    total_with_sexo = sum(sex_value_to_gender.values())
    by_norm_from_sex: Counter[str] = Counter()
    for raw, count in sex_value_to_gender.items():
        norm = normalize_sex_entity_value(raw)
        by_norm_from_sex[norm] += count

    report = {
        "summary": {
            "docs_with_subject_name": docs_with_subject_name,
            "subject_names_total": subject_names_total,
            "docs_with_sexo_entity": docs_with_sexo,
            "subject_names_with_sexo_in_doc": total_with_sexo,
            "subject_names_without_sexo_in_doc": subject_names_total - total_with_sexo,
        },
        "when_sexo_present": {
            "description": "When the document has SEXO_SUJETO_ASISTENCIA, we use it. Counts by normalized gender:",
            "fem": by_norm_from_sex.get("fem", 0),
            "masc": by_norm_from_sex.get("masc", 0),
            "other": by_norm_from_sex.get("other", 0),
            "raw_values_seen": dict(sex_value_to_gender),
            "raw_to_normalized_sample": dict(list(sex_raw_to_normalized.items())[:30]),
        },
        "when_sexo_absent": {
            "description": "When the document has NO SEXO_SUJETO_ASISTENCIA, we infer from first name (lexicon + heuristic A/O/OS).",
            "inferred_fem": inferred_fem,
            "inferred_masc": inferred_masc,
            "inferred_other": inferred_other,
            "other_reason_no_first_name": other_reason_no_first_name,
            "other_reason_heuristic_fails": other_reason_heuristic_fails,
            "lexicon_entries_used": len(lexicon),
            "sample_first_names_that_became_other": sample_first_names_other[:50],
            "sample_full_names_that_became_other": sample_full_names_other[:50],
            "top_30_first_names_other": first_name_other_counter.most_common(30),
        },
        "conclusion": {
            "other_from_annotation": by_norm_from_sex.get("other", 0),
            "other_from_pipeline_no_sexo": inferred_other,
            "total_other_expected": by_norm_from_sex.get("other", 0) + inferred_other,
        },
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Written to {args.output}")


if __name__ == "__main__":
    main()

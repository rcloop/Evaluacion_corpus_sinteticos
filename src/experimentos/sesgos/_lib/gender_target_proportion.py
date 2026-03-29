"""
Comparación de la proporción de género observada con una proporción objetivo (solo corpus).

Lee el resultado de 1.1 (o recomputa) y compara p_fem / p_masc con un objetivo (ej. 50/50).
Salida: diferencia absoluta, L1, flag si supera umbral.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from name_gender_distribution import evaluate_name_gender_distribution, DEFAULT_TARGET_LABELS


def evaluate_gender_target_proportion(
    annotations_path: str,
    lexicon_path: Optional[str] = None,
    max_files: Optional[int] = None,
    target_fem: float = 0.5,
    target_masc: float = 0.5,
    target_other: float = 0.0,
    max_abs_diff_threshold: float = 0.10,
    result_1_1: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Si result_1_1 se proporciona, lo usa; si no, ejecuta evaluate_name_gender_distribution.
    target_* deben sumar 1.0 (solo fem+masc si other=0).
    """
    if result_1_1 is None:
        result_1_1 = evaluate_name_gender_distribution(
            annotations_path=annotations_path,
            target_labels=DEFAULT_TARGET_LABELS,
            lexicon_path=lexicon_path,
            max_files=max_files,
        )
    overall = result_1_1.get("overall", {})
    counts = overall.get("counts", {})
    proportions = overall.get("proportions", {})
    p_fem = proportions.get("p_fem", 0.0)
    p_masc = proportions.get("p_masc", 0.0)
    p_other = proportions.get("p_other", 0.0)
    target = {"fem": target_fem, "masc": target_masc, "other": target_other}
    obs = {"fem": p_fem, "masc": p_masc, "other": p_other}
    diff_fem = p_fem - target_fem
    diff_masc = p_masc - target_masc
    diff_other = p_other - target_other
    l1 = abs(diff_fem) + abs(diff_masc) + abs(diff_other)
    max_abs_diff = max(abs(diff_fem), abs(diff_masc), abs(diff_other))
    flag_exceeds_threshold = max_abs_diff > max_abs_diff_threshold
    return {
        "metric": "gender_target_proportion",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_summary": {
            "annotations_path": annotations_path if result_1_1 is None else None,
            "max_files": max_files,
            "target_fem": target_fem,
            "target_masc": target_masc,
            "target_other": target_other,
            "max_abs_diff_threshold": max_abs_diff_threshold,
        },
        "observed": obs,
        "target": target,
        "difference": {"fem": diff_fem, "masc": diff_masc, "other": diff_other},
        "l1_distance": float(l1),
        "max_abs_difference": float(max_abs_diff),
        "flag_exceeds_threshold": flag_exceeds_threshold,
        "n": counts.get("n", 0),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Género vs proporción objetivo")
    parser.add_argument("--annotations_path", required=True)
    parser.add_argument("--lexicon_path", default=None)
    parser.add_argument("--max_files", type=int, default=None)
    parser.add_argument("--target_fem", type=float, default=0.5)
    parser.add_argument("--target_masc", type=float, default=0.5)
    parser.add_argument("--threshold", type=float, default=0.10)
    parser.add_argument("--output_path", default="bias_evaluation_results/gender_target_proportion.json")
    args = parser.parse_args()
    result = evaluate_gender_target_proportion(
        args.annotations_path,
        lexicon_path=args.lexicon_path,
        max_files=args.max_files,
        target_fem=args.target_fem,
        target_masc=args.target_masc,
        max_abs_diff_threshold=args.threshold,
    )
    Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_path).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Output:", args.output_path)

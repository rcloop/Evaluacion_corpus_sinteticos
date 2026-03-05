"""
Comparación de la distribución de edades observada con una referencia (solo corpus).

Lee el resultado de 1.4 (histogram por décadas) y opcionalmente una referencia (JSON: década -> p).
Calcula JSD o L1 entre observado y referencia.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from age_distribution import evaluate_age_distribution


def _js_divergence_bits(p: Dict[str, float], q: Dict[str, float]) -> Optional[float]:
    """Jensen-Shannon divergence in bits. p, q are dicts label -> probability."""
    keys = set(p.keys()) | set(q.keys())
    if not keys:
        return None
    m = {k: (p.get(k, 0.0) + q.get(k, 0.0)) / 2.0 for k in keys}
    js = 0.0
    for k in keys:
        pk, qk, mk = p.get(k, 0.0), q.get(k, 0.0), m[k]
        if mk > 0:
            if pk > 0:
                js += pk * math.log2(pk / mk)
            if qk > 0:
                js += qk * math.log2(qk / mk)
    return js / 2.0


def _l1_distance(p: Dict[str, float], q: Dict[str, float]) -> float:
    keys = set(p.keys()) | set(q.keys())
    return sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys) / 2.0


def load_age_reference(path: Optional[str]) -> Optional[Dict[str, float]]:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    ref: Dict[str, float] = {}
    if isinstance(data, dict):
        numeric = {}
        for k, v in data.items():
            if isinstance(k, str) and not k.startswith("_"):
                try:
                    numeric[k] = float(v)
                except (TypeError, ValueError):
                    continue
        total = sum(numeric.values())
        ref = {k: v / total if total else 0.0 for k, v in numeric.items()}
    return ref if ref else None


def evaluate_age_reference_comparison(
    annotations_path: str,
    max_files: Optional[int] = None,
    reference_path: Optional[str] = None,
    result_1_4: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Si result_1_4 se proporciona, lo usa; si no, ejecuta evaluate_age_distribution.
    reference_path: JSON con claves tipo "0-9", "10-19", ... y valores (counts o probabilidades).
    """
    if result_1_4 is None:
        result_1_4 = evaluate_age_distribution(
            annotations_path=annotations_path,
            max_files=max_files,
        )
    hist = result_1_4.get("histogram", {})
    bins = hist.get("bins", [])
    counts = hist.get("counts", [])
    n = hist.get("n", 0)
    obs_prob = {}
    if bins and n and n > 0:
        obs_prob = {b: counts[i] / n for i, b in enumerate(bins) if i < len(counts)}
    ref = load_age_reference(reference_path)
    jsd_bits = _js_divergence_bits(obs_prob, ref) if ref else None
    l1 = _l1_distance(obs_prob, ref) if ref else None
    return {
        "metric": "age_reference_comparison",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_summary": {
            "annotations_path": annotations_path if result_1_4 is None else None,
            "max_files": max_files,
            "reference_path": reference_path,
            "reference_provided": ref is not None,
        },
        "observed": {"bins": bins, "proportions": obs_prob, "n": n},
        "reference_proportions": ref,
        "js_divergence_bits": jsd_bits,
        "l1_distance": l1,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Edad vs distribución de referencia")
    parser.add_argument("--annotations_path", required=True)
    parser.add_argument("--max_files", type=int, default=None)
    parser.add_argument("--reference_path", default=None, help="JSON: decade_bin -> count or p")
    parser.add_argument("--output_path", default="bias_evaluation_results/age_reference_comparison.json")
    args = parser.parse_args()
    result = evaluate_age_reference_comparison(
        args.annotations_path,
        max_files=args.max_files,
        reference_path=args.reference_path,
    )
    Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_path).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Output:", args.output_path)

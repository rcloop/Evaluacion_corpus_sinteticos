"""
Resumen de diversidad (variety + balance) a partir de 1.3, 1.5 y 1.6.

No requiere recomputar: lee los JSON de salida de esas métricas (o paths opcionales).
Variety = support / número de categorías únicas.
Balance = entropía normalizada (ya calculada en cada métrica).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


def _read_json(path: Path) -> Optional[Dict]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def evaluate_diversity_summary(
    path_1_3: Optional[str] = None,
    path_1_5: Optional[str] = None,
    path_1_6: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Si output_dir se da y los path_* no, usa output_dir/1_3_..., 1_5_..., 1_6_....
    """
    if output_dir and (not path_1_3 and not path_1_5 and not path_1_6):
        base = Path(output_dir)
        path_1_3 = str(base / "1_3_geographic_toponymic_bias.json")
        path_1_5 = str(base / "1_5_institution_bias.json")
        path_1_6 = str(base / "1_6_diagnosis_condition_bias.json")
    dimensions = {}
    # 1.3 Geography
    if path_1_3:
        j = _read_json(Path(path_1_3))
        if j and "result" in j:
            j = j["result"]
        if j:
            ov = j.get("overall") or j.get("result", {}).get("overall")
            if ov:
                ent = ov.get("entropy", {})
                n = ov.get("n") or ov.get("support")
                dimensions["geography"] = {
                    "variety": int(n) if n is not None else ent.get("support"),
                    "balance_normalized_entropy": ent.get("normalized_entropy"),
                    "entropy_bits": ent.get("entropy_bits"),
                }
    # 1.5 Institution
    if path_1_5:
        j = _read_json(Path(path_1_5))
        if j and "result" in j:
            j = j["result"]
        if j:
            ov = j.get("overall") or j.get("result", {}).get("overall")
            if ov:
                n = ov.get("n")
                dimensions["institutions"] = {
                    "variety": int(n) if n is not None else None,
                    "hhi": ov.get("hhi"),
                    "gini": ov.get("gini"),
                }
    # 1.6 Diagnosis
    if path_1_6:
        j = _read_json(Path(path_1_6))
        if j and "result" in j:
            j = j["result"]
        if j:
            ov = j.get("overall") or j.get("result", {}).get("overall")
            if ov:
                ent = ov.get("entropy", {})
                dimensions["diagnosis"] = {
                    "variety": ov.get("n_unique") or ent.get("support"),
                    "balance_normalized_entropy": ent.get("normalized_entropy") if ent else None,
                    "entropy_bits": ent.get("entropy_bits") if ent else None,
                }
    return {
        "metric": "diversity_summary",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_summary": {
            "path_1_3": path_1_3,
            "path_1_5": path_1_5,
            "path_1_6": path_1_6,
        },
        "dimensions": dimensions,
        "description": "Variety = number of distinct categories; balance = normalized entropy (or HHI/Gini for institutions).",
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Resumen diversidad (variety/balance) desde 1.3, 1.5, 1.6")
    parser.add_argument("--output_dir", default=None, help="Directorio con 1_3, 1_5, 1_6 JSON")
    parser.add_argument("--path_1_3", default=None)
    parser.add_argument("--path_1_5", default=None)
    parser.add_argument("--path_1_6", default=None)
    parser.add_argument("--output_path", default="bias_evaluation_results/diversity_summary.json")
    args = parser.parse_args()
    result = evaluate_diversity_summary(
        path_1_3=args.path_1_3,
        path_1_5=args.path_1_5,
        path_1_6=args.path_1_6,
        output_dir=args.output_dir,
    )
    out = Path(args.output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Output:", out)

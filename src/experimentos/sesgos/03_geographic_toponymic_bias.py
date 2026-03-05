"""
Experimento 03 – Sesgos: Geographic/toponymic bias (1.3).
Resultados en: results/sesgos/03
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "03"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "1_3_geographic_toponymic_bias.json"

BIAS_DIR = REPO_ROOT / "src" / "bias_evaluation"
sys.path.insert(0, str(BIAS_DIR))

from geographic_toponymic_bias import evaluate_geographic_toponymic_bias
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 03 - Geographic toponymic bias")
    parser.add_argument("--corpus_root", required=True)
    parser.add_argument("--max_docs", type=int, default=None)
    parser.add_argument("--top_k", type=int, default=20)
    args = parser.parse_args()
    entidades = Path(args.corpus_root) / "entidades"
    max_files = None if (args.max_docs is not None and args.max_docs <= 0) else args.max_docs
    result = evaluate_geographic_toponymic_bias(
        annotations_path=str(entidades),
        top_k=args.top_k,
        max_files=max_files,
    )
    OUTPUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Resultados:", OUTPUT_FILE)

"""
Experimento 04 – Sesgos: Age distribution (1.4).
Resultados en: results/sesgos/04
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "04"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "1_4_age_distribution.json"

BIAS_DIR = REPO_ROOT / "src" / "bias_evaluation"
sys.path.insert(0, str(BIAS_DIR))

from age_distribution import evaluate_age_distribution
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 04 - Age distribution")
    parser.add_argument("--corpus_root", required=True)
    parser.add_argument("--max_docs", type=int, default=None)
    parser.add_argument("--underrep_min_percent", type=float, default=5.0)
    args = parser.parse_args()
    entidades = Path(args.corpus_root) / "entidades"
    max_files = None if (args.max_docs is not None and args.max_docs <= 0) else args.max_docs
    result = evaluate_age_distribution(
        annotations_path=str(entidades),
        max_files=max_files,
        underrep_min_percent=args.underrep_min_percent,
    )
    OUTPUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Resultados:", OUTPUT_FILE)

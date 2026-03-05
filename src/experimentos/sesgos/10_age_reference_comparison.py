"""
Experimento 10 – Sesgos: Age vs reference (usa 1.4).
Resultados en: results/sesgos/10
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "10"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "age_reference_comparison.json"

BIAS_DIR = REPO_ROOT / "src" / "bias_evaluation"
sys.path.insert(0, str(BIAS_DIR))

from age_distribution import evaluate_age_distribution
from age_reference_comparison import evaluate_age_reference_comparison
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 10 - Age reference comparison")
    parser.add_argument("--corpus_root", required=True)
    parser.add_argument("--max_docs", type=int, default=None)
    parser.add_argument("--age_reference_path", default=None)
    args = parser.parse_args()
    entidades = Path(args.corpus_root) / "entidades"
    max_files = None if (args.max_docs is not None and args.max_docs <= 0) else args.max_docs
    result_1_4 = evaluate_age_distribution(
        annotations_path=str(entidades),
        max_files=max_files,
    )
    result = evaluate_age_reference_comparison(
        annotations_path=str(entidades),
        max_files=max_files,
        reference_path=args.age_reference_path,
        result_1_4=result_1_4,
    )
    OUTPUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Resultados:", OUTPUT_FILE)

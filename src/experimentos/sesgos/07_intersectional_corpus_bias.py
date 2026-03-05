"""
Experimento 07 – Sesgos: Intersectional corpus bias (género×edad×geografía).
Resultados en: results/sesgos/07
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "07"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "intersectional_corpus_bias.json"

BIAS_DIR = REPO_ROOT / "src" / "bias_evaluation"
sys.path.insert(0, str(BIAS_DIR))

from intersectional_corpus_bias import evaluate_intersectional_corpus_bias
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 07 - Intersectional corpus bias")
    parser.add_argument("--corpus_root", required=True)
    parser.add_argument("--max_docs", type=int, default=None)
    parser.add_argument("--lexicon_path", default=None)
    args = parser.parse_args()
    entidades = Path(args.corpus_root) / "entidades"
    max_files = None if (args.max_docs is not None and args.max_docs <= 0) else args.max_docs
    result = evaluate_intersectional_corpus_bias(
        annotations_path=str(entidades),
        lexicon_path=args.lexicon_path,
        max_files=max_files,
    )
    OUTPUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Resultados:", OUTPUT_FILE)

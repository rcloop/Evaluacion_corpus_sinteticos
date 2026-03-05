"""
Experimento 12 – Sesgos: WEAT gender analysis.
Resultados en: results/sesgos/12
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "12"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "weat_gender_analysis.json"

BIAS_DIR = REPO_ROOT / "src" / "bias_evaluation"
sys.path.insert(0, str(BIAS_DIR))

from weat_gender_analysis import run_weat_analysis
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 12 - WEAT gender analysis")
    parser.add_argument("--corpus_root", required=True)
    parser.add_argument("--max_docs", type=int, default=None)
    parser.add_argument("--n_permutations", type=int, default=1000)
    args = parser.parse_args()
    documents = Path(args.corpus_root) / "documents"
    max_docs = None if (args.max_docs is not None and args.max_docs <= 0) else args.max_docs
    result = run_weat_analysis(
        documents_path=str(documents),
        max_docs=max_docs,
        n_permutations=args.n_permutations,
    )
    OUTPUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Resultados:", OUTPUT_FILE)

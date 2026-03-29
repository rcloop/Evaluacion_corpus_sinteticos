"""
Experiment 07 – Naturalness: statistical comparison (generated vs real reference texts).
Outputs: results/naturalidad/07

Requires non-empty directories of .txt files for both sides (default real path:
corpus_repo/real_validation_corpus). There is no synthetic fallback—populate the real
folder with your own validation export (see corpus_repo/export_real_validation_corpus.py).
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))
from repo_paths import DEFAULT_REAL_VALIDATION_DOCS_DIR, count_txt_documents_under_dir

OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "07"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "statistical_comparison_results.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from statistical_comparison import evaluate_statistical_comparison
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experiment 07 – Statistical comparison (generated vs real)")
    parser.add_argument("--generated_corpus", required=True, help="Path to generated-document .txt directory")
    parser.add_argument(
        "--real_corpus",
        default=str(DEFAULT_REAL_VALIDATION_DOCS_DIR),
        help=f"Path to real-reference .txt directory (default: {DEFAULT_REAL_VALIDATION_DOCS_DIR})",
    )
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=None)
    args = parser.parse_args()
    g, r = Path(args.generated_corpus), Path(args.real_corpus)
    if not r.is_dir():
        print(f"Error: real corpus missing or not a directory: {r}", file=sys.stderr)
        sys.exit(1)
    ng = count_txt_documents_under_dir(g) if g.is_dir() else 0
    nr = count_txt_documents_under_dir(r) if r.is_dir() else 0
    print(
        f"Experiment 07 – Statistical comparison. Generated: {args.generated_corpus} ({ng} docs) | Real: {args.real_corpus} ({nr} docs)"
    )
    if ng < 1:
        print(
            f"Error: generated corpus has no .txt files: {g}",
            file=sys.stderr,
        )
        sys.exit(1)
    if nr < 1:
        print(
            f"Error: real-reference corpus has no .txt files: {r}\n"
            "Add your validation .txt files there (or pass --real_corpus). "
            "This repo does not generate placeholder real data.",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        evaluate_statistical_comparison(
            generated_corpus_path=args.generated_corpus,
            real_corpus_path=args.real_corpus,
            output_path=args.output_path,
            sample_size=args.sample_size,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"Done. Results: {args.output_path}")

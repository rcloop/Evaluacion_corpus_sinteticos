"""
Experiment 08 – Statistical comparison: **full** synthetic documents vs real **W**-token sliding windows.

Same **W** (mean synthetic word count) and real windowing as experiment 02. Synthetic side is **not** truncated.
Compares only length-agnostic surface features (avg word length, avg sentence length, TTR); raw length
scalars are omitted from tests.

No valoración paragraph stripping (caller sets sanitize_real_chunks=False).

**Interpretation caveat:** Same as 02 — within-note dependence and a real side that may under-represent
global stylistic diversity (shared authors, templates, site habits). Bonferroni does not fix clustering.

Outputs: results/naturalidad/08/statistical_comparison_results.json
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))
from repo_paths import DEFAULT_REAL_VALIDATION_DOCS_DIR, count_txt_documents_under_dir

OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "08"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "statistical_comparison_results.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from statistical_comparison import evaluate_statistical_comparison
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Experiment 08 – Length-agnostic stats with real sliding windows"
    )
    parser.add_argument("--generated_corpus", required=True)
    parser.add_argument(
        "--real_corpus",
        default=str(DEFAULT_REAL_VALIDATION_DOCS_DIR),
        help=f"Real .txt directory (default: {DEFAULT_REAL_VALIDATION_DOCS_DIR})",
    )
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=None)
    parser.add_argument(
        "--real_window_stride",
        type=int,
        default=None,
        help="Stride between windows in tokens (default: W)",
    )
    args = parser.parse_args()
    g, r = Path(args.generated_corpus), Path(args.real_corpus)
    if not r.is_dir():
        print(f"Error: real corpus missing: {r}", file=sys.stderr)
        sys.exit(1)
    ng = count_txt_documents_under_dir(g) if g.is_dir() else 0
    nr = count_txt_documents_under_dir(r) if r.is_dir() else 0
    print(
        f"Experiment 08 – Real windows comparison. Generated: {g} ({ng} docs) | Real: {r} ({nr} docs)"
    )
    if ng < 1 or nr < 1:
        print("Error: both corpora need at least one .txt", file=sys.stderr)
        sys.exit(1)
    try:
        evaluate_statistical_comparison(
            generated_corpus_path=str(g),
            real_corpus_path=str(r),
            output_path=args.output_path,
            sample_size=args.sample_size,
            exclude_length_features=True,
            sanitize_real_chunks=False,
            real_sliding_windows=True,
            real_window_stride=args.real_window_stride,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"Done. Results: {args.output_path}")

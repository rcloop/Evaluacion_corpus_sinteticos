"""
Experiment 02 – Naturalness: AI detectability with real sliding windows.

- **W** = round(mean token count of synthetic documents), same tokenizer as experiment 07.
- Each synthetic doc is kept **in full** (one sample per file; no truncation to **W**).
- Each real doc is split into **non-overlapping** windows of **W** tokens (stride **W** by default),
  multiplying real samples and retaining content from later in long notes (including valoración
  headers inside windows — no paragraph sanitization).

**Interpretation caveat:** Windows from the same export are dependent. The real corpus may reflect a
**subset of clinicians / documentation practices**, not a uniform sample of “all human clinical
style”; see `src/experimentos/README.md` (Naturalness — limitations).

Outputs: results/naturalidad/02/ai_detection_results.json
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "02"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "ai_detection_results.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from ai_text_detection import evaluate_ai_detection
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Experiment 02 – Detectability with real corpus sliding windows (mean synthetic length)"
    )
    parser.add_argument("--generated_corpus", required=True)
    parser.add_argument(
        "--human_corpus",
        default=None,
        help="Real .txt directory (default: corpus_repo/real_validation_corpus)",
    )
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=None)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--real_window_stride",
        type=int,
        default=None,
        help="Stride in tokens between windows (default: W = non-overlapping)",
    )
    args = parser.parse_args()
    p = Path(args.generated_corpus)
    n = len(list(p.glob("*.txt"))) if p.is_dir() else 0
    print(f"Experiment 02 – Real windows detectability. Generated: {args.generated_corpus} | Docs: {n}")

    if args.human_corpus is None:
        candidate = REPO_ROOT / "corpus_repo" / "real_validation_corpus"
        if candidate.is_dir() and any(candidate.glob("*.txt")):
            args.human_corpus = str(candidate)
            print(f"[INFO] Using default human corpus: {args.human_corpus}")
        else:
            print(
                "Error: missing real/human corpus.\n"
                f"Pass --human_corpus or populate: {candidate}",
                file=sys.stderr,
            )
            raise SystemExit(1)
    else:
        hc = Path(args.human_corpus)
        if not hc.is_dir() or not any(hc.glob("*.txt")):
            print(f"Error: --human_corpus must be a directory with .txt files: {hc}", file=sys.stderr)
            raise SystemExit(1)

    evaluate_ai_detection(
        generated_corpus_path=args.generated_corpus,
        human_corpus_path=args.human_corpus,
        output_path=args.output_path,
        sample_size=args.sample_size,
        seed=args.seed,
        sanitize_real_chunks=False,
        real_sliding_windows=True,
        real_window_stride=args.real_window_stride,
    )
    print(f"Done. Results: {args.output_path}")

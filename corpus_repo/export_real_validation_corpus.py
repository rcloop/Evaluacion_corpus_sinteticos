#!/usr/bin/env python3
"""
Export real_validation_set.json to a directory of .txt files (real-only corpus).

This corpus is used for comparative naturalness experiments (e.g. as --real_corpus
in 07_statistical_comparison.py, or --human_corpus in 01_ai_detection.py).

Usage (from repo root or corpus_repo):
  python corpus_repo/export_real_validation_corpus.py [--output_dir corpus_repo/real_validation_corpus]

Output: one .txt per document, filename = {id}.txt (e.g. 1.txt, 2.txt, ...).
"""
from pathlib import Path
import argparse
import json
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_JSON = SCRIPT_DIR / "real_validation_set.json"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "real_validation_corpus"


def export_corpus(json_path: Path, output_dir: Path) -> int:
    """Load JSON and write one .txt per document. Returns number of files written."""
    if not json_path.exists():
        print(f"Error: {json_path} not found.", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading {json_path}...", flush=True)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("Error: JSON root must be a list of documents.", file=sys.stderr)
        sys.exit(1)

    count = 0
    for item in data:
        if not isinstance(item, dict):
            continue
        doc_id = item.get("id")
        text = item.get("text")
        if doc_id is None or text is None:
            continue
        # Safe filename: use string id (e.g. "1" -> "1.txt")
        safe_id = str(doc_id).replace("/", "_").replace("\\", "_")
        out_file = output_dir / f"{safe_id}.txt"
        out_file.write_text(text, encoding="utf-8")
        count += 1

    print(f"Exported {count} documents to {output_dir}")
    return count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export real_validation_set.json to a directory of .txt for naturalness experiments."
    )
    parser.add_argument(
        "--json_path",
        type=Path,
        default=DEFAULT_JSON,
        help=f"Path to real_validation_set.json (default: {DEFAULT_JSON})",
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for .txt files (default: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args()
    export_corpus(args.json_path, args.output_dir)


if __name__ == "__main__":
    main()

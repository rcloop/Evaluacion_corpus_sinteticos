"""
Experimento 11 – Sesgos: Coverage/completeness.
Resultados en: results/sesgos/11
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "11"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "coverage_completeness.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from coverage_completeness import evaluate_coverage_completeness
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 11 - Coverage completeness")
    parser.add_argument("--corpus_root", required=True)
    parser.add_argument("--max_docs", type=int, default=None)
    parser.add_argument("--lexicon_path", default=None)
    parser.add_argument("--output_path", default=str(OUTPUT_FILE), help="Ruta del JSON de salida")
    args = parser.parse_args()
    entidades = Path(args.corpus_root) / "entidades"
    max_files = None if (args.max_docs is not None and args.max_docs <= 0) else args.max_docs
    n_files = len(list(entidades.glob("*.json"))) if entidades.is_dir() else 1
    if max_files is not None:
        n_files = min(n_files, max_files)
    print(f"Experimento 11 – Coverage/completeness. Corpus: {args.corpus_root} | Documentos: {n_files}")
    result = evaluate_coverage_completeness(
        annotations_path=str(entidades),
        lexicon_path=args.lexicon_path,
        max_files=max_files,
    )
    out = Path(args.output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Listo. Resultados: {out}")

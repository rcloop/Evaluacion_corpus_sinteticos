"""
Experimento 04 – Naturalidad: Readability.
Resultados en: results/naturalidad/04
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "04"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "readability_results.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from readability import evaluate_readability
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 04 - Readability")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus")
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=None)
    args = parser.parse_args()
    p = Path(args.corpus_path)
    n = len(list(p.glob("*.txt"))) if p.is_dir() else 0
    print(f"Experimento 04 – Naturalidad: Readability. Corpus: {args.corpus_path} | Documentos: {n}")
    evaluate_readability(
        corpus_path=args.corpus_path,
        output_path=args.output_path,
        sample_size=args.sample_size,
    )
    print(f"Listo. Resultados: {args.output_path}")

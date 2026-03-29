"""
Experimento 03 – Naturalidad: Vocabulary richness.
Resultados en: results/naturalidad/03
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "03"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "vocabulary_richness_results.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from vocabulary_richness import evaluate_vocabulary_richness
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 03 - Vocabulary richness")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus")
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=None)
    args = parser.parse_args()
    p = Path(args.corpus_path)
    n = len(list(p.glob("*.txt"))) if p.is_dir() else 0
    print(f"Experimento 03 – Naturalidad: Vocabulary richness. Corpus: {args.corpus_path} | Documentos: {n}")
    evaluate_vocabulary_richness(
        corpus_path=args.corpus_path,
        output_path=args.output_path,
        sample_size=args.sample_size,
    )
    print(f"Listo. Resultados: {args.output_path}")

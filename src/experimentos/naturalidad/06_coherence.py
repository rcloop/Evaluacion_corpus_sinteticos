"""
Experimento 06 – Naturalidad: Coherence.
Resultados en: results/naturalidad/06
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "06"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "coherence_results.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from coherence import evaluate_coherence
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 06 - Coherence")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus")
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=None)
    parser.add_argument("--model_name", default="paraphrase-multilingual-MiniLM-L12-v2")
    args = parser.parse_args()
    p = Path(args.corpus_path)
    n = len(list(p.glob("*.txt"))) if p.is_dir() else 0
    print(f"Experimento 06 – Naturalidad: Coherence. Corpus: {args.corpus_path} | Documentos: {n}")
    evaluate_coherence(
        corpus_path=args.corpus_path,
        output_path=args.output_path,
        sample_size=args.sample_size,
        model_name=args.model_name,
    )
    print(f"Listo. Resultados: {args.output_path}")

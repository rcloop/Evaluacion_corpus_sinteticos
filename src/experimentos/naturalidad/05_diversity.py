"""
Experimento 05 – Naturalidad: Diversity metrics.
Resultados en: results/naturalidad/05
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "05"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "diversity_results.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from diversity_metrics import evaluate_diversity
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 05 - Diversity metrics")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus")
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=None, help="N docs (None o 0 = todo el corpus)")
    args = parser.parse_args()
    p = Path(args.corpus_path)
    n = len(list(p.glob("*.txt"))) if p.is_dir() else 0
    print(f"Experimento 05 – Naturalidad: Diversity metrics. Corpus: {args.corpus_path} | Documentos: {n}")
    sample_size = None if (args.sample_size is None or args.sample_size <= 0) else args.sample_size
    evaluate_diversity(
        corpus_path=args.corpus_path,
        output_path=args.output_path,
        sample_size=sample_size,
    )
    print(f"Listo. Resultados: {args.output_path}")

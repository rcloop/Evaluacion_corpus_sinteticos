"""
Experimento 07 – Naturalidad: Statistical comparison (generado vs real).
Resultados en: results/naturalidad/07

Corpus real de referencia: corpus_repo/real_validation_corpus (obligatorio; si no existe, el experimento falla).
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "07"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "statistical_comparison_results.json"

DEFAULT_REAL_CORPUS = REPO_ROOT / "corpus_repo" / "real_validation_corpus"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from statistical_comparison import evaluate_statistical_comparison
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 07 - Statistical comparison")
    parser.add_argument("--generated_corpus", required=True, help="Ruta al corpus generado")
    parser.add_argument(
        "--real_corpus",
        default=str(DEFAULT_REAL_CORPUS),
        help="Ruta al corpus real (default: corpus_repo/real_validation_corpus). Debe existir.",
    )
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=None)
    args = parser.parse_args()
    g, r = Path(args.generated_corpus), Path(args.real_corpus)
    if not r.is_dir():
        print(f"Error: el corpus real no existe o no es un directorio: {r}", file=sys.stderr)
        sys.exit(1)
    ng = len(list(g.glob("*.txt"))) if g.is_dir() else 0
    nr = len(list(r.glob("*.txt"))) if r.is_dir() else 0
    print(f"Experimento 07 – Naturalidad: Statistical comparison. Generado: {args.generated_corpus} ({ng} docs) | Real: {args.real_corpus} ({nr} docs)")
    evaluate_statistical_comparison(
        generated_corpus_path=args.generated_corpus,
        real_corpus_path=args.real_corpus,
        output_path=args.output_path,
        sample_size=args.sample_size,
    )
    print(f"Listo. Resultados: {args.output_path}")

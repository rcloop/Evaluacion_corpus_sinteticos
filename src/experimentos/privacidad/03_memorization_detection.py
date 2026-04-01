"""
Experimento 03 – Privacidad: Memorization Detection.
Resultados en: results/privacidad/03
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "privacidad" / "03"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "memorization_detection.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from nearest_neighbor_memorization import evaluate_memorization
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 03 - Memorization Detection")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus")
    parser.add_argument("--annotations_path", default=None, help="Ruta a entidades/ (opcional)")
    parser.add_argument("--output_path", default=str(OUTPUT_PATH))
    parser.add_argument("--semantic_model", default="paraphrase-multilingual-MiniLM-L12-v2")
    parser.add_argument("--skip_semantic", action="store_true", help="Solo duplicados exactos")
    parser.add_argument(
        "--semantic_top_k",
        type=int,
        default=5,
        help="Vecinos más similares por nota para el grafo de candidatos (sensibilidad; default 5)",
    )
    parser.add_argument("--max_docs", type=int, default=None, help="Máx. documentos a evaluar (para corpus grandes)")
    args = parser.parse_args()
    docs_dir = Path(args.corpus_path) / "documents" if (Path(args.corpus_path) / "documents").exists() else Path(args.corpus_path)
    n = len(list(docs_dir.glob("*.txt"))) if docs_dir.is_dir() else 0
    if args.max_docs is not None and args.max_docs > 0:
        n = min(n, args.max_docs)
    print(f"Experimento 03 – Privacidad: Memorization Detection. Corpus: {args.corpus_path} | Documentos: {n}")
    evaluate_memorization(
        corpus_path=args.corpus_path,
        annotations_path=args.annotations_path,
        output_path=args.output_path,
        semantic_model=args.semantic_model,
        semantic_top_k=args.semantic_top_k,
        skip_semantic=args.skip_semantic,
        max_docs=args.max_docs,
    )
    print(f"Listo. Resultados: {args.output_path}")

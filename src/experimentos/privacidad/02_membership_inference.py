"""
Experimento 02 – Privacidad: Membership Inference.
Resultados en: results/privacidad/02
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "privacidad" / "02"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "membership_inference.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from membership_inference import evaluate_membership_inference
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 02 - Membership Inference")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus")
    parser.add_argument("--external_corpus_path", default=None, help="Ruta a corpus externo (opcional)")
    parser.add_argument("--output_path", default=str(OUTPUT_PATH))
    args = parser.parse_args()
    docs_dir = Path(args.corpus_path) / "documents" if (Path(args.corpus_path) / "documents").exists() else Path(args.corpus_path)
    n = len(list(docs_dir.glob("*.txt"))) if docs_dir.is_dir() else 0
    print(f"Experimento 02 – Privacidad: Membership Inference. Corpus: {args.corpus_path} | Documentos: {n}")
    evaluate_membership_inference(
        corpus_path=args.corpus_path,
        external_corpus_path=args.external_corpus_path,
        output_path=args.output_path,
    )
    print(f"Listo. Resultados: {args.output_path}")

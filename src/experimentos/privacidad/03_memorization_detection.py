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

PRIV_DIR = REPO_ROOT / "src" / "privacy_evaluation"
sys.path.insert(0, str(PRIV_DIR))

from nearest_neighbor_memorization import evaluate_memorization
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 03 - Memorization Detection")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus")
    parser.add_argument("--annotations_path", default=None, help="Ruta a entidades/ (opcional)")
    parser.add_argument("--output_path", default=str(OUTPUT_PATH))
    parser.add_argument("--semantic_model", default="paraphrase-multilingual-MiniLM-L12-v2")
    parser.add_argument("--skip_semantic", action="store_true", help="Solo duplicados exactos")
    args = parser.parse_args()
    evaluate_memorization(
        corpus_path=args.corpus_path,
        annotations_path=args.annotations_path,
        output_path=args.output_path,
        semantic_model=args.semantic_model,
        skip_semantic=args.skip_semantic,
    )
    print("Resultados:", args.output_path)

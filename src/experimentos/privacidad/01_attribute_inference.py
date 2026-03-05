"""
Experimento 01 – Privacidad: Attribute Inference.
Resultados en: results/privacidad/01
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "privacidad" / "01"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "attribute_inference.json"

PRIV_DIR = REPO_ROOT / "src" / "privacy_evaluation"
sys.path.insert(0, str(PRIV_DIR))

from attribute_inference import evaluate_attribute_inference
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 01 - Attribute Inference")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus (directorio o .json)")
    parser.add_argument("--annotations_path", default=None, help="Ruta a entidades/ (opcional)")
    parser.add_argument("--output_path", default=str(OUTPUT_PATH))
    args = parser.parse_args()
    evaluate_attribute_inference(
        corpus_path=args.corpus_path,
        annotations_path=args.annotations_path,
        output_path=args.output_path,
    )
    print("Resultados:", args.output_path)

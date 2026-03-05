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

PRIV_DIR = REPO_ROOT / "src" / "privacy_evaluation"
sys.path.insert(0, str(PRIV_DIR))

from membership_inference import evaluate_membership_inference
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 02 - Membership Inference")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus")
    parser.add_argument("--external_corpus_path", default=None, help="Ruta a corpus externo (opcional)")
    parser.add_argument("--output_path", default=str(OUTPUT_PATH))
    args = parser.parse_args()
    evaluate_membership_inference(
        corpus_path=args.corpus_path,
        external_corpus_path=args.external_corpus_path,
        output_path=args.output_path,
    )
    print("Resultados:", args.output_path)

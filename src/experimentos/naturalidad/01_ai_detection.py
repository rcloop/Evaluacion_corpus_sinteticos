"""
Experimento 01 – Naturalidad: AI text detection.
Resultados en: results/naturalidad/01
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "01"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "ai_detection_results.json"

NAT_DIR = REPO_ROOT / "src" / "privacy_evaluation" / "naturalness_evaluation"
sys.path.insert(0, str(NAT_DIR))

from ai_text_detection import evaluate_ai_detection
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 01 - AI text detection")
    parser.add_argument("--generated_corpus", required=True, help="Ruta al corpus generado")
    parser.add_argument("--human_corpus", default=None, help="Ruta a corpus humano (opcional)")
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    args = parser.parse_args()
    evaluate_ai_detection(
        generated_corpus_path=args.generated_corpus,
        human_corpus_path=args.human_corpus,
        output_path=args.output_path,
    )
    print("Resultados:", args.output_path)

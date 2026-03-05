"""
Experimento 07 – Naturalidad: Statistical comparison (generado vs real).
Resultados en: results/naturalidad/07
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "07"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "statistical_comparison_results.json"

NAT_DIR = REPO_ROOT / "src" / "privacy_evaluation" / "naturalness_evaluation"
sys.path.insert(0, str(NAT_DIR))

from statistical_comparison import evaluate_statistical_comparison
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 07 - Statistical comparison")
    parser.add_argument("--generated_corpus", required=True, help="Ruta al corpus generado")
    parser.add_argument("--real_corpus", required=True, help="Ruta al corpus real (ej. MEDDOCAN)")
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=None)
    args = parser.parse_args()
    evaluate_statistical_comparison(
        generated_corpus_path=args.generated_corpus,
        real_corpus_path=args.real_corpus,
        output_path=args.output_path,
        sample_size=args.sample_size,
    )
    print("Resultados:", args.output_path)

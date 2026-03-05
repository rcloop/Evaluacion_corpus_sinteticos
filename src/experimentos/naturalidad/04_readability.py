"""
Experimento 04 – Naturalidad: Readability.
Resultados en: results/naturalidad/04
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "04"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "readability_results.json"

NAT_DIR = REPO_ROOT / "src" / "privacy_evaluation" / "naturalness_evaluation"
sys.path.insert(0, str(NAT_DIR))

from readability import evaluate_readability
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 04 - Readability")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus")
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=None)
    args = parser.parse_args()
    evaluate_readability(
        corpus_path=args.corpus_path,
        output_path=args.output_path,
        sample_size=args.sample_size,
    )
    print("Resultados:", args.output_path)

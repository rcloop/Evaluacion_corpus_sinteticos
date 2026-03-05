"""
Experimento 02 – Naturalidad: Perplexity.
Resultados en: results/naturalidad/02
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "02"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "perplexity_results.json"

NAT_DIR = REPO_ROOT / "src" / "privacy_evaluation" / "naturalness_evaluation"
sys.path.insert(0, str(NAT_DIR))

from perplexity import evaluate_perplexity
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 02 - Perplexity")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus")
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=None)
    parser.add_argument("--model_name", default="dccuchile/bert-base-spanish-wwm-uncased")
    args = parser.parse_args()
    evaluate_perplexity(
        corpus_path=args.corpus_path,
        output_path=args.output_path,
        sample_size=args.sample_size,
        model_name=args.model_name,
    )
    print("Resultados:", args.output_path)

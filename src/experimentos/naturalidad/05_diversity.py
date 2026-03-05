"""
Experimento 05 – Naturalidad: Diversity metrics.
Resultados en: results/naturalidad/05
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "05"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "diversity_results.json"

NAT_DIR = REPO_ROOT / "src" / "privacy_evaluation" / "naturalness_evaluation"
sys.path.insert(0, str(NAT_DIR))

from diversity_metrics import evaluate_diversity
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 05 - Diversity metrics")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus")
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=5000, help="Por rendimiento (default 5000)")
    args = parser.parse_args()
    evaluate_diversity(
        corpus_path=args.corpus_path,
        output_path=args.output_path,
        sample_size=args.sample_size,
    )
    print("Resultados:", args.output_path)

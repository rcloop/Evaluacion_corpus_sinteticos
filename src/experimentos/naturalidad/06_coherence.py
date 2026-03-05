"""
Experimento 06 – Naturalidad: Coherence.
Resultados en: results/naturalidad/06
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "06"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "coherence_results.json"

NAT_DIR = REPO_ROOT / "src" / "privacy_evaluation" / "naturalness_evaluation"
sys.path.insert(0, str(NAT_DIR))

from coherence import evaluate_coherence
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 06 - Coherence")
    parser.add_argument("--corpus_path", required=True, help="Ruta al corpus")
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument("--sample_size", type=int, default=None)
    parser.add_argument("--model_name", default="paraphrase-multilingual-MiniLM-L12-v2")
    args = parser.parse_args()
    evaluate_coherence(
        corpus_path=args.corpus_path,
        output_path=args.output_path,
        sample_size=args.sample_size,
        model_name=args.model_name,
    )
    print("Resultados:", args.output_path)

"""
Experimento 06 – Sesgos: Diagnosis/condition bias (1.6).
Resultados en: results/sesgos/06
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "06"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "1_6_diagnosis_condition_bias.json"

BIAS_DIR = REPO_ROOT / "src" / "bias_evaluation"
sys.path.insert(0, str(BIAS_DIR))

from diagnosis_condition_bias import evaluate_diagnosis_bias
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 06 - Diagnosis condition bias")
    parser.add_argument("--corpus_root", required=True)
    parser.add_argument("--max_docs", type=int, default=None)
    parser.add_argument("--diagnosis_reference_path", default=None)
    parser.add_argument("--top_k", type=int, default=20)
    args = parser.parse_args()
    documents = Path(args.corpus_root) / "documents"
    max_files = None if (args.max_docs is not None and args.max_docs <= 0) else args.max_docs
    result = evaluate_diagnosis_bias(
        documents_path=str(documents),
        reference_path=args.diagnosis_reference_path,
        top_k=args.top_k,
        max_files=max_files,
        use_sections=True,
        use_phrases=True,
    )
    OUTPUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Resultados:", OUTPUT_FILE)

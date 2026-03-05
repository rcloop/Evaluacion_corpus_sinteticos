"""
Experimento 09 – Sesgos: Gender vs target proportion (usa 1.1).
Resultados en: results/sesgos/09
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "09"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "gender_target_proportion.json"

BIAS_DIR = REPO_ROOT / "src" / "bias_evaluation"
sys.path.insert(0, str(BIAS_DIR))

from name_gender_distribution import DEFAULT_TARGET_LABELS, evaluate_name_gender_distribution
from gender_target_proportion import evaluate_gender_target_proportion
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 09 - Gender target proportion")
    parser.add_argument("--corpus_root", required=True)
    parser.add_argument("--max_docs", type=int, default=None)
    parser.add_argument("--lexicon_path", default=None)
    parser.add_argument("--target_fem", type=float, default=0.5)
    parser.add_argument("--target_masc", type=float, default=0.5)
    args = parser.parse_args()
    entidades = Path(args.corpus_root) / "entidades"
    max_files = None if (args.max_docs is not None and args.max_docs <= 0) else args.max_docs
    result_1_1 = evaluate_name_gender_distribution(
        annotations_path=str(entidades),
        target_labels=DEFAULT_TARGET_LABELS,
        lexicon_path=args.lexicon_path,
        max_files=max_files,
    )
    result = evaluate_gender_target_proportion(
        annotations_path=str(entidades),
        lexicon_path=args.lexicon_path,
        max_files=max_files,
        target_fem=args.target_fem,
        target_masc=args.target_masc,
        result_1_1=result_1_1,
    )
    OUTPUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Resultados:", OUTPUT_FILE)

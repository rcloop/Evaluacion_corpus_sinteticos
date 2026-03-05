"""
Experimento 01 – Sesgos: Name gender distribution (1.1).
Resultados en: results/sesgos/01
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "01"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "1_1_name_gender_distribution.json"

BIAS_DIR = REPO_ROOT / "src" / "bias_evaluation"
sys.path.insert(0, str(BIAS_DIR))

from name_gender_distribution import DEFAULT_TARGET_LABELS, evaluate_name_gender_distribution
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 01 - Name gender distribution")
    parser.add_argument("--corpus_root", required=True, help="Ruta a corpus (con entidades/ y documents/)")
    parser.add_argument("--max_docs", type=int, default=None, help="Máx. archivos (0 = todos)")
    parser.add_argument("--lexicon_path", default=None)
    args = parser.parse_args()
    entidades = Path(args.corpus_root) / "entidades"
    max_files = None if (args.max_docs is not None and args.max_docs <= 0) else args.max_docs
    result = evaluate_name_gender_distribution(
        annotations_path=str(entidades),
        target_labels=DEFAULT_TARGET_LABELS,
        lexicon_path=args.lexicon_path,
        max_files=max_files,
    )
    OUTPUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Resultados:", OUTPUT_FILE)

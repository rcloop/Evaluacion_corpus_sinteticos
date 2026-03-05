"""
Experimento 13 – Sesgos: Diversity summary (lee 1.3, 1.5, 1.6).
Ejecutar 03, 05 y 06 antes para que existan los JSON.
Resultados en: results/sesgos/13
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "13"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "diversity_summary.json"

# Paths a salidas de experimentos 03, 05, 06
RESULTS = REPO_ROOT / "results" / "sesgos"
PATH_1_3 = RESULTS / "03" / "1_3_geographic_toponymic_bias.json"
PATH_1_5 = RESULTS / "05" / "1_5_institution_bias.json"
PATH_1_6 = RESULTS / "06" / "1_6_diagnosis_condition_bias.json"

BIAS_DIR = REPO_ROOT / "src" / "bias_evaluation"
sys.path.insert(0, str(BIAS_DIR))

from diversity_summary import evaluate_diversity_summary
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 13 - Diversity summary (requiere 03, 05, 06)")
    parser.add_argument("--path_1_3", default=str(PATH_1_3), help="JSON de 1.3 (geographic)")
    parser.add_argument("--path_1_5", default=str(PATH_1_5), help="JSON de 1.5 (institution)")
    parser.add_argument("--path_1_6", default=str(PATH_1_6), help="JSON de 1.6 (diagnosis)")
    args = parser.parse_args()
    result = evaluate_diversity_summary(
        path_1_3=args.path_1_3 if Path(args.path_1_3).exists() else None,
        path_1_5=args.path_1_5 if Path(args.path_1_5).exists() else None,
        path_1_6=args.path_1_6 if Path(args.path_1_6).exists() else None,
    )
    OUTPUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Resultados:", OUTPUT_FILE)

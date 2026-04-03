"""
Experimento 11 – Sesgos: Diversity summary (lee 1.3 y 1.5).
Ejecutar 03 y 05 antes para que existan los JSON.
Resultados en: results/sesgos/11
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "11"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "diversity_summary.json"

# Paths a salidas de experimentos 03, 05
RESULTS = REPO_ROOT / "results" / "sesgos"
PATH_1_3 = RESULTS / "03" / "1_3_geographic_toponymic_bias.json"
PATH_1_5 = RESULTS / "05" / "1_5_institution_bias.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from diversity_summary import evaluate_diversity_summary
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 11 - Diversity summary (requiere 03, 05)")
    parser.add_argument("--path_1_3", default=str(PATH_1_3), help="JSON de 1.3 (geographic)")
    parser.add_argument("--path_1_5", default=str(PATH_1_5), help="JSON de 1.5 (institution)")
    parser.add_argument("--output_path", default=str(OUTPUT_FILE), help="Ruta del JSON de salida")
    args = parser.parse_args()
    print("Experimento 11 – Diversity summary. Leyendo resultados 03, 05...")
    result = evaluate_diversity_summary(
        path_1_3=args.path_1_3 if Path(args.path_1_3).exists() else None,
        path_1_5=args.path_1_5 if Path(args.path_1_5).exists() else None,
    )
    out = Path(args.output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Listo. Resultados: {out}")

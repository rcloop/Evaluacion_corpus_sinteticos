"""
Lista los nombres que el experimento 01 clasifica como "other" para que puedas
revisarlos y asignarlos a fem o masc.

Uso (desde repo root):
  python src/experimentos/sesgos/list_other_names.py --corpus_root corpus_repo/corpus_v1 [--max_docs N]

Genera:
  - results/sesgos/01/names_other_for_review.json  (lista con first_name, full_text, entity_label)
  - results/sesgos/01/names_other_for_review.csv   (para rellenar columna genero_revisado: fem o masc)

Después de rellenar el CSV, aplica los cambios al lexicón con:
  python src/experimentos/sesgos/apply_other_review.py --csv results/sesgos/01/names_other_for_review.csv
"""
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = REPO_ROOT / "results" / "sesgos" / "01"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from name_gender_distribution import (
    DEFAULT_TARGET_LABELS,
    collect_other_names,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Listar nombres clasificados como 'other' para revisión")
    parser.add_argument("--corpus_root", required=True, help="Ruta al corpus (con entidades/)")
    parser.add_argument("--max_docs", type=int, default=None, help="Máx. documentos (opcional)")
    args = parser.parse_args()
    entidades = Path(args.corpus_root) / "entidades"
    if not entidades.exists():
        print(f"Error: no existe {entidades}")
        sys.exit(1)

    print("Recorriendo corpus para detectar nombres clasificados como 'other'...")
    others = collect_other_names(
        annotations_path=str(entidades),
        target_labels=DEFAULT_TARGET_LABELS,
        lexicon_path=None,
        max_files=args.max_docs,
    )

    # Un nombre puede aparecer varias veces; agrupar por first_name con un ejemplo de texto
    by_first: dict = {}
    for r in others:
        fn = r.get("first_name") or ""
        if fn and fn not in by_first:
            by_first[fn] = {
                "first_name": fn,
                "full_text_example": r.get("full_text", ""),
                "entity_label": r.get("entity_label", ""),
                "count": 0,
            }
        if fn:
            by_first[fn]["count"] = by_first[fn].get("count", 0) + 1

    list_for_review = sorted(by_first.values(), key=lambda x: (x["first_name"].lower(), x["full_text_example"]))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "names_other_for_review.json"
    json_path.write_text(
        json.dumps({"description": "Nombres que quedaron como 'other'. Revisa y asigna fem/masc en el CSV.", "items": list_for_review}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"JSON: {json_path} ({len(list_for_review)} nombres únicos)")

    csv_path = OUT_DIR / "names_other_for_review.csv"
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("first_name,full_text_example,entity_label,count,genero_revisado\n")
        for r in list_for_review:
            name = (r.get("first_name") or "").replace(",", ";")
            text = (r.get("full_text_example") or "").replace(",", ";").replace("\n", " ")
            label = r.get("entity_label", "")
            count = r.get("count", 0)
            f.write(f'"{name}","{text}","{label}",{count},\n')
    print(f"CSV: {csv_path}")
    print("Rellena la columna 'genero_revisado' con fem o masc y ejecuta:")
    print("  python src/experimentos/sesgos/apply_other_review.py --csv results/sesgos/01/names_other_for_review.csv")
    if not list_for_review:
        print("(No hay nombres 'other' en el corpus con el lexicón actual.)")

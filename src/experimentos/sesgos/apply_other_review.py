"""
Aplica la revisión de nombres "other": lee un CSV con columnas first_name y genero_revisado
(fem o masc) y actualiza data/sesgos/name_gender_lexicon.json moviendo esos nombres
a la lista fem o masc.

Uso (desde repo root):
  python src/experimentos/sesgos/apply_other_review.py --csv results/sesgos/01/names_other_for_review.csv

El CSV debe tener cabecera y al menos: first_name (o nombre), genero_revisado (fem/masc).
Las filas con genero_revisado vacío o distinto de fem/masc se ignoran.
"""
import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CANONICAL_JSON = REPO_ROOT / "data" / "sesgos" / "name_gender_lexicon.json"


def normalize(s: str) -> str:
    return str(s).strip().upper() if s else ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Aplicar revisión de nombres other al lexicón")
    parser.add_argument("--csv", required=True, help="CSV con first_name/nombre y genero_revisado (fem/masc)")
    args = parser.parse_args()
    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"Error: no existe {csv_path}")
        sys.exit(1)
    if not CANONICAL_JSON.exists():
        print(f"Error: no existe lexicón canónico {CANONICAL_JSON}. Ejecuta antes export_name_gender_lexicon.py")
        sys.exit(1)

    data = json.loads(CANONICAL_JSON.read_text(encoding="utf-8"))
    fem = set(data.get("fem", []))
    masc = set(data.get("masc", []))
    other = set(data.get("other", []))

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            print("Error: CSV sin cabecera")
            sys.exit(1)
        fields = [c.strip().lower() for c in reader.fieldnames]
        name_col = "first_name" if "first_name" in fields else "nombre" if "nombre" in fields else None
        gen_col = "genero_revisado" if "genero_revisado" in fields else "genero" if "genero" in fields else None
        if not name_col or not gen_col:
            print("Error: CSV debe tener columnas first_name (o nombre) y genero_revisado (o genero)")
            sys.exit(1)
        name_key = next(c for c in reader.fieldnames if c.strip().lower() == name_col)
        gen_key = next(c for c in reader.fieldnames if c.strip().lower() == gen_col)

        added_fem = []
        added_masc = []
        for row in reader:
            name = normalize(row.get(name_key, ""))
            g = normalize(row.get(gen_key, ""))
            if not name or g not in ("FEM", "MASC"):
                continue
            if g == "FEM":
                fem.add(name)
                other.discard(name)
                added_fem.append(name)
            else:
                masc.add(name)
                other.discard(name)
                added_masc.append(name)

    data["fem"] = sorted(fem)
    data["masc"] = sorted(masc)
    data["other"] = sorted(other)
    data["count_fem"] = len(data["fem"])
    data["count_masc"] = len(data["masc"])

    CANONICAL_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Actualizado: {CANONICAL_JSON}")
    print(f"Añadidos a fem: {len(added_fem)}")
    print(f"Añadidos a masc: {len(added_masc)}")
    if added_fem:
        print("  fem:", ", ".join(sorted(added_fem)[:15]), "..." if len(added_fem) > 15 else "")
    if added_masc:
        print("  masc:", ", ".join(sorted(added_masc)[:15]), "..." if len(added_masc) > 15 else "")


if __name__ == "__main__":
    main()

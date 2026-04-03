"""
Exporta el lexicón de nombres por género (fem/masc) para revisión.

- Escribe el archivo CANÓNICO data/sesgos/name_gender_lexicon.json que usan por defecto
  todos los experimentos de sesgos que consumen el lexicón (p. ej. 01, 02, 06, 07, …). Si editas ese JSON
  (mover nombres entre fem/masc), los scripts lo cargarán sin pasar --lexicon_path.
- Además escribe results/sesgos/01/name_gender_lexicon_review.json y .csv para revisión.

Uso: desde repo root: python src/experimentos/sesgos/export_name_gender_lexicon.py
     Si ya editaste data/sesgos/name_gender_lexicon.json, no vuelvas a ejecutar export
     (o haz backup) para no sobrescribir tus cambios.
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
CANONICAL_DIR = REPO_ROOT / "data" / "sesgos"
CANONICAL_JSON = CANONICAL_DIR / "name_gender_lexicon.json"
OUT_DIR = REPO_ROOT / "results" / "sesgos" / "01"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from name_gender_distribution import _default_lexicon

if __name__ == "__main__":
    lex = _default_lexicon()
    fem = sorted(k for k, v in lex.items() if v == "fem")
    masc = sorted(k for k, v in lex.items() if v == "masc")

    out = {
        "description": "Lexicón de nombres para clasificación de género. fem = femenino, masc = masculino, other = no clasificado (opcional).",
        "fem": fem,
        "masc": masc,
        "other": [],
        "count_fem": len(fem),
        "count_masc": len(masc),
    }

    CANONICAL_DIR.mkdir(parents=True, exist_ok=True)
    CANONICAL_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Canónico (usado por todos los experimentos): {CANONICAL_JSON}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    review_json = OUT_DIR / "name_gender_lexicon_review.json"
    review_json.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Revisión JSON: {review_json}")

    csv_path = OUT_DIR / "name_gender_lexicon_review.csv"
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("nombre,genero\n")
        for n in fem:
            f.write(f"{n},fem\n")
        for n in masc:
            f.write(f"{n},masc\n")
    print(f"Revisión CSV: {csv_path}")
    print(f"Total: {len(fem)} femeninos, {len(masc)} masculinos. Añade nombres en 'other' si quieres forzar no clasificado.")

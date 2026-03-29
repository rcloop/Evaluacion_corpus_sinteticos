"""
Experimento 01 – Sesgos: Name gender distribution (1.1).
Resultados en: results/sesgos/01

Incluye AMBOS tipos de entidad de nombre:
- NOMBRE_SUJETO_ASISTENCIA (paciente): se usa SEXO_SUJETO_ASISTENCIA del mismo documento
  si existe (Varón/Hombre/M → masculino, Mujer/Femenino/F → femenino); si no, lexicón + heurísticas.
- NOMBRE_PERSONAL_SANITARIO (profesional): primero título en el texto (Dr./Dra., médico/médica,
  enfermero/enfermera, Sr./Sra.); si no hay título, mismo lexicón + heurísticas.

Un solo lexicón (data/sesgos/name_gender_lexicon.json) se usa para ambos. En el JSON puedes tener:
  fem, masc y opcionalmente other (nombres que quieres dejar explícitamente como no clasificados).
Los que no están en el lexicón y no se clasifican por heurísticas cuentan como "other".
Lexicón por defecto: data/sesgos/name_gender_lexicon.json; --lexicon_path para otro archivo.
Generar/actualizar: python src/experimentos/sesgos/export_name_gender_lexicon.py
Etiquetas: solo castellano (NOMBRE_SUJETO_ASISTENCIA, NOMBRE_PERSONAL_SANITARIO).
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "01"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "1_1_name_gender_distribution.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from name_gender_distribution import DEFAULT_TARGET_LABELS, evaluate_name_gender_distribution
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 01 - Name gender distribution")
    parser.add_argument("--corpus_root", required=True, help="Ruta a corpus (con entidades/ y documents/)")
    parser.add_argument("--max_docs", type=int, default=None, help="Máx. archivos (0 = todos)")
    parser.add_argument("--lexicon_path", default=None)
    parser.add_argument("--output_path", default=str(OUTPUT_FILE), help="Ruta del JSON de salida")
    args = parser.parse_args()
    entidades = Path(args.corpus_root) / "entidades"
    max_files = None if (args.max_docs is not None and args.max_docs <= 0) else args.max_docs
    n_files = len(list(entidades.glob("*.json"))) if entidades.is_dir() else 1
    if max_files is not None:
        n_files = min(n_files, max_files)
    print(f"Experimento 01 – Name gender distribution. Corpus: {args.corpus_root} | Documentos: {n_files}")
    result = evaluate_name_gender_distribution(
        annotations_path=str(entidades),
        target_labels=DEFAULT_TARGET_LABELS,
        lexicon_path=args.lexicon_path,
        max_files=max_files,
    )
    out = Path(args.output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Listo. Resultados: {out}")

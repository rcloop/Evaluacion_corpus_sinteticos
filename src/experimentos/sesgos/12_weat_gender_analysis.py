"""
Experimento 12 – Sesgos: WEAT gender analysis.
Resultados en: results/sesgos/12
"""
from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "sesgos" / "12"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "weat_gender_analysis.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from weat_gender_analysis import run_weat_analysis
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 12 - WEAT gender analysis")
    parser.add_argument("--corpus_root", required=True)
    parser.add_argument("--max_docs", type=int, default=None)
    parser.add_argument("--n_permutations", type=int, default=1000)
    parser.add_argument("--window_size", type=int, default=5)
    parser.add_argument(
        "--profession_cooc_window",
        type=int,
        default=None,
        help="Ventana para conteos auxiliares profesión×género; por defecto igual que --window_size.",
    )
    parser.add_argument("--output_path", default=str(OUTPUT_FILE), help="Ruta del JSON de salida")
    args = parser.parse_args()
    documents = Path(args.corpus_root) / "documents"
    max_docs = None if (args.max_docs is not None and args.max_docs <= 0) else args.max_docs
    n_files = len(list(documents.glob("*.txt"))) if documents.is_dir() else 1
    if max_docs is not None:
        n_files = min(n_files, max_docs)
    print(f"Experimento 12 – WEAT gender analysis. Corpus: {args.corpus_root} | Documentos: {n_files}")
    result = run_weat_analysis(
        documents_path=str(documents),
        max_docs=max_docs,
        window_size=args.window_size,
        n_permutations=args.n_permutations,
        profession_gender_cooccurrence_window=args.profession_cooc_window,
    )
    out = Path(args.output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Listo. Resultados: {out}")

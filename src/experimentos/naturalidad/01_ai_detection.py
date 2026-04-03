"""
Experimento 01 – Naturalidad: AI text detection.
Resultados en: results/naturalidad/01
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "results" / "naturalidad" / "01"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "ai_detection_results.json"

LIB_DIR = Path(__file__).resolve().parent / "_lib"
sys.path.insert(0, str(LIB_DIR))

from ai_text_detection import evaluate_ai_detection
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento 01 - AI text detection")
    parser.add_argument("--generated_corpus", required=True, help="Ruta al corpus generado")
    parser.add_argument(
        "--human_corpus",
        default=None,
        help="Ruta a corpus humano (.txt). Si no se pasa, se usa corpus_repo/real_validation_corpus (requerido).",
    )
    parser.add_argument("--output_path", default=str(OUTPUT_FILE))
    parser.add_argument(
        "--sample_size",
        type=int,
        default=None,
        help="Número máximo de documentos por corpus a evaluar (antes de balancear). None o <=0 = todos.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Semilla para muestreo aleatorio reproducible (balance y sampling).",
    )
    parser.add_argument(
        "--no_sanitize_real_chunks",
        action="store_true",
        help="Do not drop real-note paragraphs containing banned valoración scale headers.",
    )
    args = parser.parse_args()
    p = Path(args.generated_corpus)
    n = len(list(p.glob("*.txt"))) if p.is_dir() else 0
    print(f"Experimento 01 – Naturalidad: AI text detection. Corpus generado: {args.generated_corpus} | Documentos: {n}")

    # Default "real/human" corpus: corpus_repo/real_validation_corpus (if present and non-empty).
    # There is NO fallback split: a real corpus is required for meaningful evaluation.
    if args.human_corpus is None:
        candidate = REPO_ROOT / "corpus_repo" / "real_validation_corpus"
        if candidate.is_dir() and any(candidate.glob("*.txt")):
            args.human_corpus = str(candidate)
            print(f"[INFO] Using default human corpus: {args.human_corpus}")
        else:
            print(
                "Error: missing real/human corpus for experiment 01.\n"
                f"Provide --human_corpus <dir_with_txt> or populate: {candidate}",
                file=sys.stderr,
            )
            raise SystemExit(1)
    else:
        hc = Path(args.human_corpus)
        n_h = len(list(hc.glob("*.txt"))) if hc.is_dir() else 0
        if not hc.is_dir() or n_h < 1:
            print(
                f"Error: --human_corpus must be a directory with at least one .txt. Got: {hc}",
                file=sys.stderr,
            )
            raise SystemExit(1)

    evaluate_ai_detection(
        generated_corpus_path=args.generated_corpus,
        human_corpus_path=args.human_corpus,
        output_path=args.output_path,
        sample_size=args.sample_size,
        seed=args.seed,
        sanitize_real_chunks=not args.no_sanitize_real_chunks,
    )
    print(f"Listo. Resultados: {args.output_path}")

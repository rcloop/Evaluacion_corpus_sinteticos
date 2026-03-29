#!/usr/bin/env python3
"""
Ejecuta todos los scripts de experimentos (sesgos, privacidad, naturalidad)
con el corpus indicado y guarda resultados en results/.

Corpus de referencia: corpus_repo/corpus_v1 (corpus sintético anotado con entidades).
Uso: python run_all_experiments.py [--corpus_root corpus_repo/corpus_v1]

Requisitos: pip install -r requirements.txt (incluye PyTorch, transformers y
sentence-transformers para perplexity 02, coherence 06 y memorization semántica).
"""
import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SESGOS = REPO_ROOT / "src" / "experimentos" / "sesgos"
PRIVACIDAD = REPO_ROOT / "src" / "experimentos" / "privacidad"
NATURALIDAD = REPO_ROOT / "src" / "experimentos" / "naturalidad"


def run(script: Path, args: list, cwd: Path = None, timeout: int = 3600) -> subprocess.CompletedProcess:
    cwd = cwd or REPO_ROOT
    cmd = [sys.executable, "-u", str(script)] + args  # -u = unbuffered
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)


# Scripts que suelen tardar mucho: más timeout (4h)
HEAVY_TIMEOUT_SCRIPTS = {
    "02_perplexity.py",
    "03_memorization_detection.py",
    "05_diversity.py",  # corpus completo: Self-BLEU y n-gramas sobre 14k docs
    "06_coherence.py",
    "12_weat_gender_analysis.py",
}


def main():
    p = argparse.ArgumentParser(description="Ejecutar todos los experimentos con el corpus indicado")
    p.add_argument("--corpus_root", type=str, default="corpus_repo/corpus_v1", help="Corpus sintético anotado (documents/ y entidades/). Default: corpus_repo/corpus_v1")
    p.add_argument("--timeout", type=int, default=7200, help="Timeout por script (segundos)")
    p.add_argument("--timeout_heavy", type=int, default=14400, help="Timeout para scripts pesados (perplexity, memorization, WEAT, coherence)")
    p.add_argument("--perplexity_sample_size", type=int, default=5000, help="Máx. docs para perplexity (0 = todos, puede tardar horas)")
    p.add_argument("--memorization_max_docs", type=int, default=5000, help="Máx. docs para memorization (0 = todos)")
    p.add_argument("--full_corpus", action="store_true", help="Equivale a --perplexity_sample_size 0 --memorization_max_docs 0 (sin límites)")
    p.add_argument("--continue_on_error", action="store_true", help="Ante fallo de un experimento, continuar con el siguiente (al final se lista lo fallido)")
    args = p.parse_args()
    if getattr(args, "full_corpus", False):
        args.perplexity_sample_size = 0
        args.memorization_max_docs = 0
    corpus = Path(args.corpus_root).resolve()
    if not corpus.is_dir():
        print(f"Error: corpus_root no existe o no es directorio: {corpus}")
        sys.exit(1)
    docs_dir = corpus / "documents"
    ents_dir = corpus / "entidades"
    if not docs_dir.is_dir():
        print(f"Error: no existe {docs_dir}")
        sys.exit(1)

    def get_timeout(script_name: str) -> int:
        return args.timeout_heavy if script_name in HEAVY_TIMEOUT_SCRIPTS else args.timeout

    failed = []
    # ---- Sesgos 01-12 ----
    for i in range(1, 13):
        scripts = list(SESGOS.glob(f"{i:02d}_*.py"))
        if not scripts:
            continue
        script = scripts[0]
        run_args = ["--corpus_root", str(corpus)]
        to = get_timeout(script.name)
        print(f"\n[Sesgos] {script.name} (timeout {to}s) ...", flush=True)
        r = run(script, run_args, timeout=to)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:800]
            print(f"  FALLO: {err}", flush=True)
            failed.append(("sesgos", script.name, r))
        else:
            print(f"  OK", flush=True)

    # ---- Sesgos 13 (usa JSON de 03, 05, 06) ----
    script13 = SESGOS / "13_diversity_summary.py"
    if script13.exists():
        to = get_timeout(script13.name)
        print(f"\n[Sesgos] {script13.name} (timeout {to}s) ...", flush=True)
        r = run(script13, [], timeout=to)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:800]
            print(f"  FALLO: {err}", flush=True)
            failed.append(("sesgos", script13.name, r))
        else:
            print(f"  OK", flush=True)

    # ---- Privacidad 01, 02, 03 ----
    for name in ["01_attribute_inference.py", "02_membership_inference.py", "03_memorization_detection.py"]:
        script = PRIVACIDAD / name
        if not script.exists():
            continue
        run_args = ["--corpus_path", str(corpus)]
        if "01_" in name or "03_" in name:
            run_args.extend(["--annotations_path", str(ents_dir)])
        if name == "03_memorization_detection.py" and args.memorization_max_docs and args.memorization_max_docs > 0:
            run_args.extend(["--max_docs", str(args.memorization_max_docs)])
        to = get_timeout(script.name)
        print(f"\n[Privacidad] {script.name} (timeout {to}s) ...", flush=True)
        r = run(script, run_args, timeout=to)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:800]
            print(f"  FALLO: {err}", flush=True)
            failed.append(("privacidad", script.name, r))
        else:
            print(f"  OK", flush=True)

    # ---- Naturalidad 01-07 ----
    # 01: --generated_corpus (directorio de textos)
    s01 = NATURALIDAD / "01_ai_detection.py"
    if s01.exists():
        to = get_timeout(s01.name)
        print(f"\n[Naturalidad] {s01.name} (timeout {to}s) ...", flush=True)
        r = run(s01, ["--generated_corpus", str(docs_dir)], timeout=to)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:800]
            print(f"  FALLO: {err}", flush=True)
            failed.append(("naturalidad", s01.name, r))
        else:
            print(f"  OK", flush=True)

    for i in range(2, 8):
        scripts = list(NATURALIDAD.glob(f"{i:02d}_*.py"))
        if not scripts:
            continue
        script = scripts[0]
        if "07_" in script.name:
            real_dir = REPO_ROOT / "corpus_repo" / "real_validation_corpus"
            run_args = ["--generated_corpus", str(docs_dir), "--real_corpus", str(real_dir)]
        else:
            run_args = ["--corpus_path", str(docs_dir)]
        if script.name == "02_perplexity.py" and args.perplexity_sample_size and args.perplexity_sample_size > 0:
            run_args.extend(["--sample_size", str(args.perplexity_sample_size)])
        to = get_timeout(script.name)
        print(f"\n[Naturalidad] {script.name} (timeout {to}s) ...", flush=True)
        r = run(script, run_args, timeout=to)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:800]
            print(f"  FALLO: {err}", flush=True)
            failed.append(("naturalidad", script.name, r))
        else:
            print(f"  OK", flush=True)

    if failed:
        print(f"\n--- {len(failed)} experimento(s) fallaron ---")
        failed_log = REPO_ROOT / "results" / "failed_experiments.txt"
        failed_log.parent.mkdir(parents=True, exist_ok=True)
        with open(failed_log, "w", encoding="utf-8") as f:
            for kind, name, r in failed:
                line = f"{kind} {name}\n"
                print(f"  {line.strip()}")
                f.write(line)
                err = (r.stderr or r.stdout or "").strip()
                if err:
                    f.write(err[:2000] + "\n\n")
        print(f"  Detalle en {failed_log}")
        sys.exit(1)
    print("\n--- Todos los experimentos terminaron correctamente ---")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Re-ejecuta solo los experimentos listados en results/failed_experiments.txt
con el mismo corpus (completo). Úsalo después de corregir el código de los fallidos.

Uso: python run_failed_experiments.py [--corpus_root corpus_repo/corpus_v1]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SESGOS = REPO_ROOT / "src" / "experimentos" / "sesgos"
PRIVACIDAD = REPO_ROOT / "src" / "experimentos" / "privacidad"
NATURALIDAD = REPO_ROOT / "src" / "experimentos" / "naturalidad"
FAILED_LOG = REPO_ROOT / "results" / "failed_experiments.txt"

HEAVY_TIMEOUT_SCRIPTS = {
    "02_perplexity.py",
    "03_memorization_detection.py",
    "12_weat_gender_analysis.py",
    "06_coherence.py",
}


def get_args_for(category: str, script_name: str, corpus: Path, docs_dir: Path, ents_dir: Path) -> list:
    """Build argv for the script (without python -u script)."""
    corpus_str = str(corpus)
    docs_str = str(docs_dir)
    ents_str = str(ents_dir)
    if category == "sesgos":
        if script_name == "13_diversity_summary.py":
            return []
        return ["--corpus_root", corpus_str]
    if category == "privacidad":
        args = ["--corpus_path", corpus_str]
        if script_name in ("01_attribute_inference.py", "03_memorization_detection.py"):
            args.extend(["--annotations_path", ents_str])
        # full corpus: no --max_docs for 03 (use all docs)
        return args
    if category == "naturalidad":
        if script_name == "01_ai_detection.py":
            return ["--generated_corpus", docs_str]
        if script_name == "07_statistical_comparison.py":
            real_dir = REPO_ROOT / "corpus_repo" / "real_validation_corpus"
            return ["--generated_corpus", docs_str, "--real_corpus", str(real_dir)]
        # 02-06
        return ["--corpus_path", docs_str]
    return []


def main():
    p = argparse.ArgumentParser(description="Re-ejecutar experimentos fallidos con corpus completo")
    p.add_argument("--corpus_root", type=str, default="corpus_repo/corpus_v1")
    p.add_argument("--timeout", type=int, default=7200)
    p.add_argument("--timeout_heavy", type=int, default=14400)
    args = p.parse_args()
    corpus = Path(args.corpus_root).resolve()
    docs_dir = corpus / "documents"
    ents_dir = corpus / "entidades"
    if not corpus.is_dir() or not docs_dir.is_dir():
        print(f"Error: corpus no encontrado: {corpus}")
        sys.exit(1)

    if not FAILED_LOG.exists():
        print(f"No hay lista de fallidos: {FAILED_LOG}")
        print("Ejecuta antes: python run_all_experiments.py --corpus_root corpus_repo/corpus_v1 --full_corpus")
        sys.exit(0)

    # Parse "suite script_name" lines (ignore stderr blocks)
    to_rerun = []
    with open(FAILED_LOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            m = re.match(r"^(\w+)\s+(\S+\.py)$", line)
            if m:
                to_rerun.append((m.group(1), m.group(2)))

    if not to_rerun:
        print("No se encontraron líneas 'suite script.py' en failed_experiments.txt")
        sys.exit(0)

    print(f"Re-ejecutando {len(to_rerun)} experimento(s) con corpus completo ...")
    script_dirs = {"sesgos": SESGOS, "privacidad": PRIVACIDAD, "naturalidad": NATURALIDAD}
    failed_again = []
    for category, script_name in to_rerun:
        script_dir = script_dirs.get(category)
        if not script_dir:
            print(f"  Ignorado: categoría desconocida {category}")
            continue
        script = script_dir / script_name
        if not script.exists():
            print(f"  Ignorado: no existe {script}")
            continue
        run_args = get_args_for(category, script_name, corpus, docs_dir, ents_dir)
        timeout = args.timeout_heavy if script_name in HEAVY_TIMEOUT_SCRIPTS else args.timeout
        cmd = [sys.executable, "-u", str(script)] + run_args
        print(f"\n[{category}] {script_name} (timeout {timeout}s) ...", flush=True)
        r = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:500]
            print(f"  FALLO: {err}", flush=True)
            failed_again.append((category, script_name))
        else:
            print(f"  OK", flush=True)

    if failed_again:
        print(f"\n--- Siguen fallando {len(failed_again)} ---")
        for c, n in failed_again:
            print(f"  {c} {n}")
        sys.exit(1)
    print("\n--- Todos los re-ejecutados terminaron correctamente ---")


if __name__ == "__main__":
    main()

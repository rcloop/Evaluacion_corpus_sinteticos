#!/usr/bin/env python3
"""
Ejecuta la suite completa y, si hay fallos, re-ejecuta los experimentos fallidos
con el corpus completo (una ronda de reintento).

Uso: python run_suite_then_retry.py [--corpus_root corpus_repo/corpus_v1] [--full_corpus]
"""
import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
FAILED_LOG = REPO_ROOT / "results" / "failed_experiments.txt"


def main():
    p = argparse.ArgumentParser(description="Suite completa y luego reintento de fallidos")
    p.add_argument("--corpus_root", type=str, default="corpus_repo/corpus_v1")
    p.add_argument("--full_corpus", action="store_true")
    args = p.parse_args()
    argv = [str(REPO_ROOT / "run_all_experiments.py"), "--corpus_root", args.corpus_root]
    if args.full_corpus:
        argv.append("--full_corpus")

    print("=== Ejecutando suite completa ===\n")
    r = subprocess.run([sys.executable, "-u"] + argv, cwd=str(REPO_ROOT))
    if r.returncode != 0 and FAILED_LOG.exists():
        print("\n=== Re-ejecutando experimentos fallidos (corpus completo) ===\n")
        r2 = subprocess.run(
            [sys.executable, "-u", str(REPO_ROOT / "run_failed_experiments.py"), "--corpus_root", args.corpus_root],
            cwd=str(REPO_ROOT),
        )
        sys.exit(r2.returncode)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()

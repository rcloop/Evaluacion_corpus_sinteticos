#!/usr/bin/env python3
"""
Run the full suite; if there are failures, re-run listed failed experiments once.

Usage: python run_suite_then_retry.py [--corpus_root corpus_repo/corpus_v1] [--full_corpus]
"""
import argparse
import subprocess
import sys
from pathlib import Path

from repo_paths import REPO_ROOT

FAILED_LOG = REPO_ROOT / "results" / "failed_experiments.txt"


def main():
    p = argparse.ArgumentParser(description="Full suite then one retry pass for failures")
    p.add_argument("--corpus_root", type=str, default="corpus_repo/corpus_v1")
    p.add_argument("--full_corpus", action="store_true")
    args = p.parse_args()
    argv = [str(REPO_ROOT / "run_all_experiments.py"), "--corpus_root", args.corpus_root]
    if args.full_corpus:
        argv.append("--full_corpus")

    print("=== Running full suite ===\n")
    r = subprocess.run([sys.executable, "-u"] + argv, cwd=str(REPO_ROOT))
    if r.returncode != 0 and FAILED_LOG.exists():
        print("\n=== Re-running failed experiments ===\n")
        r2 = subprocess.run(
            [sys.executable, "-u", str(REPO_ROOT / "run_failed_experiments.py"), "--corpus_root", args.corpus_root],
            cwd=str(REPO_ROOT),
        )
        sys.exit(r2.returncode)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()

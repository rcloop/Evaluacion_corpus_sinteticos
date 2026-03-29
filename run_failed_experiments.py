#!/usr/bin/env python3
"""
Re-run only experiments listed in results/failed_experiments.txt using the same corpus layout.

Usage: python run_failed_experiments.py [--corpus_root corpus_repo/corpus_v1]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

from repo_paths import DEFAULT_REAL_VALIDATION_DOCS_DIR, REPO_ROOT

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
        return args
    if category == "naturalidad":
        if script_name == "01_ai_detection.py":
            return ["--generated_corpus", docs_str]
        if script_name == "07_statistical_comparison.py":
            return ["--generated_corpus", docs_str, "--real_corpus", str(DEFAULT_REAL_VALIDATION_DOCS_DIR)]
        return ["--corpus_path", docs_str]
    return []


def main():
    p = argparse.ArgumentParser(description="Re-run failed experiments from results/failed_experiments.txt")
    p.add_argument("--corpus_root", type=str, default="corpus_repo/corpus_v1")
    p.add_argument("--timeout", type=int, default=7200)
    p.add_argument("--timeout_heavy", type=int, default=14400)
    args = p.parse_args()
    corpus = Path(args.corpus_root).resolve()
    docs_dir = corpus / "documents"
    ents_dir = corpus / "entidades"
    if not corpus.is_dir() or not docs_dir.is_dir():
        print(f"Error: corpus not found: {corpus}")
        sys.exit(1)

    if not FAILED_LOG.exists():
        print(f"No failed list: {FAILED_LOG}")
        print("Run first: python run_all_experiments.py --corpus_root corpus_repo/corpus_v1 --full_corpus")
        sys.exit(0)

    to_rerun = []
    with open(FAILED_LOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            m = re.match(r"^(\w+)\s+(\S+\.py)$", line)
            if m:
                to_rerun.append((m.group(1), m.group(2)))

    if not to_rerun:
        print("No 'suite script.py' lines found in failed_experiments.txt")
        sys.exit(0)

    print(f"Re-running {len(to_rerun)} experiment(s) ...")
    script_dirs = {"sesgos": SESGOS, "privacidad": PRIVACIDAD, "naturalidad": NATURALIDAD}
    failed_again = []
    for category, script_name in to_rerun:
        script_dir = script_dirs.get(category)
        if not script_dir:
            print(f"  Skip: unknown category {category}")
            continue
        script = script_dir / script_name
        if not script.exists():
            print(f"  Skip: missing {script}")
            continue
        run_args = get_args_for(category, script_name, corpus, docs_dir, ents_dir)
        timeout = args.timeout_heavy if script_name in HEAVY_TIMEOUT_SCRIPTS else args.timeout
        cmd = [sys.executable, "-u", str(script)] + run_args
        print(f"\n[{category}] {script_name} (timeout {timeout}s) ...", flush=True)
        r = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:500]
            print(f"  FAIL: {err}", flush=True)
            failed_again.append((category, script_name))
        else:
            print("  OK", flush=True)

    if failed_again:
        print(f"\n--- Still failing: {len(failed_again)} ---")
        for c, n in failed_again:
            print(f"  {c} {n}")
        sys.exit(1)
    print("\n--- All re-runs finished successfully ---")


if __name__ == "__main__":
    main()

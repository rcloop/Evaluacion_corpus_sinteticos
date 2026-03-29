#!/usr/bin/env python3
"""
Run every experiment script (bias, privacy, naturalness) on the given corpus; write under results/.

Default corpus: corpus_repo/corpus_v1 (synthetic, with entidades/).
Usage: python run_all_experiments.py [--corpus_root corpus_repo/corpus_v1]

Requires: pip install -r requirements.txt (PyTorch, transformers, sentence-transformers for
perplexity 02, coherence 06, semantic memorization).
"""
import argparse
import subprocess
import sys
from pathlib import Path

from repo_paths import DEFAULT_REAL_VALIDATION_DOCS_DIR, REPO_ROOT

SESGOS = REPO_ROOT / "src" / "experimentos" / "sesgos"
PRIVACIDAD = REPO_ROOT / "src" / "experimentos" / "privacidad"
NATURALIDAD = REPO_ROOT / "src" / "experimentos" / "naturalidad"


def run(script: Path, args: list, cwd: Path = None, timeout: int = 3600) -> subprocess.CompletedProcess:
    cwd = cwd or REPO_ROOT
    cmd = [sys.executable, "-u", str(script)] + args
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)


HEAVY_TIMEOUT_SCRIPTS = {
    "02_perplexity.py",
    "03_memorization_detection.py",
    "05_diversity.py",
    "06_coherence.py",
    "12_weat_gender_analysis.py",
}


def main():
    p = argparse.ArgumentParser(description="Run all experiments on the given corpus")
    p.add_argument(
        "--corpus_root",
        type=str,
        default="corpus_repo/corpus_v1",
        help="Synthetic annotated corpus (documents/ + entidades/). Default: corpus_repo/corpus_v1",
    )
    p.add_argument("--timeout", type=int, default=7200, help="Timeout per script (seconds)")
    p.add_argument(
        "--timeout_heavy",
        type=int,
        default=14400,
        help="Timeout for heavy scripts (perplexity, memorization, WEAT, coherence)",
    )
    p.add_argument(
        "--perplexity_sample_size",
        type=int,
        default=5000,
        help="Max docs for perplexity (0 = all; can take hours)",
    )
    p.add_argument(
        "--memorization_max_docs",
        type=int,
        default=5000,
        help="Max docs for memorization (0 = all)",
    )
    p.add_argument(
        "--full_corpus",
        action="store_true",
        help="Same as --perplexity_sample_size 0 --memorization_max_docs 0",
    )
    p.add_argument(
        "--continue_on_error",
        action="store_true",
        help="On failure, continue with the next experiment (failed list at end)",
    )
    args = p.parse_args()
    if getattr(args, "full_corpus", False):
        args.perplexity_sample_size = 0
        args.memorization_max_docs = 0
    corpus = Path(args.corpus_root).resolve()
    if not corpus.is_dir():
        print(f"Error: corpus_root is not a directory: {corpus}")
        sys.exit(1)
    docs_dir = corpus / "documents"
    ents_dir = corpus / "entidades"
    if not docs_dir.is_dir():
        print(f"Error: missing {docs_dir}")
        sys.exit(1)

    def get_timeout(script_name: str) -> int:
        return args.timeout_heavy if script_name in HEAVY_TIMEOUT_SCRIPTS else args.timeout

    failed = []
    for i in range(1, 13):
        scripts = list(SESGOS.glob(f"{i:02d}_*.py"))
        if not scripts:
            continue
        script = scripts[0]
        run_args = ["--corpus_root", str(corpus)]
        to = get_timeout(script.name)
        print(f"\n[Bias] {script.name} (timeout {to}s) ...", flush=True)
        r = run(script, run_args, timeout=to)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:800]
            print(f"  FAIL: {err}", flush=True)
            failed.append(("sesgos", script.name, r))
        else:
            print("  OK", flush=True)

    script13 = SESGOS / "13_diversity_summary.py"
    if script13.exists():
        to = get_timeout(script13.name)
        print(f"\n[Bias] {script13.name} (timeout {to}s) ...", flush=True)
        r = run(script13, [], timeout=to)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:800]
            print(f"  FAIL: {err}", flush=True)
            failed.append(("sesgos", script13.name, r))
        else:
            print("  OK", flush=True)

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
        print(f"\n[Privacy] {script.name} (timeout {to}s) ...", flush=True)
        r = run(script, run_args, timeout=to)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:800]
            print(f"  FAIL: {err}", flush=True)
            failed.append(("privacidad", script.name, r))
        else:
            print("  OK", flush=True)

    s01 = NATURALIDAD / "01_ai_detection.py"
    if s01.exists():
        to = get_timeout(s01.name)
        print(f"\n[Naturalness] {s01.name} (timeout {to}s) ...", flush=True)
        r = run(s01, ["--generated_corpus", str(docs_dir)], timeout=to)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:800]
            print(f"  FAIL: {err}", flush=True)
            failed.append(("naturalidad", s01.name, r))
        else:
            print("  OK", flush=True)

    real_dir = DEFAULT_REAL_VALIDATION_DOCS_DIR
    for i in range(2, 8):
        scripts = list(NATURALIDAD.glob(f"{i:02d}_*.py"))
        if not scripts:
            continue
        script = scripts[0]
        if "07_" in script.name:
            run_args = ["--generated_corpus", str(docs_dir), "--real_corpus", str(real_dir)]
        else:
            run_args = ["--corpus_path", str(docs_dir)]
        if script.name == "02_perplexity.py" and args.perplexity_sample_size and args.perplexity_sample_size > 0:
            run_args.extend(["--sample_size", str(args.perplexity_sample_size)])
        to = get_timeout(script.name)
        print(f"\n[Naturalness] {script.name} (timeout {to}s) ...", flush=True)
        r = run(script, run_args, timeout=to)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:800]
            print(f"  FAIL: {err}", flush=True)
            failed.append(("naturalidad", script.name, r))
        else:
            print("  OK", flush=True)

    if failed:
        print(f"\n--- {len(failed)} experiment(s) failed ---")
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
        print(f"  Details: {failed_log}")
        sys.exit(1)
    print("\n--- All experiments finished successfully ---")


if __name__ == "__main__":
    main()

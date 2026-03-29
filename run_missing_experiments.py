#!/usr/bin/env python3
"""
Run only experiments that do not yet have a complete result file.
All suites use corpus_repo/corpus_v1 (documents/ + entidades/) by default.
Experiment 07 compares generated texts to the real-reference directory (default: data/real_validation_corpus).

Usage:
  python run_missing_experiments.py [--corpus_root corpus_repo/corpus_v1] [--full_corpus]
  python run_missing_experiments.py --force  # re-run all (overwrite)

  --corpus_root: synthetic annotated corpus. Default: corpus_repo/corpus_v1
  --corpus_docs: documents directory only (if set without corpus_root, only naturalness 01–06 run)
  --real_corpus: real-reference .txt directory for exp 07. Default: data/real_validation_corpus
  --full_corpus: no sampling (sample_size=0 / max_docs=0 where applicable)
  --force: re-run even if a non-empty result exists
"""
import argparse
import subprocess
import sys
from pathlib import Path

from repo_paths import DEFAULT_REAL_VALIDATION_DOCS_DIR, REPO_ROOT, count_txt_documents_under_dir

RESULTS = REPO_ROOT / "results"
SESGOS = REPO_ROOT / "src" / "experimentos" / "sesgos"
PRIVACIDAD = REPO_ROOT / "src" / "experimentos" / "privacidad"
NATURALIDAD = REPO_ROOT / "src" / "experimentos" / "naturalidad"

HEAVY_TIMEOUT = 14400
NORMAL_TIMEOUT = 7200

SESGO_RESULTS = [
    ("sesgos/01/1_1_name_gender_distribution.json", "01_name_gender_distribution.py", lambda c: ["--corpus_root", str(c["corpus_root"])]),
    ("sesgos/02/1_2_role_profession_gender_bias.json", "02_role_profession_gender_bias.py", lambda c: ["--corpus_root", str(c["corpus_root"])]),
    ("sesgos/03/1_3_geographic_toponymic_bias.json", "03_geographic_toponymic_bias.py", lambda c: ["--corpus_root", str(c["corpus_root"])]),
    ("sesgos/04/1_4_age_distribution.json", "04_age_distribution.py", lambda c: ["--corpus_root", str(c["corpus_root"])]),
    ("sesgos/05/1_5_institution_bias.json", "05_institution_bias.py", lambda c: ["--corpus_root", str(c["corpus_root"])]),
    ("sesgos/06/1_6_diagnosis_condition_bias.json", "06_diagnosis_condition_bias.py", lambda c: ["--corpus_root", str(c["corpus_root"])]),
    ("sesgos/07/intersectional_corpus_bias.json", "07_intersectional_corpus_bias.py", lambda c: ["--corpus_root", str(c["corpus_root"])]),
    ("sesgos/08/diagnosis_demography_bias.json", "08_diagnosis_demography_bias.py", lambda c: ["--corpus_root", str(c["corpus_root"])]),
    ("sesgos/09/gender_target_proportion.json", "09_gender_target_proportion.py", lambda c: ["--corpus_root", str(c["corpus_root"])]),
    ("sesgos/10/age_reference_comparison.json", "10_age_reference_comparison.py", lambda c: ["--corpus_root", str(c["corpus_root"])]),
    ("sesgos/11/coverage_completeness.json", "11_coverage_completeness.py", lambda c: ["--corpus_root", str(c["corpus_root"])]),
    ("sesgos/12/weat_gender_analysis.json", "12_weat_gender_analysis.py", lambda c: ["--corpus_root", str(c["corpus_root"])]),
    ("sesgos/13/diversity_summary.json", "13_diversity_summary.py", lambda c: []),
]

PRIVACIDAD_RESULTS = [
    ("privacidad/01/attribute_inference.json", "01_attribute_inference.py", lambda c: ["--corpus_path", str(c["corpus_root"]), "--annotations_path", str(c["ents_dir"])]),
    ("privacidad/02/membership_inference.json", "02_membership_inference.py", lambda c: ["--corpus_path", str(c["corpus_root"])]),
    ("privacidad/03/memorization_detection.json", "03_memorization_detection.py", lambda c: ["--corpus_path", str(c["corpus_root"]), "--annotations_path", str(c["ents_dir"])]),
]

NATURALIDAD_RESULTS = [
    ("naturalidad/01/ai_detection_results.json", "01_ai_detection.py", lambda c: ["--generated_corpus", str(c["docs_dir"])]),
    ("naturalidad/02/perplexity_results.json", "02_perplexity.py", lambda c: ["--corpus_path", str(c["docs_dir"])] + (["--sample_size", "0"] if c["full_corpus"] else [])),
    ("naturalidad/03/vocabulary_richness_results.json", "03_vocabulary_richness.py", lambda c: ["--corpus_path", str(c["docs_dir"])] + (["--sample_size", "0"] if c["full_corpus"] else [])),
    ("naturalidad/04/readability_results.json", "04_readability.py", lambda c: ["--corpus_path", str(c["docs_dir"])] + (["--sample_size", "0"] if c["full_corpus"] else [])),
    ("naturalidad/05/diversity_results.json", "05_diversity.py", lambda c: ["--corpus_path", str(c["docs_dir"])] + (["--sample_size", "0"] if c["full_corpus"] else [])),
    ("naturalidad/06/coherence_results.json", "06_coherence.py", lambda c: ["--corpus_path", str(c["docs_dir"])] + (["--sample_size", "0"] if c["full_corpus"] else [])),
    ("naturalidad/07/statistical_comparison_results.json", "07_statistical_comparison.py", lambda c: ["--generated_corpus", str(c["docs_dir"]), "--real_corpus", str(c["real_corpus_path"])] + (["--sample_size", "0"] if c["full_corpus"] else [])),
]


def run(script: Path, args: list, timeout: int) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-u", str(script)] + args
    return subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=timeout)


def result_complete(result_path: Path) -> bool:
    return result_path.is_file() and result_path.stat().st_size > 0


def main():
    default_real = DEFAULT_REAL_VALIDATION_DOCS_DIR.relative_to(REPO_ROOT).as_posix()
    p = argparse.ArgumentParser(description="Run experiments that lack a complete result file.")
    p.add_argument(
        "--corpus_root",
        type=str,
        default="corpus_repo/corpus_v1",
        help="Synthetic annotated corpus (documents/ + entidades/). Default: corpus_repo/corpus_v1",
    )
    p.add_argument(
        "--corpus_docs",
        type=str,
        default=None,
        help="Documents directory only. If set without corpus_root, only naturalness runs.",
    )
    p.add_argument(
        "--real_corpus",
        type=str,
        default=default_real,
        help=f"Real-reference .txt directory for exp 07. Default: {default_real}",
    )
    p.add_argument("--full_corpus", action="store_true", help="No sampling (full data)")
    p.add_argument("--force", action="store_true", help="Re-run even if result exists")
    p.add_argument("--timeout", type=int, default=NORMAL_TIMEOUT)
    p.add_argument("--timeout_heavy", type=int, default=HEAVY_TIMEOUT)
    args = p.parse_args()

    corpus_root = Path(args.corpus_root).resolve() if args.corpus_root else None
    corpus_docs = Path(args.corpus_docs).resolve() if args.corpus_docs else None
    real_corpus = Path(args.real_corpus).resolve() if args.real_corpus else None
    if real_corpus is not None and real_corpus == corpus_root:
        real_corpus = None

    if corpus_docs is not None and not corpus_docs.is_dir():
        print(f"Error: corpus_docs is not a directory: {corpus_docs}", file=sys.stderr)
        sys.exit(1)

    if corpus_root is not None and not corpus_root.is_dir():
        print(f"Error: corpus_root is not a directory: {corpus_root}", file=sys.stderr)
        sys.exit(1)

    if corpus_root is not None:
        docs_dir = (corpus_root / "documents") if (corpus_root / "documents").is_dir() else corpus_root
        ents_dir = corpus_root / "entidades"
        has_entidades = ents_dir.is_dir()
    else:
        docs_dir = corpus_docs
        ents_dir = Path("/nonexistent")
        has_entidades = False

    if docs_dir is None:
        print("Error: pass --corpus_root or --corpus_docs", file=sys.stderr)
        sys.exit(1)

    real_corpus_path = real_corpus
    skipped_07_logged = False

    def real_validation_txt_count() -> tuple[Path, int]:
        p = real_corpus_path if real_corpus_path is not None else DEFAULT_REAL_VALIDATION_DOCS_DIR
        n = count_txt_documents_under_dir(p) if p.is_dir() else 0
        return p, n

    cfg = {
        "docs_dir": docs_dir,
        "ents_dir": ents_dir,
        "corpus_root": corpus_root or docs_dir,
        "full_corpus": args.full_corpus,
        "has_entidades": has_entidades,
        "real_corpus_path": real_corpus_path,
    }

    heavy = {"02_perplexity.py", "03_memorization_detection.py", "12_weat_gender_analysis.py", "06_coherence.py"}

    def get_timeout(script_name: str) -> int:
        return args.timeout_heavy if script_name in heavy else args.timeout

    to_run = []

    if corpus_root is not None and has_entidades:
        for rel, script_name, build in SESGO_RESULTS:
            result_path = RESULTS / rel
            if args.force or not result_complete(result_path):
                script = SESGOS / script_name
                if script.exists():
                    to_run.append(("sesgos", script, build(cfg), result_path, script_name))
    else:
        if corpus_root is None:
            print("Skipping bias: need --corpus_root with documents/ and entidades/")
        else:
            print("Skipping bias: entidades/ missing under corpus_root")

    if corpus_root is not None and has_entidades:
        for rel, script_name, build in PRIVACIDAD_RESULTS:
            result_path = RESULTS / rel
            if args.force or not result_complete(result_path):
                script = PRIVACIDAD / script_name
                if script.exists():
                    to_run.append(("privacidad", script, build(cfg), result_path, script_name))

    for rel, script_name, build in NATURALIDAD_RESULTS:
        if "07_statistical" in script_name:
            _rp, _n = real_validation_txt_count()
            if _n < 1:
                if not skipped_07_logged:
                    print(
                        f"Skipping naturalidad/07: need at least one .txt under {_rp} "
                        "(populate with your real validation export).",
                        flush=True,
                    )
                    skipped_07_logged = True
                continue
        result_path = RESULTS / rel
        if args.force or not result_complete(result_path):
            script = NATURALIDAD / script_name
            if script.exists():
                to_run.append(("naturalidad", script, build(cfg), result_path, script_name))

    if not to_run:
        print("No pending experiments (all results present). Use --force to re-run.")
        return

    print(f"Running {len(to_run)} experiment(s) (full_corpus={args.full_corpus})...\n")
    failed = []
    for kind, script, run_args, result_path, script_name in to_run:
        to = get_timeout(script_name)
        print(f"[{kind}] {script_name} (timeout {to}s) ...", flush=True)
        r = run(script, run_args, timeout=to)
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:600]
            print(f"  FAIL: {err}", flush=True)
            failed.append((kind, script_name, r))
        else:
            print(f"  OK -> {result_path}", flush=True)

    if failed:
        print(f"\n--- {len(failed)} experiment(s) failed ---")
        for k, n, _ in failed:
            print(f"  {k} {n}")
        sys.exit(1)
    print("\n--- All pending experiments finished successfully ---")


if __name__ == "__main__":
    main()

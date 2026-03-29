"""Canonical filesystem paths for this repository (single source of truth)."""
from __future__ import annotations

from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parent

# Default synthetic corpus (documents/ + entidades/)
DEFAULT_SYNTHETIC_CORPUS_ROOT = REPO_ROOT / "corpus_repo" / "corpus_v1"

# Real-reference texts for naturalness experiment 07 (directory of .txt files).
# Not tracked in git (.gitignore): populate corpus_repo/real_validation_corpus locally, e.g.:
#   python corpus_repo/export_real_validation_corpus.py
# (default output dir) or copy your .txt files there.
DEFAULT_REAL_VALIDATION_DOCS_DIR = REPO_ROOT / "corpus_repo" / "real_validation_corpus"


def list_txt_documents_under_dir(directory: Path) -> List[Path]:
    """
    All .txt files under directory (recursive), case-insensitive extension.
    Same discovery for experiment 07, pytest fixture, and scripts/run_missing_experiments.py.
    """
    if not directory.is_dir():
        return []
    return sorted(
        p
        for p in directory.rglob("*")
        if p.is_file() and p.suffix.lower() == ".txt"
    )


def count_txt_documents_under_dir(directory: Path) -> int:
    return len(list_txt_documents_under_dir(directory))

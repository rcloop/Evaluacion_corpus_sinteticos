"""Canonical filesystem paths for this repository (single source of truth)."""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

# Default synthetic corpus (documents/ + entidades/)
DEFAULT_SYNTHETIC_CORPUS_ROOT = REPO_ROOT / "corpus_repo" / "corpus_v1"

# Real-reference texts for naturalness experiment 07 (directory of .txt files).
# Not tracked in git: copy or export your own files, e.g.:
#   python corpus_repo/export_real_validation_corpus.py --output_dir data/real_validation_corpus
DEFAULT_REAL_VALIDATION_DOCS_DIR = REPO_ROOT / "data" / "real_validation_corpus"

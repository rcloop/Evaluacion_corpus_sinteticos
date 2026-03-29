"""
Pytest fixtures for experiment tests (privacy, bias, naturalness).

A single minimal corpus (`corpus_mini`) backs all suites. Structure:
`test/data/corpus_mini` with `documents/` (`.txt`) and `entidades/` (`.json`).
Experiment 07 (statistical comparison) uses the same real-reference directory
as production runs (`data/real_validation_corpus`); the test is skipped if it
is missing or has no `.txt` files.
"""
import sys
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
from repo_paths import DEFAULT_REAL_VALIDATION_DOCS_DIR


@pytest.fixture(scope="session")
def repo_root():
    return REPO_ROOT


@pytest.fixture(scope="session")
def corpus_mini_path(repo_root):
    """Minimal corpus root for bias, privacy, and naturalness (documents/ + entidades/)."""
    p = repo_root / "test" / "data" / "corpus_mini"
    assert p.exists(), f"Missing test data: {p}"
    return p


@pytest.fixture(scope="session")
def corpus_mini_documents_path(corpus_mini_path):
    """`.txt` documents under corpus_mini; used by naturalness 01–06."""
    p = corpus_mini_path / "documents"
    assert p.exists(), f"Missing corpus_mini documents: {p}"
    return p


@pytest.fixture(scope="session")
def real_validation_corpus_path(repo_root):
    """Same path as experiment 07 default; skipped when no real .txt files are present."""
    p = DEFAULT_REAL_VALIDATION_DOCS_DIR
    n = len(list(p.glob("*.txt"))) if p.is_dir() else 0
    if not p.is_dir() or n < 1:
        pytest.skip(
            f"Experiment 07 needs {p} with at least one .txt (found {n}). "
            "Copy or export your real validation texts there; nothing is auto-generated."
        )
    return p


@pytest.fixture(scope="session")
def corpus_v1_path(repo_root):
    """Synthetic v1 root (`corpus_repo/corpus_v1`). Optional; full experiments outside pytest."""
    p = repo_root / "corpus_repo" / "corpus_v1"
    if not p.exists():
        pytest.skip(f"Corpus v1 not found: {p}")
    return p


@pytest.fixture(scope="session")
def corpus_v1_documents_path(corpus_v1_path):
    """`documents/` under v1. Optional; not used by unified smoke tests."""
    p = corpus_v1_path / "documents"
    if not p.exists():
        pytest.skip(f"Corpus v1 documents not found: {p}")
    return p


@pytest.fixture(scope="session")
def experiments_sesgos_path(repo_root):
    return repo_root / "src" / "experimentos" / "sesgos"


@pytest.fixture(scope="session")
def experiments_privacidad_path(repo_root):
    return repo_root / "src" / "experimentos" / "privacidad"


@pytest.fixture(scope="session")
def experiments_naturalidad_path(repo_root):
    return repo_root / "src" / "experimentos" / "naturalidad"


@pytest.fixture
def tmp_results_dir(tmp_path, repo_root):
    """Temporary output dir so runs do not touch the real `results/` tree."""
    return tmp_path

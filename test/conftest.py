"""
Pytest fixtures for experiment tests (privacy, bias, naturalness).

A single minimal corpus (`corpus_mini`) backs all suites. Structure:
`test/data/corpus_mini` with `documents/` (`.txt`) and `entidades/` (`.json`).
Experiment 07 (statistical comparison) also needs a small real-style reference
corpus: `test/data/real_corpus_mini`.
"""
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


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
def real_corpus_mini_path(repo_root):
    """Small real-style corpus for experiment 07 (generated vs real). Required like other fixtures."""
    p = repo_root / "test" / "data" / "real_corpus_mini"
    assert p.exists(), (
        f"Missing real_corpus_mini: {p}. "
        "Create with: python scripts/generate_real_validation_corpus.py "
        "--output_dir test/data/real_corpus_mini --num_docs 10"
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

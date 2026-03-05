"""
Fixtures para tests de experimentos.
Rutas a datos mínimos (corpus_mini: documents + entidades; corpus_naturalidad: textos).
"""
import pytest
from pathlib import Path

# Raíz del repo (test/ está en la raíz)
REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def repo_root():
    return REPO_ROOT


@pytest.fixture(scope="session")
def corpus_mini_path(repo_root):
    """Corpus mínimo con documents/ y entidades/ para sesgos y privacidad."""
    p = repo_root / "test" / "data" / "corpus_mini"
    assert p.exists(), f"Test data no encontrado: {p}"
    return p


@pytest.fixture(scope="session")
def corpus_naturalidad_path(repo_root):
    """Directorio con .txt para experimentos de naturalidad."""
    p = repo_root / "test" / "data" / "corpus_naturalidad"
    assert p.exists(), f"Test data no encontrado: {p}"
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
    """Directorio temporal para resultados (evita ensuciar results/ real)."""
    return tmp_path

"""
Fixtures para tests de experimentos (privacidad, sesgos, naturalidad).

Un solo corpus mínimo (corpus_mini) para todos los tests: sesgos, privacidad y naturalidad.
Estructura: test/data/corpus_mini con documents/ (.txt) y entidades/ (.json).
El experimento 07 (comparación estadística) necesita un corpus real de referencia: se usa
test/data/real_corpus_mini (versión mini del corpus real corporativo).
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
    """Corpus mínimo único para sesgos, privacidad y naturalidad (documents/ + entidades/)."""
    p = repo_root / "test" / "data" / "corpus_mini"
    assert p.exists(), f"Test data no encontrado: {p}"
    return p


@pytest.fixture(scope="session")
def corpus_mini_documents_path(corpus_mini_path):
    """Directorio de documentos .txt del corpus_mini (corpus_mini/documents). Usado por naturalidad 01-06."""
    p = corpus_mini_path / "documents"
    assert p.exists(), f"Corpus mini documents no encontrado: {p}"
    return p


@pytest.fixture(scope="session")
def real_corpus_mini_path(repo_root):
    """Corpus real mini para el test 07 (comparación estadística generado vs real). Requerido como el resto de datos de test."""
    p = repo_root / "test" / "data" / "real_corpus_mini"
    assert p.exists(), (
        f"Real corpus mini no encontrado: {p}. "
        "Crear con: python scripts/generate_real_validation_corpus.py --output_dir test/data/real_corpus_mini --num_docs 10"
    )
    return p


@pytest.fixture(scope="session")
def corpus_v1_path(repo_root):
    """Raíz del corpus sintético v1 (corpus_repo/corpus_v1). Opcional; solo para ejecutar experimentos completos fuera de tests."""
    p = repo_root / "corpus_repo" / "corpus_v1"
    if not p.exists():
        pytest.skip(f"Corpus v1 no encontrado: {p}")
    return p


@pytest.fixture(scope="session")
def corpus_v1_documents_path(corpus_v1_path):
    """Directorio de documentos .txt del corpus v1. Solo para uso opcional (no usado por los tests unificados)."""
    p = corpus_v1_path / "documents"
    if not p.exists():
        pytest.skip(f"Corpus v1 documents no encontrado: {p}")
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

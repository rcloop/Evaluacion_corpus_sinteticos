"""
Verificación de que todas las dependencias (requirements) están instaladas y completas.

Corresponde a: requirements.txt (raíz) y a la estructura de experimentos (_lib).
Ejecutar: pytest test/test_requirements_complete.py -v
"""
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Paquetes requeridos: nombre para pip/requirements.txt -> nombre del módulo al importar
REQUIRED_PACKAGES = [
    ("numpy", "numpy"),
    ("scipy", "scipy"),
    ("matplotlib", "matplotlib"),
    ("tqdm", "tqdm"),
    ("scikit-learn", "sklearn"),
    ("nltk", "nltk"),
    ("torch", "torch"),
    ("transformers", "transformers"),
    ("sentence-transformers", "sentence_transformers"),
    ("pytest", "pytest"),
]


@pytest.mark.parametrize("package_name,import_name", REQUIRED_PACKAGES)
def test_requirement_importable(package_name: str, import_name: str) -> None:
    """Cada paquete listado en requirements debe ser importable."""
    if package_name == "nltk":
        try:
            __import__(import_name)
        except ImportError:
            pytest.skip(
                "nltk no instalado (opcional para algunos experimentos). "
                "Instalar con: pip install nltk"
            )
        return
    try:
        __import__(import_name)
    except ImportError as e:
        pytest.fail(
            f"Falta el paquete '{package_name}'. "
            f"Instalar con: pip install {package_name}\n"
            f"Error: {e}"
        )


def test_python_version() -> None:
    """Python >= 3.8 requerido para compatibilidad con torch/transformers."""
    assert sys.version_info >= (3, 8), (
        "Se requiere Python >= 3.8. Actual: {}.{}".format(
            sys.version_info.major, sys.version_info.minor
        )
    )


# --- Estructura _lib (experimentos autocontenidos) ---

SESGOS_LIB_MODULES = [
    "name_gender_distribution",
    "role_profession_gender_bias",
    "geographic_toponymic_bias",
    "age_distribution",
    "institution_bias",
    "diagnosis_condition_bias",
    "intersectional_corpus_bias",
    "diagnosis_demography_bias",
    "gender_target_proportion",
    "age_reference_comparison",
    "coverage_completeness",
    "weat_gender_analysis",
    "diversity_summary",
]

PRIVACIDAD_LIB_MODULES = [
    "attribute_inference",
    "membership_inference",
    "nearest_neighbor_memorization",
    "meddocan_label_mapping",
]

NATURALIDAD_LIB_MODULES = [
    "ai_text_detection",
    "coherence",
    "diversity_metrics",
    "perplexity",
    "readability",
    "statistical_comparison",
    "vocabulary_richness",
]


def test_sesgos_lib_complete() -> None:
    """Todos los módulos de sesgos/_lib deben existir."""
    lib_dir = REPO_ROOT / "src" / "experimentos" / "sesgos" / "_lib"
    assert lib_dir.is_dir(), f"No existe {lib_dir}"
    missing = [m + ".py" for m in SESGOS_LIB_MODULES if not (lib_dir / f"{m}.py").is_file()]
    assert not missing, f"Faltan en sesgos/_lib: {missing}"


def test_privacidad_lib_complete() -> None:
    """Todos los módulos de privacidad/_lib deben existir."""
    lib_dir = REPO_ROOT / "src" / "experimentos" / "privacidad" / "_lib"
    assert lib_dir.is_dir(), f"No existe {lib_dir}"
    missing = [m + ".py" for m in PRIVACIDAD_LIB_MODULES if not (lib_dir / f"{m}.py").is_file()]
    assert not missing, f"Faltan en privacidad/_lib: {missing}"


def test_naturalidad_lib_complete() -> None:
    """Todos los módulos de naturalidad/_lib deben existir."""
    lib_dir = REPO_ROOT / "src" / "experimentos" / "naturalidad" / "_lib"
    assert lib_dir.is_dir(), f"No existe {lib_dir}"
    missing = [m + ".py" for m in NATURALIDAD_LIB_MODULES if not (lib_dir / f"{m}.py").is_file()]
    assert not missing, f"Faltan en naturalidad/_lib: {missing}"


def test_requirements_file_exists() -> None:
    """Debe existir requirements.txt en la raíz."""
    req = REPO_ROOT / "requirements.txt"
    assert req.is_file(), f"No existe {req}. Crear con las dependencias del proyecto."


def test_requirements_txt_matches_required_packages() -> None:
    """Cada paquete de REQUIRED_PACKAGES debe estar declarado en requirements.txt (evita desincronización)."""
    req_file = REPO_ROOT / "requirements.txt"
    assert req_file.is_file(), "requirements.txt debe existir"
    content = req_file.read_text(encoding="utf-8")
    # Líneas que declaran paquete: empiezan con nombre (letras/guiones) hasta el primer comparador o fin
    declared = set()
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Primera palabra (nombre del paquete pip)
        parts = line.replace(">", " ").replace("=", " ").replace("<", " ").split()
        if parts:
            declared.add(parts[0].lower())
    required_names = {pkg_name for pkg_name, _ in REQUIRED_PACKAGES}
    missing = required_names - declared
    assert not missing, (
        f"En requirements.txt faltan: {sorted(missing)}. "
        "Añadir estas dependencias o actualizar REQUIRED_PACKAGES en test_requirements_complete.py."
    )

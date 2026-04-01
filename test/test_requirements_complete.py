"""
Ensure declared requirements are importable and `_lib/` layouts are complete.

See root `requirements.txt` and `src/experimentos/*/_lib/`.
Run: pytest test/test_requirements_complete.py -v
"""
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

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
    """Every pinned package should import."""
    if package_name == "nltk":
        try:
            __import__(import_name)
        except ImportError:
            pytest.skip(
                "nltk not installed (optional for some experiments). "
                "Install with: pip install nltk"
            )
        return
    try:
        __import__(import_name)
    except ImportError as e:
        pytest.fail(
            f"Missing package '{package_name}'. "
            f"Install with: pip install {package_name}\n"
            f"Error: {e}"
        )


def test_python_version() -> None:
    """Python >= 3.8 for torch/transformers compatibility."""
    assert sys.version_info >= (3, 8), (
        "Python >= 3.8 required. Current: {}.{}".format(
            sys.version_info.major, sys.version_info.minor
        )
    )


SESGOS_LIB_MODULES = [
    "name_gender_distribution",
    "role_profession_gender_bias",
    "geographic_toponymic_bias",
    "age_distribution",
    "institution_bias",
    "intersectional_corpus_bias",
    "gender_target_proportion",
    "age_reference_comparison",
    "coverage_completeness",
    "weat_gender_analysis",
    "diversity_summary",
]

PRIVACIDAD_LIB_MODULES = [
    "attribute_inference",
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
    """All expected `sesgos/_lib` modules exist."""
    lib_dir = REPO_ROOT / "src" / "experimentos" / "sesgos" / "_lib"
    assert lib_dir.is_dir(), f"Missing {lib_dir}"
    missing = [m + ".py" for m in SESGOS_LIB_MODULES if not (lib_dir / f"{m}.py").is_file()]
    assert not missing, f"Missing in sesgos/_lib: {missing}"


def test_privacidad_lib_complete() -> None:
    """All expected `privacidad/_lib` modules exist."""
    lib_dir = REPO_ROOT / "src" / "experimentos" / "privacidad" / "_lib"
    assert lib_dir.is_dir(), f"Missing {lib_dir}"
    missing = [m + ".py" for m in PRIVACIDAD_LIB_MODULES if not (lib_dir / f"{m}.py").is_file()]
    assert not missing, f"Missing in privacidad/_lib: {missing}"


def test_naturalidad_lib_complete() -> None:
    """All expected `naturalidad/_lib` modules exist."""
    lib_dir = REPO_ROOT / "src" / "experimentos" / "naturalidad" / "_lib"
    assert lib_dir.is_dir(), f"Missing {lib_dir}"
    missing = [m + ".py" for m in NATURALIDAD_LIB_MODULES if not (lib_dir / f"{m}.py").is_file()]
    assert not missing, f"Missing in naturalidad/_lib: {missing}"


def test_requirements_file_exists() -> None:
    """Root requirements file must exist."""
    req = REPO_ROOT / "requirements.txt"
    assert req.is_file(), f"Missing {req}. Add project dependencies there."


def test_requirements_txt_matches_required_packages() -> None:
    """Each REQUIRED_PACKAGES entry must appear in requirements.txt."""
    req_file = REPO_ROOT / "requirements.txt"
    assert req_file.is_file(), "requirements.txt must exist"
    content = req_file.read_text(encoding="utf-8")
    declared = set()
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.replace(">", " ").replace("=", " ").replace("<", " ").split()
        if parts:
            declared.add(parts[0].lower())
    required_names = {pkg_name for pkg_name, _ in REQUIRED_PACKAGES}
    missing = required_names - declared
    assert not missing, (
        f"requirements.txt is missing: {sorted(missing)}. "
        "Add them or update REQUIRED_PACKAGES in test_requirements_complete.py."
    )

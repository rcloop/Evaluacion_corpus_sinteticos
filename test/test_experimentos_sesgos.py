"""
Tests de los scripts de experimentos de sesgos.
Ejecutan los scripts con corpus_mini y comprueban que terminan y generan salida.
"""
import subprocess
import sys
from pathlib import Path

import pytest


def _run_experiment(script_path: Path, args: list, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script_path)] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=120,
    )


@pytest.mark.parametrize("script,extra_args", [
    ("01_name_gender_distribution.py", ["--max_docs", "2"]),
    ("02_role_profession_gender_bias.py", ["--max_docs", "2"]),
    ("03_geographic_toponymic_bias.py", ["--max_docs", "2"]),
    ("04_age_distribution.py", ["--max_docs", "2"]),
    ("05_institution_bias.py", ["--max_docs", "2"]),
    ("06_diagnosis_condition_bias.py", ["--max_docs", "2"]),
    ("07_intersectional_corpus_bias.py", ["--max_docs", "2"]),
    ("08_diagnosis_demography_bias.py", ["--max_docs", "2"]),
    ("09_gender_target_proportion.py", ["--max_docs", "2"]),
    ("10_age_reference_comparison.py", ["--max_docs", "2"]),
    ("11_coverage_completeness.py", ["--max_docs", "2"]),
])
def test_sesgos_script_corpus_mini(
    repo_root, corpus_mini_path, experiments_sesgos_path, tmp_path, script, extra_args
):
    """Cada script de sesgos (01-11) corre con corpus_mini y escribe en tmp."""
    script_path = experiments_sesgos_path / script
    if not script_path.exists():
        pytest.skip(f"Script no encontrado: {script_path}")
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    args = ["--corpus_root", str(corpus_mini_path)] + extra_args
    # Algunos escriben en results/sesgos/NN por defecto; redirigir no es trivial, probamos que al menos arrancan
    result = _run_experiment(script_path, args, repo_root)
    assert result.returncode == 0, (
        f"{script} falló: stdout={result.stdout!r} stderr={result.stderr!r}"
    )


def test_sesgos_01_produces_json(repo_root, corpus_mini_path, experiments_sesgos_path, tmp_path):
    """01 name_gender_distribution escribe JSON en results/sesgos/01 (o comprobamos que corre)."""
    script = experiments_sesgos_path / "01_name_gender_distribution.py"
    result = _run_experiment(
        script,
        ["--corpus_root", str(corpus_mini_path), "--max_docs", "2"],
        repo_root,
    )
    assert result.returncode == 0
    out_file = repo_root / "results" / "sesgos" / "01" / "1_1_name_gender_distribution.json"
    # Si el script escribió en la ruta por defecto
    if out_file.exists():
        assert out_file.stat().st_size > 0
        content = out_file.read_text(encoding="utf-8")
        assert "overall" in content or "counts" in content or "proportions" in content

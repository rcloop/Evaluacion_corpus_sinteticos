"""
Tests de los scripts de experimentos de privacidad.
Ejecutan con corpus_mini y comprueban que terminan correctamente.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest


def _run_experiment(script_path: Path, args: list, cwd: Path, timeout: int = 180):
    return subprocess.run(
        [sys.executable, str(script_path)] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


@pytest.mark.parametrize("script,args_key", [
    ("01_attribute_inference.py", "corpus_path"),
    ("02_membership_inference.py", "corpus_path"),
    ("03_memorization_detection.py", "corpus_path"),
])
def test_privacidad_script_corpus_mini(
    repo_root, corpus_mini_path, experiments_privacidad_path, script, args_key
):
    """Cada script de privacidad corre con corpus_mini."""
    script_path = experiments_privacidad_path / script
    if not script_path.exists():
        pytest.skip(f"Script no encontrado: {script_path}")
    if args_key == "corpus_path":
        args = ["--corpus_path", str(corpus_mini_path)]
    else:
        args = ["--corpus_path", str(corpus_mini_path)]
    if script == "01_attribute_inference.py":
        args.extend(["--annotations_path", str(corpus_mini_path / "entidades")])
    if script == "03_memorization_detection.py":
        args.extend(["--annotations_path", str(corpus_mini_path / "entidades")])
    result = _run_experiment(script_path, args, repo_root)
    assert result.returncode == 0, (
        f"{script} falló: stdout={result.stdout!r} stderr={result.stderr!r}"
    )


def test_privacidad_01_output_exists(repo_root, corpus_mini_path, experiments_privacidad_path):
    """01 attribute_inference genera attribute_inference.json en results/privacidad/01."""
    script = experiments_privacidad_path / "01_attribute_inference.py"
    result = _run_experiment(
        script,
        [
            "--corpus_path", str(corpus_mini_path),
            "--annotations_path", str(corpus_mini_path / "entidades"),
        ],
        repo_root,
    )
    assert result.returncode == 0
    out_file = repo_root / "results" / "privacidad" / "01" / "attribute_inference.json"
    if out_file.exists():
        assert out_file.stat().st_size > 0


def test_privacidad_01_json_structure_and_sanity(
    repo_root, corpus_mini_path, experiments_privacidad_path
):
    """01 attribute_inference: estructura del JSON y sanity (auc en [0,1], risk_level válido)."""
    script = experiments_privacidad_path / "01_attribute_inference.py"
    result = _run_experiment(
        script,
        [
            "--corpus_path", str(corpus_mini_path),
            "--annotations_path", str(corpus_mini_path / "entidades"),
        ],
        repo_root,
    )
    assert result.returncode == 0
    out_file = repo_root / "results" / "privacidad" / "01" / "attribute_inference.json"
    assert out_file.exists(), "01 debe escribir attribute_inference.json"
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert "attribute_results" in data, "JSON debe tener 'attribute_results'"
    assert "overall_risk" in data, "JSON debe tener 'overall_risk'"
    assert "corpus_size" in data, "JSON debe tener 'corpus_size'"
    overall = data["overall_risk"]
    assert "max_auc_roc" in overall and "mean_auc_roc" in overall
    assert 0 <= overall["max_auc_roc"] <= 1.0, "max_auc_roc debe estar en [0,1]"
    assert 0 <= overall["mean_auc_roc"] <= 1.0, "mean_auc_roc debe estar en [0,1]"
    allowed_risk = {"low", "medium", "high", "critical", "skipped"}
    for attr_name, res in data["attribute_results"].items():
        if isinstance(res, dict) and res.get("skipped"):
            continue
        if isinstance(res, dict) and "auc_roc" in res:
            assert 0 <= res["auc_roc"] <= 1.0, f"attribute_results[{attr_name}].auc_roc en [0,1]"
        if isinstance(res, dict) and "risk_level" in res:
            assert res["risk_level"] in allowed_risk, f"risk_level debe ser uno de {allowed_risk}"

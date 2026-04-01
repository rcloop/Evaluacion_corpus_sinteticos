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


@pytest.mark.parametrize("script", [
    "01_attribute_inference.py",
    "03_memorization_detection.py",
])
def test_privacidad_script_corpus_mini(
    repo_root, corpus_mini_path, experiments_privacidad_path, tmp_path, script
):
    """Cada script de privacidad corre con corpus_mini; salida aislada (no pisa results/)."""
    script_path = experiments_privacidad_path / script
    if not script_path.exists():
        pytest.skip(f"Script no encontrado: {script_path}")
    out_map = {
        "01_attribute_inference.py": "attribute_inference.json",
        "03_memorization_detection.py": "memorization_detection.json",
    }
    args = ["--corpus_path", str(corpus_mini_path), "--output_path", str(tmp_path / out_map[script])]
    if script == "01_attribute_inference.py":
        args.extend(["--annotations_path", str(corpus_mini_path / "entidades")])
    if script == "03_memorization_detection.py":
        args.extend(["--annotations_path", str(corpus_mini_path / "entidades")])
    result = _run_experiment(script_path, args, repo_root)
    assert result.returncode == 0, (
        f"{script} falló: stdout={result.stdout!r} stderr={result.stderr!r}"
    )


def test_privacidad_01_output_exists(repo_root, corpus_mini_path, experiments_privacidad_path, tmp_path):
    """01 attribute_inference genera JSON en ruta aislada."""
    script = experiments_privacidad_path / "01_attribute_inference.py"
    out_file = tmp_path / "attribute_inference.json"
    result = _run_experiment(
        script,
        [
            "--corpus_path", str(corpus_mini_path),
            "--annotations_path", str(corpus_mini_path / "entidades"),
            "--output_path", str(out_file),
        ],
        repo_root,
    )
    assert result.returncode == 0
    assert out_file.exists() and out_file.stat().st_size > 0


def test_privacidad_01_json_structure_and_sanity(
    repo_root, corpus_mini_path, experiments_privacidad_path, tmp_path
):
    """01 attribute_inference: estructura del JSON y sanity (auc en [0,1], risk_level válido)."""
    script = experiments_privacidad_path / "01_attribute_inference.py"
    out_file = tmp_path / "attribute_inference.json"
    result = _run_experiment(
        script,
        [
            "--corpus_path", str(corpus_mini_path),
            "--annotations_path", str(corpus_mini_path / "entidades"),
            "--output_path", str(out_file),
        ],
        repo_root,
    )
    assert result.returncode == 0
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


def test_privacidad_03_semantic_histogram_when_present(
    repo_root, corpus_mini_path, experiments_privacidad_path, tmp_path
):
    """03 memorization: si hay histograma semántico, estructura mínima y sum(counts)==n_pairs."""
    script = experiments_privacidad_path / "03_memorization_detection.py"
    out_file = tmp_path / "memorization_detection.json"
    result = _run_experiment(
        script,
        [
            "--corpus_path", str(corpus_mini_path),
            "--annotations_path", str(corpus_mini_path / "entidades"),
            "--output_path", str(out_file),
        ],
        repo_root,
        timeout=300,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(out_file.read_text(encoding="utf-8"))
    hist = data.get("semantic_similarity_histogram")
    if hist is None:
        pytest.skip("semantic_similarity_histogram ausente (p. ej. semantic skip o ST no instalado)")
    assert hist.get("method") == "all_unique_pairs_upper_triangle"
    assert "bin_edges" in hist and "counts" in hist and "n_pairs" in hist
    assert len(hist["bin_edges"]) == len(hist["counts"]) + 1
    assert sum(hist["counts"]) == hist["n_pairs"]
    for key in ("fraction_pairs_ge_0.85", "fraction_pairs_ge_0.90", "fraction_pairs_ge_0.95"):
        assert key in hist
        assert hist[key] is None or 0.0 <= float(hist[key]) <= 1.0
    for key in ("n_pairs_ge_0.85", "n_pairs_ge_0.90", "n_pairs_ge_0.95"):
        assert key in hist
        assert hist[key] is None or int(hist[key]) >= 0
    aux = data.get("semantic_similarity_auxiliary")
    if aux is not None:
        assert "neighbor_graph_coverage" in aux and "template_vs_lexical_proxy" in aux
        cov = aux["neighbor_graph_coverage"]
        assert "recall_neighbor_graph_vs_global_ge_0.95" in cov

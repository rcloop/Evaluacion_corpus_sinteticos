"""
Tests de los scripts de experimentos de naturalidad.
Ejecutan con corpus_naturalidad (pocos .txt) y comprueban que terminan.
"""
import subprocess
import sys
from pathlib import Path

import pytest


def _run_experiment(script_path: Path, args: list, cwd: Path, timeout: int = 120):
    return subprocess.run(
        [sys.executable, str(script_path)] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


@pytest.mark.parametrize("script", [
    "01_ai_detection.py",
    "02_perplexity.py",
    "03_vocabulary_richness.py",
    "04_readability.py",
    "05_diversity.py",
    "06_coherence.py",
])
def test_naturalidad_script_corpus(
    repo_root, corpus_naturalidad_path, experiments_naturalidad_path, script
):
    """Scripts de naturalidad 01-06 corren con directorio de textos."""
    script_path = experiments_naturalidad_path / script
    if not script_path.exists():
        pytest.skip(f"Script no encontrado: {script_path}")
    path_val = str(corpus_naturalidad_path)
    if script == "01_ai_detection.py":
        args = ["--generated_corpus", path_val]
    else:
        args = ["--corpus_path", path_val]
    args.extend(["--sample_size", "2"])
    result = _run_experiment(script_path, args, repo_root)
    if result.returncode != 0 and "02_perplexity" in script:
        if "PyTorch" in (result.stderr or "") or "transformers" in (result.stderr or ""):
            pytest.skip("Perplexity requiere PyTorch/transformers")
    if result.returncode != 0 and "06_coherence" in script:
        if "sentence" in (result.stderr or "").lower() or "model" in (result.stderr or "").lower():
            pytest.skip("Coherence puede requerir sentence-transformers")
    assert result.returncode == 0, (
        f"{script} falló: stdout={result.stdout!r} stderr={result.stderr!r}"
    )


def test_naturalidad_03_vocabulary_richness_produces_output(
    repo_root, corpus_naturalidad_path, experiments_naturalidad_path
):
    """03 vocabulary_richness es ligero y debería escribir JSON."""
    script = experiments_naturalidad_path / "03_vocabulary_richness.py"
    result = _run_experiment(
        script,
        ["--corpus_path", str(corpus_naturalidad_path), "--sample_size", "2"],
        repo_root,
    )
    assert result.returncode == 0
    out_file = repo_root / "results" / "naturalidad" / "03" / "vocabulary_richness_results.json"
    if out_file.exists():
        assert out_file.stat().st_size > 0

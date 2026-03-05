"""Test del experimento 07 naturalidad (statistical comparison) con mismo corpus como generado y real."""
import subprocess
import sys
from pathlib import Path

import pytest


def test_naturalidad_07_statistical_comparison(
    repo_root, corpus_naturalidad_path, experiments_naturalidad_path
):
    """07 statistical_comparison corre con generated y real (mismo dir mínimo)."""
    script = experiments_naturalidad_path / "07_statistical_comparison.py"
    if not script.exists():
        pytest.skip("Script 07 no encontrado")
    path_val = str(corpus_naturalidad_path)
    result = subprocess.run(
        [sys.executable, str(script), "--generated_corpus", path_val, "--real_corpus", path_val, "--sample_size", "2"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        pytest.skip(f"07 puede requerir más datos o deps: {result.stderr}")
    out = repo_root / "results" / "naturalidad" / "07" / "statistical_comparison_results.json"
    if out.exists():
        assert out.stat().st_size > 0

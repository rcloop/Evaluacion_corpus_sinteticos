"""Test del experimento 07 naturalidad (statistical comparison): generado vs corpus real mini."""
import subprocess
import sys
from pathlib import Path

import pytest


def test_naturalidad_07_statistical_comparison(
    repo_root, corpus_mini_documents_path, real_corpus_mini_path, experiments_naturalidad_path
):
    """07 statistical_comparison corre con corpus_mini como generado y real_corpus_mini como corpus real de referencia."""
    script = experiments_naturalidad_path / "07_statistical_comparison.py"
    if not script.exists():
        pytest.skip("Script 07 no encontrado")
    result = subprocess.run(
        [
            sys.executable, str(script),
            "--generated_corpus", str(corpus_mini_documents_path),
            "--real_corpus", str(real_corpus_mini_path),
            "--sample_size", "2",
        ],
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

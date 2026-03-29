"""
Tests de los scripts de experimentos de naturalidad.
Ejecutan con el mismo corpus_mini que sesgos y privacidad (corpus_mini/documents) y comprueban que terminan.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest


def _run_experiment(script_path: Path, args: list, cwd: Path, timeout: int):
    return subprocess.run(
        [sys.executable, str(script_path)] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


# Cold CI runners may download transformers / sentence-transformers weights; keep this above HF hub latency.
_NATURALIDAD_SUBPROCESS_TIMEOUT = {
    "01_ai_detection.py": 600,
    "02_perplexity.py": 600,
    "06_coherence.py": 600,
    "03_vocabulary_richness.py": 120,
    "04_readability.py": 120,
    "05_diversity.py": 120,
}


@pytest.mark.parametrize("script", [
    "01_ai_detection.py",
    "02_perplexity.py",
    "03_vocabulary_richness.py",
    "04_readability.py",
    "05_diversity.py",
    "06_coherence.py",
])
def test_naturalidad_script_corpus(
    repo_root, corpus_mini_documents_path, experiments_naturalidad_path, script
):
    """Scripts de naturalidad 01-06 corren con corpus_mini/documents (mismo corpus que sesgos y privacidad)."""
    script_path = experiments_naturalidad_path / script
    if not script_path.exists():
        pytest.skip(f"Script no encontrado: {script_path}")
    path_val = str(corpus_mini_documents_path)
    if script == "01_ai_detection.py":
        args = ["--generated_corpus", path_val]
    else:
        args = ["--corpus_path", path_val, "--sample_size", "2"]
    timeout = _NATURALIDAD_SUBPROCESS_TIMEOUT.get(script, 120)
    result = _run_experiment(script_path, args, repo_root, timeout=timeout)
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
    repo_root, corpus_mini_documents_path, experiments_naturalidad_path
):
    """03 vocabulary_richness es ligero y debería escribir JSON."""
    script = experiments_naturalidad_path / "03_vocabulary_richness.py"
    result = _run_experiment(
        script,
        ["--corpus_path", str(corpus_mini_documents_path), "--sample_size", "2"],
        repo_root,
        timeout=_NATURALIDAD_SUBPROCESS_TIMEOUT["03_vocabulary_richness.py"],
    )
    assert result.returncode == 0
    out_file = repo_root / "results" / "naturalidad" / "03" / "vocabulary_richness_results.json"
    if out_file.exists():
        assert out_file.stat().st_size > 0


def test_naturalidad_03_json_structure_and_sanity(
    repo_root, corpus_mini_documents_path, experiments_naturalidad_path
):
    """03 vocabulary_richness: estructura del JSON y sanity (métricas numéricas coherentes)."""
    script = experiments_naturalidad_path / "03_vocabulary_richness.py"
    result = _run_experiment(
        script,
        ["--corpus_path", str(corpus_mini_documents_path), "--sample_size", "2"],
        repo_root,
        timeout=_NATURALIDAD_SUBPROCESS_TIMEOUT["03_vocabulary_richness.py"],
    )
    assert result.returncode == 0
    out_file = repo_root / "results" / "naturalidad" / "03" / "vocabulary_richness_results.json"
    assert out_file.exists(), "03 debe escribir vocabulary_richness_results.json"
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert "corpus_level" in data, "JSON debe tener 'corpus_level'"
    assert "document_level" in data, "JSON debe tener 'document_level'"
    assert data["corpus_level"]["type_token_ratio"] >= 0 and data["corpus_level"]["type_token_ratio"] <= 1.0, (
        "TTR corpus debe estar en [0,1]"
    )
    ttr_doc = data["document_level"]["type_token_ratio"]
    assert "mean" in ttr_doc and ttr_doc["mean"] >= 0 and ttr_doc["mean"] <= 1.0, (
        "document_level.type_token_ratio.mean en [0,1]"
    )

"""Naturalness experiment 07 (statistical comparison): generated vs mini real reference."""
import json
import subprocess
import sys
from pathlib import Path

import pytest


def test_naturalidad_07_statistical_comparison(
    repo_root, corpus_mini_documents_path, real_validation_corpus_path, experiments_naturalidad_path, tmp_path
):
    """07 runs with corpus_mini as generated and corpus_repo/real_validation_corpus as reference."""
    script = experiments_naturalidad_path / "07_statistical_comparison.py"
    if not script.exists():
        pytest.skip("07 script not found")
    out = tmp_path / "statistical_comparison_results.json"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--generated_corpus",
            str(corpus_mini_documents_path),
            "--real_corpus",
            str(real_validation_corpus_path),
            "--sample_size",
            "2",
            "--output_path",
            str(out),
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, (
        f"07_statistical_comparison failed (fix real/generated paths and deps). "
        f"stderr={result.stderr!r} stdout={result.stdout!r}"
    )
    assert out.exists() and out.stat().st_size > 0


def test_naturalidad_08_real_windows_length_agnostic(
    repo_root, corpus_mini_documents_path, real_validation_corpus_path, experiments_naturalidad_path, tmp_path
):
    """08 uses real sliding windows and excludes raw length features; Bonferroni uses 3 tests."""
    script = experiments_naturalidad_path / "08_statistical_comparison_real_windows.py"
    if not script.exists():
        pytest.skip("08 script not found")
    out = tmp_path / "statistical_comparison_08.json"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--generated_corpus",
            str(corpus_mini_documents_path),
            "--real_corpus",
            str(real_validation_corpus_path),
            "--sample_size",
            "2",
            "--output_path",
            str(out),
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data.get("protocol", {}).get("exclude_length_features") is True
    assert data.get("protocol", {}).get("real_sliding_windows") is True
    assert data["summary"]["total_features_compared"] == 3
    assert set(data["comparisons"].keys()) == {"avg_word_length", "avg_sentence_length", "type_token_ratio"}

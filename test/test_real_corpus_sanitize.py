"""Unit tests for real-note chunk filtering (valoración boilerplate)."""
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LIB = REPO_ROOT / "src" / "experimentos" / "naturalidad" / "_lib"
sys.path.insert(0, str(LIB))

from real_corpus_sanitize import (  # noqa: E402
    filter_banned_paragraph_chunks,
    sanitize_real_note_text,
)


def test_filter_drops_paragraph_with_aloracion_enfermo_critico():
    text = "Cabecera\n\naloración enfermo crítico\n\nEvolución clínica con datos."
    out = filter_banned_paragraph_chunks(text)
    assert "aloración enfermo crítico" not in out
    assert "Evolución clínica" in out
    assert "Cabecera" in out


def test_filter_drops_valoracion_hospitalizacion_general():
    text = "A\n\nValoración Hospitalización General\n\nB paragraph"
    out = filter_banned_paragraph_chunks(text)
    assert "Valoración Hospitalización General" not in out
    assert "B paragraph" in out


def test_sanitize_disabled_returns_unchanged():
    raw = "aloración enfermo crítico sola"
    assert sanitize_real_note_text(raw, enabled=False) == raw


def test_fixed_word_windows_non_overlapping():
    from length_norm import fixed_word_windows

    text = " ".join([f"w{i}" for i in range(25)])
    wins = fixed_word_windows(text, window_size=10, stride=10)
    assert len(wins) == 2
    assert wins[0].startswith("w0")
    assert "w19" in wins[1]

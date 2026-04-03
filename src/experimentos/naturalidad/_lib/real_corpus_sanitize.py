#!/usr/bin/env python3
"""
Remove boilerplate / scale blocks from real-hospital note exports before comparison.

Splits text into paragraph-like chunks (blank-line separated) and drops any chunk whose
normalized text contains banned substrings (e.g. standardized valoración headers).
"""

from __future__ import annotations

import re
import unicodedata
from typing import List, Sequence, Tuple

# User-requested headers (OCR often drops leading "V" → "aloración…").
BANNED_SUBSTRINGS_NORMALIZED: Tuple[str, ...] = (
    "aloracion enfermo critico",
    "valoracion enfermo critico",
    "aloracion hospitalizacion general",
    "valoracion hospitalizacion general",
    "aloracion hospitalización general",
    "valoracion hospitalización general",
)


def _normalize_for_match(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def _chunk_contains_banned(norm_chunk: str, banned: Sequence[str]) -> bool:
    return any(b in norm_chunk for b in banned)


def filter_banned_paragraph_chunks(text: str) -> str:
    """
    Split on blank-line boundaries; omit chunks that match any banned substring.
    If nothing remains, drop individual lines containing a ban, then rejoin.
    If still empty, return original text (caller may log).
    """
    if not (text or "").strip():
        return text
    original = text
    paragraphs = re.split(r"\n\s*\n+", text.strip())
    kept: List[str] = []
    for p in paragraphs:
        if not p.strip():
            continue
        norm_p = _normalize_for_match(p)
        if not _chunk_contains_banned(norm_p, BANNED_SUBSTRINGS_NORMALIZED):
            kept.append(p.strip())

    if kept:
        return "\n\n".join(kept)

    lines = text.splitlines()
    kept_lines: List[str] = []
    for line in lines:
        norm_line = _normalize_for_match(line)
        if not _chunk_contains_banned(norm_line, BANNED_SUBSTRINGS_NORMALIZED):
            kept_lines.append(line)
    out = "\n".join(kept_lines).strip()
    return out if out else original


def sanitize_real_note_text(text: str, enabled: bool = True) -> str:
    if not enabled or not (text or "").strip():
        return text
    return filter_banned_paragraph_chunks(text)

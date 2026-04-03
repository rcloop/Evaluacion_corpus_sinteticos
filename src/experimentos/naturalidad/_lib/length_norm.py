#!/usr/bin/env python3
"""
Word-level helpers aligned with `statistical_comparison.extract_features` tokenization.
Used for sliding-window alignment (mean synthetic length **W**, `truncate_to_word_limit`,
`expand_real_corpus_windows`) in experiments **02** and **08**.
"""

from __future__ import annotations

from typing import List

try:
    from nltk.tokenize import word_tokenize

    _NLTK = True
    try:
        import nltk

        try:
            nltk.data.find("tokenizers/punkt_tab")
        except LookupError:
            nltk.download("punkt_tab", quiet=True)
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt", quiet=True)
    except Exception:
        pass
except ImportError:
    _NLTK = False


def simple_tokenize(text: str) -> List[str]:
    import re

    text = re.sub(r"[^\w\s]", " ", text)
    return text.lower().split()


def tokenize_words(text: str) -> List[str]:
    """Match `statistical_comparison.extract_features` word list."""
    if not (text or "").strip():
        return []
    if _NLTK:
        return word_tokenize(text.lower())
    return simple_tokenize(text)


def truncate_to_word_limit(text: str, max_words: int) -> str:
    """Keep the first `max_words` tokens (same tokenizer as corpus statistics).

    If the text has at most `max_words` tokens, it is returned unchanged (no padding).
    """
    if max_words <= 0:
        return (text or "").strip()
    words = tokenize_words(text)
    if len(words) <= max_words:
        return (text or "").strip()
    return " ".join(words[:max_words])


def mean_word_count(texts: List[str]) -> float:
    """Mean token count (same tokenizer as corpus statistics)."""
    import numpy as np

    counts = [len(tokenize_words(t)) for t in texts if t and t.strip()]
    if not counts:
        return 0.0
    return float(np.mean(np.array(counts, dtype=np.float64)))


def fixed_word_windows(text: str, window_size: int, stride: int) -> List[str]:
    """
    Non-overlapping or sliding windows of exactly `window_size` tokens.
    If len(tokenize_words(text)) < window_size, returns [].
    """
    if window_size <= 0:
        return []
    words = tokenize_words(text)
    if len(words) < window_size:
        return []
    if stride <= 0:
        stride = window_size
    out: List[str] = []
    start = 0
    while start + window_size <= len(words):
        out.append(" ".join(words[start : start + window_size]))
        start += stride
    return out


def expand_real_corpus_windows(
    real_texts: List[str],
    window_size: int,
    stride: int,
) -> List[str]:
    """Flatten fixed windows from each real document."""
    expanded: List[str] = []
    for t in real_texts:
        expanded.extend(fixed_word_windows(t, window_size, stride))
    return expanded


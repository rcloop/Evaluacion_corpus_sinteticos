#!/usr/bin/env python3
"""
Readability Evaluation
Calculates Spanish readability indices (INFLESZ, Fernández Huerta, etc.)
"""

import json
import os
import re
from pathlib import Path
from typing import List, Dict
import argparse

try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    NLTK_AVAILABLE = True
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("[INFO] Downloading NLTK punkt tokenizer...")
        nltk.download('punkt', quiet=True)
except ImportError:
    NLTK_AVAILABLE = False
    print("[WARNING] NLTK not available. Using simple tokenization.")


def load_corpus(corpus_path: str) -> List[str]:
    """Load corpus texts from JSON or directory of text files."""
    texts = []
    
    if os.path.isdir(corpus_path):
        for file_path in Path(corpus_path).glob("*.txt"):
            with open(file_path, 'r', encoding='utf-8') as f:
                texts.append(f.read().strip())
    elif corpus_path.endswith('.json'):
        with open(corpus_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        texts.append(item.get('text', item.get('content', '')))
                    else:
                        texts.append(str(item))
            else:
                texts = [data.get('text', '')] if isinstance(data, dict) else []
    else:
        raise ValueError(f"Unsupported file format: {corpus_path}")
    
    return texts


def simple_tokenize(text: str) -> List[str]:
    """Simple tokenization if NLTK not available."""
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.lower().split()


def count_syllables_spanish(word: str) -> int:
    """Count syllables in Spanish word."""
    word = word.lower().strip()
    if not word:
        return 1
    
    # Remove accents for counting
    word = word.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    
    vowels = 'aeiou'
    syllable_count = 0
    prev_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            syllable_count += 1
        prev_was_vowel = is_vowel
    
    # Handle diphthongs and triphthongs (simplified)
    # Adjust for common patterns
    if 'ui' in word or 'iu' in word:
        syllable_count = max(1, syllable_count - 1)
    
    return max(1, syllable_count)


def calculate_inflesz(text: str) -> float:
    """
    Calculate INFLESZ (Spanish readability index).
    INFLESZ = 206.835 - (1.015 * ASL) - (84.6 * ASW)
    Where:
    - ASL = Average Sentence Length (words per sentence)
    - ASW = Average Syllables per Word
    """
    if NLTK_AVAILABLE:
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
    else:
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        words = simple_tokenize(text)
    
    if not sentences or not words:
        return 0.0
    
    # Average Sentence Length (ASL)
    asl = len(words) / len(sentences) if sentences else 0.0
    
    # Average Syllables per Word (ASW)
    total_syllables = sum(count_syllables_spanish(word) for word in words)
    asw = total_syllables / len(words) if words else 0.0
    
    # INFLESZ formula
    inflesz = 206.835 - (1.015 * asl) - (84.6 * asw)
    
    return inflesz


def calculate_fernandez_huerta(text: str) -> float:
    """
    Calculate Fernández Huerta readability index.
    FH = 206.84 - (0.60 * ASL) - (1.02 * ASW)
    """
    if NLTK_AVAILABLE:
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
    else:
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        words = simple_tokenize(text)
    
    if not sentences or not words:
        return 0.0
    
    asl = len(words) / len(sentences) if sentences else 0.0
    total_syllables = sum(count_syllables_spanish(word) for word in words)
    asw = total_syllables / len(words) if words else 0.0
    
    fh = 206.84 - (0.60 * asl) - (1.02 * asw)
    
    return fh


def interpret_inflesz(score: float) -> str:
    """Interpret INFLESZ score."""
    if score >= 80:
        return "Muy fácil"
    elif score >= 65:
        return "Fácil"
    elif score >= 50:
        return "Normal"
    elif score >= 30:
        return "Difícil"
    else:
        return "Muy difícil"


def evaluate_readability(
    corpus_path: str,
    output_path: str = "readability_results.json",
    sample_size: int = None
) -> Dict:
    """
    Evaluate readability of corpus.
    
    Args:
        corpus_path: Path to corpus
        output_path: Output file path
        sample_size: Number of documents to evaluate (None = all)
    
    Returns:
        Dictionary with readability statistics
    """
    print("=" * 80)
    print("READABILITY EVALUATION")
    print("=" * 80)
    
    # Load corpus
    print(f"\n1. Loading corpus: {corpus_path}")
    texts = load_corpus(corpus_path)
    print(f"   Loaded {len(texts)} documents")
    
    # Sample if requested
    if sample_size and sample_size < len(texts):
        import random
        random.seed(42)
        texts = random.sample(texts, sample_size)
        print(f"   Sampling {sample_size} documents for evaluation")
    
    # Calculate metrics for each document
    print(f"\n2. Calculating readability metrics...")
    inflesz_scores = []
    fernandez_huerta_scores = []
    
    for i, text in enumerate(texts):
        if (i + 1) % 500 == 0:
            print(f"   Processed {i + 1}/{len(texts)} documents...")
        
        inflesz = calculate_inflesz(text)
        fh = calculate_fernandez_huerta(text)
        
        if inflesz > 0:
            inflesz_scores.append(inflesz)
        if fh > 0:
            fernandez_huerta_scores.append(fh)
    
    # Statistics
    import numpy as np
    
    results = {
        'total_documents': len(texts),
        'inflesz': {
            'mean': float(np.mean(inflesz_scores)) if inflesz_scores else 0.0,
            'median': float(np.median(inflesz_scores)) if inflesz_scores else 0.0,
            'std': float(np.std(inflesz_scores)) if inflesz_scores else 0.0,
            'min': float(np.min(inflesz_scores)) if inflesz_scores else 0.0,
            'max': float(np.max(inflesz_scores)) if inflesz_scores else 0.0,
            'interpretation': interpret_inflesz(np.mean(inflesz_scores)) if inflesz_scores else "N/A"
        },
        'fernandez_huerta': {
            'mean': float(np.mean(fernandez_huerta_scores)) if fernandez_huerta_scores else 0.0,
            'median': float(np.median(fernandez_huerta_scores)) if fernandez_huerta_scores else 0.0,
            'std': float(np.std(fernandez_huerta_scores)) if fernandez_huerta_scores else 0.0,
            'min': float(np.min(fernandez_huerta_scores)) if fernandez_huerta_scores else 0.0,
            'max': float(np.max(fernandez_huerta_scores)) if fernandez_huerta_scores else 0.0
        }
    }
    
    print(f"\n3. Results:")
    print(f"   INFLESZ - Mean: {results['inflesz']['mean']:.2f} ({results['inflesz']['interpretation']})")
    print(f"   INFLESZ - Median: {results['inflesz']['median']:.2f}")
    print(f"   Fernández Huerta - Mean: {results['fernandez_huerta']['mean']:.2f}")
    print(f"   Fernández Huerta - Median: {results['fernandez_huerta']['median']:.2f}")
    
    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to: {output_path}")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Readability Evaluation")
    parser.add_argument(
        "--corpus_path",
        type=str,
        required=True,
        help="Path to corpus (JSON or directory)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="readability_results.json",
        help="Output file path"
    )
    parser.add_argument(
        "--sample_size",
        type=int,
        default=None,
        help="Number of documents to evaluate (None = all)"
    )
    
    args = parser.parse_args()
    
    evaluate_readability(
        args.corpus_path,
        args.output,
        args.sample_size
    )


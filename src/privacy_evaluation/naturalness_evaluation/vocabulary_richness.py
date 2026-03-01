#!/usr/bin/env python3
"""
Vocabulary Richness Evaluation
Measures lexical diversity and vocabulary usage patterns.
"""

import json
import os
import re
import math
from pathlib import Path
from typing import List, Dict
from collections import Counter
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
    # Remove punctuation and split
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.lower().split()


def count_syllables(word: str) -> int:
    """Simple syllable counter for Spanish."""
    word = word.lower()
    if len(word) <= 3:
        return 1
    
    vowels = 'aeiouáéíóúü'
    syllable_count = 0
    prev_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            syllable_count += 1
        prev_was_vowel = is_vowel
    
    return max(1, syllable_count)


def calculate_ttr(text: str) -> float:
    """Calculate Type-Token Ratio."""
    if NLTK_AVAILABLE:
        tokens = word_tokenize(text.lower())
    else:
        tokens = simple_tokenize(text)
    
    if not tokens:
        return 0.0
    
    unique_types = len(set(tokens))
    total_tokens = len(tokens)
    
    return unique_types / total_tokens if total_tokens > 0 else 0.0


def calculate_yules_k(text: str) -> float:
    """Calculate Yule's K (measure of vocabulary richness)."""
    if NLTK_AVAILABLE:
        tokens = word_tokenize(text.lower())
    else:
        tokens = simple_tokenize(text)
    
    if not tokens:
        return 0.0
    
    # Count word frequencies
    word_counts = Counter(tokens)
    total_tokens = len(tokens)
    
    # Calculate Yule's K
    s1 = sum(word_counts.values())  # Total tokens
    s2 = sum(count * count for count in word_counts.values())  # Sum of squares
    
    if s1 == 0:
        return 0.0
    
    k = 10000 * (s2 - s1) / (s1 * s1)
    return k


def calculate_lexical_diversity(text: str) -> Dict:
    """Calculate multiple lexical diversity metrics."""
    if NLTK_AVAILABLE:
        tokens = word_tokenize(text.lower())
        sentences = sent_tokenize(text)
    else:
        tokens = simple_tokenize(text)
        sentences = text.split('.')
    
    if not tokens:
        return {
            'ttr': 0.0,
            'yules_k': 0.0,
            'unique_words': 0,
            'total_words': 0,
            'avg_word_length': 0.0,
            'avg_sentence_length': 0.0,
            'avg_syllables_per_word': 0.0
        }
    
    unique_words = len(set(tokens))
    total_words = len(tokens)
    
    # Average word length
    avg_word_length = sum(len(word) for word in tokens) / total_words if total_words > 0 else 0.0
    
    # Average sentence length
    avg_sentence_length = total_words / len(sentences) if sentences else 0.0
    
    # Average syllables per word
    total_syllables = sum(count_syllables(word) for word in tokens)
    avg_syllables_per_word = total_syllables / total_words if total_words > 0 else 0.0
    
    return {
        'ttr': unique_words / total_words if total_words > 0 else 0.0,
        'yules_k': calculate_yules_k(text),
        'unique_words': unique_words,
        'total_words': total_words,
        'avg_word_length': avg_word_length,
        'avg_sentence_length': avg_sentence_length,
        'avg_syllables_per_word': avg_syllables_per_word
    }


def evaluate_vocabulary_richness(
    corpus_path: str,
    output_path: str = "vocabulary_richness_results.json",
    sample_size: int = None
) -> Dict:
    """
    Evaluate vocabulary richness of corpus.
    
    Args:
        corpus_path: Path to corpus
        output_path: Output file path
        sample_size: Number of documents to evaluate (None = all)
    
    Returns:
        Dictionary with vocabulary richness statistics
    """
    print("=" * 80)
    print("VOCABULARY RICHNESS EVALUATION")
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
    print(f"\n2. Calculating vocabulary richness metrics...")
    all_metrics = []
    
    for i, text in enumerate(texts):
        if (i + 1) % 500 == 0:
            print(f"   Processed {i + 1}/{len(texts)} documents...")
        
        metrics = calculate_lexical_diversity(text)
        all_metrics.append(metrics)
    
    # Aggregate statistics
    import numpy as np
    
    ttrs = [m['ttr'] for m in all_metrics]
    yules_ks = [m['yules_k'] for m in all_metrics]
    avg_word_lengths = [m['avg_word_length'] for m in all_metrics]
    avg_sentence_lengths = [m['avg_sentence_length'] for m in all_metrics]
    avg_syllables = [m['avg_syllables_per_word'] for m in all_metrics]
    
    total_unique_words = sum(m['unique_words'] for m in all_metrics)
    total_words = sum(m['total_words'] for m in all_metrics)
    corpus_ttr = total_unique_words / total_words if total_words > 0 else 0.0
    
    results = {
        'total_documents': len(texts),
        'corpus_level': {
            'total_unique_words': total_unique_words,
            'total_words': total_words,
            'type_token_ratio': corpus_ttr
        },
        'document_level': {
            'type_token_ratio': {
                'mean': float(np.mean(ttrs)),
                'median': float(np.median(ttrs)),
                'std': float(np.std(ttrs)),
                'min': float(np.min(ttrs)),
                'max': float(np.max(ttrs))
            },
            'yules_k': {
                'mean': float(np.mean(yules_ks)),
                'median': float(np.median(yules_ks)),
                'std': float(np.std(yules_ks)),
                'min': float(np.min(yules_ks)),
                'max': float(np.max(yules_ks))
            },
            'avg_word_length': {
                'mean': float(np.mean(avg_word_lengths)),
                'median': float(np.median(avg_word_lengths)),
                'std': float(np.std(avg_word_lengths))
            },
            'avg_sentence_length': {
                'mean': float(np.mean(avg_sentence_lengths)),
                'median': float(np.median(avg_sentence_lengths)),
                'std': float(np.std(avg_sentence_lengths))
            },
            'avg_syllables_per_word': {
                'mean': float(np.mean(avg_syllables)),
                'median': float(np.median(avg_syllables)),
                'std': float(np.std(avg_syllables))
            }
        }
    }
    
    print(f"\n3. Results:")
    print(f"   Corpus-level TTR: {corpus_ttr:.4f}")
    print(f"   Document-level TTR - Mean: {results['document_level']['type_token_ratio']['mean']:.4f}")
    print(f"   Yule's K - Mean: {results['document_level']['yules_k']['mean']:.2f}")
    print(f"   Avg word length: {results['document_level']['avg_word_length']['mean']:.2f} characters")
    print(f"   Avg sentence length: {results['document_level']['avg_sentence_length']['mean']:.2f} words")
    print(f"   Avg syllables per word: {results['document_level']['avg_syllables_per_word']['mean']:.2f}")
    
    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to: {output_path}")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vocabulary Richness Evaluation")
    parser.add_argument(
        "--corpus_path",
        type=str,
        required=True,
        help="Path to corpus (JSON or directory)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="vocabulary_richness_results.json",
        help="Output file path"
    )
    parser.add_argument(
        "--sample_size",
        type=int,
        default=None,
        help="Number of documents to evaluate (None = all)"
    )
    
    args = parser.parse_args()
    
    evaluate_vocabulary_richness(
        args.corpus_path,
        args.output,
        args.sample_size
    )


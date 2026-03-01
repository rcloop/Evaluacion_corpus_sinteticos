#!/usr/bin/env python3
"""
Diversity Metrics Evaluation
Measures textual diversity using Self-BLEU, distinct n-grams, and repetition ratios.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Set
from collections import Counter
import argparse
import numpy as np

try:
    from nltk.tokenize import word_tokenize
    from nltk.util import ngrams
    NLTK_AVAILABLE = True
    try:
        import nltk
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
    import re
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.lower().split()


def extract_ngrams(text: str, n: int) -> List[tuple]:
    """Extract n-grams from text."""
    if NLTK_AVAILABLE:
        tokens = word_tokenize(text.lower())
    else:
        tokens = simple_tokenize(text)
    
    if len(tokens) < n:
        return []
    
    if NLTK_AVAILABLE:
        return list(ngrams(tokens, n))
    else:
        return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def calculate_self_bleu(texts: List[str], n: int = 4) -> float:
    """
    Calculate Self-BLEU score.
    Lower Self-BLEU = more diverse (better).
    """
    if len(texts) < 2:
        return 0.0
    
    # Extract n-grams for each text
    all_ngrams = []
    for text in texts:
        ngrams_list = extract_ngrams(text, n)
        all_ngrams.append(Counter(ngrams_list))
    
    # Calculate BLEU for each text against all others
    bleu_scores = []
    
    for i, reference_ngrams in enumerate(all_ngrams):
        if not reference_ngrams:
            continue
        
        # Calculate precision for this text against all others
        precisions = []
        
        for j, candidate_ngrams in enumerate(all_ngrams):
            if i == j or not candidate_ngrams:
                continue
            
            # Count matches
            matches = sum((reference_ngrams & candidate_ngrams).values())
            total = sum(candidate_ngrams.values())
            
            if total > 0:
                precision = matches / total
                precisions.append(precision)
        
        if precisions:
            # Average precision
            avg_precision = np.mean(precisions)
            bleu_scores.append(avg_precision)
    
    return np.mean(bleu_scores) if bleu_scores else 0.0


def calculate_distinct_ngrams_ratio(texts: List[str], n: int = 2) -> float:
    """Calculate ratio of unique n-grams to total n-grams."""
    all_ngrams = []
    
    for text in texts:
        ngrams_list = extract_ngrams(text, n)
        all_ngrams.extend(ngrams_list)
    
    if not all_ngrams:
        return 0.0
    
    unique_ngrams = len(set(all_ngrams))
    total_ngrams = len(all_ngrams)
    
    return unique_ngrams / total_ngrams if total_ngrams > 0 else 0.0


def calculate_repetition_ratio(texts: List[str], min_length: int = 5) -> float:
    """Calculate ratio of repeated phrases."""
    # Extract phrases of minimum length
    all_phrases = []
    
    for text in texts:
        if NLTK_AVAILABLE:
            tokens = word_tokenize(text.lower())
        else:
            tokens = simple_tokenize(text)
        
        # Extract phrases (consecutive words)
        for i in range(len(tokens) - min_length + 1):
            phrase = ' '.join(tokens[i:i+min_length])
            all_phrases.append(phrase)
    
    if not all_phrases:
        return 0.0
    
    phrase_counts = Counter(all_phrases)
    repeated = sum(1 for count in phrase_counts.values() if count > 1)
    total = len(phrase_counts)
    
    return repeated / total if total > 0 else 0.0


def evaluate_diversity(
    corpus_path: str,
    output_path: str = "diversity_results.json",
    sample_size: int = None
) -> Dict:
    """
    Evaluate diversity metrics of corpus.
    
    Args:
        corpus_path: Path to corpus
        output_path: Output file path
        sample_size: Number of documents to evaluate (None = all)
    
    Returns:
        Dictionary with diversity statistics
    """
    print("=" * 80)
    print("DIVERSITY METRICS EVALUATION")
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
    
    # Calculate Self-BLEU
    print(f"\n2. Calculating Self-BLEU (this may take a while)...")
    self_bleu_2 = calculate_self_bleu(texts, n=2)
    self_bleu_3 = calculate_self_bleu(texts, n=3)
    self_bleu_4 = calculate_self_bleu(texts, n=4)
    
    print(f"   Self-BLEU (n=2): {self_bleu_2:.4f}")
    print(f"   Self-BLEU (n=3): {self_bleu_3:.4f}")
    print(f"   Self-BLEU (n=4): {self_bleu_4:.4f}")
    
    # Calculate distinct n-grams
    print(f"\n3. Calculating distinct n-grams ratios...")
    distinct_1 = calculate_distinct_ngrams_ratio(texts, n=1)
    distinct_2 = calculate_distinct_ngrams_ratio(texts, n=2)
    distinct_3 = calculate_distinct_ngrams_ratio(texts, n=3)
    
    print(f"   Distinct 1-grams: {distinct_1:.4f}")
    print(f"   Distinct 2-grams: {distinct_2:.4f}")
    print(f"   Distinct 3-grams: {distinct_3:.4f}")
    
    # Calculate repetition ratio
    print(f"\n4. Calculating repetition ratio...")
    repetition_ratio = calculate_repetition_ratio(texts, min_length=5)
    print(f"   Repetition ratio (phrases >= 5 words): {repetition_ratio:.4f}")
    
    results = {
        'total_documents': len(texts),
        'self_bleu': {
            'n2': float(self_bleu_2),
            'n3': float(self_bleu_3),
            'n4': float(self_bleu_4),
            'mean': float(np.mean([self_bleu_2, self_bleu_3, self_bleu_4]))
        },
        'distinct_ngrams': {
            'n1': float(distinct_1),
            'n2': float(distinct_2),
            'n3': float(distinct_3)
        },
        'repetition_ratio': {
            'phrases_min_5_words': float(repetition_ratio)
        },
        'interpretation': {
            'self_bleu_target': '< 0.3 (lower is better)',
            'distinct_ngrams_target': '> 0.4 (higher is better)',
            'repetition_ratio_target': '< 0.05 (lower is better)'
        }
    }
    
    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to: {output_path}")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Diversity Metrics Evaluation")
    parser.add_argument(
        "--corpus_path",
        type=str,
        required=True,
        help="Path to corpus (JSON or directory)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="diversity_results.json",
        help="Output file path"
    )
    parser.add_argument(
        "--sample_size",
        type=int,
        default=None,
        help="Number of documents to evaluate (None = all, recommended: 1000-5000 for speed)"
    )
    
    args = parser.parse_args()
    
    evaluate_diversity(
        args.corpus_path,
        args.output,
        args.sample_size
    )


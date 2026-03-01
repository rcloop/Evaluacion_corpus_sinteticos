#!/usr/bin/env python3
"""
Statistical Comparison Evaluation
Compares statistical distributions between generated and real medical texts.
"""

import json
import os
from pathlib import Path
from typing import List, Dict
from collections import Counter
import numpy as np
from scipy import stats
import argparse
import warnings
warnings.filterwarnings('ignore')

try:
    from nltk.tokenize import word_tokenize, sent_tokenize
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


def extract_features(text: str) -> Dict:
    """Extract statistical features from text."""
    if NLTK_AVAILABLE:
        words = word_tokenize(text.lower())
        sentences = sent_tokenize(text)
    else:
        words = simple_tokenize(text)
        sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    if not words:
        return {
            'word_count': 0,
            'sentence_count': 0,
            'avg_word_length': 0.0,
            'avg_sentence_length': 0.0,
            'char_count': len(text)
        }
    
    word_lengths = [len(word) for word in words]
    
    return {
        'word_count': len(words),
        'sentence_count': len(sentences),
        'avg_word_length': np.mean(word_lengths),
        'avg_sentence_length': len(words) / len(sentences) if sentences else 0.0,
        'char_count': len(text)
    }


def compare_distributions(
    generated_features: List[Dict],
    real_features: List[Dict],
    feature_name: str
) -> Dict:
    """Compare distributions using statistical tests."""
    gen_values = [f[feature_name] for f in generated_features if f[feature_name] > 0]
    real_values = [f[feature_name] for f in real_features if f[feature_name] > 0]
    
    if not gen_values or not real_values:
        return {'error': 'Insufficient data'}
    
    # Kolmogorov-Smirnov test
    ks_statistic, ks_pvalue = stats.ks_2samp(gen_values, real_values)
    
    # Mann-Whitney U test
    u_statistic, u_pvalue = stats.mannwhitneyu(gen_values, real_values, alternative='two-sided')
    
    # Calculate means and medians
    gen_mean = np.mean(gen_values)
    real_mean = np.mean(real_values)
    gen_median = np.median(gen_values)
    real_median = np.median(real_values)
    
    # Relative difference
    mean_diff_pct = abs(gen_mean - real_mean) / real_mean * 100 if real_mean > 0 else 0.0
    median_diff_pct = abs(gen_median - real_median) / real_median * 100 if real_median > 0 else 0.0
    
    return {
        'feature': feature_name,
        'generated': {
            'mean': float(gen_mean),
            'median': float(gen_median),
            'std': float(np.std(gen_values)),
            'count': len(gen_values)
        },
        'real': {
            'mean': float(real_mean),
            'median': float(real_median),
            'std': float(np.std(real_values)),
            'count': len(real_values)
        },
        'statistical_tests': {
            'kolmogorov_smirnov': {
                'statistic': float(ks_statistic),
                'pvalue': float(ks_pvalue),
                'significant': ks_pvalue < 0.05
            },
            'mann_whitney_u': {
                'statistic': float(u_statistic),
                'pvalue': float(u_pvalue),
                'significant': u_pvalue < 0.05
            }
        },
        'relative_difference': {
            'mean_diff_percent': float(mean_diff_pct),
            'median_diff_percent': float(median_diff_pct)
        }
    }


def evaluate_statistical_comparison(
    generated_corpus_path: str,
    real_corpus_path: str,
    output_path: str = "statistical_comparison_results.json",
    sample_size: int = None
) -> Dict:
    """
    Compare statistical distributions between generated and real texts.
    
    Args:
        generated_corpus_path: Path to generated corpus
        real_corpus_path: Path to real medical corpus (e.g., MEDDOCAN)
        output_path: Output file path
        sample_size: Number of documents to evaluate (None = all)
    
    Returns:
        Dictionary with comparison statistics
    """
    print("=" * 80)
    print("STATISTICAL COMPARISON EVALUATION")
    print("=" * 80)
    
    # Load corpora
    print(f"\n1. Loading generated corpus: {generated_corpus_path}")
    generated_texts = load_corpus(generated_corpus_path)
    print(f"   Loaded {len(generated_texts)} generated documents")
    
    print(f"\n2. Loading real corpus: {real_corpus_path}")
    real_texts = load_corpus(real_corpus_path)
    print(f"   Loaded {len(real_texts)} real documents")
    
    # Sample if requested
    if sample_size:
        import random
        random.seed(42)
        if sample_size < len(generated_texts):
            generated_texts = random.sample(generated_texts, sample_size)
        if sample_size < len(real_texts):
            real_texts = random.sample(real_texts, sample_size)
        print(f"   Sampling {sample_size} documents from each corpus")
    
    # Extract features
    print(f"\n3. Extracting features...")
    generated_features = []
    for text in generated_texts:
        features = extract_features(text)
        generated_features.append(features)
    
    real_features = []
    for text in real_texts:
        features = extract_features(text)
        real_features.append(features)
    
    # Compare distributions
    print(f"\n4. Comparing distributions...")
    comparisons = {}
    
    features_to_compare = [
        'word_count',
        'sentence_count',
        'avg_word_length',
        'avg_sentence_length',
        'char_count'
    ]
    
    for feature in features_to_compare:
        print(f"   Comparing {feature}...")
        comparison = compare_distributions(generated_features, real_features, feature)
        if 'error' not in comparison:
            comparisons[feature] = comparison
    
    # Summary
    significant_differences = sum(
        1 for comp in comparisons.values()
        if comp['statistical_tests']['kolmogorov_smirnov']['significant']
    )
    
    results = {
        'generated_corpus_size': len(generated_texts),
        'real_corpus_size': len(real_texts),
        'comparisons': comparisons,
        'summary': {
            'total_features_compared': len(comparisons),
            'significant_differences': significant_differences,
            'similarity_score': (len(comparisons) - significant_differences) / len(comparisons) if comparisons else 0.0
        }
    }
    
    print(f"\n5. Results:")
    print(f"   Features compared: {results['summary']['total_features_compared']}")
    print(f"   Significant differences: {results['summary']['significant_differences']}")
    print(f"   Similarity score: {results['summary']['similarity_score']:.2%}")
    
    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to: {output_path}")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Statistical Comparison Evaluation")
    parser.add_argument(
        "--generated_corpus",
        type=str,
        required=True,
        help="Path to generated corpus (JSON or directory)"
    )
    parser.add_argument(
        "--real_corpus",
        type=str,
        required=True,
        help="Path to real medical corpus (JSON or directory)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="statistical_comparison_results.json",
        help="Output file path"
    )
    parser.add_argument(
        "--sample_size",
        type=int,
        default=None,
        help="Number of documents to evaluate from each corpus (None = all)"
    )
    
    args = parser.parse_args()
    
    evaluate_statistical_comparison(
        args.generated_corpus,
        args.real_corpus,
        args.output,
        args.sample_size
    )


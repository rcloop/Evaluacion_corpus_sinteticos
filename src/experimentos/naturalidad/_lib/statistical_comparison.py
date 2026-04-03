#!/usr/bin/env python3
"""
Statistical Comparison Evaluation
Compares statistical distributions between generated and real medical texts.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
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
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        print("[INFO] Downloading NLTK punkt_tab tokenizer...")
        nltk.download("punkt_tab", quiet=True)
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        print("[INFO] Downloading NLTK punkt tokenizer...")
        nltk.download("punkt", quiet=True)
except ImportError:
    NLTK_AVAILABLE = False
    print("[WARNING] NLTK not available. Using simple tokenization.")

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(it, desc=None, total=None, **kwargs):
        return it


def load_corpus(corpus_path: str) -> List[str]:
    """Load corpus texts from JSON or directory of text files."""
    texts = []
    
    if os.path.isdir(corpus_path):
        root = Path(corpus_path)
        files = sorted(
            p
            for p in root.rglob("*")
            if p.is_file() and p.suffix.lower() == ".txt"
        )
        for file_path in tqdm(files, desc="Statistical comparison (documents)", unit="doc"):
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
            'char_count': len(text),
            'type_token_ratio': 0.0,
        }
    
    word_lengths = [len(word) for word in words]
    type_token_ratio = len(set(words)) / len(words) if words else 0.0
    
    return {
        'word_count': len(words),
        'sentence_count': len(sentences),
        'avg_word_length': np.mean(word_lengths),
        'avg_sentence_length': len(words) / len(sentences) if sentences else 0.0,
        'char_count': len(text),
        'type_token_ratio': type_token_ratio,
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
    
    # Kolmogorov-Smirnov test (diagnostic; sensitive to any distributional difference)
    ks_statistic, ks_pvalue = stats.ks_2samp(gen_values, real_values)

    # Mann-Whitney U test
    u_statistic, u_pvalue = stats.mannwhitneyu(gen_values, real_values, alternative='two-sided')
    n1, n2 = len(gen_values), len(real_values)
    # Rank-biserial correlation (effect size for Mann-Whitney): r = 1 - 2*U/(n1*n2)
    mw_r = 1.0 - (2.0 * u_statistic) / (n1 * n2) if (n1 * n2) > 0 else None
    
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
                'significant': bool(ks_pvalue < 0.05),
            },
            'mann_whitney_u': {
                'statistic': float(u_statistic),
                'pvalue': float(u_pvalue),
                'significant': bool(u_pvalue < 0.05),
                'rank_biserial_r': float(mw_r) if mw_r is not None else None,
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
    sample_size: int = None,
    exclude_length_features: bool = False,
    sanitize_real_chunks: bool = True,
    real_sliding_windows: bool = False,
    real_window_stride: Optional[int] = None,
) -> Dict:
    """
    Compare statistical distributions between generated and real texts.
    
    Args:
        generated_corpus_path: Path to generated corpus
        real_corpus_path: Path to real medical corpus (e.g., MEDDOCAN)
        output_path: Output file path
        sample_size: Number of documents to evaluate (None = all)
        exclude_length_features: If True, compare only avg_word_length, avg_sentence_length,
            type_token_ratio (Bonferroni uses this reduced count).
        sanitize_real_chunks: If True, drop paragraph chunks in **real** texts that match
            standardized valoración block headers (see ``real_corpus_sanitize``). Skipped when
            ``real_sliding_windows`` is True if you also disable sanitization from the caller.
        real_sliding_windows: If True, **W** = round(mean synthetic token count); synthetic docs are
            kept **in full**; each real doc is split into **non-overlapping** windows of **W** tokens
            (``real_window_stride`` overrides step). Forces ``exclude_length_features``.
    
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
    if sanitize_real_chunks and not real_sliding_windows:
        from real_corpus_sanitize import sanitize_real_note_text

        real_texts = [sanitize_real_note_text(t, enabled=True) for t in real_texts]
        print("   Applied real-corpus chunk filter (banned valoración scale headers).")

    if not generated_texts:
        raise ValueError(
            f"No documents loaded from generated corpus (empty or unreadable): {generated_corpus_path}"
        )
    if not real_texts:
        raise ValueError(
            f"No documents loaded from real corpus (empty or unreadable): {real_corpus_path}"
        )

    # Sample if requested
    if sample_size:
        import random
        random.seed(42)
        if sample_size < len(generated_texts):
            generated_texts = random.sample(generated_texts, sample_size)
        if sample_size < len(real_texts):
            real_texts = random.sample(real_texts, sample_size)
        print(f"   Sampling {sample_size} documents from each corpus")

    if real_sliding_windows:
        exclude_length_features = True
        from length_norm import mean_word_count, expand_real_corpus_windows

        w_mean = mean_word_count(generated_texts)
        W = max(1, int(round(w_mean)))
        stride = (
            int(real_window_stride)
            if (real_window_stride is not None and int(real_window_stride) > 0)
            else W
        )
        n_real_sources = len(real_texts)
        real_texts = expand_real_corpus_windows(real_texts, W, stride)
        if not real_texts:
            raise ValueError(
                f"Real windowing produced zero windows (real notes shorter than W={W}). "
                f"Mean synthetic tokens={w_mean:.2f}"
            )
        print(
            f"\n2b. Real windowing: W={W} (mean synthetic tokens={w_mean:.2f}), stride={stride} - "
            f"{n_real_sources} real files -> {len(real_texts)} windows. "
            "Synthetic left as full documents. Tests use length-agnostic features only."
        )

    protocol_meta = {
        "exclude_length_features": bool(exclude_length_features),
        "sanitize_real_chunks": bool(sanitize_real_chunks),
        "real_sliding_windows": bool(real_sliding_windows),
    }
    if real_sliding_windows:
        protocol_meta["window_tokens"] = int(W)
        protocol_meta["stride_tokens"] = int(stride)
        protocol_meta["num_real_source_documents"] = int(n_real_sources)
        protocol_meta["num_real_windows"] = int(len(real_texts))
        protocol_meta["mean_synthetic_word_count_pre_window"] = float(w_mean)

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
    
    features_to_compare = (
        ['avg_word_length', 'avg_sentence_length', 'type_token_ratio']
        if exclude_length_features
        else [
            'word_count',
            'sentence_count',
            'avg_word_length',
            'avg_sentence_length',
            'char_count',
            'type_token_ratio',
        ]
    )
    if exclude_length_features:
        print("   Protocol: length-agnostic feature set (no raw length scalars).")
    
    for feature in features_to_compare:
        print(f"   Comparing {feature}...")
        comparison = compare_distributions(generated_features, real_features, feature)
        if 'error' not in comparison:
            comparisons[feature] = comparison
    
    n_comp = len(comparisons)
    alpha = 0.05
    alpha_bonferroni = alpha / n_comp if n_comp else alpha
    
    # Add Bonferroni significance to each comparison
    for comp in comparisons.values():
        ts = comp['statistical_tests']
        ks_p = ts['kolmogorov_smirnov']['pvalue']
        mw_p = ts['mann_whitney_u']['pvalue']
        ts['kolmogorov_smirnov']['significant_bonferroni'] = bool(ks_p < alpha_bonferroni)
        ts['mann_whitney_u']['significant_bonferroni'] = bool(mw_p < alpha_bonferroni)
    
    # Summary (publication-facing): Mann–Whitney only
    significant_differences = int(sum(
        1 for comp in comparisons.values()
        if comp['statistical_tests']['mann_whitney_u']['significant']
    ))
    significant_differences_bonferroni = int(sum(
        1 for comp in comparisons.values()
        if comp['statistical_tests']['mann_whitney_u']['significant_bonferroni']
    ))
    results = {
        'generated_corpus_size': int(len(generated_texts)),
        'real_corpus_size': int(len(real_texts)),
        'protocol': protocol_meta,
        'comparisons': comparisons,
        'summary': {
            'total_features_compared': int(n_comp),
            'alpha': alpha,
            'alpha_bonferroni': float(alpha_bonferroni),
            'significant_differences': significant_differences,
            'significant_differences_bonferroni': significant_differences_bonferroni,
            'similarity_score': float((n_comp - significant_differences) / n_comp) if n_comp else 0.0,
            'similarity_score_bonferroni': float((n_comp - significant_differences_bonferroni) / n_comp) if n_comp else 0.0,
        }
    }
    
    print(f"\n5. Results:")
    print(f"   Features compared: {results['summary']['total_features_compared']}")
    print(f"   Alpha (Bonferroni): {results['summary']['alpha_bonferroni']:.4f}")
    print(f"   Significant differences (raw alpha=0.05): {results['summary']['significant_differences']}")
    print(f"   Significant differences (Bonferroni): {results['summary']['significant_differences_bonferroni']}")
    print(f"   Similarity score: {results['summary']['similarity_score']:.2%}")
    print(f"   Similarity score (Bonferroni): {results['summary']['similarity_score_bonferroni']:.2%}")
    
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
    parser.add_argument(
        "--no_sanitize_real_chunks",
        action="store_true",
        help="Do not strip banned valoración header chunks from real corpus texts.",
    )
    
    args = parser.parse_args()
    
    evaluate_statistical_comparison(
        args.generated_corpus,
        args.real_corpus,
        args.output,
        args.sample_size,
        exclude_length_features=False,
        sanitize_real_chunks=not args.no_sanitize_real_chunks,
    )


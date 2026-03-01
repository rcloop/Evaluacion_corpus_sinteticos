#!/usr/bin/env python3
"""
Coherence Evaluation
Measures semantic coherence and fluency using sentence embeddings.
"""

import json
import os
import re
from pathlib import Path
from typing import List, Dict
import numpy as np
import argparse
import warnings
warnings.filterwarnings('ignore')

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("[WARNING] sentence-transformers not available. Coherence evaluation requires this library.")


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


def split_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    # Simple sentence splitting
    sentences = re.split(r'[.!?]+\s+', text)
    # Clean and filter
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    return sentences


def calculate_semantic_coherence(text: str, model) -> Dict:
    """
    Calculate semantic coherence between consecutive sentences.
    
    Args:
        text: Input text
        model: Sentence transformer model
    
    Returns:
        Dictionary with coherence metrics
    """
    sentences = split_sentences(text)
    
    if len(sentences) < 2:
        return {
            'coherence_score': 0.0,
            'num_sentences': len(sentences),
            'sentence_similarities': []
        }
    
    # Encode sentences
    embeddings = model.encode(sentences)
    
    # Calculate cosine similarity between consecutive sentences
    from sklearn.metrics.pairwise import cosine_similarity
    
    similarities = []
    for i in range(len(embeddings) - 1):
        sim = cosine_similarity([embeddings[i]], [embeddings[i+1]])[0][0]
        similarities.append(float(sim))
    
    coherence_score = np.mean(similarities) if similarities else 0.0
    
    return {
        'coherence_score': float(coherence_score),
        'num_sentences': len(sentences),
        'sentence_similarities': similarities,
        'std_similarity': float(np.std(similarities)) if similarities else 0.0
    }


def evaluate_coherence(
    corpus_path: str,
    model_name: str = "paraphrase-multilingual-MiniLM-L12-v2",
    output_path: str = "coherence_results.json",
    sample_size: int = None
) -> Dict:
    """
    Evaluate coherence of corpus.
    
    Args:
        corpus_path: Path to corpus
        model_name: Sentence transformer model name
        output_path: Output file path
        sample_size: Number of documents to evaluate (None = all)
    
    Returns:
        Dictionary with coherence statistics
    """
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        return {'error': 'sentence-transformers library required for coherence evaluation'}
    
    print("=" * 80)
    print("COHERENCE EVALUATION")
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
    
    # Load model
    print(f"\n2. Loading sentence transformer model: {model_name}")
    try:
        model = SentenceTransformer(model_name)
        print("   Model loaded successfully")
    except Exception as e:
        return {'error': f'Error loading model: {str(e)}'}
    
    # Calculate coherence for each document
    print(f"\n3. Calculating coherence metrics...")
    coherence_scores = []
    all_similarities = []
    
    for i, text in enumerate(texts):
        if (i + 1) % 100 == 0:
            print(f"   Processed {i + 1}/{len(texts)} documents...")
        
        try:
            coherence = calculate_semantic_coherence(text, model)
            if coherence['coherence_score'] > 0:
                coherence_scores.append(coherence['coherence_score'])
                all_similarities.extend(coherence['sentence_similarities'])
        except Exception as e:
            continue
    
    if not coherence_scores:
        return {'error': 'No valid coherence scores calculated'}
    
    # Statistics
    results = {
        'model_name': model_name,
        'total_documents': len(texts),
        'successful_evaluations': len(coherence_scores),
        'coherence': {
            'mean': float(np.mean(coherence_scores)),
            'median': float(np.median(coherence_scores)),
            'std': float(np.std(coherence_scores)),
            'min': float(np.min(coherence_scores)),
            'max': float(np.max(coherence_scores)),
            'percentiles': {
                '25th': float(np.percentile(coherence_scores, 25)),
                '50th': float(np.percentile(coherence_scores, 50)),
                '75th': float(np.percentile(coherence_scores, 75)),
                '90th': float(np.percentile(coherence_scores, 90))
            }
        },
        'sentence_similarities': {
            'mean': float(np.mean(all_similarities)) if all_similarities else 0.0,
            'median': float(np.median(all_similarities)) if all_similarities else 0.0,
            'std': float(np.std(all_similarities)) if all_similarities else 0.0
        },
        'interpretation': {
            'target_coherence': '> 0.6 (higher is better)',
            'actual_mean': float(np.mean(coherence_scores))
        }
    }
    
    print(f"\n4. Results:")
    print(f"   Mean coherence: {results['coherence']['mean']:.4f}")
    print(f"   Median coherence: {results['coherence']['median']:.4f}")
    print(f"   Std deviation: {results['coherence']['std']:.4f}")
    print(f"   Mean sentence similarity: {results['sentence_similarities']['mean']:.4f}")
    
    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to: {output_path}")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coherence Evaluation")
    parser.add_argument(
        "--corpus_path",
        type=str,
        required=True,
        help="Path to corpus (JSON or directory)"
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="paraphrase-multilingual-MiniLM-L12-v2",
        help="Sentence transformer model name"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="coherence_results.json",
        help="Output file path"
    )
    parser.add_argument(
        "--sample_size",
        type=int,
        default=None,
        help="Number of documents to evaluate (None = all)"
    )
    
    args = parser.parse_args()
    
    evaluate_coherence(
        args.corpus_path,
        args.model_name,
        args.output,
        args.sample_size
    )


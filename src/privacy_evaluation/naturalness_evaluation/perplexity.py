#!/usr/bin/env python3
"""
Perplexity Evaluation
Measures how "surprised" a language model is by the text.
Lower perplexity = more natural (closer to training distribution).
"""

import json
import os
import numpy as np
from pathlib import Path
from typing import List, Dict
import argparse
import warnings
warnings.filterwarnings('ignore')

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel, AutoModelForMaskedLM
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("[WARNING] PyTorch/transformers not available. Perplexity evaluation requires these libraries.")


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


def calculate_perplexity_mlm(text: str, model, tokenizer, max_length: int = 512) -> float:
    """
    Calculate perplexity using masked language model.
    
    Args:
        text: Input text
        model: Pre-trained MLM model
        tokenizer: Tokenizer
        max_length: Maximum sequence length
    
    Returns:
        Perplexity score
    """
    # Tokenize
    encodings = tokenizer(
        text,
        return_tensors='pt',
        max_length=max_length,
        truncation=True,
        padding=True
    )
    
    input_ids = encodings['input_ids']
    attention_mask = encodings['attention_mask']
    
    # Calculate loss
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss
    
    # Perplexity = exp(loss)
    perplexity = torch.exp(loss).item()
    
    return perplexity


def calculate_perplexity_causal(text: str, model, tokenizer, max_length: int = 512) -> float:
    """
    Calculate perplexity using causal language model.
    
    Args:
        text: Input text
        model: Pre-trained causal LM model
        tokenizer: Tokenizer
        max_length: Maximum sequence length
    
    Returns:
        Perplexity score
    """
    # Tokenize
    encodings = tokenizer(
        text,
        return_tensors='pt',
        max_length=max_length,
        truncation=True,
        padding=True
    )
    
    input_ids = encodings['input_ids']
    
    # Calculate loss
    with torch.no_grad():
        outputs = model(input_ids=input_ids, labels=input_ids)
        loss = outputs.loss
    
    # Perplexity = exp(loss)
    perplexity = torch.exp(loss).item()
    
    return perplexity


def evaluate_perplexity(
    corpus_path: str,
    model_name: str = "dccuchile/bert-base-spanish-wwm-uncased",
    model_type: str = "mlm",  # "mlm" or "causal"
    output_path: str = "perplexity_results.json",
    max_length: int = 512,
    sample_size: int = None
) -> Dict:
    """
    Evaluate perplexity of corpus.
    
    Args:
        corpus_path: Path to corpus
        model_name: Pre-trained model name
        model_type: "mlm" (masked) or "causal"
        output_path: Output file path
        max_length: Maximum sequence length
        sample_size: Number of documents to evaluate (None = all)
    
    Returns:
        Dictionary with perplexity statistics
    """
    if not TORCH_AVAILABLE:
        return {'error': 'PyTorch and transformers libraries required for perplexity evaluation'}
    
    print("=" * 80)
    print("PERPLEXITY EVALUATION")
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
    print(f"\n2. Loading model: {model_name}")
    print(f"   Model type: {model_type}")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        if model_type == "mlm":
            model = AutoModelForMaskedLM.from_pretrained(model_name)
            calculate_perplexity = calculate_perplexity_mlm
        else:
            model = AutoModelForCausalLM.from_pretrained(model_name)
            calculate_perplexity = calculate_perplexity_causal
        
        model.eval()
        print("   Model loaded successfully")
        
    except Exception as e:
        return {'error': f'Error loading model: {str(e)}'}
    
    # Calculate perplexity for each document
    print(f"\n3. Calculating perplexity for {len(texts)} documents...")
    perplexities = []
    failed = 0
    
    for i, text in enumerate(texts):
        if (i + 1) % 100 == 0:
            print(f"   Processed {i + 1}/{len(texts)} documents...")
        
        try:
            # Skip very short texts
            if len(text.strip()) < 10:
                continue
            
            perplexity = calculate_perplexity(text, model, tokenizer, max_length)
            perplexities.append(perplexity)
            
        except Exception as e:
            failed += 1
            continue
    
    if not perplexities:
        return {'error': 'No valid perplexity scores calculated'}
    
    # Statistics
    perplexities = np.array(perplexities)
    
    stats = {
        'model_name': model_name,
        'model_type': model_type,
        'total_documents': len(texts),
        'successful_calculations': len(perplexities),
        'failed_calculations': failed,
        'perplexity': {
            'mean': float(np.mean(perplexities)),
            'median': float(np.median(perplexities)),
            'std': float(np.std(perplexities)),
            'min': float(np.min(perplexities)),
            'max': float(np.max(perplexities)),
            'percentiles': {
                '25th': float(np.percentile(perplexities, 25)),
                '50th': float(np.percentile(perplexities, 50)),
                '75th': float(np.percentile(perplexities, 75)),
                '90th': float(np.percentile(perplexities, 90)),
                '95th': float(np.percentile(perplexities, 95))
            }
        }
    }
    
    print(f"\n4. Results:")
    print(f"   - Mean perplexity: {stats['perplexity']['mean']:.2f}")
    print(f"   - Median perplexity: {stats['perplexity']['median']:.2f}")
    print(f"   - Std deviation: {stats['perplexity']['std']:.2f}")
    print(f"   - Min: {stats['perplexity']['min']:.2f}")
    print(f"   - Max: {stats['perplexity']['max']:.2f}")
    
    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to: {output_path}")
    
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perplexity Evaluation")
    parser.add_argument(
        "--corpus_path",
        type=str,
        required=True,
        help="Path to corpus (JSON or directory)"
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="dccuchile/bert-base-spanish-wwm-uncased",
        help="Pre-trained model name"
    )
    parser.add_argument(
        "--model_type",
        type=str,
        default="mlm",
        choices=["mlm", "causal"],
        help="Model type: 'mlm' (masked) or 'causal'"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="perplexity_results.json",
        help="Output file path"
    )
    parser.add_argument(
        "--max_length",
        type=int,
        default=512,
        help="Maximum sequence length"
    )
    parser.add_argument(
        "--sample_size",
        type=int,
        default=None,
        help="Number of documents to evaluate (None = all)"
    )
    
    args = parser.parse_args()
    
    evaluate_perplexity(
        args.corpus_path,
        args.model_name,
        args.model_type,
        args.output,
        args.max_length,
        args.sample_size
    )


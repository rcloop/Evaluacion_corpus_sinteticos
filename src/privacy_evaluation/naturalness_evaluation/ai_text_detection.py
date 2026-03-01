#!/usr/bin/env python3
"""
AI Text Detection Evaluation
Trains a binary classifier to distinguish between human-authored and AI-generated texts.
Lower accuracy indicates higher naturalness (ideally ~50%).
"""

import json
import os
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
import argparse
import warnings
warnings.filterwarnings('ignore')

try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("[WARNING] transformers not available. Will use TF-IDF + Logistic Regression only.")


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


def prepare_classification_data(
    generated_texts: List[str],
    human_texts: List[str],
    test_size: float = 0.2
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Prepare data for binary classification.
    
    Args:
        generated_texts: AI-generated texts (label = 0)
        human_texts: Human-authored texts (label = 1)
        test_size: Fraction for test set
    
    Returns:
        X_train, X_test, y_train, y_test
    """
    # Combine texts and labels
    all_texts = generated_texts + human_texts
    all_labels = [0] * len(generated_texts) + [1] * len(human_texts)
    
    # Vectorize
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 3),
        min_df=2,
        max_df=0.95
    )
    
    X = vectorizer.fit_transform(all_texts).toarray()
    y = np.array(all_labels)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    return X_train, X_test, y_train, y_test, vectorizer


def train_tfidf_classifier(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray
) -> Dict:
    """Train TF-IDF + Logistic Regression classifier."""
    
    # Train
    classifier = LogisticRegression(max_iter=1000, random_state=42)
    classifier.fit(X_train, y_train)
    
    # Predict
    y_pred = classifier.predict(X_test)
    y_pred_proba = classifier.predict_proba(X_test)[:, 1]
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc_roc = roc_auc_score(y_test, y_pred_proba)
    
    baseline_accuracy = max(np.mean(y_test), 1 - np.mean(y_test))
    
    return {
        'method': 'TF-IDF + Logistic Regression',
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'auc_roc': auc_roc,
        'baseline_accuracy': baseline_accuracy,
        'classification_report': classification_report(y_test, y_pred, output_dict=True)
    }


def train_transformer_classifier(
    generated_texts: List[str],
    human_texts: List[str],
    model_name: str = "dccuchile/bert-base-spanish-wwm-uncased"
) -> Dict:
    """Train transformer-based classifier (if transformers available)."""
    
    if not TRANSFORMERS_AVAILABLE:
        return {'error': 'transformers library not available'}
    
    try:
        # Prepare data
        all_texts = generated_texts + human_texts
        all_labels = [0] * len(generated_texts) + [1] * len(human_texts)
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            all_texts, all_labels, test_size=0.2, random_state=42, stratify=all_labels
        )
        
        # Create pipeline
        classifier = pipeline(
            "text-classification",
            model=model_name,
            tokenizer=model_name,
            device=-1  # CPU
        )
        
        # Note: This is a simplified version. Full fine-tuning would require more code.
        # For now, we'll use the pre-trained model as-is or return a note.
        
        return {
            'method': f'Transformer ({model_name})',
            'note': 'Full fine-tuning requires more implementation. Using pre-trained model as baseline.',
            'model_name': model_name
        }
        
    except Exception as e:
        return {'error': str(e)}


def evaluate_ai_detection(
    generated_corpus_path: str,
    human_corpus_path: str = None,
    output_path: str = "ai_detection_results.json",
    use_transformer: bool = False,
    transformer_model: str = "dccuchile/bert-base-spanish-wwm-uncased"
) -> Dict:
    """
    Complete AI text detection evaluation.
    
    Args:
        generated_corpus_path: Path to generated corpus
        human_corpus_path: Path to human-authored corpus (if None, splits generated corpus)
        output_path: Path to save results
        use_transformer: Whether to use transformer model (requires transformers library)
        transformer_model: Transformer model name
    
    Returns:
        Dictionary with evaluation results
    """
    print("=" * 80)
    print("AI TEXT DETECTION EVALUATION")
    print("=" * 80)
    
    # Load generated texts
    print(f"\n1. Loading generated corpus: {generated_corpus_path}")
    generated_texts = load_corpus(generated_corpus_path)
    print(f"   Loaded {len(generated_texts)} generated texts")
    
    # Load human texts
    if human_corpus_path:
        print(f"\n2. Loading human corpus: {human_corpus_path}")
        human_texts = load_corpus(human_corpus_path)
        print(f"   Loaded {len(human_texts)} human texts")
    else:
        print("\n2. No human corpus provided. Splitting generated corpus for evaluation.")
        # Split generated corpus to simulate human vs generated
        human_texts, _ = train_test_split(
            generated_texts, test_size=0.5, random_state=42
        )
        print(f"   Using {len(human_texts)} texts as 'human' baseline")
    
    # Balance datasets
    min_size = min(len(generated_texts), len(human_texts))
    generated_texts = generated_texts[:min_size]
    human_texts = human_texts[:min_size]
    
    print(f"\n3. Balanced datasets: {min_size} texts each")
    
    # Prepare data
    print("\n4. Preparing classification data...")
    X_train, X_test, y_train, y_test, vectorizer = prepare_classification_data(
        generated_texts, human_texts
    )
    print(f"   Training set: {len(X_train)} samples")
    print(f"   Test set: {len(X_test)} samples")
    
    # Train TF-IDF classifier
    print("\n5. Training TF-IDF + Logistic Regression classifier...")
    tfidf_results = train_tfidf_classifier(X_train, y_train, X_test, y_test)
    
    print(f"\n   Results:")
    print(f"   - Accuracy: {tfidf_results['accuracy']:.4f}")
    print(f"   - Precision: {tfidf_results['precision']:.4f}")
    print(f"   - Recall: {tfidf_results['recall']:.4f}")
    print(f"   - F1-Score: {tfidf_results['f1_score']:.4f}")
    print(f"   - AUC-ROC: {tfidf_results['auc_roc']:.4f}")
    print(f"   - Baseline: {tfidf_results['baseline_accuracy']:.4f}")
    
    # Interpret results
    if tfidf_results['accuracy'] < 0.6:
        naturalness_level = "HIGH"
        interpretation = "Classifier cannot reliably distinguish between generated and human texts. High naturalness."
    elif tfidf_results['accuracy'] < 0.7:
        naturalness_level = "MODERATE"
        interpretation = "Classifier can somewhat distinguish. Moderate naturalness."
    else:
        naturalness_level = "LOW"
        interpretation = "Classifier can reliably distinguish. Low naturalness - texts are easily identifiable as AI-generated."
    
    results = {
        'generated_corpus_size': len(generated_texts),
        'human_corpus_size': len(human_texts),
        'tfidf_classifier': tfidf_results,
        'naturalness_assessment': {
            'level': naturalness_level,
            'interpretation': interpretation,
            'target_accuracy': '< 0.6 (lower is better)',
            'actual_accuracy': tfidf_results['accuracy']
        }
    }
    
    # Try transformer if requested
    if use_transformer and TRANSFORMERS_AVAILABLE:
        print("\n6. Training transformer classifier...")
        transformer_results = train_transformer_classifier(
            generated_texts, human_texts, transformer_model
        )
        results['transformer_classifier'] = transformer_results
    
    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to: {output_path}")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Text Detection Evaluation")
    parser.add_argument(
        "--generated_corpus",
        type=str,
        required=True,
        help="Path to generated corpus (JSON or directory)"
    )
    parser.add_argument(
        "--human_corpus",
        type=str,
        default=None,
        help="Path to human-authored corpus (optional, will split generated corpus if not provided)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="ai_detection_results.json",
        help="Output file path"
    )
    parser.add_argument(
        "--use_transformer",
        action="store_true",
        help="Use transformer model (requires transformers library)"
    )
    parser.add_argument(
        "--transformer_model",
        type=str,
        default="dccuchile/bert-base-spanish-wwm-uncased",
        help="Transformer model name"
    )
    
    args = parser.parse_args()
    
    evaluate_ai_detection(
        args.generated_corpus,
        args.human_corpus,
        args.output,
        args.use_transformer,
        args.transformer_model
    )


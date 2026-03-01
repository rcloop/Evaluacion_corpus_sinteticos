#!/usr/bin/env python3
"""
Run All Naturalness Evaluations
Orchestrates all naturalness evaluation metrics.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    from .ai_text_detection import evaluate_ai_detection
    from .perplexity import evaluate_perplexity
    from .vocabulary_richness import evaluate_vocabulary_richness
    from .readability import evaluate_readability
    from .diversity_metrics import evaluate_diversity
    from .coherence import evaluate_coherence
    from .statistical_comparison import evaluate_statistical_comparison
except ImportError:
    # If running as script directly
    from ai_text_detection import evaluate_ai_detection
    from perplexity import evaluate_perplexity
    from vocabulary_richness import evaluate_vocabulary_richness
    from readability import evaluate_readability
    from diversity_metrics import evaluate_diversity
    from coherence import evaluate_coherence
    from statistical_comparison import evaluate_statistical_comparison


def run_all_naturalness_evaluations(
    generated_corpus_path: str,
    human_corpus_path: str = None,
    real_corpus_path: str = None,
    output_dir: str = "naturalness_evaluation_results",
    sample_size: int = None,
    skip_ai_detection: bool = False,
    skip_perplexity: bool = False,
    skip_statistical: bool = False
) -> dict:
    """
    Run all naturalness evaluations.
    
    Args:
        generated_corpus_path: Path to generated corpus
        human_corpus_path: Path to human corpus (for AI detection)
        real_corpus_path: Path to real medical corpus (for statistical comparison)
        output_dir: Output directory
        sample_size: Sample size for evaluations (None = all)
        skip_*: Flags to skip specific evaluations
    
    Returns:
        Consolidated results dictionary
    """
    print("=" * 80)
    print("NATURALNESS EVALUATION SUITE")
    print("=" * 80)
    print(f"Generated corpus: {generated_corpus_path}")
    print(f"Output directory: {output_dir}")
    print(f"Sample size: {sample_size if sample_size else 'All documents'}")
    print("=" * 80)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    all_results = {
        'timestamp': datetime.now().isoformat(),
        'generated_corpus_path': generated_corpus_path,
        'evaluations': {}
    }
    
    # 1. AI Text Detection
    if not skip_ai_detection:
        print("\n" + "=" * 80)
        print("1. AI TEXT DETECTION")
        print("=" * 80)
        try:
            ai_results = evaluate_ai_detection(
                generated_corpus_path,
                human_corpus_path,
                str(output_path / "ai_detection_results.json")
            )
            all_results['evaluations']['ai_detection'] = ai_results
        except Exception as e:
            print(f"Error in AI detection: {e}")
            all_results['evaluations']['ai_detection'] = {'error': str(e)}
    
    # 2. Perplexity
    if not skip_perplexity:
        print("\n" + "=" * 80)
        print("2. PERPLEXITY")
        print("=" * 80)
        try:
            perplexity_results = evaluate_perplexity(
                generated_corpus_path,
                output_path=str(output_path / "perplexity_results.json"),
                sample_size=sample_size
            )
            all_results['evaluations']['perplexity'] = perplexity_results
        except Exception as e:
            print(f"Error in perplexity: {e}")
            all_results['evaluations']['perplexity'] = {'error': str(e)}
    
    # 3. Vocabulary Richness
    print("\n" + "=" * 80)
    print("3. VOCABULARY RICHNESS")
    print("=" * 80)
    try:
        vocab_results = evaluate_vocabulary_richness(
            generated_corpus_path,
            output_path=str(output_path / "vocabulary_richness_results.json"),
            sample_size=sample_size
        )
        all_results['evaluations']['vocabulary_richness'] = vocab_results
    except Exception as e:
        print(f"Error in vocabulary richness: {e}")
        all_results['evaluations']['vocabulary_richness'] = {'error': str(e)}
    
    # 4. Readability
    print("\n" + "=" * 80)
    print("4. READABILITY")
    print("=" * 80)
    try:
        readability_results = evaluate_readability(
            generated_corpus_path,
            output_path=str(output_path / "readability_results.json"),
            sample_size=sample_size
        )
        all_results['evaluations']['readability'] = readability_results
    except Exception as e:
        print(f"Error in readability: {e}")
        all_results['evaluations']['readability'] = {'error': str(e)}
    
    # 5. Diversity Metrics
    print("\n" + "=" * 80)
    print("5. DIVERSITY METRICS")
    print("=" * 80)
    try:
        diversity_results = evaluate_diversity(
            generated_corpus_path,
            output_path=str(output_path / "diversity_results.json"),
            sample_size=sample_size if sample_size else 5000  # Limit for performance
        )
        all_results['evaluations']['diversity'] = diversity_results
    except Exception as e:
        print(f"Error in diversity: {e}")
        all_results['evaluations']['diversity'] = {'error': str(e)}
    
    # 6. Coherence
    print("\n" + "=" * 80)
    print("6. COHERENCE")
    print("=" * 80)
    try:
        coherence_results = evaluate_coherence(
            generated_corpus_path,
            output_path=str(output_path / "coherence_results.json"),
            sample_size=sample_size
        )
        all_results['evaluations']['coherence'] = coherence_results
    except Exception as e:
        print(f"Error in coherence: {e}")
        all_results['evaluations']['coherence'] = {'error': str(e)}
    
    # 7. Statistical Comparison
    if not skip_statistical and real_corpus_path:
        print("\n" + "=" * 80)
        print("7. STATISTICAL COMPARISON")
        print("=" * 80)
        try:
            statistical_results = evaluate_statistical_comparison(
                generated_corpus_path,
                real_corpus_path,
                output_path=str(output_path / "statistical_comparison_results.json"),
                sample_size=sample_size
            )
            all_results['evaluations']['statistical_comparison'] = statistical_results
        except Exception as e:
            print(f"Error in statistical comparison: {e}")
            all_results['evaluations']['statistical_comparison'] = {'error': str(e)}
    
    # Generate summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    summary = generate_summary(all_results['evaluations'])
    all_results['summary'] = summary
    
    print_summary(summary)
    
    # Save consolidated results
    consolidated_path = output_path / "consolidated_naturalness_report.json"
    with open(consolidated_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Consolidated results saved to: {consolidated_path}")
    
    return all_results


def generate_summary(evaluations: dict) -> dict:
    """Generate summary of all evaluations."""
    summary = {}
    
    # AI Detection
    if 'ai_detection' in evaluations and 'error' not in evaluations['ai_detection']:
        ai = evaluations['ai_detection']
        if 'naturalness_assessment' in ai:
            summary['ai_detection'] = {
                'accuracy': ai['tfidf_classifier']['accuracy'],
                'naturalness_level': ai['naturalness_assessment']['level'],
                'target': '< 0.6 (lower is better)'
            }
    
    # Perplexity
    if 'perplexity' in evaluations and 'error' not in evaluations['perplexity']:
        pp = evaluations['perplexity']
        if 'perplexity' in pp:
            summary['perplexity'] = {
                'mean': pp['perplexity']['mean'],
                'target': 'Within 20% of real texts'
            }
    
    # Vocabulary Richness
    if 'vocabulary_richness' in evaluations and 'error' not in evaluations['vocabulary_richness']:
        vocab = evaluations['vocabulary_richness']
        if 'corpus_level' in vocab:
            summary['vocabulary_richness'] = {
                'ttr': vocab['corpus_level']['type_token_ratio'],
                'target': 'Within 15% of real texts'
            }
    
    # Readability
    if 'readability' in evaluations and 'error' not in evaluations['readability']:
        read = evaluations['readability']
        if 'inflesz' in read:
            summary['readability'] = {
                'inflesz_mean': read['inflesz']['mean'],
                'interpretation': read['inflesz']['interpretation'],
                'target': '40-60 for medical texts'
            }
    
    # Diversity
    if 'diversity' in evaluations and 'error' not in evaluations['diversity']:
        div = evaluations['diversity']
        if 'self_bleu' in div:
            summary['diversity'] = {
                'self_bleu_mean': div['self_bleu']['mean'],
                'target': '< 0.3 (lower is better)'
            }
    
    # Coherence
    if 'coherence' in evaluations and 'error' not in evaluations['coherence']:
        coh = evaluations['coherence']
        if 'coherence' in coh:
            summary['coherence'] = {
                'mean': coh['coherence']['mean'],
                'target': '> 0.6 (higher is better)'
            }
    
    # Statistical Comparison
    if 'statistical_comparison' in evaluations and 'error' not in evaluations['statistical_comparison']:
        stat = evaluations['statistical_comparison']
        if 'summary' in stat:
            summary['statistical_comparison'] = {
                'similarity_score': stat['summary']['similarity_score'],
                'target': '> 0.8 (higher is better)'
            }
    
    return summary


def print_summary(summary: dict):
    """Print evaluation summary."""
    print("\nEvaluation Summary:")
    print("-" * 80)
    
    if 'ai_detection' in summary:
        ai = summary['ai_detection']
        print(f"AI Detection Accuracy: {ai['accuracy']:.4f} ({ai['naturalness_level']} naturalness)")
    
    if 'perplexity' in summary:
        pp = summary['perplexity']
        print(f"Perplexity (mean): {pp['mean']:.2f}")
    
    if 'vocabulary_richness' in summary:
        vocab = summary['vocabulary_richness']
        print(f"Type-Token Ratio: {vocab['ttr']:.4f}")
    
    if 'readability' in summary:
        read = summary['readability']
        print(f"INFLESZ: {read['inflesz_mean']:.2f} ({read['interpretation']})")
    
    if 'diversity' in summary:
        div = summary['diversity']
        print(f"Self-BLEU: {div['self_bleu_mean']:.4f}")
    
    if 'coherence' in summary:
        coh = summary['coherence']
        print(f"Coherence: {coh['mean']:.4f}")
    
    if 'statistical_comparison' in summary:
        stat = summary['statistical_comparison']
        print(f"Statistical Similarity: {stat['similarity_score']:.2%}")
    
    print("-" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run All Naturalness Evaluations")
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
        help="Path to human corpus for AI detection (optional)"
    )
    parser.add_argument(
        "--real_corpus",
        type=str,
        default=None,
        help="Path to real medical corpus for statistical comparison (optional)"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="naturalness_evaluation_results",
        help="Output directory"
    )
    parser.add_argument(
        "--sample_size",
        type=int,
        default=None,
        help="Sample size for evaluations (None = all, recommended for large corpora)"
    )
    parser.add_argument(
        "--skip_ai_detection",
        action="store_true",
        help="Skip AI detection evaluation"
    )
    parser.add_argument(
        "--skip_perplexity",
        action="store_true",
        help="Skip perplexity evaluation (requires PyTorch)"
    )
    parser.add_argument(
        "--skip_statistical",
        action="store_true",
        help="Skip statistical comparison"
    )
    
    args = parser.parse_args()
    
    run_all_naturalness_evaluations(
        args.generated_corpus,
        args.human_corpus,
        args.real_corpus,
        args.output_dir,
        args.sample_size,
        args.skip_ai_detection,
        args.skip_perplexity,
        args.skip_statistical
    )


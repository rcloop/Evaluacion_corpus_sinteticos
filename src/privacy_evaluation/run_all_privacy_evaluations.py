"""
Main script to run all privacy evaluations:
1. Membership Inference
2. Attribute Inference
3. Nearest Neighbor Memorization Detection
"""

import argparse
import json
from pathlib import Path
from membership_inference import evaluate_membership_inference
from attribute_inference import evaluate_attribute_inference
from nearest_neighbor_memorization import evaluate_memorization


def run_all_evaluations(
    corpus_path: str,
    annotations_path: str = None,
    external_corpus_path: str = None,
    output_dir: str = "privacy_evaluation_results",
    semantic_model: str = "paraphrase-multilingual-MiniLM-L12-v2",
    skip_semantic: bool = False,
):
    """
    Run all privacy evaluations and generate consolidated report.
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print("=" * 80)
    print("PRIVACY EVALUATION SUITE")
    print("=" * 80)
    print(f"Corpus: {corpus_path}")
    print(f"Output directory: {output_dir}")
    print()
    
    all_results = {}
    
    # 1. Membership Inference
    print("\n" + "=" * 80)
    print("1. MEMBERSHIP INFERENCE EVALUATION")
    print("=" * 80)
    try:
        mi_results = evaluate_membership_inference(
            corpus_path=corpus_path,
            external_corpus_path=external_corpus_path,
            output_path=str(output_path / "membership_inference.json")
        )
        all_results['membership_inference'] = mi_results
    except Exception as e:
        print(f"Error in membership inference: {e}")
        all_results['membership_inference'] = {'error': str(e)}
    
    # 2. Attribute Inference
    print("\n" + "=" * 80)
    print("2. ATTRIBUTE INFERENCE EVALUATION")
    print("=" * 80)
    try:
        ai_results = evaluate_attribute_inference(
            corpus_path=corpus_path,
            annotations_path=annotations_path,
            output_path=str(output_path / "attribute_inference.json")
        )
        all_results['attribute_inference'] = ai_results
    except Exception as e:
        print(f"Error in attribute inference: {e}")
        all_results['attribute_inference'] = {'error': str(e)}
    
    # 3. Memorization Detection
    print("\n" + "=" * 80)
    print("3. MEMORIZATION DETECTION (NEAREST NEIGHBOR)")
    print("=" * 80)
    if skip_semantic:
        print("[WARNING] Similitud semantica deshabilitada (solo busqueda exacta)")
    try:
        mem_results = evaluate_memorization(
            corpus_path=corpus_path,
            annotations_path=annotations_path,
            output_path=str(output_path / "memorization_detection.json"),
            semantic_model=semantic_model,
            skip_semantic=skip_semantic
        )
        all_results['memorization_detection'] = mem_results
    except Exception as e:
        print(f"Error in memorization detection: {e}")
        all_results['memorization_detection'] = {'error': str(e)}
    
    # Generate consolidated report
    print("\n" + "=" * 80)
    print("CONSOLIDATED PRIVACY REPORT")
    print("=" * 80)
    
    consolidated = {
        'corpus_info': {
            'corpus_path': corpus_path,
            'corpus_size': all_results.get('membership_inference', {}).get('corpus_size', 'unknown')
        },
        'evaluations': all_results,
        'overall_risk_assessment': generate_overall_risk_assessment(all_results)
    }
    
    # Save consolidated report
    consolidated_path = output_path / "consolidated_privacy_report.json"
    with open(consolidated_path, 'w', encoding='utf-8') as f:
        json.dump(consolidated, f, indent=2, ensure_ascii=False)
    
    print(f"\nConsolidated report saved to: {consolidated_path}")
    print_summary(consolidated)
    
    return consolidated


def generate_overall_risk_assessment(results: dict) -> dict:
    """Generate overall risk assessment from all evaluations."""
    risk_scores = []
    risk_details = []
    
    # Membership inference risk
    mi = results.get('membership_inference', {})
    if 'attack_metrics' in mi:
        mi_auc = mi['attack_metrics'].get('auc_roc', 0.5)
        risk_scores.append(mi_auc)
        risk_details.append({
            'test': 'membership_inference',
            'score': mi_auc,
            'risk': 'high' if mi_auc >= 0.7 else 'medium' if mi_auc >= 0.6 else 'low'
        })
    
    # Attribute inference risk
    ai = results.get('attribute_inference', {})
    if 'overall_risk' in ai:
        ai_max = ai['overall_risk'].get('max_auc_roc', 0.5)
        risk_scores.append(ai_max)
        risk_details.append({
            'test': 'attribute_inference',
            'score': ai_max,
            'risk': 'high' if ai_max >= 0.7 else 'medium' if ai_max >= 0.6 else 'low'
        })
    
    # Memorization risk
    mem = results.get('memorization_detection', {})
    if 'memorization_risk' in mem:
        mem_risk = mem['memorization_risk']
        total_repeated = mem_risk.get('total_repeated_phi_entities', 0)
        high_sim = mem_risk.get('high_similarity_pairs', 0)
        # Normalize to 0-1 scale
        mem_score = min(1.0, (total_repeated / 200.0 + high_sim / 100.0) / 2.0)
        risk_scores.append(mem_score)
        risk_details.append({
            'test': 'memorization',
            'score': mem_score,
            'risk': mem_risk.get('risk_level', 'unknown')
        })
    
    # Overall risk
    if risk_scores:
        max_risk = max(risk_scores)
        mean_risk = sum(risk_scores) / len(risk_scores)
        
        overall_risk = (
            'critical' if max_risk >= 0.8 else
            'high' if max_risk >= 0.7 else
            'medium' if max_risk >= 0.6 or mean_risk >= 0.5 else
            'low'
        )
    else:
        overall_risk = 'unknown'
        max_risk = 0.0
        mean_risk = 0.0
    
    return {
        'overall_risk_level': overall_risk,
        'max_risk_score': max_risk,
        'mean_risk_score': mean_risk,
        'individual_risks': risk_details,
        'recommendation': generate_recommendation(overall_risk, max_risk)
    }


def generate_recommendation(risk_level: str, max_score: float) -> str:
    """Generate privacy recommendation based on risk level."""
    if risk_level == 'low':
        return (
            "Low overall privacy risk detected. The synthetic corpus demonstrates good privacy "
            "properties. No immediate action required, but continue monitoring."
        )
    elif risk_level == 'medium':
        return (
            "Moderate privacy risk detected. Consider implementing additional privacy-preserving "
            "techniques such as differential privacy or increased diversity in generation."
        )
    elif risk_level == 'high':
        return (
            "High privacy risk detected. Strongly recommend implementing differential privacy "
            "or other privacy-preserving mechanisms. Review generation pipeline for potential "
            "memorization issues."
        )
    else:
        return (
            "Critical privacy risk detected. Immediate action required: implement differential "
            "privacy, review and redesign generation pipeline, and conduct thorough privacy audit."
        )


def print_summary(consolidated: dict):
    """Print summary of privacy evaluation results."""
    overall = consolidated.get('overall_risk_assessment', {})
    
    print("\n" + "-" * 80)
    print("SUMMARY")
    print("-" * 80)
    print(f"Overall Risk Level: {overall.get('overall_risk_level', 'unknown').upper()}")
    print(f"Max Risk Score: {overall.get('max_risk_score', 0.0):.4f}")
    print(f"Mean Risk Score: {overall.get('mean_risk_score', 0.0):.4f}")
    print()
    print("Individual Test Results:")
    for risk in overall.get('individual_risks', []):
        print(f"  - {risk['test']}: {risk['risk'].upper()} (score: {risk['score']:.4f})")
    print()
    print("Recommendation:")
    print(f"  {overall.get('recommendation', 'N/A')}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Complete Privacy Evaluation Suite")
    parser.add_argument(
        "--corpus_path",
        type=str,
        required=True,
        help="Path to corpus (directory or .json file)"
    )
    parser.add_argument(
        "--annotations_path",
        type=str,
        default=None,
        help="Path to annotations (optional)"
    )
    parser.add_argument(
        "--external_corpus_path",
        type=str,
        default=None,
        help="Path to external corpus for membership inference (optional)"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="privacy_evaluation_results",
        help="Output directory for results"
    )
    parser.add_argument(
        "--semantic_model",
        type=str,
        default="paraphrase-multilingual-MiniLM-L12-v2",
        help="Sentence transformer model for semantic similarity"
    )
    parser.add_argument(
        "--skip_semantic",
        action="store_true",
        help="Skip semantic similarity search (only exact similarity in memorization detection)"
    )
    
    args = parser.parse_args()
    
    run_all_evaluations(
        corpus_path=args.corpus_path,
        annotations_path=args.annotations_path,
        external_corpus_path=args.external_corpus_path,
        output_dir=args.output_dir,
        semantic_model=args.semantic_model,
        skip_semantic=args.skip_semantic,
    )


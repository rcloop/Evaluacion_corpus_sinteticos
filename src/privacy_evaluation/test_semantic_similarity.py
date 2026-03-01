"""
Test script to evaluate semantic similarity on a small sample (20 documents)
to estimate execution time for the full corpus.
"""

import json
import time
import argparse
from pathlib import Path
from nearest_neighbor_memorization import load_corpus, semantic_similarity_search

def create_sample_corpus(corpus_path: str, sample_size: int = 20, output_path: str = None):
    """Create a sample corpus with N documents for testing."""
    print(f"Loading corpus from {corpus_path}...")
    with open(corpus_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        raise ValueError("Corpus must be a JSON array")
    
    # Take first N documents
    sample = data[:sample_size]
    
    if output_path is None:
        output_path = f"corpus_sample_{sample_size}.json"
    
    print(f"Saving sample of {len(sample)} documents to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sample, f, ensure_ascii=False, indent=2)
    
    print(f"Sample corpus created: {output_path}")
    return output_path

def test_semantic_similarity(corpus_path: str, sample_size: int = 20):
    """Test semantic similarity search on a sample."""
    print("=" * 80)
    print("SEMANTIC SIMILARITY TEST")
    print("=" * 80)
    print(f"Sample size: {sample_size} documents")
    print()
    
    # Create sample corpus
    sample_path = create_sample_corpus(corpus_path, sample_size)
    
    # Load sample corpus
    print(f"\nLoading sample corpus...")
    texts = load_corpus(sample_path)
    print(f"Loaded {len(texts)} texts")
    
    # Test semantic similarity
    print("\n" + "=" * 80)
    print("Running semantic similarity search...")
    print("=" * 80)
    
    start_time = time.time()
    
    try:
        similar_pairs = semantic_similarity_search(
            texts,
            model_name='paraphrase-multilingual-MiniLM-L12-v2',
            top_k=5,
            similarity_threshold=0.85
        )
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\n{'='*80}")
        print("RESULTS")
        print(f"{'='*80}")
        print(f"Execution time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
        print(f"Time per document: {elapsed_time/len(texts):.2f} seconds")
        print(f"Found {len(similar_pairs)} similar pairs (similarity >= 0.85)")
        
        # Estimate for full corpus
        full_corpus_size = 14035
        estimated_time = (elapsed_time / len(texts)) * full_corpus_size
        estimated_hours = estimated_time / 3600
        
        print(f"\n{'='*80}")
        print("ESTIMATION FOR FULL CORPUS (14,035 documents)")
        print(f"{'='*80}")
        print(f"Estimated time: {estimated_time:.0f} seconds ({estimated_time/60:.0f} minutes, {estimated_hours:.2f} hours)")
        print(f"Note: This is a linear extrapolation. Actual time may vary due to:")
        print(f"  - Model loading overhead (only once)")
        print(f"  - Memory constraints with larger datasets")
        print(f"  - Computational complexity of similarity matrix (O(n²))")
        
        # Show top similar pairs
        if similar_pairs:
            print(f"\n{'='*80}")
            print("TOP 5 MOST SIMILAR PAIRS")
            print(f"{'='*80}")
            for i, pair in enumerate(similar_pairs[:5], 1):
                print(f"\n{i}. Similarity: {pair['similarity']:.4f}")
                print(f"   Doc 1: {pair['doc1']['filename']}")
                print(f"   Doc 2: {pair['doc2']['filename']}")
                print(f"   Preview 1: {pair['doc1']['text_preview'][:100]}...")
                print(f"   Preview 2: {pair['doc2']['text_preview'][:100]}...")
        
        # Save results
        results = {
            'sample_size': sample_size,
            'execution_time_seconds': elapsed_time,
            'execution_time_minutes': elapsed_time / 60,
            'time_per_document_seconds': elapsed_time / len(texts),
            'similar_pairs_found': len(similar_pairs),
            'estimated_time_full_corpus_seconds': estimated_time,
            'estimated_time_full_corpus_hours': estimated_hours,
            'top_similar_pairs': similar_pairs[:10]
        }
        
        results_path = f"semantic_similarity_test_results_{sample_size}.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to: {results_path}")
        
        return results
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test semantic similarity on a sample")
    parser.add_argument(
        "--corpus_path",
        type=str,
        required=True,
        help="Path to full corpus JSON file"
    )
    parser.add_argument(
        "--sample_size",
        type=int,
        default=20,
        help="Number of documents to use for testing (default: 20)"
    )
    
    args = parser.parse_args()
    
    test_semantic_similarity(args.corpus_path, args.sample_size)



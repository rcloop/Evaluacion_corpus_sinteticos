# Naturalness Evaluation Suite

Complete suite of scripts to evaluate text naturalness and linguistic quality.

## Scripts Overview

1. **`ai_text_detection.py`** - Binary classification (human vs AI-generated)
2. **`perplexity.py`** - Language model perplexity
3. **`vocabulary_richness.py`** - TTR, Yule's K, lexical diversity
4. **`readability.py`** - Spanish readability indices (INFLESZ, Fernández Huerta)
5. **`diversity_metrics.py`** - Self-BLEU, distinct n-grams, repetition ratio
6. **`coherence.py`** - Semantic coherence between sentences
7. **`statistical_comparison.py`** - Compare distributions with real texts
8. **`run_all_naturalness_evaluations.py`** - Run all evaluations

## Quick Start

### Run All Evaluations

```bash
python run_all_naturalness_evaluations.py \
    --generated_corpus "../../corpus_repo/corpus/documents" \
    --output_dir naturalness_results \
    --sample_size 1000
```

### Run Individual Evaluations

```bash
# AI Detection
python ai_text_detection.py \
    --generated_corpus "../../corpus_repo/corpus/documents" \
    --human_corpus "path/to/real/texts.json" \
    --output ai_detection.json

# Perplexity
python perplexity.py \
    --corpus_path "../../corpus_repo/corpus/documents" \
    --output perplexity.json \
    --sample_size 500

# Vocabulary Richness
python vocabulary_richness.py \
    --corpus_path "../../corpus_repo/corpus/documents" \
    --output vocab_richness.json

# Readability
python readability.py \
    --corpus_path "../../corpus_repo/corpus/documents" \
    --output readability.json

# Diversity
python diversity_metrics.py \
    --corpus_path "../../corpus_repo/corpus/documents" \
    --output diversity.json \
    --sample_size 2000

# Coherence
python coherence.py \
    --corpus_path "../../corpus_repo/corpus/documents" \
    --output coherence.json \
    --sample_size 500

# Statistical Comparison
python statistical_comparison.py \
    --generated_corpus "../../corpus_repo/corpus/documents" \
    --real_corpus "path/to/meddocan.json" \
    --output statistical_comparison.json
```

## Dependencies

```bash
pip install scikit-learn numpy scipy nltk sentence-transformers transformers torch
```

## Expected Output

Each script generates a JSON file with detailed metrics and statistics.


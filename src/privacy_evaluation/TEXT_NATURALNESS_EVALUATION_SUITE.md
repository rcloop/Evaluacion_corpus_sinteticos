# Text Naturalness Evaluation Suite

## Overview

This document proposes a comprehensive suite of evaluations to assess the naturalness and linguistic quality of the generated medical corpus. Naturalness evaluation is crucial for ensuring that synthetic texts are indistinguishable from human-authored medical documents and suitable for training NER models.

---

## Evaluation Categories

### 1. AI Text Detection
### 2. Linguistic Metrics
### 3. Readability Metrics
### 4. Statistical Comparison with Real Data
### 5. Diversity Metrics
### 6. Coherence and Fluency
### 7. Human Evaluation

---

## 1. AI Text Detection

### 1.1 Binary Classification (Human vs. AI-generated)

**Purpose:** Determine if a text classifier can distinguish between synthetic and human-authored medical texts.

**Methodology:**
- Train a binary classifier (e.g., RoBERTa, BERT) on a balanced dataset of:
  - Human-authored medical texts (from MEDDOCAN or similar)
  - Generated texts from the corpus
- Use cross-validation to evaluate performance
- Metrics: Accuracy, Precision, Recall, F1-score, AUC-ROC

**Expected Result:** Lower accuracy indicates higher naturalness (ideally ~50%, indicating the classifier cannot distinguish)

**Implementation:**
```python
# Pseudocode
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.model_selection import train_test_split

# Load human texts and generated texts
human_texts = load_meddocan_texts()
generated_texts = load_corpus_texts()

# Train classifier
model = AutoModelForSequenceClassification.from_pretrained("roberta-base")
# Fine-tune on binary classification task
# Evaluate on held-out test set
```

**Target Metric:** Classification accuracy < 60% (indicating high naturalness)

---

### 1.2 Zero-shot AI Detection Tools

**Purpose:** Use pre-trained AI detection models to assess naturalness.

**Tools to Evaluate:**
- **GPTZero** (if API available)
- **OpenAI's Classifier** (if available)
- **GLTR (Giant Language Model Test Room)**
- **DetectGPT**
- **Watermarking detection** (if applicable)

**Methodology:**
- Run each document through detection tools
- Calculate percentage of documents classified as "human-authored"
- Compare with baseline (human-authored texts)

**Target Metric:** >85% classified as human-authored

---

## 2. Linguistic Metrics

### 2.1 Perplexity

**Purpose:** Measure how "surprised" a language model is by the text (lower perplexity = more natural).

**Methodology:**
- Use a pre-trained Spanish medical language model (e.g., BETO, mBERT, or domain-specific model)
- Calculate perplexity for each document
- Compare with perplexity of human-authored medical texts

**Implementation:**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained("dccuchile/bert-base-spanish-wwm-uncased")
tokenizer = AutoTokenizer.from_pretrained("dccuchile/bert-base-spanish-wwm-uncased")

def calculate_perplexity(text, model, tokenizer):
    encodings = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**encodings, labels=encodings.input_ids)
        loss = outputs.loss
    return torch.exp(loss).item()
```

**Target Metric:** Perplexity within 20% of human-authored texts

---

### 2.2 N-gram Overlap with Real Medical Texts

**Purpose:** Compare n-gram distributions between generated and real medical texts.

**Methodology:**
- Extract n-grams (1-5) from generated corpus
- Extract n-grams from real medical corpus (MEDDOCAN)
- Calculate:
  - **Jaccard similarity** of n-gram sets
  - **KL divergence** of n-gram distributions
  - **Cosine similarity** of n-gram frequency vectors

**Target Metric:** 
- Jaccard similarity > 0.6
- KL divergence < 2.0
- Cosine similarity > 0.7

---

### 2.3 Vocabulary Richness

**Purpose:** Assess lexical diversity and vocabulary usage.

**Metrics:**
- **Type-Token Ratio (TTR):** Unique words / Total words
- **Lexical Diversity (Yule's K):** Measure of vocabulary richness
- **Average word length**
- **Average sentence length**
- **Unique n-grams ratio**

**Target Metric:** TTR and lexical diversity within 15% of human-authored texts

---

## 3. Readability Metrics

### 3.1 Spanish Readability Indices

**Purpose:** Evaluate text readability using established Spanish readability formulas.

**Metrics:**
- **Flesch-Szigriszt Index (INFLESZ):** Spanish adaptation of Flesch Reading Ease
- **Fernández Huerta Index:** Spanish readability formula
- **Gutiérrez de Polini Index:** Spanish medical text readability

**Implementation:**
```python
def calculate_inflesz(text):
    # INFLESZ = 206.835 - (1.015 * ASL) - (84.6 * ASW)
    # ASL = Average Sentence Length
    # ASW = Average Syllables per Word
    sentences = text.split('.')
    words = text.split()
    # Calculate ASL and ASW
    # Return INFLESZ score
    pass
```

**Target Metric:** INFLESZ scores similar to real medical texts (typically 40-60 for medical texts)

---

### 3.2 Sentence Structure Analysis

**Purpose:** Analyze sentence complexity and structure.

**Metrics:**
- Average sentence length
- Sentence length distribution
- Subordinate clause ratio
- Punctuation usage patterns
- Sentence type distribution (declarative, interrogative, etc.)

**Target Metric:** Sentence structure patterns similar to real medical texts

---

## 4. Statistical Comparison with Real Data

### 4.1 Distribution Comparison

**Purpose:** Compare statistical distributions of various text features.

**Features to Compare:**
- Word frequency distributions
- Character n-gram distributions
- Sentence length distributions
- Document length distributions
- POS tag distributions
- Dependency parse statistics

**Statistical Tests:**
- **Kolmogorov-Smirnov test** for distribution similarity
- **Mann-Whitney U test** for median comparisons
- **Chi-square test** for categorical distributions

**Target Metric:** p-values > 0.05 (indicating no significant difference)

---

### 4.2 Medical Terminology Analysis

**Purpose:** Assess proper use of medical terminology.

**Methodology:**
- Extract medical terms using:
  - UMLS (Unified Medical Language System) Spanish subset
  - SNOMED CT Spanish terms
  - Medical dictionaries
- Compare term frequency and usage patterns
- Check for proper medical terminology context

**Target Metric:** Medical term usage patterns similar to real medical texts

---

## 5. Diversity Metrics

### 5.1 Textual Diversity

**Purpose:** Measure diversity in generated texts.

**Metrics:**
- **Self-BLEU:** Measure similarity between generated texts (lower = more diverse)
- **Distinct n-grams:** Ratio of unique n-grams to total n-grams
- **Repetition ratio:** Percentage of repeated phrases
- **Semantic diversity:** Average semantic distance between documents

**Target Metric:**
- Self-BLEU < 0.3 (lower is better)
- Distinct n-grams ratio > 0.4
- Repetition ratio < 5%

---

### 5.2 Structural Diversity

**Purpose:** Assess diversity in document structure and format.

**Metrics:**
- Document type distribution (consultation notes, reports, etc.)
- Section structure patterns
- Paragraph organization
- Template usage patterns

**Target Metric:** High structural diversity (no single template dominates)

---

## 6. Coherence and Fluency

### 6.1 Coherence Metrics

**Purpose:** Evaluate text coherence and logical flow.

**Methods:**
- **Entity coherence:** Check if entities are used consistently throughout the document
- **Temporal coherence:** Verify temporal references are consistent
- **Semantic coherence:** Use sentence embeddings to measure semantic flow
- **Coreference resolution:** Check if pronouns and references are resolved correctly

**Implementation:**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def calculate_semantic_coherence(text):
    sentences = split_sentences(text)
    embeddings = model.encode(sentences)
    # Calculate cosine similarity between consecutive sentences
    coherence_scores = []
    for i in range(len(embeddings) - 1):
        similarity = cosine_similarity(embeddings[i], embeddings[i+1])
        coherence_scores.append(similarity)
    return np.mean(coherence_scores)
```

**Target Metric:** Coherence scores > 0.6

---

### 6.2 Fluency Metrics

**Purpose:** Assess grammatical correctness and fluency.

**Methods:**
- **Grammar checking:** Use Spanish grammar checkers (e.g., LanguageTool)
- **Language model fluency score:** Use perplexity as fluency indicator
- **Syntactic correctness:** POS tagging and dependency parsing error rates

**Target Metric:** Grammar error rate < 5%

---

## 7. Human Evaluation

### 7.1 Expert Evaluation

**Purpose:** Medical professionals evaluate text naturalness.

**Methodology:**
- Recruit medical professionals (doctors, nurses, medical transcriptionists)
- Present pairs of texts (one real, one generated) in random order
- Ask evaluators to:
  - Identify which is human-authored (forced choice)
  - Rate naturalness on 1-5 scale
  - Identify any unnatural patterns
  - Assess medical terminology usage

**Metrics:**
- **Identification accuracy:** % correctly identifying human text (target: ~50%)
- **Naturalness rating:** Average rating (target: >3.5/5)
- **Inter-annotator agreement:** Fleiss' Kappa

---

### 7.2 Crowdsourced Evaluation

**Purpose:** General population evaluates text naturalness.

**Platforms:**
- Amazon Mechanical Turk
- Prolific
- Custom survey platform

**Tasks:**
- Naturalness rating (1-5 scale)
- Grammaticality rating
- Medical terminology appropriateness
- Overall quality assessment

**Target Metric:** Average naturalness rating >3.5/5

---

## Implementation Priority

### Phase 1: Quick Wins (Easy to Implement)
1. ✅ **AI Text Detection** (Binary Classification)
2. ✅ **Vocabulary Richness** (TTR, Lexical Diversity)
3. ✅ **Readability Metrics** (INFLESZ)
4. ✅ **Statistical Comparison** (Distribution tests)

### Phase 2: Medium Complexity
5. **Perplexity Calculation**
6. **N-gram Overlap Analysis**
7. **Coherence Metrics**
8. **Diversity Metrics** (Self-BLEU, Distinct n-grams)

### Phase 3: Advanced/External
9. **Zero-shot AI Detection Tools**
10. **Medical Terminology Analysis**
11. **Human Evaluation** (Expert and Crowdsourced)

---

## Recommended Evaluation Suite (Minimum Viable)

For a comprehensive but practical evaluation, implement:

1. **AI Text Detection** (Binary classification with RoBERTa/BERT)
2. **Perplexity** (Using Spanish medical language model)
3. **Vocabulary Richness** (TTR, Lexical Diversity)
4. **Readability** (INFLESZ index)
5. **Statistical Comparison** (Distribution tests with real medical texts)
6. **Diversity Metrics** (Self-BLEU, Distinct n-grams)
7. **Coherence** (Semantic similarity between sentences)

**Estimated Implementation Time:** 2-3 weeks for full suite

---

## Expected Results for High-Quality Corpus

| Metric | Target Value | Interpretation |
|--------|-------------|----------------|
| **AI Detection Accuracy** | < 60% | Classifier cannot distinguish |
| **Perplexity** | Within 20% of real texts | Similar to human texts |
| **TTR** | Within 15% of real texts | Similar vocabulary richness |
| **INFLESZ** | 40-60 | Appropriate for medical texts |
| **Self-BLEU** | < 0.3 | High diversity |
| **Coherence Score** | > 0.6 | Good semantic flow |
| **Grammar Error Rate** | < 5% | High grammaticality |

---

## Integration with Privacy Evaluation

These naturalness evaluations complement the privacy evaluation by:

1. **Contextualizing memorization results:** High naturalness with low memorization = ideal
2. **Explaining repetition patterns:** Low diversity in naturalness metrics may explain PHI repetition
3. **Validating generation quality:** Ensures corpus is suitable for NER training despite privacy concerns

---

## References and Tools

### Python Libraries
- `transformers` (Hugging Face) - For language models
- `sentence-transformers` - For semantic similarity
- `nltk` / `spaCy` - For linguistic analysis
- `scikit-learn` - For classification and statistical tests
- `language-tool-python` - For grammar checking (Spanish)

### Pre-trained Models
- `dccuchile/bert-base-spanish-wwm-uncased` (BETO)
- `PlanTL-GOB-ES/roberta-base-bne` (Spanish RoBERTa)
- `paraphrase-multilingual-MiniLM-L12-v2` (Multilingual embeddings)

### Medical Resources
- UMLS (Spanish subset)
- SNOMED CT (Spanish terms)
- MEDDOCAN corpus (for comparison)

---

## Next Steps

1. **Implement Phase 1 evaluations** (Quick wins)
2. **Run evaluations on current corpus**
3. **Compare results with MEDDOCAN baseline**
4. **Document findings in paper**
5. **Use results to inform future generation improvements**


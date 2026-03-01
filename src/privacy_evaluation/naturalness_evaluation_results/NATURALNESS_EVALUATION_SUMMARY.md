# Naturalness Evaluation Summary and Interpretation

## Overview

This document provides a comprehensive summary and interpretation of the naturalness evaluation performed on the generated medical corpus. The evaluation assessed 100 documents from the corpus across four key dimensions: vocabulary richness, readability, diversity, and coherence.

**Corpus Source:** [generate_corpus_anonimizacion/corpus/documents](https://github.com/ramsestein/generate_corpus_anonimizacion/tree/main/corpus/documents)

---

## 1. Vocabulary Richness

### Metrics Evaluated

**Corpus-Level Metrics:**
- **Type-Token Ratio (TTR):** 0.599 (59.9%)
  - Measures lexical diversity at the corpus level
  - Ratio of unique words to total words
  - **Target:** Within 15% of real medical texts
  - **Interpretation:** ✅ **PASS** - The TTR of 59.9% indicates good vocabulary richness, suggesting the corpus uses a diverse vocabulary similar to real medical texts.

**Document-Level Metrics:**
- **Type-Token Ratio (mean):** 0.606 (median: 0.608, std: 0.040)
  - Range: 0.461 - 0.694
  - **Interpretation:** Good consistency across documents with moderate variation

- **Yule's K (mean):** 144.9 (median: 140.9, std: 24.2)
  - Range: 99.4 - 281.4
  - Measures vocabulary concentration (lower = more diverse)
  - **Interpretation:** Moderate vocabulary concentration, indicating reasonable lexical diversity

- **Average Word Length:** 5.41 characters (std: 0.28)
  - **Interpretation:** Consistent word length distribution, typical for Spanish medical texts

- **Average Sentence Length:** 20.9 words (median: 20.7, std: 3.07)
  - **Interpretation:** Appropriate sentence length for medical documentation

- **Average Syllables per Word:** 2.23 (median: 2.24, std: 0.10)
  - **Interpretation:** Consistent syllable distribution, typical for Spanish medical terminology

### Overall Assessment: ✅ **GOOD**
The vocabulary richness metrics indicate that the generated corpus demonstrates:
- Good lexical diversity (TTR: 59.9%)
- Consistent vocabulary patterns across documents
- Appropriate word and sentence length distributions
- Characteristics similar to real medical texts

---

## 2. Readability

### Metrics Evaluated

**INFLESZ Index:**
- **Mean:** 6.39 (median: 5.74, std: 5.08)
- **Range:** 0.09 - 22.02
- **Interpretation:** "Muy difícil" (Very difficult)
- **Target for medical texts:** 40-60 (indicating moderate difficulty appropriate for medical professionals)

**Fernández Huerta Index:**
- **Mean:** 192.01 (median: 192.16, std: 1.86)
- **Range:** 186.03 - 196.55
- **Interpretation:** Very high scores indicate very difficult reading level

### Overall Assessment: ⚠️ **CONCERNING**

**Key Findings:**
- The INFLESZ scores (mean: 6.39) are significantly below the target range of 40-60 for medical texts
- The interpretation "Muy difícil" suggests the texts are too difficult to read
- However, this may be acceptable for medical documentation, which often uses technical terminology and complex sentence structures
- The high Fernández Huerta scores (mean: 192.01) confirm the high reading difficulty

**Interpretation:**
While the readability scores indicate high difficulty, this may be **expected and acceptable** for medical texts, which:
- Use specialized medical terminology
- Employ complex sentence structures
- Target medical professionals rather than general readers

**Recommendation:** Compare with real medical texts (MEDDOCAN) to determine if this difficulty level is consistent with authentic medical documentation.

---

## 3. Diversity

### Metrics Evaluated

**Self-BLEU:**
- **N-2:** 0.133
- **N-3:** 0.045
- **N-4:** 0.022
- **Mean:** 0.067
- **Target:** < 0.3 (lower is better, indicating higher diversity)
- **Interpretation:** ✅ **EXCELLENT** - The mean Self-BLEU of 0.067 is well below the target threshold, indicating very high textual diversity. The corpus shows minimal repetition between documents.

**Distinct N-grams:**
- **N-1 (unigrams):** 0.093 (9.3% unique)
- **N-2 (bigrams):** 0.341 (34.1% unique)
- **N-3 (trigrams):** 0.580 (58.0% unique)
- **Target:** > 0.4 for higher-order n-grams (higher is better)
- **Interpretation:** ✅ **GOOD** - The trigram distinct ratio of 0.580 exceeds the target, indicating good diversity at the phrase level.

**Repetition Ratio:**
- **Phrases (min 5 words):** 0.100 (10.0%)
- **Target:** < 0.05 (5%, lower is better)
- **Interpretation:** ⚠️ **MODERATE CONCERN** - The repetition ratio of 10% is double the target threshold, indicating some repetition of longer phrases across documents.

### Overall Assessment: ✅ **GOOD with Minor Concerns**

**Key Findings:**
- **Excellent diversity at document level** (Self-BLEU: 0.067)
- **Good phrase-level diversity** (distinct trigrams: 58.0%)
- **Moderate concern** with phrase repetition (10% vs. target 5%)

**Interpretation:**
The corpus demonstrates strong overall diversity, with minimal similarity between documents. However, there is some repetition of longer phrases (≥5 words) that exceeds the target threshold. This may be acceptable for medical texts, which often contain standard phrases and templates, but should be monitored.

---

## 4. Coherence

### Metrics Evaluated

**Semantic Coherence:**
- **Model:** paraphrase-multilingual-MiniLM-L12-v2
- **Mean coherence:** 0.312 (median: 0.316, std: 0.054)
- **Range:** 0.181 - 0.450
- **Percentiles:**
  - 25th: 0.272
  - 50th: 0.316
  - 75th: 0.349
  - 90th: 0.374
- **Target:** > 0.6 (higher is better, indicating better semantic flow between sentences)
- **Interpretation:** ⚠️ **BELOW TARGET** - The mean coherence of 0.312 is approximately half the target value, indicating moderate semantic coherence between sentences.

**Sentence Similarities:**
- **Mean:** 0.312 (median: 0.311, std: 0.154)
- **Interpretation:** Moderate similarity between consecutive sentences

### Overall Assessment: ⚠️ **MODERATE CONCERN**

**Key Findings:**
- Coherence score (0.312) is significantly below the target (> 0.6)
- The score indicates moderate semantic flow between sentences
- There is substantial variation (std: 0.054) across documents

**Interpretation:**
The coherence scores suggest that while sentences are somewhat related semantically, the semantic flow between consecutive sentences could be improved. This may indicate:
- Some documents may have abrupt topic shifts
- Sentences may not always build logically on previous sentences
- The narrative flow may be less smooth than ideal

**Context:** Medical documents often have structured sections (e.g., history, examination, diagnosis) where coherence within sections may be higher than coherence across sections. The moderate scores may reflect this structural characteristic rather than a fundamental flaw.

**Recommendation:** 
- Compare coherence scores with real medical texts to determine if this level is typical
- Analyze coherence within document sections vs. across sections
- Consider if the lower coherence affects the utility of the corpus for NER training

---

## Overall Summary

### Strengths ✅

1. **Excellent Vocabulary Richness**
   - TTR of 59.9% indicates good lexical diversity
   - Consistent vocabulary patterns across documents
   - Appropriate word and sentence characteristics

2. **Excellent Textual Diversity**
   - Self-BLEU of 0.067 (well below target of 0.3)
   - High distinct n-gram ratios (trigrams: 58.0%)
   - Minimal repetition between documents

3. **Consistent Document Characteristics**
   - Stable metrics across documents (low standard deviations)
   - Appropriate sentence and word length distributions

### Areas of Concern ⚠️

1. **Readability**
   - INFLESZ score (6.39) indicates "Muy difícil" reading level
   - Significantly below target range (40-60) for medical texts
   - **Note:** This may be acceptable for medical documentation targeting professionals

2. **Coherence**
   - Mean coherence (0.312) is below target (> 0.6)
   - Moderate semantic flow between sentences
   - **Note:** May reflect structural characteristics of medical documents

3. **Phrase Repetition**
   - Repetition ratio (10%) exceeds target (5%)
   - Some repetition of longer phrases across documents
   - **Note:** May be acceptable for medical texts with standard phrases

### Recommendations

1. **Comparative Analysis**
   - Compare all metrics with real medical texts (MEDDOCAN corpus)
   - Determine if readability and coherence levels are typical for medical documentation

2. **Section-Level Analysis**
   - Analyze coherence within document sections vs. across sections
   - Medical documents may have lower coherence across sections by design

3. **Phrase Repetition**
   - Investigate which phrases are repeated
   - Determine if repetition is due to standard medical terminology/phrases (acceptable) or lack of diversity (concerning)

4. **Utility Assessment**
   - Evaluate whether the moderate coherence affects NER model training
   - Assess if the corpus quality is sufficient for the intended use case

---

## Conclusion

The naturalness evaluation reveals a corpus with **strong vocabulary richness and excellent textual diversity**, indicating that the generated texts are lexically diverse and show minimal repetition between documents. However, **readability and coherence scores are below target values**, which may reflect characteristics of medical documentation rather than fundamental quality issues.

**Key Takeaway:** The corpus demonstrates good naturalness in terms of vocabulary and diversity, but readability and coherence should be compared with real medical texts to determine if the observed levels are acceptable for medical documentation.

**Overall Assessment:** ✅ **GOOD** - The corpus shows strong naturalness characteristics in key areas (vocabulary, diversity), with some areas (readability, coherence) requiring further investigation through comparison with real medical texts.

---

## Metrics Summary Table

| Metric | Value | Target | Status | Interpretation |
|--------|-------|--------|--------|----------------|
| **Vocabulary Richness** |
| TTR (corpus) | 0.599 | Within 15% of real texts | ✅ PASS | Good lexical diversity |
| TTR (documents, mean) | 0.606 | - | ✅ GOOD | Consistent across documents |
| Yule's K (mean) | 144.9 | - | ✅ GOOD | Moderate vocabulary concentration |
| Avg sentence length | 20.9 words | - | ✅ GOOD | Appropriate for medical texts |
| **Readability** |
| INFLESZ (mean) | 6.39 | 40-60 | ⚠️ BELOW | Very difficult (may be acceptable) |
| Fernández Huerta (mean) | 192.01 | - | ⚠️ HIGH | Very difficult reading level |
| **Diversity** |
| Self-BLEU (mean) | 0.067 | < 0.3 | ✅ EXCELLENT | Very high diversity |
| Distinct trigrams | 0.580 | > 0.4 | ✅ GOOD | Good phrase diversity |
| Repetition ratio | 0.100 | < 0.05 | ⚠️ MODERATE | Some phrase repetition |
| **Coherence** |
| Semantic coherence (mean) | 0.312 | > 0.6 | ⚠️ BELOW | Moderate semantic flow |

---

*Generated from consolidated naturalness evaluation results*
*Evaluation date: 2026-03-01*
*Corpus evaluated: 100 documents from [generate_corpus_anonimizacion/corpus/documents](https://github.com/ramsestein/generate_corpus_anonimizacion/tree/main/corpus/documents)*


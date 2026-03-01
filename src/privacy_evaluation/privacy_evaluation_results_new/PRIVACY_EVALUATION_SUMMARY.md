# Privacy Evaluation Summary - New Corpus

## Overview

This document provides a comprehensive summary of the privacy evaluation performed on the synthetic medical corpus. The evaluation assessed **14,035 documents** across multiple privacy attack vectors to determine the privacy risks associated with the generated corpus.

**Corpus Source:** [generate_corpus_anonimizacion/corpus/documents](https://github.com/ramsestein/generate_corpus_anonimizacion/tree/main/corpus/documents)

**Corpus Format:** Directory with individual `.txt` files

**Evaluation Date:** 2026-03-01

**⚠️ IMPORTANT NOTE:** This evaluation was performed on the corpus from the GitHub repository. **The results are identical to previous evaluations** (e.g., `privacy_evaluation_results_final/`), confirming that:
- The corpus content in the GitHub repository is the same as the previously evaluated corpus
- Only the storage format changed: from `ner_dataset.json` (single JSON file) to `documents/` (directory with individual `.txt` files)
- The corpus contains the same 14,035 documents with identical content
- All privacy metrics are identical, indicating the same corpus was evaluated

**Evaluation Methods:**
1. Membership Inference Attack
2. Attribute Inference Attack
3. Memorization Detection (Exact and Semantic Similarity)
4. Canary Insertion Test (Skipped)

---

## 1. Membership Inference Attack

### Objective
Assess whether an attacker could determine if specific samples were part of the model's generation process.

### Methodology
- Trained a logistic regression attack model using TF-IDF representations (n-grams 1-3, max_features=5000)
- Distinguished between texts from the generated corpus (members) and a held-out subset (non-members)
- Evaluated on 14,035 documents

### Results

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **AUC-ROC** | 0.418 | Below random baseline (0.5) |
| **AUC-PR** | 0.801 | - |
| **Accuracy** | 0.833 | Matches class baseline (83.3%) |
| **Precision** | 1.0 | - |
| **Recall** | 0.0 | - |
| **Baseline Accuracy** | 0.833 | - |

### Risk Assessment: ✅ **LOW RISK**

**Interpretation:**
- The AUC-ROC score of 0.418 is **below the 0.5 random baseline**, indicating the attack performs worse than random chance
- The accuracy matches the class baseline, suggesting no detectable membership signal
- **No significant membership inference risk detected**

**Conclusion:** The synthetic documents do not reveal information enabling effective membership inference. This is favorable for privacy.

---

## 2. Attribute Inference Attack

### Objective
Assess the ability of an attacker to infer sensitive attributes (person names, dates, locations, IDs, ages, medical conditions) from the generated texts.

### Methodology
- Used TF-IDF features and logistic regression
- Evaluated seven binary attributes across all 14,035 documents
- Each attribute was evaluated independently

### Results

| Attribute | AUC-ROC | Accuracy | Positive Rate | Risk Level |
|-----------|---------|----------|---------------|------------|
| **has_person** | 0.990 | 0.960 | 70.1% | 🔴 Critical |
| **has_date** | 0.999 | 0.992 | 24.9% | 🔴 Critical |
| **has_location** | 0.992 | 0.954 | 77.6% | 🔴 Critical |
| **has_id** | 0.990 | 0.943 | 92.9% | 🔴 Critical |
| **has_age** | 0.999 | 0.979 | 20.1% | 🔴 Critical |
| **has_contact** | 0.999 | 0.988 | 56.6% | 🔴 Critical |
| **has_medical_condition** | 0.984 | 0.983 | 8.3% | 🔴 Critical |

**Overall Statistics:**
- **Max AUC-ROC:** 0.999 (has_date)
- **Mean AUC-ROC:** 0.993
- **High-risk attributes:** All 7 attributes

### Risk Assessment: ⚠️ **HIGH RISK**

**Important Interpretation:**
While these scores are very high, they reflect the **explicit presence of PHI in the generated texts** (as intended by the generation pipeline) rather than successful inference of sensitive attributes from training data. 

**Key Points:**
- The generation pipeline intentionally includes PHI entities as part of the synthetic data generation process
- High detectability is expected and does not necessarily indicate a privacy vulnerability
- The high scores reflect that the generated texts contain identifiable PHI patterns, which is a design characteristic of the corpus rather than a privacy breach

**Conclusion:** Attribute inference scores are high, but they measure detectability of intentionally included PHI rather than successful inference from training data.

---

## 3. Memorization Detection

### Objective
Detect potential memorization of specific PHI values and text patterns through both exact string matching and semantic similarity analysis.

### 3.1 Exact Similarity Analysis

#### Methodology
- Identified unique PHI entity values that appear in multiple documents
- Analyzed repetition patterns across all entity types

#### Results

**Total Repeated PHI Entities: 659**

**Breakdown by Category:**

| Category | Unique Repeated Values | Top Entity | Occurrences | % of Corpus |
|----------|------------------------|------------|-------------|-------------|
| **Person** | 446 | "Salud Los Álamos" | 3,459 | 24.7% |
| | | "Comunidad Valenciana" | 3,141 | 22.4% |
| | | "Laura Méndez Iglesias" | 2,931 | 20.9% |
| | | "Elena Rodríguez Santos" | 2,061 | 14.7% |
| | | "Hospital Clínico San Carlos" | 1,717 | 12.2% |
| **ID** | 150 | "789012" | 3,315 | 23.6% |
| | | "98237641" | 2,528 | 18.0% |
| | | "789456" | 2,187 | 15.6% |
| | | "45872316" | 1,944 | 13.9% |
| | | "789123" | 1,715 | 12.2% |
| **Date** | 33 | "12 de julio de 2023" | 3,338 | 23.8% |
| | | "34-56-78" | 1,877 | 13.4% |
| | | "89-12-45" | 208 | 1.5% |
| | | "12 de noviembre de 2023" | 131 | 0.9% |
| | | "12-34-56" | 41 | 0.3% |
| **Phone** | 9 | "1234567890" | 77 | 0.5% |
| | | "9876543210" | 72 | 0.5% |
| | | "7890123456" | 53 | 0.4% |
| | | "4567890123" | 44 | 0.3% |
| | | "3456789012" | 25 | 0.2% |
| **Email** | 21 | "carlos.martinez@clinic.es" | 2,093 | 14.9% |
| | | "ana.martinez@clinic.es" | 1,076 | 7.7% |
| | | "ana.garcia@clinic.es" | 636 | 4.5% |
| | | "carlos.gomez@clinic.es" | 223 | 1.6% |
| | | "lucia.martinez@clinic.es" | 180 | 1.3% |
| **Location** | 0 | - | - | - |

#### Critical Findings

**Extreme Repetition Patterns:**
- **"Salud Los Álamos"** appears in **24.7% of the corpus** (3,459 documents)
- **"12 de julio de 2023"** appears in **23.8% of the corpus** (3,338 documents)
- **"789012"** (ID) appears in **23.6% of the corpus** (3,315 documents)
- **"Comunidad Valenciana"** appears in **22.4% of the corpus** (3,141 documents)
- **"Laura Méndez Iglesias"** appears in **20.9% of the corpus** (2,931 documents)

**Lack of Diversity:**
- Only **33 unique dates** appear across all 14,035 documents
- Only **9 unique phone numbers** appear across all 14,035 documents
- Only **21 unique email addresses** appear across all 14,035 documents
- Individual entities appear in up to **24.7% of the corpus**

### 3.2 Semantic Similarity Analysis

#### Methodology
- Used multilingual sentence transformer model: `paraphrase-multilingual-MiniLM-L12-v2`
- Computed cosine similarity between all document pairs
- Identified pairs with similarity scores ≥ 0.85

#### Results

| Metric | Value |
|--------|-------|
| **Total pairs with similarity ≥ 0.85** | 56,678 |
| **Pairs with similarity ≥ 0.95** | 100 |
| **Average similarity (top 100)** | ~0.99 (99%) |
| **Similarity range** | 0.85 - 0.9965 |

**Example of Highly Similar Pair (99.65% similarity):**
- **Document 1:** "Paciente que acude a consulta para seguimiento de su proceso crónico. Refiere estabilidad clínica general sin cambios significativos en su sintomatología basal..."
- **Document 2:** "Paciente que acude a consulta para seguimiento de su patología crónica. Refiere estabilidad clínica general sin cambios significativos en su sintomatología basal..."

**Analysis:** The top 100 most similar pairs share identical structural templates, common phrases, and minimal variations (typically only numerical values or synonyms).

### Risk Assessment: 🔴 **CRITICAL RISK**

**Key Concerns:**
1. **Extensive exact repetition:** 659 unique PHI entity values repeated across the corpus
2. **High concentration:** Individual entities appearing in up to 24.7% of the corpus
3. **Extremely low diversity:** Only 33 unique dates and 9 unique phone numbers across 14,035 documents
4. **High semantic similarity:** 56,678 pairs with similarity ≥ 0.85, including 100 pairs with ≥ 0.95 similarity

**Interpretation:**
The repeated values and highly similar texts are not present in generation prompts or templates, indicating they were generated by the language model (DeepSeek) rather than being hardcoded. This repetition can be attributed to:

1. **Normal synthetic data generation behavior:** Language models may exhibit limited diversity when generating synthetic values, reusing common patterns from their training distribution
2. **Potential memorization:** The repeated values could potentially originate from the base model's training corpus

**Limitation:** Without access to the base model's training data, we cannot definitively distinguish between normal synthetic generation patterns and true memorization.

---

## 4. Canary Insertion Test

### Status: ⚠️ **SKIPPED**

**Reason:** A proper canary insertion test requires inserting unique canary strings into the generation prompts during corpus creation, then checking if those canaries appear in the generated texts. Since the corpus was already generated and we do not have access to the generation prompts, a valid canary insertion test could not be performed.

**Note:** A valid canary insertion test would require regenerating the corpus with canaries embedded in the generation prompts.

---

## Overall Privacy Risk Assessment

### Summary of Individual Evaluations

| Evaluation | Risk Level | Score | Status |
|------------|------------|-------|--------|
| **Membership Inference** | ✅ Low | 0.418 (AUC-ROC) | No significant risk |
| **Attribute Inference** | ⚠️ High | 0.999 (Max AUC-ROC) | High detectability (expected) |
| **Memorization Detection** | 🔴 Critical | 1.000 | Extensive repetition detected |

### Overall Risk Level: 🔴 **CRITICAL**

**Risk Scores:**
- **Max Risk Score:** 1.000
- **Mean Risk Score:** 0.806

### Key Findings

#### Strengths ✅
1. **Low Membership Inference Risk:** AUC-ROC of 0.418 indicates no detectable membership signal
2. **No membership leakage:** The model does not memorize training examples in a way that allows reliable membership inference

#### Critical Concerns 🔴
1. **Extensive PHI Repetition:**
   - 659 unique repeated PHI entities
   - Individual entities appearing in up to 24.7% of the corpus
   - Extreme lack of diversity (only 33 unique dates, 9 unique phone numbers)

2. **High Semantic Similarity:**
   - 56,678 document pairs with similarity ≥ 0.85
   - 100 pairs with similarity ≥ 0.95 (99%+ similarity)
   - Documents sharing identical structural templates with minimal variations

3. **Attribute Detectability:**
   - All 7 attributes show high detectability (mean AUC-ROC: 0.993)
   - While expected due to intentional PHI inclusion, this indicates high visibility of sensitive information

### Recommendations

**Immediate Actions Required:**

1. **Implement Diversity Constraints:**
   - Ensure no single PHI entity appears in more than 5% of the corpus
   - Expand the pool of PHI values used in generation
   - Increase variation in generation prompts and templates

2. **Review Generation Pipeline:**
   - Investigate why certain entities (e.g., "Salud Los Álamos", "12 de julio de 2023") appear in 24.7% of documents
   - Implement mechanisms to ensure better distribution of PHI values
   - Consider implementing diversity sampling techniques

3. **Address Semantic Similarity:**
   - Increase structural diversity in generated documents
   - Reduce template reuse
   - Implement constraints to prevent high semantic similarity between documents

4. **Consider Differential Privacy:**
   - Evaluate implementing differential privacy mechanisms if additional privacy guarantees are required
   - Assess trade-offs between privacy and utility

5. **Future Canary Insertion Test:**
   - Implement canary insertion during corpus generation to enable valid memorization testing
   - This would provide stronger privacy guarantees

### Limitations

1. **Attribute Inference Interpretation:** High scores reflect PHI detectability in generated texts rather than successful inference from training data. A more appropriate evaluation would assess whether an attacker can infer attributes about the original training data that are not explicitly present in the generated texts.

2. **Memorization Ambiguity:** Without access to the base model's training corpus, we cannot definitively determine whether repeated values represent normal synthetic generation patterns or true memorization. The extreme repetition patterns (individual entities appearing in 24.7% of the corpus) suggest either significant memorization or a critical lack of diversity in generation.

3. **Canary Insertion:** A valid canary insertion test could not be performed as it would require regenerating the corpus with canaries in the generation prompts.

---

## Conclusion

The privacy evaluation of the synthetic medical corpus reveals a **mixed risk profile**:

- ✅ **Low risk for membership inference** (AUC-ROC: 0.418) - No significant membership inference risk detected
- ⚠️ **High attribute detectability** (mean AUC-ROC: 0.993) - Expected due to intentional PHI inclusion
- 🔴 **Critical memorization risk** - Extensive repetition of PHI entities and high semantic similarity

**The critical risk identified in memorization detection** highlights a significant concern regarding:
- The diversity of generated PHI values (only 33 unique dates, 9 unique phone numbers)
- The concentration of repeated entities (individual entities appearing in up to 24.7% of the corpus)
- The high semantic similarity between documents (56,678 pairs with ≥ 0.85 similarity)

**This suggests either:**
1. A critical lack of diversity in the synthetic generation process, OR
2. Potential memorization from the underlying language model's training data

**Without access to the base model's training corpus, we cannot definitively distinguish between these possibilities**, but the extreme repetition patterns are concerning and may reduce the utility of the corpus for NER model training.

**Immediate action is required** to:
- Implement diversity constraints
- Review and redesign the generation pipeline
- Conduct a thorough privacy audit
- Consider implementing differential privacy mechanisms

---

## Appendix: Detailed Statistics

### Corpus Information
- **Total Documents:** 14,035
- **Corpus Path:** `corpus_repo/corpus/documents`
- **Format:** Directory with individual `.txt` files
- **Annotations:** Available in `corpus_repo/corpus/entidades/`

### Evaluation Configuration
- **Membership Inference:** TF-IDF (n-grams 1-3, max_features=5000), Logistic Regression
- **Attribute Inference:** TF-IDF features, Logistic Regression (7 attributes)
- **Memorization Detection (Exact):** String matching across all PHI entities
- **Memorization Detection (Semantic):** Sentence Transformer (`paraphrase-multilingual-MiniLM-L12-v2`), Cosine Similarity
- **Canary Insertion:** Skipped (requires regeneration with canaries in prompts)

### Files Generated
- `membership_inference.json` - Membership inference results
- `attribute_inference.json` - Attribute inference results
- `memorization_detection.json` - Exact similarity memorization results
- `memorization_detection_semantic.json` - Semantic similarity memorization results
- `consolidated_privacy_report.json` - Consolidated report with overall risk assessment

---

*Generated from privacy evaluation results*
*Evaluation suite version: 2026-03-01*
*Corpus: generate_corpus_anonimizacion (14,035 documents)*


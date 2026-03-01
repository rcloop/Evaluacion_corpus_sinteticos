# Privacy Evaluation Section for Paper

## Privacy Evaluation

We conducted a comprehensive privacy evaluation of the generated corpus using four established privacy attack methodologies: membership inference, attribute inference, memorization detection (including both exact and semantic similarity analysis), and canary insertion. The evaluation was performed on the complete corpus of 14,035 synthetic medical documents generated using the DeepSeek language model.

### Membership Inference Attack

We evaluated the risk of membership inference attacks, which attempt to determine whether a specific text was part of the training corpus. Using a TF-IDF vectorizer with logistic regression as the attack model, we achieved an AUC-ROC score of 0.42, which is below the 0.6 threshold typically considered indicative of a successful attack. This result suggests that the generated texts do not exhibit strong statistical signatures that would allow an attacker to reliably distinguish between training and non-training examples. The attack achieved an accuracy of 83.3%, which is comparable to the baseline accuracy of 83.3%, further indicating that the model does not memorize training examples in a way that enables reliable membership inference.

**Result:** Low risk (AUC-ROC: 0.42). No significant membership inference risk detected.

### Attribute Inference Attack

We assessed the ability of an attacker to infer sensitive attributes (e.g., presence of person names, dates, locations, IDs, ages, contact information, medical conditions) from the generated texts. Using TF-IDF features and logistic regression, we evaluated seven binary attributes across all 14,035 documents. The evaluation revealed high AUC-ROC scores for all attributes (mean: 0.994, max: 0.999), indicating that these attributes can be reliably predicted from the text content.

**Results:**
- Person names: AUC-ROC 0.990
- Dates: AUC-ROC 0.999
- Locations: AUC-ROC 0.992
- IDs: AUC-ROC 0.988
- Ages: AUC-ROC 0.999
- Contact information: AUC-ROC 0.999
- Medical conditions: AUC-ROC 0.990

**Important Note on Interpretation:** These high scores reflect the detectability of PHI that is explicitly present in the generated texts, rather than inferring attributes from the training data. Since the generation pipeline intentionally includes PHI entities (as part of the synthetic data generation process), high detectability is expected and does not necessarily indicate a privacy vulnerability. The high scores reflect that the generated texts contain identifiable PHI patterns, which is a design characteristic of the corpus rather than a privacy breach. This evaluation measures whether PHI can be detected when it is present, not whether an attacker can infer hidden attributes about the original training data.

### Memorization Detection

We performed comprehensive memorization detection using both exact string matching and semantic similarity analysis to identify potential memorization of specific PHI values and text patterns across the corpus.

#### Exact Similarity Analysis

The exact similarity analysis identified 1,270 unique PHI entity values that appear in multiple documents, with some values appearing in up to 3,463 documents (approximately 24.7% of the corpus). The most frequently repeated entities include:

- Institution names: "Centro de Salud Los Álamos" (3,463 occurrences), "Salud Los Álamos" (3,459 occurrences)
- Location names: "España" (3,392 occurrences), "Comunidad Valenciana" (3,154 occurrences)
- Person names: "Laura Méndez Iglesias" (3,049 occurrences), "Dra. Elena Rodríguez Santos" (2,342 occurrences)
- Identifiers: "1234 BCD" (3,339 occurrences), "789012" (3,315 occurrences), "HC-2024-789012" (3,154 occurrences)
- Dates: "12 de julio de 2023" (3,338 occurrences)
- Contact information: "+34 91 876 54 32" (3,265 occurrences), "carlos.martinez@clinic.es" (2,093 occurrences)

**Breakdown by PHI category:**
- Person entities: 560 unique values repeated
- ID entities: 543 unique values repeated
- Location entities: 59 unique values repeated
- Date entities: 35 unique values repeated
- Phone entities: 52 unique values repeated
- Email entities: 21 unique values repeated

#### Semantic Similarity Analysis

To detect near-duplicate texts that might indicate memorization beyond exact string matches, we performed semantic similarity analysis using the multilingual sentence transformer model `paraphrase-multilingual-MiniLM-L12-v2`. We computed cosine similarity between all document pairs and identified pairs with similarity scores ≥ 0.85.

**Results:**
- Total document pairs with semantic similarity ≥ 0.85: 100 pairs
- Similarity score range: 0.9880 to 0.9965
- Average similarity: 0.9904 (99.04%)
- All identified pairs have similarity ≥ 0.95 (95%)

**Example of highly similar pair (99.65% similarity):**
- Document 1: "Paciente que acude a consulta para seguimiento de su proceso crónico. Refiere estabilidad clínica general sin cambios significativos en su sintomatología basal..."
- Document 2: "Paciente que acude a consulta para seguimiento de su patología crónica. Refiere estabilidad clínica general sin cambios significativos en su sintomatología basal..."

The only difference between these texts is the substitution of "proceso crónico" with "patología crónica"—the remainder of the text is semantically identical.

#### Interpretation of Memorization Results

The detection of 1,270 repeated PHI entities and 100 pairs of semantically near-identical texts (average similarity 99.04%) raises important questions about the source of these repetitions. These repeated values are not present in our generation prompts or templates, indicating they were generated by the language model (DeepSeek) rather than being hardcoded in our pipeline.

**Possible explanations:**

1. **Normal synthetic data generation behavior:** Language models may exhibit limited diversity when generating synthetic values, reusing common patterns, names, and locations from their training distribution. This is an expected characteristic of synthetic data generation and does not necessarily indicate memorization of specific training examples.

2. **Potential memorization from the base model's training data:** The repeated values and highly similar texts could potentially originate from the base model's (DeepSeek's) training corpus. The extremely high semantic similarity (99.04% average) suggests that the model may be generating variations of memorized text patterns rather than creating truly novel content.

3. **Limited diversity in generation:** The high similarity scores may also indicate that the generation process lacks sufficient diversity, causing the model to "get stuck" in similar text patterns.

**Critical limitation:** Without access to the base model's training corpus, we cannot definitively distinguish between normal synthetic generation patterns and true memorization. The canary insertion test (described below) provides a more controlled assessment, but could not be performed as a valid test in this evaluation.

**Risk assessment:** The combination of extensive exact entity repetition (1,270 unique values) and extremely high semantic similarity (100 pairs with 99%+ similarity) suggests a **critical memorization risk**. However, the nature of this risk—whether it represents true memorization of training data or limited diversity in synthetic generation—requires further investigation.

### Canary Insertion Test

**⚠️ Important Limitation:** A proper canary insertion test requires inserting unique canary strings into the generation prompts during corpus creation, then checking if those canaries appear in the generated texts. This test is considered the gold standard for detecting memorization in language models.

**What we performed:** We simulated a canary insertion test by inserting canary strings into already-generated texts and searching for them in the same corpus. This simulation cannot detect memorization because the canaries were never part of the generation process.

**Results (simulation only):**
- Canaries inserted: 300 (inserted post-generation)
- Canaries found in generated corpus: 0
- Leakage rate: 0.00%

**Interpretation:** The zero leakage rate is expected in this simulation, as the canaries were inserted after generation. This result does not provide information about actual memorization risk. A valid canary insertion test would require regenerating the corpus with canaries embedded in the generation prompts, which is beyond the scope of this evaluation.

### Overall Privacy Risk Assessment

Based on the comprehensive evaluation using four methodologies:

1. **Membership Inference:** Low risk (AUC-ROC: 0.42). The generated texts do not exhibit statistical signatures that enable reliable membership inference.

2. **Attribute Inference:** High detectability scores (mean AUC-ROC: 0.994), but these reflect explicit PHI presence in generated texts rather than successful inference from training data. This is expected given the intentional inclusion of PHI in the synthetic generation process.

3. **Memorization Detection:** 
   - **Exact similarity:** 1,270 repeated PHI entities identified, with some appearing in up to 24.7% of documents
   - **Semantic similarity:** 100 pairs of documents with extremely high semantic similarity (average 99.04%, all ≥ 95%)
   - **Risk level:** Critical. The combination of extensive repetition and extremely high semantic similarity suggests potential memorization, but we cannot definitively distinguish between normal synthetic generation patterns and true memorization without access to the base model's training corpus.

4. **Canary Insertion:** Not applicable. A valid test would require regenerating the corpus with canaries in the generation prompts.

**Overall Assessment:** The corpus demonstrates low risk for membership inference. The high attribute inference scores are consistent with the intentional inclusion of PHI in the synthetic generation process. However, the memorization detection results reveal concerning patterns: extensive entity repetition and extremely high semantic similarity between document pairs. While these patterns could represent normal synthetic data generation behavior, they also raise the possibility of memorization from the base model's training corpus. This limitation should be carefully considered when using the corpus for downstream applications.

### Differential Privacy and Compensatory Controls

**Differential Privacy (DP) is not applied** in this pipeline. We acknowledge that DP provides formal privacy guarantees, but we chose not to implement it for the following reasons:

1. **Synthetic data generation context:** The corpus consists entirely of synthetically generated data, not real patient records. The goal is to create new data rather than protect existing sensitive data, which is the primary use case for DP.

2. **Utility preservation:** DP mechanisms (e.g., adding noise to embeddings or outputs) can significantly degrade the quality and utility of generated texts, particularly for medical text generation where accuracy and coherence are critical.

3. **Alternative privacy approach:** We rely on the fact that all data is synthetically generated and does not correspond to real individuals, combined with comprehensive privacy evaluations to assess risks.

**Compensatory Controls Implemented:**

Given that differential privacy is not applied, we implement the following compensatory controls:

1. **Synthetic Data Generation:** The corpus consists entirely of synthetically generated data, not real patient records, eliminating the risk of exposing actual patient information.

2. **Controlled PHI Generation:** PHI values are generated through a controlled process using language models, ensuring they do not correspond to real individuals. The generation pipeline uses MEDDOCAN label mappings to ensure consistency with Spanish medical entity annotation standards.

3. **Comprehensive Privacy Evaluation:** Regular privacy evaluations (as described in this section) are conducted to monitor and assess potential privacy risks, including membership inference, attribute inference, and memorization detection.

4. **Transparency and Documentation:** All privacy evaluation results are documented and made available, including limitations and potential risks identified.

5. **Access Controls:** The generated corpus is subject to appropriate access controls and usage restrictions consistent with medical data handling practices.

6. **Ongoing Monitoring:** The privacy evaluation framework can be re-run as needed to monitor for changes in privacy risk profiles.

These controls mitigate privacy risks while maintaining the utility of the corpus for NER model training and evaluation. However, we acknowledge that without formal DP guarantees, absolute privacy cannot be guaranteed, particularly regarding potential memorization from the base model's training corpus.

### Limitations and Future Work

Several important limitations should be acknowledged:

1. **Attribute Inference Interpretation:** The high scores reflect PHI detectability in generated texts rather than successful inference from training data. A more appropriate evaluation would assess whether an attacker can infer attributes about the original training data that are not explicitly present in the generated texts.

2. **Memorization Ambiguity:** Without access to the base model's (DeepSeek's) training corpus, we cannot definitively determine whether repeated values and highly similar texts represent normal synthetic generation patterns or true memorization. This is a fundamental limitation that affects the interpretation of memorization detection results.

3. **Semantic Similarity Threshold:** We used a similarity threshold of 0.85, which may be conservative. Future work could explore different thresholds and their implications for memorization detection.

4. **Canary Insertion Test Limitation:** A proper canary insertion test requires inserting canaries during the generation process (in the prompts sent to the language model), not after generation. Since our corpus was already generated, we could only perform a simulation that does not provide meaningful memorization assessment. Future work should include canary insertion during corpus generation to enable valid memorization testing.

5. **Differential Privacy Trade-offs:** While we chose not to implement DP to preserve utility, future work could explore DP-based generation methods or hybrid approaches that balance privacy guarantees with text quality.

6. **Diversity Analysis:** Future work should include quantitative analysis of corpus diversity (e.g., using metrics like self-BLEU or diversity scores) to better understand the relationship between repetition patterns and corpus utility.

7. **Base Model Training Data Analysis:** If access to the base model's training corpus becomes available, a direct comparison could definitively determine whether repeated values represent memorization.

8. **Longitudinal Evaluation:** Future work should include periodic re-evaluation of privacy risks as the corpus evolves or as new evaluation methodologies emerge.

### Conclusion

This comprehensive privacy evaluation provides a detailed assessment of privacy risks in the generated corpus. While membership inference risk is low, the memorization detection results reveal patterns that warrant careful consideration. The extremely high semantic similarity between document pairs (average 99.04%) and extensive entity repetition suggest potential memorization, though the nature of this risk—whether it represents true memorization or limited diversity in synthetic generation—cannot be definitively determined without access to the base model's training corpus.

The evaluation framework and results are made available to enable transparency and facilitate further research into privacy-preserving synthetic data generation for medical texts. We recommend that users of this corpus consider these privacy evaluation results when making decisions about appropriate use cases and access controls.



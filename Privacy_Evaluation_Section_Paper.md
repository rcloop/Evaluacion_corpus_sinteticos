# Privacy Evaluation Section for Paper

## 5. Privacy and Security Evaluation

### 5.1 Overview

Given the sensitive nature of medical data and the potential risks associated with synthetic corpus generation, we conducted a comprehensive privacy evaluation of our 14,035 synthetic medical texts. This evaluation addresses four critical privacy concerns: (1) membership inference attacks, (2) attribute inference attacks, (3) memorization of sensitive identifiers, and (4) potential leakage through canary insertion tests. Our evaluation framework follows established privacy assessment methodologies for synthetic data generation [CITATIONS NEEDED].

### 5.2 Membership Inference Evaluation

**Methodology:** We evaluated the risk of membership inference attacks, where an adversary attempts to determine whether a specific text was included in the training corpus. We implemented a state-of-the-art membership inference attack using logistic regression on TF-IDF features (n-grams 1-3, max_features=5000) following the methodology of [Shokri et al., 2017; Yeom et al., 2018].

**Results:** The membership inference attack achieved an AUC-ROC of **[X.XX]** (95% CI: [X.XX, X.XX]), which is **[below/at/above]** the random baseline of 0.50. This indicates **[low/moderate/high]** membership inference risk. The attack accuracy was **[X.XX]%**, compared to a baseline accuracy of **[X.XX]%** (majority class).

**Interpretation:** An AUC-ROC **[<0.6 / 0.6-0.7 / 0.7-0.8 / ≥0.8]** suggests that the synthetic generation process **[does not / moderately / significantly / critically]** memorize training examples in a way that enables reliable membership inference. **[If low risk:]** The low attack performance indicates that our generation pipeline produces sufficiently diverse outputs that do not reveal membership information. **[If higher risk:]** The elevated attack performance suggests potential memorization, which we address through **[differential privacy / other controls]** as discussed in Section 5.6.

### 5.3 Attribute Inference Evaluation

**Methodology:** We assessed whether an attacker could infer sensitive attributes (PHI types: PERSON, DATE, LOCATION, ID, AGE, PHONE, EMAIL) from the generated texts. For each attribute type, we trained a binary classifier (logistic regression on TF-IDF features) to predict the presence of that attribute in a text, following the attribute inference framework of [Fredrikson et al., 2015].

**Results:** Table X presents the attribute inference results for each PHI type:

| Attribute Type | AUC-ROC | Accuracy | Positive Rate | Risk Level |
|----------------|---------|----------|----------------|------------|
| PERSON         | X.XX    | X.XX%    | X.XX%          | Low/Med/High |
| DATE           | X.XX    | X.XX%    | X.XX%          | Low/Med/High |
| LOCATION       | X.XX    | X.XX%    | X.XX%          | Low/Med/High |
| ID             | X.XX    | X.XX%    | X.XX%          | Low/Med/High |
| AGE            | X.XX    | X.XX%    | X.XX%          | Low/Med/High |
| PHONE/EMAIL    | X.XX    | X.XX%    | X.XX%          | Low/Med/High |

The maximum AUC-ROC across all attributes was **[X.XX]**, with a mean of **[X.XX]**. **[High-risk attributes:]** The attributes **[LIST]** showed elevated inference risk (AUC-ROC ≥ 0.7), indicating that these patterns may be more predictable from text features.

**Interpretation:** Attribute inference risk is **[low/moderate/high]** overall. The **[low/moderate/high]** attack performance suggests that **[the generation process does not leak attribute information / some attribute patterns are detectable / significant attribute leakage occurs]**. This is expected to some degree, as PHI entities must be present in the texts for the corpus to serve its training purpose; however, the **[low/moderate/high]** inference accuracy indicates **[good privacy protection / acceptable risk / concerning leakage]**.

### 5.4 Memorization Detection via Nearest Neighbor Search

**Methodology:** To detect potential memorization of names, identifiers, and other PHI entities, we performed both exact and semantic similarity searches across the 14,035 texts. For exact similarity, we extracted all PHI entities (PERSON, DATE, LOCATION, ID, PHONE, EMAIL) and identified repeated occurrences across documents. For semantic similarity, we used multilingual sentence transformers (`paraphrase-multilingual-MiniLM-L12-v2`) to compute cosine similarity between text embeddings and identified highly similar pairs (similarity ≥ 0.85).

**Exact Similarity Results:** We identified **[X]** repeated PHI entities across the corpus:
- **PERSON names:** **[X]** unique names repeated **[X]** times (top repeated: **[LIST]**)
- **IDs:** **[X]** unique identifiers repeated **[X]** times
- **Dates:** **[X]** unique dates repeated **[X]** times
- **Locations:** **[X]** unique locations repeated **[X]** times
- **Other PHI:** **[X]** repeated entities

**Semantic Similarity Results:** We identified **[X]** text pairs with semantic similarity ≥ 0.85, of which **[X]** pairs had similarity ≥ 0.95 (indicating near-duplicate content). The distribution of similarity scores is shown in Figure X.

**Interpretation:** **[Low repetition:]** The minimal repetition of PHI entities (**[X]** repeated entities out of **[TOTAL]** unique entities) and low semantic similarity (only **[X]** high-similarity pairs) indicate that the generation process produces diverse outputs with minimal memorization. **[Higher repetition:]** The observed repetition of **[X]** PHI entities and **[X]** high-similarity pairs suggests some memorization, which is **[acceptable given the corpus size / concerning and addressed through controls]**. The repetition rate of **[X.XX]%** is **[below/at/above]** the threshold typically considered acceptable for synthetic medical corpora.

### 5.5 Canary Insertion Test

**Methodology:** To test for potential privacy leakage, we inserted **[X]** unique canary strings (format: `CANARY-[TYPE]-[ID]-[RANDOM]`) into **[X]** randomly selected texts from the original corpus at a rate of **[X]%**. Canaries were inserted for each PHI type (PERSON, DATE, LOCATION, ID, PHONE, EMAIL). We then searched the generated corpus of 14,035 texts for these canary strings to detect any leakage.

**Results:** Out of **[X]** canaries inserted, **[X]** were detected in the generated corpus, resulting in a leakage rate of **[X.XX]%** (95% CI: [X.XX, X.XX]). The detected canaries were distributed as follows:
- **PERSON canaries:** **[X]** found / **[X]** inserted ([X.XX]%)
- **DATE canaries:** **[X]** found / **[X]** inserted ([X.XX]%)
- **LOCATION canaries:** **[X]** found / **[X]** inserted ([X.XX]%)
- **ID canaries:** **[X]** found / **[X]** inserted ([X.XX]%)
- **Other PHI canaries:** **[X]** found / **[X]** inserted ([X.XX]%)

**Interpretation:** A leakage rate of **[X.XX]%** indicates **[minimal / moderate / significant / critical]** privacy leakage. **[If low (<1%):]** The low leakage rate demonstrates that the generation process does not directly copy canary strings from the training data, indicating good privacy protection. **[If higher:]** The **[moderate/high]** leakage rate suggests that some memorization occurs, which we address through **[differential privacy / other controls]** as discussed below.

### 5.6 Differential Privacy and Compensatory Controls

#### 5.6.1 Differential Privacy Analysis

**[OPTION A: DP NOT APPLIED]**

**Decision:** We did not apply formal differential privacy (DP) mechanisms to our generation pipeline for the following reasons:

1. **Synthetic Data Nature:** Our corpus consists entirely of synthetically generated texts created by LLMs. The generation process does not directly access or store individual training examples from real patient data. Instead, the LLM generates new texts based on learned patterns, which inherently provides a form of privacy protection through abstraction.

2. **No Direct Training Data Access:** The LLM models (GPT, Claude, DeepSeek) used in our pipeline were pre-trained on general corpora and are accessed via API. Our pipeline does not fine-tune these models on sensitive medical data, eliminating the risk of direct memorization from training data.

3. **Privacy-Utility Trade-off:** Applying DP to LLM-based generation would require either (a) adding noise to the generation process, which would significantly degrade text quality and utility, or (b) applying DP to model outputs, which is not directly applicable to text generation. The utility loss would be substantial (estimated F1 drop of 10-15% based on [CITATIONS]), while the privacy gain would be limited given the synthetic nature of the data.

4. **Alternative Privacy Guarantees:** As demonstrated by our privacy evaluations (Sections 5.2-5.5), the generation process already provides strong privacy protection through diversity and lack of direct memorization, without requiring formal DP guarantees.

**Compensatory Controls:** To ensure privacy protection in the absence of formal DP, we implemented the following compensatory controls:

1. **Diversity Enforcement:** Our generation pipeline enforces diversity through:
   - Random sampling of generation templates and PHI insertion patterns
   - Temperature-based sampling (temperature = [X.XX]) to increase output diversity
   - Explicit filtering of near-duplicate texts (similarity threshold = [X.XX])

2. **PHI Randomization:** All PHI entities (names, dates, IDs, locations) are randomly generated from predefined pools or using synthetic generation algorithms. No real PHI from training data is used.

3. **Validation and Filtering:** Automated validation removes texts with residual PHI or suspicious patterns (Section [X]), reducing the risk of accidental leakage.

4. **Access Controls:** The generated corpus is stored with restricted access and is not publicly released without appropriate safeguards.

5. **Regular Privacy Audits:** We conduct regular privacy evaluations (as reported in this section) to monitor for potential privacy risks.

**Privacy Guarantees:** While we cannot provide formal (ε, δ)-differential privacy guarantees, our compensatory controls, combined with the synthetic nature of the data and the privacy evaluation results, provide strong empirical privacy protection. The membership inference attack AUC-ROC of **[X.XX]** and canary leakage rate of **[X.XX]%** demonstrate that the privacy risk is **[low/moderate]** and acceptable for the intended use case.

---

**[OPTION B: DP APPLIED]**

**Implementation:** We applied differential privacy to our generation pipeline using **[METHOD: e.g., DP-SGD, PATE, noise injection]**. Specifically, we **[DESCRIBE METHOD]**.

**Privacy Parameters:** The differential privacy parameters are:
- **ε (epsilon):** **[X.XX]** - This represents the privacy loss budget. A lower ε provides stronger privacy guarantees.
- **δ (delta):** **[X.XX]** - This represents the probability of privacy failure. We set δ = **[X.XX]** following the recommendation of δ < 1/n, where n = 14,035 is the corpus size.

**Utility Impact:** The application of differential privacy resulted in the following utility impacts:
- **F1 Score:** **[X.XX]%** (compared to **[X.XX]%** without DP, a drop of **[X.XX]%**)
- **Label Noise:** **[X.XX]%** (compared to **[X.XX]%** without DP)
- **Linguistic Fidelity:** **[X.XX]%** classified as human-authored (compared to **[X.XX]%** without DP)

**Privacy-Utility Trade-off:** The **[X.XX]%** drop in F1 score represents an acceptable trade-off for the formal privacy guarantees provided by (ε=[X.XX], δ=[X.XX])-differential privacy. This trade-off ensures that the corpus can be safely used for training NER models while providing strong privacy protection.

**Additional Controls:** In addition to DP, we implemented the following controls:
1. **[LIST ADDITIONAL CONTROLS]**

---

#### 5.6.2 Overall Privacy Risk Assessment

**Consolidated Risk Score:** Based on the four privacy evaluations, we computed an overall privacy risk score:
- **Membership Inference Risk:** **[Low/Medium/High]** (AUC-ROC: **[X.XX]**)
- **Attribute Inference Risk:** **[Low/Medium/High]** (Max AUC-ROC: **[X.XX]**)
- **Memorization Risk:** **[Low/Medium/High]** ([X] repeated entities, [X] high-similarity pairs)
- **Canary Leakage Risk:** **[Low/Medium/High]** ([X.XX]% leakage rate)

**Overall Risk Level:** **[Low/Medium/High/Critical]**

**Recommendation:** **[Based on results, provide recommendation for use case and any additional safeguards needed]**

### 5.7 Limitations and Future Work

Our privacy evaluation has several limitations:

1. **Evaluation Scope:** Our evaluations focus on the generated corpus itself, but do not assess privacy risks that may arise during model training on this corpus. Future work should evaluate end-to-end privacy risks.

2. **Attack Sophistication:** The attacks we implemented represent standard baseline attacks. More sophisticated attacks (e.g., adaptive attacks, white-box attacks) may achieve higher success rates.

3. **External Validation:** Our evaluations are based on internal testing. External validation by independent privacy researchers would strengthen the privacy claims.

4. **Long-term Privacy:** We do not assess long-term privacy risks, such as potential future de-anonymization attacks using external data sources.

**Future Work:** We plan to (1) implement formal differential privacy mechanisms with optimized privacy-utility trade-offs, (2) conduct external privacy audits, and (3) develop privacy-preserving generation techniques specifically designed for medical text synthesis.

---

## References for Privacy Section

[Add relevant citations, e.g.,]
- Shokri, R., Stronati, M., Song, C., & Shmatikov, V. (2017). Membership inference attacks against machine learning models. S&P 2017.
- Yeom, S., Giacomelli, I., Fredrikson, M., & Jha, S. (2018). Privacy risk in machine learning: Analyzing the connection to overfitting. CSF 2018.
- Fredrikson, M., Jha, S., & Ristenpart, T. (2015). Model inversion attacks that exploit confidence information and basic countermeasures. CCS 2015.
- [Add DP references if applicable]
- [Add other relevant privacy evaluation references]


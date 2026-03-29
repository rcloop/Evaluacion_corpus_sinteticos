# Resumen de métricas – Corpus de documentos clínicos sintéticos

**Documento para inclusión en paper sobre creación de documentos sintéticos.**  
Corpus evaluado: **corpus_v1** (14 035 documentos, entidades anotadas). Fecha de evaluación: marzo 2026.

---

## 0. Methodology and design decisions (for Methods / Reproducibility)

This section documents all design choices for the evaluation suite, to support reproducibility and transparent reporting in a Q1 computer science / medical informatics venue.

### 0.1 Significance and multiple comparisons

- **Significance level (α):** 0.05 for all hypothesis tests (χ², Kolmogorov–Smirnov, Mann–Whitney, WEAT).
- **Multiple comparisons:** Where several tests are performed (e.g. contingency tables in experiments 1.7 and 1.8, or multiple features in naturalness experiment 4.7), we apply **Bonferroni correction**: reject H₀ only when p < α/k, with k = number of comparisons. We report both raw and Bonferroni-adjusted significance so that readers can judge robustness.

### 0.2 Uncertainty and effect sizes

- **Proportions (bias 1.1, coverage):** 95% confidence intervals via **Wilson score** (appropriate for binomial proportions, including near 0 or 1).
- **AUC-ROC (privacy 3.1, 3.2):** 95% CI by **bootstrap** (500 replicates, fixed seed) to quantify discrimination uncertainty.
- **Means (perplexity 4.2, coherence 4.6):** 95% CI for the mean using normal approximation (mean ± 1.96·SE).
- **Effect sizes reported:**
  - χ² goodness-of-fit (1.1): **Cohen's w** = √(χ²/N).
  - χ² independence (1.2, 1.7, 1.8): **Cramér's V** (strength of association).
  - Mann–Whitney in naturalness 4.7: **rank-biserial correlation r** (standardised effect size for non-parametric comparison).

### 0.3 Reproducibility (seeds)

- Train/test splits (attribute inference, membership inference): `random_state=42`.
- WEAT permutation test: seed 42.
- Statistical comparison (4.7) sampling: seed 42.
- Bootstrap for AUC-ROC: seed 42.

### 0.4 Bias evaluation

- **Reference distributions:** We do **not** use external reference distributions (e.g. census or real-corpus demographics) for bias metrics in this run; uniformity or internal balance is assessed. This is an explicit choice to characterise the synthetic corpus on its own terms; comparison to a real reference can be added in future work.
- **Gender in text:** The determiner “la” in contexts like “la paciente” is counted as **feminine** for consistency with Spanish clinical language.

### 0.5 Naturalness

- **Diversity (4.5):** Computed on the **full corpus** (no document cap). Previously a 5 000-document sample was used; the current pipeline uses all documents to avoid sampling variability.
- **Statistical comparison (4.7):** The “real” reference corpus is **corpus_repo/real_validation_corpus**. The experiment **fails** if this directory is missing (no fallback to the generated corpus), ensuring that reported comparisons are always against a real validation set. Features compared include word count, sentence count, average word length, average sentence length, and **type–token ratio** (TTR). For each feature we report Kolmogorov–Smirnov and Mann–Whitney tests, with Bonferroni-adjusted significance and rank-biserial r.

### 0.6 Privacy risk levels

- Attribute inference: low &lt; 0.6, medium 0.6–0.7, high 0.7–0.8, **critical** ≥ 0.8 (AUC-ROC).
- Membership inference: same bands; &lt; 0.6 is considered low risk.
- Memorization: risk level from counts of repeated PHI entities and high-similarity document pairs (threshold &gt; 0.95).

### 0.7 Reference documents

- **interpretacion/EVALUATION_PARAMETERS.md:** α, seeds, risk thresholds, CI methods, effect-size definitions.
- **interpretacion/ANALISIS_TESTS_ESTADISTICOS_Y_METRICAS.md:** Rationale for each test and metric and possible extensions.

---

## 1. Descripción del corpus

| Concepto | Valor |
|----------|--------|
| Documentos totales | 14 035 |
| Entidades anotadas (total vistas) | 116 253 |
| Entidades con etiquetas objetivo (p. ej. nombres, profesión, geografía) | 8 023–21 654 según dimensión |

---

## 2. Sesgos y equidad (Bias & Fairness)

### 2.1 Distribución de género en nombres (1.1)

| Métrica | Valor |
|---------|--------|
| Proporción global femenino | 66,9% |
| Proporción global masculino | 33,1% |
| IC 95% (Wilson) global | p_fem [65,9; 67,9%], p_masc [32,1; 34,2%] |
| Nombres clasificados (N) | 8 023 |
| Por etiqueta: NOMBRE_PERSONAL_SANITARIO | 4 107 (60,4% fem / 39,6% masc) |
| Por etiqueta: NOMBRE_SUJETO_ASISTENCIA | 3 916 (73,8% fem / 26,2% masc) |
| χ² bondad de ajuste (vs uniforme) | Cohen's w global 0,82; por etiqueta reportado |
| Desbalance extremo 70/30 (sujeto asistencia) | Sí (flag) |

*Interpretación:* Mayor representación de nombres femeninos; en sujetos de asistencia se supera el umbral 70/30. Proporciones con IC 95% (Wilson); tamaño del efecto χ² con Cohen's w.

### 2.2 Género y profesión (1.2)

| Métrica | Valor |
|---------|--------|
| χ² independencia (género × profesión) | 87,36 (p &lt; 0,001) |
| Cramér's V | 0,060 (asociación débil en magnitud) |
| Doctor: prevalencia fem vs masc (ref. masc) | 0,91 |
| Enfermería: prevalencia fem vs masc | 0,71 |
| Documentos con nombre y profesión | 5 953 |

*Interpretación:* Asociación significativa entre género y profesión; “doctor” más asociado a masculino, “enfermería” a femenino. Tamaño del efecto: Cramér's V.

### 2.3 Sesgo geográfico / toponímico (1.3)

| Métrica | Valor |
|---------|--------|
| Entidades geográficas distintas | 21 654 |
| Entropía normalizada (balance) | 0,79 |
| Entropía (bits) | 6,73 |
| Top ubicaciones (ej.) | Francia (400), Italia (387), Portugal (380), Colombia (359) |

*Interpretación:* Alta variedad geográfica; distribución relativamente equilibrada.

### 2.4 Distribución de edad (1.4)

| Métrica | Valor |
|---------|--------|
| Edades parseadas (N) | 2 804 |
| Entropía normalizada | 0,40 |
| Soporte (décadas con datos) | 7 |
| Décadas predominantes | 60–69 (62,9%), 70–79 (35,0%) |
| Subrepresentación (&lt;5%) | 80–89, 90–99 (flag) |

*Interpretación:* Concentración en 60–79 años; escasa representación de edades muy altas.

### 2.5 Sesgo institucional (1.5)

| Métrica | Valor |
|---------|--------|
| Instituciones distintas | 10 524 |
| Índice HHI | 0,022 |
| Gini | 0,76 |
| Resumen diversidad (13) | Variety 10 524, HHI 0,022, Gini 0,76 |

*Interpretación:* Mucha variedad de centros; HHI bajo indica baja concentración.

### 2.6 Sesgo diagnóstico / condición (1.6)

| Métrica | Valor |
|---------|--------|
| Diagnósticos únicos | 435 |
| Menciones totales | 623 |
| Documentos con diagnóstico extraído | 441 |
| Entropía normalizada | 0,93 |
| Entropía (bits) | 8,18 |

*Interpretación:* Alta diversidad diagnóstica y buen balance.

### 2.7 Sesgo interseccional (género × edad × geografía) (1.7)

| Métrica | Valor |
|---------|--------|
| Documentos con género | 3 506 |
| Documentos con edad | 2 501 |
| Documentos con geografía | 5 914 |
| Documentos con género y edad | 687 |
| χ² género × edad | 12,53 (p = 0,40); Cramér's V reportado; p_value_bonferroni (×3 tablas) |
| χ² género × geografía | (evaluado por región) |

*Interpretación:* No se detecta asociación significativa género–edad en la tabla de contingencia. Cramér's V y Bonferroni para múltiples tablas.

### 2.8 Diagnóstico × demografía (1.8)

| Métrica | Valor |
|---------|--------|
| Documentos con diagnóstico y género | 94 |
| Documentos con diagnóstico y edad | 95 |
| χ² independencia | Cramér's V y p_value_bonferroni (×2 tablas) reportados |
| Top diagnósticos (ej.) | Presunción (51), Apendicitis aguda (18), Proceso neumónico (10) |

### 2.9 Proporción de género vs objetivo (1.9)

| Métrica | Valor |
|---------|--------|
| Objetivo (referencia) | 50% fem / 50% masc |
| Observado | 66,9% fem / 33,1% masc |
| Diferencia máxima (abs) | 0,169 |
| Distancia L1 | 0,34 |
| Supera umbral 0,1 | Sí |

*Interpretación:* Desviación notable respecto a paridad 50/50.

### 2.10 Edad vs referencia (1.10)

| Métrica | Valor |
|---------|--------|
| Proporciones por década | 0–59: &lt;1% cada una; 60–69: 62,9%; 70–79: 35,0%; 80–89: 0,07% |
| Referencia externa | No usada en esta evaluación |
| JS divergence / L1 | N/A |

### 2.11 Cobertura y completitud (1.11)

| Dimensión | Documentos con dato | Porcentaje |
|-----------|---------------------|------------|
| Con género | 6 158 | 43,9% |
| Con edad | 2 501 | 17,8% |
| Con geografía | 5 914 | 42,1% |
| Género y edad | 1 238 | 8,8% |
| Género y geografía | 2 687 | 19,1% |
| Edad y geografía | 1 071 | 7,6% |
| Las tres dimensiones | 549 | 3,9% |

### 2.12 WEAT – análisis de género (1.12)

| Métrica | Valor |
|---------|--------|
| Tamaño de vocabulario | 6 824 |
| Documentos analizados | 14 035 |
| Efecto WEAT | −0,31 (dirección femenino) |
| p-value | 0,775 (no significativo; 1 000 permutaciones, seed 42) |
| Interpretación | Sesgo pequeño, no significativo |
| Ratio menciones masculino/femenino | 0,26 (más menciones femeninas) |
| Co-ocurrencia profesión: masculino 24%, femenino 76% |

*Interpretación:* Asociación WEAT género–palabras no significativa; corpus con más menciones femeninas. El experimento se ejecutó correctamente (embeddings por co-ocurrencia + SVD, test de permutación). Fuente: `results/sesgos/12/weat_gender_analysis.json`.

### 2.13 Resumen de diversidad (1.13)

| Dimensión | Variedad | Balance / concentración |
|-----------|----------|--------------------------|
| Geografía | 21 654 | Entropía norm. 0,79; 6,73 bits |
| Instituciones | 10 524 | HHI 0,022; Gini 0,76 |
| Diagnóstico | 435 | Entropía norm. 0,93; 8,18 bits |

---

## 3. Privacidad (Privacy)

### 3.1 Inferencia de atributos (Attribute Inference)

Clasificador binario (¿documento contiene atributo?) sobre 14 035 documentos. **AUC-ROC** se reporta con **IC 95% por bootstrap** (500 réplicas, semilla fija); ver JSON en results/privacidad/01.

| Atributo | Accuracy | AUC-ROC | Tasa positivos | Nivel de riesgo |
|----------|----------|---------|----------------|------------------|
| has_person | 90,5% | 0,969 | 70,1% | Crítico |
| has_date | 97,6% | 0,999 | 24,9% | Crítico |
| has_location | 91,3% | 0,976 | 77,6% | Crítico |
| has_id | 94,2% | 0,983 | 92,9% | Crítico |
| has_age | 97,1% | 0,997 | 20,1% | Crítico |
| has_contact | 96,7% | 0,996 | 56,6% | Crítico |
| has_medical_condition | 96,7% | 0,977 | 5,7% | Crítico |

| Resumen global | Valor |
|----------------|--------|
| AUC-ROC media | 0,985 |
| AUC-ROC máxima | 0,999 (has_date) |
| Atributos de alto riesgo | Los 7 evaluados |

*Interpretación:* Los atributos PHI son predecibles con alta discriminación (AUC alto), lo que indica riesgo de inferencia de atributos sensible a la privacidad.

### 3.2 Inferencia de pertenencia (Membership Inference)

| Métrica | Valor |
|---------|--------|
| Tamaño corpus | 14 035 |
| Accuracy del ataque | 83,3% |
| AUC-ROC | 0,42 |
| AUC-ROC IC 95% | Bootstrap (500 réplicas) |
| AUC-PR | 0,80 |
| Precisión / Recall | 1,0 / 0,0 |
| Nivel de riesgo | Bajo |
| Interpretación | No se detecta riesgo significativo de membership inference; el modelo no memoriza de forma que permita inferir pertenencia de manera fiable. |

### 3.3 Detección de memorización (Memorization)

| Métrica | Valor |
|---------|--------|
| Duplicados exactos (personas) | 215 entidades repetidas |
| Duplicados exactos (otros tipos PHI) | 802 (inst.), 17 (fechas), 169 (ubic.), 86 (ID), 66 (email), etc. |
| Pares de alta similitud semántica | 100 |
| Entidades PHI repetidas (total) | 1 355 |
| Nivel de riesgo | Crítico |
| Interpretación | Riesgo crítico de memorización: repetición extensa de entidades; revisión recomendada. |

---

## 4. Naturalidad (Naturalness)

### 4.1 Detección de texto generado por IA (AI text detection)

| Métrica | Valor |
|---------|--------|
| Clasificador | TF-IDF + regresión logística (generado vs humano) |
| Accuracy | 40,2% |
| F1 (macro) | 0,42 |
| AUC-ROC | 0,37 |
| Objetivo (naturalidad) | Accuracy &lt; 0,6 (peor = más indistinguible) |
| Nivel de naturalidad | Alto |
| Interpretación | El clasificador no distingue de forma fiable entre texto generado y humano; naturalidad percibida alta. |

### 4.2 Perplejidad (BERT español)

| Métrica | Valor |
|---------|--------|
| Modelo | dccuchile/bert-base-spanish-wwm-uncased |
| Documentos | 14 035 |
| Perplejidad media | 26,29 |
| IC 95% para la media | Normal (mean ± 1,96·SE) |
| Mediana | 23,80 |
| Desv. estándar | 21,41 |
| P25 / P75 | 17,81 / 31,67 |
| P90 | 40,38 |

### 4.3 Riqueza léxica (Vocabulary richness)

| Nivel | Métrica | Valor |
|-------|---------|--------|
| Corpus | Palabras únicas | 1 963 900 |
| Corpus | Palabras totales | 3 227 294 |
| Corpus | Type-token ratio (TTR) | 0,609 |
| Por documento | TTR (media) | 0,614 |
| Por documento | Yule’s K (media) | 140,1 |
| Por documento | Longitud media palabra | 5,51 |
| Por documento | Longitud media oración | 21,3 |

### 4.4 Legibilidad (Readability)

| Índice | Media | Mediana | Interpretación |
|--------|--------|---------|----------------|
| Inflesz | 5,41 | 4,40 | Muy difícil |
| Fernández Huerta | 191,7 | 191,9 | — |

### 4.5 Diversidad (Self-BLEU, n-gramas, repetición)

*Calculado sobre el **corpus completo** (14 035 documentos). Fuente: `results/naturalidad/05/diversity_results.json`.*

| Métrica | Valor | Objetivo (referencia) |
|---------|--------|---------------------------|
| Documentos evaluados | 14 035 | — |
| Self-BLEU (media n2–n4) | 0,056 | &lt; 0,3 (menor mejor) |
| Distinct unigrams (n1) | 0,0044 | — |
| Distinct bigrams (n2) | 0,043 | — |
| Distinct trigrams (n3) | 0,139 | &gt; 0,4 (mayor mejor) |
| Repetición frases ≥5 palabras | 22,9% | &lt; 5% (menor mejor) |

*Interpretación:* Self-BLEU bajo (bueno). Distinct n-gramas por debajo del objetivo en n3; repetición de frases elevada respecto al umbral 5%.

### 4.6 Coherencia (embeddings semánticos)

*14 035 documentos. Fuente: `results/naturalidad/06/coherence_results.json`.*

| Métrica | Valor |
|---------|--------|
| Modelo | paraphrase-multilingual-MiniLM-L12-v2 |
| Documentos evaluados | 14 035 |
| Coherencia media (similitud entre oraciones) | 0,322 |
| IC 95% para la media | [0,321; 0,323] |
| Mediana | 0,322 |
| Desv. estándar | 0,057 |
| Objetivo (referencia) | &gt; 0,6 (mayor mejor) |
| Interpretación | Coherencia por debajo del objetivo; margen de mejora. |

### 4.7 Comparación estadística (generado vs real)

*Corpus real: **corpus_repo/real_validation_corpus** (500 documentos). Generado: 14 035 documentos. Características: word_count, sentence_count, avg_word_length, avg_sentence_length, char_count, type_token_ratio. Tests: Kolmogorov–Smirnov y Mann–Whitney; Bonferroni α/k con k=6 (α_Bonferroni = 0,0083). Fuente: `results/naturalidad/07/statistical_comparison_results.json`.*

| Característica | Media generado | Media real | Diferencia relativa (media) | rank_biserial_r | Significativo (Bonferroni) |
|----------------|----------------|------------|-----------------------------|-----------------|----------------------------|
| word_count | 229,9 | 2 111,5 | +89% (real mayor) | 0,78 | Sí |
| sentence_count | 11,0 | 177,9 | +94% (real mayor) | 0,85 | Sí |
| avg_word_length | 5,51 | 4,49 | −18% (generado mayor) | −0,97 | Sí |
| avg_sentence_length | 21,3 | 13,1 | −39% (generado mayor) | −0,91 | Sí |
| char_count | 1 472,7 | 12 381,3 | +88% (real mayor) | 0,76 | Sí |
| type_token_ratio | 0,614 | 0,414 | −33% (generado mayor) | −0,77 | Sí |

| Resumen | Valor |
|---------|--------|
| Características comparadas | 6 |
| Diferencias significativas (raw α=0,05) | 6 |
| Diferencias significativas (Bonferroni) | 6 |
| Similarity score (Bonferroni) | 0% |
| Alpha Bonferroni | 0,0083 |

*Interpretación:* Las distribuciones de las seis características difieren de forma significativa entre corpus generado y real (incluso tras Bonferroni). El corpus real de validación tiene documentos mucho más largos (más palabras, oraciones y caracteres); el generado tiene oraciones más largas en media y TTR más alto. Esto es esperable si el real son informes clínicos completos y el sintético son notas más cortas; para el paper conviene describir el origen de ambos corpus y comentar si la diferencia de longitud es deseable o un límite a generalizar.

---

## 5. Tablas resumen para el paper

### Tabla 1 – Resumen de sesgos y equidad

| ID | Métrica | Resultado principal | Nota |
|----|---------|---------------------|------|
| 1.1 | Género (nombres) | 67% fem, 33% masc; desbalance en sujetos | Objetivo paridad |
| 1.2 | Género × profesión | χ² significativo; doctor→masc, nurse→fem | Asociación estadística |
| 1.3 | Geografía | 21 654 valores; entropía norm. 0,79 | Buena diversidad |
| 1.4 | Edad | Concentración 60–79 años; 80+ subrepresentados | Revisar generación |
| 1.5 | Instituciones | 10 524; HHI 0,02 | Baja concentración |
| 1.6 | Diagnóstico | 435 únicos; entropía 0,93 | Muy diverso |
| 1.7 | Interseccional | Género×edad no significativo (p=0,40) | — |
| 1.9 | Paridad género | L1=0,34; supera umbral 0,1 | Desviación de 50/50 |
| 1.11 | Cobertura | 44% género, 18% edad, 42% geo; 3,9% las tres | Completitud limitada |
| 1.12 | WEAT género | Efecto −0,31, p=0,78 (no sign.) | Sesgo WEAT bajo |

### Tabla 2 – Resumen de privacidad

| Experimento | Métrica principal | Resultado | Riesgo |
|-------------|-------------------|-----------|--------|
| Attribute inference | AUC-ROC media | 0,985 | Crítico (atributos predecibles) |
| Membership inference | AUC-ROC | 0,42 | Bajo |
| Memorization | Entidades PHI repetidas / pares similares | 1 355 / 100 | Crítico |

### Tabla 3 – Resumen de naturalidad

| Experimento | Métrica principal | Valor | Interpretación |
|-------------|-------------------|--------|----------------|
| AI detection | Accuracy clasificador | 40,2% | Alta naturalidad (indistinguible) |
| Perplexity | Media (BERT-es) | 26,3 | — |
| Vocabulary | TTR corpus | 0,61 | Riqueza léxica moderada-alta |
| Readability | Inflesz (media) | 5,41 | Muy difícil |
| Diversity | Self-BLEU (14 035 docs) | 0,056 | Bajo (deseable); repetición frases 22,9% |
| Coherence | Media similitud (IC 95%) | 0,322 [0,321–0,323] | Por debajo de objetivo 0,6 |
| Statistical comparison | Generado vs real (500 docs) | 6/6 características distintas (Bonferroni) | Documentos sintéticos más cortos que real; TTR y oración más larga en sintético |

---

## 6. Conclusiones para el paper (borrador)

- **Sesgos:** El corpus presenta desbalance de género (más nombres femeninos y desviación respecto a paridad 50/50), asociación significativa género–profesión, y concentración de edad en 60–79 años con poca representación de 80+. La diversidad geográfica, institucional y diagnóstica es alta; WEAT de género no significativo.
- **Privacidad:** Alta predictibilidad de atributos PHI (riesgo crítico de inferencia de atributos). Riesgo bajo de membership inference. Memorización crítica: repetición elevada de entidades PHI y pares de documentos muy similares.
- **Naturalidad:** Los textos sintéticos son difíciles de distinguir de humanos (AI detection ~40% accuracy). Perplejidad y TTR coherentes con texto médico; coherencia (0,32, IC 95% reportado) y repetición de frases (22,9%) son puntos a mejorar. La **comparación estadística con corpus real** (real_validation_corpus, 500 documentos) muestra diferencias significativas en las seis características (word_count, sentence_count, avg_word_length, avg_sentence_length, char_count, TTR) incluso tras Bonferroni: el corpus sintético tiene documentos más cortos que el real; en cambio, oración más larga y TTR más alto en el sintético. Conviene explicar en el paper el origen y uso esperado de ambos corpus (p. ej. notas breves vs informes largos) para interpretar estas diferencias.

---

---

## 7. Reproducibilidad

- **Comando de la suite:** `python run_all_experiments.py --corpus_root corpus_repo/corpus_v1 --full_corpus`
- **Corpus:** corpus_v1 (14 035 documentos); para experimento 4.7 es obligatorio `corpus_repo/real_validation_corpus`.
- **Resultados:** `results/sesgos`, `results/privacidad`, `results/naturalidad`. Los JSON incluyen, cuando aplica: proporciones con IC Wilson, Cohen's w, Cramér's V, p_value_bonferroni, auc_roc_ci_95, mean_ci_95, rank_biserial_r, similarity_score_bonferroni.
- **Parámetros fijos:** Ver `interpretacion/EVALUATION_PARAMETERS.md`.

### Estado de la última ejecución

Este documento refleja los resultados de la suite ejecutada con corpus completo (14 035 documentos) y corpus real `corpus_repo/real_validation_corpus` (500 documentos) para el experimento 4.7. Las secciones 4.5, 4.6 y 4.7 incorporan los valores de `results/naturalidad/05/`, `06/` y `07/`. Sesgos, privacidad y el resto de naturalidad se mantienen según los JSON en `results/sesgos`, `results/privacidad` y `results/naturalidad`.

*Documento actualizado con metodología, decisiones de diseño y resultados actuales para redacción del paper (Q1 informática/medicina).*

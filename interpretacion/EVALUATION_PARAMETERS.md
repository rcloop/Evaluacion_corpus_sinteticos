# Parámetros de evaluación – Suite de corpus sintético

Documento de referencia: valores fijos usados en los experimentos para **reproducibilidad** y para **reportar en el paper**.

---

## Nivel de significación (α)

| Parámetro | Valor | Uso |
|-----------|--------|-----|
| **α** | 0.05 | Umbral para rechazar H0 en tests (χ², KS, Mann-Whitney, WEAT). |
| **α Bonferroni** | 0.05 / k | En comparación estadística (07), k = número de características comparadas. |

---

## Semillas (reproducibilidad)

| Contexto | Valor | Uso |
|----------|--------|-----|
| **Train/test split** | 42 | `random_state=42` en sklearn (attribute inference, membership inference). |
| **WEAT permutation test** | 42 | `WEAT_RANDOM_SEED` en weat_gender_analysis. |
| **Statistical comparison sample** | 42 | `random.seed(42)` al muestrear documentos (07). |
| **Bootstrap AUC-ROC** | 42 | Semilla en attribute_inference y membership_inference para IC 95%. |

---

## Umbrales de riesgo (privacidad)

### Attribute inference (AUC-ROC por atributo)

| Nivel | Condición | Interpretación |
|-------|-----------|----------------|
| Bajo | AUC-ROC < 0.6 | Atributo poco predecible. |
| Medio | 0.6 ≤ AUC-ROC < 0.7 | Riesgo moderado. |
| Alto | 0.7 ≤ AUC-ROC < 0.8 | Riesgo alto. |
| Crítico | AUC-ROC ≥ 0.8 | Riesgo crítico. |

### Membership inference (AUC-ROC)

| Nivel | Condición | Interpretación |
|-------|-----------|----------------|
| Bajo | AUC-ROC < 0.6 | No se detecta riesgo significativo de membership inference. |
| Medio | 0.6–0.7 | Riesgo moderado. |
| Alto | 0.7–0.8 | Riesgo alto. |
| Crítico | ≥ 0.8 | Riesgo crítico. |

### Memorization

| Concepto | Valor | Uso |
|----------|--------|-----|
| **Umbral similitud semántica** | > 0.95 | Par de documentos con similitud por encima se consideran “alta similitud”. |
| **Riesgo** | Basado en total_repeated_phi_entities y high_similarity_pairs | Nivel crítico según umbrales internos del script. |

---

## Sesgos: criterios operativos

| Criterio | Valor | Uso |
|----------|--------|-----|
| **Desbalance extremo género (70/30)** | p_max > 0.7 sobre (fem + masc) | Flag en name gender distribution (1.1). |
| **Proporción objetivo género (09)** | 50% fem / 50% masc | Referencia para L1 y flag. |
| **Umbral diferencia máxima (09)** | max \|diff\| > 0.10 | Flag si se supera respecto al objetivo. |
| **Subrepresentación edad (04)** | &lt; 5% en un bin de década | Flag “underrepresented”. |

---

## Naturalidad

| Métrica | Objetivo / umbral | Uso |
|--------|-------------------|-----|
| **AI detection accuracy** | &lt; 0.6 (menor = más natural) | Clasificador generado vs humano. |
| **Coherence (media)** | &gt; 0.6 (mayor = mejor) | Interpretación en resultados. |
| **Self-BLEU (diversity)** | &lt; 0.3 (menor = menos repetición) | Interpretación en resultados. |
| **Repetición frases (≥5 palabras)** | &lt; 5% | Interpretación en resultados. |

---

## Intervalos de confianza

| Métrica | Método | Nivel |
|---------|--------|--------|
| **Proporciones (género, cobertura)** | Wilson score | 95% |
| **AUC-ROC (attribute/membership)** | Bootstrap (500 réplicas) | 95% |
| **Media perplejidad** | Normal (mean ± 1.96·std/√n) | 95% |
| **Media coherencia** | Normal (mean ± 1.96·std/√n) | 95% |

---

## Tamaños del efecto reportados

| Experimento | Efecto |
|-------------|--------|
| χ² bondad de ajuste (01) | Cohen's w = √(χ²/N) |
| χ² independencia (02, 07, 08) | Cramér's V |
| Mann-Whitney (07) | r de correlación biserial por rangos (rank-biserial) |
| WEAT (12) | Diferencia estandarizada (effect size) |

---

**Resultados:** Los valores numéricos obtenidos con estos parámetros se recogen en **interpretacion/RESUMEN_METRICAS_PAPER.md** (suite con corpus completo 14 035 documentos y corpus real 500 para experimento 4.7). Justificación de tests y métricas: **interpretacion/ANALISIS_TESTS_ESTADISTICOS_Y_METRICAS.md**.

*Documento generado para la suite de experimentos en `src/experimentos/`. Fecha: marzo 2026.*

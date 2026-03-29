# Análisis de tests estadísticos y métricas – Suite de evaluación de corpus sintético

Documento de referencia para el paper: qué tests y métricas se usan en cada experimento, por qué son relevantes para validar un corpus sintético, y sugerencias de mejora.

---

## 1. Por qué son importantes para validar un corpus sintético

Un corpus sintético debe ser **útil** (cobertura, diversidad, naturalidad), **equitativo** (sin sesgos demográficos o asociativos indebidos) y **privado** (sin memorización ni inferencia de atributos/pertenencia). Los tests estadísticos y las métricas permiten:

- **Objetivar** juicios (no solo “parece diverso”, sino entropía, HHI, χ²).
- **Comparar** con referencia (corpus real, proporciones objetivo) o con baseline (azar, mayoría).
- **Reproducir** resultados (semillas, parámetros documentados).
- **Publicar** con rigor (p-values, tamaños de efecto, intervalos).

---

## 2. Sesgos (Bias & Fairness)

### 2.1 Name gender distribution (01)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Conteo por categoría (fem/masc/other) | **Proporciones** p_fem, p_masc, p_other | Cuantificar representación de género. |
| Desviación respecto a uniforme | **χ² de bondad de ajuste** (vs uniforme 1/3–1/3–1/3) | Detectar si la distribución se aleja de la equiprobabilidad (gl=2). |
| Desbalance extremo | **Flag 70/30** (p_max sobre fem+masc > 0,7) | Alerta operativa para paridad. |

**Importancia para corpus sintético:** Un corpus con fuerte desbalance de género en nombres puede reforzar estereotipos en downstream (NER, generación). El χ² indica si la desviación es estadísticamente significativa.

**Posible mejora:** Usar χ² frente a una **referencia externa** (p. ej. proporción real en población o en corpus real) en lugar de solo frente a uniforme; reportar **intervalos de confianza** para las proporciones (Wilson score o binomial).

---

### 2.2 Role/profession vs gender (02)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Tabla de contingencia género × profesión | **Conteos** por celda | Base para asociación. |
| Independencia | **χ² de independencia** (Pearson) | ¿Género y profesión son independientes? (H0: independencia). |
| Magnitud por rol | **Razones de prevalencia** p(rol\|género) / p(rol\|ref) | Cuantificar sobrerrepresentación (ej. doctor→masc, nurse→fem). |

**Importancia:** Detecta estereotipos profesión–género (p. ej. “médico” masculino, “enfermera” femenino). El χ² responde “¿hay asociación?”; las prevalencias responden “¿cuánto?”.

**Posible mejora:** Reportar **tamaño del efecto** (Cramér’s V o similar) además del p-value; considerar **corrección por múltiples comparaciones** si se hacen muchos roles.

---

### 2.3 Geographic/toponymic bias (03)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Conteo de entidades geográficas | **Top-k**, **variety** (n únicos) | Diversidad nominal. |
| Concentración | **Entropía de Shannon** (bits y normalizada) | Balance: alta entropía = más repartido; baja = pocos topónimos dominan. |

**Importancia:** Un corpus muy concentrado en pocos países/regiones puede ser poco representativo. La entropía resume el balance sin depender solo del top-k.

**Posible mejora:** Incluir **HHI** o **Gini** (como en instituciones) para concentración; opcional **χ² vs referencia** si se tiene distribución geográfica de referencia.

---

### 2.4 Age distribution (04)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Histograma por décadas | **Conteos y porcentajes** por bin | Ver concentración en edades. |
| Concentración | **Entropía de Shannon** (bits y normalizada) | Balance entre décadas. |
| Subrepresentación | **Flags** (p. ej. &lt;5% en 80–89, 90–99) | Alertas para edades muy altas. |

**Importancia:** Evitar que el corpus solo represente un rango estrecho de edad (p. ej. solo 60–79). La entropía y los flags ayudan a vigilar cobertura.

**Posible mejora:** **Test χ²** frente a una distribución de referencia (población o corpus real); **JS divergence** o **L1** respecto a esa referencia (como en 2.10).

---

### 2.5 Institution bias (05)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Conteo de instituciones | **Top-k**, **variety** | Diversidad. |
| Concentración | **HHI** (Herfindahl–Hirschman): Σ p_i² | Mercado “concentrado” vs “repartido”; bajo = diverso. |
| Desigualdad | **Gini** sobre frecuencias | Desigualdad en el reparto de menciones. |
| Curva | **Lorenz** (opcional) | Visualización de la desigualdad. |

**Importancia:** HHI y Gini son estándar en economía/competencia; aquí indican si el corpus depende de muy pocas instituciones (riesgo de sesgo o de identificación).

**Posible mejora:** Añadir **entropía normalizada** para alinear con geografía y diagnóstico; opcional comparación con un HHI/Gini de referencia.

---

### 2.6 Diagnosis/condition bias (06)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Extracción de diagnósticos (secciones/frases) | **Conteos**, **n únicos**, **top-k** | Cobertura y diversidad diagnóstica. |
| Balance | **Entropía de Shannon** (bits y normalizada) | Evitar que pocos diagnósticos dominen. |

**Importancia:** Un corpus con muy pocos diagnósticos o muy concentrado puede ser poco útil para entrenar modelos clínicos. La entropía resume el reparto.

**Posible mejora:** **χ² o JS** frente a una distribución de referencia (p. ej. CIE o corpus real) si está disponible.

---

### 2.7 Intersectional corpus bias (07)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Tablas contingencia género×edad, género×geografía, edad×geografía | **Conteos** por celda | Base para interacciones. |
| Independencia en cada tabla | **χ² de independencia** | ¿Las dos variables son independientes? (p. ej. género y grupo de edad). |

**Importancia:** Los sesgos pueden ser interseccionales (p. ej. “mujer + mayor” o “hombre + región X”). El χ² detecta asociaciones significativas entre dimensiones.

**Posible mejora:** Con muchas celdas, revisar **conteos esperados** (χ² poco fiable con celdas &lt;5); reportar **Cramér’s V**; considerar **residuos tipificados** para ver qué celdas aportan al rechazo.

---

### 2.8 Diagnosis × demography (08)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Tablas diagnóstico×género y diagnóstico×edad | **Conteos**, **top diagnósticos** | Asociación diagnóstico–demografía. |
| Independencia | **χ² de independencia** | ¿Diagnóstico y género/edad son independientes? |

**Importancia:** Evitar asociaciones estereotipadas (p. ej. cierto diagnóstico solo con un género o rango de edad). El χ² da una prueba formal.

**Posible mejora:** Igual que 2.7: Cramér’s V, residuos, comprobar supuestos de χ².

---

### 2.9 Gender target proportion (09)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Proporciones observadas (de 1.1) vs objetivo (ej. 50/50) | **Diferencia por categoría**, **L1** (Σ|obs − target|), **max |diff|** | Distancia global y peor categoría. |
| Umbral | **Flag** si max |diff| &gt; 0,1 | Decisión binaria “¿cumplimos paridad?”. |

**Importancia:** Traduce “queremos 50/50” en una métrica numérica y un criterio claro. L1 es interpretable (desviación total).

**Posible mejora:** **χ² de bondad de ajuste** frente a (0.5, 0.5) con gl=1; **intervalos de confianza** para las proporciones observadas.

---

### 2.10 Age reference comparison (10)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Histograma observado (de 1.4) vs referencia (JSON décadas→p) | **Jensen–Shannon divergence (bits)** | Simetría, acotada; buena para comparar distribuciones. |
| Alternativa | **L1** entre distribuciones | Interpretable como “cuánta masa se mueve”. |

**Importancia:** Si tienes una referencia (población, corpus real), JSD y L1 miden si la distribución de edad del sintético se parece. JSD tiene propiedades teóricas (métrica, acotada).

**Posible mejora:** Usar **siempre** una referencia cuando exista (no dejar JSD/L1 en null); documentar formato del JSON de referencia; opcional **χ²** observado vs referencia.

---

### 2.11 Coverage/completeness (11)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Por documento: ¿tiene género/edad/geografía? | **Conteos y porcentajes** (has_gender, has_age, has_geo, combinaciones) | Cobertura de dimensiones demográficas. |
| Combinaciones | **Conteos (género∧edad, género∧geo, etc., las tres)** | Completitud interseccional. |

**Importancia:** Un corpus “con sesgos medidos” pero con pocos documentos con edad o geografía limita los análisis. No hay test de hipótesis; es descriptivo.

**Posible mejora:** Definir **umbrales mínimos** de cobertura por dimensión y flag si no se alcanzan; opcional **intervalos de confianza** para proporciones (Wilson).

---

### 2.12 WEAT gender analysis (12)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Embeddings (co-ocurrencias + SVD) sobre corpus | **Diferencia de asociación** profesiones–(masculino vs femenino) | WEAT: asociación implícita profesión–género. |
| Significación | **Permutation test** (n_permutations=1000): p-value = proporción de |efecto permutado| ≥ |observado| | H0: no diferencia de asociación; no asume normalidad. |
| Magnitud | **Tamaño del efecto** (diferencia estandarizada) | “Cuánto” sesgo, no solo “si” hay. |
| Complemento | **Ratio de menciones** masculino/femenino y **co-ocurrencias** profesión–género | Contexto léxico. |

**Importancia:** WEAT es estándar para sesgo implícito en embeddings. El permutation test es no paramétrico y adecuado para este tipo de medida. Importante para validar que el corpus no introduce asociaciones estereotipadas a nivel semántico.

**Posible mejora:** **Intervalo de confianza** para el efecto (bootstrap o más permutaciones); documentar **lista exacta** de palabras profesión/masculino/femenino; considerar **WEAT multinomial** o **segunda etapa** (más atributos).

---

### 2.13 Diversity summary (13)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Agregación de 1.3, 1.5, 1.6 | **Variety**, **entropía normalizada**, **HHI/Gini** (según dimensión) | Resumen único de diversidad geográfica, institucional y diagnóstica. |

**Importancia:** Da una vista consolidada para el paper o el informe; no añade tests nuevos.

---

## 3. Privacidad (Privacy)

### 3.1 Attribute inference (01)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Clasificador binario (¿documento contiene atributo PHI?) con train/test | **Accuracy** | Rendimiento del atacante. |
| Discriminación | **AUC-ROC** | Capacidad de rankear positivos vs negativos; independiente del umbral. |
| Baseline | **Baseline accuracy** (mayoría) | Comparar con “adivinar la clase mayoritaria”. |
| Riesgo | **Niveles** por AUC (p. ej. &lt;0.6 bajo, ≥0.8 crítico) | Interpretación operativa. |

**Importancia:** Si un atacante puede predecir bien la presencia de PHI (persona, fecha, ubicación, etc.), el corpus tiene riesgo de inferencia de atributos. AUC-ROC es la métrica estándar en detección.

**Posible mejora:** **AUC-PR** cuando hay desbalance fuerte; **intervalos de confianza** (bootstrap) para AUC y accuracy; **múltiples splits** o cross-validation para estabilidad.

---

### 3.2 Membership inference (02)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Ataque: ¿el documento perteneció al conjunto de entrenamiento del generador? | **Accuracy**, **AUC-ROC**, **AUC-PR** | Capacidad de distinguir miembro vs no miembro. |
| Baseline | **Baseline accuracy** | Comparar con adivinar mayoría. |
| Riesgo | **Umbrales AUC-ROC** (p. ej. &lt;0.6 bajo) | Interpretación. |

**Importancia:** La membership inference mide si el modelo “recuerda” ejemplos. AUC &lt;0.6 suele interpretarse como riesgo bajo. No se usa un test de hipótesis clásico; la métrica es el rendimiento del ataque.

**Posible mejora:** **Intervalos de confianza**; **múltiples runs** con distintos splits; considerar **calibrated attack** (con scores de pérdida/perplexidad si están disponibles).

---

### 3.3 Memorization detection (03)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Duplicados exactos de entidades PHI entre documentos | **Conteos** por tipo (persona, institución, fecha, etc.) y **total_repeated** | Repetición literal. |
| Similitud semántica entre pares de documentos | **Umbral** (p. ej. &gt;0.95) y **número de pares** por encima | Posible memorización de frases/parágrafos. |
| Resumen | **total_repeated_phi_entities**, **high_similarity_pairs**, **risk_level** | Resumen para informe. |

**Importancia:** La repetición exacta o casi exacta de PHI o de texto indica memorización. No hay test paramétrico; la decisión es por umbrales y conteos.

**Posible mejora:** **Distribución de similitudes** (histograma) y sensibilidad al umbral; **canary/secret** en entrenamiento para test de memorización canónica; cuantificar **% de documentos** con al menos un duplicado.

---

## 4. Naturalidad (Naturalness)

### 4.1 AI text detection (01)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Clasificador (TF-IDF + logística) generado vs humano | **Accuracy**, **precision**, **recall**, **F1**, **AUC-ROC** | Capacidad de distinguir sintético vs humano. |
| Baseline | **0.5** (azar) | Objetivo: accuracy **baja** (~0.5) = textos indistinguibles. |
| Interpretación | **Nivel** (ej. HIGH naturalness si accuracy &lt; 0.6) | Comunicar resultado. |

**Importancia:** Si un clasificador simple no separa bien sintético y real, se considera alta naturalidad. La métrica principal es accuracy (o AUC); no hay test de hipótesis sobre “igualdad de distribuciones”.

**Posible mejora:** **Test binomial** para “accuracy no mayor que 0.6” (H0: p≤0.6); **intervalos de confianza**; probar **varios clasificadores** (incl. basados en LM) y reportar todos.

---

### 4.2 Perplexity (02)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Perplejidad por documento (modelo MLM, p. ej. BERT-es) | **Media, mediana, std, min, max, percentiles** | Nivel de “sorpresa” del modelo ante el texto. |

**Importancia:** Perplejidad baja suele indicar texto más “predecible” o parecido al dominio del modelo. Es descriptivo; no hay comparación formal con corpus real en este script.

**Posible mejora:** **Comparación estadística** (KS, Mann-Whitney o t-test según normalidad) de la distribución de perplejidad **generado vs real**; reportar **IC para la media**.

---

### 4.3 Vocabulary richness (03)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Type-token ratio (TTR), Yule’s K, longitudes | **Media, mediana, std** a nivel documento y/o corpus | Riqueza léxica y longitud. |

**Importancia:** Un corpus sintético muy repetitivo tendría TTR bajo. Solo descriptivo.

**Posible mejora:** **Comparación generado vs real** (igual que en 4.2 y 4.7): mismas características y tests (KS, Mann-Whitney) para TTR y Yule’s K.

---

### 4.4 Readability (04)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Índices (Inflesz, Fernández Huerta) por documento | **Media, mediana, std** | Dificultad de lectura. |

**Importancia:** Coherencia con estándares de legibilidad en español. Descriptivo.

**Posible mejora:** **Comparación con corpus real** (estadísticos + test KS/Mann-Whitney) para comprobar si la legibilidad del sintético es comparable.

---

### 4.5 Diversity (05)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Self-BLEU (n=2,3,4), distinct n-grams, repetición de frases (≥5 palabras) | **Medias**, **ratios** | Diversidad y repetición a nivel de n-gramas/frases. |

**Importancia:** Self-BLEU bajo = menos repetición entre documentos; distinct alto = más variedad. Objetivos típicos: self-BLEU &lt;0.3, repetición &lt;5%. Descriptivo.

**Posible mejora:** **Comparación con corpus real** (distribuciones de self-BLEU y distinct); **tests de igualdad de distribuciones** (KS, Mann-Whitney) y tamaños del efecto.

---

### 4.6 Coherence (06)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Similitud entre oraciones (embeddings) por documento | **Media, mediana, std** de coherencia | Coherencia local. |

**Importancia:** Texto coherente tiene oraciones semánticamente cercanas. Descriptivo; umbral “&gt;0.6” es orientativo.

**Posible mejora:** **Comparación generado vs real** (estadísticos + test); **IC** para la media de coherencia.

---

### 4.7 Statistical comparison (07)

| Qué se hace | Test / métrica | Por qué |
|-------------|-----------------|---------|
| Extracción de características (word_count, sentence_count, avg_word_length, avg_sentence_length, char_count) en generado y real | **Media, mediana, std** por corpus | Descripción de cada variable. |
| Igualdad de distribuciones | **Kolmogorov-Smirnov (KS)** a dos muestras | H0: la distribución de la variable es la misma en generado y real. No paramétrico. |
| Igualdad de ubicación | **Mann-Whitney U** (bilateral) | H0: no diferencia de tendencia central; robusto, no asume normalidad. |
| Magnitud | **Diferencia relativa** (media y mediana en %) | Tamaño del efecto en escala interpretable. |

**Importancia:** Es el único experimento que compara **explícitamente** distribuciones generado vs real con tests estadísticos. KS y Mann-Whitney son estándar para “¿las dos muestras vienen de la misma distribución / misma tendencia?”. Crucial para argumentar que el sintético es estadísticamente similar al real en esas características.

**Posible mejora:** Añadir **tamaño del efecto** (e.g. r de Wilcoxon o diferencia estandarizada); **corrección por múltiples comparaciones** (Bonferroni o FDR) al hacer varios tests; incluir **más características** (TTR, perplejidad por doc, longitud de oración, etc.) en la misma pipeline; **bootstrap** para IC de las diferencias.

---

## 5. Resumen en tabla

| Experimento | Test estadístico principal | Métricas principales | ¿Comparación con referencia? |
|-------------|----------------------------|----------------------|------------------------------|
| Sesgos 01 | χ² bondad ajuste (uniforme) | Proporciones, flag 70/30 | No (solo uniforme) |
| Sesgos 02 | χ² independencia | Tabla contingencia, razones prevalencia | No |
| Sesgos 03 | — | Entropía Shannon, variety, top-k | No |
| Sesgos 04 | — | Entropía, histograma, flags | No |
| Sesgos 05 | — | HHI, Gini, variety | No |
| Sesgos 06 | — | Entropía Shannon, variety | No |
| Sesgos 07 | χ² independencia (×3 tablas) | Contingencias interseccionales | No |
| Sesgos 08 | χ² independencia (×2) | Diagnóstico×género/edad | No |
| Sesgos 09 | — | L1, max |diff|, flag | Sí (proporción objetivo) |
| Sesgos 10 | — | JSD, L1 (si hay referencia) | Sí (si se pasa referencia) |
| Sesgos 11 | — | Porcentajes cobertura | No |
| Sesgos 12 | Permutation test (WEAT) | Efecto WEAT, p-value, ratios menciones | No (solo efecto en corpus) |
| Sesgos 13 | — | Resumen entropía/HHI/Gini | No |
| Priv 01 | — | Accuracy, AUC-ROC por atributo | Baseline mayoría |
| Priv 02 | — | Accuracy, AUC-ROC, AUC-PR | Baseline mayoría |
| Priv 03 | — | Conteos, umbral similitud, risk_level | Umbrales fijos |
| Nat 01 | — | Accuracy, F1, AUC-ROC | Baseline 0.5 |
| Nat 02 | — | Media/mediana perplejidad | No |
| Nat 03 | — | TTR, Yule’s K, longitudes | No |
| Nat 04 | — | Inflesz, Fernández Huerta | No |
| Nat 05 | — | Self-BLEU, distinct, repetición | No |
| Nat 06 | — | Media coherencia | No |
| Nat 07 | **KS, Mann-Whitney U** | Media/mediana por feature, diff % | **Sí (generado vs real)** |

---

## 6. Recomendaciones generales de mejora

1. **Referencias externas donde aplique**  
   En sesgos (género, edad, geografía, diagnóstico), usar distribuciones de referencia (población, corpus real, CIE) y reportar χ², JSD o L1 frente a ellas, no solo estadísticos descriptivos.

2. **Tamaños del efecto**  
   Junto con p-values (χ², WEAT, KS, Mann-Whitney), reportar Cramér’s V, r de Wilcoxon, diferencias estandarizadas o JSD/L1 para que el lector juzgue relevancia práctica.

3. **Incertidumbre**  
   Donde se reporten proporciones, medias o AUC: **intervalos de confianza** (Wilson, bootstrap o asintóticos) para mejorar la interpretación y la reproducibilidad.

4. **Múltiples comparaciones**  
   En 07 (varias características) y en sesgos (varias tablas/roles): corrección (Bonferroni, FDR) o predefinir unas pocas hipótesis principales.

5. **Consistencia generado vs real**  
   Reutilizar la lógica de 07 (KS, Mann-Whitney, diferencias) para perplejidad, TTR, legibilidad, coherencia y diversidad (self-BLEU, distinct), de modo que todas las dimensiones de naturalidad tengan una comparación estadística explícita con el corpus real.

6. **Documentación de decisiones**  
   Dejar explícito en el paper: α=0.05, semillas, umbrales de riesgo (AUC, similitud), criterios 70/30 y L1&gt;0.1, para que la validación del corpus sintético sea reproducible y defendible.

---

## 7. Resultados de la ejecución actual (resumen)

Las siguientes mejoras del análisis están ya implementadas y los resultados incorporados en **interpretacion/RESUMEN_METRICAS_PAPER.md**:

- **Sesgos:** IC 95% Wilson para proporciones (1.1); Cohen's w en χ² bondad de ajuste; Cramér's V en χ² independencia (1.2, 1.7, 1.8); p_value_bonferroni en tablas múltiples (1.7, 1.8).
- **Privacidad:** AUC-ROC con IC 95% por bootstrap (500 réplicas) en attribute y membership inference.
- **Naturalidad:**  
  - **Diversity (05):** Calculado sobre **corpus completo** (14 035 documentos); Self-BLEU media 0,056; repetición frases 22,9%; distinct n-gramas reportados.  
  - **Coherence (06):** Media 0,322 con **mean_ci_95** [0,321; 0,323].  
  - **Statistical comparison (07):** Corpus real **data/real_validation_corpus** (500 documentos). Se comparan 6 características (word_count, sentence_count, avg_word_length, avg_sentence_length, char_count, type_token_ratio). Para cada una: KS y Mann-Whitney; **Bonferroni** (α=0,0083) y **rank_biserial r**. Resultado: las 6 características difieren significativamente (generado más corto que real; oración más larga y TTR más alto en generado). Justificación para el paper: describir el origen de ambos corpus (notas breves vs informes largos) para interpretar las diferencias de longitud.

Los parámetros fijos (α, semillas, umbrales, métodos de IC) están documentados en **interpretacion/EVALUATION_PARAMETERS.md**.

---

*Documento generado a partir del código en `src/experimentos/` (sesgos, privacidad, naturalidad). Fecha: marzo 2026.*

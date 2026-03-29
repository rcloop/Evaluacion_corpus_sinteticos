# Suite de experimentos – Evaluación de corpus sintéticos

Documento generado automáticamente. Lista de experimentos por tipo: **privacidad**, **sesgos** y **naturalidad**.

## Privacidad

Experimentos en `src/experimentos/privacidad/`.

| Nº | Experimento | Script | Resultados | Notas |
|----|-------------|--------|------------|-------|
| 01 | Attribute Inference | `01_attribute_inference.py` | `results/privacidad/01` | — |
| 02 | Membership Inference | `02_membership_inference.py` | `results/privacidad/02` | — |
| 03 | Memorization Detection | `03_memorization_detection.py` | `results/privacidad/03` | — |

## Sesgos

Experimentos en `src/experimentos/sesgos/`.

| Nº | Experimento | Script | Resultados | Notas |
|----|-------------|--------|------------|-------|
| 01 | Name gender distribution (1.1) | `01_name_gender_distribution.py` | `results/sesgos/01` | — |
| 02 | Role/profession gender bias (1.2) | `02_role_profession_gender_bias.py` | `results/sesgos/02` | — |
| 03 | Geographic/toponymic bias (1.3) | `03_geographic_toponymic_bias.py` | `results/sesgos/03` | — |
| 04 | Age distribution (1.4) | `04_age_distribution.py` | `results/sesgos/04` | — |
| 05 | Institution bias (1.5) | `05_institution_bias.py` | `results/sesgos/05` | — |
| 06 | Diagnosis/condition bias (1.6) | `06_diagnosis_condition_bias.py` | `results/sesgos/06` | — |
| 07 | Intersectional corpus bias (género×edad×geografía) | `07_intersectional_corpus_bias.py` | `results/sesgos/07` | — |
| 08 | Diagnosis × demography bias | `08_diagnosis_demography_bias.py` | `results/sesgos/08` | — |
| 09 | Gender vs target proportion (usa 1.1) | `09_gender_target_proportion.py` | `results/sesgos/09` | — |
| 10 | Age vs reference (usa 1.4) | `10_age_reference_comparison.py` | `results/sesgos/10` | — |
| 11 | Coverage/completeness | `11_coverage_completeness.py` | `results/sesgos/11` | — |
| 12 | WEAT gender analysis | `12_weat_gender_analysis.py` | `results/sesgos/12` | — |
| 13 | Diversity summary (lee 1.3, 1.5, 1.6) | `13_diversity_summary.py` | `results/sesgos/13` | Ejecutar 03, 05 y 06 antes para que existan los JSON. |

## Naturalidad

Experimentos en `src/experimentos/naturalidad/`.

| Nº | Experimento | Script | Resultados | Notas |
|----|-------------|--------|------------|-------|
| 01 | AI text detection | `01_ai_detection.py` | `results/naturalidad/01` | — |
| 02 | Perplexity | `02_perplexity.py` | `results/naturalidad/02` | — |
| 03 | Vocabulary richness | `03_vocabulary_richness.py` | `results/naturalidad/03` | — |
| 04 | Readability | `04_readability.py` | `results/naturalidad/04` | — |
| 05 | Diversity metrics | `05_diversity.py` | `results/naturalidad/05` | — |
| 06 | Coherence | `06_coherence.py` | `results/naturalidad/06` | — |
| 07 | Statistical comparison (generado vs real) | `07_statistical_comparison.py` | `results/naturalidad/07` | — |

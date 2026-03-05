# Experimentos

Experimentos numerados: **sesgos**, **privacidad** y **naturalidad**. Cada número tiene su carpeta de resultados en `results/<tipo>/<NN>`.

## Sesgos (`sesgos/`)

Un script por métrica de sesgo. Corpus con `entidades/` y `documents/`.

| Nº | Script | Resultados |
|----|--------|------------|
| 01 | `01_name_gender_distribution.py` | `results/sesgos/01` |
| 02 | `02_role_profession_gender_bias.py` | `results/sesgos/02` |
| 03 | `03_geographic_toponymic_bias.py` | `results/sesgos/03` |
| 04 | `04_age_distribution.py` | `results/sesgos/04` |
| 05 | `05_institution_bias.py` | `results/sesgos/05` |
| 06 | `06_diagnosis_condition_bias.py` | `results/sesgos/06` |
| 07 | `07_intersectional_corpus_bias.py` | `results/sesgos/07` |
| 08 | `08_diagnosis_demography_bias.py` | `results/sesgos/08` |
| 09 | `09_gender_target_proportion.py` | `results/sesgos/09` |
| 10 | `10_age_reference_comparison.py` | `results/sesgos/10` |
| 11 | `11_coverage_completeness.py` | `results/sesgos/11` |
| 12 | `12_weat_gender_analysis.py` | `results/sesgos/12` |
| 13 | `13_diversity_summary.py` | `results/sesgos/13` (requiere 03, 05, 06) |

Ejecutar desde la raíz del repo:
```bash
python src/experimentos/sesgos/01_name_gender_distribution.py --corpus_root ruta/al/corpus
# Opcional: --max_docs 0 (todos), --lexicon_path ruta/lexicon.csv
```

## Privacidad (`privacidad/`)

Solo tres evaluaciones: Attribute Inference, Membership Inference, Memorization Detection.

| Nº | Script | Resultados |
|----|--------|------------|
| 01 | `01_attribute_inference.py` | `results/privacidad/01` |
| 02 | `02_membership_inference.py` | `results/privacidad/02` |
| 03 | `03_memorization_detection.py` | `results/privacidad/03` |

Ejecutar desde la raíz, por ejemplo:
```bash
python src/experimentos/privacidad/01_attribute_inference.py --corpus_path ruta/al/corpus
python src/experimentos/privacidad/02_membership_inference.py --corpus_path ruta/al/corpus
python src/experimentos/privacidad/03_memorization_detection.py --corpus_path ruta/al/corpus [--annotations_path ruta/entidades]
```

## Naturalidad (`naturalidad/`)

Un script por métrica de naturalidad del texto (corpus generado).

| Nº | Script | Resultados |
|----|--------|------------|
| 01 | `01_ai_detection.py` | `results/naturalidad/01` |
| 02 | `02_perplexity.py` | `results/naturalidad/02` |
| 03 | `03_vocabulary_richness.py` | `results/naturalidad/03` |
| 04 | `04_readability.py` | `results/naturalidad/04` |
| 05 | `05_diversity.py` | `results/naturalidad/05` |
| 06 | `06_coherence.py` | `results/naturalidad/06` |
| 07 | `07_statistical_comparison.py` | `results/naturalidad/07` |

Ejecutar desde la raíz:
```bash
python src/experimentos/naturalidad/01_ai_detection.py --generated_corpus ruta/corpus [--human_corpus ruta/humano]
python src/experimentos/naturalidad/02_perplexity.py --corpus_path ruta/corpus
python src/experimentos/naturalidad/07_statistical_comparison.py --generated_corpus ruta/generado --real_corpus ruta/real
# Opcional en varios: --sample_size N
```

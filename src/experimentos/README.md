# Experimentos

Experimentos numerados: **sesgos**, **privacidad** y **naturalidad**. Cada número tiene su carpeta de resultados en `results/<tipo>/<NN>`.

**Corpus:** todos los experimentos usan **`corpus_repo/corpus_v1`** (documentos en `documents/`, anotaciones en `entidades/`). El experimento **07** (comparación estadística) compara ese corpus generado (v1) con el corpus real **`data/real_validation_corpus`**.

**Referente único:** toda la lógica de evaluación está bajo esta carpeta. Cada tipo tiene un subdirectorio `_lib/` con los módulos que usan los scripts (sesgos: métricas de sesgo; privacidad: attribute/membership/memorization; naturalidad: perplexity, coherence, etc.). No hay suites duplicadas bajo `src/`; los 23 experimentos usan solo estos scripts y `_lib/`. (Copias históricas opcionales solo en local bajo `restos/`, fuera de git.)

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

Ejecutar desde la raíz del repo (corpus = corpus_repo/corpus_v1):
```bash
python src/experimentos/sesgos/01_name_gender_distribution.py --corpus_root corpus_repo/corpus_v1
# Opcional: --max_docs 0 (todos), --lexicon_path ruta/lexicon.csv
```
En **Windows PowerShell 5** (sin `&&`): desde la raíz usa `.\run.ps1 python ...` o ejecuta solo `python ...` si ya estás en la raíz.

## Privacidad (`privacidad/`)

Solo tres evaluaciones: Attribute Inference, Membership Inference, Memorization Detection.

| Nº | Script | Resultados |
|----|--------|------------|
| 01 | `01_attribute_inference.py` | `results/privacidad/01` |
| 02 | `02_membership_inference.py` | `results/privacidad/02` |
| 03 | `03_memorization_detection.py` | `results/privacidad/03` |

Ejecutar desde la raíz (corpus = corpus_repo/corpus_v1):
```bash
python src/experimentos/privacidad/01_attribute_inference.py --corpus_path corpus_repo/corpus_v1 --annotations_path corpus_repo/corpus_v1/entidades
python src/experimentos/privacidad/02_membership_inference.py --corpus_path corpus_repo/corpus_v1
python src/experimentos/privacidad/03_memorization_detection.py --corpus_path corpus_repo/corpus_v1 --annotations_path corpus_repo/corpus_v1/entidades
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

Ejecutar desde la raíz (documentos = corpus_repo/corpus_v1/documents para 01-06):
```bash
python src/experimentos/naturalidad/01_ai_detection.py --generated_corpus corpus_repo/corpus_v1/documents
python src/experimentos/naturalidad/02_perplexity.py --corpus_path corpus_repo/corpus_v1/documents
# 03-06 igual: --corpus_path corpus_repo/corpus_v1/documents
# 07 (comparativo): generado = corpus_v1/documents, real = data/real_validation_corpus
python src/experimentos/naturalidad/07_statistical_comparison.py --generated_corpus corpus_repo/corpus_v1/documents --real_corpus data/real_validation_corpus
# Opcional en varios: --sample_size N (0 = todo el corpus)
```

**Ejecutar solo los que no tienen resultado (con todo el corpus):** desde la raíz:
```bash
python run_missing_experiments.py --corpus_root corpus_repo/corpus_v1 --full_corpus
```
Usa `corpus_repo/corpus_v1` para todos; el 07 usa además `data/real_validation_corpus` como corpus real (por defecto).

**Dependencias para naturalidad:** el 02 (perplexity) y el 06 (coherence) requieren PyTorch y transformers (y sentence-transformers para coherence). Instalación desde la raíz: `pip install -r requirements.txt`.

# Experiments

Numbered experiments for **bias (`sesgos`)**, **privacy (`privacidad`)**, and **naturalness (`naturalidad`)**. Each index has a matching folder under `results/<type>/<NN>`.

**Corpus:** runs assume **`corpus_repo/corpus_v1`** (`documents/` + `entidades/`). Experiment **07** (statistical comparison) compares that synthetic corpus to the real reference corpus at **`data/real_validation_corpus`**.

**Single source of truth:** all evaluation code is under this tree. Each suite has a **`_lib/`** package (bias metrics; privacy attacks; naturalness metrics). The 23 experiment scripts use only these entry points and `_lib/`. Optional legacy copies may exist locally under `restos/` (gitignored).

## Bias (`sesgos/`)

One script per bias metric. Expects `entidades/` and `documents/`.

| # | Script | Outputs |
|---|--------|---------|
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
| 13 | `13_diversity_summary.py` | `results/sesgos/13` (needs 03, 05, 06) |

From the repo root (`corpus_root = corpus_repo/corpus_v1`):

```bash
python src/experimentos/sesgos/01_name_gender_distribution.py --corpus_root corpus_repo/corpus_v1
# Optional: --max_docs 0 (all), --lexicon_path path/to/lexicon.csv
```

On **Windows PowerShell 5** (no `&&`): run from the root with `.\run.ps1 python ...` or plain `python ...`.

## Privacy (`privacidad/`)

Three evaluations: Attribute Inference, Membership Inference, Memorization Detection.

| # | Script | Outputs |
|---|--------|---------|
| 01 | `01_attribute_inference.py` | `results/privacidad/01` |
| 02 | `02_membership_inference.py` | `results/privacidad/02` |
| 03 | `03_memorization_detection.py` | `results/privacidad/03` |

From the repo root:

```bash
python src/experimentos/privacidad/01_attribute_inference.py --corpus_path corpus_repo/corpus_v1 --annotations_path corpus_repo/corpus_v1/entidades
python src/experimentos/privacidad/02_membership_inference.py --corpus_path corpus_repo/corpus_v1
python src/experimentos/privacidad/03_memorization_detection.py --corpus_path corpus_repo/corpus_v1 --annotations_path corpus_repo/corpus_v1/entidades
```

## Naturalness (`naturalidad/`)

One script per naturalness metric on the generated corpus.

| # | Script | Outputs |
|---|--------|---------|
| 01 | `01_ai_detection.py` | `results/naturalidad/01` |
| 02 | `02_perplexity.py` | `results/naturalidad/02` |
| 03 | `03_vocabulary_richness.py` | `results/naturalidad/03` |
| 04 | `04_readability.py` | `results/naturalidad/04` |
| 05 | `05_diversity.py` | `results/naturalidad/05` |
| 06 | `06_coherence.py` | `results/naturalidad/06` |
| 07 | `07_statistical_comparison.py` | `results/naturalidad/07` |

From the repo root (documents = `corpus_repo/corpus_v1/documents` for 01–06):

```bash
python src/experimentos/naturalidad/01_ai_detection.py --generated_corpus corpus_repo/corpus_v1/documents
python src/experimentos/naturalidad/02_perplexity.py --corpus_path corpus_repo/corpus_v1/documents
# 03–06: same --corpus_path corpus_repo/corpus_v1/documents
# 07: generated = corpus_v1/documents, real = data/real_validation_corpus
python src/experimentos/naturalidad/07_statistical_comparison.py --generated_corpus corpus_repo/corpus_v1/documents --real_corpus data/real_validation_corpus
# Optional on several scripts: --sample_size N (0 = full corpus)
```

**Run only missing experiments (full corpus)** from the root:

```bash
python run_missing_experiments.py --corpus_root corpus_repo/corpus_v1 --full_corpus
```

Uses `corpus_repo/corpus_v1` everywhere; 07 also uses `data/real_validation_corpus` by default.

**Naturalness deps:** 02 (perplexity) and 06 (coherence) need PyTorch and `transformers` (plus `sentence-transformers` for coherence). Install with `pip install -r requirements.txt` from the repo root.

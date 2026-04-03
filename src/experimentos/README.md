# Experiments

Numbered experiments for **bias (`sesgos`)**, **privacy (`privacidad`)**, and **naturalness (`naturalidad`)**. Indices are **contiguous** per suite: `sesgos` **01–11**, `privacidad` **01–02**, `naturalidad` **01–08**; each maps to `results/<type>/<NN>`.

Default paths are centralized in **`repo_paths.py`** at the repository root (`DEFAULT_SYNTHETIC_CORPUS_ROOT`, `DEFAULT_REAL_VALIDATION_DOCS_DIR`).

**Corpus:** runs assume **`corpus_repo/corpus_v1`** (`documents/` + `entidades/`). Experiments **07** and **08** compare generated `.txt` files to **`corpus_repo/real_validation_corpus`** (gitignored); populate with **`corpus_repo/export_real_validation_corpus.py`** or copy `.txt` files there. Those scripts fail if that folder has no `.txt` files.

**Single source of truth:** all evaluation code is under this tree. Each suite has a **`_lib/`** package (bias metrics; privacy attacks; naturalness metrics). The **21** numbered evaluation entry points (`sesgos` 11 + `privacidad` 2 + `naturalidad` 8) use only these trees and `_lib/`. Helper utilities under `sesgos/` (lexicon export / review) are optional. Optional legacy copies may exist locally under `restos/` (gitignored).

## Bias (`sesgos/`)

One script per bias metric. Expects `entidades/` and `documents/`.

| # | Script | Outputs |
|---|--------|---------|
| 01 | `01_name_gender_distribution.py` | `results/sesgos/01` |
| 02 | `02_role_profession_gender_bias.py` | `results/sesgos/02` |
| 03 | `03_geographic_toponymic_bias.py` | `results/sesgos/03` |
| 04 | `04_age_distribution.py` | `results/sesgos/04` |
| 05 | `05_institution_bias.py` | `results/sesgos/05` |
| 06 | `06_intersectional_corpus_bias.py` | `results/sesgos/06` |
| 07 | `07_gender_target_proportion.py` | `results/sesgos/07` |
| 08 | `08_age_reference_comparison.py` | `results/sesgos/08` |
| 09 | `09_coverage_completeness.py` | `results/sesgos/09` |
| 10 | `10_weat_gender_analysis.py` | `results/sesgos/10` |
| 11 | `11_diversity_summary.py` | `results/sesgos/11` (needs 03, 05) |

From the repo root (`corpus_root = corpus_repo/corpus_v1`):

```bash
python src/experimentos/sesgos/01_name_gender_distribution.py --corpus_root corpus_repo/corpus_v1
# Optional: --max_docs 0 (all), --lexicon_path path/to/lexicon.csv
```

On **Windows PowerShell 5** (no `&&`): run from the root with `.\scripts\run.ps1 python ...` or plain `python ...`.

## Privacy (`privacidad/`)

Two evaluations: **attribute inference** (PHI-category predictability from text) and **memorization-style screening** (repeated PHI strings and near-duplicate documents). Pretraining exposure of the commercial generator is **not** audited (out of scope); synthetic-vs-real differences are covered under naturalness experiments.

| # | Script | Outputs |
|---|--------|---------|
| 01 | `01_attribute_inference.py` | `results/privacidad/01` |
| 02 | `02_memorization_detection.py` | `results/privacidad/02` |

From the repo root:

```bash
python src/experimentos/privacidad/01_attribute_inference.py --corpus_path corpus_repo/corpus_v1 --annotations_path corpus_repo/corpus_v1/entidades
python src/experimentos/privacidad/02_memorization_detection.py --corpus_path corpus_repo/corpus_v1 --annotations_path corpus_repo/corpus_v1/entidades
```

## Naturalness (`naturalidad/`)

One script per naturalness metric on the generated corpus.

| # | Script | Outputs |
|---|--------|---------|
| 01 | `01_ai_detection.py` | `results/naturalidad/01` |
| 02 | `02_ai_detection_real_windows.py` | `results/naturalidad/02` |
| 03 | `03_vocabulary_richness.py` | `results/naturalidad/03` |
| 04 | `04_readability.py` | `results/naturalidad/04` |
| 05 | `05_diversity.py` | `results/naturalidad/05` |
| 06 | `06_coherence.py` | `results/naturalidad/06` |
| 07 | `07_statistical_comparison.py` | `results/naturalidad/07` |
| 08 | `08_statistical_comparison_real_windows.py` | `results/naturalidad/08` |

**Methods — full documents (01 / 07) vs length-aligned windows (02 / 08)**

- **01 / 07 (default):** Compare **entire** `.txt` files (after optional `--sample_size`). **07** reports surface features on both sides; use **`--exclude_length_features`** on **07** if you want Mann–Whitney + Bonferroni **α/3** on **only** average word length, average sentence length, and type–token ratio (TTR), without windowing. For length-aligned comparison with real long exports, use **02 / 08** (sliding windows on the real side; synthetic = full generated notes per file, **W** = round mean synthetic token count).
- **Real export cleanup (default on) for 01 and 07:** Paragraph-level chunks on the **real** side that match standardized **valoración** scale headers are removed before metrics (`naturalidad/_lib/real_corpus_sanitize.py`): e.g. *aloración/valoración enfermo crítico* and *aloración/valoración hospitalización/hospitalizacion general* (accent- and case-insensitive). Synthetic documents are not modified. Use **`--no_sanitize_real_chunks`** to disable.
- **02 / 08 — real sliding windows:** **W** = round(**mean** synthetic word count), same tokenizer as **07** (`length_norm` / statistical comparison pipeline). Each **synthetic** file is kept as the **full document** (no truncation to **W**; notes shorter than **W** words are unchanged). Each **real** file is split into **non-overlapping** windows of **W** tokens (optional **`--real_window_stride`** for overlap). **Sanitization is off** so valoración blocks can appear inside windows. **08** compares **only** the three length-agnostic shape features (Mann–Whitney + Bonferroni **α/3**); raw token/character totals are omitted from tests. **Interpretation:** real units are fixed-width **W**-word spans; synthetic units are **whole generated notes**, so the comparison is **intentionally asymmetric** (real coverage vs full synthetic text).

**Limitations — dependence and what “human” means here**

- **Within-document dependence:** Many windows come from the **same** clinical export; they are **not** independent draws. Multiplicity correction (Bonferroni) addresses multiple **tests**, not correlation **within** a patient file.
- **Clinician and site style:** Real notes typically reflect **specific teams, authors, and documentation habits** (templates, EHR shortcuts, local phrasing). The reference corpus is **not** a random sample of “all possible human clinical writing”; it may show **lower stylistic variability** than a broader multi-centre benchmark. Results characterize **this** real reference **relative to** the synthetic corpus, not universal human naturalness.
- **Sampling asymmetry:** Synthetic side = **one full document** per generated file; real side = **several** **W**-word windows per long export. The classifier (**02**) and **08** stats therefore mix **variable-length synthetic** units with **fixed-width real** windows unless you change the protocol.

From the repo root (documents = `corpus_repo/corpus_v1/documents` for 01, 02, 03–06):

```bash
python src/experimentos/naturalidad/01_ai_detection.py --generated_corpus corpus_repo/corpus_v1/documents
python src/experimentos/naturalidad/02_ai_detection_real_windows.py --generated_corpus corpus_repo/corpus_v1/documents
# 03–06: same --corpus_path corpus_repo/corpus_v1/documents
# 07–08: generated = corpus_v1/documents, real = corpus_repo/real_validation_corpus
python src/experimentos/naturalidad/07_statistical_comparison.py --generated_corpus corpus_repo/corpus_v1/documents --real_corpus corpus_repo/real_validation_corpus
python src/experimentos/naturalidad/08_statistical_comparison_real_windows.py --generated_corpus corpus_repo/corpus_v1/documents --real_corpus corpus_repo/real_validation_corpus
# Optional on several scripts: --sample_size N (0 = full corpus)
```

**Naturalness deps:** 06 (coherence) needs PyTorch and `transformers` plus `sentence-transformers`. Install with `pip install -r requirements.txt` from the repo root.

## Models used in evaluation

This repository **evaluates** an already-generated synthetic corpus; it does **not** host the proprietary **generator LLM** (model id/version is out of scope here—state it in the paper if you release it).

| Component | Model or method | Experiments | Notes |
|-----------|-----------------|-------------|--------|
| PHI-category inference | TF–IDF + L2 logistic regression (scikit-learn) | `privacidad/01` | No neural LM |
| memorization (semantic) | **`sentence-transformers`:** `paraphrase-multilingual-MiniLM-L12-v2` | `privacidad/02` | Whole-note embeddings, cosine similarity |
| AI vs human (default) | TF–IDF + L2 logistic regression (`class_weight=balanced`) | `naturalidad/01` | No neural LM unless you opt in |
| AI vs human (real windows) | Same as 01 + **real** **W**-word windows (**W** = round mean synthetic wc); synthetic = **full** docs | `naturalidad/02` | Asymmetric units; see limitations |
| AI vs human (optional) | **`transformers`:** `dccuchile/bert-base-spanish-wwm-uncased` | `naturalidad/01` | Only if `--use_transformer` |
| coherence | **`sentence-transformers`:** `paraphrase-multilingual-MiniLM-L12-v2` | `naturalidad/06` | Within-note mean sentence similarity |
| WEAT | Corpus **co-occurrence + SVD** vectors (no HF download) | `sesgos/10` | Windowed counts on your `.txt`; not a pretrained embedding table |
| Surface stats vs real (windowed, length-agnostic) | Mann–Whitney + Bonferroni on **3** shape features; same **W** as 02 | `naturalidad/08` | Raw length totals omitted at fixed **W** |
| Surface stats vs real (optional full-doc) | **07** with `--exclude_length_features` | `naturalidad/07` | Full notes; same 3 tests only |

**Why `paraphrase-multilingual-MiniLM-L12-v2` for `privacidad/02` and `naturalidad/06`?**

- **Task fit:** Both scripts need **dense semantic similarity** (whole-note vectors for near-duplicate screening; sentence–sentence similarity for within-note coherence). This checkpoint is from the `sentence-transformers` hub and is trained for **semantic textual similarity / paraphrase-style** encodings, which is closer to “same meaning, different words” than using raw MLM representations ad hoc.
- **Language:** It is **multilingual** (including Spanish), so one fixed model covers our Spanish clinical notes without maintaining separate monolingual pipelines.
- **Compute:** **MiniLM** at **12 layers** is much lighter than large cross-lingual encoders, which matters when embedding **tens of thousands of full documents** (memorization **02**) and **many sentences per note** (`06`) on typical hardware.
- **Consistency:** Using the **same encoder** for memorization-style similarity and coherence keeps embeddings in a **single semantic space** and simplifies reproduction (one stack, one version pin).
- **Caveat:** It is **not** a Spanish clinical specialist model; cosine scores are a **screening proxy** (ranking / tail behavior), not a proof of duplication or factual coherence. Swap the checkpoint with `privacidad/02_memorization_detection.py --semantic_model …` or `naturalidad/06_coherence.py --model_name …` if you run a sensitivity analysis.

All other listed scripts (e.g. vocabulary richness, diversity, readability formulas, statistical comparison, most bias metrics) use **rules, counts, and classical stats** only—no transformer checkpoints.

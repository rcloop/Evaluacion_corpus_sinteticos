# Experiment tests (privacy, bias, naturalness)

Tests for the synthetic-corpus evaluation scripts. A single **`corpus_mini`** drives privacy, bias, and naturalness smoke tests; experiment **07** uses **`corpus_repo/real_validation_corpus`** (same default as production) and is **skipped** if that directory has no `.txt` files. The goal is **smoke coverage** where data exists, plus light **structure / sanity** checks on produced JSON.

## Design: no generator model access

Metrics use the synthetic corpus (and optional external text) only, **without** access to the generative model. Scores come from text + annotations or from **public** proxy models.

- **Privacy (attribute / membership):** attacks on the published data only.
- **Memorization detection:** heuristic repetition / near-duplicate risk in the corpus (exact + semantic), not internal model memorization.
- **Perplexity:** computed with a **public** language model proxy (e.g. Spanish BERT / causal LM), not the generator.
- **Bias:** WEAT and distributional checks are **corpus-only** (counts and embeddings).
- **Other naturalness metrics:** operate on text and public models only.

If you later add **canaries** for membership inference, document them here.

## Test data

The same minimal **`corpus_mini`** backs all suites: six documents under `documents/` and JSON entities under `entidades/`. Experiment **07** uses **`corpus_repo/real_validation_corpus/`** with at least one `.txt`; otherwise the 07 test is skipped.

| Fixture | Path | Purpose |
|---------|------|---------|
| `corpus_mini_path` | `test/data/corpus_mini/` | Root: `documents/` (`.txt`) + `entidades/` (`.json`) |
| `corpus_mini_documents_path` | `test/data/corpus_mini/documents/` | `.txt` only; naturalness 01–06 and generated side of 07 |
| `real_validation_corpus_path` | `corpus_repo/real_validation_corpus/` | Real-reference `.txt` for 07; **skipped** if missing/empty |

Tests do **not** assert production thresholds or generator quality—only successful runs and plausible JSON shapes. Experiment subprocesses write JSON under **pytest `tmp_path`**, not under `results/`, so CI and local runs do not overwrite paper-grade result files.

## Dependency / layout check

**`test_requirements_complete.py`** verifies imports for `requirements.txt` and that expected modules exist under each **`_lib/`**:

- Packages (numpy, scipy, matplotlib, tqdm, scikit-learn, nltk, torch, transformers, sentence-transformers, pytest) import cleanly where required.
- Python **≥ 3.8**.
- `sesgos/_lib`, `privacidad/_lib`, `naturalidad/_lib` contain the expected `.py` files.
- **`requirements.txt`** exists at the repo root.

```bash
pytest test/test_requirements_complete.py -v
```

## How to run

```bash
pytest test/ -v

pytest test/test_requirements_complete.py -v

pytest test/test_experimentos_sesgos.py -v
pytest test/test_experimentos_privacidad.py -v
pytest test/test_experimentos_naturalidad.py -v
```

## What each layer checks

- **Smoke:** each script runs on the mini corpus with `returncode == 0`.
- **Structure:** for bias 01 and privacy 01, JSON keys and basic ranges (proportions in `[0,1]`, AUC in `[0,1]`, valid `risk_level`).
- **Naturalness 03:** vocabulary JSON exposes `corpus_level`, `document_level`, and numeric metrics.
- **Fixtures:** `corpus_mini` is **required**—missing data fails fast. **`real_validation_corpus`** is optional for the overall suite (07 skipped if absent). Heavy optional deps (e.g. PyTorch, sentence-transformers) may trigger **skip** so the rest of the suite can run.

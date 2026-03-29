# Corpus (`corpus_repo`)

## Annotated synthetic corpus: `corpus_v1`

**`corpus_repo/corpus_v1`** is the default synthetic corpus for experiments. It contains:

- **`documents/`** – text files (e.g. `.txt`).
- **`entidades/`** – entity annotations for bias and privacy scripts.

Bulky exports (`train_set.json`, `ner_dataset.json`, `validation_results/`, …) are **not** tracked in git; only `documents/` and `entidades/` (and other small JSON you choose to keep) are versioned.

Default runners use:

- `run_all_experiments.py`, `run_missing_experiments.py` → `corpus_repo/corpus_v1`
- `src/experimentos/run_missing_full_corpus.ps1` → `corpus_repo\corpus_v1`

## Real-reference texts for experiment 07

The evaluation repo expects real-reference **`.txt`** files under **`data/real_validation_corpus/`** at the **repository root** (see root `repo_paths.DEFAULT_REAL_VALIDATION_DOCS_DIR`).

From this folder you can export into that location:

```bash
python export_real_validation_corpus.py --output_dir ../../data/real_validation_corpus
```

(or any absolute path to `.../Evaluacion_corpus_sinteticos/data/real_validation_corpus`)

## Other files here

- **`real_validation_set.json`** (root of `corpus_repo`) – source list for real documents (not tracked if large / sensitive).
- **`export_real_validation_corpus.py`** – builds a directory of `.txt` from that JSON.

## Summary

| Path | Role |
|------|------|
| `corpus_v1/` | Synthetic annotated corpus; default input for experiments. |
| `data/real_validation_corpus/` (repo root) | Real-reference `.txt` set for naturalness experiment 07. |

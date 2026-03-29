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

Real holdout **`.txt`** files live under **`corpus_repo/real_validation_corpus/`** (see `repo_paths.DEFAULT_REAL_VALIDATION_DOCS_DIR`). That directory is **gitignored**; keep it only on your machine.

Export from JSON (from `corpus_repo/`):

```bash
python export_real_validation_corpus.py
```

Default output is `corpus_repo/real_validation_corpus/`. Override with `--output_dir` if needed.

## Other files here

- **`real_validation_set.json`** (root of `corpus_repo`) – source list for real documents (not tracked if large / sensitive).
- **`export_real_validation_corpus.py`** – builds a directory of `.txt` from that JSON.

## Summary

| Path | Role |
|------|------|
| `corpus_v1/` | Synthetic annotated corpus; default input for experiments. |
| `real_validation_corpus/` (here, gitignored) | Real-reference `.txt` set for naturalness experiment 07. |

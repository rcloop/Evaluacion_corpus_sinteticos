# Corpus (`corpus_repo`)

## Annotated synthetic corpus: `corpus_v1`

**`corpus_repo/corpus_v1`** is the default synthetic corpus for every experiment (bias, privacy, naturalness). It should contain:

- **`documents/`** – text files (e.g. `.txt`) for each synthetic document.
- **`entidades/`** – entity annotations in the format expected by the bias and privacy scripts.

Suite entry points default to this tree:

- `run_all_experiments.py` – `--corpus_root corpus_repo/corpus_v1` by default.
- `run_missing_experiments.py` – same default.
- `src/experimentos/run_missing_full_corpus.ps1` – calls the runner with `corpus_repo\corpus_v1`.

## Other assets

- **`real_validation_set.json`** – describes real (non-generated) documents used to build the validation export.
- **`real_validation_corpus/`** – `.txt` export derived from that JSON; reference **real** text for experiment 07 (generated vs real).
- **`export_real_validation_corpus.py`** – regenerates `real_validation_corpus/` from the JSON.

## Summary

| Path | Role |
|------|------|
| `corpus_v1/` | Annotated synthetic corpus; **default input for all experiments**. |
| `real_validation_corpus/` | Real reference corpus for experiment 07 (naturalness comparison). |

# Experiment results (`results/`)

JSON outputs from **`scripts/run_all_experiments.py`**, **`scripts/run_missing_experiments.py`**, or individual scripts under `src/experimentos/`.

## Full corpus (paper-grade)

- **`scripts/run_all_experiments.py`** uses the **entire** synthetic corpus by default (no cap on perplexity, memorization, or naturalness sample sizes).
- For a faster local run on large corpora, pass **`--quick`** (caps perplexity and memorization at 5000 documents).

**Pytest** experiment tests write under **temporary directories**, not here—running `pytest` should **not** overwrite these files.

## Sanity check

After a full run, spot-check that JSON files reflect full scale, for example:

- `results/privacidad/01/attribute_inference.json` → `corpus_size` matches the document count under your `corpus_root` (e.g. 14 035 for `corpus_repo/corpus_v1`).
- Naturalness outputs should report document counts consistent with full `documents/`.

If `corpus_size` is very small, you likely have a partial run or stale files—re-run:

`python scripts/run_all_experiments.py --corpus_root corpus_repo/corpus_v1`

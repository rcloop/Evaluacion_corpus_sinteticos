# Synthetic corpus evaluation

Evaluation of synthetic clinical corpora across **bias**, **privacy**, and **text naturalness**.

## Layout

- **`src/experimentos/`** – Numbered entry-point scripts and per-suite **`_lib/`** packages (`sesgos`, `privacidad`, `naturalidad`).
- **`repo_paths.py`** – Single source of truth for default corpus paths (`DEFAULT_SYNTHETIC_CORPUS_ROOT`, `DEFAULT_REAL_VALIDATION_DOCS_DIR`).
- **`test/`** – Pytest suite and minimal data under `test/data/`.
- **`corpus_repo/corpus_v1/`** – Versioned synthetic corpus (`documents/` + `entidades/`). Large training/export JSON under `corpus_v1/` (e.g. `train_set.json`) are not tracked—only what’s needed to run experiments.
- **`data/real_validation_corpus/`** – **Your** real-reference `.txt` files for **experiment 07** (not in git). You populate this directory from **your own** validation export; the repo does not invent that dataset.
- **`data/`** – Small reference assets (e.g. lexicons under `data/sesgos/`).
- **`results/`** – Experiment outputs (JSON). Log `.txt` under `results/` is ignored.
- **`scripts/`** – Auxiliary scripts.
- **`restos/`** – Optional **local-only** legacy snapshots (gitignored).
- **Root** – `requirements.txt`, runners (`run_all_experiments.py`, `run_missing_experiments.py`, …), `run.ps1`.

### Outputs (`results/`)

Write under **`results/`** at the repo root:

- `results/sesgos/01` … `13`
- `results/privacidad/01` … `03`
- `results/naturalidad/01` … `07`

Global `*.json` in `.gitignore` is relaxed for **`results/`**, **`test/data/`**, **`corpus_repo/corpus_v1/`** (metrics + annotations only; bulky exports listed in `.gitignore`).

### Experiment 07 (generated vs real)

Default real side: **`data/real_validation_corpus/`** (`repo_paths.DEFAULT_REAL_VALIDATION_DOCS_DIR`). That folder must contain **one `.txt` per real document** you are allowed to use (de-identified, etc.). Options:

1. **Use your own files** – Copy or sync your real validation texts into `data/real_validation_corpus/` (any safe workflow you already have).

2. **Export from your JSON manifest** – If you maintain something like `corpus_repo/real_validation_set.json` with paths or text fields for **real** holdout documents, you can fill `data/real_validation_corpus/` from that, e.g.:

   ```bash
   python corpus_repo/export_real_validation_corpus.py --output_dir data/real_validation_corpus
   ```

3. **Placeholder only (tests / smoke)** – `scripts/generate_real_validation_corpus.py` writes **fixed synthetic Spanish snippets**, not your real dataset. Use it for `test/data/real_corpus_mini` or quick local checks, **not** as a substitute for your real validation corpus in a paper run.

## Requirements

```bash
pip install -r requirements.txt
```

**GPU (NVIDIA):** optional; for faster perplexity / coherence / memorization / AI detection:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
```

## Usage

See **`src/experimentos/README.md`**. Example:

`python src/experimentos/sesgos/01_name_gender_distribution.py --corpus_root corpus_repo/corpus_v1`

## License

MIT — see **[LICENSE](LICENSE)**.

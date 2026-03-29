# Synthetic corpus evaluation

Evaluation of synthetic clinical corpora across **bias**, **privacy**, and **text naturalness**.

## Layout

- **`src/experimentos/`** – Numbered entry-point scripts and per-suite **`_lib/`** packages (`sesgos`, `privacidad`, `naturalidad`).
- **`repo_paths.py`** – Single source of truth for default corpus paths (`DEFAULT_SYNTHETIC_CORPUS_ROOT`, `DEFAULT_REAL_VALIDATION_DOCS_DIR`).
- **`test/`** – Pytest suite and minimal data under `test/data/`.
- **`corpus_repo/corpus_v1/`** – Versioned synthetic corpus (`documents/` + `entidades/`). Large training/export JSON under `corpus_v1/` (e.g. `train_set.json`) are not tracked—only what’s needed to run experiments.
- **`data/real_validation_corpus/`** – Real-reference `.txt` documents for **experiment 07** (not tracked; generate locally). See `scripts/generate_real_validation_corpus.py`.
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

Defaults use **`data/real_validation_corpus`** (see `repo_paths.DEFAULT_REAL_VALIDATION_DOCS_DIR`). Populate it before running 07 or full runners:

```bash
python scripts/generate_real_validation_corpus.py --output_dir data/real_validation_corpus --num_docs 50
```

To export from `corpus_repo/real_validation_set.json` into the same layout:

```bash
python corpus_repo/export_real_validation_corpus.py --output_dir data/real_validation_corpus
```

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

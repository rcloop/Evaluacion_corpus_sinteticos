# Synthetic corpus evaluation

Evaluation of synthetic clinical corpora across **bias**, **privacy**, and **text naturalness**.

## Layout

- **`src/experimentos/`** – Numbered entry-point scripts and per-suite **`_lib/`** packages (`sesgos`, `privacidad`, `naturalidad`).
- **`repo_paths.py`** – Single source of truth for default corpus paths (`DEFAULT_SYNTHETIC_CORPUS_ROOT`, `DEFAULT_REAL_VALIDATION_DOCS_DIR`).
- **`test/`** – Pytest suite and minimal data under `test/data/`.
- **`corpus_repo/corpus_v1/`** – Versioned synthetic corpus (`documents/` + `entidades/`). Large training/export JSON under `corpus_v1/` (e.g. `train_set.json`) are not tracked—only what’s needed to run experiments.
- **`data/real_validation_corpus/`** – **Your** real-reference `.txt` files for **experiment 07** (**gitignored**). You populate it locally from **your own** validation export; nothing is committed or auto-generated.
- **`data/`** – Small reference assets (e.g. lexicons under `data/sesgos/`).
- **`results/`** – Experiment outputs (JSON). Log `.txt` under `results/` is ignored.
- **`scripts/`** – Optional small utilities (may be empty).
- **`restos/`** – Optional **local-only** legacy snapshots (gitignored).
- **Root** – `requirements.txt`, runners (`run_all_experiments.py`, `run_missing_experiments.py`, …), `run.ps1`. Full-suite default = **all documents** (use `run_all_experiments.py --quick` to cap heavy steps at 5000 docs).

### Outputs (`results/`)

Write under **`results/`** at the repo root:

- `results/sesgos/01` … `13`
- `results/privacidad/01` … `03`
- `results/naturalidad/01` … `07`

Global `*.json` in `.gitignore` is relaxed for **`results/`**, **`test/data/`**, **`corpus_repo/corpus_v1/`** (metrics + annotations only; bulky exports listed in `.gitignore`).

### Experiment 07 (generated vs real)

Default real side: **`data/real_validation_corpus/`** (`repo_paths.DEFAULT_REAL_VALIDATION_DOCS_DIR`). Experiment **07** exits with an error if that directory is missing, is not a directory, or contains **no** `.txt` files—there is no synthetic fallback. Discovery is **recursive**; extension match is **case-insensitive** (`.txt` / `.TXT`).

1. **Use your own files** – Copy or sync your real validation `.txt` files into `data/real_validation_corpus/` (local only; see `.gitignore`).

2. **Export from your JSON manifest** – If you maintain something like `corpus_repo/real_validation_set.json` with paths or text fields for **real** holdout documents:

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

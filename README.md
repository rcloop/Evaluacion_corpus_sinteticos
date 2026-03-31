# Synthetic corpus evaluation

Evaluation of synthetic clinical corpora across **bias**, **privacy**, and **text naturalness**.

## Layout

- **`src/experimentos/`** – Numbered entry-point scripts and per-suite **`_lib/`** packages (`sesgos`, `privacidad`, `naturalidad`).
- **`repo_paths.py`** – Single source of truth for default corpus paths (`DEFAULT_SYNTHETIC_CORPUS_ROOT`, `DEFAULT_REAL_VALIDATION_DOCS_DIR`).
- **`test/`** – Pytest suite and minimal data under `test/data/`.
- **`corpus_repo/corpus_v1/`** – Versioned synthetic corpus (`documents/` + `entidades/`). Large training/export JSON under `corpus_v1/` (e.g. `train_set.json`) are not tracked—only what’s needed to run experiments.
- **`corpus_repo/real_validation_corpus/`** – **Your** real-reference `.txt` files for **experiment 07** (**gitignored**). Populate locally (export script or copy); never committed.
- **`data/`** – Small reference assets (e.g. lexicons under `data/sesgos/`).
- **`results/`** – Experiment outputs (JSON). Log `.txt` under `results/` is ignored.
- **`scripts/`** – **Runners**: `run_all_experiments.py`, `run.ps1` (from repo root: `python scripts/run_all_experiments.py`, or `.\scripts\run.ps1 python ...`). Heavy steps use a **24h** per-script timeout by default (`--timeout_heavy`).
- **`restos/`** – Optional **local-only** legacy snapshots (gitignored).
- **Root** – `requirements.txt`, `repo_paths.py`, `pytest.ini`. Full-suite default = **all documents** (use `python scripts/run_all_experiments.py --quick` to cap heavy steps at 5000 docs).

### Outputs (`results/`)

Write under **`results/`** at the repo root:

- `results/sesgos/01` … `13`
- `results/privacidad/01` … `03`
- `results/naturalidad/01` … `07`

Global `*.json` in `.gitignore` is relaxed for **`results/`**, **`test/data/`**, **`corpus_repo/corpus_v1/`** (metrics + annotations only; bulky exports listed in `.gitignore`).

### Experiment 07 (generated vs real)

Default real side: **`corpus_repo/real_validation_corpus/`** (`repo_paths.DEFAULT_REAL_VALIDATION_DOCS_DIR`). Experiment **07** exits with an error if that directory is missing, is not a directory, or contains **no** `.txt` files—there is no synthetic fallback. Discovery is **recursive**; extension match is **case-insensitive** (`.txt` / `.TXT`).

1. **Use your own files** – Copy or sync your real validation `.txt` files into `corpus_repo/real_validation_corpus/` (local only; see `.gitignore`).

2. **Export from your JSON manifest** – If you maintain something like `corpus_repo/real_validation_set.json` with paths or text fields for **real** holdout documents:

   ```bash
   python corpus_repo/export_real_validation_corpus.py
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

## Notes on age parsing (bias 1.4)

Experiment **1.4 (age distribution)** extracts ages from `entidades/` and bins them by decade. Besides numeric ages (e.g. `70 años`), it also recovers some **text-only** age mentions:

- **`sexagenario/a`** → bin **60–69**
- **`septuagenario/a`** → **70–79**
- **`octogenario/a`** → **80–89**
- **`nonagenario/a`** → **90–99**
- **`centenario/a`** → **100–109**
- **`sexta década`** → **50–59**
- **`séptima década`** → **60–69**
- **`octava década`** → **70–79**
- **`novena década`** → **80–89**
- **`décima década`** → **90–99**
- **`octogenario próximo`** → **70–79** (agreed conservative mapping)

Vague descriptors like `adulto mayor`, `edad avanzada`, `geriátrico` are **not** converted to a numeric decade bin.

## License

MIT — see **[LICENSE](LICENSE)**.

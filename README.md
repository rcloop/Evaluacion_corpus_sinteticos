# Synthetic corpus evaluation

Evaluation of synthetic clinical corpora across **bias**, **privacy**, and **text naturalness**.

## Layout

- **`src/`** – Source code
  - **`experimentos/`** – Numbered entry-point scripts:
    - **`sesgos/`** – scripts `01`…`13` (one metric per file) and **`_lib/`** (shared bias logic)
    - **`privacidad/`** – scripts `01`…`03` and **`_lib/`** (attribute / membership / memorization)
    - **`naturalidad/`** – scripts `01`…`07` and **`_lib/`** (perplexity, coherence, readability, etc.)
  - **`utils/`** – Shared helpers (optional; see folder)
  - **`models/`** – Model-related references or assets, if any
- **`test/`** – Pytest suite and minimal data under `test/data/`
- **`corpus_repo/corpus_v1/`** – Versioned synthetic corpus (`documents/` + `entidades/`). The real validation tree under `corpus_repo/real_validation_corpus/` is not tracked (see `.gitignore`).
- **`data/`** – Additional reference data (small samples, lexicons, etc.)
- **`results/`** – Experiment outputs (JSON and similar; see below)
- **`scripts/`** – Auxiliary scripts (data prep, utilities)
- **`restos/`** (optional, **untracked**) – Local snapshots of legacy suites; listed in `.gitignore` and not pushed
- **Repo root** – `requirements.txt`, plus optional `run.ps1` / `run_*.py` orchestration

All evaluation logic lives under **`src/experimentos/`** and the per-suite **`_lib/`** folders.

### Outputs (`results/`)

Write outputs under **`results/`** at the repo root, not under `src/`:

- `results/sesgos/01` … `13`
- `results/privacidad/01` … `03`
- `results/naturalidad/01` … `07`

`src/` should hold **code** only. JSON, logs, and generated artifacts belong in **`results/`**.

A global `*.json` rule exists in `.gitignore`, but **`results/`**, **`test/data/`**, and **`corpus_repo/corpus_v1/`** JSON paths are **tracked** so clones get metrics and annotation fixtures. **`test/data/`** and synthetic **`corpus_v1`** `.txt` files are tracked; `results/**/*.txt` log files are ignored.

## Requirements

```bash
pip install -r requirements.txt
```

Includes **PyTorch**, **transformers** (naturalness: perplexity 02, optional AI detection), and **sentence-transformers** (coherence 06, semantic memorization). If `torch` fails to install, try `pip install torch` first, then the rest.

**NVIDIA GPU:** the default install may be CPU-only. For GPU on perplexity, coherence, memorization, and AI detection:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
```

Adjust `cu124` to your CUDA stack if needed; see [pytorch.org](https://pytorch.org). Check with: `python -c "import torch; print(torch.cuda.is_available())"`.

**Tests:** the same stack covers `pytest` and `test/`.

## Usage

- **Numbered experiments:** see `src/experimentos/README.md`. Example:  
  `python src/experimentos/sesgos/01_name_gender_distribution.py --corpus_root <path>`  
  Each script writes flat outputs (e.g. JSON) under `results/<suite>/<NN>/`.

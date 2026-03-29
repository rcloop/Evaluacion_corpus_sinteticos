# Corpus (corpus_repo)

## Corpus sintético anotado: `corpus_v1`

**`corpus_repo/corpus_v1`** es el corpus sintético sobre el que se ejecutan todos los experimentos (sesgos, privacidad, naturalidad). Debe contener:

- **`documents/`** — documentos de texto (p. ej. `.txt`), generados de forma sintética.
- **`entidades/`** — anotaciones de entidades sintéticas (formato esperado por los scripts de sesgos y privacidad).

Los scripts de la suite toman este corpus por defecto:

- `run_all_experiments.py` — usa `--corpus_root corpus_repo/corpus_v1` por defecto.
- `run_missing_experiments.py` — usa `--corpus_root corpus_repo/corpus_v1` por defecto.
- `src/experimentos/run_missing_full_corpus.ps1` — invoca el runner con `corpus_repo\corpus_v1`.

## Otros recursos

- **`real_validation_set.json`** — documentos reales (no generados); origen del corpus de validación.
- **`real_validation_corpus/`** — export en `.txt` desde `real_validation_set.json`; se usa como referencia real en el experimento 07 (comparación estadística generado vs real).
- **`export_real_validation_corpus.py`** — script para regenerar `real_validation_corpus/` a partir del JSON.

## Resumen

| Recurso | Uso |
|--------|-----|
| `corpus_v1/` | Corpus sintético anotado; **referencia para todos los experimentos**. |
| `real_validation_corpus/` | Corpus real; referencia en exp. 07 (naturalidad, comparación). |

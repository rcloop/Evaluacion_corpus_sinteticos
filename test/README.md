# Tests de experimentos

Tests para los scripts en `src/experimentos/` (sesgos, privacidad, naturalidad).

## Datos de prueba

- **`data/corpus_mini/`**: corpus mínimo con `documents/` (2 .txt) y `entidades/` (2 .json) para sesgos y privacidad.
- **`data/corpus_naturalidad/`**: 2 archivos .txt para experimentos de naturalidad.

## Ejecutar tests

Desde la raíz del repo:

```bash
pip install pytest
pytest test/
```

Solo un tipo de experimentos:

```bash
pytest test/test_experimentos_sesgos.py
pytest test/test_experimentos_privacidad.py
pytest test/test_experimentos_naturalidad.py
```

Algunos tests pueden requerir dependencias de las suites (scipy, sklearn, etc.). Instala `requirements.txt` y los `requirements.txt` de `src/bias_evaluation` y `src/privacy_evaluation` si hace falta.

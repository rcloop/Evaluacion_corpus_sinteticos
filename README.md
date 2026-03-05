# Evaluacion_corpus_sinteticos

Evaluación de corpus sintéticos: sesgo (bias), privacidad y naturalidad sobre textos clínicos.

## Estructura

- **`src/`** – Código fuente
  - `bias_evaluation/` – Suite de evaluación de sesgo
  - `privacy_evaluation/` – Suite de evaluación de privacidad
  - `utils/` – Utilidades compartidas
  - `experimentos/` – Experimentos numerados: `sesgos/01`…`13`, `privacidad/01`…`03`, `naturalidad/01`…`07` (un script por métrica)
  - `models/` – Definiciones o referencias a modelos
  - `test/` – Tests
- **`data/`** – Datos (corpus, muestras)
- **`results/`** – Resultados de experimentos, numerados por tipo:
  - `results/sesgos/01` … `13` – resultados de cada métrica de sesgo
  - `results/privacidad/01` … `03` – resultados de privacidad (Attribute, Membership, Memorization)
  - `results/naturalidad/01` … `07` – resultados de naturalidad (AI detection, perplexity, vocabulario, legibilidad, diversidad, coherencia, comparación estadística)
- **`bibliography/`** – Documentos de referencia y explicaciones (.md, .tex)

## Requisitos

```bash
pip install -r requirements.txt
```

Cada submódulo (`src/bias_evaluation`, `src/privacy_evaluation`) puede tener requisitos adicionales en su propio `requirements.txt`.

## Uso

- **Experimentos numerados:** ver `src/experimentos/README.md`. Ejemplo:  
  `python src/experimentos/sesgos/01_name_gender_distribution.py --corpus_root <ruta>`
- **Suites originales:** ver README en `src/bias_evaluation/` y `src/privacy_evaluation/`.

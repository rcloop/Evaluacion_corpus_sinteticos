# Bias Evaluation Suite

Suite mínima para evaluar **bias / fairness** en un dataset de **clasificación binaria** por grupos (atributo sensible).

## Quick start (Windows)

Desde `src/bias_evaluation/`:

```bash
python setup_venv.py
```

Ejecutar:

```powershell
.\run_bias_suite.ps1 -DataPath "..\..\ruta\al\archivo.csv" -SensitiveCol "sexo"
```

## Formato de entrada (CSV)

El CSV debe tener header e incluir:

- `y_true` (**requerido**): 0/1 (también acepta true/false)
- `y_pred` (**opcional**): 0/1
- `y_score` (**opcional**): float (si no hay `y_pred`, se deriva `y_pred = y_score >= threshold`)
- columna sensible: la que indiques con `--sensitive_col` / `-SensitiveCol`

Ejemplo:

```text
y_true,y_score,sexo
1,0.92,F
0,0.33,M
1,0.51,F
0,0.49,M
```

## Salida

Genera un JSON (por default `bias_evaluation_results/bias_report.json`) con:

- métricas globales y por grupo (accuracy, selection_rate, TPR/FPR, precision, etc.)
- gaps/ratios clásicos:
  - demographic parity difference / ratio (disparate impact)
  - equal opportunity difference (TPR gap)
  - false positive rate difference (FPR gap)
  - equalized odds difference

## Métrica 1.1: Distribución de género en nombres (sintéticos)

Proporción fem/masc/otros-no-determinable para:

- `NOMBRE_SUJETO_ASISTENCIA` (alias: `NAME_OF_ASSISTED_SUBJECT`)
- `NOMBRE_PERSONAL_SANITARIO` (alias: `NAME_OF_HEALTHCARE_PERSONNEL`)

Ejemplo con el corpus v1:

```powershell
cd .\src\bias_evaluation
.\venv\Scripts\Activate.ps1
python .\name_gender_distribution.py `
  --annotations_path "..\..\corpus_repo\corpus_v1\entidades" `
  --make_plot
```

Salida:

- `bias_evaluation_results/name_gender_distribution.json`
- `bias_evaluation_results/name_gender_distribution_stacked.png` (si `matplotlib` está instalado)

## Métrica 1.2: Sesgo rol‑profesión vs género

Matriz de contingencia **(género × rol/profesión)** a partir de `NOMBRE_PERSONAL_SANITARIO` + `PROFESION` (asociado por documento).

```powershell
cd .\src\bias_evaluation
.\venv\Scripts\Activate.ps1
python .\role_profession_gender_bias.py `
  --annotations_path "..\..\corpus_repo\corpus_v1\entidades" `
  --max_files 200 `
  --make_plot
```

Salida:

- `bias_evaluation_results/role_profession_gender_bias.json`
- `bias_evaluation_results/role_profession_gender_heatmap.png` (si `matplotlib` está instalado)

## Métrica 1.3: Sesgo geográfico / toponímico

Distribución de topónimos por labels geográficos (p.ej. `TERRITORIO`, `PAIS`, `CALLE`, ...), con **top‑k** e **índice de entropía (Shannon)**.

```powershell
cd .\src\bias_evaluation
.\venv\Scripts\Activate.ps1
python .\geographic_toponymic_bias.py `
  --annotations_path "..\..\corpus_repo\corpus_v1\entidades" `
  --top_k 20 `
  --max_files 200 `
  --make_plot
```

Salida:

- `bias_evaluation_results/geographic_toponymic_bias.json`
- `bias_evaluation_results/geographic_toponymic_topk.png` (si `matplotlib` está instalado)

## Métrica 1.4: Distribución de edades (por décadas)

Histograma 0–9, 10–19, ... con porcentajes, entropía, y flags de infrarrepresentación (default: bins \(\ge 80\) con <5%).

```powershell
cd .\src\bias_evaluation
.\venv\Scripts\Activate.ps1
python .\age_distribution.py `
  --annotations_path "..\..\corpus_repo\corpus_v1\entidades" `
  --make_plot
```

Salida:

- `bias_evaluation_results/age_distribution.json`
- `bias_evaluation_results/age_distribution_hist.png` (si `matplotlib` está instalado)

## Métrica 1.5: Sesgo / concentración en instituciones

Top‑k instituciones y métricas de concentración (**HHI** y **Gini**), con curva de Lorenz.

```powershell
cd .\src\bias_evaluation
.\venv\Scripts\Activate.ps1
python .\institution_bias.py `
  --annotations_path "..\..\corpus_repo\corpus_v1\entidades" `
  --top_k 20 `
  --make_plot
```

Salida:

- `bias_evaluation_results/institution_bias.json`
- `bias_evaluation_results/institution_lorenz.png` (si `matplotlib` está instalado)

## WEAT — Sesgo de género (embedding association)

Análisis **Word Embedding Association Test** (Caliskan et al., 2017) sobre el texto del corpus: asociación de profesiones médicas con términos masculinos vs femeninos. Usa embeddings por co-ocurrencia + SVD y test de permutación para el p-value.

Referencia: [weat_gender_analysis.py](https://github.com/ramsestein/generate_corpus_anonimizacion/blob/main/src/weat_gender_analysis.py)

```powershell
cd .\src\bias_evaluation
.\venv\Scripts\Activate.ps1
python .\weat_gender_analysis.py `
  --documents_path "..\..\corpus_repo\corpus_v1\documents" `
  --max_docs 5000
```

Salida: `bias_evaluation_results/weat_gender_analysis.json` (effect size, p-value, ratio de menciones, co-ocurrencias profesión–género).

## Métricas adicionales (corpus only)

Integradas en `run_bias_suite_corpus_v1.py`:

- **Interseccionalidad** (`intersectional_corpus_bias.json`): género×edad, género×geografía, edad×geografía (tablas contingencia, χ²).
- **Diagnóstico × demografía** (`diagnosis_demography_bias.json`): diagnóstico×género y diagnóstico×edad por documento.
- **Género vs objetivo** (`gender_target_proportion.json`): desviación de la proporción observada respecto a un objetivo (ej. 50/50).
- **Edad vs referencia** (`age_reference_comparison.json`): JSD/L1 entre histograma de edades y distribución de referencia (`--age_reference_path`).
- **Cobertura/completitud** (`coverage_completeness.json`): % de documentos con género, edad, geografía (y combinaciones).
- **Resumen diversidad** (`diversity_summary.json`): variety y balance (entropía) para geografía, instituciones y diagnósticos.

Referencias de ejemplo: `reference_diagnosis_flat.json` (1.6), `reference_age_flat.json` (edad). Ver `BIAS_METRICS_CORPUS_ONLY_ROADMAP.md`.

---

## Métrica 1.6: Sesgo en diagnósticos/condiciones (si hay secciones clínicas)

Extrae diagnósticos/condiciones desde `documents/*.txt` por heurística (headers tipo `Diagnóstico:` y frases tipo `diagnóstico de ...`).

```powershell
cd .\src\bias_evaluation
.\venv\Scripts\Activate.ps1
python .\diagnosis_condition_bias.py `
  --documents_path "..\..\corpus_repo\corpus_v1\documents" `
  --top_k 20 `
  --make_plot
```

Si tienes una distribución de referencia (CSV/JSON `diagnosis->p`), añade:

```powershell
python .\diagnosis_condition_bias.py `
  --documents_path "..\..\corpus_repo\corpus_v1\documents" `
  --reference_path "..\..\ruta\ref_dx.json"
```

Salida:

- `bias_evaluation_results/diagnosis_condition_bias.json`
- `bias_evaluation_results/diagnosis_topk.png` (si `matplotlib` está instalado)



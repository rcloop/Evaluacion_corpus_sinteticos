# Tests de la suite de experimentos (privacidad, sesgos, naturalidad)

Esta carpeta contiene tests para los scripts de evaluación de **corpus sintéticos** (privacidad, sesgos, naturalidad). Los datos de prueba usan un **único corpus_mini** para los tres tipos; el experimento 07 (comparación estadística) usa además un **corpus real mini** como referencia. El objetivo principal es **smoke tests** (que los scripts arranquen y terminen) más algunas comprobaciones de **estructura y sanity** de los JSON generados.

## Diseño: evaluación sin acceso al modelo base

La suite está pensada para evaluar **solo con el corpus sintético** (y opcionalmente corpus externo), **sin acceso al modelo generador** (p. ej. DeepSeek). Todas las métricas se calculan a partir de los textos y anotaciones, o usando modelos públicos como proxy.

- **Privacidad (attribute inference, membership inference)**: ataques sobre los datos; no requieren el modelo generador.
- **Memorization detection**: detección **heurística** de repetición/copia de entidades (similitud exacta y semántica). No mide memorización interna del modelo; mide riesgo de repetición en el corpus.
- **Perplexity**: se calcula con un **modelo proxy** (p. ej. BERT/causal en español), no con el modelo generador. Interpretación: “naturalidad según un LM público”.
- **Sesgos**: WEAT y distribuciones (nombres, geografía, edad, etc.) son **solo corpus** (conteos y embeddings sobre el texto).
- **Naturalidad (AI detection, vocabulario, legibilidad, coherencia, comparación estadística)**: todo sobre el texto y modelos públicos.

Si en el futuro se usan **canaries** para membership inference, conviene documentarlo aquí.

## Datos de prueba

Un **mismo corpus mínimo** (`corpus_mini`) se usa para **todos** los tests: sesgos, privacidad y naturalidad. Incluye 6 documentos en `documents/` y sus anotaciones en `entidades/` (suficientes para clasificadores y splits). El experimento 07 necesita además un corpus **real** de referencia (`real_corpus_mini`).

| Fixture | Ruta | Uso |
|--------|------|-----|
| `corpus_mini_path` | `test/data/corpus_mini/` | Raíz del corpus único: `documents/` (`.txt`) + `entidades/` (`.json`) para sesgos, privacidad y naturalidad |
| `corpus_mini_documents_path` | `test/data/corpus_mini/documents/` | Solo documentos `.txt`; usado por naturalidad 01–06 (y como corpus *generado* en 07) |
| `real_corpus_mini_path` | `test/data/real_corpus_mini/` | Corpus real mini (documentos `.txt` clínicos); usado por el test del experimento 07 como `--real_corpus` |

**Corpus real mini para el 07:** el directorio `test/data/real_corpus_mini/` es **requerido** (igual que `corpus_mini`). En el repo se incluye una versión mini con pocos `.txt`. Si faltara, generarla con:  
`python scripts/generate_real_validation_corpus.py --output_dir test/data/real_corpus_mini --num_docs 10`

Los tests no validan umbrales de producción ni calidad del modelo; solo que los scripts corran y que las salidas tengan la forma esperada.

## Verificación de requirements completos

El archivo **`test_requirements_complete.py`** comprueba que todas las dependencias necesarias están instaladas y que la estructura de experimentos está completa:

- **Paquetes**: cada entrada de `requirements.txt` (numpy, scipy, matplotlib, tqdm, scikit-learn, nltk, torch, transformers, sentence-transformers, pytest) debe ser importable.
- **Versión de Python**: se requiere >= 3.8.
- **Estructura _lib**: existen y están completos los módulos en `sesgos/_lib`, `privacidad/_lib` y `naturalidad/_lib`.
- **Fichero requirements.txt** en la raíz del repo.

Si algún test falla, el mensaje indica qué falta (p. ej. `pip install nltk`).

```bash
pytest test/test_requirements_complete.py -v
```

## Cómo ejecutar

```bash
# Todos los tests
pytest test/ -v

# Solo verificación de requirements
pytest test/test_requirements_complete.py -v

# Solo un módulo de experimentos
pytest test/test_experimentos_sesgos.py -v
pytest test/test_experimentos_privacidad.py -v
pytest test/test_experimentos_naturalidad.py -v
```

## Estructura de los tests

- **Smoke**: cada script se ejecuta con corpus mínimo y se comprueba `returncode == 0`.
- **Estructura/sanity**: para 01 sesgos (name_gender) y 01 privacidad (attribute_inference) se carga el JSON y se comprueban claves esperadas y rangos (proporciones en [0,1], AUC en [0,1], `risk_level` válido).
- **Naturalidad 03**: se comprueba que el JSON de vocabulary_richness tenga `corpus_level`, `document_level` y métricas numéricas coherentes.
- **Datos de test** (`corpus_mini`, `real_corpus_mini`): son **obligatorios**; si faltan, el test **falla** con mensaje claro (no skip). Solo se hace **skip** cuando falta una dependencia opcional pesada (p. ej. PyTorch para Perplexity, sentence-transformers para Coherence) para que el resto de la suite pueda correr.

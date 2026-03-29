# Evaluacion_corpus_sinteticos

Evaluación de corpus sintéticos: sesgo (bias), privacidad y naturalidad sobre textos clínicos.

## Estructura

- **`src/`** – Código fuente de la suite
  - **`experimentos/`** – Punto de entrada para las evaluaciones numeradas:
    - **`sesgos/`** – scripts `01`…`13` (una métrica por archivo) y **`_lib/`** (lógica compartida de sesgo)
    - **`privacidad/`** – scripts `01`…`03` y **`_lib/`** (attribute / membership / memorization)
    - **`naturalidad/`** – scripts `01`…`07` y **`_lib/`** (perplexity, coherencia, legibilidad, etc.)
  - **`utils/`** – Utilidades compartidas (opcional; ver carpeta)
  - **`models/`** – Referencias o artefactos relacionados con modelos, si los hay
- **`test/`** – Tests pytest y datos mínimos (`test/data/`)
- **`data/`** – Datos de referencia (por ejemplo corpus real de validación para comparaciones)
- **`results/`** – **Salidas numéricas** de los experimentos (JSON, etc.; ver siguiente apartado)
- **`interpretacion/`** – Textos de interpretación y apoyo al paper (Markdown); **no se versiona** (`.gitignore`).
- **`scripts/`** – Scripts auxiliares (preparación de datos, utilidades)
- **`restos/`** (opcional, **no se versiona**) – Si mantienes copias locales de suites antiguas (`bias_evaluation`, `privacy_evaluation`), colócalas aquí; está listada en `.gitignore` y no se sube a GitHub.
- **Raíz** – `requirements.txt`, y opcionalmente `run.ps1` / `run_*.py` para orquestar ejecuciones

La lógica de evaluación vive bajo **`src/experimentos/`** y sus **`_lib/`**; no hace falta otra carpeta de suite bajo `src/` para ejecutar los experimentos.

### Dónde van los resultados (`results/`)

Convención del proyecto: **escribir siempre bajo `results/` en la raíz del repositorio**, no bajo `src/`:

- `results/sesgos/01` … `13`
- `results/privacidad/01` … `03`
- `results/naturalidad/01` … `07`

**Motivo:** `src/` debe contener **código** (módulos y scripts). Los JSON, logs y tablas generadas son **artefactos**; mantenerlos en `results/` en la raíz evita mezclarlos con paquetes Python y simplifica `.gitignore` y la reproducción de experimentos.

Los resultados por experimento existen **una sola vez**, bajo `results/` en la raíz (no bajo `src/`).

La **interpretación** (textos para paper, notas) es **manual** y puede vivir en **`interpretacion/`** (local, `.gitignore`). El repo publica **resultados planos** bajo `results/` (p. ej. JSON de métricas). En `.gitignore`, `*.json` es global por defecto, pero **sí se versionan** los JSON de **`results/`** y los de **`test/data/`** (fixtures), para que quien clone el repo pueda ver números y ejecutar tests. Los **`.txt`** del corpus grande siguen fuera porque las carpetas `corpus/` y `corpus_repo/` están ignoradas; los **`.txt`** de **`test/data/`** sí pueden versionarse. Los `.txt` tipo log bajo `results/` se ignoran.

## Requisitos

```bash
pip install -r requirements.txt
```

Incluye **PyTorch** y **transformers** (para naturalidad: perplexity 02, AI detection opcional) y **sentence-transformers** (coherencia 06, memorization semántica). Si falla la instalación de `torch`, prueba primero: `pip install torch` y luego el resto.

**Usar GPU (NVIDIA CUDA):** por defecto `pip install -r requirements.txt` puede instalar PyTorch solo CPU. Para usar la GPU en perplexity, coherence, memorization y AI detection, instala PyTorch con CUDA y luego el resto:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
```

(ajusta `cu124` a tu versión de CUDA si hace falta; ver [pytorch.org](https://pytorch.org)). Comprobar: `python -c "import torch; print(torch.cuda.is_available())"`.

**Tests:** las mismas dependencias cubren `pytest` y la ejecución de `test/`.

## Uso

- **Experimentos numerados:** ver `src/experimentos/README.md`. Ejemplo:  
  `python src/experimentos/sesgos/01_name_gender_distribution.py --corpus_root <ruta>`  
  Cada script escribe **salidas planas** (p. ej. JSON) en `results/<tipo>/<NN>/`; no hay generadores automáticos de textos interpretativos en el código.

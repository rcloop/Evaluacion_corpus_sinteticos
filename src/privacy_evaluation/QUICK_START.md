# Quick Start Guide - Privacy Evaluation Suite

## Pasos para Ejecutar la Suite de Evaluación de Privacidad

### Paso 1: Verificar/Activar el Entorno Virtual

**Verificar si estás en el venv:**
```bash
cd src\privacy_evaluation
python check_venv.py
```

**Si NO estás en el venv, activarlo:**
```bash
# Windows (CMD)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de tu prompt.

### Paso 2: Verificar/Instalar Dependencias

**Verificar si las dependencias están instaladas:**
```bash
python -c "import sklearn, numpy, sentence_transformers; print('✓ Todas las dependencias instaladas')"
```

**Si falta alguna dependencia, instalar:**
```bash
pip install -r requirements.txt
```

### Paso 3: Preparar los Datos

Asegúrate de tener:
- **Corpus de textos**: Los 14,035 textos sintéticos
  - Formato: Directorio con archivos `.txt` o archivo `.json`
  - Ruta esperada: `../../corpus/documents/` o similar
- **Anotaciones (opcional)**: Archivos JSON con entidades PHI
  - Ruta esperada: `../../corpus/entidades/` o similar

**Verificar estructura del corpus:**
```bash
# Si tienes un directorio de documentos
dir ..\..\corpus\documents  # Windows
ls ../../corpus/documents    # Linux/Mac

# Si tienes un archivo JSON
dir ..\..\corpus\documents  # Windows
ls ../../corpus/documents    # Linux/Mac
```

### Paso 4: Ejecutar las Evaluaciones

#### Opción A: Ejecutar TODAS las evaluaciones (Recomendado)

```bash
python run_all_privacy_evaluations.py \
    --corpus_path ..\..\corpus\documents \
    --annotations_path ..\..\corpus\entidades \
    --output_dir privacy_evaluation_results
```

**En Windows PowerShell (una línea - RECOMENDADO):**
```powershell
python run_all_privacy_evaluations.py --corpus_path ..\..\corpus\documents --annotations_path ..\..\corpus\entidades --output_dir privacy_evaluation_results
```

**O usando el script PowerShell:**
```powershell
.\run_evaluations_no_semantic.ps1
```

**En Windows CMD:**
```cmd
python run_all_privacy_evaluations.py --corpus_path ..\..\corpus\documents --annotations_path ..\..\corpus\entidades --output_dir privacy_evaluation_results
```

#### Opción B: Ejecutar TODAS las evaluaciones SIN similitud semántica (Más rápido)

**En Windows PowerShell (una línea):**
```powershell
python run_all_privacy_evaluations.py --corpus_path ..\..\corpus\documents --annotations_path ..\..\corpus\entidades --output_dir privacy_evaluation_results --skip_semantic
```

**O usando el script helper (PowerShell):**
```powershell
.\run_evaluations_no_semantic.bat --corpus_path ..\..\corpus\documents --annotations_path ..\..\corpus\entidades
```

**En CMD o Linux/Mac:**
```bash
python run_all_privacy_evaluations.py \
    --corpus_path ../corpus/documents \
    --annotations_path ../corpus/entidades \
    --output_dir privacy_evaluation_results \
    --skip_semantic
```

**Nota:** Esto ejecuta todas las evaluaciones excepto la búsqueda de similitud semántica, reduciendo el tiempo de ~3-7 horas a ~30-60 minutos.

#### Opción C: Ejecutar evaluaciones individuales

**1. Membership Inference:**
```bash
python membership_inference.py --corpus_path ..\..\corpus\documents --output_path membership_inference_results.json
```

**2. Attribute Inference:**
```bash
python attribute_inference.py --corpus_path ..\..\corpus --output_path attribute_inference_results.json
```

**3. Memorization Detection:**
```bash
python nearest_neighbor_memorization.py --corpus_path ..\..\corpus\documents --annotations_path ..\..\corpus\entidades --output_path memorization_results.json
```

**4. Canary Insertion:**
```bash
python canary_insertion.py --original_corpus_path ..\..\corpus\documents --generated_corpus_path ..\..\corpus\documents --output_path canary_results.json
```

### Paso 5: Revisar los Resultados

Los resultados se guardarán en:
- `privacy_evaluation_results/` (si usaste `--output_dir`)
- O en el directorio actual (si especificaste `--output_path`)

**Archivos generados:**
- `membership_inference.json` - Resultados de membership inference
- `attribute_inference.json` - Resultados de attribute inference
- `memorization_detection.json` - Resultados de detección de memorización
- `canary_insertion.json` - Resultados de canary insertion
- `consolidated_privacy_report.json` - Reporte consolidado con evaluación de riesgo general

**Ver resultados:**
```bash
# Windows
type privacy_evaluation_results\consolidated_privacy_report.json

# Linux/Mac
cat privacy_evaluation_results/consolidated_privacy_report.json
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'sklearn'"
**Solución:** Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "No se encontró el corpus"
**Solución:** Verifica la ruta del corpus. Usa rutas absolutas si es necesario:
```bash
python run_all_privacy_evaluations.py --corpus_path "C:\Users\Usuario\Anonimization_research\corpus\documents"
```

### Error: "Out of memory" durante semantic similarity
**Solución:** 
- Usa `requirements-minimal.txt` para desactivar semantic similarity
- O procesa el corpus en lotes más pequeños
- O usa una GPU si está disponible

### El proceso es muy lento
**Solución:**
- La búsqueda de similitud semántica puede tardar horas con 14,035 textos
- Considera usar GPU: `pip install torch --index-url https://download.pytorch.org/whl/cu118`
- O ejecuta solo las evaluaciones que necesites (sin semantic similarity)

## Tiempo Estimado de Ejecución

Para un corpus de 14,035 textos:
- **Membership Inference**: ~5-15 minutos
- **Attribute Inference**: ~10-30 minutos
- **Memorization Detection (exact)**: ~5-10 minutos
- **Memorization Detection (semantic)**: ~2-6 horas ⚠️
- **Canary Insertion**: ~5-15 minutos
- **Total (sin semantic)**: ~30-60 minutos
- **Total (con semantic)**: ~3-7 horas

## Próximos Pasos Después de la Ejecución

1. **Revisar el reporte consolidado** (`consolidated_privacy_report.json`)
2. **Integrar resultados en el paper** usando `Privacy_Evaluation_Section_Paper.md`
3. **Reemplazar valores `[X.XX]`** en la sección del paper con los resultados reales
4. **Decidir sobre DP** basándote en los niveles de riesgo detectados

## Comando Rápido (Todo en Uno)

```bash
# 1. Ir al directorio
cd src\privacy_evaluation

# 2. Activar venv
venv\Scripts\activate

# 3. Verificar dependencias
python -c "import sklearn, numpy, sentence_transformers; print('OK')"

# 4. Ejecutar todas las evaluaciones
python run_all_privacy_evaluations.py --corpus_path ..\..\corpus\documents --annotations_path ..\..\corpus\entidades --output_dir privacy_evaluation_results
```


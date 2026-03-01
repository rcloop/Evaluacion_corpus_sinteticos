# Tiempo Estimado de Ejecución - Privacy Evaluation Suite

## Corpus: 14,035 documentos sintéticos

### Tiempo Estimado por Evaluación (SIN similitud semántica)

| Evaluación | Tiempo Estimado | Complejidad | Notas |
|------------|----------------|-------------|-------|
| **1. Membership Inference** | 15-30 min | Media | Vectorización TF-IDF de 14k textos, entrenamiento modelo |
| **2. Attribute Inference** | 20-40 min | Media-Alta | Múltiples modelos (uno por atributo PHI) |
| **3. Memorization Detection** | 10-20 min | Baja | Solo búsqueda exacta (sin semántica) |
| **4. Canary Insertion** | 10-15 min | Baja | Generación e inserción de canaries |
| **TOTAL (sin semántica)** | **55-105 min** | | **~1-2 horas** |

### Tiempo Estimado CON similitud semántica

Si ejecutas **CON** similitud semántica (sin `--skip_semantic`):

| Evaluación | Tiempo Estimado |
|------------|----------------|
| **3. Memorization Detection (con semántica)** | **2-6 horas** ⚠️ |
| **TOTAL (con semántica)** | **3-7 horas** |

## Factores que Afectan el Tiempo

### Aceleran:
- ✅ **CPU rápido**: Procesamiento más rápido
- ✅ **RAM suficiente**: Evita swapping
- ✅ **SSD**: Carga de archivos más rápida
- ✅ **Sin similitud semántica**: Ahorra 2-6 horas

### Ralentizan:
- ⚠️ **CPU lento**: Más tiempo de procesamiento
- ⚠️ **Poca RAM**: Swapping a disco
- ⚠️ **HDD**: Carga más lenta
- ⚠️ **Con similitud semántica**: Requiere cargar modelo de transformers

## Recomendación

**Para una primera ejecución rápida:**
```powershell
# Ejecuta SIN similitud semántica (~1-2 horas)
python run_all_privacy_evaluations.py `
    --corpus_path "..\..\corpus_repo\corpus\documents" `
    --annotations_path "..\..\corpus_repo\corpus\entidades" `
    --output_dir privacy_evaluation_results `
    --skip_semantic
```

**Si necesitas similitud semántica después:**
```powershell
# Ejecuta solo memorization detection CON semántica (2-6 horas adicionales)
python nearest_neighbor_memorization.py `
    --corpus_path "..\..\corpus_repo\corpus\ner_dataset.json" `
    --annotations_path "..\..\corpus_repo\corpus\entidades" `
    --output_path memorization_semantic.json
```

## Monitoreo del Progreso

Los scripts muestran progreso en tiempo real:
- Número de textos cargados
- Progreso de vectorización
- Progreso de entrenamiento
- Resultados parciales

## Interrupción y Reanudación

- Puedes interrumpir con `Ctrl+C` en cualquier momento
- Los resultados parciales se guardan automáticamente
- Puedes ejecutar evaluaciones individuales si una falla



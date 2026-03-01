# Naturalness Evaluation - Quick Start

## ✅ Venv Configuration

**Sí, todos los scripts están configurados para usar el venv.**

El venv está en: `src/privacy_evaluation/venv/`

## Dependencias Instaladas

Todas las dependencias necesarias están instaladas en el venv:
- ✅ numpy
- ✅ scikit-learn
- ✅ sentence-transformers
- ✅ transformers
- ✅ torch
- ✅ nltk (recién instalado)
- ✅ scipy (ya estaba instalado)

## Cómo Ejecutar

### Opción 1: Scripts con Venv Automático (Recomendado)

**PowerShell:**
```powershell
cd C:\Users\Usuario\Anonimization_research\src\privacy_evaluation
.\naturalness_evaluation\run_naturalness_with_venv.ps1
```

**CMD/Batch:**
```cmd
cd C:\Users\Usuario\Anonimization_research\src\privacy_evaluation
naturalness_evaluation\run_naturalness_with_venv.bat
```

### Opción 2: Activar Venv Manualmente

**PowerShell:**
```powershell
cd C:\Users\Usuario\Anonimization_research\src\privacy_evaluation
.\venv\Scripts\Activate.ps1
python naturalness_evaluation\run_all_naturalness_evaluations.py --generated_corpus "..\..\corpus_repo\corpus\documents" --output_dir naturalness_results --sample_size 1000
```

**CMD:**
```cmd
cd C:\Users\Usuario\Anonimization_research\src\privacy_evaluation
venv\Scripts\activate.bat
python naturalness_evaluation\run_all_naturalness_evaluations.py --generated_corpus "..\..\corpus_repo\corpus\documents" --output_dir naturalness_results --sample_size 1000
```

### Opción 3: Usar Python del Venv Directamente

```powershell
cd C:\Users\Usuario\Anonimization_research\src\privacy_evaluation
.\venv\Scripts\python.exe naturalness_evaluation\run_all_naturalness_evaluations.py --generated_corpus "..\..\corpus_repo\corpus\documents" --output_dir naturalness_results --sample_size 1000
```

## Verificar Venv

Para verificar que estás usando el venv:

```powershell
python check_venv.py
```

O:

```powershell
.\venv\Scripts\python.exe -c "import sys; print('Python:', sys.executable)"
```

Deberías ver: `C:\Users\Usuario\Anonimization_research\src\privacy_evaluation\venv\Scripts\python.exe`

## Ejecutar Evaluaciones Individuales

Todos los scripts individuales también funcionan con el venv:

```powershell
# Activar venv primero
.\venv\Scripts\Activate.ps1

# Luego ejecutar cualquier script
python naturalness_evaluation\vocabulary_richness.py --corpus_path "..\..\corpus_repo\corpus\documents"
python naturalness_evaluation\readability.py --corpus_path "..\..\corpus_repo\corpus\documents"
# etc.
```

## Notas

- Todos los scripts están diseñados para funcionar con el venv existente
- Las dependencias están instaladas en el venv
- Los scripts detectan automáticamente si NLTK/otros están disponibles
- Si falta alguna dependencia, los scripts mostrarán un warning pero continuarán con las métricas disponibles


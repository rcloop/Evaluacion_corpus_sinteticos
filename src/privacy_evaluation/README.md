# Privacy Evaluation Suite

This directory contains scripts for comprehensive privacy evaluation of the synthetic medical corpus.

**🚀 Quick Start:** See [QUICK_START.md](QUICK_START.md) for step-by-step instructions.

## Overview

The privacy evaluation suite includes three main evaluations:

1. **Membership Inference**: Tests whether an attacker can determine if a specific text was in the training corpus
2. **Attribute Inference**: Tests whether an attacker can infer sensitive attributes (PHI types) from texts
3. **Memorization Detection**: Detects potential memorization of names/identifiers through exact and semantic similarity search

## Installation

### Opción 1: Usando el script Python (Recomendado - Multiplataforma)

```bash
python setup_venv.py
```

Este script funciona en Windows, Linux y Mac y creará automáticamente un entorno virtual (`venv`) e instalará todas las dependencias.

### Opción 2: Usando scripts específicos del sistema

**Windows:**
```bash
setup_venv.bat
```

**Linux/Mac:**
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

### Opción 3: Configuración manual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Usage

### Activar el entorno virtual

Antes de ejecutar cualquier script, asegúrate de activar el entorno virtual:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Run All Evaluations

**Opción 1: Usando el script helper (Windows)**
```bash
run_evaluations.bat --corpus_path ..\..\corpus\documents --annotations_path ..\..\corpus\entidades
```

**Opción 2: Ejecutar directamente**
```bash
python run_all_privacy_evaluations.py \
    --corpus_path ../corpus/documents \
    --annotations_path ../corpus/entidades \
    --output_dir privacy_evaluation_results
```

### Run Individual Evaluations

#### Membership Inference

```bash
python membership_inference.py \
    --corpus_path ../corpus/documents \
    --external_corpus_path ../external_corpus \
    --output_path membership_inference_results.json
```

#### Attribute Inference

```bash
python attribute_inference.py \
    --corpus_path ../corpus \
    --output_path attribute_inference_results.json
```

#### Memorization Detection

```bash
python nearest_neighbor_memorization.py \
    --corpus_path ../corpus/documents \
    --annotations_path ../corpus/entidades \
    --output_path memorization_results.json \
    --semantic_model paraphrase-multilingual-MiniLM-L12-v2 \
    --similarity_threshold 0.85
```

## Output Format

Each evaluation generates a JSON file with:
- Evaluation metrics (AUC-ROC, accuracy, etc.)
- Risk assessment (low/medium/high/critical)
- Interpretation and recommendations

The consolidated report (`consolidated_privacy_report.json`) includes:
- All individual evaluation results
- Overall risk assessment
- Recommendations

## Interpreting Results

### Membership Inference
- **AUC-ROC < 0.6**: Low risk - attack performs poorly
- **AUC-ROC 0.6-0.7**: Medium risk
- **AUC-ROC 0.7-0.8**: High risk
- **AUC-ROC ≥ 0.8**: Critical risk

### Attribute Inference
- Similar thresholds as membership inference
- Check which specific attributes are at risk

### Memorization Detection
- **Low risk**: < 10 repeated entities, < 5 high-similarity pairs
- **Medium risk**: 10-50 repeated entities, 5-20 high-similarity pairs
- **High risk**: 50-200 repeated entities, 20-100 high-similarity pairs
- **Critical risk**: > 200 repeated entities, > 100 high-similarity pairs

## Requirements

### Standard Installation (Recommended)

```bash
pip install -r requirements.txt
```

This installs:
- **numpy**: Numerical operations
- **scikit-learn**: Machine learning utilities (TF-IDF, logistic regression, similarity metrics)
- **sentence-transformers**: Semantic similarity (nearest neighbor search)
- **torch**: PyTorch (dependency of sentence-transformers)
- **transformers**: HuggingFace transformers (dependency of sentence-transformers)

### Minimal Installation (No Semantic Similarity)

If you only need exact similarity search (not semantic), you can use:

```bash
pip install -r requirements-minimal.txt
```

**Note:** This will disable semantic similarity in `nearest_neighbor_memorization.py`.

### Development Dependencies

For development and testing:

```bash
pip install -r requirements-dev.txt
```

## Notes

- The semantic similarity search requires a sentence transformer model. By default, it uses `paraphrase-multilingual-MiniLM-L12-v2` which supports multiple languages including Spanish.
- For large corpora (14,035 texts), the semantic similarity search may take several hours. Consider using a GPU for faster processing.
- **GPU Support**: If you have a CUDA-compatible GPU, install PyTorch with CUDA support for faster processing:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```

## Integration with Paper

The results from these evaluations should be integrated into the paper's privacy evaluation section. See `Privacy_Evaluation_Section_Paper.md` for a template of how to present these results.


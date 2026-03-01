#!/bin/bash
# Script para ejecutar las evaluaciones de privacidad con venv activado (Linux/Mac)

set -e

echo "========================================"
echo "Privacy Evaluation - Ejecutar Evaluaciones"
echo "========================================"
echo ""

# Verificar si el venv existe
if [ ! -d "venv" ]; then
    echo "ERROR: El entorno virtual no existe."
    echo "Por favor ejecuta primero: ./setup_venv.sh"
    exit 1
fi

# Activar venv
echo "Activando entorno virtual..."
source venv/bin/activate

# Ejecutar evaluaciones
if [ $# -eq 0 ]; then
    echo "Uso: ./run_evaluations.sh --corpus_path RUTA [opciones]"
    echo ""
    echo "Ejemplo:"
    echo "  ./run_evaluations.sh --corpus_path ../../corpus/documents --annotations_path ../../corpus/entidades"
    echo ""
    echo "Ejecutando con valores por defecto..."
    echo ""
    python run_all_privacy_evaluations.py --corpus_path ../../corpus/documents --output_dir privacy_evaluation_results
else
    python run_all_privacy_evaluations.py "$@"
fi

echo ""
echo "Evaluaciones completadas."


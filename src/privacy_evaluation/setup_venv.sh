#!/bin/bash
# Script para crear y configurar el entorno virtual para privacy evaluation (Linux/Mac)

set -e

echo "========================================"
echo "Privacy Evaluation - Setup Virtual Environment"
echo "========================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    exit 1
fi

echo "[1/4] Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "El entorno virtual ya existe. Eliminando..."
    rm -rf venv
fi
python3 -m venv venv
echo "✓ Entorno virtual creado"
echo ""

echo "[2/4] Activando entorno virtual..."
source venv/bin/activate
echo "✓ Entorno virtual activado"
echo ""

echo "[3/4] Actualizando pip..."
pip install --upgrade pip
echo "✓ pip actualizado"
echo ""

echo "[4/4] Instalando dependencias..."
pip install -r requirements.txt
echo "✓ Dependencias instaladas"
echo ""

echo "========================================"
echo "Setup completado exitosamente!"
echo "========================================"
echo ""
echo "Para activar el entorno virtual en el futuro, ejecuta:"
echo "  source venv/bin/activate"
echo ""
echo "Para desactivar el entorno virtual:"
echo "  deactivate"
echo ""


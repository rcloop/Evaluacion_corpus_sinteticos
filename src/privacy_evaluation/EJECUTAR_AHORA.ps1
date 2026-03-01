# Script rápido para ejecutar TODAS las evaluaciones SIN similitud semántica
# Uso: .\EJECUTAR_AHORA.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Privacy Evaluation Suite" -ForegroundColor Cyan
Write-Host "Ejecutando SIN similitud semántica" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activar venv
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "ERROR: venv no encontrado. Ejecuta: python setup_venv.py" -ForegroundColor Red
    exit 1
}

# Ejecutar con rutas por defecto
Write-Host "Ejecutando evaluaciones..." -ForegroundColor Green
Write-Host "Corpus: ..\..\corpus\documents" -ForegroundColor Gray
Write-Host "Anotaciones: ..\..\corpus\entidades" -ForegroundColor Gray
Write-Host ""

python run_all_privacy_evaluations.py --corpus_path ..\..\corpus\documents --annotations_path ..\..\corpus\entidades --output_dir privacy_evaluation_results --skip_semantic

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Completado!" -ForegroundColor Green
Write-Host "Resultados en: privacy_evaluation_results\" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan


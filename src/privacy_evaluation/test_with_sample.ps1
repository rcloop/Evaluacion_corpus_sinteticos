# Script para probar con una muestra de 100 documentos
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Privacy Evaluation - Prueba con Muestra (100 docs)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activar venv
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "ERROR: venv no encontrado" -ForegroundColor Red
    exit 1
}

# Crear muestra de 100 documentos
Write-Host "[1/2] Creando muestra de 100 documentos..." -ForegroundColor Yellow
python create_sample.py --n 100 --input "..\..\corpus_repo\corpus\documents" --output "corpus_sample_100.json"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: No se pudo crear la muestra" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Muestra creada" -ForegroundColor Green
Write-Host ""

# Ejecutar evaluaciones con la muestra
Write-Host "[2/2] Ejecutando evaluaciones con muestra..." -ForegroundColor Yellow
Write-Host ""

python run_all_privacy_evaluations.py `
    --corpus_path "corpus_sample_100.json" `
    --annotations_path "..\..\corpus_repo\corpus\entidades" `
    --output_dir privacy_evaluation_results_sample `
    --skip_semantic

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Prueba completada!" -ForegroundColor Green
Write-Host "Resultados en: privacy_evaluation_results_sample\" -ForegroundColor Cyan
Write-Host ""
Write-Host "Si todo funciona bien, ejecuta con el corpus completo:" -ForegroundColor Yellow
Write-Host "  .\EJECUTAR_CON_JSON.ps1" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan




# Script para ejecutar evaluaciones usando el archivo JSON directamente
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Privacy Evaluation - Usando JSON" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activar venv
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "ERROR: venv no encontrado. Ejecuta: python setup_venv.py" -ForegroundColor Red
    exit 1
}

# Ruta al corpus (directorio con archivos .txt)
$corpusPath = "..\..\corpus_repo\corpus\documents"
$annotationsPath = "..\..\corpus_repo\corpus\entidades"

# Verificar que existe
if (-not (Test-Path $corpusPath)) {
    Write-Host "ERROR: No se encontró el directorio del corpus en: $corpusPath" -ForegroundColor Red
    Write-Host "Verifica que el repositorio se haya clonado correctamente." -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Corpus encontrado: $corpusPath" -ForegroundColor Green
Write-Host "✓ Anotaciones: $annotationsPath" -ForegroundColor Green
Write-Host ""
Write-Host "Ejecutando evaluaciones..." -ForegroundColor Yellow
Write-Host ""

# Ejecutar
python run_all_privacy_evaluations.py `
    --corpus_path $corpusPath `
    --annotations_path $annotationsPath `
    --output_dir privacy_evaluation_results `
    --skip_semantic

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Completado!" -ForegroundColor Green
Write-Host "Resultados en: privacy_evaluation_results\" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan



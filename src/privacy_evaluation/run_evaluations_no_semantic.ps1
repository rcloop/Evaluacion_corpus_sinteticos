# Script PowerShell para ejecutar evaluaciones sin similitud semántica

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Privacy Evaluation - Sin Similitud Semantica" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si el venv existe
if (-not (Test-Path "venv")) {
    Write-Host "ERROR: El entorno virtual no existe." -ForegroundColor Red
    Write-Host "Por favor ejecuta primero: python setup_venv.py" -ForegroundColor Yellow
    exit 1
}

# Activar venv
Write-Host "Activando entorno virtual..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

# Ejecutar evaluaciones
Write-Host ""
Write-Host "Ejecutando evaluaciones (sin similitud semántica)..." -ForegroundColor Green
Write-Host ""

$corpusPath = if ($args[0]) { $args[0] } else { "..\..\corpus\documents" }
$annotationsPath = if ($args[1]) { $args[1] } else { "..\..\corpus\entidades" }
$outputDir = if ($args[2]) { $args[2] } else { "privacy_evaluation_results" }

python run_all_privacy_evaluations.py `
    --corpus_path $corpusPath `
    --annotations_path $annotationsPath `
    --output_dir $outputDir `
    --skip_semantic

Write-Host ""
Write-Host "Evaluaciones completadas (sin similitud semántica)." -ForegroundColor Green


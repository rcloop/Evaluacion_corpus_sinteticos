# Script PowerShell para ejecutar evaluaciones de naturalidad con venv activado

# Cambiar al directorio del script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir
Set-Location ..

# Verificar si el venv existe
if (-not (Test-Path "venv")) {
    Write-Host "ERROR: venv no encontrado en el directorio actual" -ForegroundColor Red
    Write-Host "Por favor ejecuta primero: python setup_venv.py" -ForegroundColor Yellow
    exit 1
}

# Activar venv
Write-Host "Activando venv..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

# Verificar que el venv está activo
$pythonPath = (Get-Command python).Source
if ($pythonPath -notlike "*venv*") {
    Write-Host "ADVERTENCIA: El venv podría no estar activo correctamente" -ForegroundColor Yellow
}

Write-Host "Python: $pythonPath" -ForegroundColor Green
Write-Host ""

# Ejecutar las evaluaciones
Write-Host "Ejecutando evaluaciones de naturalidad..." -ForegroundColor Cyan
Write-Host ""

python naturalness_evaluation\run_all_naturalness_evaluations.py `
    --generated_corpus "..\..\corpus_repo\corpus\documents" `
    --output_dir naturalness_evaluation_results `
    --sample_size 1000

Write-Host ""
Write-Host "Evaluaciones completadas!" -ForegroundColor Green


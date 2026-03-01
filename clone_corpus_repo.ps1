# Script para clonar el repositorio del corpus
Write-Host "Clonando repositorio del corpus..." -ForegroundColor Cyan

$repoUrl = "https://github.com/ramsestein/generate_corpus_anonimizacion.git"
$targetDir = "corpus_repo"

if (Test-Path $targetDir) {
    Write-Host "El directorio $targetDir ya existe." -ForegroundColor Yellow
    $response = Read-Host "¿Deseas eliminarlo y clonar de nuevo? (s/n)"
    if ($response -eq "s") {
        Remove-Item -Recurse -Force $targetDir
        Write-Host "Directorio eliminado." -ForegroundColor Green
    } else {
        Write-Host "Cancelado." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "Clonando desde: $repoUrl" -ForegroundColor Green
git clone $repoUrl $targetDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Repositorio clonado exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ubicación: $PWD\$targetDir" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Ahora puedes ejecutar las evaluaciones con:" -ForegroundColor Yellow
    Write-Host "  cd src\privacy_evaluation" -ForegroundColor Gray
    Write-Host "  python run_all_privacy_evaluations.py --corpus_path ..\..\corpus_repo\corpus\documents --annotations_path ..\..\corpus_repo\corpus\entidades --output_dir privacy_evaluation_results --skip_semantic" -ForegroundColor Gray
} else {
    Write-Host "✗ Error al clonar el repositorio." -ForegroundColor Red
    Write-Host "Asegúrate de tener git instalado y acceso a internet." -ForegroundColor Yellow
}


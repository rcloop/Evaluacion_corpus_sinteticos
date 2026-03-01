@echo off
REM Script para ejecutar las evaluaciones de privacidad con venv activado

echo ========================================
echo Privacy Evaluation - Ejecutar Evaluaciones
echo ========================================
echo.

REM Verificar si el venv existe
if not exist venv (
    echo ERROR: El entorno virtual no existe.
    echo Por favor ejecuta primero: setup_venv.bat
    pause
    exit /b 1
)

REM Activar venv
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar si se proporcionaron argumentos
if "%1"=="" (
    echo Uso: run_evaluations.bat --corpus_path RUTA [opciones]
    echo.
    echo Ejemplo:
    echo   run_evaluations.bat --corpus_path ..\..\corpus\documents --annotations_path ..\..\corpus\entidades
    echo.
    echo Ejecutando con valores por defecto...
    echo.
    python run_all_privacy_evaluations.py --corpus_path ..\..\corpus\documents --output_dir privacy_evaluation_results
) else (
    python run_all_privacy_evaluations.py %*
)

echo.
echo Evaluaciones completadas.
pause


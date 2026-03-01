@echo off
REM Script para ejecutar todas las evaluaciones EXCEPTO similitud semántica

echo ========================================
echo Privacy Evaluation - Sin Similitud Semantica
echo ========================================
echo.

REM Verificar si el venv existe
if not exist venv (
    echo ERROR: El entorno virtual no existe.
    echo Por favor ejecuta primero: setup_venv.py
    pause
    exit /b 1
)

REM Activar venv
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Ejecutar evaluaciones sin similitud semántica
echo.
echo Ejecutando evaluaciones (sin similitud semántica)...
echo.

if "%1"=="" (
    echo Uso: run_evaluations_no_semantic.bat --corpus_path RUTA [opciones]
    echo.
    echo Ejemplo:
    echo   run_evaluations_no_semantic.bat --corpus_path ..\..\corpus\documents --annotations_path ..\..\corpus\entidades
    echo.
    echo Ejecutando con valores por defecto...
    echo.
    python run_all_privacy_evaluations.py --corpus_path ..\..\corpus\documents --output_dir privacy_evaluation_results --skip_semantic
) else (
    python run_all_privacy_evaluations.py %* --skip_semantic
)

echo.
echo Evaluaciones completadas (sin similitud semántica).
pause


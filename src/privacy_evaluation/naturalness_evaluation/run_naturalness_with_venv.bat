@echo off
REM Script para ejecutar evaluaciones de naturalidad con venv activado

REM Cambiar al directorio del script
cd /d "%~dp0\.."

REM Verificar si el venv existe
if not exist venv (
    echo ERROR: venv no encontrado
    echo Por favor ejecuta primero: python setup_venv.py
    exit /b 1
)

REM Activar venv
echo Activando venv...
call venv\Scripts\activate.bat

REM Ejecutar las evaluaciones
echo Ejecutando evaluaciones de naturalidad...
echo.

python naturalness_evaluation\run_all_naturalness_evaluations.py ^
    --generated_corpus "..\..\corpus_repo\corpus\documents" ^
    --output_dir naturalness_evaluation_results ^
    --sample_size 1000

echo.
echo Evaluaciones completadas!


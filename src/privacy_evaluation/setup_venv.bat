@echo off
REM Script para crear y configurar el entorno virtual para privacy evaluation

echo ========================================
echo Privacy Evaluation - Setup Virtual Environment
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

echo [1/4] Creando entorno virtual...
if exist venv (
    echo El entorno virtual ya existe. Eliminando...
    rmdir /s /q venv
)
python -m venv venv
if errorlevel 1 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo ✓ Entorno virtual creado
echo.

echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)
echo ✓ Entorno virtual activado
echo.

echo [3/4] Actualizando pip...
python -m pip install --upgrade pip
echo ✓ pip actualizado
echo.

echo [4/4] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo ✓ Dependencias instaladas
echo.

echo ========================================
echo Setup completado exitosamente!
echo ========================================
echo.
echo Para activar el entorno virtual en el futuro, ejecuta:
echo   venv\Scripts\activate.bat
echo.
echo Para desactivar el entorno virtual:
echo   deactivate
echo.
pause


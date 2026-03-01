@echo off
REM Script para instalar dependencias en Windows evitando problemas de compilación

echo ========================================
echo Instalación de Dependencias (Windows)
echo ========================================
echo.

REM Actualizar pip primero
echo [1/4] Actualizando pip...
python -m pip install --upgrade pip
echo.

REM Instalar numpy primero (con wheel precompilado)
echo [2/4] Instalando numpy (wheel precompilado)...
pip install numpy>=1.24.0 --only-binary :all:
if errorlevel 1 (
    echo ERROR: No se pudo instalar numpy
    echo Intentando con versión específica...
    pip install numpy==1.26.4 --only-binary :all:
)
echo.

REM Instalar scikit-learn
echo [3/4] Instalando scikit-learn...
pip install scikit-learn>=1.0.0,<2.0.0
echo.

REM Instalar sentence-transformers y dependencias
echo [4/4] Instalando sentence-transformers y dependencias...
pip install sentence-transformers>=2.2.0,<3.0.0
echo.

REM Verificar instalación
echo ========================================
echo Verificando instalación...
echo ========================================
python -c "import numpy; print('✓ numpy:', numpy.__version__)"
python -c "import sklearn; print('✓ scikit-learn:', sklearn.__version__)"
python -c "import sentence_transformers; print('✓ sentence-transformers: OK')"
echo.

echo ========================================
echo Instalación completada!
echo ========================================
pause


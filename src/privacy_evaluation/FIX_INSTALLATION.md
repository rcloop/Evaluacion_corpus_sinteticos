# Solución a Problemas de Instalación en Windows

## Problema: Error al instalar numpy

Si ves este error:
```
ERROR: Unknown compiler(s): [['icl'], ['cl'], ['cc'], ['gcc'], ['clang'], ['clang-cl'], ['pgcc']]
```

**Causa:** pip está intentando compilar numpy desde el código fuente, pero no encuentra un compilador C.

## Solución Rápida

### Opción 1: Usar el script de instalación (Recomendado)

```bash
install_fix_windows.bat
```

Este script instala las dependencias usando wheels precompilados.

### Opción 2: Instalación manual paso a paso

```bash
# 1. Actualizar pip
python -m pip install --upgrade pip

# 2. Instalar numpy con wheel precompilado
pip install numpy>=1.24.0 --only-binary :all:

# 3. Instalar el resto
pip install scikit-learn>=1.0.0,<2.0.0
pip install sentence-transformers>=2.2.0,<3.0.0
```

### Opción 3: Instalar desde requirements.txt con flag

```bash
pip install -r requirements.txt --only-binary :all: --prefer-binary
```

## Alternativa: Usar versiones específicas con wheels

Si sigue fallando, instala versiones específicas que tienen wheels disponibles:

```bash
pip install numpy==1.26.4 scikit-learn==1.3.2 sentence-transformers==2.2.2 torch==2.1.0 transformers==4.35.0
```

## Verificar Instalación

Después de instalar, verifica:

```bash
python -c "import numpy, sklearn, sentence_transformers; print('✓ Todas las dependencias instaladas')"
```

## Si Aún Falla

1. **Instalar Visual Studio Build Tools:**
   - Descarga: https://visualstudio.microsoft.com/downloads/
   - Instala "Desktop development with C++"

2. **O usar conda en lugar de pip:**
   ```bash
   conda install numpy scikit-learn
   pip install sentence-transformers
   ```

3. **O usar Python 3.10 o 3.11** (en lugar de 3.13) que tiene mejor soporte de wheels:
   - Python 3.13 es muy nuevo y algunos paquetes pueden no tener wheels aún


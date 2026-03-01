# Configuración del Corpus

## ❌ NO incluyas los documentos en Git

Los 14,035 textos son demasiado grandes para Git. En su lugar:

## Opción 1: Clonar el repositorio de ramsestein (Recomendado)

```powershell
# Desde el directorio raíz del proyecto
cd C:\Users\Usuario\Anonimization_research

# Clonar el repositorio (solo si no lo tienes)
git clone https://github.com/ramsestein/generate_corpus_anonimizacion.git corpus_repo

# O si ya lo tienes en otra ubicación, crear un enlace simbólico
# mklink /D corpus C:\ruta\a\tu\repositorio\generate_corpus_anonimizacion\corpus
```

Luego ejecuta las evaluaciones con la ruta correcta:

```powershell
python run_all_privacy_evaluations.py `
    --corpus_path ..\..\corpus_repo\corpus\documents `
    --annotations_path ..\..\corpus_repo\corpus\entidades `
    --output_dir privacy_evaluation_results `
    --skip_semantic
```

## Opción 2: Usar rutas absolutas

Si tienes el corpus en otra ubicación:

```powershell
python run_all_privacy_evaluations.py `
    --corpus_path "C:\ruta\completa\a\corpus\documents" `
    --annotations_path "C:\ruta\completa\a\corpus\entidades" `
    --output_dir privacy_evaluation_results `
    --skip_semantic
```

## Opción 3: Crear estructura local

Si prefieres tener los datos localmente sin clonar todo el repo:

1. Crea el directorio:
```powershell
mkdir C:\Users\Usuario\Anonimization_research\corpus
mkdir C:\Users\Usuario\Anonimization_research\corpus\documents
mkdir C:\Users\Usuario\Anonimization_research\corpus\entidades
```

2. Copia los archivos desde el repo de ramsestein a estos directorios

3. Ejecuta:
```powershell
python run_all_privacy_evaluations.py `
    --corpus_path ..\..\corpus\documents `
    --annotations_path ..\..\corpus\entidades `
    --output_dir privacy_evaluation_results `
    --skip_semantic
```

## Verificar que los archivos existen

Antes de ejecutar, verifica:

```powershell
# Ver cuántos archivos .txt hay
(Get-ChildItem -Path "..\..\corpus\documents" -Filter "*.txt").Count

# Debería mostrar 14,035 (o el número que tengas)
```

## Estructura esperada

```
corpus/
├── documents/
│   ├── doc_0001.txt
│   ├── doc_0002.txt
│   └── ... (14,035 archivos .txt)
└── entidades/
    ├── doc_0001.json
    ├── doc_0002.json
    └── ... (archivos JSON con anotaciones)
```

## Nota sobre .gitignore

Si decides tener el corpus localmente, asegúrate de agregarlo a `.gitignore`:

```
# En .gitignore
corpus/
corpus_repo/
*.txt
!requirements.txt
```


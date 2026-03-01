#!/usr/bin/env python3
"""
Script para crear y configurar el entorno virtual para privacy evaluation.
Funciona en Windows, Linux y Mac.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path


def run_command(command, check=True, shell=False):
    """Ejecuta un comando y muestra el output."""
    if isinstance(command, str):
        command = command.split()
    
    print(f"  Ejecutando: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            check=check,
            shell=shell,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: {e}")
        if e.stderr:
            print(f"  {e.stderr}")
        if check:
            sys.exit(1)
        return e


def get_python_executable():
    """Obtiene la ruta al ejecutable de Python."""
    return sys.executable


def get_venv_python(venv_path):
    """Obtiene la ruta al Python del venv."""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"


def get_pip_command(venv_path):
    """Obtiene el comando pip del venv."""
    if sys.platform == "win32":
        return [str(venv_path / "Scripts" / "pip.exe")]
    else:
        return [str(venv_path / "bin" / "pip")]


def main():
    """Función principal."""
    print("=" * 80)
    print("Privacy Evaluation - Setup Virtual Environment")
    print("=" * 80)
    print()
    
    # Directorio actual
    script_dir = Path(__file__).parent.absolute()
    venv_path = script_dir / "venv"
    requirements_file = script_dir / "requirements.txt"
    
    # Verificar Python
    python_exe = get_python_executable()
    print(f"[1/4] Verificando Python...")
    print(f"  Python: {python_exe}")
    version_result = run_command([python_exe, "--version"], check=False)
    if version_result.returncode != 0:
        print("ERROR: No se pudo verificar la versión de Python")
        sys.exit(1)
    print("✓ Python verificado")
    print()
    
    # Crear venv
    print(f"[2/4] Creando entorno virtual en: {venv_path}")
    if venv_path.exists():
        print("  El entorno virtual ya existe. Eliminando...")
        import shutil
        try:
            shutil.rmtree(venv_path)
            print("  ✓ Entorno virtual anterior eliminado")
        except Exception as e:
            print(f"  ERROR: No se pudo eliminar el entorno virtual: {e}")
            response = input("  ¿Continuar de todos modos? (s/n): ")
            if response.lower() != 's':
                sys.exit(1)
    
    try:
        venv.create(venv_path, with_pip=True)
        print("✓ Entorno virtual creado")
    except Exception as e:
        print(f"ERROR: No se pudo crear el entorno virtual: {e}")
        sys.exit(1)
    print()
    
    # Actualizar pip
    print("[3/4] Actualizando pip...")
    venv_python = get_venv_python(venv_path)
    if not venv_python.exists():
        print(f"ERROR: No se encontró Python en el venv: {venv_python}")
        sys.exit(1)
    
    pip_cmd = get_pip_command(venv_path)
    run_command(pip_cmd + ["install", "--upgrade", "pip"])
    print("✓ pip actualizado")
    print()
    
    # Instalar dependencias
    print("[4/4] Instalando dependencias...")
    if not requirements_file.exists():
        print(f"ADVERTENCIA: No se encontró {requirements_file}")
        print("  Continuando sin instalar dependencias...")
    else:
        print(f"  Instalando desde: {requirements_file}")
        run_command(pip_cmd + ["install", "-r", str(requirements_file)])
        print("✓ Dependencias instaladas")
    print()
    
    # Verificar instalación
    print("[Verificación] Verificando instalación...")
    try:
        import_check = subprocess.run(
            [str(venv_python), "-c", "import sklearn, numpy, sentence_transformers; print('✓ Todas las dependencias están instaladas')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if import_check.returncode == 0:
            print(import_check.stdout.strip())
        else:
            print("  ADVERTENCIA: Algunas dependencias podrían no estar instaladas correctamente")
    except Exception as e:
        print(f"  ADVERTENCIA: No se pudo verificar las dependencias: {e}")
    print()
    
    # Instrucciones
    print("=" * 80)
    print("Setup completado exitosamente!")
    print("=" * 80)
    print()
    print("Para activar el entorno virtual:")
    if sys.platform == "win32":
        print(f"  {venv_path}\\Scripts\\activate")
    else:
        print(f"  source {venv_path}/bin/activate")
    print()
    print("Para desactivar el entorno virtual:")
    print("  deactivate")
    print()
    print("Para ejecutar las evaluaciones:")
    if sys.platform == "win32":
        print("  python run_all_privacy_evaluations.py --corpus_path <ruta>")
    else:
        print("  python run_all_privacy_evaluations.py --corpus_path <ruta>")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


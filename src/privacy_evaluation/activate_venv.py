#!/usr/bin/env python3
"""
Script para activar el entorno virtual.
En Windows, esto abrirá un nuevo shell con el venv activado.
"""

import sys
import os
import subprocess
from pathlib import Path


def find_venv():
    """Busca el venv en el directorio actual o padre."""
    current_dir = Path.cwd()
    
    # Buscar en directorio actual y padre
    search_paths = [
        current_dir / "venv",
        current_dir.parent / "venv",
        current_dir / "env",
        current_dir.parent / "env"
    ]
    
    for venv_path in search_paths:
        if venv_path.exists():
            return venv_path
    
    return None


def activate_venv_windows(venv_path):
    """Activa el venv en Windows abriendo un nuevo cmd con el venv activado."""
    activate_script = venv_path / "Scripts" / "activate.bat"
    
    if not activate_script.exists():
        print(f"ERROR: No se encontró {activate_script}")
        return False
    
    print(f"Activando venv: {venv_path}")
    print("Abriendo nueva ventana de comandos con venv activado...")
    
    # Crear un script temporal que active el venv y mantenga el shell abierto
    temp_script = venv_path.parent / "activate_temp.bat"
    with open(temp_script, 'w', encoding='utf-8') as f:
        f.write(f'@echo off\n')
        f.write(f'call "{activate_script}"\n')
        f.write(f'echo.\n')
        f.write(f'echo [OK] Entorno virtual activado!\n')
        f.write(f'echo Python: {venv_path}\\Scripts\\python.exe\n')
        f.write(f'echo.\n')
        f.write(f'cd /d "{Path.cwd()}"\n')
        f.write(f'cmd /k\n')
    
    # Ejecutar en nueva ventana
    subprocess.Popen(['cmd', '/c', f'start cmd /k "{temp_script}"'])
    
    return True


def activate_venv_unix(venv_path):
    """Activa el venv en Linux/Mac."""
    activate_script = venv_path / "bin" / "activate"
    
    if not activate_script.exists():
        print(f"ERROR: No se encontró {activate_script}")
        return False
    
    print(f"Activando venv: {venv_path}")
    print("\nPara activar el venv, ejecuta en tu terminal:")
    print(f"  source {activate_script}")
    print("\nO ejecuta este script desde tu shell (no desde Python):")
    print(f"  . {activate_script}")
    
    return True


def main():
    """Función principal."""
    print("=" * 80)
    print("Activador de Entorno Virtual")
    print("=" * 80)
    print()
    
    # Buscar venv
    venv_path = find_venv()
    
    if not venv_path:
        print("ERROR: No se encontró ningún entorno virtual.")
        print("\nBuscando en:")
        print(f"  - {Path.cwd() / 'venv'}")
        print(f"  - {Path.cwd().parent / 'venv'}")
        print("\nPara crear un venv, ejecuta:")
        print("  python setup_venv.py")
        return 1
    
    print(f"✓ Venv encontrado: {venv_path}")
    print()
    
    # Activar según el sistema operativo
    if sys.platform == "win32":
        success = activate_venv_windows(venv_path)
        if success:
            print("\n✓ Nueva ventana de comandos abierta con venv activado.")
            print("  Puedes cerrar esta ventana.")
    else:
        success = activate_venv_unix(venv_path)
    
    return 0 if success else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nOperación cancelada.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


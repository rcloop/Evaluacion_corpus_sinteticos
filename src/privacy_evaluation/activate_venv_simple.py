#!/usr/bin/env python3
"""
Versión simple: solo muestra el comando para activar el venv.
"""

import sys
from pathlib import Path


def main():
    """Muestra el comando para activar el venv."""
    current_dir = Path.cwd()
    venv_path = current_dir / "venv"
    
    if not venv_path.exists():
        venv_path = current_dir.parent / "venv"
    
    if not venv_path.exists():
        print("ERROR: No se encontró el venv.")
        print("Ejecuta: python setup_venv.py")
        return 1
    
    print("Para activar el venv, ejecuta:")
    print()
    
    if sys.platform == "win32":
        print(f"  {venv_path}\\Scripts\\activate")
        print()
        print("O en PowerShell:")
        print(f"  {venv_path}\\Scripts\\Activate.ps1")
    else:
        print(f"  source {venv_path}/bin/activate")
    
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())


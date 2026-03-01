#!/usr/bin/env python3
"""
Script para verificar si estás en un entorno virtual (venv).
"""

import sys
import os
from pathlib import Path


def is_venv():
    """
    Verifica si el script está ejecutándose dentro de un entorno virtual.
    
    Returns:
        tuple: (bool, str) - (True si está en venv, mensaje descriptivo)
    """
    # Método 1: Verificar sys.prefix vs sys.base_prefix
    # En un venv, sys.prefix apunta al venv y sys.base_prefix al Python del sistema
    if hasattr(sys, 'real_prefix'):
        # virtualenv (antiguo)
        return True, "virtualenv (método antiguo)"
    elif hasattr(sys, 'base_prefix'):
        if sys.prefix != sys.base_prefix:
            return True, "venv activo"
        else:
            return False, "Python del sistema (no venv)"
    
    # Método 2: Verificar variables de entorno
    if os.environ.get('VIRTUAL_ENV'):
        venv_path = os.environ.get('VIRTUAL_ENV')
        return True, f"venv activo (VIRTUAL_ENV={venv_path})"
    
    # Método 3: Verificar si el ejecutable está en un directorio venv
    python_exe = Path(sys.executable)
    if 'venv' in python_exe.parts or 'env' in python_exe.parts:
        return True, f"venv detectado por ruta: {python_exe}"
    
    return False, "No se detectó un entorno virtual"


def get_venv_info():
    """Obtiene información detallada sobre el entorno virtual."""
    info = {
        'in_venv': False,
        'method': '',
        'python_executable': str(sys.executable),
        'python_version': sys.version,
        'sys_prefix': sys.prefix,
        'sys_base_prefix': getattr(sys, 'base_prefix', 'N/A'),
        'virtual_env': os.environ.get('VIRTUAL_ENV', 'No definido'),
        'pip_location': None
    }
    
    in_venv, method = is_venv()
    info['in_venv'] = in_venv
    info['method'] = method
    
    # Intentar encontrar pip
    try:
        import pip
        info['pip_location'] = pip.__file__
    except ImportError:
        info['pip_location'] = 'pip no disponible'
    
    return info


def main():
    """Función principal."""
    print("=" * 80)
    print("Verificación de Entorno Virtual (venv)")
    print("=" * 80)
    print()
    
    in_venv, method = is_venv()
    
    # Estado visual
    if in_venv:
        status = "✓ SÍ - Estás en un entorno virtual"
        status_symbol = "✓"
    else:
        status = "✗ NO - No estás en un entorno virtual"
        status_symbol = "✗"
    
    print(f"Estado: {status}")
    print(f"Método de detección: {method}")
    print()
    
    # Información detallada
    info = get_venv_info()
    print("Información detallada:")
    print(f"  Python ejecutable: {info['python_executable']}")
    print(f"  Python versión: {info['python_version'].split()[0]}")
    print(f"  sys.prefix: {info['sys_prefix']}")
    print(f"  sys.base_prefix: {info['sys_base_prefix']}")
    print(f"  VIRTUAL_ENV: {info['virtual_env']}")
    print(f"  pip ubicación: {info['pip_location']}")
    print()
    
    # Verificar si existe venv en el directorio actual
    current_dir = Path.cwd()
    venv_paths = [
        current_dir / "venv",
        current_dir.parent / "venv",
        current_dir / "env",
        current_dir.parent / "env"
    ]
    
    existing_venvs = [p for p in venv_paths if p.exists()]
    
    if existing_venvs:
        print("Entornos virtuales encontrados en el directorio:")
        for venv_path in existing_venvs:
            print(f"  - {venv_path}")
            
            # Verificar si este es el venv activo
            if in_venv and str(venv_path) in info['python_executable']:
                print(f"    → Este es el venv activo")
        print()
    
    # Recomendaciones
    print("Recomendaciones:")
    if not in_venv:
        print("  ✗ No estás en un entorno virtual.")
        if existing_venvs:
            print(f"  → Para activar el venv, ejecuta:")
            if sys.platform == "win32":
                for venv_path in existing_venvs:
                    print(f"     {venv_path}\\Scripts\\activate")
            else:
                for venv_path in existing_venvs:
                    print(f"     source {venv_path}/bin/activate")
        else:
            print("  → Para crear un venv, ejecuta:")
            print("     python setup_venv.py")
    else:
        print("  ✓ Estás en un entorno virtual. Todo correcto!")
        print("  → Para desactivar el venv, ejecuta: deactivate")
    
    print()
    print("=" * 80)
    
    # Return code para scripts
    return 0 if in_venv else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nOperación cancelada.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


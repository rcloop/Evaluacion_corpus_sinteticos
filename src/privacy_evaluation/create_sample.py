#!/usr/bin/env python3
"""
Crea una muestra de los primeros N documentos del corpus para pruebas rápidas.
"""

import json
import argparse
from pathlib import Path


def create_sample(input_json: str, output_json: str, n_docs: int = 100):
    """Crea una muestra de los primeros N documentos."""
    print(f"Leyendo corpus completo: {input_json}")
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total = len(data)
    print(f"Total documentos: {total:,}")
    
    # Tomar primeros N
    sample = data[:n_docs]
    print(f"Extrayendo primeros {n_docs} documentos...")
    
    # Guardar muestra
    output_path = Path(output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sample, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Muestra guardada en: {output_path}")
    print(f"  Documentos: {len(sample)}")
    
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crear muestra del corpus")
    parser.add_argument(
        "--input",
        type=str,
        default="../../corpus_repo/corpus/documents",
        help="Archivo JSON de entrada o directorio con archivos .txt"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="corpus_sample_100.json",
        help="Archivo JSON de salida"
    )
    parser.add_argument(
        "--n",
        type=int,
        default=100,
        help="Número de documentos a extraer"
    )
    
    args = parser.parse_args()
    
    create_sample(args.input, args.output, args.n)


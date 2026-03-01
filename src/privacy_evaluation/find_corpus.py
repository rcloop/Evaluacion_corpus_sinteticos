#!/usr/bin/env python3
"""
Script para encontrar el corpus en diferentes ubicaciones posibles.
"""

import os
from pathlib import Path


def find_corpus():
    """Busca el corpus en ubicaciones comunes (directorios .txt o archivos JSON)."""
    import json
    current_dir = Path.cwd()
    root_dir = current_dir.parent.parent
    
    # Buscar directorios con .txt
    possible_dirs = [
        root_dir / "corpus" / "documents",
        root_dir / "corpus_repo" / "corpus" / "documents",
        root_dir / "generate_corpus_anonimizacion" / "corpus" / "documents",
        Path("C:/Users/Usuario/Anonimization_research/corpus/documents"),
        Path("C:/Users/Usuario/generate_corpus_anonimizacion/corpus/documents"),
    ]
    
    # Buscar archivos JSON (mantener compatibilidad con formato JSON)
    possible_json = [
        root_dir / "corpus_repo" / "corpus" / "ner_dataset.json",
        root_dir / "corpus_repo" / "corpus" / "train_set.json",
        root_dir / "corpus" / "ner_dataset.json",
    ]
    
    print("Buscando corpus en ubicaciones posibles...")
    print("=" * 80)
    
    found_locations = []
    
    # Buscar directorios
    for location in possible_dirs:
        if location.exists() and location.is_dir():
            txt_files = list(location.glob("*.txt"))
            if txt_files:
                found_locations.append(("dir", location, len(txt_files)))
                print(f"✓ ENCONTRADO (directorio): {location}")
                print(f"  Archivos .txt: {len(txt_files)}")
                print()
    
    # Buscar JSON
    for json_file in possible_json:
        if json_file.exists() and json_file.is_file():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        count = len(data)
                        found_locations.append(("json", json_file, count))
                        print(f"✓ ENCONTRADO (JSON): {json_file}")
                        print(f"  Documentos: {count}")
                        print()
            except Exception as e:
                pass
    
    if not found_locations:
        print("❌ No se encontró el corpus.")
        print()
        print("Busca en:")
        for loc in possible_dirs + possible_json:
            print(f"  - {loc}")
        print()
        print("Solución: Usa el directorio del corpus:")
        print("  --corpus_path ..\\..\\corpus_repo\\corpus\\documents")
        return None
    
    # Mejor opción
    best = max(found_locations, key=lambda x: x[2])
    loc_type, location, count = best
    
    print("=" * 80)
    print(f"📍 ENCONTRADO: {location}")
    print(f"   Tipo: {loc_type}, Documentos: {count}")
    print()
    print("Comando:")
    print(f"  --corpus_path \"{location}\"")
    
    # Anotaciones
    if loc_type == "json":
        ann_path = location.parent / "entidades"
    else:
        ann_path = location.parent / "entidades"
    
    if ann_path.exists():
        json_files = list(ann_path.glob("*.json"))
        print(f"  --annotations_path \"{ann_path}\" ({len(json_files)} JSON)")
    
    return location


if __name__ == "__main__":
    find_corpus()


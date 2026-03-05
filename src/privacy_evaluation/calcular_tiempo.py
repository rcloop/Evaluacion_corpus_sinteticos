#!/usr/bin/env python3
"""Calcula el tiempo estimado de ejecución para las evaluaciones."""

import json
import os
from pathlib import Path

# Ruta al corpus
corpus_path = Path("../../corpus_repo/corpus/documents")

if not corpus_path.exists():
    print("ERROR: No se encontró el corpus")
    print(f"Buscado en: {corpus_path.absolute()}")
    exit(1)

print("Analizando corpus...")

# Detectar si es directorio o archivo JSON
if corpus_path.is_dir():
    # Es un directorio con archivos .txt
    txt_files = list(corpus_path.glob("*.txt"))
    total_docs = len(txt_files)
    print(f"✓ Total documentos: {total_docs:,}")
    
    # Calcular longitud promedio (muestra)
    sample_size = min(100, total_docs)
    sample_files = txt_files[:sample_size]
    lengths = []
    for txt_file in sample_files:
        with open(txt_file, 'r', encoding='utf-8') as f:
            lengths.append(len(f.read()))
    avg_length = sum(lengths) / len(lengths) if lengths else 0
    total_chars = sum(lengths)
else:
    # Es un archivo JSON
    with open(corpus_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_docs = len(data)
    print(f"✓ Total documentos: {total_docs:,}")
    
    # Calcular longitud promedio (muestra)
    sample_size = min(100, total_docs)
    avg_length = sum(len(d.get('text', '')) for d in data[:sample_size]) / sample_size
    total_chars = sum(len(d.get('text', '')) for d in data[:sample_size])

print(f"✓ Longitud promedio (muestra {sample_size}): {avg_length:.0f} caracteres")
print(f"✓ Total caracteres (estimado): ~{total_docs * avg_length / 1_000_000:.1f}M")

# Calcular tiempos estimados
print("\n" + "=" * 80)
print("TIEMPO ESTIMADO DE EJECUCIÓN")
print("=" * 80)

# Tiempos base por 1000 documentos
base_times = {
    'membership': 1.5,  # minutos por 1000 docs
    'attribute': 2.0,   # minutos por 1000 docs
    'memorization': 1.0, # minutos por 1000 docs (sin semántica)
}

# Calcular tiempos
times = {}
for key, base in base_times.items():
    times[key] = (total_docs / 1000) * base

print(f"\n1. Membership Inference:      {times['membership']:.1f} - {times['membership']*1.5:.1f} minutos")
print(f"2. Attribute Inference:        {times['attribute']:.1f} - {times['attribute']*1.5:.1f} minutos")
print(f"3. Memorization Detection:      {times['memorization']:.1f} - {times['memorization']*1.5:.1f} minutos")

total_min = sum(times.values())
total_max = sum(t * 1.5 for t in times.values())

print(f"\n{'='*80}")
print(f"TOTAL (SIN similitud semántica): {total_min:.0f} - {total_max:.0f} minutos")
print(f"                                  ({total_min/60:.1f} - {total_max/60:.1f} horas)")
print(f"{'='*80}")

# Con semántica
semantic_time = (total_docs / 1000) * 15  # ~15 min por 1000 docs con semántica
print(f"\nSi incluyes similitud semántica:")
print(f"  + Memorization (semántica):    {semantic_time:.0f} - {semantic_time*2:.0f} minutos")
print(f"  TOTAL (CON semántica):        {total_min + semantic_time:.0f} - {total_max + semantic_time*2:.0f} minutos")
print(f"                                 ({total_min/60 + semantic_time/60:.1f} - {total_max/60 + semantic_time*2/60:.1f} horas)")

print(f"\n{'='*80}")
print("RECOMENDACIÓN:")
print(f"  Ejecuta SIN similitud semántica primero (~{total_min/60:.1f}-{total_max/60:.1f} horas)")
print(f"  Luego ejecuta semántica por separado si la necesitas (+{semantic_time/60:.1f} horas)")
print(f"{'='*80}")



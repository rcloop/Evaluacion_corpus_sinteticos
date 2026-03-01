#!/usr/bin/env python3
"""Analiza los resultados del conteo de 'centro de salud los alamos'"""

from collections import Counter
from pathlib import Path

# Leer el archivo de resultados
result_file = Path("resultados_centro_salud_alamos.txt")

if not result_file.exists():
    print("No se encontró el archivo de resultados.")
    exit(1)

# Extraer los conteos (solo líneas que parecen nombres de archivo)
counts = []
with open(result_file, 'r', encoding='utf-8') as f:
    for line in f:
        # Ignorar líneas del encabezado y solo procesar líneas que parecen nombres de archivo
        if ':' in line and 'ocurrencia' in line and '.txt:' in line:
            try:
                count = int(line.split(':')[1].strip().split()[0])
                counts.append(count)
            except:
                pass

# Calcular estadísticas
counter = Counter(counts)

print("=" * 80)
print("ESTADISTICAS: Centro de Salud Los Alamos")
print("=" * 80)
print(f"\nTotal de archivos con ocurrencias: {len(counts)}")
print(f"Total de ocurrencias encontradas: {sum(counts)}")
print(f"Promedio de ocurrencias por archivo: {sum(counts)/len(counts):.2f}")
print(f"Maximo de ocurrencias en un archivo: {max(counts)}")
print(f"Minimo de ocurrencias en un archivo: {min(counts)}")

print("\n" + "=" * 80)
print("DISTRIBUCION DE OCURRENCIAS POR ARCHIVO")
print("=" * 80)
for count in sorted(counter.keys(), reverse=True):
    num_files = counter[count]
    percentage = (num_files / len(counts)) * 100
    print(f"  {count} ocurrencia(s): {num_files:4d} archivo(s) ({percentage:5.2f}%)")


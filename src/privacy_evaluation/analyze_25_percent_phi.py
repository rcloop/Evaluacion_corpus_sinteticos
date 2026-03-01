#!/usr/bin/env python3
"""
Análisis específico: ¿Qué triple de entidades PHI aparece en el 25% del corpus?
Enfocado en el problema de que el 25% de los documentos comparten las mismas 3 etiquetas.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import Counter, defaultdict
from itertools import combinations
from meddocan_label_mapping import map_meddocan_to_phi


def load_corpus_with_annotations(corpus_path: str, annotations_path: str) -> Dict[str, Dict]:
    """Carga el corpus completo con sus anotaciones"""
    corpus = {}
    
    # Cargar corpus
    with open(corpus_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    doc_id = item.get('id', '')
                    if doc_id:
                        corpus[doc_id] = {
                            'text': item.get('text', item.get('content', '')),
                            'filename': item.get('filename', f"doc_{doc_id}.json")
                        }
    
    # Cargar anotaciones
    if os.path.isdir(annotations_path):
        for ann_file in Path(annotations_path).glob("*.json"):
            try:
                with open(ann_file, 'r', encoding='utf-8') as f:
                    ann_data = json.load(f)
                    doc_id = ann_file.stem
                    if doc_id in corpus:
                        corpus[doc_id]['annotations'] = ann_data
            except Exception as e:
                continue
    
    return corpus


def extract_phi_entities_from_annotations(annotations: Dict) -> Dict[str, List[str]]:
    """Extrae entidades PHI de las anotaciones"""
    entities = {
        'person': [],
        'id': [],
        'date': [],
        'location': [],
        'phone': [],
        'email': [],
        'age': []
    }
    
    if not annotations:
        return entities
    
    if isinstance(annotations, dict):
        if 'data' in annotations and isinstance(annotations['data'], list):
            for entity_item in annotations['data']:
                if isinstance(entity_item, dict):
                    entity_type = entity_item.get('entity', '').strip()
                    value = entity_item.get('text', entity_item.get('value', ''))
                    if not value:
                        continue
                    
                    phi_category = map_meddocan_to_phi(entity_type)
                    if phi_category in entities:
                        entities[phi_category].append(value)
    
    return entities


def analyze_25_percent_phi(corpus: Dict[str, Dict]) -> Dict:
    """Analiza si hay triples de entidades que aparecen en el 25% del corpus"""
    
    print("=" * 80)
    print("ANÁLISIS: ¿25% DE DOCUMENTOS COMPARTEN LAS MISMAS 3 ETIQUETAS?")
    print("=" * 80)
    
    # 1. Extraer todas las entidades PHI por documento
    print("\n1. Extrayendo entidades PHI de cada documento...")
    doc_entities = {}
    entity_to_docs = defaultdict(set)
    
    for doc_id, doc_data in corpus.items():
        annotations = doc_data.get('annotations', {})
        entities = extract_phi_entities_from_annotations(annotations)
        
        # Crear conjunto de todas las entidades (sin distinguir tipo)
        all_entities = []
        for phi_type, values in entities.items():
            unique_values = list(set(values))
            all_entities.extend(unique_values)
            for value in unique_values:
                entity_to_docs[value].add(doc_id)
        
        doc_entities[doc_id] = all_entities
    
    print(f"   Documentos procesados: {len(doc_entities)}")
    print(f"   Entidades PHI únicas totales: {len(entity_to_docs)}")
    
    # 2. Encontrar entidades que aparecen en >20% del corpus
    print("\n2. Identificando entidades que aparecen en >20% del corpus...")
    threshold_20_percent = len(corpus) * 0.20
    threshold_25_percent = len(corpus) * 0.25
    
    frequent_entities = []
    for entity, docs in entity_to_docs.items():
        count = len(docs)
        percentage = (count / len(corpus)) * 100
        if count >= threshold_20_percent:
            frequent_entities.append((entity, count, percentage))
    
    frequent_entities.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n   Entidades que aparecen en >=20% del corpus ({threshold_20_percent:.0f} documentos):")
    for entity, count, percentage in frequent_entities[:15]:
        print(f"      - \"{entity[:60]}\": {count:,} documentos ({percentage:.1f}%)")
    
    # 3. Analizar todas las combinaciones de 3 entidades frecuentes
    print(f"\n3. Analizando combinaciones de 3 entidades que aparecen en >=25% del corpus...")
    print(f"   (Buscando triples que aparezcan en >={threshold_25_percent:.0f} documentos)")
    
    # Tomar las top 15 entidades más frecuentes
    top_entities = [entity for entity, _, _ in frequent_entities[:15]]
    
    print(f"\n   Analizando combinaciones de las top {len(top_entities)} entidades...")
    
    triple_counts = Counter()
    for doc_id, entities in doc_entities.items():
        # Encontrar qué entidades top aparecen en este documento
        doc_top_entities = [e for e in entities if e in top_entities]
        if len(doc_top_entities) >= 3:
            # Generar todas las combinaciones de 3
            for triple in combinations(sorted(doc_top_entities), 3):
                triple_counts[triple] += 1
    
    # Filtrar triples que aparecen en >=25% del corpus
    significant_triples = [
        (triple, count) for triple, count in triple_counts.items()
        if count >= threshold_25_percent
    ]
    
    if significant_triples:
        print(f"\n   [OK] ENCONTRADOS {len(significant_triples)} triples que aparecen en >=25% del corpus:")
        significant_triples.sort(key=lambda x: x[1], reverse=True)
        for i, (triple, count) in enumerate(significant_triples, 1):
            percentage = (count / len(corpus)) * 100
            print(f"\n   {i}. {count:,} documentos ({percentage:.1f}% del corpus):")
            for entity in triple:
                entity_count = len(entity_to_docs[entity])
                entity_pct = (entity_count / len(corpus)) * 100
                print(f"      - \"{entity[:60]}\" (aparece en {entity_count:,} docs = {entity_pct:.1f}%)")
    else:
        print(f"\n   [NO] NO se encontraron triples que aparezcan en >=25% del corpus")
        print(f"\n   Mostrando los triples más frecuentes (aunque sean <25%):")
        top_triples = triple_counts.most_common(10)
        for i, (triple, count) in enumerate(top_triples, 1):
            percentage = (count / len(corpus)) * 100
            print(f"\n   {i}. {count:,} documentos ({percentage:.1f}% del corpus):")
            for entity in triple:
                entity_count = len(entity_to_docs[entity])
                entity_pct = (entity_count / len(corpus)) * 100
                print(f"      - \"{entity[:60]}\" (aparece en {entity_count:,} docs = {entity_pct:.1f}%)")
    
    # 4. Análisis alternativo: ¿qué porcentaje de documentos tienen al menos 3 de las top entidades?
    print(f"\n4. Análisis alternativo: ¿Cuántos documentos tienen al menos 3 de las top entidades?")
    
    docs_with_3_top = 0
    docs_with_4_top = 0
    docs_with_5_top = 0
    
    for doc_id, entities in doc_entities.items():
        doc_top_count = len([e for e in entities if e in top_entities])
        if doc_top_count >= 3:
            docs_with_3_top += 1
        if doc_top_count >= 4:
            docs_with_4_top += 1
        if doc_top_count >= 5:
            docs_with_5_top += 1
    
    print(f"\n   Documentos con >=3 entidades top: {docs_with_3_top:,} ({(docs_with_3_top/len(corpus)*100):.1f}%)")
    print(f"   Documentos con >=4 entidades top: {docs_with_4_top:,} ({(docs_with_4_top/len(corpus)*100):.1f}%)")
    print(f"   Documentos con >=5 entidades top: {docs_with_5_top:,} ({(docs_with_5_top/len(corpus)*100):.1f}%)")
    
    # 5. Análisis específico: ¿hay un conjunto específico de 3 entidades que aparezca en muchos documentos?
    print(f"\n5. Análisis específico: Buscando el conjunto de 3 entidades más común...")
    
    if triple_counts:
        most_common_triple, most_common_count = triple_counts.most_common(1)[0]
        most_common_pct = (most_common_count / len(corpus)) * 100
        
        print(f"\n   Triple más común:")
        print(f"      Aparece en: {most_common_count:,} documentos ({most_common_pct:.1f}% del corpus)")
        print(f"      Entidades:")
        for entity in most_common_triple:
            entity_count = len(entity_to_docs[entity])
            entity_pct = (entity_count / len(corpus)) * 100
            print(f"         - \"{entity[:60]}\"")
            print(f"           (aparece individualmente en {entity_count:,} docs = {entity_pct:.1f}%)")
        
        # Verificar si este triple aparece en el 25% del corpus
        if most_common_pct >= 25.0:
            print(f"\n   [WARNING] PROBLEMA CONFIRMADO: Este triple aparece en >=25% del corpus")
        else:
            print(f"\n   [INFO] Este triple aparece en {most_common_pct:.1f}% del corpus (menos del 25%)")
    
    # Guardar resultados
    results = {
        'corpus_size': len(corpus),
        'threshold_25_percent': threshold_25_percent,
        'frequent_entities': [
            {
                'entity': entity,
                'document_count': count,
                'percentage': percentage
            }
            for entity, count, percentage in frequent_entities
        ],
        'significant_triples_25_percent': [
            {
                'entities': list(triple),
                'document_count': count,
                'percentage': (count / len(corpus)) * 100
            }
            for triple, count in significant_triples
        ] if significant_triples else [],
        'top_triples': [
            {
                'entities': list(triple),
                'document_count': count,
                'percentage': (count / len(corpus)) * 100
            }
            for triple, count in triple_counts.most_common(10)
        ],
        'docs_with_multiple_top_entities': {
            'docs_with_3_top': docs_with_3_top,
            'docs_with_3_top_percentage': (docs_with_3_top / len(corpus)) * 100,
            'docs_with_4_top': docs_with_4_top,
            'docs_with_4_top_percentage': (docs_with_4_top / len(corpus)) * 100,
            'docs_with_5_top': docs_with_5_top,
            'docs_with_5_top_percentage': (docs_with_5_top / len(corpus)) * 100,
        }
    }
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analiza si el 25% del corpus comparte las mismas 3 etiquetas")
    parser.add_argument(
        "--corpus_path",
        type=str,
        default="../../corpus_repo/corpus/documents",
        help="Ruta al corpus completo"
    )
    parser.add_argument(
        "--annotations_path",
        type=str,
        default="../../corpus_repo/corpus/entidades",
        help="Ruta al directorio de anotaciones"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="phi_25_percent_analysis.json",
        help="Archivo de salida"
    )
    
    args = parser.parse_args()
    
    print("Cargando corpus y anotaciones...")
    corpus = load_corpus_with_annotations(args.corpus_path, args.annotations_path)
    
    results = analyze_25_percent_phi(corpus)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Análisis guardado en: {args.output}")


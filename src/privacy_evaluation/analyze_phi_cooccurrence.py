#!/usr/bin/env python3
"""
Análisis de co-ocurrencia de entidades PHI: cuántos documentos comparten las mismas entidades.
Enfocado en el problema de que el 25% de los documentos comparten las mismas 3 etiquetas.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import Counter, defaultdict
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
                    # Intentar mapear por doc_id
                    if isinstance(ann_data, dict):
                        # Buscar doc_id en el archivo de anotación
                        # Asumimos que el nombre del archivo corresponde al doc_id
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


def analyze_phi_cooccurrence(corpus: Dict[str, Dict]) -> Dict:
    """Analiza la co-ocurrencia de entidades PHI"""
    
    print("=" * 80)
    print("ANÁLISIS DE CO-OCURRENCIA DE ENTIDADES PHI")
    print("=" * 80)
    
    # 1. Extraer todas las entidades PHI por documento
    doc_entities = {}
    entity_to_docs = defaultdict(set)
    
    print("\n1. Extrayendo entidades PHI de cada documento...")
    for doc_id, doc_data in corpus.items():
        annotations = doc_data.get('annotations', {})
        entities = extract_phi_entities_from_annotations(annotations)
        
        # Crear conjunto de entidades únicas por tipo
        doc_entity_set = {}
        for phi_type, values in entities.items():
            unique_values = list(set(values))
            doc_entity_set[phi_type] = unique_values
            for value in unique_values:
                entity_to_docs[value].add(doc_id)
        
        doc_entities[doc_id] = doc_entity_set
    
    print(f"   Documentos procesados: {len(doc_entities)}")
    print(f"   Entidades PHI únicas totales: {len(entity_to_docs)}")
    
    # 2. Encontrar entidades más repetidas
    print("\n2. Analizando entidades más repetidas...")
    entity_counts = {entity: len(docs) for entity, docs in entity_to_docs.items()}
    top_entities = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    
    print("\n   Top 20 entidades más repetidas:")
    for i, (entity, count) in enumerate(top_entities, 1):
        percentage = (count / len(corpus)) * 100
        print(f"   {i:2d}. \"{entity[:50]}\": {count:,} documentos ({percentage:.1f}% del corpus)")
    
    # 3. Analizar co-ocurrencia de las top entidades
    print("\n3. Analizando co-ocurrencia de las top entidades...")
    
    # Tomar las top 10 entidades más repetidas
    top_10_entities = [entity for entity, _ in top_entities[:10]]
    
    cooccurrence_matrix = {}
    for entity1 in top_10_entities:
        cooccurrence_matrix[entity1] = {}
        docs1 = entity_to_docs[entity1]
        for entity2 in top_10_entities:
            if entity1 != entity2:
                docs2 = entity_to_docs[entity2]
                cooccurrence = len(docs1.intersection(docs2))
                cooccurrence_matrix[entity1][entity2] = {
                    'count': cooccurrence,
                    'percentage': (cooccurrence / len(corpus)) * 100
                }
    
    # 4. Encontrar triples de entidades que aparecen juntas
    print("\n4. Analizando triples de entidades que aparecen juntas...")
    
    # Para cada documento, encontrar qué entidades top aparecen juntas
    doc_top_entities = {}
    for doc_id, entities in doc_entities.items():
        doc_top_entities[doc_id] = []
        for entity_type, values in entities.items():
            for value in values:
                if value in top_10_entities:
                    doc_top_entities[doc_id].append(value)
    
    # Contar triples más comunes
    triple_counts = Counter()
    for doc_id, entities in doc_top_entities.items():
        if len(entities) >= 3:
            # Generar todas las combinaciones de 3
            from itertools import combinations
            for triple in combinations(sorted(entities), 3):
                triple_counts[triple] += 1
    
    print("\n   Top 10 triples de entidades que aparecen juntas:")
    top_triples = triple_counts.most_common(10)
    for i, (triple, count) in enumerate(top_triples, 1):
        percentage = (count / len(corpus)) * 100
        print(f"   {i:2d}. {count:,} documentos ({percentage:.1f}%):")
        for entity in triple:
            print(f"        - \"{entity[:60]}\"")
    
    # 5. Análisis específico: documentos que comparten las mismas 3 entidades top
    print("\n5. Análisis específico: documentos con las mismas 3 entidades top...")
    
    # Encontrar el triple más común
    if top_triples:
        most_common_triple = top_triples[0][0]
        count_most_common = top_triples[0][1]
        percentage_most_common = (count_most_common / len(corpus)) * 100
        
        print(f"\n   Triple más común aparece en {count_most_common:,} documentos ({percentage_most_common:.1f}% del corpus):")
        for entity in most_common_triple:
            print(f"      - \"{entity[:60]}\"")
        
        # Encontrar documentos que tienen exactamente estas 3 entidades
        docs_with_triple = []
        for doc_id, entities in doc_top_entities.items():
            if set(most_common_triple).issubset(set(entities)):
                docs_with_triple.append(doc_id)
        
        print(f"\n   Documentos que contienen estas 3 entidades: {len(docs_with_triple)}")
    
    # 6. Análisis de diversidad: cuántas entidades únicas por tipo
    print("\n6. Análisis de diversidad de entidades...")
    
    entity_diversity = {}
    for phi_type in ['person', 'id', 'date', 'location', 'phone', 'email', 'age']:
        unique_entities = set()
        for doc_id, entities in doc_entities.items():
            unique_entities.update(entities.get(phi_type, []))
        entity_diversity[phi_type] = {
            'unique_count': len(unique_entities),
            'total_occurrences': sum(len(entities.get(phi_type, [])) for entities in doc_entities.values())
        }
        print(f"   {phi_type:10s}: {len(unique_entities):,} valores únicos")
    
    # Guardar resultados
    results = {
        'corpus_size': len(corpus),
        'total_unique_entities': len(entity_to_docs),
        'top_entities': [
            {
                'entity': entity,
                'document_count': count,
                'percentage': (count / len(corpus)) * 100
            }
            for entity, count in top_entities
        ],
        'top_triples': [
            {
                'entities': list(triple),
                'document_count': count,
                'percentage': (count / len(corpus)) * 100
            }
            for triple, count in top_triples[:10]
        ],
        'entity_diversity': entity_diversity,
        'cooccurrence_matrix': {
            entity1: {
                entity2: data
                for entity2, data in cooccurrence_matrix[entity1].items()
                if data['percentage'] > 20  # Solo mostrar co-ocurrencias >20%
            }
            for entity1 in top_10_entities
        }
    }
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analiza co-ocurrencia de entidades PHI")
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
        default="phi_cooccurrence_analysis.json",
        help="Archivo de salida"
    )
    
    args = parser.parse_args()
    
    print("Cargando corpus y anotaciones...")
    corpus = load_corpus_with_annotations(args.corpus_path, args.annotations_path)
    
    results = analyze_phi_cooccurrence(corpus)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Análisis guardado en: {args.output}")


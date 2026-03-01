#!/usr/bin/env python3
"""
Análisis detallado de los pares más similares en la evaluación de similitud semántica.
Identifica qué hace que los textos sean tan similares (estructura, contenido, PHI).
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter
from difflib import SequenceMatcher


def load_corpus(corpus_path: str) -> Dict[str, str]:
    """Carga el corpus completo y devuelve un diccionario doc_id -> text"""
    corpus = {}
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    doc_id = item.get('id', '')
                    text = item.get('text', item.get('content', ''))
                    if doc_id and text:
                        corpus[doc_id] = text
    
    return corpus


def extract_phi_patterns(text: str) -> Dict[str, List[str]]:
    """Extrae patrones comunes de PHI del texto"""
    patterns = {
        'dates': re.findall(r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', text),
        'ids': re.findall(r'[A-Z]{1,2}-?\d{4}-?\d{4,6}', text) + re.findall(r'\d{8,12}[A-Z]?', text),
        'phones': re.findall(r'\+?\d{2,3}[\s-]?\d{2,3}[\s-]?\d{2,3}[\s-]?\d{2,3}', text),
        'emails': re.findall(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text),
        'locations': re.findall(r'(?:Centro de Salud|Hospital|Clínica)\s+[\w\sÁÉÍÓÚáéíóú]+', text),
    }
    return patterns


def compare_texts(text1: str, text2: str) -> Dict:
    """Compara dos textos y identifica similitudes y diferencias"""
    # Similitud de secuencia
    seq_similarity = SequenceMatcher(None, text1, text2).ratio()
    
    # Palabras comunes
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    common_words = words1.intersection(words2)
    unique_words1 = words1 - words2
    unique_words2 = words2 - words1
    
    # Patrones PHI
    phi1 = extract_phi_patterns(text1)
    phi2 = extract_phi_patterns(text2)
    
    # Estructura (oraciones)
    sentences1 = re.split(r'[.!?]\s+', text1)
    sentences2 = re.split(r'[.!?]\s+', text2)
    
    # Frases comunes
    common_phrases = []
    for sent1 in sentences1[:5]:  # Primeras 5 oraciones
        for sent2 in sentences2[:5]:
            if len(sent1) > 20 and len(sent2) > 20:
                similarity = SequenceMatcher(None, sent1.lower(), sent2.lower()).ratio()
                if similarity > 0.8:
                    common_phrases.append((sent1[:100], sent2[:100], similarity))
    
    return {
        'sequence_similarity': seq_similarity,
        'common_words_count': len(common_words),
        'unique_words_count_1': len(unique_words1),
        'unique_words_count_2': len(unique_words2),
        'phi_patterns_1': phi1,
        'phi_patterns_2': phi2,
        'common_phrases': common_phrases[:3],  # Top 3
        'text1_length': len(text1),
        'text2_length': len(text2),
    }


def analyze_similar_pairs(
    similarity_results_path: str,
    corpus_path: str,
    top_n: int = 20,
    output_path: str = "similar_pairs_analysis.json"
):
    """Analiza los top N pares más similares"""
    
    print("=" * 80)
    print("ANÁLISIS DE PARES MÁS SIMILARES")
    print("=" * 80)
    
    # Cargar resultados de similitud
    print(f"\n1. Cargando resultados de similitud: {similarity_results_path}")
    with open(similarity_results_path, 'r', encoding='utf-8') as f:
        similarity_data = json.load(f)
    
    pairs = similarity_data.get('semantic_similarities', [])
    print(f"   Total pares encontrados: {len(pairs)}")
    
    # Cargar corpus completo
    print(f"\n2. Cargando corpus completo: {corpus_path}")
    corpus = load_corpus(corpus_path)
    print(f"   Documentos cargados: {len(corpus)}")
    
    # Analizar top N pares
    print(f"\n3. Analizando top {top_n} pares más similares...")
    top_pairs = pairs[:top_n]
    
    analysis_results = []
    
    for i, pair in enumerate(top_pairs, 1):
        doc1_id = pair['doc1']['doc_id']
        doc2_id = pair['doc2']['doc_id']
        similarity = pair['similarity']
        
        print(f"\n   [{i}/{top_n}] Analizando par (similitud: {similarity:.4f})...")
        print(f"      Doc1: {doc1_id}")
        print(f"      Doc2: {doc2_id}")
        
        # Obtener textos completos
        text1 = corpus.get(doc1_id, '')
        text2 = corpus.get(doc2_id, '')
        
        if not text1 or not text2:
            print(f"      [WARNING] No se encontraron textos completos para uno o ambos documentos")
            continue
        
        # Comparar textos
        comparison = compare_texts(text1, text2)
        
        # Identificar diferencias clave
        differences = []
        if comparison['unique_words_count_1'] > 0 or comparison['unique_words_count_2'] > 0:
            # Encontrar palabras clave diferentes
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            unique1 = list(words1 - words2)[:5]
            unique2 = list(words2 - words1)[:5]
            differences.append({
                'type': 'vocabulary',
                'unique_in_doc1': unique1,
                'unique_in_doc2': unique2
            })
        
        # Verificar PHI compartido
        phi_shared = {}
        for phi_type in ['dates', 'ids', 'phones', 'emails', 'locations']:
            phi1_set = set(comparison['phi_patterns_1'].get(phi_type, []))
            phi2_set = set(comparison['phi_patterns_2'].get(phi_type, []))
            shared = list(phi1_set.intersection(phi2_set))
            if shared:
                phi_shared[phi_type] = shared
        
        analysis = {
            'pair_number': i,
            'similarity_score': similarity,
            'doc1': {
                'id': doc1_id,
                'filename': pair['doc1']['filename'],
                'text_length': len(text1),
                'text_preview': text1[:200] + '...' if len(text1) > 200 else text1
            },
            'doc2': {
                'id': doc2_id,
                'filename': pair['doc2']['filename'],
                'text_length': len(text2),
                'text_preview': text2[:200] + '...' if len(text2) > 200 else text2
            },
            'comparison': {
                'sequence_similarity': comparison['sequence_similarity'],
                'common_words_count': comparison['common_words_count'],
                'unique_words_count': {
                    'doc1': comparison['unique_words_count_1'],
                    'doc2': comparison['unique_words_count_2']
                },
                'common_phrases': comparison['common_phrases']
            },
            'phi_analysis': {
                'shared_phi': phi_shared,
                'doc1_phi': {k: len(v) for k, v in comparison['phi_patterns_1'].items()},
                'doc2_phi': {k: len(v) for k, v in comparison['phi_patterns_2'].items()}
            },
            'differences': differences
        }
        
        analysis_results.append(analysis)
        
        # Imprimir resumen
        print(f"      Similitud de secuencia: {comparison['sequence_similarity']:.4f}")
        print(f"      Palabras comunes: {comparison['common_words_count']}")
        print(f"      PHI compartido: {len(phi_shared)} tipos")
        if phi_shared:
            for phi_type, values in phi_shared.items():
                print(f"        - {phi_type}: {len(values)} valores compartidos")
    
    # Análisis agregado
    print("\n" + "=" * 80)
    print("ANÁLISIS AGREGADO")
    print("=" * 80)
    
    # Patrones comunes
    all_common_phrases = []
    all_shared_phi = Counter()
    
    for analysis in analysis_results:
        all_common_phrases.extend(analysis['comparison']['common_phrases'])
        for phi_type in analysis['phi_analysis']['shared_phi'].keys():
            all_shared_phi[phi_type] += 1
    
    print(f"\nPatrones PHI compartidos más comunes:")
    for phi_type, count in all_shared_phi.most_common():
        print(f"  - {phi_type}: aparece en {count} pares")
    
    # Guardar resultados
    output = {
        'summary': {
            'total_pairs_analyzed': len(analysis_results),
            'average_similarity': sum(p['similarity_score'] for p in analysis_results) / len(analysis_results),
            'phi_types_shared': dict(all_shared_phi)
        },
        'detailed_analysis': analysis_results
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Análisis guardado en: {output_path}")
    
    return output


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analiza los pares más similares")
    parser.add_argument(
        "--similarity_results",
        type=str,
        default="privacy_evaluation_results_semantic/memorization_detection.json",
        help="Ruta al archivo de resultados de similitud semántica"
    )
    parser.add_argument(
        "--corpus_path",
        type=str,
        default="../../corpus_repo/corpus/documents",
        help="Ruta al corpus completo"
    )
    parser.add_argument(
        "--top_n",
        type=int,
        default=20,
        help="Número de pares a analizar"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="similar_pairs_analysis.json",
        help="Archivo de salida"
    )
    
    args = parser.parse_args()
    
    analyze_similar_pairs(
        args.similarity_results,
        args.corpus_path,
        args.top_n,
        args.output
    )



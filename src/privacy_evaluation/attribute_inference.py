"""
Attribute Inference Attack Evaluation
Tests whether an attacker can infer sensitive attributes (e.g., PHI types, medical conditions)
from the generated texts.
"""

import json
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report
from typing import List, Dict, Tuple, Set
import argparse
from pathlib import Path
import re
from meddocan_label_mapping import map_meddocan_to_phi


def load_corpus_with_annotations(corpus_path: str, annotations_path: str = None) -> Tuple[List[str], List[Dict]]:
    """
    Load corpus with PHI annotations.
    
    Args:
        corpus_path: Path to corpus (directory or .json file)
        annotations_path: Path to directory with annotation JSON files (optional)
    
    Returns:
        texts: List of text strings
        annotations: List of annotation dictionaries
    """
    texts = []
    annotations = []
    
    if os.path.isdir(corpus_path):
        # Load from directory structure
        # Assume structure: corpus/documents/*.txt and corpus/entidades/*.json
        docs_dir = Path(corpus_path) / "documents"
        ents_dir = Path(annotations_path) if annotations_path else Path(corpus_path) / "entidades"
        
        if not docs_dir.exists():
            docs_dir = Path(corpus_path)
        
        for txt_file in docs_dir.glob("*.txt"):
            with open(txt_file, 'r', encoding='utf-8') as f:
                texts.append(f.read().strip())
            
            # Try to load corresponding annotation
            json_file = ents_dir / f"{txt_file.stem}.json" if ents_dir.exists() else None
            if json_file and json_file.exists():
                with open(json_file, 'r', encoding='utf-8') as f:
                    annotations.append(json.load(f))
            else:
                annotations.append({})
    
    elif corpus_path.endswith('.json'):
        # Load from JSON file
        with open(corpus_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        text = item.get('text', item.get('content', ''))
                        texts.append(text)
                        
                        # Try to get annotations from entidades directory
                        doc_id = item.get('id', '')
                        if doc_id and annotations_path:
                            # Look for corresponding annotation file
                            if os.path.isdir(annotations_path):
                                ann_file = Path(annotations_path) / f"{doc_id}.json"
                                if ann_file.exists():
                                    with open(ann_file, 'r', encoding='utf-8') as af:
                                        ann_data = json.load(af)
                                        annotations.append(ann_data)
                                    continue
                        
                        # Fallback: use entities/annotations from item
                        ann = item.get('entities', item.get('annotations', {}))
                        if not ann and 'labels' in item:
                            # Convert numeric labels to empty dict (will extract from text)
                            ann = {}
                        annotations.append(ann)
                    else:
                        texts.append(str(item))
                        annotations.append({})
    
    return texts, annotations


def extract_phi_types(annotations: List[Dict]) -> Set[str]:
    """Extract all PHI types present in annotations."""
    phi_types = set()
    
    for ann in annotations:
        if isinstance(ann, dict):
            if 'entities' in ann:
                for entity in ann['entities']:
                    if isinstance(entity, dict):
                        phi_types.add(entity.get('label', entity.get('type', '')))
            elif 'labels' in ann:
                # IOB format
                for label in ann['labels']:
                    if label != 'O' and '-' in label:
                        phi_types.add(label.split('-')[1])
    
    return phi_types


def extract_attributes_from_text(text: str, annotations: Dict) -> Dict[str, bool]:
    """
    Extract binary attributes from text and annotations.
    
    Attributes:
    - Contains PERSON name
    - Contains DATE
    - Contains LOCATION
    - Contains ID
    - Contains AGE
    - Contains PHONE/EMAIL
    - Contains specific medical conditions (if detectable)
    """
    attributes = {
        'has_person': False,
        'has_date': False,
        'has_location': False,
        'has_id': False,
        'has_age': False,
        'has_contact': False,
        'has_medical_condition': False
    }
    
    # Check annotations
    if isinstance(annotations, dict):
        # Handle format with "data" array (from entidades JSON files)
        if 'data' in annotations and isinstance(annotations['data'], list):
            for entity_item in annotations['data']:
                if isinstance(entity_item, dict):
                    entity_type = entity_item.get('entity', '').strip()
                    # Map MEDDOCAN label to generic PHI category
                    phi_category = map_meddocan_to_phi(entity_type)
                    
                    if phi_category == 'person':
                        attributes['has_person'] = True
                    elif phi_category == 'date':
                        attributes['has_date'] = True
                    elif phi_category == 'location':
                        attributes['has_location'] = True
                    elif phi_category == 'id':
                        attributes['has_id'] = True
                    elif phi_category == 'age':
                        attributes['has_age'] = True
                    elif phi_category in ['phone', 'email']:
                        attributes['has_contact'] = True
                    
                    # Fallback: also check for common patterns in label name
                    entity_type_upper = entity_type.upper()
                    if 'PERSON' in entity_type_upper or 'NOMBRE' in entity_type_upper:
                        attributes['has_person'] = True
                    elif 'DATE' in entity_type_upper or 'FECHA' in entity_type_upper:
                        attributes['has_date'] = True
                    elif 'LOCATION' in entity_type_upper or 'LOC' in entity_type_upper or 'PAIS' in entity_type_upper or 'CIUDAD' in entity_type_upper or 'TERRITORIO' in entity_type_upper:
                        attributes['has_location'] = True
                    elif 'ID' in entity_type_upper:
                        attributes['has_id'] = True
                    elif 'AGE' in entity_type_upper or 'EDAD' in entity_type_upper:
                        attributes['has_age'] = True
                    elif 'PHONE' in entity_type_upper or 'TELEFONO' in entity_type_upper or 'FAX' in entity_type_upper:
                        attributes['has_contact'] = True
                    elif 'EMAIL' in entity_type_upper or 'CORREO' in entity_type_upper:
                        attributes['has_contact'] = True
        
        # Handle format with "entities" array
        entities = annotations.get('entities', [])
        labels = annotations.get('labels', [])
        
        # Check entity types
        for entity in entities:
            if isinstance(entity, dict):
                label = entity.get('label', entity.get('type', '')).strip()
                # Map MEDDOCAN label to generic PHI category
                phi_category = map_meddocan_to_phi(label)
                
                if phi_category == 'person':
                    attributes['has_person'] = True
                elif phi_category == 'date':
                    attributes['has_date'] = True
                elif phi_category == 'location':
                    attributes['has_location'] = True
                elif phi_category == 'id':
                    attributes['has_id'] = True
                elif phi_category == 'age':
                    attributes['has_age'] = True
                elif phi_category in ['phone', 'email']:
                    attributes['has_contact'] = True
                
                # Fallback: also check for common patterns in label name
                label_upper = label.upper()
                if 'PERSON' in label_upper or 'NOMBRE' in label_upper:
                    attributes['has_person'] = True
                elif 'DATE' in label_upper or 'FECHA' in label_upper:
                    attributes['has_date'] = True
                elif 'LOCATION' in label_upper or 'LOC' in label_upper or 'PAIS' in label_upper or 'CIUDAD' in label_upper or 'TERRITORIO' in label_upper:
                    attributes['has_location'] = True
                elif 'ID' in label_upper:
                    attributes['has_id'] = True
                elif 'AGE' in label_upper or 'EDAD' in label_upper:
                    attributes['has_age'] = True
                elif 'PHONE' in label_upper or 'TELEFONO' in label_upper or 'FAX' in label_upper:
                    attributes['has_contact'] = True
                elif 'EMAIL' in label_upper or 'CORREO' in label_upper:
                    attributes['has_contact'] = True
        
        # Check IOB labels
        for label in labels:
            if label != 'O' and '-' in label:
                label_type = label.split('-')[1].upper()
                if 'PERSON' in label_type:
                    attributes['has_person'] = True
                elif 'DATE' in label_type:
                    attributes['has_date'] = True
                elif 'LOCATION' in label_type or 'LOC' in label_type:
                    attributes['has_location'] = True
                elif 'ID' in label_type:
                    attributes['has_id'] = True
                elif 'AGE' in label_type:
                    attributes['has_age'] = True
                elif 'PHONE' in label_type or 'EMAIL' in label_type:
                    attributes['has_contact'] = True
    
    # Check text patterns for medical conditions
    medical_keywords = [
        'diabetes', 'hipertensión', 'cáncer', 'asma', 'epilepsia',
        'diabetes', 'hypertension', 'cancer', 'asthma', 'epilepsy'
    ]
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in medical_keywords):
        attributes['has_medical_condition'] = True
    
    return attributes


def train_attribute_inference_attack(
    X: np.ndarray,
    y: np.ndarray,
    attribute_name: str
) -> Tuple[LogisticRegression, Dict[str, float]]:
    """Train attribute inference attack for a specific attribute."""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train attack model
    attack_model = LogisticRegression(max_iter=1000, random_state=42)
    attack_model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = attack_model.predict(X_test)
    y_pred_proba = attack_model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_pred_proba) if len(np.unique(y_test)) > 1 else 0.0
    
    metrics = {
        'attribute': attribute_name,
        'accuracy': accuracy,
        'auc_roc': auc_score,
        'positive_rate': np.mean(y),
        'baseline_accuracy': max(np.mean(y), 1 - np.mean(y))
    }
    
    return attack_model, metrics


def evaluate_attribute_inference(
    corpus_path: str,
    annotations_path: str = None,
    output_path: str = "attribute_inference_results.json"
) -> Dict:
    """
    Complete attribute inference evaluation.
    
    Args:
        corpus_path: Path to corpus with annotations
        annotations_path: Path to directory with annotation JSON files (optional)
        output_path: Path to save results
    """
    print("Loading corpus with annotations...")
    texts, annotations = load_corpus_with_annotations(corpus_path, annotations_path)
    print(f"Loaded {len(texts)} texts with annotations")
    
    # Extract attributes for each text
    print("Extracting attributes...")
    all_attributes = []
    for text, ann in zip(texts, annotations):
        attrs = extract_attributes_from_text(text, ann)
        all_attributes.append(attrs)
    
    # Get all attribute names
    attribute_names = list(all_attributes[0].keys())
    
    # Vectorize texts
    print("Vectorizing texts...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 3),
        min_df=2,
        max_df=0.95
    )
    X = vectorizer.fit_transform(texts).toarray()
    
    # Evaluate each attribute
    print("Evaluating attribute inference attacks...")
    results = {
        'corpus_size': len(texts),
        'attributes_evaluated': attribute_names,
        'attribute_results': {}
    }
    
    for attr_name in attribute_names:
        y = np.array([attrs[attr_name] for attrs in all_attributes])
        
        # Skip if attribute is constant (all True or all False)
        if len(np.unique(y)) < 2:
            results['attribute_results'][attr_name] = {
                'skipped': True,
                'reason': 'Constant attribute (all same value)'
            }
            continue
        
        print(f"  Evaluating {attr_name}...")
        attack_model, metrics = train_attribute_inference_attack(X, y, attr_name)
        
        # Risk assessment
        risk_level = (
            'low' if metrics['auc_roc'] < 0.6 else
            'medium' if metrics['auc_roc'] < 0.7 else
            'high' if metrics['auc_roc'] < 0.8 else
            'critical'
        )
        
        results['attribute_results'][attr_name] = {
            **metrics,
            'risk_level': risk_level
        }
    
    # Overall risk assessment
    risk_scores = [
        r.get('auc_roc', 0) for r in results['attribute_results'].values()
        if isinstance(r, dict) and 'auc_roc' in r
    ]
    
    results['overall_risk'] = {
        'max_auc_roc': max(risk_scores) if risk_scores else 0.0,
        'mean_auc_roc': np.mean(risk_scores) if risk_scores else 0.0,
        'high_risk_attributes': [
            attr for attr, res in results['attribute_results'].items()
            if isinstance(res, dict) and res.get('auc_roc', 0) >= 0.7
        ]
    }
    
    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nAttribute Inference Results:")
    print(f"  Attributes evaluated: {len(attribute_names)}")
    print(f"  Max AUC-ROC: {results['overall_risk']['max_auc_roc']:.4f}")
    print(f"  Mean AUC-ROC: {results['overall_risk']['mean_auc_roc']:.4f}")
    print(f"  High-risk attributes: {results['overall_risk']['high_risk_attributes']}")
    print(f"\nResults saved to {output_path}")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Attribute Inference Attack Evaluation")
    parser.add_argument(
        "--corpus_path",
        type=str,
        required=True,
        help="Path to corpus (directory or .json file with annotations)"
    )
    parser.add_argument(
        "--annotations_path",
        type=str,
        default=None,
        help="Path to directory with annotation JSON files (optional)"
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="attribute_inference_results.json",
        help="Path to save results"
    )
    
    args = parser.parse_args()
    
    evaluate_attribute_inference(
        args.corpus_path,
        args.annotations_path,
        args.output_path
    )


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word Embedding Association Test (WEAT) para análisis de sesgo de género en corpus médico.

Implementa el WEAT de Caliskan et al. (2017) para detectar sesgos de género
en profesiones médicas dentro del corpus sintético.

Referencia:
  Caliskan, A., Bryson, J. J., & Narayanan, A. (2017).
  Semantics derived automatically from language corpora contain human-like biases.
  Science, 356(6334), 183-186.

Fuente adaptada de: https://github.com/ramsestein/generate_corpus_anonimizacion
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

# Semilla fija para reproducibilidad (permutaciones WEAT y cualquier aleatoriedad futura).
WEAT_RANDOM_SEED = 42


def _progress(iterable, desc: str = ""):
    return tqdm(iterable, desc=desc) if TQDM_AVAILABLE else iterable


# Profesiones médicas (target WEAT)
MEDICAL_PROFESSIONS = [
    "médico", "medico", "doctor", "doctora", "enfermero", "enfermera",
    "cirujano", "cirujana", "pediatra", "psiquiatra", "cardiólogo", "cardióloga",
    "oncólogo", "oncóloga", "neurólogo", "neuróloga", "ginecólogo", "ginecóloga",
    "traumatólogo", "traumatóloga", "anestesista", "radiólogo", "radióloga",
    "dermatólogo", "dermatóloga", "oftalmólogo", "oftalmóloga",
    "otorrinolaringólogo", "otorrinolaringóloga", "urólogo", "uróloga",
    "endocrinólogo", "endocrinóloga", "internista", "intensivista",
    "residente", "especialista", "médica", "medica",
]

# Atributos masculinos
MALE_TERMS = [
    "hombre", "él", "masculino", "varón", "varon", "padre", "hijo", "hermano",
    "esposo", "marido", "abuelo", "tío", "tio", "sobrino", "primo", "yerno",
    "nieto", "cuñado", "cunado", "padrino", "suegro",
]

# Atributos femeninos
FEMALE_TERMS = [
    "mujer", "ella", "femenino", "madre", "hija", "hermana",
    "esposa", "abuela", "tía", "tia", "sobrina", "prima", "nuera",
    "nieta", "cuñada", "cunada", "madrina", "suegra",
]


def load_documents(corpus_dir: Path, max_docs: Optional[int] = None) -> List[str]:
    """Carga documentos .txt del corpus. Orden determinista: sorted por ruta."""
    txt_files = sorted(corpus_dir.glob("*.txt"), key=lambda p: p.name)
    if max_docs is not None:
        txt_files = txt_files[:max_docs]
    documents = []
    for fp in _progress(txt_files, desc="Cargando"):
        try:
            text = fp.read_text(encoding="utf-8").strip()
            if text:
                documents.append(text)
        except Exception:
            continue
    return documents


def build_vocabulary(documents: List[str], min_count: int = 5) -> Dict[str, int]:
    """Construye vocabulario (palabras con al menos min_count ocurrencias).
    Tokenización: regex \\b\\w+\\b, lowercased. Orden de claves: orden de aparición en documentos.
    """
    vocab: Counter = Counter()
    for doc in _progress(documents, desc="Vocabulario"):
        tokens = re.findall(r"\b\w+\b", doc.lower())
        vocab.update(tokens)
    # Orden determinista: ordenar por palabra para que mismo corpus dé mismo vocab orden
    filtered = [(w, c) for w, c in vocab.items() if c >= min_count]
    filtered.sort(key=lambda x: x[0])
    return dict(filtered)


def train_cooccurrence_embeddings(
    documents: List[str],
    vocab: Dict[str, int],
    window_size: int = 5,
    dim: int = 100,
) -> Dict[str, np.ndarray]:
    """
    Embeddings por co-ocurrencia + SVD (estilo LSA).
    """
    word_to_idx = {w: i for i, w in enumerate(vocab.keys())}
    n = len(word_to_idx)
    cooc = np.zeros((n, n))

    for doc in _progress(documents, desc="Co-ocurrencia"):
        tokens = re.findall(r"\b\w+\b", doc.lower())
        tokens = [t for t in tokens if t in word_to_idx]
        for i, word in enumerate(tokens):
            start = max(0, i - window_size)
            end = min(len(tokens), i + window_size + 1)
            for j in range(start, end):
                if i != j:
                    cooc[word_to_idx[word], word_to_idx[tokens[j]]] += 1

    U, S, Vt = np.linalg.svd(cooc, full_matrices=False)
    # Fijar signo de cada componente para reproducibilidad (SVD puede devolver ±u)
    for j in range(U.shape[1]):
        col = U[:, j]
        idx = np.argmax(np.abs(col))
        if col[idx] < 0:
            U[:, j] = -U[:, j]
    emb = U[:, :dim] * np.sqrt(S[:dim])
    norms = np.linalg.norm(emb, axis=1, keepdims=True)
    emb = emb / (norms + 1e-10)

    return {w: emb[i] for w, i in word_to_idx.items()}


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    n1 = np.linalg.norm(vec1)
    n2 = np.linalg.norm(vec2)
    if n1 < 1e-10 or n2 < 1e-10:
        return 0.0
    return float(np.dot(vec1, vec2) / (n1 * n2))


def mean_cosine_similarity(
    word: str, word_list: List[str], embeddings: Dict[str, np.ndarray]
) -> float:
    if word not in embeddings:
        return 0.0
    sims = []
    for w in word_list:
        if w in embeddings:
            sims.append(cosine_similarity(embeddings[word], embeddings[w]))
    return float(np.mean(sims)) if sims else 0.0


def weat_effect_size(
    target_words: List[str],
    attribute1: List[str],
    attribute2: List[str],
    embeddings: Dict[str, np.ndarray],
) -> float:
    """
    Efecto WEAT (d de Cohen): media de s(t,A1,A2) / std(s),
    con s(t,A1,A2) = mean_sim(t,A1) - mean_sim(t,A2).
    """
    test_stats = []
    for target in target_words:
        if target in embeddings:
            s = mean_cosine_similarity(target, attribute1, embeddings) - mean_cosine_similarity(
                target, attribute2, embeddings
            )
            test_stats.append(s)
    if not test_stats:
        return 0.0
    mean_s = np.mean(test_stats)
    std_s = np.std(test_stats)
    return float(mean_s / (std_s + 1e-10))


def weat_permutation_test(
    target_words: List[str],
    attribute1: List[str],
    attribute2: List[str],
    embeddings: Dict[str, np.ndarray],
    n_permutations: int = 1000,
) -> Tuple[float, float]:
    """Test de permutación para p-value del WEAT."""
    observed = weat_effect_size(target_words, attribute1, attribute2, embeddings)
    all_attr = list(attribute1) + list(attribute2)
    n1 = len(attribute1)
    perm_effects = []
    rng = np.random.default_rng(WEAT_RANDOM_SEED)
    for _ in range(n_permutations):
        perm = rng.permutation(len(all_attr))
        p1 = [all_attr[i] for i in perm[:n1]]
        p2 = [all_attr[i] for i in perm[n1:]]
        perm_effects.append(
            weat_effect_size(target_words, p1, p2, embeddings)
        )
    perm_effects = np.array(perm_effects)
    p_value = float(np.mean(np.abs(perm_effects) >= np.abs(observed)))
    return observed, p_value


def count_mentions(word_list: List[str], vocab: Dict[str, int]) -> int:
    return sum(vocab.get(w, 0) for w in word_list)


def analyze_profession_gender_cooccurrence(
    documents: List[str],
    window: int = 10,
) -> Dict[str, Any]:
    """Co-ocurrencias entre profesiones médicas y términos de género en ventana."""
    male_cooc = 0
    female_cooc = 0
    prof_set = set(MEDICAL_PROFESSIONS)
    male_set = set(MALE_TERMS)
    female_set = set(FEMALE_TERMS)

    for doc in documents:
        tokens = re.findall(r"\b\w+\b", doc.lower())
        for i, token in enumerate(tokens):
            if token in prof_set:
                start = max(0, i - window)
                end = min(len(tokens), i + window + 1)
                for j in range(start, end):
                    w = tokens[j]
                    if w in male_set:
                        male_cooc += 1
                    if w in female_set:
                        female_cooc += 1
    total = male_cooc + female_cooc
    return {
        "male_cooccurrences": int(male_cooc),
        "female_cooccurrences": int(female_cooc),
        "male_cooc_ratio": float(male_cooc / total) if total else 0.0,
        "female_cooc_ratio": float(female_cooc / total) if total else 0.0,
    }


def run_weat_analysis(
    documents_path: str,
    max_docs: Optional[int] = None,
    window_size: int = 5,
    embedding_dim: int = 100,
    min_word_count: int = 5,
    n_permutations: int = 1000,
) -> Dict[str, Any]:
    """
    Ejecuta el análisis WEAT completo.
    """
    p = Path(documents_path)
    if not p.exists() or not p.is_dir():
        raise FileNotFoundError(f"Directorio de documentos no encontrado: {documents_path}")

    documents = load_documents(p, max_docs=max_docs)
    if not documents:
        return {
            "metric": "weat_gender_analysis",
            "error": "No se cargó ningún documento",
            "documents_path": str(p),
            "max_docs": max_docs,
        }

    vocab = build_vocabulary(documents, min_count=min_word_count)
    embeddings = train_cooccurrence_embeddings(
        documents, vocab, window_size=window_size, dim=embedding_dim
    )

    # WEAT: profesiones vs masculino/femenino
    # effect = mean_sim(profesiones, MALE) - mean_sim(profesiones, FEMALE); positivo = sesgo masculino.
    # Si el signo difiere de otra implementación (ej. ramsestein/generate_corpus_anonimizacion), suele deberse
    # a corpus distinto (ellos 67+1708 menciones vs nuestros 1k+4k) o a orden de atributos en la fórmula.
    effect_size, p_value = weat_permutation_test(
        target_words=MEDICAL_PROFESSIONS,
        attribute1=MALE_TERMS,
        attribute2=FEMALE_TERMS,
        embeddings=embeddings,
        n_permutations=n_permutations,
    )

    if abs(effect_size) < 0.2:
        interpretation = "Sesgo negligible"
    elif abs(effect_size) < 0.5:
        interpretation = "Sesgo pequeño"
    elif abs(effect_size) < 0.8:
        interpretation = "Sesgo moderado"
    else:
        interpretation = "Sesgo grande"

    bias_direction = "masculino" if effect_size > 0 else "femenino"

    male_count = count_mentions(MALE_TERMS, vocab)
    female_count = count_mentions(FEMALE_TERMS, vocab)
    total_gender = male_count + female_count
    male_ratio = male_count / total_gender if total_gender else 0.0
    female_ratio = female_count / total_gender if total_gender else 0.0

    cooc = analyze_profession_gender_cooccurrence(documents, window=10)

    return {
        "metric": "weat_gender_analysis",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_summary": {
            "documents_path": str(p),
            "max_docs": max_docs,
            "documents_loaded": len(documents),
            "vocabulary_size": len(vocab),
            "window_size": window_size,
            "embedding_dim": embedding_dim,
            "min_word_count": min_word_count,
            "n_permutations": n_permutations,
            "permutation_seed": WEAT_RANDOM_SEED,
            "cooccurrence_window_profession": 10,
        },
        "reproducibility": {
            "description": "Mismos valores si se repite con mismo corpus y mismos parámetros.",
            "parameters_affecting_result": [
                "documents_path",
                "max_docs",
                "min_word_count",
                "window_size (co-ocurrencias para embeddings)",
                "embedding_dim",
                "n_permutations",
                "permutation_seed",
                "tokenization: regex \\b\\w+\\b, lowercased",
                "document_order: sorted by file name",
                "vocab_order: sorted by word (after min_count filter)",
                "SVD: sign normalized per column (max-abs element positive)",
            ],
        },
        "weat_analysis": {
            "effect_size": float(effect_size),
            "p_value": float(p_value),
            "interpretation": interpretation,
            "bias_direction": bias_direction,
            "significant": bool(p_value < 0.05),
        },
        "mention_ratio": {
            "male_mentions": int(male_count),
            "female_mentions": int(female_count),
            "male_ratio": float(male_ratio),
            "female_ratio": float(female_ratio),
            "male_female_ratio": float(male_count / female_count) if female_count > 0 else None,
        },
        "profession_cooccurrence": cooc,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="WEAT: análisis de sesgo de género en corpus médico (Caliskan et al. 2017)"
    )
    parser.add_argument(
        "--documents_path",
        required=True,
        help="Directorio con documentos .txt del corpus (ej. corpus_repo/corpus_v1/documents)",
    )
    parser.add_argument(
        "--max_docs",
        type=int,
        default=None,
        help="Máximo de documentos a cargar (por defecto todos). Para pruebas usar ej. 5000.",
    )
    parser.add_argument(
        "--output_path",
        default="bias_evaluation_results/weat_gender_analysis.json",
        help="Ruta del JSON de salida",
    )
    parser.add_argument("--window_size", type=int, default=5)
    parser.add_argument("--embedding_dim", type=int, default=100)
    parser.add_argument("--min_word_count", type=int, default=5)
    parser.add_argument("--n_permutations", type=int, default=1000)
    args = parser.parse_args()

    result = run_weat_analysis(
        documents_path=args.documents_path,
        max_docs=args.max_docs,
        window_size=args.window_size,
        embedding_dim=args.embedding_dim,
        min_word_count=args.min_word_count,
        n_permutations=args.n_permutations,
    )

    out_p = Path(args.output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    if "error" in result:
        print("ERROR:", result["error"])
    else:
        w = result["weat_analysis"]
        m = result["mention_ratio"]
        print("=" * 80)
        print("WEAT - ANÁLISIS DE SESGO DE GÉNERO")
        print("=" * 80)
        print(f"Output: {out_p}")
        print(f"Effect size (d): {w['effect_size']:.4f}")
        print(f"p-value: {w['p_value']:.4f}")
        print(f"Interpretación: {w['interpretation']} (dirección: {w['bias_direction']})")
        print(f"Menciones masculinas: {m['male_mentions']:,} ({m['male_ratio']*100:.1f}%)")
        print(f"Menciones femeninas: {m['female_mentions']:,} ({m['female_ratio']*100:.1f}%)")

"""
Run bias evaluation metrics (1.1–1.6 + WEAT + interseccionalidad, diagnóstico×demografía,
género vs objetivo, edad vs referencia, cobertura, diversidad) on corpus_v1.

Designed to mirror privacy suite style: run multiple metrics and write a consolidated report.
Supports running on the first N documents (sorted by filename) for quick checks.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from age_distribution import evaluate_age_distribution
from age_reference_comparison import evaluate_age_reference_comparison
from coverage_completeness import evaluate_coverage_completeness
from diagnosis_condition_bias import evaluate_diagnosis_bias
from diagnosis_demography_bias import evaluate_diagnosis_demography_bias
from diversity_summary import evaluate_diversity_summary
from gender_target_proportion import evaluate_gender_target_proportion
from geographic_toponymic_bias import evaluate_geographic_toponymic_bias
from institution_bias import evaluate_institution_bias
from intersectional_corpus_bias import evaluate_intersectional_corpus_bias
from name_gender_distribution import DEFAULT_TARGET_LABELS, evaluate_name_gender_distribution
from role_profession_gender_bias import evaluate_role_profession_gender_bias
from weat_gender_analysis import run_weat_analysis


def _write_json(path: Path, obj: Dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)


def run_suite(
    corpus_root: str,
    output_dir: str = "bias_evaluation_results_suite",
    max_docs: Optional[int] = 10,
    make_plots: bool = False,
    lexicon_path: Optional[str] = None,
    diagnosis_reference_path: Optional[str] = None,
    age_reference_path: Optional[str] = None,
) -> Dict[str, Any]:
    root = Path(corpus_root)
    entidades_dir = root / "entidades"
    documents_dir = root / "documents"

    if not entidades_dir.is_dir():
        raise FileNotFoundError(f"No se encontró entidades/: {entidades_dir}")
    if not documents_dir.is_dir():
        raise FileNotFoundError(f"No se encontró documents/: {documents_dir}")

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Convention: max_docs <= 0 => process all files
    max_docs_effective: Optional[int] = None if (max_docs is not None and max_docs <= 0) else max_docs

    suite_meta = {
        "suite": "bias_suite_corpus_v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "corpus_root": str(root),
        "paths": {"entidades": str(entidades_dir), "documents": str(documents_dir)},
        "max_docs": max_docs_effective,
        "make_plots": make_plots,
        "lexicon_path": lexicon_path,
        "diagnosis_reference_path": diagnosis_reference_path,
        "age_reference_path": age_reference_path,
    }

    results: Dict[str, Any] = {"meta": suite_meta, "metrics": {}}

    # 1.1
    m11 = evaluate_name_gender_distribution(
        annotations_path=str(entidades_dir),
        target_labels=DEFAULT_TARGET_LABELS,
        lexicon_path=lexicon_path,
        max_files=max_docs_effective,
    )
    m11_path = _write_json(out_dir / "1_1_name_gender_distribution.json", m11)
    results["metrics"]["1.1_name_gender_distribution"] = {"output_path": m11_path, "result": m11}

    # 1.2
    m12 = evaluate_role_profession_gender_bias(
        annotations_path=str(entidades_dir),
        lexicon_path=lexicon_path,
        max_files=max_docs_effective,
        association_mode="cartesian",
    )
    m12_path = _write_json(out_dir / "1_2_role_profession_gender_bias.json", m12)
    results["metrics"]["1.2_role_profession_gender_bias"] = {"output_path": m12_path, "result": m12}

    # 1.3
    m13 = evaluate_geographic_toponymic_bias(
        annotations_path=str(entidades_dir),
        top_k=20,
        max_files=max_docs_effective,
    )
    m13_path = _write_json(out_dir / "1_3_geographic_toponymic_bias.json", m13)
    results["metrics"]["1.3_geographic_toponymic_bias"] = {"output_path": m13_path, "result": m13}

    # 1.4
    m14 = evaluate_age_distribution(
        annotations_path=str(entidades_dir),
        max_files=max_docs_effective,
        underrep_min_percent=5.0,
    )
    m14_path = _write_json(out_dir / "1_4_age_distribution.json", m14)
    results["metrics"]["1.4_age_distribution"] = {"output_path": m14_path, "result": m14}

    # 1.5
    m15 = evaluate_institution_bias(
        annotations_path=str(entidades_dir),
        top_k=20,
        max_files=max_docs_effective,
    )
    m15_path = _write_json(out_dir / "1_5_institution_bias.json", m15)
    results["metrics"]["1.5_institution_bias"] = {"output_path": m15_path, "result": m15}

    # 1.6
    m16 = evaluate_diagnosis_bias(
        documents_path=str(documents_dir),
        reference_path=diagnosis_reference_path,
        top_k=20,
        max_files=max_docs_effective,
        use_sections=True,
        use_phrases=True,
    )
    m16_path = _write_json(out_dir / "1_6_diagnosis_condition_bias.json", m16)
    results["metrics"]["1.6_diagnosis_condition_bias"] = {"output_path": m16_path, "result": m16}

    # Interseccionalidad: género×edad, género×geografía, edad×geografía
    try:
        m_int = evaluate_intersectional_corpus_bias(
            annotations_path=str(entidades_dir),
            lexicon_path=lexicon_path,
            max_files=max_docs_effective,
        )
        m_int_path = _write_json(out_dir / "intersectional_corpus_bias.json", m_int)
        results["metrics"]["intersectional_corpus_bias"] = {"output_path": m_int_path, "result": m_int}
    except Exception as e:
        results["metrics"]["intersectional_corpus_bias"] = {"error": str(e), "result": None}

    # Diagnóstico × demografía (género y edad por doc)
    try:
        m_ddx = evaluate_diagnosis_demography_bias(
            annotations_path=str(entidades_dir),
            documents_path=str(documents_dir),
            lexicon_path=lexicon_path,
            max_files=max_docs_effective,
        )
        m_ddx_path = _write_json(out_dir / "diagnosis_demography_bias.json", m_ddx)
        results["metrics"]["diagnosis_demography_bias"] = {"output_path": m_ddx_path, "result": m_ddx}
    except Exception as e:
        results["metrics"]["diagnosis_demography_bias"] = {"error": str(e), "result": None}

    # Género vs proporción objetivo (usa 1.1)
    try:
        m_gt = evaluate_gender_target_proportion(
            annotations_path=str(entidades_dir),
            lexicon_path=lexicon_path,
            max_files=max_docs_effective,
            target_fem=0.5,
            target_masc=0.5,
            result_1_1=m11,
        )
        m_gt_path = _write_json(out_dir / "gender_target_proportion.json", m_gt)
        results["metrics"]["gender_target_proportion"] = {"output_path": m_gt_path, "result": m_gt}
    except Exception as e:
        results["metrics"]["gender_target_proportion"] = {"error": str(e), "result": None}

    # Edad vs referencia (usa 1.4)
    try:
        m_ar = evaluate_age_reference_comparison(
            annotations_path=str(entidades_dir),
            max_files=max_docs_effective,
            reference_path=age_reference_path,
            result_1_4=m14,
        )
        m_ar_path = _write_json(out_dir / "age_reference_comparison.json", m_ar)
        results["metrics"]["age_reference_comparison"] = {"output_path": m_ar_path, "result": m_ar}
    except Exception as e:
        results["metrics"]["age_reference_comparison"] = {"error": str(e), "result": None}

    # Cobertura/completitud por documento
    try:
        m_cov = evaluate_coverage_completeness(
            annotations_path=str(entidades_dir),
            lexicon_path=lexicon_path,
            max_files=max_docs_effective,
        )
        m_cov_path = _write_json(out_dir / "coverage_completeness.json", m_cov)
        results["metrics"]["coverage_completeness"] = {"output_path": m_cov_path, "result": m_cov}
    except Exception as e:
        results["metrics"]["coverage_completeness"] = {"error": str(e), "result": None}

    # WEAT (sesgo de género por embeddings)
    try:
        weat = run_weat_analysis(
            documents_path=str(documents_dir),
            max_docs=max_docs_effective,
            n_permutations=1000,
        )
        weat_path = _write_json(out_dir / "weat_gender_analysis.json", weat)
        results["metrics"]["weat_gender_analysis"] = {"output_path": weat_path, "result": weat}
    except Exception as e:
        results["metrics"]["weat_gender_analysis"] = {"error": str(e), "result": None}

    # Resumen diversidad (variety/balance desde 1.3, 1.5, 1.6)
    try:
        m_div = evaluate_diversity_summary(output_dir=str(out_dir))
        m_div_path = _write_json(out_dir / "diversity_summary.json", m_div)
        results["metrics"]["diversity_summary"] = {"output_path": m_div_path, "result": m_div}
    except Exception as e:
        results["metrics"]["diversity_summary"] = {"error": str(e), "result": None}

    # Consolidated
    consolidated_path = _write_json(out_dir / "consolidated_bias_report.json", results)
    return {"output_dir": str(out_dir), "consolidated_path": consolidated_path, "report": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run bias suite (1.1–1.6 + WEAT) on corpus_v1")
    parser.add_argument("--corpus_root", required=True, help="Ruta a corpus_v1 (con documents/ y entidades/)")
    parser.add_argument("--output_dir", default="bias_evaluation_results_suite")
    parser.add_argument(
        "--max_docs",
        type=int,
        default=10,
        help="Cantidad de archivos a procesar (ordenados por nombre). Usa 0 para procesar TODOS.",
    )
    parser.add_argument("--make_plots", action="store_true", help="(placeholder) plots are run per-metric scripts")
    parser.add_argument("--lexicon_path", default=None, help="CSV/JSON opcional nombre->género (para 1.1/1.2)")
    parser.add_argument("--diagnosis_reference_path", default=None, help="CSV/JSON con distribución de referencia (1.6)")
    parser.add_argument("--age_reference_path", default=None, help="JSON década->p para age_reference_comparison")
    args = parser.parse_args()

    out = run_suite(
        corpus_root=args.corpus_root,
        output_dir=args.output_dir,
        max_docs=args.max_docs,
        make_plots=args.make_plots,
        lexicon_path=args.lexicon_path,
        diagnosis_reference_path=args.diagnosis_reference_path,
        age_reference_path=args.age_reference_path,
    )

    print("=" * 80)
    print("BIAS SUITE (1.1–1.6 + WEAT + interseccionalidad, diagnóstico×demografía, objetivo, referencia, cobertura, diversidad) COMPLETADA")
    print("=" * 80)
    print(f"Output dir: {out['output_dir']}")
    print(f"Consolidated: {out['consolidated_path']}")

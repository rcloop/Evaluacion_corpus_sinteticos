#!/usr/bin/env python3
"""
Generate the real validation corpus locally for experiment 07 (statistical comparison).

This corpus is used as --real_corpus when running:
  python src/experimentos/naturalidad/07_statistical_comparison.py \
    --generated_corpus <path_to_generated> --real_corpus <path_to_this_corpus>

Output: data/real_validation_corpus/*.txt (one document per file, UTF-8 plain text).

Usage:
  python scripts/generate_real_validation_corpus.py [--output_dir DATA/real_validation_corpus] [--num_docs 50]
"""
from pathlib import Path
import argparse
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "real_validation_corpus"

# Fixed clinical-style Spanish sentences (reproducible, MEDDOCAN-like domain).
# These are synthetic placeholders; for real validation you can replace with MEDDOCAN test set.
_SAMPLES = [
    "Paciente de 67 años que ingresa por dolor torácico de 24 horas de evolución.",
    "Antecedentes personales: HTA en tratamiento, dislipemia. Sin alergias medicamentosas conocidas.",
    "Exploración: Consciente y orientado. TA 145/90 mmHg. FC 78 lpm. SatO2 96% en aire ambiente.",
    "A la auscultación cardíaca ritmo regular sin soplos. Murmullo vesicular conservado.",
    "Se solicita analítica de ingreso con troponina y ECG seriado.",
    "ECG: ritmo sinusal, sin alteraciones agudas del segmento ST.",
    "Troponina I negativa. Se descarta síndrome coronario agudo en este momento.",
    "Se mantiene observación y control de constantes. Dieta absoluta hasta descartar patología digestiva.",
    "En la radiografía de tórax no se observan infiltrados ni derrame pleural.",
    "El paciente refiere mejoría del dolor tras analgesia. Se pauta alta con control en atención primaria.",
    "Informe de alta: Ingreso por dolor torácico. Estudio completo sin hallazgos de isquemia.",
    "Recomendaciones: Seguir tratamiento antihipertensivo. Control analítico en una semana.",
    "Paciente derivado desde urgencias para valoración por neumología.",
    "Tos seca de dos semanas de evolución. Fiebre ocasional. No pérdida de peso.",
    "En la TC torácica se observa imagen nodular en lóbulo superior derecho de 15 mm.",
    "Se programa broncoscopia con biopsia para caracterización histológica.",
    "Antecedentes: Exfumador de 20 paquetes año. No otros factores de riesgo.",
    "Exploración respiratoria: crepitantes basales derechos. Resto sin hallazgos.",
    "Gasometría arterial en aire ambiente: pH 7.42, pCO2 38 mmHg, pO2 72 mmHg.",
    "Espirometría: patrón obstructivo leve. FEV1 78% teórico. Se completa estudio.",
    "Alta con diagnóstico de neumonía adquirida en la comunidad. Tratamiento antibiótico completado.",
    "Control en consultas externas de neumología en 4 semanas con nueva TC.",
    "Paciente ingresado para estudio de anemia crónica. Hemoglobina 9.2 g/dL.",
    "Ferritina baja. Transferrina elevada. Estudio de sangrado digestivo indicado.",
    "Gastroscopia: mucosa gástrica sin lesiones. Colonoscopia programada.",
    "En colonoscopia se identifica lesión polipoide en colon ascendente. Resección endoscópica.",
    "Anatomía patológica: adenoma tubular con displasia de bajo grado. Margen libre.",
    "Se recomienda colonoscopia de control a los 3 años según guías.",
    "Paciente con insuficiencia cardíaca conocida. Ingreso por descompensación con edemas.",
    "Ecocardiograma: FEVI 35%. Dilatación de cavidades izquierdas. Insuficiencia mitral leve.",
    "Se optimiza tratamiento diurético y se ajusta dosis de IECA según tolerancia.",
    "Alta a domicilio con plan de cuidados y control en insuficiencia cardíaca.",
    "Nota de evolución: Estable. Sin disnea en reposo. Diuresis adecuada.",
    "Analítica de control: creatinina 1.1 mg/dL, potasio 4.2 mEq/L. Sin alteraciones.",
    "Informe de interconsulta a cardiología: Valorar indicación de dispositivo.",
    "Paciente con diabetes tipo 2. Control en consulta de endocrinología.",
    "HbA1c 7.8%. Se intensifica tratamiento con metformina y se añade inhibidor SGLT2.",
    "Revisión podológica: pie diabético sin lesiones. Sensibilidad conservada.",
    "Fondo de ojo: retinopatía diabética no proliferativa leve. Control anual.",
    "Recomendaciones dietéticas y de ejercicio entregadas. Control en 3 meses.",
]


def _make_document(sample_indices: list[int], samples: list[str]) -> str:
    """Build one document from selected samples (one or more sentences)."""
    return " ".join(samples[i % len(samples)] for i in sample_indices)


def generate_corpus(
    output_dir: Path,
    num_docs: int = 50,
    min_sentences: int = 2,
    max_sentences: int = 8,
) -> None:
    """Write num_docs .txt files into output_dir with reproducible clinical-style Spanish text."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    n = len(_SAMPLES)

    for i in range(num_docs):
        # Reproducible: deterministic sequence per doc (no random).
        # Each doc gets 2–8 sentences from _SAMPLES (cycled indices).
        num_sent = min_sentences + (i % (max_sentences - min_sentences + 1))
        indices = [(i * 7 + j) % n for j in range(num_sent)]
        text = _make_document(indices, _SAMPLES)
        out_file = output_dir / f"doc_{i:04d}.txt"
        out_file.write_text(text, encoding="utf-8")

    print(f"Generated {num_docs} documents in {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate real validation corpus for experiment 07 (statistical comparison)."
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for .txt files (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--num_docs",
        type=int,
        default=50,
        help="Number of documents to generate (default: 50)",
    )
    parser.add_argument(
        "--min_sentences",
        type=int,
        default=2,
        help="Minimum sentences per document (default: 2)",
    )
    parser.add_argument(
        "--max_sentences",
        type=int,
        default=8,
        help="Maximum sentences per document (default: 8)",
    )
    args = parser.parse_args()

    if args.num_docs < 1:
        print("Error: num_docs must be >= 1", file=sys.stderr)
        sys.exit(1)
    if args.min_sentences < 1 or args.max_sentences < args.min_sentences:
        print("Error: need 1 <= min_sentences <= max_sentences", file=sys.stderr)
        sys.exit(1)

    generate_corpus(
        output_dir=args.output_dir,
        num_docs=args.num_docs,
        min_sentences=args.min_sentences,
        max_sentences=args.max_sentences,
    )


if __name__ == "__main__":
    main()

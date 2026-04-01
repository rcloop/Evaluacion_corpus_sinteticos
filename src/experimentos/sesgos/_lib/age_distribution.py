"""
Metric 1.4 - Distribución de edades (AGE_OF_SUBJECT / EDAD_SUJETO_ASISTENCIA)

Qué:
  Histograma por décadas (0–9, 10–19, ...), porcentajes por bin, entropía (Shannon),
  y detección simple de infrarrepresentación (configurable).

Entrada:
  - Directorio `entidades/` con JSON por documento (formato MEDDOCAN-like):
      { "id": "...", "data": [ { "entity": "...", "text": "..." }, ... ] }
    o bien:
      { "entities": [ { "label": "...", "text": "..." }, ... ] }

Salida:
  - JSON con bins + métricas
  - (opcional) PNG con histograma (requiere matplotlib)
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Literal

from name_gender_distribution import iter_entities_from_annotation_obj


DEFAULT_AGE_LABELS = [
    # MEDDOCAN (es)
    "EDAD_SUJETO_ASISTENCIA",
    # english alias
    "AGE_OF_SUBJECT",
]


def parse_age(text: str) -> Optional[int]:
    """
    Extract age as integer from a string.
    Accepts patterns like: "85", "85 años", "Edad: 32", "32-year-old" (best-effort).
    """
    s = str(text).strip()
    if not s:
        return None

    sl = s.lower()

    # Recover ages expressed without digits (agreed rules):
    # - "octogenario próximo" -> 70-79 (approx. close to 80)
    if "octogenario" in sl and ("próximo" in sl or "proximo" in sl):
        return 79

    # -X-agenario forms
    if re.search(r"\bsexagenari[oa]?\b", sl):
        return 65
    if re.search(r"\bseptuagenari[oa]?\b", sl):
        return 75
    if re.search(r"\boctogenari[oa]?\b", sl):
        return 85
    if re.search(r"\bnonagenari[oa]?\b", sl):
        return 95
    if re.search(r"\bcentenari[oa]?\b", sl):
        return 105

    # Decade-of-life expressions:
    # sixth decade -> 50-59; seventh -> 60-69; eighth -> 70-79; ninth -> 80-89; tenth -> 90-99
    # (These map to representative ages in-bin.)
    if ("sexta década" in sl) or ("sexta decada" in sl):
        return 55
    if ("séptima década" in sl) or ("septima década" in sl) or ("séptima decada" in sl) or ("septima decada" in sl):
        return 65
    if ("octava década" in sl) or ("octava decada" in sl):
        return 75
    if ("novena década" in sl) or ("novena decada" in sl):
        return 85
    if ("décima década" in sl) or ("decima década" in sl) or ("décima decada" in sl) or ("decima decada" in sl):
        return 95

    # Prefer explicit 0-120 like numbers; avoid IDs by restricting magnitude.
    m = re.search(r"(?<!\d)(\d{1,3})(?!\d)", s)
    if not m:
        return None
    try:
        age = int(m.group(1))
    except Exception:
        return None
    if age < 0 or age > 120:
        return None
    return age


def decade_bin(age: int, max_decade: int = 120) -> str:
    """
    Returns a label like '0-9', '10-19', ..., '80-89', '90-99', '100-109', '110-119', '120+'.
    """
    if age >= max_decade:
        return f"{max_decade}+"
    start = (age // 10) * 10
    end = start + 9
    return f"{start}-{end}"


def shannon_entropy(counter: Counter) -> Dict[str, Optional[float]]:
    total = sum(counter.values())
    if total == 0:
        return {"entropy_bits": None, "normalized_entropy": None, "support": 0}
    h = 0.0
    for _, v in counter.items():
        p = v / total
        if p > 0:
            h -= p * math.log(p, 2)
    support = len(counter)
    h_norm = None
    if support > 1:
        h_norm = h / math.log(support, 2)
    return {
        "entropy_bits": float(h),
        "normalized_entropy": (float(h_norm) if h_norm is not None else None),
        "support": int(support),
    }


def make_histogram_plot(bins: List[str], percentages: List[float], out_path: Path) -> Optional[str]:
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception:
        return None

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(range(len(bins)), percentages)
    ax.set_xticks(range(len(bins)))
    ax.set_xticklabels(bins, rotation=30, ha="right")
    ax.set_ylabel("%")
    ax.set_title("Distribución de edades por décadas")
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    return str(out_path)


def evaluate_age_distribution(
    annotations_path: str,
    age_labels: Optional[List[str]] = None,
    max_files: Optional[int] = None,
    max_decade: int = 120,
    underrep_min_percent: float = 5.0,
    underrep_bins: Optional[List[str]] = None,
    aggregation: Literal["mention", "doc_mode"] = "mention",
) -> Dict[str, Any]:
    p = Path(annotations_path)
    if not p.exists():
        raise FileNotFoundError(str(p))

    label_set = {l.upper().strip() for l in (age_labels or DEFAULT_AGE_LABELS)}

    ages_seen = 0  # age-labeled entities encountered (mention-level)
    ages_parsed = 0  # parsed age entities (mention-level)
    ages_recovered_textual = 0  # parsed ages recovered from non-digit expressions (mention-level)
    docs_seen: Optional[int] = 0
    docs_with_age_entity = 0
    docs_with_parsed_age = 0
    docs_with_multiple_parsed_ages = 0
    docs_mode_ties = 0

    bin_counts: Counter = Counter()

    def extract_parsed_ages_from_obj(obj: Any) -> List[int]:
        nonlocal ages_seen, ages_parsed, ages_recovered_textual
        parsed: List[int] = []
        for lab, txt in iter_entities_from_annotation_obj(obj):
            lu = lab.upper().strip()
            if lu not in label_set:
                continue
            ages_seen += 1
            raw = str(txt).strip()
            age = parse_age(raw)
            if age is None:
                continue
            # If no digits in raw but we recovered an age, count as textual recovery.
            if not re.search(r"\d", raw):
                ages_recovered_textual += 1
            ages_parsed += 1
            parsed.append(age)
        return parsed

    def choose_doc_age_mode(ages: List[int]) -> Optional[int]:
        """
        Selects a single representative age for a document using the most frequent parsed age.
        Tie-break is deterministic: choose the smallest age among tied modes.
        """
        nonlocal docs_mode_ties
        if not ages:
            return None
        c = Counter(ages)
        max_count = max(c.values())
        modes = sorted([a for a, v in c.items() if v == max_count])
        if len(modes) > 1:
            docs_mode_ties += 1
        return modes[0]

    if p.is_dir():
        files = sorted(p.glob("*.json"))
        if max_files is not None:
            files = files[: max_files]
        for fp in files:
            docs_seen += 1
            try:
                obj = json.loads(fp.read_text(encoding="utf-8"))
            except Exception:
                continue
            parsed_ages = extract_parsed_ages_from_obj(obj)
            # Determine doc-level signals precisely (scan only labels/texts, no parsing).
            has_age_entity = False
            for lab, txt in iter_entities_from_annotation_obj(obj):
                if lab.upper().strip() in label_set and str(txt).strip():
                    has_age_entity = True
                    break
            if has_age_entity:
                docs_with_age_entity += 1
            if parsed_ages:
                docs_with_parsed_age += 1
                if len(parsed_ages) > 1:
                    docs_with_multiple_parsed_ages += 1

            if aggregation == "mention":
                for age in parsed_ages:
                    bin_counts[decade_bin(age, max_decade=max_decade)] += 1
            elif aggregation == "doc_mode":
                doc_age = choose_doc_age_mode(parsed_ages)
                if doc_age is not None:
                    bin_counts[decade_bin(doc_age, max_decade=max_decade)] += 1
            else:
                raise ValueError(f"Unknown aggregation mode: {aggregation}")
    else:
        obj = json.loads(p.read_text(encoding="utf-8"))
        parsed_ages = extract_parsed_ages_from_obj(obj)
        # For single-document mode we still report doc-level counters.
        docs_seen = None
        docs_with_age_entity = 1 if any(
            (lab.upper().strip() in label_set and str(txt).strip())
            for lab, txt in iter_entities_from_annotation_obj(obj)
        ) else 0
        docs_with_parsed_age = 1 if parsed_ages else 0
        docs_with_multiple_parsed_ages = 1 if (len(parsed_ages) > 1) else 0
        if aggregation == "mention":
            for age in parsed_ages:
                bin_counts[decade_bin(age, max_decade=max_decade)] += 1
        elif aggregation == "doc_mode":
            doc_age = choose_doc_age_mode(parsed_ages)
            if doc_age is not None:
                bin_counts[decade_bin(doc_age, max_decade=max_decade)] += 1
        else:
            raise ValueError(f"Unknown aggregation mode: {aggregation}")

    # build ordered bins (0-9.., plus max_decade+)
    decade_starts = list(range(0, max_decade, 10))
    bins = [f"{s}-{s+9}" for s in decade_starts] + [f"{max_decade}+"]

    n = sum(bin_counts.values())
    percentages = [(bin_counts.get(b, 0) * 100.0 / n) if n else 0.0 for b in bins]

    underrep_bins = underrep_bins or [b for b in bins if b.startswith("80-") or b.startswith("90-") or b.endswith("+")]
    underrep = []
    for b in underrep_bins:
        pct = (bin_counts.get(b, 0) * 100.0 / n) if n else 0.0
        underrep.append(
            {
                "bin": b,
                "percent": pct,
                "flag_underrepresented": (pct < underrep_min_percent) if n else None,
                "threshold_percent": underrep_min_percent,
            }
        )

    return {
        "metric": "1.4_age_distribution",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_summary": {
            "annotations_path": str(annotations_path),
            "age_labels": sorted(label_set),
            "max_files": max_files,
            "docs_seen": docs_seen if p.is_dir() else None,
            "aggregation": aggregation,
            "docs_with_age_entity": int(docs_with_age_entity),
            "docs_with_parsed_age": int(docs_with_parsed_age),
            "docs_with_multiple_parsed_ages": int(docs_with_multiple_parsed_ages),
            "docs_mode_ties": int(docs_mode_ties),
            "ages_entities_seen": ages_seen,
            "ages_parsed": ages_parsed,
            "ages_recovered_textual": ages_recovered_textual,
            "max_decade": max_decade,
        },
        "histogram": {
            "bins": bins,
            "counts": [int(bin_counts.get(b, 0)) for b in bins],
            "percentages": percentages,
            "n": int(n),
        },
        "entropy": shannon_entropy(bin_counts),
        "underrepresentation_checks": underrep,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Metric 1.4 - Distribución de edades por décadas")
    parser.add_argument("--annotations_path", required=True, help="Ruta a entidades/ (directorio) o a un JSON")
    parser.add_argument("--max_files", type=int, default=None, help="Limita cantidad de JSON a leer (para pruebas)")
    parser.add_argument("--output_path", default="bias_evaluation_results/age_distribution.json")
    parser.add_argument("--make_plot", action="store_true", help="Genera histograma PNG (requiere matplotlib)")
    parser.add_argument("--plot_path", default="bias_evaluation_results/age_distribution_hist.png")
    parser.add_argument("--underrep_min_percent", type=float, default=5.0)
    args = parser.parse_args()

    result = evaluate_age_distribution(
        annotations_path=args.annotations_path,
        max_files=args.max_files,
        underrep_min_percent=args.underrep_min_percent,
    )

    out_p = Path(args.output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    plot_written = None
    if args.make_plot:
        plot_written = make_histogram_plot(
            bins=result["histogram"]["bins"],
            percentages=result["histogram"]["percentages"],
            out_path=Path(args.plot_path),
        )
    result["plot_path"] = plot_written
    if args.make_plot and plot_written is None:
        result["plot_warning"] = "Plot requested but matplotlib is not available."
        out_p.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=" * 80)
    print("METRIC 1.4 - AGE DISTRIBUTION")
    print("=" * 80)
    print(f"Output: {out_p}")
    if plot_written:
        print(f"Plot: {plot_written}")
    print("Entropy:", result["entropy"])


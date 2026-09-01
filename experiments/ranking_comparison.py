from __future__ import annotations

import csv
from pathlib import Path

from agentic_prevapt.io import load_paths
from agentic_prevapt.ranking import kendall_tau_b, kendall_tau_exact_pvalue, kendall_tau_permutation_pvalue, stratified_kendall_tau_b
from agentic_prevapt.risk import RiskModel

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "synthetic_paths_30.json"
OUTPUT = ROOT / "data" / "ranking_comparison.csv"


def main() -> None:
    model = RiskModel()
    rows = []
    for path in load_paths(INPUT):
        if path.cvss_max is None:
            raise ValueError(f"{path.id} is missing cvss_max")
        probability = model.path_probability(path)
        impact = model.impact(path.impact)
        length = len(path.steps)
        rows.append({
            "id": path.id,
            "length": length,
            "path_probability": probability,
            "impact_only": impact,
            "prevapt_score": probability * impact,
            "length_normalized_score": probability ** (1.0 / length) * impact,
            "cvss_max": path.cvss_max,
        })

    def mapping(field: str) -> dict[str, float]:
        return {str(row["id"]): float(row[field]) for row in rows}

    score, cvss = mapping("prevapt_score"), mapping("cvss_max")
    impact, normalized = mapping("impact_only"), mapping("length_normalized_score")
    lengths = {str(row["id"]): int(row["length"]) for row in rows}
    metrics = {
        "tau_prevapt_vs_cvss": kendall_tau_b(score, cvss),
        "p_prevapt_vs_cvss_exact": kendall_tau_exact_pvalue(score, cvss),
        "tau_prevapt_vs_impact": kendall_tau_b(score, impact),
        "p_prevapt_vs_impact_permutation": kendall_tau_permutation_pvalue(score, impact),
        "tau_prevapt_vs_cvss_within_length": stratified_kendall_tau_b(score, cvss, lengths),
        "tau_length_normalized_vs_cvss": kendall_tau_b(normalized, cvss),
    }
    for length in sorted(set(lengths.values())):
        ids = [item for item, value in lengths.items() if value == length]
        length_score = {item: score[item] for item in ids}
        length_cvss = {item: cvss[item] for item in ids}
        metrics[f"tau_prevapt_vs_cvss_length_{length}"] = kendall_tau_b(length_score, length_cvss)
        metrics[f"p_prevapt_vs_cvss_length_{length}_exact"] = kendall_tau_exact_pvalue(length_score, length_cvss)

    rows.sort(key=lambda row: float(row["prevapt_score"]), reverse=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        fields = ["rank", "id", "length", "path_probability", "impact_only", "prevapt_score", "length_normalized_score", "cvss_max"]
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for rank, row in enumerate(rows, start=1):
            writer.writerow({
                "rank": rank,
                "id": row["id"],
                "length": row["length"],
                "path_probability": f"{float(row['path_probability']):.6f}",
                "impact_only": f"{float(row['impact_only']):.2f}",
                "prevapt_score": f"{float(row['prevapt_score']):.6f}",
                "length_normalized_score": f"{float(row['length_normalized_score']):.6f}",
                "cvss_max": f"{float(row['cvss_max']):.1f}",
            })

    print(f"paths={len(rows)}")
    for name, value in metrics.items():
        print(f"{name}={value:.6g}")
    print(f"input={INPUT}")
    print(f"output={OUTPUT}")


if __name__ == "__main__":
    main()

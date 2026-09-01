from __future__ import annotations

import csv
from pathlib import Path

from agentic_prevapt.io import load_paths
from agentic_prevapt.ranking import kendall_tau_b
from agentic_prevapt.risk import RiskModel


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "ranking_comparison.csv"


def main() -> None:
    model = RiskModel()
    rows: list[dict[str, str | float]] = []
    for scenario_file in sorted((ROOT / "examples").glob("scenario_*.json")):
        scenario = scenario_file.stem.removeprefix("scenario_")
        for path in load_paths(scenario_file):
            if path.cvss_max is None:
                raise ValueError(f"{path.id} is missing cvss_max")
            rows.append(
                {
                    "id": f"{scenario}:{path.id}",
                    "scenario": scenario,
                    "path": path.id,
                    "prevapt_score": model.path_score(path),
                    "cvss_max": path.cvss_max,
                    "impact_only": model.impact(path.impact),
                }
            )

    score = {str(row["id"]): float(row["prevapt_score"]) for row in rows}
    cvss = {str(row["id"]): float(row["cvss_max"]) for row in rows}
    impact = {str(row["id"]): float(row["impact_only"]) for row in rows}
    tau_cvss = kendall_tau_b(score, cvss)
    tau_impact = kendall_tau_b(score, impact)

    rows.sort(key=lambda row: float(row["prevapt_score"]), reverse=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["rank", "scenario", "path", "prevapt_score", "cvss_max", "impact_only"],
        )
        writer.writeheader()
        for rank, row in enumerate(rows, start=1):
            writer.writerow(
                {
                    "rank": rank,
                    "scenario": row["scenario"],
                    "path": row["path"],
                    "prevapt_score": f"{float(row['prevapt_score']):.6f}",
                    "cvss_max": f"{float(row['cvss_max']):.1f}",
                    "impact_only": f"{float(row['impact_only']):.2f}",
                }
            )

    print(f"paths={len(rows)}")
    print(f"tau_prevapt_vs_cvss={tau_cvss:.6f}")
    print(f"tau_prevapt_vs_impact={tau_impact:.6f}")
    print(f"output={OUTPUT}")


if __name__ == "__main__":
    main()

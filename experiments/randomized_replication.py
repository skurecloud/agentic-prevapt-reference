from __future__ import annotations

import csv
import json
from math import sqrt
from pathlib import Path
from random import Random

from agentic_prevapt.ranking import kendall_tau_b, stratified_kendall_tau_b
from agentic_prevapt.risk import AttackPath, ImpactFeatures, RiskModel, StepFeatures

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "randomized_replication.csv"
SUMMARY = ROOT / "data" / "randomized_replication_summary.json"
SEED = 20260901
REPLICATIONS = 1000


def quantile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def summarize(values: list[float]) -> dict[str, float]:
    mean = sum(values) / len(values)
    sd = sqrt(sum((value - mean) ** 2 for value in values) / (len(values) - 1))
    return {"mean": mean, "sd": sd, "q025": quantile(values, 0.025), "q975": quantile(values, 0.975)}


def run(seed: int = SEED, replications: int = REPLICATIONS) -> tuple[list[dict[str, float | int]], dict[str, object]]:
    random = Random(seed)
    model = RiskModel()
    rows: list[dict[str, float | int]] = []
    for replication in range(1, replications + 1):
        score: dict[str, float] = {}
        cvss: dict[str, float] = {}
        lengths: dict[str, int] = {}
        for length in (2, 3, 4):
            for index in range(10):
                item_id = f"r{replication}-L{length}-{index}"
                steps = [StepFeatures(
                    exploitability=random.uniform(0.25, 0.90),
                    privilege=random.uniform(0.20, 0.90),
                    attack_ease=random.uniform(0.25, 0.90),
                    detection_difficulty=random.uniform(0.20, 0.90),
                )]
                for _ in range(1, length):
                    steps.append(StepFeatures(
                        exploitability=random.uniform(0.25, 0.90),
                        privilege=random.uniform(0.20, 0.90),
                        attack_ease=random.uniform(0.25, 0.90),
                        detection_difficulty=random.uniform(0.20, 0.90),
                        conditional_probability=random.uniform(0.65, 0.90),
                    ))
                path = AttackPath(
                    id=item_id,
                    steps=tuple(steps),
                    impact=ImpactFeatures(
                        data_sensitivity=random.uniform(3.0, 9.5),
                        business_criticality=random.uniform(3.0, 9.5),
                        operational_impact=random.uniform(3.0, 9.5),
                    ),
                    cvss_max=random.uniform(4.0, 9.0),
                )
                score[item_id] = model.path_score(path)
                cvss[item_id] = float(path.cvss_max)
                lengths[item_id] = length
        pooled = kendall_tau_b(score, cvss)
        stratified = stratified_kendall_tau_b(score, cvss, lengths)
        tau_score_length = kendall_tau_b(score, {item: float(length) for item, length in lengths.items()})
        tau_cvss_length = kendall_tau_b(cvss, {item: float(length) for item, length in lengths.items()})
        rows.append({
            "replication": replication,
            "tau_pooled": pooled,
            "tau_within_length": stratified,
            "tau_score_length": tau_score_length,
            "tau_cvss_length": tau_cvss_length,
        })
    pooled_values = [float(row["tau_pooled"]) for row in rows]
    stratified_values = [float(row["tau_within_length"]) for row in rows]
    differences = [abs(a - b) for a, b in zip(pooled_values, stratified_values)]
    sign_disagreement = sum((a < 0) != (b < 0) for a, b in zip(pooled_values, stratified_values)) / replications
    summary: dict[str, object] = {
        "seed": seed,
        "replications": replications,
        "paths_per_replication": 30,
        "cvss_distribution": "Uniform(4, 9), independent of path length and features",
        "pooled_tau": summarize(pooled_values),
        "within_length_tau": summarize(stratified_values),
        "absolute_pooled_minus_within": summarize(differences),
        "sign_disagreement_rate": sign_disagreement,
    }
    return rows, summary


def main() -> None:
    rows, summary = run()
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"output={OUTPUT}")


if __name__ == "__main__":
    main()

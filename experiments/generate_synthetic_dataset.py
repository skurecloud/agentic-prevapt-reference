from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "synthetic_paths_30.json"


def main() -> None:
    paths = []
    for length in (2, 3, 4):
        for index in range(10):
            exploitability = 0.35 + 0.045 * index
            steps = [{
                "exploitability": round(exploitability, 3),
                "privilege": round(0.35 + 0.04 * ((index * 3) % 7), 3),
                "attack_ease": round(0.40 + 0.05 * ((index * 2) % 6), 3),
                "detection_difficulty": round(0.30 + 0.05 * ((index * 5) % 8), 3),
            }]
            for step_index in range(1, length):
                steps.append({
                    "exploitability": round(min(0.95, exploitability + 0.03 * step_index), 3),
                    "privilege": 0.50,
                    "attack_ease": 0.55,
                    "detection_difficulty": 0.50,
                    "conditional_probability": round(0.70 + 0.02 * ((index + step_index) % 6), 3),
                })
            paths.append({
                "id": f"L{length}-P{index + 1:02d}",
                "steps": steps,
                "impact": {
                    "data_sensitivity": round(5.0 + 0.35 * index, 2),
                    "business_criticality": round(5.5 + 0.30 * index, 2),
                    "operational_impact": round(4.5 + 0.40 * index, 2),
                },
                "cvss_max": round(5.0 + 1.0 * (length - 2) + 0.1 * index, 1),
            })
    OUTPUT.write_text(json.dumps({"attack_paths": paths}, indent=2) + "\n", encoding="utf-8")
    print(f"paths={len(paths)}")
    print(f"output={OUTPUT}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

from .risk import AttackPath, ImpactFeatures, StepFeatures


def load_paths(path: str | Path) -> list[AttackPath]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    result: list[AttackPath] = []

    for item in payload["attack_paths"]:
        steps = tuple(
            StepFeatures(
                exploitability=s["exploitability"],
                privilege=s["privilege"],
                complexity=s["complexity"],
                detection_difficulty=s["detection_difficulty"],
                conditional_probability=s.get("conditional_probability"),
            )
            for s in item["steps"]
        )
        impact = ImpactFeatures(**item["impact"])
        result.append(
            AttackPath(
                id=item["id"],
                steps=steps,
                impact=impact,
                labels=tuple(item.get("labels", [])),
            )
        )
    return result

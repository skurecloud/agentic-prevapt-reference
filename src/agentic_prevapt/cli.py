from __future__ import annotations

import argparse
import json

from .engine import AssessmentEngine
from .io import load_paths


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the Agentic Pre-VAPT reference risk model."
    )
    parser.add_argument("scenario", help="Path to scenario JSON")
    args = parser.parse_args()

    paths = load_paths(args.scenario)
    result = AssessmentEngine().assess(paths)

    output = {
        "raw_system_score": round(result.raw_system_score, 6),
        "normalized_system_score": round(result.normalized_system_score, 6),
        "aggregation_method": result.aggregation_method,
        "paths": [
            {
                "id": p.id,
                "probability": round(p.probability, 6),
                "impact": round(p.impact, 6),
                "prioritization_score": round(p.risk, 6),
            }
            for p in result.paths
        ],
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

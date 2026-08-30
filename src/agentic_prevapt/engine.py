from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .risk import AttackPath, RiskModel


@dataclass(frozen=True)
class PathResult:
    id: str
    probability: float
    impact: float
    risk: float


@dataclass(frozen=True)
class AssessmentResult:
    paths: tuple[PathResult, ...]
    raw_system_risk: float
    normalized_system_risk: float


class AssessmentEngine:
    def __init__(self, model: RiskModel | None = None) -> None:
        self.model = model or RiskModel()

    def assess(self, paths: Iterable[AttackPath]) -> AssessmentResult:
        path_results = []
        for path in paths:
            probability = self.model.path_probability(path)
            impact = self.model.impact(path.impact)
            risk = probability * impact
            path_results.append(PathResult(path.id, probability, impact, risk))

        raw = sum(item.risk for item in path_results)
        normalized = self.model.normalize(raw)

        return AssessmentResult(tuple(path_results), raw, normalized)

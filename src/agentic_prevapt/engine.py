from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .overlap import pairwise_corrected_score
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
    raw_system_score: float
    normalized_system_score: float
    aggregation_method: str

    @property
    def raw_system_risk(self) -> float:
        return self.raw_system_score

    @property
    def normalized_system_risk(self) -> float:
        return self.normalized_system_score


class AssessmentEngine:
    def __init__(self, model: RiskModel | None = None) -> None:
        self.model = model or RiskModel()

    def assess(
        self,
        paths: Iterable[AttackPath],
        *,
        pairwise_joints: dict[tuple[str, str], float] | None = None,
        top_k: int | None = None,
    ) -> AssessmentResult:
        path_results = []
        for path in paths:
            probability = self.model.path_probability(path)
            impact = self.model.impact(path.impact)
            risk = probability * impact
            path_results.append(PathResult(path.id, probability, impact, risk))

        path_results.sort(key=lambda item: item.risk, reverse=True)
        if top_k is not None:
            if top_k <= 0:
                raise ValueError("top_k must be positive")
            path_results = path_results[:top_k]

        if pairwise_joints is None:
            raw = sum(item.risk for item in path_results)
            aggregation_method = "additive_without_overlap_correction"
        else:
            raw = pairwise_corrected_score(
                {item.id: item.probability for item in path_results},
                {item.id: item.impact for item in path_results},
                pairwise_joints,
            )
            aggregation_method = "pairwise_second_order_with_explicit_joints"
        normalized = self.model.normalize(raw)

        return AssessmentResult(
            tuple(path_results), raw, normalized, aggregation_method
        )

from __future__ import annotations

from dataclasses import dataclass, field
from math import exp
from typing import Iterable


def _unit_interval(value: float, name: str) -> float:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1], got {value}")
    return float(value)


def _zero_ten(value: float, name: str) -> float:
    if not 0.0 <= value <= 10.0:
        raise ValueError(f"{name} must be in [0, 10], got {value}")
    return float(value)


@dataclass(frozen=True)
class StepFeatures:
    """Normalized inputs used by the step exploitability model."""

    exploitability: float
    privilege: float
    complexity: float
    detection_difficulty: float
    conditional_probability: float | None = None

    def __post_init__(self) -> None:
        _unit_interval(self.exploitability, "exploitability")
        _unit_interval(self.privilege, "privilege")
        _unit_interval(self.complexity, "complexity")
        _unit_interval(self.detection_difficulty, "detection_difficulty")
        if self.conditional_probability is not None:
            _unit_interval(self.conditional_probability, "conditional_probability")


@dataclass(frozen=True)
class ImpactFeatures:
    """Business impact inputs on a 0-10 scale."""

    data_sensitivity: float
    business_criticality: float
    operational_impact: float

    def __post_init__(self) -> None:
        _zero_ten(self.data_sensitivity, "data_sensitivity")
        _zero_ten(self.business_criticality, "business_criticality")
        _zero_ten(self.operational_impact, "operational_impact")


@dataclass(frozen=True)
class AttackPath:
    id: str
    steps: tuple[StepFeatures, ...]
    impact: ImpactFeatures
    labels: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.steps:
            raise ValueError("An attack path must contain at least one step.")


@dataclass
class RiskModel:
    """Paper-aligned reference scoring model.

    The default coefficients are heuristic priors, not empirically calibrated
    probability parameters.
    """

    intercept: float = -1.0
    w_exploitability: float = 0.4
    w_privilege: float = 0.3
    w_complexity: float = 0.2
    w_detection: float = 0.1

    alpha_data: float = 0.5
    beta_business: float = 0.3
    gamma_operational: float = 0.2

    tau: float = 10.0

    @staticmethod
    def sigmoid(x: float) -> float:
        return 1.0 / (1.0 + exp(-x))

    def step_probability(self, features: StepFeatures) -> float:
        score = (
            self.intercept
            + self.w_exploitability * features.exploitability
            + self.w_privilege * features.privilege
            + self.w_complexity * features.complexity
            + self.w_detection * features.detection_difficulty
        )
        return self.sigmoid(score)

    def path_probability(self, path: AttackPath) -> float:
        first = self.step_probability(path.steps[0])
        probability = first

        for step in path.steps[1:]:
            # Explicit conditional probability takes precedence. When it is
            # unavailable, the step model is used as a transparent fallback.
            conditional = (
                step.conditional_probability
                if step.conditional_probability is not None
                else self.step_probability(step)
            )
            probability *= conditional

        return probability

    def impact(self, impact: ImpactFeatures) -> float:
        return (
            self.alpha_data * impact.data_sensitivity
            + self.beta_business * impact.business_criticality
            + self.gamma_operational * impact.operational_impact
        )

    def path_risk(self, path: AttackPath) -> float:
        return self.path_probability(path) * self.impact(path.impact)

    def raw_system_risk(self, paths: Iterable[AttackPath]) -> float:
        return sum(self.path_risk(path) for path in paths)

    def normalize(self, raw_risk: float) -> float:
        if raw_risk < 0:
            raise ValueError("raw_risk cannot be negative")
        if self.tau <= 0:
            raise ValueError("tau must be positive")
        return 100.0 * (1.0 - exp(-raw_risk / self.tau))

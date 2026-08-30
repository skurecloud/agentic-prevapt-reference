from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class PathEvent:
    id: str
    probability: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.probability <= 1.0:
            raise ValueError("probability must be in [0, 1]")


def union_probability_two(
    a: PathEvent,
    b: PathEvent,
    joint_probability: float,
) -> float:
    """Exact two-event inclusion-exclusion.

    P(A ∪ B) = P(A) + P(B) - P(A ∩ B)

    The joint probability must be supplied from a model or observed evidence.
    This implementation deliberately does not invent it from shared graph nodes.
    """

    if not 0.0 <= joint_probability <= min(a.probability, b.probability):
        raise ValueError(
            "joint_probability must be between 0 and min(P(A), P(B))"
        )

    result = a.probability + b.probability - joint_probability
    return min(1.0, max(0.0, result))


def pairwise_corrected_union(
    events: list[PathEvent],
    pairwise_joints: Mapping[tuple[str, str], float],
) -> float:
    """Second-order inclusion-exclusion approximation for multiple events.

    P(union A_i) ≈ ΣP(A_i) - ΣP(A_i ∩ A_j)

    This is exact only when higher-order intersections are zero or represented
    elsewhere. It is therefore returned as a bounded approximation.
    """

    total = sum(event.probability for event in events)
    ids = [e.id for e in events]

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            key = (ids[i], ids[j])
            reverse = (ids[j], ids[i])
            joint = pairwise_joints.get(key, pairwise_joints.get(reverse, 0.0))
            if joint < 0:
                raise ValueError("joint probabilities cannot be negative")
            total -= joint

    return min(1.0, max(0.0, total))

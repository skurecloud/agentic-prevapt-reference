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


def pairwise_corrected_score(
    probabilities: Mapping[str, float],
    impacts: Mapping[str, float],
    pairwise_joints: Mapping[tuple[str, str], float],
) -> float:
    """Apply a documented second-order correction to path scores.

    Each path contributes ``P(A_i) * I(A_i)``.  A supplied pairwise joint
    probability is subtracted once using the smaller of the two impacts.  The
    smaller-impact rule avoids claiming loss above either shared path's impact;
    it is still an approximation and is not used unless joint inputs are
    explicitly supplied.
    """

    if probabilities.keys() != impacts.keys():
        raise ValueError("probabilities and impacts must contain the same path ids")

    total = 0.0
    for path_id, probability in probabilities.items():
        if not 0.0 <= probability <= 1.0:
            raise ValueError("probabilities must be in [0, 1]")
        if impacts[path_id] < 0.0:
            raise ValueError("impacts cannot be negative")
        total += probability * impacts[path_id]

    ids = list(probabilities)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            left, right = ids[i], ids[j]
            joint = pairwise_joints.get(
                (left, right), pairwise_joints.get((right, left), 0.0)
            )
            if not 0.0 <= joint <= min(probabilities[left], probabilities[right]):
                raise ValueError(
                    "joint probability must be in [0, min(P(A_i), P(A_j))]"
                )
            total -= joint * min(impacts[left], impacts[right])

    return max(0.0, total)

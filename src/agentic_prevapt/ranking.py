from __future__ import annotations

from math import sqrt
from typing import Mapping


def kendall_tau_b(left: Mapping[str, float], right: Mapping[str, float]) -> float:
    """Return Kendall's tau-b for two score mappings with identical keys."""

    if left.keys() != right.keys():
        raise ValueError("rankings must contain identical item ids")
    ids = list(left)
    if len(ids) < 2:
        raise ValueError("at least two items are required")

    concordant = discordant = ties_left = ties_right = 0
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            dl = left[ids[i]] - left[ids[j]]
            dr = right[ids[i]] - right[ids[j]]
            if dl == 0 and dr == 0:
                continue
            if dl == 0:
                ties_left += 1
            elif dr == 0:
                ties_right += 1
            elif dl * dr > 0:
                concordant += 1
            else:
                discordant += 1

    denominator = sqrt(
        (concordant + discordant + ties_left)
        * (concordant + discordant + ties_right)
    )
    if denominator == 0:
        raise ValueError("tau-b is undefined for constant rankings")
    return (concordant - discordant) / denominator

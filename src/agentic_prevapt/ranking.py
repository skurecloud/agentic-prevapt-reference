from __future__ import annotations

from math import factorial, sqrt
from random import Random
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


def stratified_kendall_tau_b(
    left: Mapping[str, float], right: Mapping[str, float], strata: Mapping[str, object]
) -> float:
    """Return tau-b using only pairs belonging to the same stratum."""
    if left.keys() != right.keys() or left.keys() != strata.keys():
        raise ValueError("rankings and strata must contain identical item ids")
    ids = list(left)
    concordant = discordant = ties_left = ties_right = 0
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if strata[ids[i]] != strata[ids[j]]:
                continue
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
    denominator = sqrt((concordant + discordant + ties_left) * (concordant + discordant + ties_right))
    if denominator == 0:
        raise ValueError("stratified tau-b is undefined")
    return (concordant - discordant) / denominator


def kendall_tau_exact_pvalue(left: Mapping[str, float], right: Mapping[str, float]) -> float:
    """Exact two-sided permutation p-value for untied Kendall rankings."""
    if left.keys() != right.keys():
        raise ValueError("rankings must contain identical item ids")
    ids = sorted(left, key=left.get)
    if len(set(left.values())) != len(ids) or len(set(right.values())) != len(ids):
        raise ValueError("exact p-value currently requires untied rankings")
    ranks = {item: rank for rank, item in enumerate(sorted(ids, key=right.get))}
    permutation = [ranks[item] for item in ids]
    inversions = sum(permutation[i] > permutation[j] for i in range(len(ids)) for j in range(i + 1, len(ids)))
    counts = [1]
    for size in range(1, len(ids) + 1):
        updated = [0] * (len(counts) + size - 1)
        for prior, count in enumerate(counts):
            for added in range(size):
                updated[prior + added] += count
        counts = updated
    pairs = len(ids) * (len(ids) - 1) // 2
    distance = abs(pairs - 2 * inversions)
    extreme = sum(count for inv, count in enumerate(counts) if abs(pairs - 2 * inv) >= distance)
    return extreme / factorial(len(ids))


def kendall_tau_permutation_pvalue(
    left: Mapping[str, float], right: Mapping[str, float], *, permutations: int = 20000, seed: int = 20260901
) -> float:
    """Deterministic Monte Carlo two-sided p-value, including tied rankings."""
    if permutations <= 0:
        raise ValueError("permutations must be positive")
    observed = abs(kendall_tau_b(left, right))
    ids, values = list(right), list(right.values())
    random = Random(seed)
    extreme = 0
    for _ in range(permutations):
        random.shuffle(values)
        permuted = dict(zip(ids, values))
        if abs(kendall_tau_b(left, permuted)) >= observed - 1e-12:
            extreme += 1
    return (extreme + 1) / (permutations + 1)

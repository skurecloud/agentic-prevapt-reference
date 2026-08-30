from __future__ import annotations


def bayesian_update(
    prior: float,
    likelihood_if_path: float,
    evidence_probability: float,
) -> float:
    """Return P(A|E) = P(E|A)P(A)/P(E)."""

    for name, value in {
        "prior": prior,
        "likelihood_if_path": likelihood_if_path,
        "evidence_probability": evidence_probability,
    }.items():
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be in [0, 1], got {value}")

    if evidence_probability == 0.0:
        raise ValueError("evidence_probability must be > 0")

    posterior = likelihood_if_path * prior / evidence_probability

    # A posterior above 1 signals inconsistent caller-supplied probabilities.
    if posterior > 1.0 + 1e-12:
        raise ValueError(
            "Inconsistent probabilities: Bayes update produced posterior > 1."
        )

    return min(1.0, posterior)

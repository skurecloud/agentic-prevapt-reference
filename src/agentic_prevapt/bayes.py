from __future__ import annotations


def bayesian_update(
    prior: float,
    likelihood_if_path: float,
    likelihood_if_no_path: float,
) -> float:
    """Return P(A|E) with the evidence marginal computed internally."""

    for name, value in {
        "prior": prior,
        "likelihood_if_path": likelihood_if_path,
        "likelihood_if_no_path": likelihood_if_no_path,
    }.items():
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be in [0, 1], got {value}")

    evidence_probability = (
        likelihood_if_path * prior
        + likelihood_if_no_path * (1.0 - prior)
    )
    if evidence_probability == 0.0:
        raise ValueError("evidence has zero probability under both hypotheses")
    return likelihood_if_path * prior / evidence_probability

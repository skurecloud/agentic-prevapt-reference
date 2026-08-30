import pytest
from agentic_prevapt.bayes import bayesian_update


def test_bayes_update():
    posterior = bayesian_update(0.2, 0.6, 0.3)
    assert abs(posterior - 0.4) < 1e-12


def test_rejects_inconsistent_probabilities():
    with pytest.raises(ValueError):
        bayesian_update(0.9, 0.9, 0.2)

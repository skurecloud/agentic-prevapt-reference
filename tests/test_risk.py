from agentic_prevapt.risk import RiskModel, StepFeatures, ImpactFeatures, AttackPath


def test_sigmoid_is_bounded():
    model = RiskModel()
    assert 0 < model.sigmoid(-10) < 1
    assert 0 < model.sigmoid(10) < 1


def test_path_probability_multiplies_conditionals():
    model = RiskModel()
    first = StepFeatures(0.5, 0.5, 0.5, 0.5)
    second = StepFeatures(0.5, 0.5, 0.5, 0.5, conditional_probability=0.5)
    path = AttackPath(
        "p1",
        (first, second),
        ImpactFeatures(5, 5, 5),
    )
    expected = model.step_probability(first) * 0.5
    assert abs(model.path_probability(path) - expected) < 1e-12


def test_later_step_requires_conditional_probability():
    import pytest

    model = RiskModel()
    step = StepFeatures(0.5, 0.5, 0.5, 0.5)
    path = AttackPath("missing-conditional", (step, step), ImpactFeatures(5, 5, 5))
    with pytest.raises(ValueError, match="conditional_probability"):
        model.path_probability(path)


def test_impact_default_weights_sum_correctly():
    model = RiskModel()
    impact = ImpactFeatures(10, 10, 10)
    assert model.impact(impact) == 10


def test_normalization_increases_with_risk():
    model = RiskModel()
    assert model.normalize(2) < model.normalize(4)

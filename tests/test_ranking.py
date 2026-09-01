from agentic_prevapt.ranking import kendall_tau_b


def test_kendall_tau_b_perfect_agreement():
    left = {"a": 3.0, "b": 2.0, "c": 1.0}
    right = {"a": 30.0, "b": 20.0, "c": 10.0}
    assert kendall_tau_b(left, right) == 1.0

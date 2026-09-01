from agentic_prevapt.ranking import kendall_tau_b, kendall_tau_exact_pvalue, stratified_kendall_tau_b


def test_kendall_tau_b_perfect_agreement():
    left = {"a": 3.0, "b": 2.0, "c": 1.0}
    right = {"a": 30.0, "b": 20.0, "c": 10.0}
    assert kendall_tau_b(left, right) == 1.0


def test_exact_pvalue_matches_six_path_review_check():
    left = {str(i): value for i, value in enumerate([1.583, 1.467, 1.408, 1.359, 1.348, 0.830])}
    right = {str(i): value for i, value in enumerate([7.8, 7.5, 8.4, 8.8, 8.1, 9.1])}
    assert round(kendall_tau_exact_pvalue(left, right), 3) == 0.136


def test_stratified_tau_uses_only_within_group_pairs():
    left = {"a": 1.0, "b": 2.0, "c": 10.0, "d": 9.0}
    right = {"a": 1.0, "b": 2.0, "c": 3.0, "d": 4.0}
    strata = {"a": 1, "b": 1, "c": 2, "d": 2}
    assert stratified_kendall_tau_b(left, right, strata) == 0.0

from agentic_prevapt.overlap import PathEvent, union_probability_two, pairwise_corrected_union


def test_two_event_union():
    a = PathEvent("a", 0.4)
    b = PathEvent("b", 0.3)
    assert abs(union_probability_two(a, b, 0.1) - 0.6) < 1e-12


def test_pairwise_corrected_union():
    events = [PathEvent("a", 0.4), PathEvent("b", 0.3), PathEvent("c", 0.2)]
    joints = {("a", "b"): 0.1, ("b", "c"): 0.05}
    assert abs(pairwise_corrected_union(events, joints) - 0.75) < 1e-12

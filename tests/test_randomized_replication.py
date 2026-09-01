from experiments.randomized_replication import run


def test_randomized_replication_is_seeded_and_complete():
    rows_a, summary_a = run(seed=7, replications=3)
    rows_b, summary_b = run(seed=7, replications=3)
    assert rows_a == rows_b
    assert summary_a == summary_b
    assert len(rows_a) == 3
    assert summary_a["paths_per_replication"] == 30

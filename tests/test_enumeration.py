from agentic_prevapt.enumeration import enumerate_candidate_paths
from agentic_prevapt.graph import SecurityKnowledgeGraph


def test_enumeration_is_bounded_and_cycle_free():
    graph = SecurityKnowledgeGraph()
    for node in ("internet", "api", "role", "db"):
        graph.add_node(node, "resource")
    graph.add_edge("internet", "api", "exposes")
    graph.add_edge("api", "role", "assumes")
    graph.add_edge("role", "db", "accesses")
    graph.add_edge("role", "api", "cycle")
    paths = enumerate_candidate_paths(
        graph, {"internet"}, {"db"}, max_depth=4, top_k=10
    )
    assert [path.nodes for path in paths] == [("internet", "api", "role", "db")]


def test_enumeration_requires_priority_when_truncating():
    graph = SecurityKnowledgeGraph()
    for node in ("s", "short", "long", "mid", "t"):
        graph.add_node(node, "resource")
    graph.add_edge("s", "short", "edge")
    graph.add_edge("short", "t", "edge")
    graph.add_edge("s", "long", "edge")
    graph.add_edge("long", "mid", "edge")
    graph.add_edge("mid", "t", "edge")
    try:
        enumerate_candidate_paths(graph, {"s"}, {"t"}, top_k=1)
    except ValueError as error:
        assert "path_priority" in str(error)
    else:
        raise AssertionError("expected explicit priority requirement")
    paths = enumerate_candidate_paths(
        graph, {"s"}, {"t"}, top_k=1,
        path_priority=lambda path: len(path.relations),
    )
    assert paths[0].nodes == ("s", "long", "mid", "t")

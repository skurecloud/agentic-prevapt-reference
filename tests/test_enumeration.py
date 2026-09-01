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

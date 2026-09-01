from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .graph import Edge, SecurityKnowledgeGraph


@dataclass(frozen=True)
class EnumeratedPath:
    nodes: tuple[str, ...]
    relations: tuple[str, ...]


def enumerate_candidate_paths(
    graph: SecurityKnowledgeGraph,
    sources: set[str],
    targets: set[str],
    *,
    max_depth: int = 6,
    top_k: int = 20,
    edge_is_feasible: Callable[[Edge], bool] | None = None,
) -> list[EnumeratedPath]:
    """Enumerate bounded simple paths with deterministic depth-first search.

    Cycles are forbidden, paths longer than ``max_depth`` edges are pruned,
    and only edges accepted by ``edge_is_feasible`` are traversed. Results are
    ordered by path length and lexical node order, then truncated to ``top_k``.
    Worst-case time is O(b**d), where b is branching factor and d=max_depth.
    """

    if max_depth <= 0 or top_k <= 0:
        raise ValueError("max_depth and top_k must be positive")
    feasible = edge_is_feasible or (lambda edge: True)
    results: list[EnumeratedPath] = []

    def visit(node: str, nodes: tuple[str, ...], relations: tuple[str, ...]) -> None:
        if node in targets and len(nodes) > 1:
            results.append(EnumeratedPath(nodes, relations))
            return
        if len(relations) >= max_depth:
            return
        for edge in sorted(
            graph.outgoing(node), key=lambda item: (item.target, item.relation)
        ):
            if edge.target in nodes or not feasible(edge):
                continue
            visit(
                edge.target,
                nodes + (edge.target,),
                relations + (edge.relation,),
            )

    for source in sorted(sources):
        if source not in graph.nodes:
            raise KeyError(f"unknown source node: {source}")
        visit(source, (source,), ())

    results.sort(key=lambda path: (len(path.relations), path.nodes, path.relations))
    return results[:top_k]

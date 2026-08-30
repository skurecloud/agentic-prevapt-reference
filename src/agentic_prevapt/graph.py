from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
    id: str
    label: str
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class Edge:
    source: str
    target: str
    relation: str
    properties: dict[str, Any] = field(default_factory=dict)


class SecurityKnowledgeGraph:
    """Minimal labeled-property graph used for reproducible experiments."""

    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []

    def add_node(self, node_id: str, label: str, **properties: Any) -> None:
        self.nodes[node_id] = Node(node_id, label, dict(properties))

    def add_edge(
        self,
        source: str,
        target: str,
        relation: str,
        **properties: Any,
    ) -> None:
        if source not in self.nodes or target not in self.nodes:
            raise KeyError("source and target must exist before adding an edge")
        self.edges.append(Edge(source, target, relation, dict(properties)))

    def outgoing(self, node_id: str) -> list[Edge]:
        return [edge for edge in self.edges if edge.source == node_id]

    def incoming(self, node_id: str) -> list[Edge]:
        return [edge for edge in self.edges if edge.target == node_id]

    def evidence_for(self, node_id: str) -> dict[str, Any]:
        return dict(self.nodes[node_id].properties)

__all__ = []

from dataclasses import dataclass
from typing import Callable


@dataclass
class Node:
    edges: list["Node"]

@dataclass
class Graph:
    nodes: list[Node]


def bfs(graph: Graph, key: Callable):
    raise NotImplementedError()

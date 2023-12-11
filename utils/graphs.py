__all__ = ["AdjacencyListType", "topological_sort"]

from collections.abc import Callable, Hashable

AdjacencyListType = dict[Hashable, list[Hashable]] | list[list[int]]


def densify_keys(adj_list: dict[Hashable, list[Hashable]]) -> tuple[list[list[int]], list, dict]:
    """
    Replaces an adjacency list with arbitrary nodes with one using only ints

    Returns a new adjacency list, a conversion from int to node, and a conversion from node to int
    :param adj_list:
    :return:
    """
    itoa = sorted(adj_list.keys())
    atoi = {val: idx for idx, val in enumerate(itoa)}
    new_adj_list: AdjacencyListType = {k: [] for k in range(len(itoa))}
    for key, neighbors in adj_list.items():
        i = atoi[key]
        new_neighbors = list(map(lambda x: atoi[x], neighbors))
        new_adj_list[i] = new_neighbors
    return new_adj_list, itoa, atoi


def topological_sort(adj_list: AdjacencyListType) -> list[int]:
    visited = set()
    stack = []

    def _top_sort_helper(v: Hashable):
        visited.add(v)
        for neighbor in adj_list.get(v, []):
            if neighbor not in visited:
                _top_sort_helper(neighbor)
        stack.append(v)

    for key in adj_list:
        if key not in visited:
            _top_sort_helper(key)

    return stack[::-1]


def bfs(graph: AdjacencyListType, key: Callable):
    raise NotImplementedError()


def reverse_edges(adj_list: AdjacencyListType) -> AdjacencyListType:
    """
    Reverses the edges in an adjacency list graph
    """
    new_adj_list = {k: [] for k in adj_list}
    for node, neighbors in adj_list.items():
        for neighbor in neighbors:
            new_adj_list[neighbor].append(node)
    return new_adj_list

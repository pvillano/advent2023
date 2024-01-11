import random
from collections import defaultdict

from utils import benchmark, get_day, test
from utils.graphs import densify_keys


def parse(raw: str):
    ret = dict()
    for line in raw.splitlines():
        key, values = line.split(': ')
        values = values.split(' ')
        ret[key] = values
    return ret


def find_set(u, forest):
    while forest[u] != u:
        u, forest[u] = forest[u], forest[forest[u]]
    return u


def union_set(u, v, forest, sizes):
    u = find_set(u, forest)
    v = find_set(v, forest)
    if u == v:
        return
    if sizes[u] < sizes[v]:
        u, v = v, u
    assert sizes[u] >= sizes[v]
    forest[v] = u  # u is new root
    sizes[u] += sizes[v]


def run_iter(new_adj_list, weight_sorted_edges):
    forest = list(range(len(new_adj_list)))
    sizes = [1] * len(new_adj_list)
    for i, (u, v) in enumerate(weight_sorted_edges):
        u = find_set(u, forest)
        v = find_set(v, forest)
        if u != v:
            if sizes[u] + sizes[v] == len(sizes):
                return len(weight_sorted_edges) - i, sizes[u] * sizes[v]
            union_set(u, v, forest, sizes)


def part1(raw: str):
    lines = parse(raw)
    bidir_str_graph = {key: set(value) for key, value in lines.items()}
    bidir_str_graph = defaultdict(set, bidir_str_graph)
    for key, values in lines.items():
        for value in values:
            bidir_str_graph[value].add(key)
    new_adj_list, _, _ = densify_keys(bidir_str_graph)
    del bidir_str_graph, lines
    weight_sorted_edges = []
    for key, values in enumerate(new_adj_list):
        for value in values:
            if key < value:
                weight_sorted_edges.append((key, value))
    best = (len(weight_sorted_edges), 0)
    while True:
        random.shuffle(weight_sorted_edges)
        candidate = run_iter(new_adj_list, weight_sorted_edges)
        if candidate < best:
            best = candidate
            print(best)
            count, product = candidate
            if count == 3:
                return product


def part2(raw: str):
    lines = parse(raw)


test1 = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""

expected1 = 54

test2 = test1
expected2 = None


def main():
    test(part1, test1, expected1)
    raw = get_day(25, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

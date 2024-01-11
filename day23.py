import sys
from collections import defaultdict

from utils import benchmark, get_day, test, debug_print
from utils.grids import NEWS_RC


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(line)
    return ret


def part1(raw: str):
    lines = parse(raw)
    n_rows = len(lines)
    n_cols = len(lines[0])
    start = (0, 1)
    assert lines[start[0]][start[1]] == "."
    end = (n_rows - 1, n_cols - 2)
    assert lines[end[0]][end[1]] == "."
    critical = set()
    as_graph = defaultdict(list)
    for row in range(n_rows):
        for col in range(n_cols):
            if lines[row][col] == "#":
                continue
            if lines[row][col] in "^<>v":
                for dr, dc in NEWS_RC:
                    if (lines[row][col], (dr, dc)) in zip("^><v", NEWS_RC):
                        r2, c2 = row + dr, col + dc
                        as_graph[(row, col)] = [(r2, c2)]
                        break
                continue
            for dr, dc in NEWS_RC:
                r2, c2 = row + dr, col + dc
                if r2 not in range(n_rows) or c2 not in range(n_cols):
                    continue
                ch = lines[r2][c2]
                if ch == "#":
                    continue
                as_graph[(row, col)].append((r2, c2))
    stack = []
    sys.setrecursionlimit(15000)
    best = 0

    def recurse(node):
        stack.append(node)
        for next_node in as_graph[node]:
            if next_node != stack[-1] and next_node not in stack:
                if next_node == end:
                    assert len(stack) == len(set(stack))
                    # debug_print_sparse_grid(stack, transpose=True)
                    yield len(stack)
                else:
                    yield from recurse(next_node)
        stack.pop()

    for path in recurse(start):
        debug_print(path, stack)
        best = max(best, path)
    # assert not best == XXXX
    return best


def part2(raw: str):
    lines = parse(raw)
    n_rows = len(lines)
    n_cols = len(lines[0])
    start = (0, 1)
    end = (n_rows - 1, n_cols - 2)
    critical = {start, end}
    # generate list of critical nodes
    for r in range(n_rows):
        for c in range(n_cols):
            if lines[r][c] == "#":
                continue
            num_neighbours = 0
            for dr2, dc in NEWS_RC:
                r2, c2 = r + dr2, c + dc
                if r2 not in range(n_rows) or c2 not in range(n_cols):
                    continue
                ch = lines[r2][c2]
                if ch != "#":
                    num_neighbours += 1
            if num_neighbours > 2:
                critical.add((r, c))

    # generate graph
    as_graph = dict()
    for r, c in critical:
        neighbours = dict()
        for dr, dc in NEWS_RC:
            ri, ci = r + dr, c + dc
            if ri not in range(n_rows) or ci not in range(n_cols):
                continue
            if lines[ri][ci] == "#":
                continue
            prev = r, c
            d = 1
            while (ri, ci) not in critical:
                for dr2, dc2 in NEWS_RC:
                    ri2, ci2 = ri + dr2, ci + dc2
                    if ri2 not in range(n_rows) or ci2 not in range(n_cols):
                        continue
                    if lines[ri2][ci2] == "#":
                        continue
                    if (ri2, ci2) == prev:
                        continue
                    prev = (ri, ci)
                    ri, ci = ri2, ci2
                    d += 1
                    break
            neighbours[(ri, ci)] = d
        as_graph[(r, c)] = neighbours

    # # verify reciprocity
    # for node, neighbours in as_graph.items():
    #     for neighbour, distance in neighbours.items():
    #         assert distance == as_graph[neighbour][node]

    stack = []
    length = [0]
    best = 0

    def recurse(node):
        stack.append(node)
        for next_node, step_size in as_graph[node].items():
            length[0] += step_size
            if next_node != stack[-1] and next_node not in stack:
                if next_node == end:
                    assert len(stack) == len(set(stack))
                    # debug_print_sparse_grid(stack, transpose=True)
                    yield length[0]
                else:
                    yield from recurse(next_node)
            length[0] -= step_size
        stack.pop()

    for path in recurse(start):
        debug_print(path, stack)
        best = max(best, path)
    return best


test1 = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

expected1 = 94

test2 = test1
expected2 = 154


def main():
    test(part1, test1, expected1)
    raw = get_day(23, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

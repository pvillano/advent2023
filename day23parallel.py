import sys
from collections import defaultdict

import trio
import trio_parallel

from utils import benchmark, get_day, test, debug_print
from utils.grids import NEWS_RC


def parse1(raw: str):
    lines = raw.splitlines()
    n_rows = len(lines)
    n_cols = len(lines[0])
    start = (0, 1)
    assert lines[start[0]][start[1]] == "."
    end = (n_rows - 1, n_cols - 2)
    assert lines[end[0]][end[1]] == "."
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
    return start, as_graph, end

def recurse1(node, stack, as_graph, end):
    sys.setrecursionlimit(15000)

    stack.append(node)
    best = 0
    for next_node in as_graph[node]:
        if next_node != stack[-1] and next_node not in stack:
            if next_node == end:
                # assert len(stack) == len(set(stack))
                # debug_print_sparse_grid(stack, transpose=True)
                best = max(best, len(stack))
            else:
                best = max(best, recurse1(next_node, stack, as_graph, end))
    stack.pop()
    return best

def part1(raw: str):
    sys.setrecursionlimit(15000)

    start, as_graph, end = parse1(raw)
    heads = []
    starting_stack_depth = 899
    sss = []
    def starting_stacks(node):
        sss.append(node)
        for next_node in as_graph[node]:
            if next_node != sss[-1] and next_node not in sss:
                if len(sss) == starting_stack_depth or next_node == end:
                    heads.append(list(sss))
                else:
                    starting_stacks(next_node)
        sss.pop()
    starting_stacks(start)
    # pprint([len(heads), heads])


    results = [0] * len(heads)

    async def worker(j, stack):
        results[j] = await trio_parallel.run_sync(recurse1, stack[-1], stack[:-1], as_graph, end)
        # print(j, "done")

    async def async_main():
        print(len(heads), "workers")
        async with trio.open_nursery() as nursery:
            for idx, stack in enumerate(heads):
                nursery.start_soon(worker, idx, stack)
        # all threads joined
        print(results)
        return max(results)

    return trio.run(async_main)

def parse2(raw: str):
    lines = raw.splitlines()
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

    return start, as_graph, end


def recurse2(node, stack, as_graph, end, length_so_far):
    best = 0
    stack.append(node)
    for next_node, step_size in as_graph[node].items():
        length_so_far += step_size
        if next_node != stack[-1] and next_node not in stack:
            if next_node == end:
                # debug_print_sparse_grid(stack, transpose=True)
                best = max(best, length_so_far)
            else:
                best = max(best, recurse2(next_node, stack, as_graph, end, length_so_far))
        length_so_far -= step_size
    stack.pop()
    return best

def part2(raw: str):
    sys.setrecursionlimit(15000)

    start, as_graph, end = parse2(raw)
    heads = []
    head_lengths = []
    starting_stack_depth = 10
    sss = []
    def starting_stacks(node, length_so_far):
        sss.append(node)
        for next_node, step_size in as_graph[node].items():
            length_so_far += step_size
            if next_node != sss[-1] and next_node not in sss:
                # assert len(sss) == len(set(sss))
                if len(sss) == starting_stack_depth or next_node == end:
                    heads.append(list(sss))
                    head_lengths.append(length_so_far - step_size)
                else:
                    starting_stacks(next_node, length_so_far)
            length_so_far -= step_size
        sss.pop()
    starting_stacks(start, 0)
    results = [0] * len(heads)

    async def worker(j, stack, lsf):
        results[j] = await trio_parallel.run_sync(recurse2, stack[-1], stack[:-1], as_graph, end, lsf)
        # print(j, "done")

    async def async_main():
        print(len(heads), "workers")
        async with trio.open_nursery() as nursery:
            for idx, stack in enumerate(heads):
                nursery.start_soon(worker, idx, stack, head_lengths[idx])
        # all threads joined
        print(results)
        return max(results)

    return trio.run(async_main)


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
    raw = get_day(23, override=True)
    # test(part1, test1, expected1)
    # benchmark(part1, raw)
    # test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

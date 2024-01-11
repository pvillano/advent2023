from collections import defaultdict, Counter

from utils import benchmark, get_day, test, debug_print_grid, debug_print_sparse_grid
from utils.graphs import topological_sort, reverse_edges
from utils.grids import NEWS_RC


Counter


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(line)
    return ret


def part1(raw: str):

    lines = parse(raw)
    n_rows = len(lines)
    n_cols = len(lines[0])
    start = (0,1)
    end = (n_rows-1, n_cols-2)
    critical = set()
    as_graph = defaultdict(list)
    for row in range(n_rows):
        for col in range(n_cols):
            if lines[row][col] == "#":
                continue
            if lines[row][col] in "^<>v":
                for dr, dc in NEWS_RC:
                    if (lines[row][col], (dr, dc)) in zip("^><v", NEWS_RC):
                        r2, c2 = row+dr, col+dc
                        as_graph[(row,col)] = [(r2, c2)]
                        break
                continue
            for dr, dc in NEWS_RC:
                r2, c2 = row+dr, col+dc
                if r2 not in range(n_rows) or c2 not in range(n_cols):
                    continue
                ch = lines[r2][c2]
                if ch == "#":
                    continue
                if ch == ".":
                    as_graph[(row, col)].append((r2, c2))
                    continue
                if (ch, (dr, dc)) in zip("v<>^", NEWS_RC):
                    continue
                as_graph[(row, col)].append((r2, c2))
    preds = reverse_edges(as_graph)
    longest_ending_at = defaultdict(int)
    for v in topological_sort(as_graph):
        longest_ending_at[v] = max(longest_ending_at[v2] for v2 in preds[v]) + 1
    debug_print_sparse_grid(longest_ending_at, transpose=True)
    return longest_ending_at[end]




def part2(raw: str):
    lines = parse(raw)


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
expected2 = None


def main():
    test(part1, test1, expected1)
    raw = get_day(23, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

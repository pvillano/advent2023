from collections import deque, defaultdict

import numpy as np

from utils import benchmark, get_day, test, debug_print
from utils.grids import NEWS_RC


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(line)
    return ret


def find_s(lines):
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == "S":
                return r, c


def part1(raw: str):
    max_steps = 6 if raw == test1 else 64
    grid = parse(raw)
    n_rows = len(grid)
    n_cols = len(grid[0])
    d_origin = np.full((n_rows, n_cols), dtype=int, fill_value=-1)

    s_r, s_c = find_s(grid)
    d_origin[s_r, s_c] = 0
    q = deque([(s_r, s_c, 0)])
    while q:
        r, c, steps = q.pop()
        if steps >= max_steps:
            continue
        drc = d_origin[r, c]
        if drc >= 64:
            continue
        for dr, dc in NEWS_RC:
            r2, c2 = r + dr, c + dc
            if r2 not in range(n_rows) or c2 not in range(n_cols):
                continue
            if grid[r2][c2] == "#":
                continue
            if d_origin[r2][c2] != -1:
                continue
            d_origin[r2, c2] = d_origin[r, c] + 1
            q.appendleft((r2, c2, steps + 1))

    return ((d_origin % 2) == 0).sum()


def part2(raw: str):
    max_steps = 5000 if raw == test1 else 26501365
    grid = parse(raw)
    n_rows = len(grid)
    n_cols = len(grid[0])
    d_origin = np.full((n_rows, n_cols), dtype=int, fill_value=-1)

    pred = dict()
    succ = defaultdict(list)

    s_r, s_c = find_s(grid)
    d_origin[s_r, s_c] = 0
    q = deque([(s_r, s_c, 0)])
    while q:
        r, c, steps = q.pop()
        for dr, dc in NEWS_RC:
            r2, c2 = (r + dr) % n_rows, (c + dc) % n_cols
            if grid[r2][c2] == "#":
                continue
            if d_origin[r2][c2] != -1:
                continue
            d_origin[r2, c2] = d_origin[r, c] + 1
            pred[(r2, c2)] = (r, c)
            succ[(r, c)].append((r2, c2))
            q.appendleft((r2, c2, steps + 1))
    seen = np.zeros((n_rows, n_cols), dtype=int)
    seen[s_r, s_c] = 1
    for i in range(max_steps):
        next_seen = np.zeros((n_rows, n_cols), dtype=int)
        for (r2, c2), (r, c) in pred.items():
            next_seen[r2, c2] += seen[r, c]
        seen = next_seen
        if i in [6, 10, 50, 100, 500, 1000]:
            debug_print(seen.sum())
    return seen.sum()


test1 = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

expected1 = 16

test2 = test1
expected2 = 16733044


def main():
    test(part1, test1, expected1)
    raw = get_day(21, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

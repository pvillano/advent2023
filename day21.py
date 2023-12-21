from collections import deque, Counter
from functools import cache
from itertools import product

import numpy as np

from utils import benchmark, get_day, test
from utils.grids import NEWS_RC
from utils.otqdm import otqdm


@cache
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


RC_NEWS = {k: v for v, k in enumerate(NEWS_RC)}


# def step(raw, center: np.ndarray, neighbourhood: list[np.ndarray]) -> np.ndarray:
#     grid = parse(raw)
#     n_rows, n_cols = len(grid), len(grid[0])
#     x = _step(raw, center.tobytes(), tuple(n.tobytes() for n in neighbourhood))
#     return np.frombuffer(x, dtype=bool).reshape((n_rows, n_cols))


@cache
def _step(raw, center: bytes, neighbourhood: tuple[bytes]) -> bytes:
    grid = parse(raw)
    n_rows, n_cols = len(grid), len(grid[0])
    center = np.frombuffer(center, dtype=bool).reshape((n_rows, n_cols))
    neighbourhood = [np.frombuffer(n, dtype=bool).reshape((n_rows, n_cols)) for n in neighbourhood]
    out = np.zeros_like(center)

    for r, c in product(range(n_rows), range(n_cols)):
        if grid[r][c] == "#":
            continue
        for dr, dc in NEWS_RC:
            r2, c2 = r + dr, c + dc
            if grid[r2 % n_rows][c2 % n_cols] == "#":
                continue
            if r2 in range(n_rows) and c2 in range(n_cols):
                neighbour = center[r2, c2]
            else:
                if r2 == -1:
                    r2 = n_rows - 1
                    from_block = neighbourhood[RC_NEWS[(-1, 0)]]
                elif r2 == n_rows:
                    r2 = 0
                    from_block = neighbourhood[RC_NEWS[(1, 0)]]
                elif c2 == -1:
                    c2 = n_cols - 1
                    from_block = neighbourhood[RC_NEWS[(0, -1)]]
                elif c2 == n_cols:
                    c2 = 0
                    from_block = neighbourhood[RC_NEWS[(0, 1)]]
                else:
                    assert False
                neighbour = from_block[r2, c2]
            if neighbour:
                out[r, c] = True
                break
    out.setflags(write=False)
    return out.tobytes()


def part2(raw: str):
    max_steps = 5000 if raw == test1 else 26501365
    grid = parse(raw)
    n_rows = len(grid)
    n_cols = len(grid[0])
    zeros = np.zeros((n_rows, n_cols), dtype=bool)
    zeros.setflags(write=False)
    zeros = zeros.tobytes()
    # hashlife = dict()

    cachelife = Counter()

    initial = np.zeros((n_rows, n_cols), dtype=bool)
    s_r, s_c = find_s(grid)
    initial[s_r, s_c] = True
    initial.setflags(write=False)
    cachelife[(initial.tobytes(), tuple([zeros] * 4))] = 1

    for i in otqdm(range(1, max_steps + 1)):
        next_cachelife = Counter()
        for (block, neighbours), count in cachelife.items():
            direct_desc = _step(raw, block, neighbours)
            next_cachelife[direct_desc] += count
            for n_idx, neighbour in enumerate(neighbours):
                if neighbour != zeros:
                    continue
        cachelife = next_cachelife

        # if i in [6, 10, 50, 100, 500, 1000, 5000]:
        alive = sum(np.frombuffer(v[0], dtype=bool).sum() * cnt for v, cnt in cachelife.items())
        print(f"{i=} {len(cachelife)=} {alive=} {_step.cache_info()}")
        # debug_print_grid(hashlife[(0,0)])
    alive = sum(np.frombuffer(v[0], dtype=bool).sum() * cnt for v, cnt in cachelife.items())
    return alive


def explore_me(keys):
    for r, c in keys:
        yield r, c
        for dr, dc in NEWS_RC:
            r2, c2 = r + dr, c + dc
            yield r2, c2


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
expected2 = 167004


def main():
    # test(part1, test1, expected1)
    raw = get_day(21, override=True)
    # benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

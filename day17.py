from collections import deque

import numpy as np

from utils import benchmark, get_day, test, debug_print, debug_print_grid
from utils.grids import NEWS_RC

test1 = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

expected1 = 102

test2 = test1
expected2 = 94

test22 = """111111111111
999999999991
999999999991
999999999991
999999999991"""
expected22 = 71


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(list(map(int, line)))
    return ret


def part1(raw: str):
    grid = parse(raw)
    row_count = len(grid)
    col_count = len(grid[0])
    seen = np.full((row_count, col_count, 3, 3, 4), np.iinfo(int).max)
    seen[0, 0, :, :, :] = 0
    q = deque([(0, 0, 0, 0, 0)])

    while q:
        r, c, dr, dc, t = q.pop()
        d = seen[r, c, dr, dc, t]
        assert 0 <= d < np.iinfo(int).max
        for next_dr, next_dc in NEWS_RC:
            if next_dr == -dr and next_dc == -dc:
                continue
            if next_dr == dr and next_dc == dc:
                if t == 3:
                    continue
                t2 = t + 1
            else:
                t2 = 1
            r2, c2 = r + next_dr, c + next_dc
            if r2 not in range(row_count) or c2 not in range(col_count):
                continue
            d2 = d + grid[r2][c2]
            # if d2 >= worst:
            #     continue
            # if r2 == row_count - 1 and c2 == col_count - 1:
            #     worst = min(worst, d2)
            best = seen[r2, c2, next_dr, next_dc, t2]
            if d2 < best:
                seen[r2, c2, next_dr, next_dc, t2] = d2
                q.appendleft((r2, c2, next_dr, next_dc, t2))

    return seen[-1, -1, :, :, :].min()


# Completed in 369.942 seconds. kek


def part2(raw: str):
    grid = parse(raw)
    row_count = len(grid)
    col_count = len(grid[0])
    seen = np.full((row_count, col_count, 3, 3, 11), np.iinfo(int).max)
    seen[0, 0, :, :, :] = 0
    q = deque([(0, 0, 0, 1, 0), (0, 0, 1, 0, 0)])

    worst = np.iinfo(int).max
    while q:
        r, c, dr, dc, t = q.pop()
        d = seen[r, c, dr, dc, t]
        assert 0 <= d < np.iinfo(int).max
        for next_dr, next_dc in NEWS_RC:
            if next_dr == -dr and next_dc == -dc:
                continue
            if next_dr == dr and next_dc == dc:
                if t >= 10:
                    continue
                t2 = t + 1
            else:
                if t < 4:
                    continue
                else:
                    t2 = 1

            r2, c2 = r + next_dr, c + next_dc
            if r2 not in range(row_count) or c2 not in range(col_count):
                continue
            d2 = d + grid[r2][c2]
            if d2 >= worst:
                continue
            if r2 == row_count - 1 and c2 == col_count - 1 and t2 >= 4:
                worst = min(worst, d2)
                print(worst, len(q))
            best = seen[r2, c2, next_dr, next_dc, t2]
            if d2 < best:
                seen[r2, c2, next_dr, next_dc, t2] = d2
                q.appendleft((r2, c2, next_dr, next_dc, t2))
    debug_print_grid(seen.min((2, 3, 4)))
    for i in range(10):
        debug_print(i, seen[-1, -1, :, :, i].min())
    return seen[-1, -1, :, :, 4:].min()


def main():
    test(part1, test1, expected1)
    raw = get_day(17, override=True)
    # benchmark(part1, raw)
    test(part2, test2, expected2)
    test(part2, test22, expected22)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

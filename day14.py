from collections import Counter

from utils import benchmark, get_day, test, debug_print_grid
from utils.grids import transpose

test1 = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

expected1 = 136

test2 = test1
expected2 = 64


def parse(raw: str):
    return raw.splitlines()


def flow_north(grid):
    grid = transpose(grid)
    grid = [list(row) for row in grid]
    for row in grid:
        for i in range(len(row)):
            if row[i] in "#.":
                continue
            while i - 1 in range(len(row)) and row[i - 1] == ".":
                row[i - 1], row[i] = row[i], row[i - 1]
                i -= 1
    return transpose(grid)


def calc_load(grid):
    load = 0
    for i, row in enumerate(grid):
        multiplier = len(grid) - i
        load += Counter(row)["O"] * multiplier
    return load


def part1(raw: str):
    grid = parse(raw)
    grid = flow_north(grid)
    return calc_load(grid)


def freeze_grid(grid):
    return tuple("".join(line) for line in grid)


def part2(raw: str):
    grid = parse(raw)
    seen_at = dict()
    for cycle in range(1, 1000000000):
        for wash in range(4):
            grid = flow_north(grid)
            grid = rotate_clockwise(grid)
        if raw == test2 and cycle < 4:
            debug_print_grid(grid)
        if freeze_grid(grid) not in seen_at:
            seen_at[freeze_grid(grid)] = cycle
            continue
        first_seen = seen_at[freeze_grid(grid)]
        period = cycle - first_seen
        remainder = (1000000000 - first_seen) % period
        target = first_seen + remainder
        for k, v in seen_at.items():
            if v != target:
                continue
            return calc_load(k)


def main():
    test(part1, test1, expected1)
    raw = get_day(14, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

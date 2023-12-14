from utils import benchmark, get_day, test, debug_print_grid
from utils.itertools2 import transpose

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
    ret = []
    for line in raw.splitlines():
        ret.append(line)
    return ret


def part1(raw: str):
    grid = transpose(parse(raw))
    grid = [list(row) for row in grid]
    for row in grid:
        for i in range(len(row)):
            if row[i] in "#.":
                continue
            while i - 1 in range(len(row)) and row[i - 1] == ".":
                row[i - 1], row[i] = row[i], row[i - 1]
                i -= 1
    grid = transpose(grid)
    debug_print_grid(grid)
    load = 0
    for i, multiplier in enumerate(reversed(range(1, len(grid) + 1))):
        for ch in grid[i]:
            if ch == "O":
                load += multiplier
    return load


def hashable(grid):
    return tuple("".join(line) for line in grid)


def part2(raw: str):
    grid = transpose(parse(raw))
    grid = [list(row) for row in grid]
    seen_at = dict()
    for cycle in range(0, 30000000000000000):
        for wash in range(4):
            for row in grid:
                for i in range(len(row)):
                    if row[i] in "#.":
                        continue
                    while i - 1 in range(len(row)) and row[i - 1] == ".":
                        row[i - 1], row[i] = row[i], row[i - 1]
                        i -= 1
            grid = transpose(grid)
            grid = [list(row) for row in grid]
            grid = list(reversed(grid))
        debug_print_grid(transpose(grid))
        if hashable(grid) not in seen_at:
            seen_at[hashable(grid)] = cycle
            continue
        first_seen = seen_at[hashable(grid)]
        period = cycle - first_seen
        remainder = (1000000000 - first_seen - 1) % period
        target = first_seen + remainder
        for k, v in seen_at.items():
            if v != target:
                continue
            return calc_load(k)


def calc_load(grid):
    load = 0
    grid = transpose(grid)
    for i, multiplier in enumerate(reversed(range(1, len(grid) + 1))):
        for ch in grid[i]:
            if ch == "O":
                load += multiplier
    return load


def main():
    # test(part1, test1, expected1)
    raw = get_day(14, override=True)
    # benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

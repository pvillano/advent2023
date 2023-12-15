from itertools import combinations

from utils import benchmark, get_day, test
from utils.grids import transpose

test1 = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

expected1 = 374

test2 = test1
expected2 = 8410


def parse(raw: str):
    return raw.splitlines()


def part1(raw: str):
    lines = parse(raw)
    lines2 = []
    for line in lines:
        if set(line) == set("."):
            lines2.append(line)
        lines2.append(line)
    lines3 = transpose(lines2)
    lines4 = []
    for line in lines3:
        if set(line) == set("."):
            lines4.append(line)
        lines4.append(line)
    stars = []
    for r, line in enumerate(lines4):
        for c, char in enumerate(line):
            if char == "#":
                stars.append((r, c))
    s = 0
    for (star1row, star1col), (star2row, star2col) in combinations(stars, 2):
        d = abs(star1row - star2row) + abs(star1col - star2col)
        s += d
    return s


def part2(raw: str):
    million = 100 if raw == test2 else 1000000
    lines = parse(raw)
    blank_rows = []
    for r, line in enumerate(lines):
        if set(line) == set("."):
            blank_rows.append(r)
    blank_cols = []
    for c, col in enumerate(transpose(lines)):
        if set(col) == set("."):
            blank_cols.append(c)
    stars = []
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == "#":
                stars.append((r, c))
    stars2 = []
    for sr, sc in stars:
        sr2 = sr + (million - 1) * sum(1 for r in blank_rows if r < sr)
        sc2 = sc + (million - 1) * sum(1 for c in blank_cols if c < sc)
        stars2.append((sr2, sc2))
    s = 0
    for (p1r, p1c), (p2r, p2c) in combinations(stars2, 2):
        d = abs(p1r - p2r) + abs(p1c - p2c)
        s += d
    return s


def main():
    test(part1, test1, expected1)
    raw = get_day(11, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

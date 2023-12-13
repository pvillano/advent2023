from collections import Counter

from utils import benchmark, get_day, test
from utils.itertools2 import transpose

test1 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

expected1 = 405

test2 = test1
expected2 = 400


def parse(raw: str):
    ret = []
    for line in raw.split("\n\n"):
        ret.append(line.splitlines())
    return ret


def candidates(line):
    for i in range(1, len(line)):
        left, right = line[:i], line[i:]
        left = left[::-1]
        if all(map(lambda x: x[0] == x[1], zip(left, right))):
            yield i


def part1(raw: str):
    s = 0
    for grid in parse(raw):
        cands = set(range(len(grid[0])))
        for line in grid:
            cands &= set(candidates(line))
        if len(cands) == 1:
            s += list(cands)[0]
            continue
        grid = transpose(grid)
        cands = set(range(len(grid[0])))
        for line in grid:
            cands &= set(candidates(line))
        if len(cands) == 1:
            s += list(cands)[0] * 100
            continue
    return s


def part2(raw: str):
    s = 0
    for grid in parse(raw):
        cands = Counter()
        for line in grid:
            for c in candidates(line):
                cands[c] += 1
        broke = False
        for second_most_common, smc_count in cands.most_common(2):
            if smc_count == len(grid) - 1:
                s += second_most_common
                broke = True
                break
        if broke:
            continue
        grid = transpose(grid)
        cands = Counter()
        for line in grid:
            for c in candidates(line):
                cands[c] += 1
        broke = False
        for second_most_common, smc_count in cands.most_common(2):
            if smc_count == len(grid) - 1:
                s += second_most_common * 100
                broke = True
                break
        if broke:
            continue
    return s


def main():
    test(part1, test1, expected1)
    raw = get_day(13, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

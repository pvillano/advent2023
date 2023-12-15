from collections import Counter

from utils import benchmark, get_day, test
from utils.grids import transpose

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


def find_candidates(line):
    for i in range(1, len(line)):
        left, right = line[:i], line[i:]
        left = left[::-1]
        if all(map(lambda x: x[0] == x[1], zip(left, right))):
            yield i


def part1(raw: str):
    s = 0
    for grid in parse(raw):
        for flipped, factor in ((grid, 1), (transpose(grid), 100)):
            candidates = set(range(1, len(flipped[0])))
            for line in flipped:
                candidates &= set(find_candidates(line))
            if len(candidates) == 1:
                s += list(candidates)[0] * factor
    return s


def part2(raw: str):
    s = 0
    for grid in parse(raw):
        for flipped, factor in ((grid, 1), (transpose(grid), 100)):
            candidates = Counter()
            for line in flipped:
                for candidate in find_candidates(line):
                    candidates[candidate] += 1
            for less_common, less_common_count in candidates.most_common(2):
                if less_common_count == len(flipped) - 1:
                    s += less_common * factor
    return s


def main():
    test(part1, test1, expected1)
    raw = get_day(13, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

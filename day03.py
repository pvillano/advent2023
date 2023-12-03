import operator
from collections import defaultdict
from functools import reduce

from utils import benchmark, get_day

test = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def parse(raw: str):
    lines = raw.split("\n")
    line: str
    for i, line in enumerate(lines):
        j = 0
        while j < len(line):
            ch = line[j]
            if ch.isnumeric():
                k = j
                while k < len(line) and line[k].isnumeric():
                    k += 1
                # k points past end line or is not numeric
                num = line[j:k]
                assert num.isnumeric()
                ispartnum = False
                for li in range(max(i - 1, 0), min(i + 2, len(lines))):
                    for lj in range(max(j - 1, 0), min(k + 1, len(line))):
                        if lines[li][lj] not in "0123456789.":
                            ispartnum = True
                if ispartnum:
                    yield int(num)
                j = k
            j += 1


def part1(raw: str):
    return sum(parse(raw))


def parse2(raw: str):
    lines = raw.split("\n")
    gears = defaultdict(list)
    line: str
    for i, line in enumerate(lines):
        j = 0
        while j < len(line):
            ch = line[j]
            if ch.isnumeric():
                k = j
                while k < len(line) and line[k].isnumeric():
                    k += 1
                # k points past end line or is not numeric
                num = line[j:k]
                assert num.isnumeric()
                for li in range(max(i - 1, 0), min(i + 2, len(lines))):
                    for lj in range(max(j - 1, 0), min(k + 1, len(line))):
                        if lines[li][lj] == "*":
                            gears[(li, lj)].append(int(num))
                j = k
            j += 1
    return gears


def part2(raw: str):
    s = 0
    for v in parse2(raw).values():
        if len(v) > 1:
            s += reduce(operator.mul, v, 1)
    return s


def main():
    raw = get_day(3, test)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

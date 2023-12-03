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


def parse1(raw: str):
    lines = raw.split("\n")
    line: str
    for line_no, line in enumerate(lines):
        num_start = 0
        while num_start < len(line):
            ch = line[num_start]
            if ch.isnumeric():
                num_end = num_start
                while num_end < len(line) and line[num_end].isnumeric():
                    num_end += 1
                num = line[num_start:num_end]
                assert num.isnumeric()
                is_part = False
                for symb_row in range(max(line_no - 1, 0), min(line_no + 2, len(lines))):
                    for symb_col in range(max(num_start - 1, 0), min(num_end + 1, len(line))):
                        if lines[symb_row][symb_col] not in "0123456789.":
                            is_part = True
                if is_part:
                    yield int(num)
                num_start = num_end
            num_start += 1


def part1(raw: str):
    return sum(parse1(raw))


def parse2(raw: str):
    lines = raw.split("\n")
    gears = defaultdict(list)
    line: str
    for line_no, line in enumerate(lines):
        num_start = 0  # inclusive
        while num_start < len(line):
            ch = line[num_start]
            if ch.isnumeric():
                num_end = num_start  # exclusive
                while num_end < len(line) and line[num_end].isnumeric():
                    num_end += 1
                num = line[num_start:num_end]
                assert num.isnumeric()
                for gear_row in range(max(line_no - 1, 0), min(line_no + 2, len(lines))):
                    for gear_col in range(max(num_start - 1, 0), min(num_end + 1, len(line))):
                        if lines[gear_row][gear_col] == "*":
                            gears[(gear_row, gear_col)].append(int(num))
                num_start = num_end
            num_start += 1
    return gears


def part2(raw: str):
    sum_gears = 0
    for v in parse2(raw).values():
        if len(v) == 2:
            sum_gears += reduce(operator.mul, v, 1)
    return sum_gears


def main():
    raw = get_day(3, test)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

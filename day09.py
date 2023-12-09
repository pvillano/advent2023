import operator as op
from itertools import starmap

from utils import benchmark, get_day, test, extract_ints

test1 = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

expected1 = 114

test2 = test1
expected2 = 2


def parse(raw: str):
    lines = raw.splitlines()
    return [list(extract_ints(line)) for line in lines]


def difference_operator(x):
    r = list(starmap(op.sub, zip(x[1:], x)))
    assert len(r) == len(x) - 1
    return r


def part1(raw: str):
    histories = parse(raw)
    s = 0
    for history in histories:
        tree = [history]
        while any(tree[-1]):
            tree.append(difference_operator(tree[-1]))
        tree = list(reversed(tree))
        for i in range(1, len(tree)):
            tree[i].append(tree[i][-1] + tree[i - 1][-1])
        s += tree[-1][-1]
    return s


def part2(raw: str):
    raw2 = "\n".join(" ".join(reversed(line.split())) for line in raw.splitlines())
    return part1(raw2)


def main():
    test(part1, test1, expected1)
    test(part2, test2, expected2)
    raw = get_day(9, override=True)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

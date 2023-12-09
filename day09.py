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


def zoop(x):
    r = list(map(lambda a: a[1] - a[0], zip(x, x[1:])))
    assert len(r) == len(x) - 1
    return r


def part1(raw: str):
    historys = parse(raw)
    s = 0
    for history in historys:
        tree = [history]
        while any(tree[-1]):
            tree.append(zoop(tree[-1]))
        tree = list(reversed(tree))
        for i in range(1, len(tree)):
            tree[i].append(tree[i][-1] + tree[i - 1][-1])
        s += tree[-1][-1]
    return s


def part2(raw: str):
    historys = parse(raw)
    s = 0
    for history in historys:
        tree = [history]
        while any(tree[-1]):
            tree.append(zoop(tree[-1]))
        tree = list(reversed(tree))

        for i in range(1, len(tree)):
            x = tree[i][0] - tree[i - 1][0]
            tree[i] = [x] + tree[i]
        s += tree[-1][0]
    return s


def main():
    test(part1, test1, expected1)
    raw = get_day(9, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

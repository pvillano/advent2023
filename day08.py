import re
from itertools import cycle
from math import lcm

from utils import benchmark, get_day

test1 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

test2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def parse(raw: str):
    path_str, nodes_str = raw.split('\n\n')
    path_str = tuple({"L": 0, "R": 1}[p] for p in path_str)
    nodes = {k: (l, r) for k, l, r in map(re.compile("\\w{3}").findall, nodes_str.splitlines())}
    return path_str, nodes


def part1(raw: str):
    path, nodes = parse(raw)
    current = "AAA"
    for i, direction in enumerate(cycle(path), 1):
        current = nodes[current][direction]
        if current == "ZZZ":
            return i


def part2(raw: str):
    path, nodes = parse(raw)
    a_set = (x for x in nodes.keys() if x.endswith("A"))

    def characterize(node):
        seen = dict()
        current = node
        for i, (loop_step, direction) in enumerate(cycle(enumerate(path))):
            key = (current, loop_step)
            if key in seen:
                start_of_loop = seen[key]
                length_of_loop = i - start_of_loop
                return length_of_loop
            seen[key] = i
            current = nodes[current][direction]

    characterized = list(map(characterize, a_set))
    return lcm(*(x for x in characterized))


def main():
    raw = get_day(8, test1)
    benchmark(part1, raw)
    raw = get_day(8, test2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

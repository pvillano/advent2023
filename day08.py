from itertools import cycle
from math import lcm

from utils import benchmark, get_day, debug_print

test = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

def parse(raw: str):
    path, rest = raw.split('\n\n')
    onetwo = {"L": 0, "R": 1}
    path = tuple(onetwo[p] for p in path)
    nodes = dict()
    for line in rest.splitlines():
        head, tails = line.split(" = ")
        left, right = tails[1:-1].split(", ")
        nodes[head] = (left, right)
    return path, nodes


# def part1(raw: str):
#     path, nodes = parse(raw)
#     current = "AAA"
#     for i, dir in enumerate(cycle(path)):
#         if dir == "L":
#             current = nodes[current][0]
#         elif dir == "R":
#             current = nodes[current][1]
#         else:
#             assert False
#         if current == "ZZZ":
#             return i+1


def part2(raw: str):
    path, nodes = parse(raw)
    a_set = set(x for x in nodes.keys() if x.endswith("A"))

    def characterize(node):
        seen = dict()
        current = node
        for i, (loop_step, dir) in enumerate(cycle(enumerate(path))):
            key = (current, loop_step)
            if key in seen:
                start_of_loop = seen[key]
                length_of_loop = i - start_of_loop
                # print(f"{node} has a cycle of length {length_of_loop} starting at {key}")

                break
            seen[key] = i
            current = nodes[current][dir]


        modulus = length_of_loop
        remainders = []
        first = key
        current = first
        while True:
            if current[0].endswith('Z'):
                remainders.append(seen[current] % modulus)
            current = nodes[current[0]][path[current[1]]], (current[1] + 1) % len(path)
            if current == first:
                break
        print(f"{node} has Zs at t%{length_of_loop}=={remainders[0]}")
        assert length_of_loop % len(path) == 0
        return modulus, remainders

    characterized = list(map(characterize, a_set))
    period = lcm(*(x[0] for x in characterized))
    # print(f"The combined period of all cycles is {period}")
    return period


def main():
    raw = test
    # benchmark(part1, raw)
    benchmark(part2, raw)
    raw = get_day(8, test)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

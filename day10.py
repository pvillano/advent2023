import sys
from collections import deque
from math import inf

from utils import benchmark, get_day, test

test1 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

expected1 = 8

test2 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""
expected2 = 4

adjacency = """S nsew
| ns
- we
L ne
J nw
7 sw
F se"""
adjacency = {k: v for k, v in [line.split(" ") for line in adjacency.splitlines()]}


def parse(raw: str):
    return raw.splitlines()


def connected(lines, r1, c1, r2, c2):
    if lines[r1][c1] == '.' or lines[r2][c2] == '.':
        return False
    if r1 == r2:
        if c1 > c2:
            c1, c2 = c2, c1
        assert c1 < c2
        ch1, ch2 = lines[r1][c1], lines[r2][c2]
        return "e" in adjacency[ch1] and "w" in adjacency[ch2]
    else:
        assert c1 == c2
        if r1 > r2:
            r1, r2 = r2, r1
        assert r1 < r2
        ch1, ch2 = lines[r1][c1], lines[r2][c2]
        return "s" in adjacency[ch1] and "n" in adjacency[ch2]


def find_s(lines):
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == "S":
                return r, c


def part1(raw: str):
    lines = parse(raw)

    origin_r, origin_c = find_s(lines)

    def find_furthest():
        distances = [[inf] * len(l) for l in lines]
        distances[origin_r][origin_c] = 0
        best = 0
        todo = deque([(origin_r, origin_c)])
        while todo:
            r, c = todo.popleft()
            assert distances[r][c] <= best
            assert lines[r][c] != '.'
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                r2, c2 = r + dx, c + dy
                if r2 not in range(len(lines)) or c2 not in range(len(lines[0])):
                    continue
                if distances[r2][c2] != inf:
                    continue
                if not connected(lines, r, c, r2, c2):
                    continue
                distances[r2][c2] = distances[r][c] + 1
                todo.append((r2, c2))
                best = max(best, distances[r2][c2])
        return best

    return find_furthest()


def part2(raw: str):
    lines = parse(raw)

    origin_r, origin_c = find_s(lines)

    stack = []
    sys.setrecursionlimit(15000)

    def recurse(r, c):
        assert lines[r][c] != '.'
        for delta_r, delta_c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r2, c2 = r + delta_r, c + delta_c
            if r2 not in range(len(lines)) or c2 not in range(len(lines[0])):
                continue
            if stack and (r2, c2) == stack[-1]:
                continue
            if not connected(lines, r, c, r2, c2):
                continue
            if stack and (r2, c2) == stack[0]:
                stack.append((r, c))
                return True
            stack.append((r, c))
            finished = recurse(r2, c2)
            if finished:
                return True
            stack.pop()
        return False

    recurse(origin_r, origin_c)
    assert stack
    stack = {rc: i for i, rc in enumerate(stack)}

    # debug_print_sparse_grid(set(stack), transpose=True)

    def flood():
        seen = set()
        to_flood = deque([(.5, .5)])
        while to_flood:
            src_r, src_c = to_flood.popleft()
            if (src_r, src_c) in seen:
                continue
            for delta_r, delta_c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                dest_r, dest_c = src_r + delta_r, src_c + delta_c
                if not (0.5 <= dest_r < len(lines) - .5 and 0.5 <= dest_c < len(lines[0]) - .5):
                    continue
                if src_r != dest_r:
                    r_avg = int((src_r + dest_r) / 2)
                    p1, p2 = (r_avg, int(src_c + .5)), (r_avg, int(src_c - .5))
                else:
                    c_avg = int((src_c + dest_c) / 2)
                    p1, p2 = (int(src_r - .5), c_avg), (int(src_r + .5), c_avg)

                if p1 not in stack or p2 not in stack:
                    to_flood.appendleft((dest_r, dest_c))
                elif abs(stack[p1] - stack[p2]) not in (1,len(stack)-1):
                    to_flood.appendleft((dest_r, dest_c))
            seen.add((src_r, src_c))
        return seen

    flooded = flood()

    def count_wet():
        wet_count = 0
        for r in range(len(lines)):
            for c in range(len(lines[0])):
                wet = True
                for delta_r, delta_c in [(-1, -1), (1, 1), (1, -1), (-1, 1)]:
                    corner_r = r + delta_r / 2
                    corner_c = c + delta_c / 2
                    if not (0 <= corner_r < len(lines) - .5 and 0 <= corner_c < len(lines[0]) - .5):
                        continue  # outside corners are wet
                    if (corner_r, corner_c) not in flooded:
                        wet = False
                        break
                    else:
                        pass
                if wet:
                    wet_count += 1
        return wet_count

    area_wet = count_wet()
    area_stack = len(stack)
    area_total = len(lines) * len(lines[0])
    return area_total - area_stack - area_wet


def main():
    test(part1, test1, expected1)
    raw = get_day(10, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

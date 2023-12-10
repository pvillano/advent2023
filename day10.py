import sys
from collections import deque
from math import inf

from utils import benchmark, get_day, test, debug_print_sparse_grid

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


def part1(raw: str):
    lines = parse(raw)

    def connected(rr, cc, rrr, ccc):
        if rr == rrr:
            if cc > ccc:
                cc, ccc = ccc, cc
            assert cc < ccc
            ch1, ch2 = lines[rr][cc], lines[rrr][ccc]
            return "e" in adjacency[ch1] and "w" in adjacency[ch2]
        assert cc == ccc
        if rr > rrr:
            rr, rrr = rrr, rr
        assert rr < rrr
        ch1, ch2 = lines[rr][cc], lines[rrr][ccc]
        return "s" in adjacency[ch1] and "n" in adjacency[ch2]

    for ra, line in enumerate(lines):
        for ca, char in enumerate(line):
            if char == "S":
                r, c = ra, ca
                break

    distances = [[inf] * len(l) for l in lines]
    distances[r][c] = 0
    best = 0
    todo = deque([(r, c)])
    while todo:
        assert distances[r][c] <= best
        assert lines[r][c] != '.'
        r, c = todo.popleft()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r2, c2 = r + dx, c + dy
            if r2 not in range(len(lines)) or c2 not in range(len(lines[0])):
                continue
            if lines[r2][c2] == '.':
                continue
            if distances[r2][c2] != inf:
                continue
            if not connected(r, c, r2, c2):
                continue
            distances[r2][c2] = distances[r][c] + 1
            todo.append((r2, c2))
            best = max(best, distances[r2][c2])
    return best


def part2(raw: str):
    lines = parse(raw)

    def connected(rr, cc, rrr, ccc):
        if lines[rr][cc] == '.' or lines[rrr][ccc] == '.':
            return False
        if rr == rrr:
            if cc > ccc:
                cc, ccc = ccc, cc
            assert cc < ccc
            ch1, ch2 = lines[rr][cc], lines[rrr][ccc]
            return "e" in adjacency[ch1] and "w" in adjacency[ch2]
        assert cc == ccc
        if rr > rrr:
            rr, rrr = rrr, rr
        assert rr < rrr
        ch1, ch2 = lines[rr][cc], lines[rrr][ccc]
        return "s" in adjacency[ch1] and "n" in adjacency[ch2]

    for ra, line in enumerate(lines):
        for ca, char in enumerate(line):
            if char == "S":
                r, c = ra, ca
                break
    origin = r, c

    stack = []
    sys.setrecursionlimit(15000)
    def rec(r, c):
        assert lines[r][c] != '.'
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r2, c2 = r + dx, c + dy
            if r2 not in range(len(lines)) or c2 not in range(len(lines[0])):
                continue
            if lines[r2][c2] == '.':
                continue
            if stack and (r2, c2) == stack[-1]:
                continue
            if stack and (r2, c2) == stack[0]:
                stack.append((r, c))
                return True
            if not connected(r, c, r2, c2):
                continue
            stack.append((r, c))
            finished = rec(r2, c2)
            if finished:
                return True
            stack.pop()
        return False

    rec(*origin)
    assert stack
    debug_print_sparse_grid(set(stack), transpose=True)
    pass
    area = 0

    to_flood = deque([(.5, .5)])
    flooded = set()
    while to_flood:
        r, c = to_flood.popleft()
        if (r, c) in flooded:
            continue
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r2, c2 = r + dx, c + dy
            if not (0 <= r2 < len(lines)-.5 and 0 <= c2 < len(lines[0])-.5):
                continue
            if r != r2:
                r_avg = int((r + r2) / 2)
                if not connected(r_avg, int(c + .5), r_avg, int(c - .5)):
                    to_flood.appendleft((r2, c2))
                elif (r_avg, int(c + .5)) not in stack or (r_avg, int(c - .5)) not in stack:
                    to_flood.appendleft((r2, c2))
            else:
                c_avg = int((c + c2) / 2)
                if not connected(int(r - .5), c_avg, int(r + .5), c_avg):
                    to_flood.appendleft((r2, c2))
                elif (int(r - .5), c_avg) not in stack or (int(r + .5), c_avg) not in stack:
                    to_flood.appendleft((r2, c2))

        flooded.add((r, c))
    s = 0
    for r1 in range(len(lines)):
        for c1 in range(len(lines[0])):
            wet = True
            for dx, dy in [(-1, -1), (1, 1), (1, -1), (-1, 1)]:
                cornerr = r1 + dx/2
                cornerc = c1 + dy/2
                if not (0 <= cornerr < len(lines) - .5 and 0 <= cornerc < len(lines[0]) - .5):
                    continue  # outside corners are wet
                if (cornerr, cornerc) not in flooded:
                    wet = False
                    break
                else:
                    pass
            if wet:
                s += 1
    a_stack = len(stack)
    a_tot = len(lines) * len(lines[0])
    return a_tot - a_stack - s


def main():
    test(part1, test1, expected1)
    raw = get_day(10, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

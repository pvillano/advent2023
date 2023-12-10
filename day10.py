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

    for find_s_r, line in enumerate(lines):
        for find_s_c, char in enumerate(line):
            if char == "S":
                origin_r, origin_c = find_s_r, find_s_c
                break
    origin = origin_r, origin_c

    stack = []
    sys.setrecursionlimit(15000)

    def rec(r, c):
        assert lines[r][c] != '.'
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r2, c2 = r + dr, c + dc
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
    to_flood = deque([(.5, .5)])
    flooded = set()
    while to_flood:
        origin_r, origin_c = to_flood.popleft()
        if (origin_r, origin_c) in flooded:
            continue
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r2, c2 = origin_r + dr, origin_c + dc
            if not (0 <= r2 < len(lines) - .5 and 0 <= c2 < len(lines[0]) - .5):
                continue
            if origin_r != r2:
                r_avg = int((origin_r + r2) / 2)
                if not connected(r_avg, int(origin_c + .5), r_avg, int(origin_c - .5)):
                    to_flood.appendleft((r2, c2))
                elif (r_avg, int(origin_c + .5)) not in stack or (r_avg, int(origin_c - .5)) not in stack:
                    to_flood.appendleft((r2, c2))
            else:
                c_avg = int((origin_c + c2) / 2)
                if not connected(int(origin_r - .5), c_avg, int(origin_r + .5), c_avg):
                    to_flood.appendleft((r2, c2))
                elif (int(origin_r - .5), c_avg) not in stack or (int(origin_r + .5), c_avg) not in stack:
                    to_flood.appendleft((r2, c2))

        flooded.add((origin_r, origin_c))
    s = 0
    for r1 in range(len(lines)):
        for c1 in range(len(lines[0])):
            wet = True
            for dr, dc in [(-1, -1), (1, 1), (1, -1), (-1, 1)]:
                corner_r = r1 + dr / 2
                corner_c = c1 + dc / 2
                if not (0 <= corner_r < len(lines) - .5 and 0 <= corner_c < len(lines[0]) - .5):
                    continue  # outside corners are wet
                if (corner_r, corner_c) not in flooded:
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

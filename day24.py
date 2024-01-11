from itertools import combinations

import numpy as np

from utils import benchmark, get_day, test, extract_ints, debug_print


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        px, py, pz, vx, vy, vz = extract_ints(line)
        ret.append(((px, py, pz), (vx, vy, vz)))
    return ret


def part1(raw: str):
    if raw == test1:
        xy_min, xy_max = 7, 27
    else:
        xy_min, xy_max = 200000000000000, 400000000000000
    hailstones = parse(raw)
    s = 0
    for ((p1x, p1y, p1z), (v1x, v1y, v1z)), ((p2x, p2y, p2z), (v2x, v2y, v2z)) in combinations(hailstones, 2):
        debug_print(((p1x, p1y, p1z), (v1x, v1y, v1z)), ((p2x, p2y, p2z), (v2x, v2y, v2z)))
        if v1x * v2y == v2x * v1y:
            debug_print("Hailstones' paths are parallel; they never intersect.")
            continue
        a = np.array([[v1x, -v2x], [v1y, -v2y]])
        b = np.array([p2x - p1x, p2y - p1y])
        t1, t2 = np.linalg.solve(a, b)
        if t1 < 0 or t2 < 0:
            debug_print("Hailstones' paths crossed in the past")
            continue
        x = p1x + v1x * t1
        y = p1y + v1y * t1
        if xy_min < x < xy_max and xy_min < y < xy_max:
            debug_print("Hailstones' paths will cross inside the test area", end=" ")
            s += 1
        else:
            debug_print("Hailstones' paths will cross outside the test area", end=" ")
        debug_print((x,y))
    return s


# if (p1x - p2x) * (v2y - v1y) == (p1y - p2y) * (v2x - v1x):
#     t = (p1x - p2x) / (v2x - v1x)
#     debug_print(t)
#     if t < 0:
#         pass
#     x = p1x + t * v1x
#     y = p1y + t * v1y
#     if xy_min < x < xy_max and xy_min < y < xy_max:
#         s += 1

def part2(raw: str):
    lines = parse(raw)


test1 = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

expected1 = 2

test2 = test1
expected2 = None


def main():
    test(part1, test1, expected1)
    raw = get_day(24, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

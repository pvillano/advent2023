from collections import defaultdict
from functools import reduce
from itertools import combinations, count
from math import gcd

import numpy as np

from utils import benchmark, get_day, test, extract_ints, debug_print, flatten


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

def lies_on_line(p0, v0):
    pass

def part2(raw: str):
    lines = parse(raw)
    vx_list = defaultdict(list)
    vy_list = defaultdict(list)
    vz_list = defaultdict(list)
    for p, v in lines:
        vx, vy, vz = v
        vx_list[vx].append((p,v))
        vy_list[vy].append((p,v))
        vz_list[vz].append((p,v))
    # for v_list in (vx_list, vy_list, vz_list):
    #     for v, items in v_list.items():
    #         if len(items) > 1:
    #             print(v, items)
    #     print()
    def it(i):
        v_list = (vx_list, vy_list, vz_list)[i]
        # v0 must be able to be negative
        for v0 in flatten(zip(count(), count(-1, -1))):
            cascade = False
            for pv_list in v_list.values():
                for (p1,v1), (p2,v2) in combinations(pv_list, 2):
                    # p2 + v1t2 = p0 + t2v0
                    # p1 + v1t1 = p0 + t1v0
                    # p2-p1 + v1(t2-t1) = 0 + (t2-t1)v0
                    # dp + v1*dt = dt*v0
                    # dp = dt(v0 - v1)
                    # => dp % (v0-v1) == 0
                    dp = p2[i] - p1[i]
                    if v0 > dp > 0 or v0 < dp < 0:
                        return
                    if v0 == v1[i]:
                        continue
                    if dp % (v0 - v1[i]) != 0:
                        cascade = True
                        break
                if cascade:
                    break
            if not cascade:
                yield v0

    # very wrong : )
    vx = next(iter(it(0)))
    vy = next(iter(it(1)))
    vz = next(iter(it(2)))
    # print(vx, vy, vz)

    (p1x, p1y, p1z), (v1x, v1y, v1z) = lines[0]
    (p2x, p2y, p2z), (v2x, v2y, v2z) = lines[1]
    for t1 in count():
        # px0 + vx0*t1 = px1+vx1*t1
        px0 = p1x + (v1x - vx) * t1
        py0 = p1y + (v1y - vy) * t1
        pz0 = p1z + (v1z - vz) * t1
        # px0 + vx0*t2 = px2 + vx2*t2
        # t2(vx0-vx2) = px2-px0
        t2 = (p2x - px0) / (vx - v2x)
        y_match = abs(py0 + vy*t2 - (p2y + v2y*t2)) < .5
        z_match = abs(pz0 + vz*t2 - (p2z + v2z*t2)) < .5
        if y_match and z_match:
            print(px0 + py0 + pz0)


test1 = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

expected1 = 2

test2 = test1
expected2 = None


def main():
    # test(part1, test1, expected1)
    raw = get_day(24, override=True)
    # benchmark(part1, raw)
    # test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

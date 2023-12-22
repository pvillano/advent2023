from collections import defaultdict
from copy import deepcopy

import numpy as np

from utils import benchmark, get_day, test, extract_ints


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        xyzxyz = extract_ints(line)
        ret.append((xyzxyz[:3], xyzxyz[3:]))
    return ret


def part1(raw: str):
    bricks = parse(raw)
    bricks = sorted(bricks, key=lambda x: (min(x[0][-1], x[1][-1]), x))
    x_max = max(max(b[0][0], b[1][0]) for b in bricks)
    y_max = max(max(b[0][1], b[1][1]) for b in bricks)
    z_max = max(max(b[0][2], b[1][2]) for b in bricks)
    print(x_max, y_max, z_max)
    taken = np.zeros((x_max + 1, y_max + 1, z_max + 1), dtype=int)
    heights = np.zeros((x_max + 1, y_max + 1), dtype=int)
    supported_by = dict()
    for i, brick in enumerate(bricks, start=1):
        (x1, y1, z1), (x2, y2, z2) = brick
        assert x1 <= x2 and y1 <= y2 and z1 <= z2
        atop = heights[x1:x2 + 1, y1:y2 + 1].max()
        z0 = atop
        z3 = z0 + z2 - z1 + 1
        taken[x1:x2 + 1, y1:y2 + 1, z0:z3] = i
        if atop == 0:
            supported_by[i] = {}
        else:
            supported_by[i] = set(taken[x1:x2 + 1, y1:y2 + 1, atop - 1].flatten()) - {0}
        heights[x1:x2 + 1, y1:y2 + 1] = z3
    supporting = defaultdict(set)
    for upper, lowers in supported_by.items():
        for lower in lowers:
            supporting[lower].add(upper)
    single_supported = {k for k, v in supported_by.items() if len(v) == 1}
    supporting_single = {k for k, v in supporting.items() if (v & single_supported)}
    return len(bricks) - len(supporting_single)


def part2(raw: str):
    bricks = parse(raw)
    bricks = sorted(bricks, key=lambda x: (min(x[0][-1], x[1][-1]), x))
    x_max = max(max(b[0][0], b[1][0]) for b in bricks)
    y_max = max(max(b[0][1], b[1][1]) for b in bricks)
    z_max = max(max(b[0][2], b[1][2]) for b in bricks)
    print(x_max, y_max, z_max)
    taken = np.zeros((x_max + 1, y_max + 1, z_max + 1), dtype=int)
    heights = np.zeros((x_max + 1, y_max + 1), dtype=int)
    supported_by = dict()
    for i, brick in enumerate(bricks, start=1):
        (x1, y1, z1), (x2, y2, z2) = brick
        assert x1 <= x2 and y1 <= y2 and z1 <= z2
        atop = heights[x1:x2 + 1, y1:y2 + 1].max()
        z0 = atop
        z3 = z0 + z2 - z1 + 1
        taken[x1:x2 + 1, y1:y2 + 1, z0:z3] = i
        if atop == 0:
            supported_by[i] = {}
        else:
            supported_by[i] = set(taken[x1:x2 + 1, y1:y2 + 1, atop - 1].flatten()) - {0}
        heights[x1:x2 + 1, y1:y2 + 1] = z3
    supporting = defaultdict(set)
    for upper, lowers in supported_by.items():
        for lower in lowers:
            supporting[lower].add(upper)
    single_supported = {k for k, v in supported_by.items() if len(v) == 1}
    supporting_single = {k for k, v in supporting.items() if (v & single_supported)}
    tote_yote = 0
    for initial in supporting_single:
        supported_by2 = deepcopy(supported_by)
        supporting2 = deepcopy(supporting)
        delq = [initial]
        while delq:
            to_remove = delq.pop()
            if to_remove not in supporting2:
                continue
            children = supporting2[to_remove]
            for child in children:
                supported_by2[child].remove(to_remove)
                if len(supported_by2[child]) == 0:
                    delq.append(child)
                    del supported_by2[child]
            del supporting2[to_remove]
        yeeted = len(supported_by) - len(supported_by2)
        tote_yote += yeeted
    return tote_yote


test1 = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

expected1 = 5

test2 = test1
expected2 = 7


def main():
    test(part1, test1, expected1)
    raw = get_day(22, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    if benchmark(part2, raw) in [59334]:
        print("FAIL")


if __name__ == "__main__":
    main()

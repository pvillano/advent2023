import numpy as np

from utils import benchmark, get_day, test, debug_print, debug_print_grid, debug_print_sparse_grid

test1 = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

expected1 = 62

test2 = test1
expected2 = 952408144115

UDLR = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        facing, distance, color = line.split()
        distance = int(distance)
        ret.append((facing, distance, color))
    return ret


def part1(raw: str):
    lines = parse(raw)
    path = [(0, 0)]
    pos = [0, 0]
    for facing, distance, color in lines:
        for i in range(distance):
            pos[0] += UDLR[facing][0]
            pos[1] += UDLR[facing][1]
            path.append(tuple(pos))
    debug_print_sparse_grid(set(path))
    assert path[0] == path[-1]
    path = path[:-1]
    flooded = flood(path)
    wet_count = count_wet(flooded)
    area_total = flooded.shape[0] * flooded.shape[1]
    area_stack = len(path)
    debug_print(f"{wet_count=} {area_total=} {area_stack=}")
    debug_print_grid(flooded)
    return area_total - wet_count


def count_wet(flooded):
    wet_count = 0
    for r in range(flooded.shape[0]):
        for c in range(flooded.shape[1]):
            wet = True
            for delta_r, delta_c in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                corner_r = r + delta_r
                corner_c = c + delta_c
                if not (0 <= corner_r < flooded.shape[0] and 0 <= corner_c < flooded.shape[1]):
                    continue  # outside corners are wet
                if not flooded[corner_r, corner_c]:
                    wet = False
                    break
            if wet:
                wet_count += 1
    return wet_count


def flood(path: list[tuple[int, int]]):
    xmin = min(xy[0] for xy in path)
    ymin = min(xy[1] for xy in path)
    path2 = [(x - xmin + 1, y - ymin + 1) for x, y in path]
    xmax = max(xy[0] for xy in path2)
    ymax = max(xy[1] for xy in path2)

    seen = np.zeros((xmax + 1, ymax + 1), dtype=bool)
    stack = {tuple(rc): i for i, rc in enumerate(path2)}

    to_flood = [(0, 0)]
    while to_flood:
        src_r, src_c = to_flood.pop()
        if seen[src_r, src_c]:
            continue
        for delta_r, delta_c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            dest_r, dest_c = src_r + delta_r, src_c + delta_c
            if not (0 <= dest_r < seen.shape[0] and 0 <= dest_c < seen.shape[1]):
                continue
            if seen[dest_r, dest_c]:
                continue
            if src_r != dest_r:
                r_avg = (src_r + dest_r + 1) / 2
                p1, p2 = (r_avg, src_c + 1), (r_avg, src_c)
            else:
                c_avg = (src_c + dest_c + 1) / 2
                p1, p2 = (src_r, c_avg), (src_r + 1, c_avg)

            if p1 not in stack or p2 not in stack:
                to_flood.append((dest_r, dest_c))
            elif abs(stack[p1] - stack[p2]) not in (1, len(stack) - 1):
                to_flood.append((dest_r, dest_c))
        seen[src_r, src_c] = True
    return seen


def parse2(raw):
    ret = []
    for line in raw.splitlines():
        _, _, color = line.split()
        color = color[2:-1]
        distance = int(color[:-1], 16)
        facing = "RDLU"[int(color[-1])]
        ret.append((facing, distance))
    return ret


def shoelace_area(points):
    inside = 0
    outside = 0
    for (x1, y1), (x2, y2) in zip(points, points[1:] + [points[0]]):
        inside += (x2 - x1) * (y2 + y1)
        outside += abs(x2 - x1) + abs(y2 - y1)
    return inside/2 + outside/2 + 1


def part2(raw: str):
    lines = parse2(raw)
    x, y = 0, 0
    points = [(0,0)]
    for facing, distance in lines:
        x += UDLR[facing][0] * distance
        y += UDLR[facing][1] * distance
        points.append((x,y))
    return shoelace_area(points)


def main():
    test(part1, test1, expected1)
    raw = get_day(18, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

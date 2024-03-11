from itertools import chain

from utils import benchmark, get_day, test

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
        ret.append((facing, distance))
    return ret


def to_points(lines):
    x, y = 0, 0
    points = [(0, 0)]
    for facing, distance in lines:
        x += UDLR[facing][0] * distance
        y += UDLR[facing][1] * distance
        points.append((x, y))
    return points


def part1(raw: str):
    return shoelace_area(to_points(parse(raw)))


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
    outside = 1
    for (x1, y1), (x2, y2) in zip(points, chain(points[1:], points[0:1])):
        inside += (x2 - x1) * (y2 + y1) / 2
        outside += (abs(x2 - x1) + abs(y2 - y1)) / 2
    return int(abs(inside) + outside)


def part2(raw: str):
    return shoelace_area(to_points(parse2(raw)))


def main():
    test(part1, test1, expected1)
    raw = get_day(18, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

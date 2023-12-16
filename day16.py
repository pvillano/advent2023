from collections import deque

from utils import benchmark, get_day, test, debug_print_grid

test1 = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""  # :\

expected1 = 46

test2 = test1
expected2 = 51


def parse(raw: str):
    return raw.splitlines()


def part1(raw: str, start=((0, -1), (0, 1))):
    grid = parse(raw)
    row_count = len(grid)
    col_count = len(grid[0])
    processed = set()
    heads = deque([start])  # position, heading
    while heads:
        (r0, c0), (dr, dc) = heads.popleft()
        r, c = r0 + dr, c0 + dc
        if r not in range(row_count) or c not in range(col_count):
            continue
        if ((r, c), (dr, dc)) in processed:
            continue
        processed.add(((r, c), (dr, dc)))
        ch1 = grid[r][c]

        if ch1 == ".":
            heads.append(((r, c), (dr, dc)))
        elif ch1 in "|-":
            if (ch1 == "-") == (dr == 0):
                heads.append(((r, c), (dr, dc)))
            else:
                heads.append(((r, c), (dc, dr)))
                heads.append(((r, c), (-dc, -dr)))
        elif ch1 == "/":
            heads.append(((r, c), (-dc, -dr)))
        else:
            assert ch1 == "\\"
            heads.append(((r, c), (dc, dr)))

    energized_set = set(x[0] for x in processed)
    energized = [[(r, c) in energized_set for c in range(col_count)] for r in range(row_count)]
    debug_print_grid(energized)
    return len(energized_set)


def part2(raw: str):
    best = 0
    grid = parse(raw)
    row_count = len(grid)
    col_count = len(grid[0])
    for r in range(row_count):
        start = ((r, -1), (0, 1))
        best = max(best, part1(raw, start))
        start = ((r, col_count), (0, -1))
        best = max(best, part1(raw, start))
    for c in range(col_count):
        start = ((-1, c), (1, 0))
        best = max(best, part1(raw, start))
        start = ((col_count, c), (-1, 0))
        best = max(best, part1(raw, start))
    return best


def main():
    test(part1, test1, expected1)
    raw = get_day(16, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

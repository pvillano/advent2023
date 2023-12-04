from utils import benchmark, get_day, extract_ints

test = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def parse(raw: str):
    lines = raw.splitlines()
    ret = []
    for line in lines:
        _, rest = line.split(":")
        winning, mine = rest.split("|")
        winning = extract_ints(winning)
        mine = extract_ints(mine)
        ret.append((winning, mine))
    return ret


def part1(raw: str):
    lines = parse(raw)
    points = 0
    for winning, mine in lines:
        count = len(set(winning) & set(mine))
        points += 2 ** count // 2
    return points


def part2(raw: str):
    lines = parse(raw)
    counts = [1] * len(lines)
    for i, (winning, mine) in enumerate(lines):
        wins = len(set(winning) & set(mine))
        if wins:
            for j in range(i + 1, i + wins + 1):
                counts[j] += counts[i]
    return sum(counts)


def main():
    raw = get_day(4, test)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

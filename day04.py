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

    def it():
        for line in lines:
            card, rest = line.split(":")
            left, right = rest.split("|")
            card = extract_ints(card)[0]
            left = extract_ints(left)
            right = extract_ints(right)
            yield card, left, right

    return list(it())


def part1(raw: str):
    lines = parse(raw)

    def it():
        for card, winning, mine in lines:
            count = len(set(winning) & set(mine))
            points = 2 ** (count - 1) if count > 0 else 0
            yield points

    return sum(it())


def part2(raw: str):
    lines = parse(raw)
    lines = [[1, x[1], x[2]] for x in lines]
    for i in range(len(lines)):
        count, winning, mine = lines[i]
        following = len(set(winning) & set(mine))
        if following:
            for j in range(1, following + 1):
                lines[i + j][0] += count
    return sum(x[0] for x in lines)


def main():
    raw = get_day(4, test)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

from utils import benchmark, get_day, extract_ints
from utils.grids import transpose

test = """Time:      7  15   30
Distance:  9  40  200"""


def parse(raw: str):
    return transpose(map(extract_ints, raw.splitlines()))


def part1(raw: str):
    races = parse(raw)
    ret = 1
    for time, distance in races:
        cnt1 = 0
        for hold in range(time):
            run = time - hold
            distance2 = run * hold
            if distance2 > distance:
                cnt1 += 1
        ret *= cnt1
    return ret


def part2(raw: str):
    time, distance = [int(line.split(":")[1].replace(" ", "")) for line in raw.splitlines()]
    lower, upper = 0, time // 2

    def traveled(t):
        return t * (time - t)

    while True:
        middle = (lower + upper) // 2
        if traveled(middle) > distance and traveled(middle - 1) < distance:
            return time - middle - middle + 1
        if traveled(middle) > distance:
            upper = middle
        elif traveled(middle) < distance:
            lower = middle


def part2slow(raw: str):
    time, distance = [int(line.split(":")[1].replace(" ", "")) for line in raw.splitlines()]

    def traveled(t):
        return t * (time - t)

    for middle in range(time // 2):
        if traveled(middle) > distance and traveled(middle - 1) < distance:
            return (time - middle) - middle + 1


def main():
    raw = get_day(6, test)
    benchmark(part1, raw)
    benchmark(part2, raw)
    benchmark(part2slow, raw)


if __name__ == "__main__":
    main()

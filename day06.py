from utils import benchmark, get_day, extract_ints
from utils.itertools2 import transpose

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
    time, distance = [int(l.split(":")[1].replace(" ", "")) for l in raw.splitlines()]
    lower, upper = 0, time // 2

    def traveled(t):
        return t * (time - t)

    assert traveled(upper) > distance
    assert traveled(lower) < distance
    while upper - lower > 1:
        middle = (lower + upper) // 2
        if traveled(middle) > distance and traveled(middle - 1) < distance:
            return time - middle - middle + 1
        if traveled(middle) > distance:
            upper = middle
        elif traveled(middle) < distance:
            lower = middle
    pass


def main():
    raw = get_day(6, test)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

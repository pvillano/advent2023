from functools import cache

from utils import benchmark, get_day, test, extract_ints, debug_print

test1 = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

expected1 = 21

test2 = test1
expected2 = 525152


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        sprints, counts = line.split()
        counts = extract_ints(counts)
        ret.append((sprints, counts))
    return ret


def arrangements(s):
    if s == "":
        yield ""
        return
    if s[0] == "?":
        for suffix in arrangements(s[1:]):
            yield "#" + suffix
            yield "." + suffix
    else:
        for suffix in arrangements(s[1:]):
            yield s[0] + suffix


def part1(raw: str):
    s = 0
    for sprints, counts in parse(raw):
        ss = 0
        for arrangement in arrangements(sprints):
            blorp = arrangement.split(".")
            blorp = [len(x) for x in blorp if x != ""]
            if tuple(blorp) == counts:
                ss += 1
        debug_print(sprints, ss)
        s += ss
    return s


def parse2(raw: str):
    ret = []
    for line in raw.splitlines():
        sprints, counts = line.split()
        counts = extract_ints(counts)
        ret.append(("?".join([sprints] * 5), counts * 5))
    return ret


@cache
def rec(sprints: str, counts: tuple[int]):
    # debug_print_recursive("start", sprints, counts)
    if len(counts) == 0:
        if sprints and "#" in sprints:
            return 0
        return 1
    # assert len(counts) != 0
    if len(sprints) == 0 or not ('#' in sprints or '?' in sprints):
        return 0  # need what don't have
    while sprints[0] == ".":
        sprints = sprints[1:]
    spring_length = counts[0]
    ways = 0
    if set(sprints[:spring_length]) <= set("#?"):
        if len(sprints) == spring_length or (spring_length < len(sprints) and sprints[spring_length] in "?."):
            ways += rec(sprints[spring_length + 1:], counts[1:])
    if sprints[0] == "?":
        ways += rec(sprints[1:], counts)
    # debug_print_recursive("end", sprints, counts, ways)
    return ways


def part2(raw: str):
    s = 0
    for sprints, counts in parse2(raw):
        ss = rec(sprints, counts)
        debug_print(sprints, ss)
        s += ss
    return s


def main():
    # test(part1, test1, expected1)
    raw = get_day(12, override=True)
    # benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

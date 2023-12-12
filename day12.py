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
        springs, counts = line.split()
        counts = extract_ints(counts)
        ret.append((springs, counts))
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
    total_arrangements = 0
    for springs, spans in parse(raw):
        partial_arrangements = 0
        for arrangement in arrangements(springs):
            runs_with_spaces = arrangement.split(".")
            run_lengths = [len(x) for x in runs_with_spaces if x != ""]
            if tuple(run_lengths) == spans:
                partial_arrangements += 1
        debug_print(springs, partial_arrangements)
        total_arrangements += partial_arrangements
    return total_arrangements


def parse2(raw: str):
    ret = []
    for line in raw.splitlines():
        springs, counts = line.split()
        counts = extract_ints(counts)
        ret.append(("?".join([springs] * 5), counts * 5))
    return ret


@cache
def rec(springs: str, spans: tuple[int]):
    # debug_print_recursive("start", springs, counts)
    if len(spans) == 0:
        if springs and "#" in springs:
            return 0
        return 1
    if len(springs) == 0 or not ('#' in springs or '?' in springs):
        return 0  # need what don't have
    while springs[0] == ".":
        springs = springs[1:]
    spring_length = spans[0]
    ways = 0
    if set(springs[:spring_length]) <= set("#?"):
        if len(springs) == spring_length or (spring_length < len(springs) and springs[spring_length] in "?."):
            ways += rec(springs[spring_length + 1:], spans[1:])
    if springs[0] == "?":
        ways += rec(springs[1:], spans)
    # debug_print_recursive("end", springs, counts, ways)
    return ways


def part2(raw: str):
    total_arrangements = 0
    for springs, spans in parse2(raw):
        partial_arrangements = rec(springs, spans)
        debug_print(springs, partial_arrangements)
        total_arrangements += partial_arrangements
    return total_arrangements


def main():
    test(part1, test1, expected1)
    raw = get_day(12, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

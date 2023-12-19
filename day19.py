import operator as op
from collections import defaultdict
from copy import copy
from functools import reduce

from utils import benchmark, get_day, test


def parse(raw: str):
    first, second = raw.split("\n\n")

    rules = defaultdict(list)
    for line in first.splitlines():
        rule_name, rest = line.split("{")
        rest = rest[:-1].split(",")
        for rule in rest:
            if '<' in rule:
                var, val = rule.split("<")
                val, to = val.split(":")
                rules[rule_name].append((var, op.lt, int(val), to))
            elif '>' in rule:
                var, val = rule.split(">")
                val, to = val.split(":")
                rules[rule_name].append((var, op.gt, int(val), to))
            else:
                to = rule
                rules[rule_name].append(("a", op.ne, None, to))

    parts = []
    for line in second.splitlines():
        part = dict()
        for item in line[1:-1].split(","):
            var, val = item.split("=")
            part[var] = int(val)
        parts.append(part)
    return rules, parts


def part1(raw: str):
    rules, parts = parse(raw)
    s = 0
    for part in parts:
        station = "in"
        while station not in ("A", "R"):
            for var, cond, val, to in rules[station]:
                if cond(part[var], val):
                    station = to
                    break
        if station == "A":
            s += sum(part.values())
    return s


def part2(raw: str):
    rules, _ = parse(raw)

    def recurse(part, station):
        while station not in ("A", "R"):
            for var, cond, val, to in rules[station]:
                if cond(part[var][0], val) != cond(part[var][1] - 1, val):
                    if cond == op.gt:
                        val += 1
                    vals = sorted(part[var] + [val])
                    left_part = copy(part)
                    left_part[var] = vals[:2]
                    right_part = copy(part)
                    right_part[var] = vals[1:]
                    return recurse(left_part, station) + recurse(right_part, station)
                if cond(part[var][0], val) and cond(part[var][1] - 1, val):
                    station = to
                    break
        if station == "A":
            return reduce(op.mul, [x[1] - x[0] for x in part.values()], 1)
        assert station == "R"
        return 0

    return recurse({k: [1, 4001] for k in "xmas"}, "in")


test1 = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

expected1 = 19114

test2 = test1
expected2 = 167409079868000


def main():
    test(part1, test1, expected1)
    raw = get_day(19, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

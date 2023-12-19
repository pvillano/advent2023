import operator as op
from collections import defaultdict
from functools import reduce
from itertools import product

from utils import benchmark, get_day, test, debug_print

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

def make_parts(cvs):
    blorg = [zip(cvs[x], cvs[x][1:]) for x in "xmas"]
    for xmas in product(*blorg):
        yield {k:v for k,v in zip("xmas", xmas)}

def part2(raw: str):
    rules, _ = parse(raw)
    critical_values = defaultdict(set)
    for ruleset in rules.values():
        for var, cond, val, to in ruleset:
            if val is not None:
                critical_values[var].add(val-1)
                critical_values[var].add(val)
                critical_values[var].add(val+1)
    for k in critical_values.keys():
        cvs = critical_values[k].add(1)
        cvs = critical_values[k].add(4001)
        critical_values[k] = sorted(critical_values[k])

    s = 0
    for part in make_parts(critical_values): # inclusive, exclusive
        station = "in"
        while station not in ("A", "R"):
            for var, cond, val, to in rules[station]:
                assert cond(part[var][0], val) == cond(part[var][1] - 1, val)
                if cond(part[var][0], val):
                    station = to
                    break
        if station == "A":
            s += reduce(op.mul, [x[1] - x[0] for x in part.values()], 1)
    return s




def main():
    test(part1, test1, expected1)
    raw = get_day(19, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

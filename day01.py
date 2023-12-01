from utils import benchmark, get_day, debug_print

test = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
test = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


def parse(raw: str):
    return raw.split("\n")


def part1(raw: str):
    lines = parse(raw)
    tot = 0
    for l in lines:
        j = []
        for ch in l:
            if '0' <= ch <= '9':
                j.append(ch)
        num = j[0] + j[-1]
        debug_print(num)
        tot += int(num)
    return tot

DIGITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
def part2(raw: str):
    lines = parse(raw)
    tot = 0
    for l in lines:
        best_start = len(l)
        best_end = len(l)
        start_value = 0
        end_value = 0
        for d, digit in enumerate(DIGITS):
            try:
                if l.index(digit) <= best_start:
                    best_start = l.index(digit)
                    start_value = d
            except ValueError as e:
                pass
            try:
                if "".join(reversed(l)).index("".join(reversed(digit))) <= best_end:
                    best_end = "".join(reversed(l)).index("".join(reversed(digit)))
                    end_value = d
            except ValueError as e:
                pass
        for d, digit in enumerate(str(i) for i in range(10)):
            try:
                if l.index(digit) <= best_start:
                    best_start = l.index(digit)
                    start_value = d
            except ValueError as e:
                pass
            try:
                if "".join(reversed(l)).index("".join(reversed(digit))) <= best_end:
                    best_end = "".join(reversed(l)).index("".join(reversed(digit)))
                    end_value = d
            except ValueError as e:
                pass
        debug_print(start_value*10+end_value)
        tot += start_value*10+end_value
    return tot



def main():
    raw = get_day(1, test)
    # benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

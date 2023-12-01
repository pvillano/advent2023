from utils import benchmark, get_day, debug_print

test1 = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
test2 = """two1nine
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
    for line in lines:
        j = []
        for ch in line:
            if '0' <= ch <= '9':
                j.append(ch)
        num = int(j[0] + j[-1])
        debug_print(num)
        tot += num
    return tot


DIGIT_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
DIGIT_DIGITS = [str(i) for i in range(10)]


def part2(raw: str):
    lines = parse(raw)
    tot = 0
    for line in lines:
        first_digit_idx = len(line)
        last_digit_idx = len(line)
        for digit_list in [DIGIT_WORDS, DIGIT_DIGITS]:
            for digit_int, digit in zip(range(10), digit_list):
                if digit in line and line.index(digit) <= first_digit_idx:
                    first_digit_idx = line.index(digit)
                    first_digit = digit_int
                enil = "".join(reversed(line))
                tigid = "".join(reversed(digit))
                if tigid in enil and enil.index(tigid) <= last_digit_idx:
                    last_digit_idx = enil.index(tigid)
                    last_digit_value = digit_int
        tot += first_digit * 10 + last_digit_value
    return tot


def main():
    raw = get_day(1, test1)
    benchmark(part1, raw)
    raw = get_day(1, test2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

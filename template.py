import os
import datetime

with open("template.py") as template_file:
    eric_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5), "EST"))

    if eric_time.month == 11 and eric_time.day == 30:
        up_to_day = 1
    elif eric_time.month == 12:
        # only generate the next day's template if it is close to midnight
        if eric_time.hour < 23:
            up_to_day = eric_time.day
        else:
            up_to_day = eric_time.day + 1
    else:
        up_to_day = 25
    template_string = template_file.read().split("#" * 80)[-1].lstrip()
    # inclusive range
    for i in range(1, up_to_day + 1):
        p = f"day{i:02}.py"
        if not os.path.exists(p):
            file_contents = template_string.replace("DAYNUMBER", str(i))
            with open(p, "x") as out_file:
                out_file.write(file_contents)
exit(0)
DAYNUMBER = 0
################################################################################
from utils import benchmark, get_day, test


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(line)
    return ret


def part1(raw: str):
    lines = parse(raw)


def part2(raw: str):
    lines = parse(raw)


test1 = """"""

expected1 = None

test2 = test1
expected2 = None


def main():
    test(part1, test1, expected1)
    raw = get_day(DAYNUMBER, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

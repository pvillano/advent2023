from utils import benchmark, get_day

test = """"""


def parse(raw: str):
    return raw.split("\n")


def part1(raw: str):
    lines = parse(raw)


def part2(raw: str):
    lines = parse(raw)

####
# start of elided portion
import os
import datetime

with open("template.py") as template_file:
    eric_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5), "EST"))

    # only generate the next day's template if it is close to midnight
    if eric_time.month == 12:
        if eric_time.hour < 23:
            up_to_day = eric_time.day
        else:
            up_to_day = eric_time.day + 1
    elif eric_time.month == 11:
        up_to_day = 1
    else:
        up_to_day = 25
    sections = template_file.read().split("####")
    template_string = sections[0] + sections[-1]
    # inclusive range
    for i in range(1, up_to_day + 1):
        p = f"day{i:02}.py"
        if not os.path.exists(p):
            file_contents = template_string.replace("1337", str(i))
            with open(p, "x") as out_file:
                out_file.write(file_contents)
exit(0)


# end of elided portion
####
def main():
    raw = get_day(1337, test)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

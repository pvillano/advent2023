test = """"""

# raw = get_day(DAYNUMBER, test)
# lines = raw.split("\n")


def part1():
    pass


def part2():
    pass


if __name__ == "__main__":
    # benchmark(part1)
    # benchmark(part2)

####
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
        else:
            up_to_day = 25
        template_string = template_file.read().split("####")[0].replace("# ", "")
        # inclusive range
        for i in range(1, up_to_day + 1):
            p = f"day{i:02}.py"
            if not os.path.exists(p):
                file_contents = template_string.replace("DAYNUMBER", str(i))
                with open(p, "x") as out_file:
                    out_file.write(file_contents)

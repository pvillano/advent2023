__all__ = [
    "benchmark",
    "DEBUG",
    "flatten",
    "pipe",
    "submit"
]

import os
import sys
import time
import datetime
from itertools import chain
from pprint import pprint as not_my_pp
from typing import Callable

import requests as requests

DEBUG = bool(sys.gettrace())

flatten = chain.from_iterable


def pipe(first, *args: Callable):
    for func in args:
        first = func(first)
    return first


def pprint(object_, stream=None, indent=1, width=80, depth=None, *,
           compact=False, sort_dicts=True, underscore_numbers=False):
    if isinstance(object_, str):
        print('"""', file=stream)
        print(object_.replace("\\", "\\\\"))
        print('"""', file=stream)
    else:
        not_my_pp(object_, stream, indent, width, depth, compact=compact, sort_dicts=sort_dicts,
                  underscore_numbers=underscore_numbers)


def test(part: Callable, data, expected=None):
    start_time = time.perf_counter_ns()
    ans = part(data)
    end_time = time.perf_counter_ns()
    seconds = (end_time - start_time) / 10 ** 9
    if DEBUG:
        pprint(ans, stream=sys.stderr)
        print(
            f"completed in {seconds:0.3f} seconds\n", file=sys.stderr, flush=True
        )
    else:
        pprint(ans)
        print(f"completed in {seconds:0.3f} seconds\n")
    assert ans == expected


def benchmark(part: Callable) -> None:
    """
    Calls a function and prints the return value
    :param part:
    :return: None
    """
    file = sys.stderr if DEBUG else sys.stdout

    datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    print("Started", datetime.datetime.now().strftime("%I:%M%p"), file=file, flush=True)
    start_time = time.perf_counter_ns()
    ans = part()
    end_time = time.perf_counter_ns()
    seconds = (end_time - start_time) / 10 ** 9
    pprint(ans, stream=file)
    print(f"Completed in {seconds:0.3f} seconds.\n", file=file, flush=True)
    return ans


def submit(answer, day, level, year):
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    data = {"level": level, "answer": answer}
    with open(".token", "r") as token_file:
        cookies = {"session": token_file.read()}
    response = requests.post(url=url, data=data, cookies=cookies)
    print(response.text, file=sys.stderr)
    if "That's the right answer!" in response.text:
        print("That's the right answer!")
    elif "That's not the right answer." in response.text:
        print("That's not the right answer.", file=sys.stderr)
        raise ...
    elif "You don't seem to be solving the right level." in response.text:
        raise ...
    else:
        raise NotImplementedError()

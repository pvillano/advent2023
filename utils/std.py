__all__ = [
    "benchmark",
    "DEBUG",
    "flatten",
    "test"
]

import datetime
import sys
import time
from collections.abc import Callable
from itertools import chain
from pprint import pprint as not_my_pp
from typing import Any

has_trace = hasattr(sys, 'gettrace') and sys.gettrace() is not None
has_breakpoint = sys.breakpointhook.__module__ != "sys"
DEBUG = has_trace or has_breakpoint

flatten = chain.from_iterable


def pprint(object_, stream=None, indent=1, width=80, depth=None, *,
           compact=False, sort_dicts=True, underscore_numbers=False):
    if isinstance(object_, str):
        print('"""', file=stream)
        print(object_.replace("\\", "\\\\"), file=stream)
        print('"""', file=stream)
    else:
        not_my_pp(object_, stream, indent, width, depth, compact=compact, sort_dicts=sort_dicts,
                  underscore_numbers=underscore_numbers)


def test(func: Callable, data, expected):
    name = func.__name__ if hasattr(func, "__name__") else "benchmark"
    out_stream = sys.stderr if DEBUG else sys.stdout
    print("Testing", name, datetime.datetime.now().strftime("%I:%M%p"), file=out_stream, flush=DEBUG)
    start_time = time.perf_counter_ns()
    ans = func(data)
    end_time = time.perf_counter_ns()
    seconds = (end_time - start_time) / 10 ** 9
    if not ans == expected:
        print(f"FAILED in {seconds:0.3f} seconds", file=out_stream, flush=DEBUG)
        print("Expected:", expected, file=out_stream, flush=True)
        print("Actual:  ", ans, file=out_stream, flush=True)
        exit(1)
    print(f"Passed in {seconds:0.3f} seconds\n", file=out_stream, flush=DEBUG)


def benchmark(func: Callable, *args, **kwargs) -> Any:
    """
    Calls a function and prints the return value
    :param func:
    :return: None
    """
    out_stream = sys.stderr if DEBUG else sys.stdout
    name = func.__name__ if hasattr(func, "__name__") else "benchmark"
    print("Started", name, datetime.datetime.now().strftime("%I:%M%p"), file=out_stream, flush=True)
    start_time = time.perf_counter_ns()
    ans = func(*args, **kwargs)
    end_time = time.perf_counter_ns()
    seconds = (end_time - start_time) / 10 ** 9
    pprint(ans, stream=out_stream)
    print(f"Completed in {seconds:0.3f} seconds.\n", file=out_stream, flush=True)
    return ans

__all__ = ["debug_print", "debug_print_grid", "debug_print_sparse_grid", "debug_print_recursive"]

import inspect
import sys
from collections.abc import Iterable
from itertools import chain
from typing import Any

import numpy as np

from .std import DEBUG


def debug_print(*args, override=False, **kwargs) -> None:
    """
    Passes arguments to `print`,
    if currently executing program
    is being debugged or override is True
    :param args: same as print
    :param override:
    :param kwargs: same as print
    :return:
    """
    if not (DEBUG or override):
        return
    return print(*args, **kwargs, file=sys.stderr, flush=True)


def debug_print_grid(grid: list[str] or list[list[any]] or np.ndarray, *, override=False) -> None:
    """

    :param grid:
    :param override:
    :return:
    """
    if not (DEBUG or override):
        return

    if isinstance(grid[0], str):
        for line in grid:
            print(line, file=sys.stderr)
        print(file=sys.stderr, flush=True)
        return

    if isinstance(grid[0][0], bool) or isinstance(grid[0][0], np.bool_):
        for line in grid:
            for i in line:
                print('#' if i else '.', file=sys.stderr, end=" ")
            print(file=sys.stderr)
        print(file=sys.stderr, flush=True)
        return

    max_len = max(map(len, map(str, chain.from_iterable(grid))))
    for line in grid:
        for i in line:
            print(str(i).rjust(max_len), file=sys.stderr, end=" ")
        print(file=sys.stderr)
    print(file=sys.stderr, flush=True)


BASE_INDENT = len(inspect.stack()) - 7


def debug_print_recursive(*args, override=False, **kwargs) -> None:
    """
    Prints with an indent proportional to the current call stack depth
    :param args:
    :param override:
    :param kwargs:
    :return:
    """
    if not (DEBUG or override):
        return
    indent = len(inspect.stack()) - BASE_INDENT
    return print(" |" * indent, *args, **kwargs, file=sys.stderr, flush=True)


def debug_print_sparse_grid(
        grid_map: dict[(int, int), Any] or set, *, transpose=False, override=False
) -> None:
    """
    Prints a sparse grid
    :param grid_map:
    :param transpose:
    :param override:
    :return:
    """
    if not (DEBUG or override):
        return
    if isinstance(grid_map, Iterable):
        grid_map = {k: "#" for k in grid_map}
    x0, x1 = min(k[0] for k in grid_map.keys()), max(k[0] for k in grid_map.keys())
    y0, y1 = min(k[1] for k in grid_map.keys()), max(k[1] for k in grid_map.keys())
    max_w = max(len(str(v)) for v in grid_map.values())
    if max_w > 1:
        max_w += 1
    if not transpose:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if (x, y) in grid_map:
                    print(
                        str(grid_map[(x, y)]).rjust(max_w), end="", file=sys.stderr
                    )
                else:
                    print("." * max_w, end="", file=sys.stderr)
            print(file=sys.stderr, flush=True)
    else:
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if (x, y) in grid_map:
                    print(
                        str(grid_map[(x, y)]).rjust(max_w), end="", file=sys.stderr
                    )
                else:
                    print("." * max_w, end="", file=sys.stderr)
            print(file=sys.stderr, flush=True)
    print(file=sys.stderr, flush=True)

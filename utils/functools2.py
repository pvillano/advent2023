from collections.abc import Callable


def pipe(first, *args: Callable):
    for func in args:
        first = func(first)
    return first

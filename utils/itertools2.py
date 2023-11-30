from itertools import chain
from typing import Iterable, Sized


def rotations(iterable: Iterable):
    iterable = tuple(iterable)
    for idx in range(len(iterable)):
        yield tuple(chain(iterable[-idx:], iterable[:-idx]))


def transpose(iterable):
    assert len(set(map(len, iterable))) == 1
    return zip(*iterable)


def main():
    l = [[10 * x + y for y in range(10)] for x in range(20)]
    lt = transpose(l)
    for i, line in enumerate(lt):
        for j, val in enumerate(line):
            assert val == l[j][i]


if __name__ == '__main__':
    main()

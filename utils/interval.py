from collections.abc import Iterable


def range_overlaps(a: range, b: range):
    return a.start < b.stop and b.start < a.stop


class IntervalSet:
    """
    Can be constructed from
    a list

    invariants:
    __intervals is a list of non-overlapping ranges
    """
    __intervals: list[range]

    def __init__(self, iterable: Iterable[range] = None):
        if iterable is None:
            iterable = ()
        self.__intervals = list(iterable)
        self.__normalize()

    def __normalize(self):
        if len(self.__intervals) == 0:
            return
        first: range
        rest: list[range]
        first, *rest = sorted(self.__intervals, key=lambda x: x.start)
        self.__intervals = [first]
        for r in rest:
            if r.start in self.__intervals[-1]:
                stop = max(self.__intervals[-1].stop, r.stop)
                self.__intervals[-1] = range(self.__intervals[-1].start, stop)

    def __contains__(self, item):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def add(self, value):
        raise NotImplementedError()

    def discard(self, value):
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()

    def __and__(self, other):
        raise NotImplementedError()

    def __or__(self, other):
        raise NotImplementedError()

    def __sub__(self, other):
        raise NotImplementedError()

    def __xor__(self, other):
        raise NotImplementedError()

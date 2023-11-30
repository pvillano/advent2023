from typing import Iterable, Hashable

__all__ = ["bitset_factory_factory", "FrozenBitset"]


class FrozenBitset:
    __insides: int
    __backing_dict: dict[Hashable, int]

    def __init__(self, insides: int, backing_dict: dict[Hashable, int]):
        self.__insides = insides
        self.__backing_dict = backing_dict

    def __contains__(self, item: Hashable):
        return item in self.__backing_dict and self.__insides & 1 << self.__backing_dict[item]

    def __and__(self, other):
        self.__siblings_check(other)
        return FrozenBitset(self.__insides & other.__insides, self.__backing_dict)

    def __or__(self, other):
        self.__siblings_check(other)
        return FrozenBitset(self.__insides | other.__insides, self.__backing_dict)

    def __eq__(self, other):
        self.__siblings_check(other)
        return self.__insides == other.__insides

    def __siblings_check(self, other: "FrozenBitset"):
        if not isinstance(other, FrozenBitset):
            raise NotImplementedError("unsupported operand types: bitset and not bitset")
        if id(self.__backing_dict) != id(other.__backing_dict):
            raise TypeError("bitsets must have the same backing dict")

    def __hash__(self):
        return self.__insides ^ id(self.__backing_dict)


def bitset_factory_factory():
    backing_dict: dict[Hashable, int] = dict()

    def make_bitset(values: list[Hashable] = None):
        if values is None:
            values = []
        insides = 0
        for element in values:
            if element not in backing_dict:
                backing_dict[element] = len(backing_dict)
            insides |= 1 << backing_dict[element]
        return FrozenBitset(insides, backing_dict=backing_dict)

    return make_bitset


def main():
    set_ = bitset_factory_factory()
    bs1 = set_(["ape", "boa", "cow"])
    bs2 = set_(["ape", "boa", "cow"])
    bs3 = set_(["dog"])

    assert "ape" in bs1
    assert "dog" not in bs1
    assert bs1 == bs2
    assert bs1 != bs3
    assert not (bs1 != bs2)
    assert not (bs1 == bs3)

    make_bitset2 = bitset_factory_factory()
    bs_a = make_bitset2(["ape", "boa", "cow"])
    try:
        assert not bs1 == bs_a
    except TypeError:
        pass
    else:
        raise AssertionError("failed")


if __name__ == '__main__':
    main()

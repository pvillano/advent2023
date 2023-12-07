from collections import Counter

from utils import benchmark, get_day

test = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

strengths = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")
strengths = {ch: -i for i, ch in enumerate(strengths)}


def parse(raw: str):
    for l in raw.splitlines():
        cards, bet = l.split(" ")
        yield cards, int(bet)


def key(hand_and_bet: tuple[str, int]):
    hand, bet = hand_and_bet
    card_strengths = tuple(strengths[card] for card in hand)
    of_a_kind = Counter(Counter(hand).values())
    if of_a_kind == {5: 1}:
        return 5, card_strengths
    elif of_a_kind == {4: 1, 1: 1}:
        return 4, card_strengths
    elif of_a_kind == {3: 1, 2: 1}:
        return 3.5, card_strengths
    if of_a_kind == {3: 1, 1: 2}:
        return 3, card_strengths
    if of_a_kind == {2: 2, 1: 1}:
        return 2, card_strengths
    if of_a_kind == {2: 1, 1: 3}:
        return 1, card_strengths
    if of_a_kind == {1: 5}:
        return 0, card_strengths
    raise ValueError(str(of_a_kind))


def part1(raw: str):
    lines = list(parse(raw))
    sorted_lines = sorted(lines, key=key)
    s = 0
    for i, (hand, bet) in enumerate(sorted_lines):
        s += (i + 1) * bet
    return s


def key2(hand_and_bet: (str, int)):
    hand, _ = hand_and_bet
    card_strengths = tuple((-1 if card == "J" else strengths[card]) for card in hand)
    of_a_kind = Counter(Counter(hand.replace("J", "")).values())
    if of_a_kind in ({5: 1}, {4: 1}, {3: 1}, {2: 1}, {1: 1}, dict()):
        return 5, card_strengths  # Five of a kind
    elif of_a_kind in ({4: 1, 1: 1}, {3: 1, 1: 1}, {2: 1, 1: 1}, {1: 2}):
        return 4, card_strengths  # Four of a kind
    elif of_a_kind in ({3: 1, 2: 1}, {2: 2}):
        return 3.5, card_strengths  # Full house
    elif of_a_kind in ({3: 1, 1: 2}, {1: 2, 2: 1}, {1: 3}):
        return 3, card_strengths  # Three of a kind
    elif of_a_kind == {2: 2, 1: 1}:
        return 2, card_strengths  # Two pair
    elif of_a_kind in ({2: 1, 1: 3}, {1: 4}):
        return 1, card_strengths  # One pair
    elif of_a_kind == {1: 5}:
        return 0, card_strengths  # High card
    raise ValueError(str(of_a_kind))  # keep implementing cases until this goes away


def part2(raw: str):
    lines = list(parse(raw))
    sorted_lines = sorted(lines, key=key2)
    s = 0
    for i, (hand, bet) in enumerate(sorted_lines):
        s += (i + 1) * bet
    return s


def main():
    raw = get_day(7, test)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

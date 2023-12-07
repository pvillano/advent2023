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


def key(handbet: str):
    hand, bet = handbet
    card_strengths = tuple(strengths[card] for card in hand)
    ofakind = Counter(Counter(hand).values())
    if ofakind == {5: 1}:
        return 5, card_strengths
    elif ofakind == {4: 1, 1: 1}:
        return 4, card_strengths
    elif ofakind == {3: 1, 2: 1}:
        return 3.5, card_strengths
    if ofakind == {3: 1, 1: 2}:
        return 3, card_strengths
    if ofakind == {2: 2, 1: 1}:
        return 2, card_strengths
    if ofakind == {2: 1, 1: 3}:
        return 1, card_strengths
    if ofakind == {1: 5}:
        return 0, card_strengths
    raise ValueError(str(ofakind))


def part1(raw: str):
    lines = list(parse(raw))
    fugg = sorted(lines, key=key)
    s = 0
    for i, (hand, bet) in enumerate(fugg):
        s += (i + 1) * bet
    return s


strengths = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")
strengths = {ch: -i for i, ch in enumerate(strengths)}


def key2(hand_and_bet: (str, int)):
    hand, _ = hand_and_bet
    card_strengths = tuple((-1 if card == "J" else strengths[card]) for card in hand)
    of_a_kind = Counter(Counter(hand.replace("J", "")).values())
    if of_a_kind in ({5: 1}, {4: 1}, {3: 1}, {2: 1}, {1: 1}, dict()):
        return 5, card_strengths  # Five of a kind
    elif of_a_kind in ({4: 1, 1: 1}, {3: 1, 1: 1}, {2: 1, 1: 1}, {1: 2}):
        return 4, card_strengths  # Four of a kind
    elif of_a_kind in ({3: 1, 2: 1}, {2: 2}, {3: 1, 1: 1}):
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
    for line in lines:
        if not key2(line) >= key(line):
            print(line, key2(line))
    fugg = sorted(lines, key=key2)
    assert len(set(map(key2, lines))) == len(lines)
    s = 0
    for i, (hand, bet) in enumerate(fugg):
        s += (i + 1) * bet
    return s
    # not 252122402
    # not 252474561


def main():
    raw = get_day(7, test)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

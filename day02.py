import re
from collections import defaultdict
from functools import reduce
from itertools import batched

from utils import benchmark, get_day

test = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


def parse(raw: str):
    lines = raw.split("\n")
    for line in lines:
        id_str, games_str = line.split(": ")
        game_id = int(id_str.split(" ")[-1])
        game_str_list = games_str.split("; ")
        game_list = []
        for game in game_str_list:
            game_dict = dict()
            for s in game.split(", "):
                val, color = s.split(" ")
                val = int(val)
                game_dict[color] = val
            game_list.append(game_dict)

        yield game_id, game_list


def part1(raw: str):
    lines = parse(raw)
    added_ids = 0
    for game_id, game_list in lines:
        fail = False
        for game in game_list:
            if (game.get("red", 0) > 12
                    or game.get("green", 0) > 13
                    or game.get("blue", 0) > 14):
                fail = True
        if not fail:
            added_ids += game_id
    return added_ids


def part2(raw: str):
    lines = parse(raw)
    power = 0
    for game_id, game_list in lines:
        gamegame = defaultdict(int)
        for game in game_list:
            for red in ("red", "green", "blue"):
                if red in game:
                    gamegame[red] = max(gamegame[red], game[red])
        power += gamegame["red"] * gamegame["green"] * gamegame["blue"]
    return power

import operator as op
def golf(raw: str):
    print(sum(
        g for g, l in enumerate(raw.split("\n"), 1)
        if all(
            int(n) <= {"r": 12, "g": 13, "b": 14}[c[0]]
            for n, c in batched(re.split("[;,:]? ", l)[2:], 2))))

    power = 0
    for g, l in enumerate(raw.split("\n"), 1):
        d = {"r": 0, "g": 0, "b": 0}
        for n, c in batched(re.split("[;,:]? ", l)[2:], 2):
            d[c[0]] = max(d[c[0]], int(n))
        power += reduce(op.mul, d.values())
    return power


def main():
    raw = get_day(2, test)
    benchmark(part1, raw)
    benchmark(part2, raw)
    benchmark(golf, raw)


if __name__ == "__main__":
    main()

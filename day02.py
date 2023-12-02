from collections import defaultdict

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
        games = games_str.split("; ")
        game_list = []
        for game in games:
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
        possible = True
        for game in game_list:
            if "red" in game and game["red"] > 12:
                possible = False
            if "green" in game and game["green"] > 13:
                possible = False
            if "blue" in game and game["blue"] > 14:
                possible = False
        if possible:
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


def main():
    raw = get_day(2, test)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

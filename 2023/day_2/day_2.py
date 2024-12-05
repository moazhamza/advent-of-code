import re


GAME_HAD = {
    "red": 12,
    "blue": 14,
    "green": 13,
}

sample_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


def part_1(_input) -> None:
    id_total = 0
    for game in _input.split("\n"):
        if not game:
            continue
        game_id = int(re.search(r"Game (\d+):", game).group(1))
        max_for_game = find_max_for_game(game)

        if (
            max_for_game["red"] <= GAME_HAD["red"]
            and max_for_game["blue"] <= GAME_HAD["blue"]
            and max_for_game["green"] <= GAME_HAD["green"]
        ):
            id_total += game_id

    print(id_total)


def find_max_for_game(game: str) -> dict[str, int]:
    max_for_game = {"red": 0, "blue": 0, "green": 0}
    for reach in game.split(":")[1].split(";"):
        num_red, num_green, num_blue = 0, 0, 0
        if red_search := re.search(r"(\d+) red", reach):
            num_red = int(red_search.group(1))
        if blue_search := re.search(r"(\d+) blue", reach):
            num_blue = int(blue_search.group(1))
        if green_search := re.search(r"(\d+) green", reach):
            num_green = int(green_search.group(1))
        max_for_game["red"] = max(max_for_game["red"], num_red)
        max_for_game["blue"] = max(max_for_game["blue"], num_blue)
        max_for_game["green"] = max(max_for_game["green"], num_green)
    return max_for_game


def part_2(_input) -> None:
    power_total = 0
    for game in _input.split("\n"):
        if not game:
            continue
        min_for_game = find_max_for_game(game)

        power_total += min_for_game["red"] * min_for_game["blue"] * min_for_game["green"]

    print(power_total)


def main() -> None:
    with open("input.txt", "r") as file:
        _input = file.read()
    part_1(_input)
    part_2(_input)


if __name__ == "__main__":
    main()

import re


sample_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


class Board:
    def __init__(self, _input):
        self.my_board = []
        for line in _input.split("\n"):
            line = self.replace_single_digits(list(line))
            self.my_board.append(list(line))

    @staticmethod
    def replace_single_digits(line):
        current_int = {"number": "", "idxs": []}
        for x in range(len(line)):
            if line[x].isdigit():
                current_int["number"] += line[x]
                current_int["idxs"].append(x)
            else:
                if current_int["number"]:
                    for idx in current_int["idxs"]:
                        line[idx] = current_int["number"]
                    current_int = {"number": "", "idxs": []}

        if current_int["number"]:
            for idx in current_int["idxs"]:
                line[idx] = current_int["number"]
        return line

    def _is_out_of_bounds(self, x, y):
        return x >= len(self.my_board) or x < 0 or y >= len(self.my_board[x]) or y < 0

    @staticmethod
    def _neighbor_idxs(x, y):
        return [
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
        ]

    def find_adjacent_parts(self, x, y):
        return [
            neighbor
            for neighbor in self._neighbor_idxs(x, y)
            if not self._is_out_of_bounds(*neighbor)
        ]

    def __str__(self):
        str_rep = ""
        for line in self.my_board:
            str_rep += str(line) + "\n"
        return str_rep


def is_symbol(entry):
    return bool(re.search(r"[$%/=+*&\-#@]+", entry))


def part_1(_input) -> None:
    board = Board(_input)
    parts = []
    for idx, row in enumerate(board.my_board):
        for idy, entry in enumerate(row):
            if is_symbol(entry):
                valid_adjacent_parts = board.find_adjacent_parts(idx, idy)
                numbers_adjacent_to_symbol = set(
                    [
                        int(board.my_board[x][y])
                        for x, y in valid_adjacent_parts
                        if board.my_board[x][y] != "." and not is_symbol(board.my_board[x][y])
                    ]
                )
                parts += list(numbers_adjacent_to_symbol)

    # print(parts)
    print(sum(list(parts)))
    return parts


def main():
    with open("input.txt", "r") as file:
        _input = file.read()
    # print(set(_input) - set(string.digits))

    part_1(_input)
    # print(set([int(x) for x in _input.split(".") if x.isdigit()]) - parts)
    all_parts = [int(x) for x in _input.split(".") if x.isdigit()]
    # print(all_parts)
    print(sum(all_parts))
    part_2(_input)


if __name__ == "__main__":
    main()

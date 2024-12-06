"""
--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?
"""

import dataclasses

from aoc_2024.utils import load_input


@dataclasses.dataclass
class Index:
    x: int
    y: int


RANGE_OF_IDXS_T = list[tuple[int, int]]
SEARCH_IDX_T = list[RANGE_OF_IDXS_T]


def indices(start_x: int, start_y: int) -> SEARCH_IDX_T:
    """Search indices"""
    return [
        # Horizontal
        [(start_x, start_y + shift) for shift in range(4)],
        [(start_x, start_y - shift) for shift in range(4)],
        # Vertical
        [(start_x + shift, start_y) for shift in range(4)],
        [(start_x - shift, start_y) for shift in range(4)],
        # Diagonals
        [(start_x + shift, start_y + shift) for shift in range(4)],
        [(start_x + shift, start_y - shift) for shift in range(4)],
        [(start_x - shift, start_y + shift) for shift in range(4)],
        [(start_x - shift, start_y - shift) for shift in range(4)],
    ]


def _retrieve_text_for_range(
    input_matrix: list[list[str]], range_of_idxs: RANGE_OF_IDXS_T
) -> str:
    try:
        text_list = [
            input_matrix[x][y] if x >= 0 and y >= 0 else "" for x, y in range_of_idxs
        ]
        return "".join(text_list)
    except IndexError:
        return ""


def part_1(input_matrix: list[list[str]]) -> int:
    total_xmases = 0
    for i, row in enumerate(input_matrix):
        for j, col in enumerate(row):
            if col == "X":
                idxs_to_search = indices(i, j)
                for _range in idxs_to_search:
                    text = _retrieve_text_for_range(input_matrix, _range)
                    if text == "XMAS":
                        total_xmases += 1

    return total_xmases


def part_2(input_text: list[list[str]]) -> int:
    pass


def main():
    raw_input = load_input()
    input_list = raw_input.split("\n")
    input_matrix = []
    for row in input_list:
        input_matrix.append(list(row))
    part_1_answer = part_1(input_matrix)
    print(f"Part 1 result: {part_1_answer}")

    part_2_answer = part_2(input_list)
    print(f"Part 2 result: {part_2_answer}")


if __name__ == "__main__":
    main()

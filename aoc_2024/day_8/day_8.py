"""
--- Day 8: Resonant Collinearity ---
You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........
Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........
The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?


"""

import dataclasses
import time
from collections import defaultdict
from typing import List, Self


from aoc_2024.utils import load_input


example_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


@dataclasses.dataclass
class Location:
    freq: str | None
    anti_node: set[str]

    def __repr__(self):
        if self.freq:
            return self.freq

        if self.anti_node:
            return "#"

        else:
            return "."


class Graph:
    def __init__(self, location_list: List[List[Location]]):
        self.location_list = location_list
        self.freq_locations = self._unique_freqs()

    @classmethod
    def from_raw_input(cls, raw_input: str) -> Self:
        location_list = []
        for row in raw_input.split("\n"):
            location_list.append(
                [Location(x if x != "." else None, set()) for x in list(row)]
            )

        return cls(location_list)

    def _unique_freqs(self) -> dict[str, set[tuple[int, int]]]:
        freq_locations = defaultdict(set)
        for i, row in enumerate(self.location_list):
            for j, location in enumerate(row):
                if location.freq:
                    freq_locations[location.freq].add((i, j))
        return freq_locations

    def _calculate_antinode_location(
        self, node_a: tuple[int, int], node_b: tuple[int, int]
    ) -> tuple[int, int]:
        new_i = node_a[0] + (node_a[0] - node_b[0])
        new_j = node_a[1] + (node_a[1] - node_b[1])
        return new_i, new_j

    def _calculate_antidote_offset(
        self, node_a: tuple[int, int], node_b: tuple[int, int]
    ):
        return (node_a[0] - node_b[0]), (node_a[1] - node_b[1])

    def _populate_antinodes_for_freq(
        self, freq: str, set_of_locations: set[tuple[int, int]]
    ) -> None:
        for curr_node in set_of_locations:
            for other_node in set_of_locations:
                if curr_node == other_node:
                    continue
                anti_node_location_i, anti_node_location_j = (
                    self._calculate_antinode_location(curr_node, other_node)
                )
                if 0 <= anti_node_location_i < len(
                    self.location_list
                ) and 0 <= anti_node_location_j < len(
                    self.location_list[anti_node_location_i]
                ):
                    self.location_list[anti_node_location_i][
                        anti_node_location_j
                    ].anti_node.add(freq)

    def _populate_antinodes_for_freq_pt2(
        self, freq: str, set_of_locations: set[tuple[int, int]]
    ) -> None:
        for curr_node in set_of_locations:
            for other_node in set_of_locations:
                if curr_node == other_node:
                    continue
                offset_i, offset_j = self._calculate_antidote_offset(
                    curr_node, other_node
                )
                anti_node_location_i = curr_node[0] + offset_i
                anti_node_location_j = curr_node[1] + offset_j

                while 0 <= anti_node_location_i < len(
                    self.location_list
                ) and 0 <= anti_node_location_j < len(
                    self.location_list[anti_node_location_i]
                ):
                    self.location_list[anti_node_location_i][
                        anti_node_location_j
                    ].anti_node.add(freq)

                    anti_node_location_i += offset_i
                    anti_node_location_j += offset_j

    def populate_antinodes_pt1(self) -> None:
        for freq, set_of_locations in self.freq_locations.items():
            # add the antinode for each location with every other location
            self._populate_antinodes_for_freq(freq, set_of_locations)

    def populate_antinodes_pt2(self) -> None:
        for freq, set_of_locations in self.freq_locations.items():
            # add the antinode for each location with every other location
            self._populate_antinodes_for_freq_pt2(freq, set_of_locations)

    def num_unique_antinode_locations(self) -> int:
        unique_locations = set()
        for i, row in enumerate(self.location_list):
            for j, location in enumerate(row):
                if location.freq:
                    unique_locations.add((i, j))
                if len(location.anti_node) > 0:
                    unique_locations.add((i, j))

        return len(unique_locations)

    def __repr__(self):
        _repr = ""
        for row in self.location_list:
            for j in row:
                _repr += str(j)
            _repr += "\n"
        return _repr


def part_1(raw_input: str) -> int:
    my_graph = Graph.from_raw_input(raw_input)
    my_graph.populate_antinodes_pt1()
    return my_graph.num_unique_antinode_locations()


def part_2(raw_input: str) -> int:
    my_graph = Graph.from_raw_input(raw_input)
    my_graph.populate_antinodes_pt2()
    print(my_graph)
    return my_graph.num_unique_antinode_locations()


def main():
    raw_input = load_input()
    # raw_input = example_input

    start_time = time.time()
    part_1_answer = part_1(raw_input)
    print(f"Part 1 result: {part_1_answer}")
    end_time = time.time()
    print(f"Part 1 time: {end_time - start_time:.4f} seconds\n")

    start_time = time.time()
    part_2_answer = part_2(raw_input)
    print(f"Part 2 result: {part_2_answer}")
    end_time = time.time()
    print(f"Part 2 time: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    main()

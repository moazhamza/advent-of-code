"""--- Day 9: Disk Fragmenter ---
Another push of the button leaves you in the familiar hallways of some friendly amphipods! Good thing you each somehow got your own personal mini submarine. The Historians jet away in search of the Chief, mostly by driving directly into walls.

While The Historians quickly figure out how to pilot these things, you notice an amphipod in the corner struggling with his computer. He's trying to make more contiguous free space by compacting all of the files, but his program isn't working; you offer to help.

He shows you the disk map (your puzzle input) he's already generated. For example:

2333133121414131402
The disk map uses a dense format to represent the layout of files and free space on the disk. The digits alternate between indicating the length of a file and the length of free space.

So, a disk map like 12345 would represent a one-block file, two blocks of free space, a three-block file, four blocks of free space, and then a five-block file. A disk map like 90909 would represent three nine-block files in a row (with no free space between them).

Each file on disk also has an ID number based on the order of the files as they appear before they are rearranged, starting with ID 0. So, the disk map 12345 has three files: a one-block file with ID 0, a three-block file with ID 1, and a five-block file with ID 2. Using one character for each block where digits are the file ID and . is free space, the disk map 12345 represents these individual blocks:

0..111....22222
The first example above, 2333133121414131402, represents these individual blocks:

00...111...2...333.44.5555.6666.777.888899
The amphipod would like to move file blocks one at a time from the end of the disk to the leftmost free space block (until there are no gaps remaining between file blocks). For the disk map 12345, the process looks like this:

0..111....22222
02.111....2222.
022111....222..
0221112...22...
02211122..2....
022111222......
The first example requires a few more steps:

00...111...2...333.44.5555.6666.777.888899
009..111...2...333.44.5555.6666.777.88889.
0099.111...2...333.44.5555.6666.777.8888..
00998111...2...333.44.5555.6666.777.888...
009981118..2...333.44.5555.6666.777.88....
0099811188.2...333.44.5555.6666.777.8.....
009981118882...333.44.5555.6666.777.......
0099811188827..333.44.5555.6666.77........
00998111888277.333.44.5555.6666.7.........
009981118882777333.44.5555.6666...........
009981118882777333644.5555.666............
00998111888277733364465555.66.............
0099811188827773336446555566..............
The final step of this file-compacting process is to update the filesystem checksum. To calculate the checksum, add up the result of multiplying each of these blocks' position with the file ID number it contains. The leftmost block is in position 0. If a block contains free space, skip it instead.

Continuing the first example, the first few blocks' position multiplied by its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on. In this example, the checksum is the sum of these, 1928.

Compact the amphipod's hard drive using the process he requested. What is the resulting filesystem checksum? (Be careful copy/pasting the input for this puzzle; it is a single, very long line.)"""

import dataclasses
import time
from typing import Dict, List, Self

from aoc_2024.utils import load_input


example_input = "2333133121414131402"


class FileSystem:
    def __init__(self, disk_map: List[str]):
        self.disk_map = disk_map

    @classmethod
    def from_raw_input(cls, raw_input: str) -> Self:
        disk_map = []
        file_id = 0
        for odd_or_even, file_size in enumerate(raw_input):
            if odd_or_even % 2 == 0:
                disk_map.extend([str(file_id)] * int(file_size))
                file_id += 1
            else:
                disk_map.extend(["."] * int(file_size))
        return cls(disk_map)

    def _find_first_free_space(self, starting_at: int) -> int:
        for i, val in enumerate(self.disk_map[starting_at:]):
            if val == ".":
                return i + starting_at

        return len(self.disk_map) + 1

    def compact_disk_map(self) -> None:
        # Find first free space
        free_space_idx = self._find_first_free_space(0)
        # Pop the file from the end
        while free_space_idx < len(self.disk_map):
            file_to_move = self.disk_map.pop()
            if file_to_move == ".":
                continue
            self.disk_map[free_space_idx] = file_to_move
            free_space_idx = self._find_first_free_space(free_space_idx + 1)

    def calculate_checksum(self) -> int:
        checksum = 0
        for pos, val in enumerate(self.disk_map):
            checksum += pos * int(val)

        return checksum


class FileSystemOptimized(FileSystem):
    def calculate_checksum(self) -> int:
        checksum = 0

        left_ptr = 0
        right_ptr = len(self.disk_map) - 1

        while left_ptr <= right_ptr:
            left_val = self.disk_map[left_ptr]
            if left_val == ".":
                right_val = self.disk_map[right_ptr]
                while right_val == ".":
                    right_ptr -= 1
                    right_val = self.disk_map[right_ptr]
                left_val = right_val
                right_ptr -= 1

            checksum += left_ptr * int(left_val)
            left_ptr += 1

        return checksum


@dataclasses.dataclass
class _File:
    id: int
    size: int


@dataclasses.dataclass
class _FreeSpace:
    size: int


DISK_ENTRY_T = List[_File | _FreeSpace]


class FileSystemPt2:
    def __init__(self, disk_map: DISK_ENTRY_T):
        self.disk_map = disk_map

    @classmethod
    def from_raw_input(cls, raw_input: str) -> Self:
        disk_map: DISK_ENTRY_T = []

        file_id = 0
        for odd_or_even, file_size in enumerate(raw_input):
            if odd_or_even % 2 == 0:
                disk_map.append(_File(id=file_id, size=int(file_size)))
                file_id += 1
            else:
                if int(file_size) > 0:
                    disk_map.append(_FreeSpace(size=int(file_size)))
        return cls(disk_map)

    def _find_largest_file_id(self) -> int:
        for i in range(len(self.disk_map) - 1, 0, -1):
            block = self.disk_map[i]
            if isinstance(block, _File):
                return block.id

        return -1

    def _find_open_space(self, size: int, end_idx: int) -> int | None:
        for idx, block in enumerate(self.disk_map):
            if idx >= end_idx:
                return None
            if isinstance(block, _FreeSpace) and block.size >= size:
                return idx
        return None

    def compact_diskmap(self) -> None:
        largest_id = self._find_largest_file_id()

        lookup_index = len(self.disk_map) - 1
        for file_id in range(largest_id, 0, -1):
            file_to_move = self.disk_map[lookup_index]
            while not isinstance(file_to_move, _File) or not file_id == file_to_move.id:
                lookup_index -= 1
                file_to_move = self.disk_map[lookup_index]
                continue

            # We now have the next file_id to move
            # Find space to move it
            idx_to_move_to = self._find_open_space(file_to_move.size, lookup_index)
            if not idx_to_move_to:
                continue

            free_space = self.disk_map[idx_to_move_to]
            new_free_space_size = free_space.size - file_to_move.size
            if new_free_space_size >= 0:
                # Create new free_space block
                self.disk_map.insert(
                    idx_to_move_to + 1, _FreeSpace(new_free_space_size)
                )
                # Insert the new block
                self.disk_map[idx_to_move_to] = file_to_move
                # Remove the old block
                self.disk_map[lookup_index + 1] = _FreeSpace(file_to_move.size)
            # print(
            #     "".join(
            #         str(x.id) * x.size if isinstance(x, _File) else "." * x.size
            #         for x in self.disk_map
            #     )
            # )

    def calculate_checksum(self) -> int:
        checksum = 0
        idx = 0
        for block in self.disk_map:
            if isinstance(block, _File):
                for i in range(1, block.size + 1):
                    checksum += block.id * idx
                    idx += 1
            else:
                for i in range(1, block.size + 1):
                    idx += 1

        return checksum

    def _find_file_to_move(self, size: int, i: int) -> bool:
        # Find a file to move that is at most size big
        for j in range(len(self.disk_map) - 1, i, -1):
            if isinstance(self.disk_map[j], _File) and self.disk_map[j].size <= size:
                # calculate how much free space is left
                free_space = size - self.disk_map[j].size
                # Move the file
                self.disk_map[i] = self.disk_map[j]
                # Update the free space
                self.disk_map[j] = _FreeSpace(size=free_space)
                self.disk_map.insert(i + 1, _FreeSpace(size=free_space))

                return True

        # If no file is found, you're done
        return False


def part_1(raw_input: str) -> int:
    my_file_system = FileSystemOptimized.from_raw_input(raw_input)
    return my_file_system.calculate_checksum()


def part_2(raw_input: str) -> int:
    my_file_system = FileSystemPt2.from_raw_input(raw_input)
    my_file_system.compact_diskmap()
    return my_file_system.calculate_checksum()


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

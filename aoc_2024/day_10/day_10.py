import time

from aoc_2024.utils import load_input


def part_1(raw_input: str) -> int:
    pass


def part_2(raw_input: str) -> int:
    pass


def main():
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

from typing import List


def load_input() -> List[str]:
    with open("input.txt") as file:
        return file.read().strip().split("\n")

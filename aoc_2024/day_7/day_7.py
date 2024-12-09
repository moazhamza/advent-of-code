"""--- Day 7: Bridge Repair ---
The Historians take you to a familiar rope bridge over a river in the middle of a jungle. The Chief isn't on this side of the bridge, though; maybe he's on the other side?

When you go to cross the bridge, you notice a group of engineers trying to repair it. (Apparently, it breaks pretty frequently.) You won't be able to cross until it's fixed.

You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:

190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators, two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.
The engineers just need the total calibration result, which is the sum of the test values from just the equations that could possibly be true. In the above example, the sum of the test values for the three equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?

"""

import concurrent
import itertools
from concurrent.futures.process import ProcessPoolExecutor
from functools import cache
from typing import List

from tqdm import tqdm

from aoc_2024.utils import load_input

example_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

OPERATORS = ["*", "+"]
NEW_OPERATORS = ["*", "+", "||"]


def fill_place_holders(operand_list: List[str]) -> str:
    operands = operand_list.copy()
    if len(operands) == 2:
        return operands[0] + " _ " + operands[1]

    new_first_operand = operands[0] + " _ " + operands[1]
    operands[0] = new_first_operand
    operands.pop(1)
    return fill_place_holders(operands)


@cache
def dont_do_pemdas(original_equation: str) -> int:
    equation = original_equation.split(" ")
    if len(equation) == 3:
        if equation[1] == "||":
            return int(equation[0] + equation[2])

        return eval("".join(equation))

    first_part = str(dont_do_pemdas(" ".join(equation[0:3])))

    equation[0] = first_part
    equation.pop(1)
    equation.pop(1)
    return dont_do_pemdas(" ".join(equation))


def is_possible(total: int, operands: List[str], operators: List[str]) -> int:
    # Number of places an operation can go
    num_choices = len(operands) - 1
    # List of operations with "_" filled in between them
    place_holders_list = fill_place_holders(operands).split(" ")

    # n different combos of "*" and "+" where n=number of spots available
    combos = itertools.product(operators, repeat=num_choices)
    # Try every combo of * and +
    for combo in combos:
        num_inserted = 0

        # Replace the placeholder (or last operation) with the new operation
        for choice in range(num_choices):
            place_holders_list[choice + num_inserted + 1] = combo[choice]
            num_inserted += 1

        # Turn them into an equation list
        equation_str = " ".join(place_holders_list)
        if dont_do_pemdas(equation_str) == int(total):
            return total
    return 0


def part_1(raw_input: str) -> int:
    list_of_equations = raw_input.split("\n")

    futures = []
    with tqdm(total=len(list_of_equations)) as pbar:
        with ProcessPoolExecutor() as executor:
            for equation in list_of_equations:
                split_eq = equation.split(": ")
                total = int(split_eq[0])
                operands = split_eq[1].split(" ")
                futures.append(executor.submit(is_possible, total, operands, OPERATORS))

            for _ in concurrent.futures.as_completed(futures):
                pbar.update()

    return sum([x.result() for x in futures])


def part_2(raw_input: str) -> int:
    list_of_equations = raw_input.split("\n")

    futures = []
    with tqdm(total=len(list_of_equations)) as pbar:
        with ProcessPoolExecutor(1) as executor:
            for equation in list_of_equations:
                split_eq = equation.split(": ")
                total = int(split_eq[0])
                operands = split_eq[1].split(" ")
                futures.append(
                    executor.submit(is_possible, total, operands, NEW_OPERATORS)
                )

            for _ in concurrent.futures.as_completed(futures):
                pbar.update()

    return sum([x.result() for x in futures])


def main():
    raw_input = load_input()
    # raw_input = example_input

    part_1_answer = part_1(raw_input)
    print(f"Part 1 result: {part_1_answer}\n")

    part_2_answer = part_2(raw_input)
    print(f"Part 2 result: {part_2_answer}")


if __name__ == "__main__":
    main()

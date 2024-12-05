"""
--- Day 2: Red-Nosed Reports ---
Fortunately, the first location The Historians want to search isn't a long walk from the Chief Historian's office.

While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain no sign of the Chief Historian, the engineers there run up to you as soon as they see you. Apparently, they still talk about the time Rudolph was saved through molecular synthesis from a single electron.

They're quick to add that - since you're already here - they'd really appreciate your help analyzing some unusual data from the Red-Nosed reactor. You turn to check if The Historians are waiting for you, but they seem to have already divided into groups that are currently searching every corner of the facility. You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report per line. Each report is a list of numbers called levels that are separated by spaces. For example:

7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?

--- Part Two ---
The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

7 6 4 2 1: Safe without removing any level.
1 2 7 8 9: Unsafe regardless of which level is removed.
9 7 6 2 1: Unsafe regardless of which level is removed.
1 3 2 4 5: Safe by removing the second level, 3.
8 6 4 4 1: Safe by removing the third level, 4.
1 3 6 7 9: Safe without removing any level.
Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?
"""

import dataclasses
from enum import StrEnum
from typing import List

from aoc_2024.utils import load_input


class SafetyReason(StrEnum):
    UNIFORMITY = "uniform"
    LARGE_DIFF = "difference"


@dataclasses.dataclass
class SafetyResult:
    safe: bool
    ascending: bool = True

    bad_index: int = -1
    reason: SafetyReason | None = None

    def __bool__(self) -> bool:
        return self.safe


def _is_safe(level_list: List[int]) -> SafetyResult:
    ascending = True if level_list[0] < level_list[1] else False

    if not ascending:
        level_list = list(reversed(level_list))

    for i in range(0, len(level_list) - 1):
        if level_list[i] >= level_list[i + 1]:
            return SafetyResult(False, ascending, i, SafetyReason.UNIFORMITY)
        diff = level_list[i + 1] - level_list[i]
        if diff > 3 or diff < 1:
            return SafetyResult(False, ascending, i, SafetyReason.LARGE_DIFF)

    return SafetyResult(True)


def part_1(input_list: List[str]) -> int:
    num_safe_reports = 0
    for report in input_list:
        report_list = [int(level) for level in report.split(" ")]

        ascending = True if report_list[0] < report_list[1] else False

        safe = True
        if not ascending:
            report_list = list(reversed(report_list))

        for i in range(0, len(report_list) - 1):
            if report_list[i] >= report_list[i + 1]:
                safe = False
                break
            diff = report_list[i + 1] - report_list[i]
            if diff > 3 or diff < 1:
                safe = False
                break
        if safe:
            num_safe_reports += 1

    return num_safe_reports


def part_1_updated(input_list: List[str]) -> int:
    num_safe_reports = 0
    for report in input_list:
        report_list = [int(level) for level in report.split(" ")]

        report_is_safe = _is_safe(report_list)
        if report_is_safe:
            num_safe_reports += 1
    return num_safe_reports


def _dampen_list(report_list: List[int], bad_index: int) -> bool:
    new_list = list(report_list)
    # If the report is not safe, try to remove one of the problem levels
    new_list.pop(bad_index)

    return _is_safe(new_list).safe


def _is_safe_pt_2(level_list: List[int]) -> bool:
    original_report_is_safe = _is_safe(level_list)
    safe = original_report_is_safe.safe
    if not safe:
        for problem_index in range(len(level_list)):
            # Try removing that problem index
            safe = _dampen_list(level_list, problem_index)
            if safe:
                return True
    else:
        return True
    return False


def part_2(input_list: List[str]) -> int:
    num_safe_reports = 0
    for report in input_list:
        report_list = [int(level) for level in report.split(" ")]
        if _is_safe_pt_2(report_list):
            num_safe_reports += 1

    return num_safe_reports


def main():
    input_list = load_input()
    part_1_answer = part_1(input_list)
    print(f"Part 1 result: {part_1_answer}")
    part_1_updated_answer = part_1_updated(input_list)
    print(f"Part 1 updated result: {part_1_updated_answer}")

    part_2_answer = part_2(input_list)
    print(f"Part 2 result: {part_2_answer}")


if __name__ == "__main__":
    main()

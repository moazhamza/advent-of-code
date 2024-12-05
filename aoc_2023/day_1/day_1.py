"""--- Day 1: Trebuchet?! ---

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?
"""


def find_first_digit(line: str) -> int:
    """Finds the first digit in a line of text.
    Args:
        line: the text

    Returns:
        the first digit in the line
    """
    for char in line:
        if char.isdigit():
            return int(char)


def find_last_digit(line: str) -> int:
    """Finds the last digit in a line of text.
    Args:
        line: the text

    Returns:
        the last digit in the line
    """
    for char in reversed(line):
        if char.isdigit():
            return int(char)


def part_1() -> None:
    """Answer to part 1

    Returns:

    """
    total = 0
    with open("input.txt", "r") as f:
        for line in f:
            first_digit = find_first_digit(line)
            last_digit = find_last_digit(line)
            total += first_digit * 10 + last_digit
    print(total)


digit_look_up_dict = {
    "o": {"one": 1},
    "t": {"two": 2, "three": 3},
    "f": {
        "four": 4,
        "five": 5,
    },
    "s": {
        "six": 6,
        "seven": 7,
    },
    "e": {
        "eight": 8,
    },
    "n": {"nine": 9},
}


def find_first_digit_with_words(line: str) -> int:
    """Args:
        line:

    Returns:

    """
    for idx, char in enumerate(line):
        # if it's a number, then return it
        if char.isdigit():
            return int(char)

        # Now we know it's not a number
        # if it's a letter, and it's one of the letters that start a number
        if char in digit_look_up_dict:
            # then check all the numbers that start with this letter
            for digit_word in digit_look_up_dict[char].keys():
                # if the rest of the line isn't long enough to contain the digit word, then skip it
                if idx + len(digit_word) >= len(line):
                    continue
                # look at where the digit word should be starting with the character
                if line[idx : idx + len(digit_word)] == digit_word:
                    # if it's the number we're looking for, then return it
                    return digit_look_up_dict[char][digit_word]


def find_last_digit_with_words(line: str) -> int:
    """Args:
        line:

    Returns:

    """
    last_seen = 0
    for idx, char in enumerate(line):
        # if it's a number, then return it
        if char.isdigit():
            last_seen = int(char)

        # Now we know it's not a number
        # if it's a letter, and it's one of the letters that start a number
        if char in digit_look_up_dict:
            # then check all the numbers that start with this letter
            for digit_word in digit_look_up_dict[char].keys():
                # if the rest of the line isn't long enough to contain the digit word, then skip it
                if idx + len(digit_word) >= len(line):
                    continue
                # look at where the digit word should be starting with the character
                if line[idx : idx + len(digit_word)] == digit_word:
                    # if it's the number we're looking for, then return it
                    last_seen = digit_look_up_dict[char][digit_word]
    return last_seen


def part_2() -> None:
    """It looks like some of the digits are actually spelled out with letters:
    one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".
    """
    total = 0
    with open("input.txt", "r") as f:
        for line in f:
            total += find_first_digit_with_words(line) * 10 + find_last_digit_with_words(line)

    print(total)


def main() -> None:
    part_1()
    part_2()


if __name__ == "__main__":
    main()

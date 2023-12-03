from __future__ import annotations

import sys
import timeit
from itertools import chain
from pathlib import Path

import pytest


INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(s: str) -> int:
    numbers_map = {}
    symbols_map = {}
    for line_index, line in enumerate(s.splitlines()):
        digit_start = -1
        for char_index, char in enumerate(chain(line, ".")):
            if char.isdigit():
                if digit_start < 0:
                    digit_start = char_index
                continue
            elif digit_start >= 0:
                number = int(line[digit_start:char_index])
                for digit_index in range(digit_start, char_index):
                    numbers_map[(line_index, digit_index)] = (number, (line_index, digit_start))
                digit_start = -1
            if char != ".":
                symbols_map[(line_index, char_index)] = char

    numbers_sum = 0
    numbers = []
    for line_index, char_index in symbols_map:
        adjacent_coordinates = [
            (line_index - 1, char_index),
            (line_index + 1, char_index),
            (line_index, char_index - 1),
            (line_index, char_index + 1),
            # and diagonals
            (line_index - 1, char_index - 1),
            (line_index - 1, char_index + 1),
            (line_index + 1, char_index - 1),
            (line_index + 1, char_index + 1),
        ]
        adjacent_numbers = set()
        for coord_id, coord in enumerate(adjacent_coordinates):
            if coord in numbers_map:
                adjacent_numbers.add(numbers_map[coord])
        numbers_sum += sum(number for number, *_ in adjacent_numbers)
        numbers.extend(adjacent_numbers)

    return numbers_sum


INPUT_S = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
EXPECTED = 4361

INPUT_S2 = """\
12.......*..
+.........34
.......-12..
..78........
..*....60...
78.........9
.5.....23..$
8...90*12...
............
2.2......12.
.*.........*
1.1..503+.56
"""
EXPECTED2 = 925

@pytest.mark.parametrize("input_s,expected", [
        (INPUT_S, EXPECTED),
        (INPUT_S2, EXPECTED2),
    ],
)
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 531932


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


if __name__ == "__main__":
    input_data = read_input()
    print("Answer is:", compute(input_data))

    if "-b" in sys.argv:
        number_of_runs = 1000
        bench_time = timeit.timeit(
            "compute(data)",
            setup="from __main__ import compute",
            globals={"data": input_data},
            number=number_of_runs,
        )
        print(f"{number_of_runs} runs took {bench_time} seconds")

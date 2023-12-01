from __future__ import annotations

import heapq
import os
from typing import Iterable

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

SPELLED_NUMBERS = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def iter_all_occurrences(text: str, sub: str):
    start = 0
    while True:
        start = text.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)


def _replace_spelled_numbers(text: str, *, direction: int) -> str:
    to_replace = []
    for num, spelled_number in enumerate(SPELLED_NUMBERS, start=1):
        for index in iter_all_occurrences(text, spelled_number):
            heapq.heappush(to_replace, (index * direction, index, spelled_number, str(num)))
    while to_replace:
        _, index, old_number, new_number = heapq.heappop(to_replace)
        text = text[:index] + text[index:].replace(old_number, new_number, 1)
    return text


def compute(s: str) -> int:
    result = 0
    for line in s.splitlines():
        left_line = _replace_spelled_numbers(line, direction=1)
        right_line = _replace_spelled_numbers(line, direction=-1)
        left_number = _find_first_number(left_line)
        right_number = _find_first_number(reversed(right_line))
        result += left_number * 10 + right_number
    return result


def _find_first_number(text: Iterable[str]) -> int:
    for char in text:
        if char.isdigit():
            return int(char)
    raise ValueError("No number found")



INPUT_S = '''\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''
EXPECTED = 281


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        ("sdonefour77one", 11),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    with open(INPUT_TXT) as f:
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

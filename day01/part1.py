from __future__ import annotations

import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    result = 0
    for line in s.splitlines():
        left = 0
        right = len(line) - 1
        left_number = -1
        right_number = -1
        while left <= right:
            if left_number >= 0 and right_number >= 0:
                break

            if left_number < 0:
                left_char = line[left]
                if left_char.isdigit():
                    left_number = int(left_char)
                    continue
                left += 1
            if right_number < 0:
                right_char = line[right]
                if right_char.isdigit():
                    right_number = int(right_char)
                    continue
                right -= 1
        result += left_number * 10 + right_number
    return result


INPUT_S = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
EXPECTED = 142


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    with open(INPUT_TXT) as f:
        result = compute(f.read())

    assert result == 54953


def main() -> int:
    with open(INPUT_TXT) as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

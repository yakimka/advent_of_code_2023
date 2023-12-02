from __future__ import annotations

import os

import pytest

from support import iter_lines_as_numbers

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    for num in iter_lines_as_numbers(s):
        pass

    for line in s.splitlines():
        pass

    return 0


INPUT_S = """\
"""
EXPECTED = 21000


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


@pytest.mark.skip("Set answer for refactoring")
def test_input() -> None:
    with open(INPUT_TXT) as f:
        result = compute(f.read())

    assert result == 0


def main() -> int:
    with open(INPUT_TXT) as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

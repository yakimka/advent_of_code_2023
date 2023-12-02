from __future__ import annotations

import sys
import timeit
from pathlib import Path

import pytest

from support import iter_lines_as_numbers

INPUT_TXT = Path(__file__).parent / "input.txt"


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

from __future__ import annotations

import sys
import timeit
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(s: str) -> int:
    lines = s.splitlines()
    time = _line_to_int(lines[0])
    distance = _line_to_int(lines[1])

    range_len = time + 1
    range_middle = range_len // 2

    index_start = bisect_right_range(0, range_middle, distance, key=_key(time))
    num_variants = 2 * (range_middle - index_start) + range_len % 2
    return num_variants


def _key(time: int):
    return lambda x: (time - x) * x


def bisect_right_range(i_start, i_end, x, *, key):
    if i_start < 0:
        raise ValueError("i_start must be non-negative")
    while i_start < i_end:
        mid = (i_start + i_end) // 2
        if x < key(mid):
            i_end = mid
        else:
            i_start = mid + 1
    return i_start


def _line_to_int(line: str) -> int:
    _, nums = line.split(":")
    return int(nums.strip().replace(" ", ""))


INPUT_S = """\
Time:      7  15   30
Distance:  9  40  200
"""
EXPECTED = 71503


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 38220708


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


if __name__ == "__main__":
    input_data = read_input()
    print("Answer is:     ", compute(input_data))

    if "-b" in sys.argv:
        number_of_runs = 1000
        bench_time = timeit.timeit(
            "compute(data)",
            setup="from __main__ import compute",
            globals={"data": input_data},
            number=number_of_runs,
        )
        print(f"{number_of_runs} runs took: {bench_time}s")
        one_run = sup.humanized_seconds(bench_time / number_of_runs)
        print(f"Average time:   {one_run}")

from __future__ import annotations

import bisect
import sys
import timeit
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(s: str) -> int:
    lines = s.splitlines()
    time_data = _line_to_ints(lines[0])
    distance_data = _line_to_ints(lines[1])

    result = 1
    for time, distance in zip(time_data, distance_data):
        range_len = time + 1
        range_middle = range_len // 2
        timeline = list(range(range_middle))
        index_start = bisect.bisect_right(timeline, distance, key=_key(time))
        num_variants = 2 * (range_middle - index_start) + range_len % 2
        result *= num_variants

    return result


def _key(time: int):
    return lambda x: (time - x) * x


def _line_to_ints(line: str) -> list[int]:
    _, nums = line.split(":")
    return [int(nums.strip().replace(" ", ""))]


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

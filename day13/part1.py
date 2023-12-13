from __future__ import annotations

import sys
import timeit
from itertools import chain
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(s: str) -> int:
    pattern = []
    result = 0
    for line in chain(s.splitlines(), [""]):
        if not line:
            if pattern:
                if (line := search_horizontal_reflection_line(pattern)) is not None:
                    result += line * 100
                elif (
                    line := search_horizontal_reflection_line(
                        flip_matrix_by_90(pattern)
                    )
                ) is not None:
                    result += line
            pattern = []
            continue
        pattern.append(list(line))

    return result


def flip_matrix_by_90(matrix):
    return [list(reversed(row)) for row in zip(*matrix)]


def search_horizontal_reflection_line(pattern) -> int | None:
    for i in range(0, len(pattern) - 1):
        if check_horizontal_symmetry(pattern, i):
            return i + 1

    return None


def check_horizontal_symmetry(pattern, i) -> bool:
    for i, j in zip(range(i, -1, -1), range(i + 1, len(pattern))):
        if pattern[i] != pattern[j]:
            return False

    return True


INPUT_S = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
EXPECTED = 405


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 37561


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

from __future__ import annotations

import sys
import timeit
from functools import cache
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
                    line := search_horizontal_reflection_line(flip_matrix(pattern))
                ) is not None:
                    result += line
            pattern = []
            continue
        pattern.append(tuple(line))

    return result


def flip_matrix(matrix):
    return [row for row in zip(*matrix)]


def search_horizontal_reflection_line(pattern) -> int | None:
    for line in range(0, len(pattern) - 1):
        smudges_cleared = 0
        for i, j in zip(range(line, -1, -1), range(line + 1, len(pattern))):
            pattern1 = row_to_int(pattern[i])
            pattern2 = row_to_int(pattern[j])
            if pattern1 != pattern2:
                if smudges_cleared == 0 and (pattern1 ^ pattern2).bit_count() == 1:
                    smudges_cleared += 1
                else:
                    break
        else:
            if smudges_cleared == 1:
                return line + 1

    return None


def check_horizontal_symmetry(pattern, i) -> bool:
    for i, j in zip(range(i, -1, -1), range(i + 1, len(pattern))):
        if pattern[i] != pattern[j]:
            return False

    return True


@cache
def row_to_int(row: tuple[str]) -> int:
    return int("".join("1" if c == "#" else "0" for c in row), 2)


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
EXPECTED = 400


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 31108


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

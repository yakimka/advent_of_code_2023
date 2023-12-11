from __future__ import annotations

import itertools
import sys
import timeit
from contextlib import suppress
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(s: str) -> int:
    lines = s.splitlines()
    galaxy = []
    clear_rows = list(range(len(lines)))
    clear_cols = list(range(len(lines[0])))
    planets = []
    for x, line in enumerate(s.splitlines()):
        galaxy.append([])
        for y, char in enumerate(line):
            if char == "#":
                with suppress(ValueError):
                    clear_rows.remove(x)
                with suppress(ValueError):
                    clear_cols.remove(y)
                planets.append((x, y))
            galaxy[-1].append(char)

    result = 0
    for p1, p2 in itertools.combinations(planets, 2):
        intersection_x = set(clear_rows) & set(range(min(p1[0], p2[0]), max(p1[0], p2[0])))
        intersection_y = set(clear_cols) & set(range(min(p1[1], p2[1]), max(p1[1], p2[1])))
        x_expand = len(intersection_x)
        y_expand = len(intersection_y)
        x1, y1 = p1
        x2, y2 = p2
        if x1 < x2:
            x2 += x_expand
        else:
            x1 += x_expand
        if y1 < y2:
            y2 += y_expand
        else:
            y1 += y_expand
        result += shortest_path((x1, y1), (x2, y2))
    return result


def shortest_path(coords1: tuple[int, int], coords2: tuple[int, int]) -> int:
    return abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1])


INPUT_S = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
EXPECTED = 374


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 9550717


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

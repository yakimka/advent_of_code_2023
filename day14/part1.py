from __future__ import annotations

import sys
import timeit
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"

Coords = tuple[int, int]


def compute(s: str) -> int:
    bridge = []
    round_rocks = []
    for x, line in enumerate(s.splitlines()):
        beam = []
        for y, c in enumerate(line):
            if c == "O":
                round_rocks.append((x, y))
            beam.append(c)
        bridge.append(beam)
    beams_count = len(bridge)

    stack = list(reversed(round_rocks))
    result = 0
    while stack:
        x, y = stack.pop()
        next_coords = roll_to_up(bridge, x, y)
        if next_coords is None:
            result += beams_count - x
            continue
        new_x, new_y = next_coords
        bridge[new_x][new_y], bridge[x][y] = bridge[x][y], bridge[new_x][new_y]
        stack.append(next_coords)

    return result


def roll_to_up(bridge, x: int, y: int) -> Coords | None:
    if x > 0:
        next_x, next_y = x - 1, y
        if bridge[next_x][next_y] == ".":
            return next_x, next_y

    return None


INPUT_S = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
EXPECTED = 136


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 109833


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

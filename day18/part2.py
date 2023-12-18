from __future__ import annotations

import sys
import timeit
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


DIRECTION_MAP = {
    "0": "right",
    "1": "down",
    "2": "left",
    "3": "up",
}


def compute(s: str) -> int:
    prev_coords = (0, 0)

    coordinates = [prev_coords]
    bounds = 0
    for line in s.splitlines():
        _, instructions = line.split("(")
        direction = DIRECTION_MAP[instructions[-2]]
        steps = int(instructions[1:-2], 16)
        bounds += steps
        x, y = prev_coords
        prev_coords = sup.cartesian_next_coords(x, y, direction, size=steps)
        coordinates.append(prev_coords)

    # https://uk.wikipedia.org/wiki/Формула_площі_Гаусса#Складніший_приклад
    area_in = 0
    area_out = 0
    for i in range(len(coordinates)):
        x1, y1 = coordinates[i]
        x2, y2 = coordinates[(i + 1) % len(coordinates)]

        area_in += x1 * y2
        area_out += x2 * y1
    area = abs(area_in - area_out) // 2

    # https://uk.wikipedia.org/wiki/Теорема_Піка
    return area + bounds // 2 + 1


INPUT_S = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
EXPECTED = 952408144115


@pytest.mark.parametrize(
    "input_s,expected",
    [
        (INPUT_S, EXPECTED),
    ],
)
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 82712746433310


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

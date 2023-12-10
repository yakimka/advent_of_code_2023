from __future__ import annotations

import sys
import timeit
from collections import deque
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"

PIPES = {
    "|": ("down", "up"),  # north and south
    "-": ("right", "left"),  # east and west
    "L": ("right", "up"),  # north and east
    "J": ("left", "up"),  # north and west
    "7": ("left", "down"),  # south and west
    "F": ("right", "down"),  # south and east
}

OPPOSITE_DIRECTIONS = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}


def goto(start_x, start_y, d: str, field) -> tuple[tuple[int, int], str] | None:
    directions = {
        "up": (start_x - 1, start_y),
        "down": (start_x + 1, start_y),
        "left": (start_x, start_y - 1),
        "right": (start_x, start_y + 1),
    }
    x, y = directions[d]
    if x < 0 or y < 0:
        return None
    if x >= len(field) or y >= len(field[0]):
        return None
    if field[x][y] == ".":
        return None

    if field[x][y] == "S":
        return (x, y), "S"

    # remove the direction we came from
    new_directions = list(PIPES[field[x][y]])
    try:
        new_directions.remove(OPPOSITE_DIRECTIONS[d])
    except ValueError:
        # Can't go to pipe with this shape
        return None

    return (x, y), new_directions[0]


def compute(s: str) -> int:
    field = []
    start = (0, 0)
    for i, line in enumerate(s.splitlines()):
        field.append(list(line))
        if (s_index := line.find("S")) != -1:
            start = (i, s_index)

    queue = deque([
        (start, 0, "up"),
        (start, 0, "down"),
        (start, 0, "left"),
        (start, 0, "right"),
    ])
    while queue:
        (x, y), path_len, direction = queue.popleft()
        if val := goto(x, y, direction, field):
            new_coords, new_direction = val
            if new_direction == "S":
                full_path_len = path_len + 1
                return full_path_len // 2
            queue.append((new_coords, path_len + 1, new_direction))


INPUT_S1 = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""
EXPECTED1 = 4
INPUT_S2 = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""
EXPECTED2 = 4
INPUT_S3 = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
EXPECTED3 = 8


@pytest.mark.parametrize("input_s,expected", [
    (INPUT_S1, EXPECTED1),
    (INPUT_S2, EXPECTED2),
    (INPUT_S3, EXPECTED3),
])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 6725


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

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


NewCoords = tuple[int, int]
Value = str | int
NewDirection = str


def try_path(
    start_x, start_y, d: str, field
) -> tuple[NewCoords | None, NewDirection | None, Value | None]:
    directions = {
        "up": (start_x - 1, start_y),
        "down": (start_x + 1, start_y),
        "left": (start_x, start_y - 1),
        "right": (start_x, start_y + 1),
    }
    x, y = directions[d]
    new_value = get_value(x, y, field)
    if new_value is None:
        return None, None, None

    if new_value in PIPES:
        new_directions = list(PIPES[field[x][y]])
        # remove the direction we came from
        try:
            new_directions.remove(OPPOSITE_DIRECTIONS[d])
        except ValueError:
            # Can't go to pipe with this shape
            return (x, y), None, new_value
        return (x, y), new_directions[0], new_value

    return (x, y), None, new_value


def get_value(x, y, field) -> Value | None:
    if (0 > x > len(field)) or (0 > y > len(field[0])):
        return None

    return field[x][y]


def compute(s: str) -> int:
    field = []
    start = (0, 0)
    for i, line in enumerate(s.splitlines()):
        field.append(list(line))
        if (s_index := line.find("S")) != -1:
            start = (i, s_index)

    queue = deque([
        (start, "up", 1),
        (start, "down", 2),
        (start, "left", 3),
        (start, "right", 4),
    ])
    path_storage = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
    }
    id_to_last_coords = {}
    while queue:
        (x, y), direction, id = queue.popleft()

        new_coords, new_direction, _ = try_path(x, y, direction, field)
        coords_to_id = {v: id for id, st in id_to_last_coords.items() for v in st}
        if new_coords in coords_to_id:
            curr_path = path_storage[id]
            visited_path = path_storage[coords_to_id[new_coords]]

            return max(curr_path, visited_path)

        if new_coords is not None and new_direction is not None:
            queue.append((new_coords, new_direction, id))
            nx, ny = new_coords
            path_storage[id] += 1
            id_to_last_coords[id] = ((x, y), (nx, ny))


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


@pytest.mark.parametrize(
    "input_s,expected",
    [
        (INPUT_S1, EXPECTED1),
        (INPUT_S2, EXPECTED2),
        (INPUT_S3, EXPECTED3),
    ],
)
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

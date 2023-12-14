from __future__ import annotations

import sys
import timeit
from collections import deque
from itertools import cycle
from pathlib import Path
from typing import Generator

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"

Coords = tuple[int, int]


def compute(s: str) -> int:
    bridge = []
    next_stack = []
    for x, line in enumerate(s.splitlines()):
        beam = []
        for y, c in enumerate(line):
            if c == "O":
                next_stack.append((x, y))
            beam.append(c)
        bridge.append(beam)
    beams_count = len(bridge)

    results = []
    for i, direction in enumerate(cycle(["up", "left", "down", "right"])):
        state = divmod(i, 4)
        if state == (250, 0):
            return _extrapolate(results, 1_000_000_000)
        stack = deque(sorted(next_stack, key=sort_key(direction)))
        next_stack = []
        result = 0
        while stack:
            x, y = stack.popleft()
            if next_coords := get_next_coords(bridge, x, y, direction):
                new_x, new_y = next_coords
                bridge[new_x][new_y], bridge[x][y] = bridge[x][y], bridge[new_x][new_y]
                stack.appendleft(next_coords)
            else:
                result += beams_count - x
                next_stack.append((x, y))
        # save only results for end of cycle
        if state[1] == 3:
            results.append(result)

    raise RuntimeError("Should not be here")


def _extrapolate(results: list[int], cycle_num: int) -> int:
    results_len = len(results)
    if results_len >= cycle_num:
        raise ValueError("Cycle number is too small")

    window = 3
    pattern = None
    while window < results_len / 2:
        if len(set(_three_windows_from_end(results, window))) == 1:
            pattern = results[-window:]
            break
        else:
            window += 1

    if pattern is None:
        raise RuntimeError("Cannot find pattern. Try to enlarge results list")

    return pattern[(cycle_num - results_len) % window - 1]


def _three_windows_from_end(
    results: list[int], n: int
) -> Generator[tuple[int, ...], None, None]:
    end = len(results) - 1
    slices = (
        (end - n, end),
        (end - n * 2, end - n),
        (end - n * 3, end - n * 2),
    )
    for start, end in slices:
        yield tuple(results[start:end])


def get_next_coords(bridge, x: int, y: int, direction: str) -> Coords | None:
    if direction == "up":
        next_x, next_y = x - 1, y
    elif direction == "down":
        next_x, next_y = x + 1, y
    elif direction == "left":
        next_x, next_y = x, y - 1
    elif direction == "right":
        next_x, next_y = x, y + 1
    else:
        raise ValueError(f"Unknown direction {direction}")

    if 0 > next_x or 0 > next_y or next_x >= len(bridge) or next_y >= len(bridge[0]):
        return None

    if bridge[next_x][next_y] == ".":
        return next_x, next_y

    return None


def sort_key(direction: str):
    def key(coords):
        x, y = coords
        if direction == "up":
            return x, y
        elif direction == "down":
            return -x, -y
        elif direction == "left":
            return y, -x
        elif direction == "right":
            return -y, x

    return key


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
EXPECTED = 64


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 99875


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

from __future__ import annotations

import sys
import timeit
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


DIRECTION_MAP = {
    "R": "right",
    "D": "down",
    "L": "left",
    "U": "up",
}


def compute(s: str) -> int:
    matrix = [["." for _ in range(10)] for _ in range(10)]
    m = 0
    n = 0

    borders = 0
    for line in s.splitlines():
        direction, steps, *_ = line.split()
        direction = DIRECTION_MAP[direction]
        steps = int(steps)
        borders += steps
        for _ in range(steps):
            m, n = _next_coords_and_extend_if_needed(matrix, m, n, direction)
            matrix[m][n] = "#"

    start_m, start_n = _search_one_coords_inside_border(matrix)
    filled = fill_matrix(matrix, start_m, start_n)
    return borders + filled


def fill_matrix(matrix, start_m, start_n, filler="#") -> int:
    neighbors_cross_diag = sup.max_bounds_closure(sup.neighbors_cross_diag, matrix)
    stack = [(start_m, start_n)]
    count = 0
    while stack:
        m, n = stack.pop()
        if matrix[m][n] == filler:
            continue
        matrix[m][n] = filler
        count += 1
        for neighbor in neighbors_cross_diag(m, n):
            stack.append(neighbor)
    return count


def _search_one_coords_inside_border(matrix):
    m_len = len(matrix)
    n_len = len(matrix[0])
    for m in range(m_len - 1):
        for n in range(n_len - 1):
            if matrix[m][n] == "#":
                # Dont want to write complex logic for this case
                #   if we have multiple # in one row - just skip it
                #   (cause it can be a solid border: #########
                #                                    #       #)
                #   and go to the next row in hope to find single #
                if matrix[m][n + 1] == "#":
                    break
                return m, n + 1
    raise RuntimeError("No one coords inside border")


def _next_coords_and_extend_if_needed(
    matrix, start_m, start_n, direction, extend_size=10
):
    m_len = len(matrix)
    n_len = len(matrix[0])
    res = sup.next_coords(start_m, start_n, direction, (m_len - 1, n_len - 1))
    if res is None:
        _extend_matrix(matrix, direction, extend_size)
        if direction == "right":
            n_len += extend_size
        elif direction == "left":
            start_n += extend_size
            n_len += extend_size
        elif direction == "up":
            start_m += extend_size
            m_len += extend_size
        elif direction == "down":
            m_len += extend_size
        start_m, start_n = sup.next_coords(
            start_m, start_n, direction, (m_len - 1, n_len - 1)
        )
    else:
        start_m, start_n = res

    return start_m, start_n


def _extend_matrix(matrix, direction, size):
    if direction == "right":
        for row in matrix:
            row.extend(["." for _ in range(size)])
    elif direction == "left":
        for row in matrix:
            row[:0] = ["." for _ in range(size)]
    elif direction == "up":
        matrix[:0] = [["." for _ in range(len(matrix[0]))] for _ in range(size)]
    elif direction == "down":
        matrix.extend([["." for _ in range(len(matrix[0]))] for _ in range(size)])


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
EXPECTED = 62


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

    assert result == 50465


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

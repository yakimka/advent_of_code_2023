from __future__ import annotations

import sys
import timeit
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"

Coords = tuple[int, int]
Move = tuple[int, int, str]


def compute(s: str) -> int:
    matrix, _, _ = sup.make_matrix_from_input(s)
    next_coords = sup.max_bounds_closure(sup.next_coords, matrix)
    seen_mirrors = set()

    max_seen = 0
    for move in get_first_moves(matrix):
        stack = [move]
        seen_cells = set()
        seen_mirrors = set()

        while stack:
            m, n, direction = stack.pop()
            if matrix[m][n] != ".":
                mirror = (m, n, direction)
                if mirror in seen_mirrors:
                    continue
                seen_mirrors.add(mirror)
            seen_cells.add((m, n))
            next_moves = get_next_moves(matrix, next_coords, m, n, direction)
            stack.extend(next_moves)

        if (len_cells := len(seen_cells)) > max_seen:
            max_seen = len_cells

    return max_seen


def get_first_moves(matrix) -> list[Move]:
    moves = []
    m_len = len(matrix)
    n_len = len(matrix[0])
    for n in range(n_len):
        moves.append((0, n, "down"))
        moves.append((m_len - 1, n, "up"))
        if n > 0:
            moves.append((0, n, "left"))
            moves.append((m_len - 1, n, "left"))
        if n < n_len - 1:
            moves.append((0, n, "right"))
            moves.append((m_len - 1, n, "right"))
    for m in range(m_len):
        moves.append((m, 0, "right"))
        moves.append((m, n_len - 1, "left"))
        if m > 0:
            moves.append((m, 0, "up"))
            moves.append((m, n_len - 1, "up"))
        if m < m_len - 1:
            moves.append((m, 0, "down"))
            moves.append((m, n_len - 1, "down"))
    return moves


def get_next_moves(matrix, next_coords, m: int, n: int, direction: str) -> list[Move]:
    new_directions = []
    current_value = matrix[m][n]
    if (direction, current_value) in [("up", "\\"), ("down", "/")]:
        new_directions.append("left")
    elif (direction, current_value) in [("up", "/"), ("down", "\\")]:
        new_directions.append("right")
    elif (direction, current_value) in [("left", "\\"), ("right", "/")]:
        new_directions.append("up")
    elif (direction, current_value) in [("left", "/"), ("right", "\\")]:
        new_directions.append("down")
    elif direction in ["left", "right"] and current_value == "|":
        new_directions.extend(["up", "down"])
    elif direction in ["up", "down"] and current_value == "-":
        new_directions.extend(["left", "right"])
    else:
        new_directions.append(direction)

    result = []
    for direction in new_directions:
        if coords := next_coords(m, n, direction):
            result.append((*coords, direction))

    return result


INPUT_S = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
EXPECTED = 51


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 7853


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

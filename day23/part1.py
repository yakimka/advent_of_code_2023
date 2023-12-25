from __future__ import annotations

import heapq
import sys
import timeit
from pathlib import Path
from typing import Callable, Generator

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(s: str) -> int:
    matrix, m_len, n_len = sup.make_matrix_from_input(s)
    neighbors_cross = sup.max_bounds_closure(sup.neighbors_cross, matrix)
    graph = make_graph_for_matrix(matrix, ["#"], neighbors_cross)
    end = (m_len - 1, n_len - 2)
    _, prev = sup.a_star(graph, (0, 1), end, heuristic_longest)
    path = _get_path(prev, end)
    for m, n in path:
        matrix[m][n] = "O"

    sup.print_matrix(matrix)

    return len(path)


def _get_path(prev: dict[tuple[int, int], tuple[int, int]], end: tuple[int, int]) -> list[tuple[int, int]]:
    path = []
    node = end
    while node:
        path.append(node)
        node = prev[node]
    return path[::-1]


def heuristic_longest(coords1, coords2) -> int:
    return -sup.cartesian_shortest_path(coords1, coords2)


def make_graph_for_matrix(
    matrix,
    obstacles: list[str],
    neighbors: Callable[[int, int], Generator[tuple[int, int]]],
) -> dict:
    graph = {}
    for m, row in enumerate(matrix):
        for n, cell in enumerate(row):
            graph[(m, n)] = {}
            if cell in obstacles:
                continue
            neighbors_iter = neighbors(m, n)
            if cell in "^>v<":
                neighbors_iter = [_get_slide_end_cell(matrix, (m, n))]

            for neighbor in neighbors_iter:
                n_m, n_n = neighbor
                if matrix[n_m][n_n] in obstacles:
                    continue
                graph[(m, n)][neighbor] = 0
    return graph


SLIDES_MAP = {
    "^": "up",
    ">": "right",
    "v": "down",
    "<": "left",
}


def _get_slide_end_cell(
    matrix: list[list[str]], start: tuple[int, int]
) -> tuple[int, int]:
    m, n = start
    slides = "^>v<"
    if matrix[m][n] not in slides:
        raise ValueError(f"Invalid start cell value: {matrix[m][n]}")

    next_coords = sup.max_bounds_closure(sup.next_coords, matrix)
    while matrix[m][n] in slides:
        m, n = next_coords(m, n, SLIDES_MAP[matrix[m][n]])
    return m, n


INPUT_S = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""
EXPECTED = 94


@pytest.mark.parametrize(
    "input_s,expected",
    [
        (INPUT_S, EXPECTED),
    ],
)
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


@pytest.mark.skip("Set answer for refactoring")
def test_input() -> None:
    result = compute(read_input())

    assert result == 0


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

from __future__ import annotations

import sys
import timeit
from pathlib import Path
from typing import Callable, Generator

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(s: str, steps_num: int = 64) -> int:
    matrix, *_ = sup.make_matrix_from_input(s)
    start = None
    for m, row in enumerate(matrix):
        for n, cell in enumerate(row):
            if cell == "S":
                start = (m, n)
                break
        if start:
            break

    neighbors_cross = sup.max_bounds_closure(sup.neighbors_cross, matrix)
    graph = make_graph_for_matrix(matrix, ["#"], neighbors_cross)

    nodes = {start}
    for _ in range(steps_num):
        new_nodes = set()
        for node in nodes:
            for neighbor in graph[node]:
                new_nodes.add(neighbor)
        nodes = new_nodes

    return len(nodes)


def make_graph_for_matrix(
    matrix,
    obstacles: list[str],
    neighbors: Callable[[int, int], Generator[tuple[int, int]]],
    weight_calculator: Callable[[tuple[int, int]], int] | None = None,
) -> dict:
    graph = {}
    for m, row in enumerate(matrix):
        for n, cell in enumerate(row):
            graph[(m, n)] = {}
            if cell in obstacles:
                continue
            for neighbor in neighbors(m, n):
                n_m, n_n = neighbor
                if matrix[n_m][n_n] in obstacles:
                    continue
                graph[(m, n)][neighbor] = (
                    weight_calculator((n_m, n_n)) if weight_calculator else 0
                )
    return graph


INPUT_S = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""
EXPECTED = 16


@pytest.mark.parametrize(
    "input_s,expected",
    [
        (INPUT_S, EXPECTED),
    ],
)
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s, steps_num=6) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 3733


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


if __name__ == "__main__":
    input_data = read_input()
    print("Answer is:     ", compute(input_data))

    if "-b" in sys.argv:
        number_of_runs = 100
        bench_time = timeit.timeit(
            "compute(data)",
            setup="from __main__ import compute",
            globals={"data": input_data},
            number=number_of_runs,
        )
        print(f"{number_of_runs} runs took: {bench_time}s")
        one_run = sup.humanized_seconds(bench_time / number_of_runs)
        print(f"Average time:   {one_run}")

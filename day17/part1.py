from __future__ import annotations

import sys
import timeit
from itertools import product
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


DIRECTIONS = ("right", "down", "left", "up")
OPPOSITE_DIRECTIONS_MAP = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}


def compute(s: str) -> int:
    matrix, len_m, len_n = sup.make_matrix_from_input(s, cast_func=int)
    graph = create_graph(matrix)
    dist, _ = sup.dijkstra(graph, ((0, 0), "right", 1))
    return min(v for k, v in dist.items() if k[0] == (len_m - 1, len_n - 1))


def create_graph(matrix):
    graph = {}
    next_coords = sup.max_bounds_closure(sup.next_coords, matrix)

    for start_m, start_n, start_steps_num, start_direction in product(
        range(len(matrix)), range(len(matrix[0])), range(1, 4), DIRECTIONS
    ):
        start_coords = (start_m, start_n)
        if start_steps_num > 1:
            opposite_direction = OPPOSITE_DIRECTIONS_MAP[start_direction]
            prev_coords = next_coords(*start_coords, opposite_direction)
            if (
                not prev_coords
                or start_steps_num == 3
                and not next_coords(*prev_coords, opposite_direction)
            ):
                continue

        start_key = (start_coords, start_direction, start_steps_num)
        for dest_direction in DIRECTIONS:
            if dest_coords := next_coords(start_m, start_n, dest_direction):
                if dest_direction == OPPOSITE_DIRECTIONS_MAP[start_direction]:
                    continue
                dest_m, dest_n = dest_coords
                dest_steps_num = start_steps_num
                if start_direction == dest_direction:
                    dest_steps_num += 1
                else:
                    dest_steps_num = 1
                if dest_steps_num > 3:
                    continue
                dest_key = (dest_coords, dest_direction, dest_steps_num)
                value = matrix[dest_m][dest_n]
                graph.setdefault(start_key, {})[dest_key] = value
    return graph


INPUT_S = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""
EXPECTED = 102


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


@pytest.mark.skip("qwe")
def test_input() -> None:
    result = compute(read_input())

    assert result == 1065


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

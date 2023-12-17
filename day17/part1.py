from __future__ import annotations

import sys
import timeit
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


# 1  function Dijkstra(Graph, source):
#  2
#  3      for each vertex v in Graph.Vertices:
#  4          dist[v] ← INFINITY
#  5          prev[v] ← UNDEFINED
#  6          add v to Q
#  7      dist[source] ← 0
#  8
#  9      while Q is not empty:
# 10          u ← vertex in Q with min dist[u]
# 11          remove u from Q
# 12
# 13          for each neighbor v of u still in Q:
# 14              alt ← dist[u] + Graph.Edges(u, v)
# 15              if alt < dist[v]:
# 16                  dist[v] ← alt
# 17                  prev[v] ← u
# 18
# 19      return dist[], prev[]


def dijkstra(graph: dict[str, dict[str, int]], source: str) -> tuple[dict[str, int], dict[str, str]]:
    # """
    # Find shortest paths from source to all vertices in graph.
    # Example:
    # >>> graph = {
    # ...     "a": {"b": 7, "c": 9, "f": 14},
    # ...     "b": {"a": 7, "c": 10, "d": 15},
    # ...     "c": {"a": 9, "b": 10, "d": 11, "f": 2},
    # ...     "d": {"b": 15, "c": 11, "e": 6},
    # ...     "e": {"d": 6, "f": 9},
    # ...     "f": {"a": 14, "c": 2, "e": 9},
    # ... }
    # >>> dist, prev = dijkstra(graph, "a")
    # >>> dist["e"]
    # 20
    # >>> prev["e"]
    # 'f'
    # """
    dist: dict[str, int] = {}
    prev: dict[str, str] = {}
    q = set(graph.keys())

    for vertex in graph.keys():
        dist[vertex] = float("inf")
        prev[vertex] = None
    dist[source] = 0

    while q:
        u = min(q, key=lambda v: dist[v])
        q.remove(u)

        for v in q.intersection(graph[u].keys()):
            alt = dist[u] + graph[u][v]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev


DIRECTIONS = ("right", "down", "left", "up")
OPPOSITE_DIRECTIONS_MAP = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}

def compute(s: str) -> int:
    matrix, *_ = sup.make_matrix_from_input(s, cast_func=int)
    graph = {}
    next_coords = sup.max_bounds_closure(sup.next_coords, matrix)
    for start_m, row in enumerate(matrix):
        for start_n, _ in enumerate(row):
            start_coords = (start_m, start_n)
            start_steps_num = 1
            for start_direction in DIRECTIONS:
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


    # bigger_steps = {}
    # for start_key, dest in graph.items():
    #     start_coords, direction, steps = start_key
    #     opposite_direction = OPPOSITE_DIRECTIONS_MAP[direction]
    #     if coords := next_coords(*start_coords, opposite_direction):
    #         new_steps = steps + 1
    #         new_key = (start_coords, direction, new_steps)
    #         bigger_steps[new_key] = {(d_coords, d_direct, d_steps + 1): v for (d_coords, d_direct, d_steps), v in dest.items()}
    #         if new_coords := next_coords(*coords, opposite_direction):
    #             new_steps = steps + 2
    #             new_key = (start_coords, direction, new_steps)
    #             bigger_steps[new_key] = {(d_coords, d_direct, d_steps + 2): v for (d_coords, d_direct, d_steps), v in dest.items()}
    # graph.update(bigger_steps)

    res = dijkstra(graph, ((0, 0), "right", 1))
    return 0


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

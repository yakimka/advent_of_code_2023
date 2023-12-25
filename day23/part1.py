from __future__ import annotations

import sys
import timeit
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


SLIDES_MAP = {
    "up": "^",
    "right": ">",
    "down": "v",
    "left": "<",
}


def compute(s: str) -> int:
    matrix, m_len, n_len = sup.make_matrix_from_input(s)
    next_coords = sup.max_bounds_closure(sup.next_coords, matrix)
    start = (0, 1)
    end = (m_len - 1, n_len - 2)

    maximum = 0
    stack = [(start, {start})]
    while stack:
        node, seen = stack.pop()
        for direction in SLIDES_MAP:
            candidate = next_coords(*node, direction)
            if not candidate:
                continue
            value = matrix[candidate[0]][candidate[1]]
            if candidate == end:
                maximum = max(maximum, len(seen))
            elif candidate not in seen and value in [".", SLIDES_MAP[direction]]:
                stack.append((candidate, seen | {candidate}))
    return maximum


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


def test_input() -> None:
    result = compute(read_input())

    assert result == 2182


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


if __name__ == "__main__":
    input_data = read_input()
    print("Answer is:     ", compute(input_data))

    if "-b" in sys.argv:
        number_of_runs = 10
        bench_time = timeit.timeit(
            "compute(data)",
            setup="from __main__ import compute",
            globals={"data": input_data},
            number=number_of_runs,
        )
        print(f"{number_of_runs} runs took: {bench_time}s")
        one_run = sup.humanized_seconds(bench_time / number_of_runs)
        print(f"Average time:   {one_run}")

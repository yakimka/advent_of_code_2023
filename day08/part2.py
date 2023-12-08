from __future__ import annotations

import math
import sys
import timeit
from functools import reduce
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(s: str) -> int:
    lines = s.splitlines()
    mapping = {}
    starting_nodes = []
    for line in lines[2:]:
        line = (
            line.replace(" = ", " ").replace("(", "").replace(")", "").replace(",", " ")
        )
        node_name, *values = line.split()
        mapping[node_name] = values
        if node_name.endswith("A"):
            starting_nodes.append(node_name)

    counts = []
    steps_index = ["L", "R"]
    for node in starting_nodes:
        count = 0
        while not node.endswith("Z"):
            map_i = count % len(lines[0])
            node = mapping[node][steps_index.index(lines[0][map_i])]
            count += 1
        counts.append(count)

    return reduce(math.lcm, counts)


INPUT_S1 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
EXPECTED1 = 6


@pytest.mark.parametrize(
    "input_s,expected",
    [
        (INPUT_S1, EXPECTED1),
    ],
)
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 12324145107121


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

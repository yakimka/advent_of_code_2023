from __future__ import annotations

import sys
import timeit
from functools import reduce
from itertools import count
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def steps_generator(steps: str) -> str:
    for i in count():
        for step in steps:
            yield i, step


def compute(s: str) -> int:
    lines = s.splitlines()
    mapping = {}
    starting_nodes = []
    for line in lines[2:]:
        line = line.replace(" = ", " ").replace("(", "").replace(")", "").replace(",", " ")
        node_name, *values = line.split()
        mapping[node_name] = values
        if node_name.endswith("A"):
            starting_nodes.append(node_name)

    current_list = list(starting_nodes)
    steps_count = 0
    steps_index = ["L", "R"]
    starting_paths_count = len(starting_nodes)
    steps_len = len(lines[0])
    found_z = []
    for i, (loop_num, step) in enumerate(steps_generator(lines[0])):
        step_i = i % steps_len
        steps_count += 1
        for i, current in enumerate(current_list):
            if current in mapping:
                current_list[i] = mapping[current][steps_index.index(step)]

            if current_list[i].endswith("Z"):
                found_z.append((loop_num + 1, step_i + 1, i))

        if len(found_z) > starting_paths_count and found_z[-1][2] == len(current_list) - 1:
            break

    data = {}
    for item in found_z:
        data.setdefault(item[2], []).append(item[0])
    data = sorted([v[-1] - v[-2] for k, v in data.items()])
    number = reduce(lowest_common_multiple, data)
    return number * found_z[0][1]


def greatest_common_divisor(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def lowest_common_multiple(a: int, b: int) -> int:
    return a * b // greatest_common_divisor(a, b)


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


# @pytest.mark.parametrize("input_s,expected", [
#     (INPUT_S1, EXPECTED1),
# ])
# def test_debug(input_s: str, expected: int) -> None:
#     assert compute(input_s) == expected


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

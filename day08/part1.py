from __future__ import annotations

import sys
import timeit
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def steps_generator(steps: str) -> str:
    while True:
        yield from steps


def compute(s: str) -> int:
    lines = s.splitlines()
    mapping = {}
    for line in lines[2:]:
        line = line.replace(" = ", " ").replace("(", "").replace(")", "").replace(",", " ")
        node_name, *values = line.split()
        mapping[node_name] = values

    current = "AAA"
    steps_count = 0
    steps_index = ["L", "R"]
    for step in steps_generator(lines[0]):
        steps_count += 1
        if current in mapping:
            current = mapping[current][steps_index.index(step)]

        if current == "ZZZ":
            return steps_count

    raise RuntimeError("No ZZZ found")


INPUT_S1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
EXPECTED1 = 2

INPUT_S2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
EXPECTED2 = 6


@pytest.mark.parametrize("input_s,expected", [
    (INPUT_S1, EXPECTED1),
    (INPUT_S2, EXPECTED2),
])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 13207


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

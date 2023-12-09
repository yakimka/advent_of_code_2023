from __future__ import annotations

import sys
import timeit
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(s: str) -> int:
    return sum(predict([int(x) for x in line.split()]) for line in s.splitlines())


def predict(data: list[int]) -> int:
    predict_layers = [data]
    for layer in predict_layers:
        if all(v == 0 for v in layer):
            break
        new_layer = [layer[i] - layer[i - 1] for i in range(1, len(layer))]
        predict_layers.append(new_layer)

    new_value = 0
    for layer in reversed(predict_layers):
        new_value += layer[-1]

    return new_value


INPUT_S = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
EXPECTED = 114


@pytest.mark.parametrize("input_s,expected", [
    (INPUT_S, EXPECTED),
])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


# @pytest.mark.skip("Set answer for refactoring")
def test_input() -> None:
    result = compute(read_input())

    assert result == 1584748274


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

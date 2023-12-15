from __future__ import annotations

import sys
import timeit
from collections import OrderedDict
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(s: str) -> int:
    boxes = [OrderedDict() for _ in range(256)]
    for step in s.splitlines()[0].strip().split(","):
        label, value = parse_step(step)

        key = hash_func(label)
        box = boxes[key]
        if not value:
            box.pop(label, None)
        else:
            box[label] = value

    return sum(
        box_id * slot * value
        for box_id, box in enumerate(boxes, start=1)
        if box
        for slot, (label, value) in enumerate(box.items(), start=1)
    )


def parse_step(step: str) -> tuple[str, int]:
    step = step.replace("-", "=")
    label, value = step.split("=")
    return label, int(value or "0")


def hash_func(value: str) -> int:
    current_value = 0
    for c in value:
        code_value = ord(c)
        current_value += code_value
        current_value *= 17
        current_value %= 256
    return current_value


INPUT_S = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
EXPECTED = 145


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

    assert result == 248279


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

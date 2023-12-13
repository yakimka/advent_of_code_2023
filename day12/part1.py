from __future__ import annotations

import sys
import timeit
from itertools import product
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def validate_combination(combination: str, group_sizes: list[int]) -> bool:
    groups = [len(group) for group in combination.split(".") if group]

    return groups == group_sizes


def compute(s: str) -> int:
    total_count = 0
    for line in s.splitlines():
        spring_states, group_sizes = line.split(" ")
        group_sizes = list(map(int, group_sizes.split(",")))

        unknown_count = spring_states.count("?")
        possible_combinations = product(".#", repeat=unknown_count)

        valid_combinations = 0
        for combination in possible_combinations:
            combination_index = 0
            temp_spring_states = list(spring_states)

            for i, state in enumerate(temp_spring_states):
                if state == "?":
                    temp_spring_states[i] = combination[combination_index]
                    combination_index += 1

            if validate_combination("".join(temp_spring_states), group_sizes):
                valid_combinations += 1

        total_count += valid_combinations

    return total_count


INPUT_S = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
EXPECTED = sum([
    1,
    4,
    1,
    1,
    4,
    10,
])  # 21


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 8075


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


if __name__ == "__main__":
    input_data = read_input()
    print("Answer is:     ", compute(input_data))

    if "-b" in sys.argv:
        number_of_runs = 3
        bench_time = timeit.timeit(
            "compute(data)",
            setup="from __main__ import compute",
            globals={"data": input_data},
            number=number_of_runs,
        )
        print(f"{number_of_runs} runs took: {bench_time}s")
        one_run = sup.humanized_seconds(bench_time / number_of_runs)
        print(f"Average time:   {one_run}")

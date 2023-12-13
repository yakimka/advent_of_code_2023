from __future__ import annotations

import re
import sys
import timeit
from functools import cache
from itertools import chain, repeat
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"

CLEAN_RE = re.compile(r"\.+")


# I had to look up the solution to this problem 🫣
def compute(s: str) -> int:
    result = 0
    for line in s.splitlines():
        spring_states, group_sizes = line.split(" ")
        spring_states = "?".join(spring_states for _ in range(5))
        spring_states = clean_pattern(spring_states)
        group_sizes = ",".join(group_sizes for _ in range(5))
        group_sizes = tuple(map(int, group_sizes.split(",")))
        temp_res = calc_combinations(spring_states, group_sizes)
        result += temp_res

    return result


def clean_pattern(pattern: str) -> str:
    one_dot = CLEAN_RE.sub(".", pattern)
    return f"{one_dot.strip('.')}."


@cache
def calc_combinations(pattern: str, pieces: tuple[int, ...]) -> int:
    if not pieces:
        return 0 if "#" in pattern else 1

    first = pieces[0]
    rest = tuple(pieces[1:])
    total = 0
    min_pattern_size = sum(pieces) + len(pieces)
    for i in range(len(pattern) - min_pattern_size + 1):
        if valid_piece(pattern, i, first):
            next_pattern_start = i + first + 1
            total += calc_combinations(pattern[next_pattern_start:], rest)
        if pattern[i] == "#":
            break
    return total


def valid_piece(pattern: str, i: int, size: int) -> bool:
    for pat_c, size_c in zip(pattern[i:], chain(repeat("#", size), ".")):
        if pat_c == "?":
            continue
        if pat_c != size_c:
            return False
    return True


INPUT_S = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
EXPECTED = 525152


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 4232520187524


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

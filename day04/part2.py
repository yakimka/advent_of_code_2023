from __future__ import annotations

import sys
import timeit
from functools import lru_cache
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(s: str) -> int:
    games_map = {}
    max_game_id = 0
    for game_id, line in enumerate(s.splitlines(), start=1):
        _, numbers = line.split(": ")
        winning, i_have = numbers.split(" | ")
        winning_count = len(set(winning.split()) & set(i_have.split()))
        if winning_count:
            games_map[game_id] = winning_count
        max_game_id = game_id

    @lru_cache(maxsize=None)
    def calc_points(game_id: int) -> int:
        count = games_map.get(game_id, 0)
        return 1 + sum(calc_points(game_id + i) for i in range(1, count + 1))

    return sum(calc_points(game_id) for game_id in range(1, max_game_id + 1))


INPUT_S = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
EXPECTED = 30


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 6857330


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

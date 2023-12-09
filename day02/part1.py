from __future__ import annotations

import sys
import timeit
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"

TOTAL_RED, TOTAL_GREEN, TOTAL_BLUE = 12, 13, 14


def compute(s: str) -> int:
    possible_games_sum = 0
    for game_id, line in enumerate(s.splitlines(), start=1):
        _, game_data = line.split(": ")
        turns = game_data.split("; ")
        is_possible = True
        for turn in turns:
            for turn_data in turn.split(", "):
                count, color = turn_data.split(" ")
                count = int(count)
                if color == "red":
                    total_color = TOTAL_RED
                elif color == "green":
                    total_color = TOTAL_GREEN
                elif color == "blue":
                    total_color = TOTAL_BLUE
                else:
                    raise ValueError(f"Unknown color {color}")

                if count > total_color:
                    is_possible = False
        if is_possible:
            possible_games_sum += game_id
    return possible_games_sum


INPUT_S = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
EXPECTED = 8


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    with open(INPUT_TXT) as f:
        result = compute(f.read())

    assert result == 2720


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

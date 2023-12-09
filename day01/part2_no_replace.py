from __future__ import annotations

import sys
import timeit
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"

SPELLED_NUMBERS = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def _make_path_graph_from_words(words: list[str]):
    graph = {}
    for word in words:
        word_len = len(word)
        current = graph
        for i, char in enumerate(word):
            default = {} if i < word_len - 1 else True
            current = current.setdefault(char, default)
    return graph


SPELLED_GRAPH = _make_path_graph_from_words(SPELLED_NUMBERS)
SPELLED_NUMBERS_REVERSED = [word[::-1] for word in SPELLED_NUMBERS]
SPELLED_GRAPH_REVERSED = _make_path_graph_from_words(SPELLED_NUMBERS_REVERSED)


def resolve_path(graph: dict, path: Iterable[str]) -> int:
    """
    Return -1 if path is not found
        1 if path is resolved completely
        0 if path is resolved partially
    """
    current = graph
    for char in path:
        if current is True:
            return -1
        if char not in current:
            return -1
        current = current[char]

    return 1 if current is True else 0


@lru_cache(maxsize=None)
def resolve_left_path(path: Iterable[str]) -> int:
    return resolve_path(SPELLED_GRAPH, path)


@lru_cache(maxsize=None)
def resolve_right_path(path: Iterable[str]) -> int:
    return resolve_path(SPELLED_GRAPH_REVERSED, path)


def compute(s: str) -> int:
    result = 0
    for line in s.splitlines():
        left = 0
        right = len(line) - 1
        left_number = -1
        right_number = -1
        left_graph_path = []
        right_graph_path = []
        while left <= right:
            if left_number >= 0 and right_number >= 0:
                break

            # Part that checking left and right numbers
            #   can be extracted to separate function
            #   but i don't want to do it
            if left_number < 0:
                left_char = line[left]
                if left_char.isdigit():
                    left_number = int(left_char)
                    continue

                new_left_graph_path = (*left_graph_path, left_char)
                left_resolved = resolve_left_path(new_left_graph_path)
                if left_resolved != -1:
                    left_graph_path = new_left_graph_path
                else:
                    for i in range(1, len(left_graph_path) + 1):
                        left_resolved = resolve_left_path(new_left_graph_path[i:])
                        if left_resolved != -1:
                            left_graph_path = new_left_graph_path[i:]
                            break
                    else:
                        left_graph_path = []
                if left_resolved == 1:
                    left_number = SPELLED_NUMBERS.index("".join(left_graph_path)) + 1
                    continue

                left += 1

            if right_number < 0:
                right_char = line[right]
                if right_char.isdigit():
                    right_number = int(right_char)
                    continue

                new_right_graph_path = (*right_graph_path, right_char)
                right_resolved = resolve_right_path(new_right_graph_path)
                if right_resolved != -1:
                    right_graph_path = new_right_graph_path
                else:
                    for i in range(1, len(right_graph_path) + 1):
                        right_resolved = resolve_right_path(new_right_graph_path[i:])
                        if right_resolved != -1:
                            right_graph_path = new_right_graph_path[i:]
                            break
                    else:
                        right_graph_path = []
                if right_resolved == 1:
                    right_number = (
                        SPELLED_NUMBERS_REVERSED.index("".join(right_graph_path)) + 1
                    )
                    continue

                right -= 1
        result += left_number * 10 + right_number
    return result


INPUT_S = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
EXPECTED = 281


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (INPUT_S, EXPECTED),
        ("sdonefour77one", 11),
        ("ktnxrj2sixsevenrcnqbksgbgdfxrdqgz", 27),
        ("ktnxrj2sixsevenrcn", 27),
        ("1drjnqoneninennhqt", 19),
        ("twofiveoneseven1rqjvrrxtwonen", 21),
        ("two7fivenrgdqshs", 25),
        ("7ninetphdpcx", 79),
    ),
)
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 53868


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

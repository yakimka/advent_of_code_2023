from __future__ import annotations

import sys
import timeit
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import pytest

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


def _make_spelled_graph_from_words(words: list[str]):
    graph = {}
    for word in words:
        word_len = len(word)
        current = graph
        for i, char in enumerate(word):
            default = {} if i < word_len - 1 else words.index(word) + 1
            current = current.setdefault(char, default)
    return graph


SPELLED_GRAPH = _make_spelled_graph_from_words(SPELLED_NUMBERS)
SPELLED_NUMBERS_REVERSED = [word[::-1] for word in SPELLED_NUMBERS]
SPELLED_GRAPH_REVERSED = _make_spelled_graph_from_words(SPELLED_NUMBERS_REVERSED)


def resolve_path(graph: dict, path: Iterable[str]) -> int | None:
    current = graph
    for char in path:
        if isinstance(current, int):
            return None
        if char not in current:
            return None
        current = current[char]

    return current


@lru_cache(maxsize=None)
def resolve_left_path(path: Iterable[str]) -> int | None:
    return resolve_path(SPELLED_GRAPH, path)


@lru_cache(maxsize=None)
def resolve_right_path(path: Iterable[str]) -> int | None:
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

            if left_number < 0:
                left_char = line[left]
                if left_char.isdigit():
                    left_number = int(left_char)
                    continue

                new_left_graph_path = (*left_graph_path, left_char)
                left_resolved = resolve_left_path(new_left_graph_path)
                if left_resolved is not None:
                    left_graph_path = new_left_graph_path
                else:
                    for i in range(1, len(left_graph_path) + 1):
                        left_resolved = resolve_left_path(new_left_graph_path[i:])
                        if left_resolved is not None:
                            left_graph_path = new_left_graph_path[i:]
                            break
                    else:
                        left_graph_path = []
                if isinstance(left_resolved, int):
                    left_number = left_resolved
                    continue

                left += 1

            if right_number < 0:
                right_char = line[right]
                if right_char.isdigit():
                    right_number = int(right_char)
                    continue

                new_right_graph_path = (*right_graph_path, right_char)
                right_resolved = resolve_right_path(new_right_graph_path)
                if right_resolved is not None:
                    right_graph_path = new_right_graph_path
                else:
                    for i in range(1, len(right_graph_path) + 1):
                        right_resolved = resolve_right_path(new_right_graph_path[i:])
                        if right_resolved is not None:
                            right_graph_path = new_right_graph_path[i:]
                            break
                    else:
                        right_graph_path = []
                if isinstance(right_resolved, int):
                    right_number = right_resolved
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


@pytest.mark.skip()
@pytest.mark.parametrize("line", INPUT_TXT.read_text().splitlines())
def test_find_problem(line) -> None:
    from .part2 import compute as compute_valid

    assert compute_valid(line) == compute(line)


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


if __name__ == "__main__":
    input_data = read_input()
    print("Answer is:", compute(input_data))

    if "-b" in sys.argv:
        bench_time = timeit.timeit(
            "compute(data)",
            setup="from __main__ import compute",
            globals={"data": input_data},
            number=1000,
        )
        print("1000 runs took", bench_time, "seconds")

from __future__ import annotations

import sys
import timeit
import bisect
from collections import Counter
from functools import partial
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def hand_calculator(hand: str, cards_order: str) -> tuple[int, tuple[int, ...]]:
    hand_counts = Counter(hand).most_common(len(hand))

    def five_of_a_kind(base_points: int) -> int:
        for card, count in hand_counts:
            if count == 5:
                return base_points

        return 0

    def four_of_a_kind(base_points) -> int:
        for card, count in hand_counts:
            if count == 4:
                return base_points

        return 0

    def full_house(base_points) -> int:
        counts = hand_counts
        for i, (card, count) in enumerate(counts[:-1]):
            if count == 3 and counts[i + 1][1] == 2:
                return base_points

        return 0

    def three_of_kind(base_points) -> int:
        for card, count in hand_counts:
            if count == 3:
                return base_points

        return 0

    def two_pairs(base_points) -> int:
        counts = hand_counts
        for i, (card, count) in enumerate(counts[:-1]):
            if count == 2 and counts[i + 1][1] == 2:
                return base_points

        return 0

    def pair(base_points) -> int:
        for card, count in hand_counts:
            if count == 2:
                return base_points

        return 0

    def high_card(base_points) -> int:
        return base_points

    for func in [
        partial(five_of_a_kind, 1000),
        partial(four_of_a_kind, 900),
        partial(full_house, 800),
        partial(three_of_kind, 700),
        partial(two_pairs, 600),
        partial(pair, 500),
        partial(high_card, 400),
    ]:
        if points := func():
            return points, tuple(cards_order.index(card) for card in hand)
    raise RuntimeError("Can't calculate points")


def compute(s: str) -> int:
    ordered_hands = []
    for line in s.splitlines():
        hand, bid = line.split()
        points = hand_calculator(hand, cards_order="23456789TJQKA")
        bisect.insort(ordered_hands, (points, int(bid)))

    result = 0
    for i, (_, bid) in enumerate(ordered_hands, start=1):
        result += i * bid

    return result


INPUT_S = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
EXPECTED = 6440


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


@pytest.mark.skip("Set answer for refactoring")
def test_input() -> None:
    result = compute(read_input())

    assert result == 0


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

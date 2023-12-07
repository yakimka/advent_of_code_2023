from __future__ import annotations

import sys
import timeit
from collections import Counter
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def hand_calculator(hand: str, cards_order: str) -> tuple[int, tuple[int, ...]]:
    hand_counts = Counter(hand).most_common(len(hand))
    second_order_argument = tuple(cards_order.index(card) for card in hand)

    # five_of_a_kind
    for card, count in hand_counts:
        if count == 5:
            return 1000, second_order_argument

    # four_of_a_kind
    for card, count in hand_counts:
        if count == 4:
            return 900, second_order_argument

    # full_house
    for i, (card, count) in enumerate(hand_counts[:-1]):
        if count == 3 and hand_counts[i + 1][1] == 2:
            return 800, second_order_argument

    # three_of_kind
    for card, count in hand_counts:
        if count == 3:
            return 700, second_order_argument

    # two_pairs
    for i, (card, count) in enumerate(hand_counts[:-1]):
        if count == 2 and hand_counts[i + 1][1] == 2:
            return 600, second_order_argument

    # pair
    for card, count in hand_counts:
        if count == 2:
            return 500, second_order_argument

    return 400, second_order_argument


def compute(s: str) -> int:
    ordered_hands = []
    for line in s.splitlines():
        hand, bid = line.split()
        points = hand_calculator(hand, cards_order="23456789TJQKA")
        ordered_hands.append((points, int(bid)))

    ordered_hands.sort()
    return sum(i * bid for i, (_, bid) in enumerate(ordered_hands, start=1))


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


# @pytest.mark.skip("Set answer for refactoring")
def test_input() -> None:
    result = compute(read_input())

    assert result == 251287184


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

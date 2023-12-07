from __future__ import annotations

import sys
import timeit
from collections import Counter
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def hand_calculator(hand: str, cards_order: str) -> tuple[int, tuple[int, ...]]:
    hand_counter = Counter(hand)
    joker_count = hand_counter.pop("J", 0)
    first_count, second_count, *_ = (
        count for _, count in [*hand_counter.most_common(2), (None, 0), (None, 0)]
    )
    count_to_points = {
        5: 1000,
        4: 900,
        3: 700,
        2: 500,
        1: 400,
    }
    first_total = first_count + joker_count
    points = count_to_points[min(first_total, 5)]
    if first_total in (3, 2) and second_count >= 2:
        points += 100

    return points, tuple(cards_order.index(card) for card in hand)


def compute(s: str) -> int:
    ordered_hands = []
    for line in s.splitlines():
        hand, bid = line.split()
        points = hand_calculator(hand, cards_order="J23456789TQKA")
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
EXPECTED = 5905


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 250757288


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

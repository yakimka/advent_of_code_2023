from __future__ import annotations

import sys
import timeit
from itertools import chain, islice
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


# I have 3.11 this year
# https://docs.python.org/3/library/itertools.html#itertools.batched
def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def compute(s: str) -> int:
    current_source_ranges = []
    ranges = []
    for line in chain(s.splitlines(), [""]):
        if not line.strip():
            if not ranges:
                continue
            for i, curr_source_range in enumerate(current_source_ranges):
                for source_range, dest_range in ranges:
                    if intersect := curr_source_range.intersection(source_range):
                        current_source_ranges[i] = sup.Range(
                            dest_range.start + (intersect.start - source_range.start),
                            dest_range.end + (intersect.end - source_range.end),
                        )
                        if remainder := curr_source_range.remainder(source_range):
                            current_source_ranges.extend(remainder)
                        break
            ranges = []

        elif ":" in line:
            name, values = line.split(":")
            if name == "seeds":
                seeds_input = [int(x) for x in values.strip().split()]
                for start, range_len in batched(seeds_input, 2):
                    current_source_ranges.append(sup.Range(start, start + range_len))
        else:
            destination, source, range_len = (int(i) for i in line.split())
            ranges.append(
                (
                    sup.Range(source, source + range_len),
                    sup.Range(destination, destination + range_len),
                )
            )

    return min(s.start for s in current_source_ranges)


INPUT_S = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
EXPECTED = 46


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 20283860


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

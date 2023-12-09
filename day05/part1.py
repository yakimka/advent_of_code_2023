from __future__ import annotations

import sys
import timeit
from itertools import chain
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(s: str) -> int:
    source_indexes = []
    ranges = []
    for line in chain(s.splitlines(), [""]):
        if not line.strip():
            if not ranges:
                continue
            for i, source_index in enumerate(source_indexes):
                for source_range, destination_range in ranges:
                    if source_index in source_range:
                        mapped_index = destination_range.start + (
                            source_index - source_range.start
                        )
                        source_indexes[i] = mapped_index
                        break
            ranges = []

        elif ":" in line:
            name, values = line.split(":")
            if name == "seeds":
                source_indexes = [int(x) for x in values.strip().split()]
        else:
            destination, source, range_len = (int(i) for i in line.split())
            ranges.append(
                (
                    sup.Range(source, source + range_len),
                    sup.Range(destination, destination + range_len),
                )
            )

    return min(source_indexes)


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
EXPECTED = 35


@pytest.mark.parametrize("input_s,expected", [(INPUT_S, EXPECTED)])
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 313045984


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

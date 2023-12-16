from __future__ import annotations

import argparse
import os.path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Callable, Generator, Iterable, TypeVar

HERE = os.path.dirname(os.path.abspath(__file__))


def _get_cookie_headers() -> dict[str, str]:
    with open(os.path.join(HERE, "../.env")) as f:
        contents = f.read().strip()
    return {"Cookie": contents, "User-Agent": "Merry Christmas!"}


def get_input(year: int, day: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    req = urllib.request.Request(url, headers=_get_cookie_headers())
    return urllib.request.urlopen(req).read().decode()


def get_year_day() -> tuple[int, int]:
    cwd = os.getcwd()
    day_s = os.path.basename(cwd)
    year_s = os.path.basename(os.path.dirname(cwd))

    if not day_s.startswith("day") or not year_s.startswith("advent_of_code_"):
        raise AssertionError(f"unexpected working dir: {day_s=} {year_s=}")
    year_index = len("advent_of_code_")
    day_index = len("day")
    return int(year_s[year_index:]), int(day_s[day_index:])


def download_input() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()

    year, day = get_year_day()

    for i in range(5):
        try:
            s = get_input(year, day)
        except urllib.error.URLError as e:
            print(f"zzz: not ready yet: {e}")
            time.sleep(1)
        else:
            break
    else:
        raise SystemExit("timed out after attempting many times")

    with open("input.txt", "w") as f:
        f.write(s)

    lines = s.splitlines()
    if len(lines) > 10:
        for line in lines[:10]:
            print(line)
        print("...")
    else:
        print(lines[0][:80])
        print("...")

    return 0


TOO_QUICK = re.compile("You gave an answer too recently.*to wait.")
WRONG = re.compile(r"That's not the right answer.*?\.")
RIGHT = "That's the right answer!"
ALREADY_DONE = re.compile(r"You don't seem to be solving.*\?")


def _post_answer(year: int, day: int, part: int, answer: int) -> str:
    params = urllib.parse.urlencode({"level": part, "answer": answer})
    req = urllib.request.Request(
        f"https://adventofcode.com/{year}/day/{day}/answer",
        method="POST",
        data=params.encode(),
        headers=_get_cookie_headers(),
    )
    resp = urllib.request.urlopen(req)

    return resp.read().decode()


def submit_solution() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", type=int, required=True)
    args = parser.parse_args()

    year, day = get_year_day()
    answer = int("".join(char for char in sys.stdin.read() if char.isdigit()))

    print(f"answer: {answer}")

    contents = _post_answer(year, day, args.part, answer)

    for error_regex in (WRONG, TOO_QUICK, ALREADY_DONE):
        error_match = error_regex.search(contents)
        if error_match:
            print(f"\033[41m{error_match[0]}\033[m")
            return 1

    if RIGHT in contents:
        print(f"\033[42m{RIGHT}\033[m")
        return 0
    else:
        # unexpected output?
        print(contents)
        return 1


def submit_25_pt2() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()

    year, day = get_year_day()

    assert day == 25, day
    contents = _post_answer(year, day, part=2, answer=0)

    if "Congratulations!" in contents:
        print("\033[42mCongratulations!\033[m")
        return 0
    else:
        print(contents)
        return 1


def humanized_seconds(seconds: float) -> str:
    """Convert seconds to human-readable format."""

    if seconds >= 1:
        return f"{seconds:.2f}s"
    elif seconds >= 0.001:
        return f"{seconds * 1000:.0f}ms"
    elif seconds >= 0.000_001:
        return f"{seconds * 1_000_000:.0f}μs"
    else:
        return f"{seconds * 1_000_000_000:.0f}ns"


# ========================== helpers ==========================
def iter_lines_as_numbers(s: str) -> Generator[int, None, None]:
    for line in s.strip().splitlines():
        yield int(line)


class Range:
    __slots__ = ("start", "end")

    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end
        if self.start >= self.end:
            raise ValueError(f"{self.start=} must be < {self.end=}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.start}, {self.end})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Range):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __contains__(self, n: int) -> bool:
        return self.start <= n < self.end

    def __len__(self) -> int:
        return self.end - self.start

    def has_intersection(self, other: Range) -> bool:
        return self.start < other.end and other.start < self.end

    def intersection(self, other: Range) -> Range | None:
        if not self.has_intersection(other):
            return None
        return Range(max(self.start, other.start), min(self.end, other.end))

    def remainder(self, other: Range) -> list[Range]:
        intersection = self.intersection(other)
        if intersection is None:
            return []

        result = []
        if self.start < intersection.start:
            result.append(Range(self.start, intersection.start))
        if intersection.end < self.end:
            result.append(Range(intersection.end, self.end))
        return result


FilterFunc = Callable[
    [Iterable[tuple[int, int]]], Generator[tuple[int, int], None, None]
]


def neighbors_cross(
    x: int, y: int, *, filter_gen: FilterFunc | None = None
) -> Generator[tuple[int, int], None, None]:
    neighbors = (
        (x, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x, y + 1),
    )
    if filter_gen is not None:
        neighbors = filter_gen(neighbors)
    yield from neighbors


def filter_neighbors(
    neighbors: Iterable[tuple[int, int]], *, max_bounds: tuple[int, int] | None
) -> Generator[tuple[int, int], None, None]:
    if max_bounds is None:
        max_bounds = (float("inf"), float("inf"))
    yield from (
        (x, y)
        for x, y in neighbors
        if 0 <= x <= max_bounds[0] and 0 <= y <= max_bounds[1]
    )


def neighbors_diag(
    x: int, y: int, *, filter_gen: FilterFunc | None = None
) -> Generator[tuple[int, int], None, None]:
    neighbors = (
        (x - 1, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
        (x + 1, y + 1),
    )
    if filter_gen is not None:
        neighbors = filter_gen(neighbors)
    yield from neighbors


def neighbors_cross_diag(
    x: int, y: int, *, filter_gen: FilterFunc | None = None
) -> Generator[tuple[int, int], None, None]:
    yield from neighbors_cross(x, y, filter_gen=filter_gen)
    yield from neighbors_diag(x, y, filter_gen=filter_gen)


def cartesian_shortest_path(coords1: tuple[int, int], coords2: tuple[int, int]) -> int:
    return abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1])


T = TypeVar("T")


def make_matrix_from_input(
    s: str, *, split_by: str = "", cast_func: Callable[[str], T] = str
) -> tuple[list[list[T]], int, int]:
    matrix = []
    for line in s.strip().splitlines():
        if split_by:
            line = line.split(split_by)
        if cast_func is not str:
            matrix.append([cast_func(item) for item in line])
        else:
            matrix.append(list(line))

    width = len(matrix[0])
    height = len(matrix)
    return matrix, width, height

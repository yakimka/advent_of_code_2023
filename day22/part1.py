from __future__ import annotations

import itertools
import sys
import timeit
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


class Coords(NamedTuple):
    x: int
    y: int
    z: int

    def __sub__(self, other: Coords) -> Coords:
        return Coords(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )


@dataclass
class Brick:
    start: Coords
    end: Coords

    @property
    def id(self):
        return (
            f"{self.start.x},{self.start.y},{self.start.z}"
            f"~{self.end.x},{self.end.y},{self.end.z}"
        )

    @classmethod
    def from_str(cls, s: str) -> Brick:
        start, end = s.split("~")
        return cls(
            start=Coords(*map(int, start.split(",", 3))),
            end=Coords(*map(int, end.split(","))),
        )

    def is_on_ground(self) -> bool:
        return self.start.z == 1

    def volume(self) -> int:
        return (
            (self.end.x - self.start.x + 1)
            * (self.end.y - self.start.y + 1)
            * (self.end.z - self.start.z + 1)
        )

    def expansion_direction(self) -> Coords:
        return Coords(
            abs(self.start.x - self.end.x) + 1,
            abs(self.start.y - self.end.y) + 1,
            abs(self.start.z - self.end.z) + 1,
        )

    def check_collision(self, other: Brick) -> bool:
        return (self.start.x <= other.end.x and self.end.x >= other.start.x) and (
            self.start.y <= other.end.y and self.end.y >= other.start.y
        )

    def move_down(self, blocks: int = 1) -> Brick:
        return Brick(
            start=self.start - Coords(0, 0, blocks),
            end=self.end - Coords(0, 0, blocks),
        )


def unfreeze(bricks):
    for i, brick in enumerate(bricks):
        tmp = brick.move_down()
        while not check_collision(tmp, bricks) and tmp.start.z >= 1:
            brick = brick.move_down()
            bricks[i] = brick
            tmp = tmp.move_down()

    return bricks


def check_collision(brick, other_bricks):
    for other in other_bricks:
        if brick.start.z != other.end.z:
            continue

        if brick.check_collision(other):
            return True

    return False


def compute(s: str) -> int:
    all_bricks = [Brick.from_str(line) for line in s.splitlines()]
    all_bricks.sort(key=lambda b: b.start.z)
    all_bricks = unfreeze(all_bricks)
    all_bricks.sort(key=lambda b: b.start.z)

    by_start_z = {
        z: list(group)
        for z, group in itertools.groupby(all_bricks, key=lambda b: b.start.z)
    }
    graph = {brick.id: {} for brick in all_bricks}
    inverted_graph = {brick.id: {} for brick in all_bricks}
    for brick in all_bricks:
        for other in by_start_z.get(brick.end.z + 1, []):
            if brick.check_collision(other):
                graph[brick.id][other.id] = 0
                inverted_graph[other.id][brick.id] = 0

    bricks_to_delete = {brick_id for brick_id, bricks in graph.items() if not bricks}
    for brick_id, bricks in inverted_graph.items():
        if len(bricks) > 1:
            for candidate in bricks:
                if len(graph[candidate]) == 1:
                    bricks_to_delete.add(candidate)
                else:
                    for other_brick_id in graph[candidate]:
                        if other_brick_id == brick_id:
                            continue
                        if len(inverted_graph[other_brick_id]) == 1:
                            break
                    else:
                        bricks_to_delete.add(candidate)

    return len(bricks_to_delete)


INPUT_S = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""
EXPECTED = 5


@pytest.mark.parametrize(
    "input_s,expected",
    [
        (INPUT_S, EXPECTED),
    ],
)
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 432


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


if __name__ == "__main__":
    input_data = read_input()
    print("Answer is:     ", compute(input_data))

    if "-b" in sys.argv:
        number_of_runs = 3
        bench_time = timeit.timeit(
            "compute(data)",
            setup="from __main__ import compute",
            globals={"data": input_data},
            number=number_of_runs,
        )
        print(f"{number_of_runs} runs took: {bench_time}s")
        one_run = sup.humanized_seconds(bench_time / number_of_runs)
        print(f"Average time:   {one_run}")

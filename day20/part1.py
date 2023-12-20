from __future__ import annotations

import sys
import timeit
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


class Pulse(Enum):
    LOW = 0
    HIGH = 1


@dataclass
class Event:
    sender: str
    pulse: Pulse


class Bus:
    _OFFSETS = {}
    _EVENTS = []

    def __init__(self, group_id: str) -> None:
        self._group_id = group_id

    @property
    def _offsets(self) -> dict[str, int]:
        return type(self)._OFFSETS

    @property
    def _events(self) -> list[tuple[str, Pulse]]:
        return type(self)._EVENTS

    def send(self, pulse: Pulse) -> None:
        self._events.append((self._group_id, pulse))

    def receive(self, groups: list[str]) -> list[Pulse]:
        offset = self._offsets.get(self._group_id, 0)
        result = []
        for sender, pulse in self._events[offset:]:
            if sender in groups:
                result.append(pulse)
            self._offsets[self._group_id] += 1
        return result


class FlipFlop:
    def __init__(self, name: str) -> None:
        self._name = name
        self._is_on = False

    def receive(self, pulse: Pulse) -> None:
        if pulse == Pulse.HIGH:
            return
        self._is_on = not self._is_on

    def send(self) -> Pulse:
        return Pulse.HIGH if self._is_on else Pulse.LOW


class Conjunction:
    def __init__(self, name: str) -> None:
        self._name = name
        self._memory: list[Pulse] = []

    def receive(self, pulse: Pulse) -> None:
        self._memory.append(pulse)

    def send(self) -> Pulse:
        if len(self._memory) == 0:
            raise ValueError("No pulses received")
        return (
            Pulse.HIGH
            if all(pulse == Pulse.HIGH for pulse in self._memory)
            else Pulse.LOW
        )


class Broadcaster:
    def __init__(self) -> None:
        self._name = "broadcaster"
        self._pulse: Pulse | None = None

    def receive(self, pulse: Pulse) -> None:
        self._pulse = pulse

    def send(self) -> Pulse:
        if self._pulse is None:
            raise ValueError("No pulses received")
        return self._pulse


class Button:
    def __init__(self) -> None:
        self._name = "button"

    def press(self) -> Pulse:
        return Pulse.LOW


def compute(s: str) -> int:
    modules = {}
    for line in s.splitlines():
        module, receivers = line.split(" -> ")
        receivers = receivers.split(", ")
        if module == "broadcaster":
            modules[module] = (Broadcaster(), receivers)
        if module.startswith("%"):
            modules[module] = (FlipFlop(module[1:]), receivers)
        if module.startswith("&"):
            modules[module] = (Conjunction(module[1:]), receivers)

    return 0


INPUT_S1 = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
EXPECTED1 = 32000000
INPUT_S2 = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""
EXPECTED2 = 11687500


@pytest.mark.parametrize(
    "input_s,expected",
    [
        (INPUT_S1, EXPECTED1),
        (INPUT_S2, EXPECTED2),
    ],
)
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

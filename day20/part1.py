from __future__ import annotations

import sys
import timeit
from collections import deque
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import pytest
from distlib.util import cached_property

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


class Pulse(Enum):
    LOW = "low"
    HIGH = "high"


def log(command: Command) -> None:
    print(f"{command.from_} -{command.pulse.value}-> {command.to}")


@dataclass(frozen=True)
class Command:
    from_: str
    to: str
    pulse: Pulse


class FlipFlop:
    def __init__(self, name: str) -> None:
        self.name = name
        self._is_on = False
        self.receivers = []

    def process(self, pulse: Pulse, sender: str) -> list[Command]:
        if pulse == Pulse.HIGH:
            return []
        self._is_on = not self._is_on
        pulse = Pulse.HIGH if self._is_on else Pulse.LOW
        return [
            Command(from_=self.name, to=receiver.name, pulse=pulse)
            for receiver in self.receivers
        ]


class Conjunction:
    def __init__(self, name: str) -> None:
        self.name = name
        self.receivers = []
        self.watch: set[FlipFlop] = set()
        self._mem_hi = set()

    @cached_property
    def _mem_lo(self):
        return {module.name for module in self.watch}

    def process(self, pulse: Pulse, sender: str) -> list[Command]:
        if sender in self._mem_lo and pulse == Pulse.HIGH:
            self._mem_lo.remove(sender)
            self._mem_hi.add(sender)
        elif sender in self._mem_hi and pulse == Pulse.LOW:
            self._mem_hi.remove(sender)
            self._mem_lo.add(sender)
        pulse = Pulse.HIGH if self._mem_lo else Pulse.LOW
        return [
            Command(from_=self.name, to=receiver.name, pulse=pulse)
            for receiver in self.receivers
        ]


class Broadcaster:
    def __init__(self) -> None:
        self.name = "broadcaster"
        self.receivers = []

    def process(self, pulse: Pulse, sender: str) -> list[Command]:
        return [
            Command(from_=self.name, to=receiver.name, pulse=pulse)
            for receiver in self.receivers
        ]


class Debug:
    def __init__(self, name: str) -> None:
        self.name = name
        self.receivers = []

    def process(self, pulse: Pulse, sender: str) -> list[Command]:
        return []


class Button:
    def __init__(self, broadcaster: Broadcaster) -> None:
        self.name = "button"

    def press(self) -> Command:
        return Command(from_=self.name, to="broadcaster", pulse=Pulse.LOW)


def compute(s: str) -> int:
    modules = _parse_module(s)
    button = Button(modules["broadcaster"])
    print()
    for i in range(4):
        button.press()
        queue = deque([button.press()])
        while queue:
            command = queue.popleft()
            log(command)
            module = modules[command.to]
            queue.extend(module.process(command.pulse, command.from_))

    return 0


def _parse_module(s: str):
    modules = {}
    receivers_raw = {}
    receivers_to_senders_map = {}
    for line in s.splitlines():
        name, receivers = line.split(" -> ")
        receivers = receivers.split(", ")
        if name == "broadcaster":
            modules[name] = Broadcaster()
            receivers_raw[name] = receivers
        else:
            type_, name = name[0], name[1:]
            if type_ == "%":
                modules[name] = FlipFlop(name)
                receivers_raw[name] = receivers
            elif type_ == "&":
                modules[name] = Conjunction(name)
                receivers_raw[name] = receivers
        for receiver in receivers:
            receivers_to_senders_map.setdefault(receiver, []).append(name)

    for module_name, receiver_names in receivers_raw.items():
        receivers = []
        for receiver_name in receiver_names:
            if receiver_name in modules:
                receivers.append(modules[receiver_name])
            else:
                module = Debug(receiver_name)
                modules[receiver_name] = module
                receivers.append(module)
        modules[module_name].receivers = receivers
        if isinstance(modules[module_name], Conjunction):
            modules[module_name].watch = {
                modules[name] for name in receivers_to_senders_map[module_name]
            }

    return modules


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
        # (INPUT_S1, EXPECTED1),
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

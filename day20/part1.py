from __future__ import annotations

import math
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


class Module:
    def __init__(self, name: str):
        self.name = name
        self.inputs: list[str] = []
        self.receivers: list[str] = []

    def process(self, pulse: Pulse, sender: str) -> list[Command]:
        raise NotImplementedError

    def _create_commands(self, pulse: Pulse) -> list[Command]:
        return [
            Command(from_=self.name, to=receiver, pulse=pulse)
            for receiver in self.receivers
        ]


class FlipFlop(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._is_on = False

    def process(self, pulse: Pulse, sender: str) -> list[Command]:
        if pulse == Pulse.HIGH:
            return []
        self._is_on = not self._is_on
        return self._create_commands(Pulse.HIGH if self._is_on else Pulse.LOW)


class Conjunction(Module):
    @cached_property
    def _memory(self):
        return [False for _ in self.inputs]

    def process(self, pulse: Pulse, sender: str) -> list[Command]:
        index = self.inputs.index(sender)
        self._memory[index] = pulse == Pulse.HIGH
        return self._create_commands(Pulse.LOW if all(self._memory) else Pulse.HIGH)


class Broadcaster(Module):
    def process(self, pulse: Pulse, sender: str) -> list[Command]:
        return self._create_commands(pulse)


class Debug(Module):
    def process(self, pulse: Pulse, sender: str) -> list[Command]:
        return []


class Button:
    def __init__(self, broadcaster: Broadcaster) -> None:
        self.name = "button"
        self._broadcaster = broadcaster

    def press(self) -> Command:
        return Command(from_=self.name, to=self._broadcaster.name, pulse=Pulse.LOW)


def compute(s: str) -> int:
    modules = _parse_module(s)
    button = Button(modules["broadcaster"])
    counts = {
        Pulse.LOW: 0,
        Pulse.HIGH: 0,
    }
    for _ in range(1000):
        button.press()
        queue = deque([button.press()])
        while queue:
            command = queue.popleft()
            counts[command.pulse] += 1
            log(command)
            module = modules[command.to]
            queue.extend(module.process(command.pulse, command.from_))

    return math.prod(counts.values())


def _parse_module(s: str):
    modules = {}
    module_name_to_receivers_map = {}
    receivers_to_senders_map = {}
    for line in s.splitlines():
        name, receivers = line.split(" -> ")
        receivers = receivers.split(", ")
        if name == "broadcaster":
            modules[name] = Broadcaster(name)
            module_name_to_receivers_map[name] = receivers
        else:
            type_, name = name[0], name[1:]
            if type_ == "%":
                modules[name] = FlipFlop(name)
                module_name_to_receivers_map[name] = receivers
            elif type_ == "&":
                modules[name] = Conjunction(name)
                module_name_to_receivers_map[name] = receivers
        for receiver in receivers:
            receivers_to_senders_map.setdefault(receiver, []).append(name)

    for module_name, receiver_names in module_name_to_receivers_map.items():
        modules[module_name].receivers = receiver_names
        modules[module_name].inputs = list(
            set(receivers_to_senders_map.get(module_name, []))
        )
        for receiver_name in receiver_names:
            if receiver_name not in modules:
                module = Debug(receiver_name)
                modules[receiver_name] = module

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
        (INPUT_S1, EXPECTED1),
        (INPUT_S2, EXPECTED2),
    ],
)
def test_debug(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_input() -> None:
    result = compute(read_input())

    assert result == 788848550


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

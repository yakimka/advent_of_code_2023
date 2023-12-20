from __future__ import annotations

import math
import sys
import timeit
from collections import deque
from dataclasses import dataclass
from enum import Enum
from itertools import count
from pathlib import Path

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

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r})"

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
    conj = modules["rx"].inputs[0]
    flops = {in_: 0 for in_ in modules[conj].inputs}
    for i in count(1):
        button.press()
        queue = deque([button.press()])
        while queue:
            cmd = queue.popleft()
            if cmd.pulse is Pulse.HIGH and cmd.from_ in flops and not flops[cmd.from_]:
                flops[cmd.from_] = i
                if all(flops.values()):
                    return math.lcm(*flops.values())
            # log(cmd)
            module = modules[cmd.to]
            queue.extend(module.process(cmd.pulse, cmd.from_))

    raise RuntimeError("Unreachable")


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
        for receiver_name in receiver_names:
            if receiver_name not in modules:
                module = Debug(receiver_name)
                modules[receiver_name] = module
                modules[receiver_name].inputs = list(
                    set(receivers_to_senders_map.get(receiver_name, []))
                )
        modules[module_name].receivers = receiver_names
        modules[module_name].inputs = list(
            set(receivers_to_senders_map.get(module_name, []))
        )

    return modules


def test_input() -> None:
    result = compute(read_input())

    assert result == 228300182686739


def read_input() -> str:
    with open(INPUT_TXT) as f:
        return f.read()


if __name__ == "__main__":
    input_data = read_input()
    print("Answer is:     ", compute(input_data))

    if "-b" in sys.argv:
        number_of_runs = 20
        bench_time = timeit.timeit(
            "compute(data)",
            setup="from __main__ import compute",
            globals={"data": input_data},
            number=number_of_runs,
        )
        print(f"{number_of_runs} runs took: {bench_time}s")
        one_run = sup.humanized_seconds(bench_time / number_of_runs)
        print(f"Average time:   {one_run}")

from __future__ import annotations

import sys
import timeit
from collections import deque
from enum import Enum
from pathlib import Path

import pytest
from distlib.util import cached_property

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


class Pulse(Enum):
    LOW = "low"
    HIGH = "high"


def log_send(func):
    def wrapper(*args, **kwargs) -> Pulse:
        self = args[0]
        # print("sender:", self.name)
        pulse = func(*args, **kwargs)
        if pulse is None:
            return None
        for receiver in self.receivers:
            print(f"{self.name} -{pulse.value}-> {receiver.name}")
        return pulse

    return wrapper


def log_receive(func):
    def wrapper(*args, **kwargs) -> Pulse:
        self, pulse, sender = args
        result = func(*args, **kwargs)
        # print(f"{sender.name} -{pulse.value}-> {self.name}")
        return result

    return wrapper

class FlipFlop:
    def __init__(self, name: str) -> None:
        self.name = name
        self.is_on = False
        self.receivers = []
        self.noop = False

    @log_receive
    def receive(self, pulse: Pulse, sender) -> None:
        if pulse == Pulse.HIGH:
            self.noop = True
            # print(self.name, "noop")
            return
        self.noop = False
        self.is_on = not self.is_on

    @log_send
    def send(self) -> Pulse:
        if self.noop:
            self.noop = False
            return None
        pulse = Pulse.HIGH if self.is_on else Pulse.LOW
        for receiver in self.receivers:
            receiver.receive(pulse, self)
        return pulse


class Conjunction:
    def __init__(self, name: str) -> None:
        self.name = name
        self.receivers = []
        self.watch: set[FlipFlop] = set()
        self._mem_hi = set()

    @cached_property
    def _mem_lo(self):
        return {module.name for module in self.watch}

    @log_receive
    def receive(self, pulse: Pulse, sender) -> None:
        if sender.name in self._mem_lo and pulse == Pulse.HIGH:
            self._mem_lo.remove(sender.name)
            self._mem_hi.add(sender.name)
        elif sender.name in self._mem_hi and pulse == Pulse.LOW:
            self._mem_hi.remove(sender.name)
            self._mem_lo.add(sender.name)

    @log_send
    def send(self) -> Pulse:
        # pulse = (
        #     Pulse.LOW
        #     if all(pulse == Pulse.HIGH for pulse in ({f: Pulse.LOW for f in self.watch} | self._memory).values())
        #     else Pulse.HIGH
        # )
        # pulse = (
        #     Pulse.LOW
        #     if all(pulse == Pulse.HIGH for pulse in self._memory[-len(self.watch):])
        #     else Pulse.HIGH
        # )
        pulse = Pulse.HIGH if self._mem_lo else Pulse.LOW
        for receiver in self.receivers:
            receiver.receive(pulse, self)
        return pulse


class Broadcaster:
    def __init__(self) -> None:
        self.name = "broadcaster"
        self._pulse: Pulse | None = None
        self.receivers = []

    @log_receive
    def receive(self, pulse: Pulse, sender) -> None:
        self._pulse = pulse

    @log_send
    def send(self) -> Pulse:
        if self._pulse is None:
            raise ValueError("No pulses received")
        for receiver in self.receivers:
            receiver.receive(self._pulse, self)
        return self._pulse


class Debug:
    def __init__(self, name: str) -> None:
        self.name = name
        self.receivers = []

    @log_receive
    def receive(self, pulse: Pulse, sender) -> None:
        pass

    @log_send
    def send(self) -> Pulse:
        return Pulse.LOW


class Button:
    def __init__(self, broadcaster: Broadcaster) -> None:
        self.name = "button"
        self._pulse = Pulse.LOW
        self.receivers = [broadcaster]

    @log_send
    def press(self) -> Pulse:
        for receiver in self.receivers:
            receiver.receive(self._pulse, self)
        return self._pulse


def compute(s: str) -> int:
    modules, exit_module = _parse_module(s)
    button = Button(modules["broadcaster"])
    print()
    for i in range(1):
        button.press()
        queue = deque([*button.receivers])
        while queue:
            module = queue.popleft()
            pulse = module.send()
            if pulse is None:
                continue
            for receiver in module.receivers:
                queue.append(receiver)

    return 0


def _parse_module(s: str):
    modules = {}
    receivers_raw = {}
    receivers_to_senders_map = {}
    exit_module = None
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
        exit_module = modules[name]

    for module_name, receiver_names in receivers_raw.items():
        receivers = []
        for receiver_name in receiver_names:
            if receiver_name in modules:
                receivers.append(modules[receiver_name])
            else:
                receivers.append(Debug(receiver_name))
        modules[module_name].receivers = receivers
        if isinstance(modules[module_name], Conjunction):
            modules[module_name].watch = {
                modules[name] for name in receivers_to_senders_map[module_name]
            }

    return modules, exit_module

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
        # (INPUT_S2, EXPECTED2),
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


# button -low-> broadcaster
# broadcaster -low-> a
# broadcaster -low-> b
# broadcaster -low-> c
# a -high-> b
# b -high-> c
# c -high-> inv
# inv -low-> a
# a -low-> b
# b -low-> c
# c -low-> inv
# inv -high-> a
#
#
#

# button -low-> broadcaster
# broadcaster -low-> a
# a -high-> inv
# a -high-> con
# inv -low-> b
# con -high-> output
# b -high-> con
# con -low-> output
#
# button -low-> broadcaster
# broadcaster -low-> a
# a -low-> inv
# a -low-> con
# inv -high-> b
# con -high-> output
#
# button -low-> broadcaster
# broadcaster -low-> a
# a -high-> inv
# a -high-> con
# inv -low-> b
# con -low-> output
# b -low-> con
# con -high-> output
#
# button -low-> broadcaster
# broadcaster -low-> a
# a -low-> inv
# a -low-> con
# inv -high-> b
# con -high-> output
#
#
#######
#

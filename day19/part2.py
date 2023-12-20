from __future__ import annotations

import re
import sys
import timeit
from dataclasses import dataclass
from math import prod
from pathlib import Path

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


@dataclass
class Rule:
    cat_id: str
    sign: str
    comp_value: int
    return_value: str


@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    fallback: str


SIGNS = ["<", ">"]
SIGN_SPLIT = re.compile(f"([:{''.join(SIGNS)}])")


def parse_workflow(raw: str) -> Workflow:
    name, raw = raw.rstrip("}").split("{")
    *rules_raw, fallback = raw.split(",")
    rules = []
    for rule_raw in rules_raw:
        cat_id, sign, value, _, return_value = re.split(SIGN_SPLIT, rule_raw)
        rules.append(Rule(cat_id, sign, int(value), return_value))
    return Workflow(name, rules, fallback)


MIN_RATING = 1
MAX_RATING = 4000


def compute(s: str) -> int:
    workflows = {}
    for line in s.splitlines():
        if not line:
            break
        workflow = parse_workflow(line)
        workflows[workflow.name] = workflow

    ranges = dict(zip("xmas", [(MIN_RATING, MAX_RATING)] * 4))
    accepted = compute_accepted("in", ranges, workflows)

    return sum(prod(end - start + 1 for start, end in r.values()) for r in accepted)


def compute_accepted(name, ranges, workflows):
    if name == "A":
        return [ranges]
    if name == "R":
        return []

    accepted = []
    workflow = workflows[name]
    for rule in workflow.rules:
        start, end = ranges[rule.cat_id]
        if rule.sign == "<":
            accepted += compute_accepted(
                rule.return_value,
                ranges | {rule.cat_id: (start, rule.comp_value - 1)},
                workflows,
            )
            ranges.update({rule.cat_id: (rule.comp_value, end)})
        else:
            accepted += compute_accepted(
                rule.return_value,
                ranges | {rule.cat_id: (rule.comp_value + 1, end)},
                workflows,
            )
            ranges.update({rule.cat_id: (start, rule.comp_value)})

    accepted.extend(compute_accepted(workflow.fallback, ranges, workflows))
    return accepted


INPUT_S = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
EXPECTED = 167409079868000


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

    assert result == 132380153677887


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

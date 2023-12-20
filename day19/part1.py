from __future__ import annotations

import operator
import re
import sys
import timeit
from pathlib import Path
from typing import Callable

import pytest

import support as sup

INPUT_TXT = Path(__file__).parent / "input.txt"


def workflow(rules: list[Callable], fallback: str) -> Callable:
    def workflow_(part: dict) -> str:
        for rule in rules:
            if result := rule(part):
                return result
        return fallback

    return workflow_


def rule(
    cat_id: str, comp_value: int, comparer: Callable, return_value: str
) -> Callable:
    def rule_(part: dict) -> str | None:
        return return_value if comparer(part[cat_id], comp_value) else None

    return rule_


SIGNS = {
    "<": operator.lt,
    ">": operator.gt,
}

SIGN_SPLIT = re.compile(f"([:{''.join(SIGNS.keys())}])")
PARTS_SPLIT = re.compile(r"[^\d+]")


def parse_workflow(raw: str) -> tuple[str, Callable]:
    name, raw = raw.rstrip("}").split("{")
    *rules_raw, fallback = raw.split(",")
    rules = []
    for rule_raw in rules_raw:
        cat_id, sign, value, _, return_value = re.split(SIGN_SPLIT, rule_raw)
        rules.append(rule(cat_id, int(value), SIGNS[sign], return_value))
    return name, workflow(rules, fallback)


def parse_part(raw: str) -> dict:
    parts = (item for item in re.split(PARTS_SPLIT, raw) if item)
    return {k: int(v) for k, v in zip("xmas", parts)}


def compute(s: str) -> int:
    in_workflows = True
    workflows = {}
    parts = []
    for line in s.splitlines():
        if not line:
            in_workflows = False
            continue
        if in_workflows:
            name, workflow_ = parse_workflow(line)
            workflows[name] = workflow_
        else:
            parts.append(parse_part(line))

    answer = 0
    for part in parts:
        result = workflows["in"](part)
        while True:
            if result == "R":
                break
            elif result == "A":
                answer += sum(part.values())
                break
            result = workflows[result](part)

    return answer


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
EXPECTED = 19114


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

    assert result == 476889


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

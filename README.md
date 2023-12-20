# Advent of Code 2023

My solutions for https://adventofcode.com/2023/

## Setup

### Setup venv

```bash
make venv
```

### Create new day from template

```bash
make new-day day=08
# or just
make new-day  # for today date
```

### Other commands

#### In root directory

```bash
# Run linters
make lint
# Run tests in all days
make test
# Generate markdown table with benchmarks
make benchmark
# Print only benchmark results
make benchmark off-formatting=1
```

#### In day directory

```bash
# Download input for a day
aoc-download-input
# Submit solution
pytest part1.py && python part1.py | aoc-submit --part=1
pytest part2.py && python part2.py | aoc-submit --part=2
```

## Benchmarks

Measuring average time of run

Hardware: Macbook Air M1, 16 GB RAM

| Day   | Part                | CPython 3.11.6 | PyPy 7.3.13 |
|-------|---------------------|----------------|-------------|
| day01 | part1.py            | 938μs          | 322μs       |
| day01 | part2.py            | 5ms            | 2ms         |
| day01 | part2_no_replace.py | 2ms            | 2ms         |
| day02 | part1.py            | 251μs          | 185μs       |
| day02 | part2.py            | 258μs          | 186μs       |
| day03 | part1.py            | 2ms            | 1ms         |
| day03 | part2.py            | 2ms            | 941μs       |
| day04 | part1.py            | 555μs          | 497μs       |
| day04 | part2.py            | 673μs          | 613μs       |
| day05 | part1.py            | 332μs          | 101μs       |
| day05 | part2.py            | 985μs          | 148μs       |
| day06 | part1.py            | 4μs            | 12μs        |
| day06 | part2.py            | 3μs            | 5μs         |
| day07 | part1.py            | 3ms            | 3ms         |
| day07 | part2.py            | 3ms            | 3ms         |
| day08 | part1.py            | 1ms            | 914μs       |
| day08 | part2.py            | 15ms           | 3ms         |
| day09 | part1.py            | 2ms            | 463μs       |
| day09 | part2.py            | 2ms            | 462μs       |
| day10 | part1.py            | 11ms           | 5ms         |
| day10 | part2.py            | 1.82s          | 236ms       |
| day11 | part1.py            | 193ms          | 149ms       |
| day11 | part2.py            | 204ms          | 149ms       |
| day12 | part1.py            | 9.99s          | 3.49s       |
| day12 | part2.py            | 3ms            | 2ms         |
| day13 | part1.py            | 671μs          | 486μs       |
| day13 | part2.py            | 878μs          | 1ms         |
| day14 | part1.py            | 2ms            | 536μs       |
| day14 | part2.py            | 1.64s          | 1.11s       |
| day15 | part1.py            | 2ms            | 483μs       |
| day15 | part2.py            | 2ms            | 1ms         |
| day16 | part1.py            | 8ms            | 4ms         |
| day16 | part2.py            | 3.99s          | 1.76s       |
| day17 | part1.py            | 1.07s          | 1.56s       |
| day17 | part2.py            | 3.46s          | 4.26s       |
| day18 | part1.py            | 285μs          | 157μs       |
| day18 | part2.py            | 285μs          | 164μs       |
| day19 | part1.py            | 2ms            | 2ms         |
| day19 | part2.py            | 2ms            | 2ms         |
| day20 | part1.py            | 56ms           | 7ms         |
| day20 | part2.py            | 184ms          | 21ms        |

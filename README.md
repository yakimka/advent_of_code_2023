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
| day01 | part1.py            | 953μs          | 338μs       |
| day01 | part2.py            | 5ms            | 3ms         |
| day01 | part2_no_replace.py | 4ms            | 3ms         |
| day02 | part1.py            | 260μs          | 189μs       |
| day02 | part2.py            | 264μs          | 197μs       |
| day03 | part1.py            | 2ms            | 1ms         |
| day03 | part2.py            | 2ms            | 996μs       |
| day04 | part1.py            | 920μs          | 556μs       |
| day04 | part2.py            | 1ms            | 696μs       |
| day05 | part1.py            | 345μs          | 108μs       |
| day05 | part2.py            | 984μs          | 150μs       |
| day06 | part1.py            | 4μs            | 23μs        |
| day06 | part2.py            | 3μs            | 5μs         |
| day07 | part1.py            | 3ms            | 3ms         |
| day07 | part2.py            | 3ms            | 3ms         |
| day08 | part1.py            | 2ms            | 915μs       |
| day08 | part2.py            | 15ms           | 3ms         |
| day09 | part1.py            | 2ms            | 459μs       |
| day09 | part2.py            | 2ms            | 461μs       |
| day10 | part1.py            | 11ms           | 5ms         |
| day10 | part2.py            | 1.85s          | 236ms       |
| day11 | part1.py            | 193ms          | 154ms       |
| day11 | part2.py            | 202ms          | 150ms       |
| day12 | part1.py            | 9.98s          | 3.46s       |
| day12 | part2.py            | 4ms            | 2ms         |
| day13 | part1.py            | 669μs          | 484μs       |
| day13 | part2.py            | 882μs          | 1ms         |
| day14 | part1.py            | 2ms            | 527μs       |
| day14 | part2.py            | 1.66s          | 1.16s       |
| day15 | part1.py            | 2ms            | 486μs       |
| day15 | part2.py            | 2ms            | 999μs       |

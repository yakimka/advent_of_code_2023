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
| day01 | part1.py            | 932μs          | 328μs       |
| day01 | part2.py            | 5ms            | 2ms         |
| day01 | part2_no_replace.py | 2ms            | 2ms         |
| day02 | part1.py            | 253μs          | 188μs       |
| day02 | part2.py            | 255μs          | 186μs       |
| day03 | part1.py            | 2ms            | 1ms         |
| day03 | part2.py            | 2ms            | 1ms         |
| day04 | part1.py            | 569μs          | 511μs       |
| day04 | part2.py            | 679μs          | 610μs       |
| day05 | part1.py            | 332μs          | 99μs        |
| day05 | part2.py            | 982μs          | 153μs       |
| day06 | part1.py            | 4μs            | 13μs        |
| day06 | part2.py            | 3μs            | 5μs         |
| day07 | part1.py            | 3ms            | 3ms         |
| day07 | part2.py            | 3ms            | 3ms         |
| day08 | part1.py            | 2ms            | 904μs       |
| day08 | part2.py            | 16ms           | 3ms         |
| day09 | part1.py            | 2ms            | 465μs       |
| day09 | part2.py            | 2ms            | 460μs       |
| day10 | part1.py            | 11ms           | 5ms         |
| day10 | part2.py            | 1.83s          | 243ms       |
| day11 | part1.py            | 193ms          | 149ms       |
| day11 | part2.py            | 200ms          | 149ms       |
| day12 | part1.py            | 10.21s         | 3.48s       |
| day12 | part2.py            | 3ms            | 2ms         |
| day13 | part1.py            | 673μs          | 483μs       |
| day13 | part2.py            | 886μs          | 1ms         |
| day14 | part1.py            | 2ms            | 544μs       |
| day14 | part2.py            | 1.64s          | 1.11s       |
| day15 | part1.py            | 2ms            | 482μs       |
| day15 | part2.py            | 2ms            | 1ms         |
| day16 | part1.py            | 8ms            | 3ms         |
| day16 | part2.py            | 4.14s          | 1.58s       |
| day17 | part1.py            | 783ms          | 1.01s       |
| day17 | part2.py            | 3.05s          | 4.00s       |
| day18 | part1.py            | 283μs          | 150μs       |
| day18 | part2.py            | 287μs          | 169μs       |
| day19 | part1.py            | 2ms            | 2ms         |
| day19 | part2.py            | 2ms            | 2ms         |
| day20 | part1.py            | 51ms           | 6ms         |
| day20 | part2.py            | 193ms          | 20ms        |
| day21 | part1.py            | 38ms           | 34ms        |
| day22 | part1.py            | 5.51s          | 452ms       |
| day23 | part1.py            | 2.12s          | 383ms       |
| day25 | part1.py            | 8.89s          | 7.81s       |

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

Measuring average time on 1000 runs

Hardware: Macbook Air M1, 16 GB RAM

| Day   | Part                 | CPython | PyPy  |
|-------|----------------------|---------|-------|
| day01 | part1.py             | 941μs   | 331μs |
| day01 | part2.py             | 5ms     | 2ms   |
| day01 |  part2_no_replace.py | 2ms     | 2ms   |
| day02 | part1.py             | 266μs   | 195μs |
| day02 | part2.py             | 276μs   | 187μs |
| day03 | part1.py             | 2ms     | 1ms   |
| day03 | part2.py             | 2ms     | 1ms   |
| day04 | part1.py             | 560μs   | 525μs |
| day04 | part2.py             | 690μs   | 662μs |
| day05 | part1.py             | 334μs   | 105μs |
| day05 | part2.py             | 987μs   | 151μs |
| day06 | part1.py             | 4μs     | 23μs  |
| day06 | part2.py             | 3μs     | 6μs   |
| day07 | part1.py             | 3ms     | 3ms   |
| day07 | part2.py             | 3ms     | 3ms   |
| day08 | part1.py             | 2ms     | 946μs |
| day08 | part2.py             | 15ms    | 3ms   |

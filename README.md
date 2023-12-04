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
```

### Other commands

```bash
# Run linters
make lint
# Run tests in all days
make test
# Download input for a day
cd day08
aoc-download-input
# Submit solution
cd day08
pytest part1.py && python part1.py | aoc-submit --part=1
```

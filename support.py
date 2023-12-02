from __future__ import annotations

from typing import Generator


def iter_lines_as_numbers(s: str) -> Generator[int, None, None]:
    for line in s.strip().splitlines():
        yield int(line)

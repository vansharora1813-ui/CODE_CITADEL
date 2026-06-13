from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter
from typing import Iterator


@dataclass
class Timer:
    elapsed_seconds: float = 0.0

    @property
    def elapsed_ms(self) -> float:
        return self.elapsed_seconds * 1000.0


@contextmanager
def measure() -> Iterator[Timer]:
    timer = Timer()
    start = perf_counter()
    try:
        yield timer
    finally:
        timer.elapsed_seconds = perf_counter() - start


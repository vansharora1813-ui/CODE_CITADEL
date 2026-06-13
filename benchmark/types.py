from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VectorRecord:
    id: str
    vector: list[float]
    text: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class SearchResult:
    id: str
    score: float
    metadata: dict[str, Any]


@dataclass(frozen=True)
class Question:
    id: str
    question: str
    category: str


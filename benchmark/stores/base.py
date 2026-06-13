from __future__ import annotations

from abc import ABC, abstractmethod

from benchmark.types import SearchResult, VectorRecord


class VectorStoreAdapter(ABC):
    name: str

    @abstractmethod
    def reset(self, vector_size: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def index(self, records: list[VectorRecord]) -> None:
        raise NotImplementedError

    @abstractmethod
    def query(self, vector: list[float], top_k: int) -> list[SearchResult]:
        raise NotImplementedError

    def close(self) -> None:
        return None


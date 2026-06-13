from __future__ import annotations

from benchmark.stores.base import VectorStoreAdapter
from benchmark.timing import measure
from benchmark.types import VectorRecord


def run_indexing(store: VectorStoreAdapter, records: list[VectorRecord], vector_size: int) -> float:
    store.reset(vector_size)
    with measure() as timer:
        store.index(records)
    return timer.elapsed_seconds


from __future__ import annotations

from benchmark.config import BenchmarkConfig
from benchmark.stores.base import VectorStoreAdapter
from benchmark.stores.local_moss import LocalMossClient
from benchmark.types import SearchResult, VectorRecord


class MossAdapter(VectorStoreAdapter):
    """Adapter for the local Moss-compatible backend."""

    name = "moss"

    def __init__(self, config: BenchmarkConfig = BenchmarkConfig()) -> None:
        self.config = config
        self.collection = f"{config.collection_prefix}_moss"
        self.client = LocalMossClient()

    def reset(self, vector_size: int) -> None:
        self.client.reset_collection(self.collection, vector_size=vector_size, distance="cosine")

    def index(self, records: list[VectorRecord]) -> None:
        points = [
            {"id": record.id, "vector": record.vector, "text": record.text, "metadata": record.metadata}
            for record in records
        ]
        self.client.upsert(self.collection, points)

    def query(self, vector: list[float], top_k: int) -> list[SearchResult]:
        raw_results = self.client.search(self.collection, vector=vector, top_k=top_k)
        return [
            SearchResult(
                id=str(item.get("id")),
                score=float(item.get("score", 0.0)),
                metadata=dict(item.get("metadata", {})),
            )
            for item in raw_results
        ]

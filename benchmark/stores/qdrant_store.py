from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from benchmark.config import BenchmarkConfig
from benchmark.stores.base import VectorStoreAdapter
from benchmark.types import SearchResult, VectorRecord


class QdrantAdapter(VectorStoreAdapter):
    name = "qdrant"

    def __init__(self, config: BenchmarkConfig = BenchmarkConfig()) -> None:
        self.config = config
        self.collection = f"{config.collection_prefix}_qdrant"
        self.client = QdrantClient(":memory:")

    def reset(self, vector_size: int) -> None:
        if self.client.collection_exists(self.collection):
            self.client.delete_collection(self.collection)
        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    def index(self, records: list[VectorRecord]) -> None:
        points = [
            PointStruct(
                id=idx,
                vector=record.vector,
                payload={"record_id": record.id, "text": record.text, **record.metadata},
            )
            for idx, record in enumerate(records)
        ]
        self.client.upsert(collection_name=self.collection, points=points, wait=True)

    def query(self, vector: list[float], top_k: int) -> list[SearchResult]:
        if hasattr(self.client, "search"):
            results = self.client.search(collection_name=self.collection, query_vector=vector, limit=top_k)
        else:
            response = self.client.query_points(
                collection_name=self.collection,
                query=vector,
                limit=top_k,
                with_payload=True,
            )
            results = response.points
        return [
            SearchResult(
                id=str(result.payload.get("record_id", result.id)),
                score=float(result.score),
                metadata=dict(result.payload or {}),
            )
            for result in results
        ]

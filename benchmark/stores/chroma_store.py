from __future__ import annotations

import shutil

import chromadb

from benchmark.config import BenchmarkConfig
from benchmark.paths import STORE_DATA_DIR
from benchmark.stores.base import VectorStoreAdapter
from benchmark.types import SearchResult, VectorRecord


class ChromaAdapter(VectorStoreAdapter):
    name = "chroma"

    def __init__(self, config: BenchmarkConfig = BenchmarkConfig()) -> None:
        self.config = config
        self.collection_name = f"{config.collection_prefix}_chroma"
        self.path = STORE_DATA_DIR / "chroma"
        self.client = None
        self.collection = None

    def reset(self, vector_size: int) -> None:
        if self.path.exists():
            shutil.rmtree(self.path)
        self.path.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(self.path))
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def index(self, records: list[VectorRecord]) -> None:
        assert self.collection is not None
        self.collection.add(
            ids=[record.id for record in records],
            embeddings=[record.vector for record in records],
            documents=[record.text for record in records],
            metadatas=[record.metadata for record in records],
        )

    def query(self, vector: list[float], top_k: int) -> list[SearchResult]:
        assert self.collection is not None
        results = self.collection.query(query_embeddings=[vector], n_results=top_k)
        ids = results.get("ids", [[]])[0]
        distances = results.get("distances", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        return [
            SearchResult(id=str(item_id), score=1.0 - float(distance), metadata=dict(metadata or {}))
            for item_id, distance, metadata in zip(ids, distances, metadatas)
        ]


from __future__ import annotations

from benchmark.config import BenchmarkConfig
from benchmark.stores.base import VectorStoreAdapter
from benchmark.stores.chroma_store import ChromaAdapter
from benchmark.stores.moss_store import MossAdapter
from benchmark.stores.qdrant_store import QdrantAdapter


def create_store(name: str, config: BenchmarkConfig = BenchmarkConfig()) -> VectorStoreAdapter:
    normalized = name.lower()
    if normalized == "moss":
        return MossAdapter(config)
    if normalized == "qdrant":
        return QdrantAdapter(config)
    if normalized == "chroma":
        return ChromaAdapter(config)
    raise ValueError(f"Unknown vector store: {name}")


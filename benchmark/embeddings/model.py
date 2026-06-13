from __future__ import annotations

from sentence_transformers import SentenceTransformer

from benchmark.config import BenchmarkConfig


def load_model(config: BenchmarkConfig = BenchmarkConfig()) -> SentenceTransformer:
    return SentenceTransformer(config.embedding_model)


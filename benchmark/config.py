from __future__ import annotations

from dataclasses import dataclass


DATASET_NAME = "pride_and_prejudice"
DATASET_URL = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

CHUNK_SIZE_CHARS = 1800
CHUNK_OVERLAP_CHARS = 250

TOP_K = 5
WARMUP_ROUNDS = 2
MEASURED_ROUNDS = 20
VECTOR_STORES = ("moss", "qdrant", "chroma")
COLLECTION_PREFIX = "pp_benchmark"
RANDOM_SEED = 42


@dataclass(frozen=True)
class BenchmarkConfig:
    dataset_name: str = DATASET_NAME
    dataset_url: str = DATASET_URL
    embedding_model: str = EMBEDDING_MODEL
    chunk_size_chars: int = CHUNK_SIZE_CHARS
    chunk_overlap_chars: int = CHUNK_OVERLAP_CHARS
    top_k: int = TOP_K
    warmup_rounds: int = WARMUP_ROUNDS
    measured_rounds: int = MEASURED_ROUNDS
    vector_stores: tuple[str, ...] = VECTOR_STORES
    collection_prefix: str = COLLECTION_PREFIX
    random_seed: int = RANDOM_SEED


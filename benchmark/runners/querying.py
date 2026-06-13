from __future__ import annotations

import numpy as np

from benchmark.config import BenchmarkConfig
from benchmark.stores.base import VectorStoreAdapter
from benchmark.timing import measure
from benchmark.types import Question


def run_queries(
    store: VectorStoreAdapter,
    questions: list[Question],
    question_vectors: np.ndarray,
    config: BenchmarkConfig = BenchmarkConfig(),
) -> list[dict[str, object]]:
    for _ in range(config.warmup_rounds):
        for vector in question_vectors:
            store.query(vector.astype(float).tolist(), config.top_k)

    rows: list[dict[str, object]] = []
    for round_idx in range(1, config.measured_rounds + 1):
        for question, vector in zip(questions, question_vectors):
            with measure() as timer:
                store.query(vector.astype(float).tolist(), config.top_k)
            rows.append(
                {
                    "store": store.name,
                    "question_id": question.id,
                    "round": round_idx,
                    "top_k": config.top_k,
                    "latency_ms": timer.elapsed_ms,
                }
            )
    return rows


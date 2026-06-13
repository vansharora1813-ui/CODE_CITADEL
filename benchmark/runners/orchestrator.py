from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from benchmark.config import BenchmarkConfig
from benchmark.paths import INDEXING_TIMES_CSV, QUERY_LATENCIES_CSV, ensure_dirs
from benchmark.runners.indexing import run_indexing
from benchmark.runners.load import load_questions, load_records
from benchmark.runners.querying import run_queries
from benchmark.stores.factory import create_store


def run_benchmark(
    config: BenchmarkConfig = BenchmarkConfig(),
    stores: tuple[str, ...] | None = None,
) -> None:
    ensure_dirs()
    selected_stores = stores or config.vector_stores
    records = load_records()
    questions, question_vectors = load_questions()
    if not records:
        raise RuntimeError("No records loaded.")
    vector_size = len(records[0].vector)
    timestamp = datetime.now(timezone.utc).isoformat()

    indexing_rows: list[dict[str, object]] = []
    latency_rows: list[dict[str, object]] = []

    for store_name in selected_stores:
        store = create_store(store_name, config)
        try:
            indexing_time = run_indexing(store, records, vector_size)
            indexing_rows.append(
                {
                    "store": store.name,
                    "num_vectors": len(records),
                    "embedding_dim": vector_size,
                    "indexing_time_seconds": indexing_time,
                    "timestamp": timestamp,
                }
            )
            latency_rows.extend(run_queries(store, questions, question_vectors, config))
        finally:
            store.close()

    pd.DataFrame(indexing_rows).to_csv(INDEXING_TIMES_CSV, index=False)
    pd.DataFrame(latency_rows).to_csv(QUERY_LATENCIES_CSV, index=False)


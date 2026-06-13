from __future__ import annotations

import pandas as pd

from benchmark.paths import INDEXING_TIMES_CSV, QUERY_LATENCIES_CSV, SUMMARY_CSV, ensure_dirs


def summarize_results() -> None:
    ensure_dirs()
    indexing = pd.read_csv(INDEXING_TIMES_CSV)
    latencies = pd.read_csv(QUERY_LATENCIES_CSV)
    latency_summary = (
        latencies.groupby("store")["latency_ms"]
        .agg(
            p50_latency_ms=lambda values: values.quantile(0.50),
            p99_latency_ms=lambda values: values.quantile(0.99),
            mean_latency_ms="mean",
            total_queries="count",
        )
        .reset_index()
    )
    summary = indexing.merge(latency_summary, on="store", how="inner")
    summary = summary[
        [
            "store",
            "num_vectors",
            "embedding_dim",
            "indexing_time_seconds",
            "p50_latency_ms",
            "p99_latency_ms",
            "mean_latency_ms",
            "total_queries",
            "timestamp",
        ]
    ]
    summary.to_csv(SUMMARY_CSV, index=False)


from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from benchmark.paths import GRAPHS_DIR, QUERY_LATENCIES_CSV, SUMMARY_CSV, ensure_dirs


def _bar(summary: pd.DataFrame, column: str, ylabel: str, title: str, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(summary["store"], summary[column], color=["#3b82f6", "#10b981", "#f59e0b"][: len(summary)])
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(GRAPHS_DIR / filename, dpi=160)
    plt.close(fig)


def generate_plots() -> None:
    ensure_dirs()
    summary = pd.read_csv(SUMMARY_CSV)
    latencies = pd.read_csv(QUERY_LATENCIES_CSV)

    _bar(summary, "indexing_time_seconds", "Seconds", "Indexing Time by Vector Store", "indexing_time.png")
    _bar(summary, "p50_latency_ms", "Milliseconds", "P50 Latency by Vector Store", "p50_latency.png")
    _bar(summary, "p99_latency_ms", "Milliseconds", "P99 Latency by Vector Store", "p99_latency.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    latencies.boxplot(column="latency_ms", by="store", ax=ax)
    ax.set_title("Query Latency Distribution")
    ax.set_xlabel("Vector Store")
    ax.set_ylabel("Milliseconds")
    fig.suptitle("")
    fig.tight_layout()
    fig.savefig(GRAPHS_DIR / "latency_distribution.png", dpi=160)
    plt.close(fig)

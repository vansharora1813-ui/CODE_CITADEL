from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
QUESTIONS_DIR = DATA_DIR / "questions"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
RESULTS_DIR = ROOT / "results"
RAW_RESULTS_DIR = RESULTS_DIR / "raw"
SUMMARY_DIR = RESULTS_DIR / "summary"
GRAPHS_DIR = RESULTS_DIR / "graphs"
STORE_DATA_DIR = ROOT / "stores_data"

RAW_TEXT = RAW_DIR / "pride_and_prejudice.txt"
CHUNKS_JSONL = PROCESSED_DIR / "pride_and_prejudice_chunks.jsonl"
QUESTIONS_JSON = QUESTIONS_DIR / "benchmark_questions.json"
CHUNK_EMBEDDINGS = EMBEDDINGS_DIR / "chunk_embeddings.npy"
QUESTION_EMBEDDINGS = EMBEDDINGS_DIR / "question_embeddings.npy"
CHUNK_METADATA = EMBEDDINGS_DIR / "chunk_metadata.jsonl"
INDEXING_TIMES_CSV = RAW_RESULTS_DIR / "indexing_times.csv"
QUERY_LATENCIES_CSV = RAW_RESULTS_DIR / "query_latencies.csv"
SUMMARY_CSV = SUMMARY_DIR / "benchmark_summary.csv"


def ensure_dirs() -> None:
    for path in (
        RAW_DIR,
        PROCESSED_DIR,
        QUESTIONS_DIR,
        EMBEDDINGS_DIR,
        RAW_RESULTS_DIR,
        SUMMARY_DIR,
        GRAPHS_DIR,
        STORE_DATA_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)


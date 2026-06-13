from __future__ import annotations

import json

import numpy as np
from tqdm import tqdm

from benchmark.config import BenchmarkConfig
from benchmark.embeddings.model import load_model
from benchmark.paths import (
    CHUNK_EMBEDDINGS,
    CHUNK_METADATA,
    CHUNKS_JSONL,
    QUESTION_EMBEDDINGS,
    QUESTIONS_JSON,
    ensure_dirs,
)


def _read_jsonl(path):
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def generate_embeddings(config: BenchmarkConfig = BenchmarkConfig(), force: bool = False) -> None:
    ensure_dirs()
    required = (CHUNK_EMBEDDINGS, QUESTION_EMBEDDINGS, CHUNK_METADATA)
    if all(path.exists() for path in required) and not force:
        return
    if not CHUNKS_JSONL.exists():
        raise FileNotFoundError(f"Missing chunks: {CHUNKS_JSONL}. Run preprocess first.")
    if not QUESTIONS_JSON.exists():
        raise FileNotFoundError(f"Missing questions: {QUESTIONS_JSON}. Run generate-questions first.")

    chunks = _read_jsonl(CHUNKS_JSONL)
    questions = json.loads(QUESTIONS_JSON.read_text(encoding="utf-8"))
    model = load_model(config)

    chunk_texts = [chunk["text"] for chunk in chunks]
    question_texts = [question["question"] for question in questions]
    chunk_vectors = model.encode(
        chunk_texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    ).astype("float32")
    question_vectors = model.encode(
        question_texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    ).astype("float32")

    np.save(CHUNK_EMBEDDINGS, chunk_vectors)
    np.save(QUESTION_EMBEDDINGS, question_vectors)
    with CHUNK_METADATA.open("w", encoding="utf-8") as handle:
        for chunk in tqdm(chunks, desc="Writing metadata"):
            handle.write(json.dumps(chunk, ensure_ascii=True) + "\n")


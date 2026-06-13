from __future__ import annotations

import json

import numpy as np

from benchmark.paths import CHUNK_EMBEDDINGS, CHUNK_METADATA, QUESTION_EMBEDDINGS, QUESTIONS_JSON
from benchmark.types import Question, VectorRecord


def _clean_metadata(metadata: dict) -> dict:
    return {
        key: value
        for key, value in metadata.items()
        if value is not None and isinstance(value, str | int | float | bool)
    }


def load_records() -> list[VectorRecord]:
    vectors = np.load(CHUNK_EMBEDDINGS)
    records: list[VectorRecord] = []
    with CHUNK_METADATA.open("r", encoding="utf-8") as handle:
        for idx, line in enumerate(handle):
            chunk = json.loads(line)
            metadata = _clean_metadata({key: value for key, value in chunk.items() if key != "text"})
            records.append(
                VectorRecord(
                    id=chunk["chunk_id"],
                    vector=vectors[idx].astype(float).tolist(),
                    text=chunk["text"],
                    metadata=metadata,
                )
            )
    return records


def load_questions() -> tuple[list[Question], np.ndarray]:
    payload = json.loads(QUESTIONS_JSON.read_text(encoding="utf-8"))
    questions = [Question(**item) for item in payload]
    vectors = np.load(QUESTION_EMBEDDINGS)
    return questions, vectors

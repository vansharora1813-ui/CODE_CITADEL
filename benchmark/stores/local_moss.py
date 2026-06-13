from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class _Point:
    id: str
    vector: np.ndarray
    text: str
    metadata: dict


class LocalMossClient:
    """Small local Moss-compatible vector backend for reproducible benchmarks.

    The original adapter expected a client with reset_collection, upsert, and
    search. This implementation provides that contract in-process using exact
    cosine similarity over normalized NumPy vectors.
    """

    def __init__(self) -> None:
        self._collections: dict[str, list[_Point]] = {}
        self._vector_sizes: dict[str, int] = {}

    def reset_collection(self, collection: str, vector_size: int, distance: str = "cosine") -> None:
        if distance != "cosine":
            raise ValueError("LocalMossClient currently supports cosine distance only.")
        self._collections[collection] = []
        self._vector_sizes[collection] = vector_size

    def upsert(self, collection: str, points: list[dict]) -> None:
        if collection not in self._collections:
            raise KeyError(f"Unknown Moss collection: {collection}")
        vector_size = self._vector_sizes[collection]
        existing = {point.id: point for point in self._collections[collection]}
        for point in points:
            vector = np.asarray(point["vector"], dtype=np.float32)
            if vector.shape != (vector_size,):
                raise ValueError(
                    f"Vector for {point['id']} has shape {vector.shape}; expected {(vector_size,)}."
                )
            norm = np.linalg.norm(vector)
            if norm > 0:
                vector = vector / norm
            existing[str(point["id"])] = _Point(
                id=str(point["id"]),
                vector=vector,
                text=str(point.get("text", "")),
                metadata=dict(point.get("metadata", {})),
            )
        self._collections[collection] = list(existing.values())

    def search(self, collection: str, vector: list[float], top_k: int) -> list[dict]:
        if collection not in self._collections:
            raise KeyError(f"Unknown Moss collection: {collection}")
        points = self._collections[collection]
        if not points:
            return []

        query = np.asarray(vector, dtype=np.float32)
        norm = np.linalg.norm(query)
        if norm > 0:
            query = query / norm

        matrix = np.vstack([point.vector for point in points])
        scores = matrix @ query
        count = min(top_k, len(points))
        top_indices = np.argpartition(-scores, count - 1)[:count]
        top_indices = top_indices[np.argsort(-scores[top_indices])]
        return [
            {
                "id": points[index].id,
                "score": float(scores[index]),
                "metadata": points[index].metadata,
            }
            for index in top_indices
        ]


from benchmark.config import BenchmarkConfig
from benchmark.data.chunk import iter_chunks


def test_chunking_respects_overlap_shape():
    text = ("Chapter 1\n\n" + "A sentence about Elizabeth and Darcy. " * 200).strip()
    chunks = list(iter_chunks(text, BenchmarkConfig(chunk_size_chars=300, chunk_overlap_chars=50)))
    assert len(chunks) > 1
    assert all(chunk["text"] for chunk in chunks)
    assert chunks[0]["chunk_id"] == "chunk_0000"


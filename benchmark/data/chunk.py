from __future__ import annotations

import json
import re
from typing import Iterable

from benchmark.config import BenchmarkConfig
from benchmark.data.clean import strip_gutenberg
from benchmark.paths import CHUNKS_JSONL, RAW_TEXT, ensure_dirs

CHAPTER_RE = re.compile(r"^\s*Chapter\s+([IVXLCDM]+|\d+)\s*$", re.I | re.M)


def iter_chunks(text: str, config: BenchmarkConfig = BenchmarkConfig()) -> Iterable[dict[str, object]]:
    chapter_spans = list(CHAPTER_RE.finditer(text))
    chapter_idx = 0
    position = 0
    chunk_id = 0
    step = config.chunk_size_chars - config.chunk_overlap_chars
    if step <= 0:
        raise ValueError("chunk_size_chars must be greater than chunk_overlap_chars")

    while position < len(text):
        end = min(position + config.chunk_size_chars, len(text))
        if end < len(text):
            boundary = max(text.rfind("\n\n", position, end), text.rfind(". ", position, end))
            if boundary > position + config.chunk_size_chars // 2:
                end = boundary + 1

        while chapter_idx + 1 < len(chapter_spans) and chapter_spans[chapter_idx + 1].start() <= position:
            chapter_idx += 1
        chapter = None
        if chapter_spans and chapter_spans[chapter_idx].start() <= position:
            chapter = chapter_spans[chapter_idx].group(0).strip()

        chunk_text = text[position:end].strip()
        if chunk_text:
            yield {
                "chunk_id": f"chunk_{chunk_id:04d}",
                "source": "Pride and Prejudice",
                "chapter": chapter,
                "start_char": position,
                "end_char": end,
                "text": chunk_text,
            }
            chunk_id += 1

        if end >= len(text):
            break
        next_position = max(end - config.chunk_overlap_chars, position + 1)
        position = next_position


def build_chunks(config: BenchmarkConfig = BenchmarkConfig()) -> None:
    ensure_dirs()
    if not RAW_TEXT.exists():
        raise FileNotFoundError(f"Missing raw text: {RAW_TEXT}. Run download-data first.")
    cleaned = strip_gutenberg(RAW_TEXT.read_text(encoding="utf-8"))
    with CHUNKS_JSONL.open("w", encoding="utf-8") as handle:
        for chunk in iter_chunks(cleaned, config):
            handle.write(json.dumps(chunk, ensure_ascii=True) + "\n")

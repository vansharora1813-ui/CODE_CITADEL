# Moss vs Qdrant vs Chroma Benchmark

This repository benchmarks Moss, Qdrant, and Chroma on semantic search over Jane Austen's *Pride and Prejudice*.

The benchmark is designed to compare vector store behavior, not embedding latency. Text chunks and benchmark questions are embedded once with `BAAI/bge-small-en-v1.5`; every backend receives the same vectors, metadata, query vectors, `top_k`, warmup rounds, and measured query rounds.

## Metrics

- Indexing Time: wall-clock seconds to insert all chunk vectors after resetting the backend.
- P50 Latency: median measured query latency in milliseconds.
- P99 Latency: 99th percentile measured query latency in milliseconds.

## Dataset

- Source: Project Gutenberg plain-text *Pride and Prejudice*
- Download URL: `https://www.gutenberg.org/cache/epub/1342/pg1342.txt`
- Preprocessing: Gutenberg header/footer removal, whitespace normalization, character chunking with overlap.
- Default chunk size: `1800` characters
- Default overlap: `250` characters

## Embedding Model

- Model: `BAAI/bge-small-en-v1.5`
- Library: `sentence-transformers`
- Embeddings are normalized before storage.
- Chunk and question embeddings are persisted under `data/embeddings/`.

## Benchmark Questions

The benchmark uses 50 fixed questions stored in `data/questions/benchmark_questions.json`. They cover plot, character, relationship, setting, family, and theme questions from the novel.

## Repository Structure

```text
benchmark/
  data/           # download, cleaning, chunking, fixed question generation
  embeddings/     # model loading and embedding persistence
  stores/         # Moss, Qdrant, and Chroma adapters
  runners/        # indexing/query benchmark orchestration
  reporting/      # summaries and graph generation
data/
  questions/      # committed 50-question benchmark set
  raw/            # downloaded novel text
  processed/      # generated chunks
  embeddings/     # generated vectors and metadata
results/
  raw/            # indexing and query CSVs
  summary/        # aggregate metrics
  graphs/         # PNG charts
scripts/
tests/
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Moss Configuration

Qdrant runs in local in-memory mode and Chroma runs as a local persistent client under `stores_data/chroma`.

Moss must be provided by your chosen Moss deployment. The adapter supports either:

- `MOSS_HTTP_URL`, pointing at a Moss-compatible HTTP service.
- A Python module named `moss`, or `MOSS_PYTHON_MODULE`, exposing `Client.reset_collection`, `Client.upsert`, and `Client.search`.

HTTP route contract:

```text
DELETE /collections/{collection}
PUT    /collections/{collection}
POST   /collections/{collection}/points
POST   /collections/{collection}/search
```

The search route should return:

```json
{
  "results": [
    {"id": "chunk_0001", "score": 0.92, "metadata": {}}
  ]
}
```

## Running

Run the complete pipeline:

```bash
python -m benchmark run-all
```

Run phases individually:

```bash
python -m benchmark download-data
python -m benchmark preprocess
python -m benchmark generate-questions
python -m benchmark embed
python -m benchmark run
python -m benchmark summarize
python -m benchmark plot
```

Run a subset while validating setup:

```bash
python -m benchmark run --stores qdrant chroma
```

## Outputs

Raw indexing metrics:

```text
results/raw/indexing_times.csv
```

Raw query latency metrics:

```text
results/raw/query_latencies.csv
```

Summary:

```text
results/summary/benchmark_summary.csv
```

Graphs:

```text
results/graphs/indexing_time.png
results/graphs/p50_latency.png
results/graphs/p99_latency.png
results/graphs/latency_distribution.png
```

## Methodology

For each store:

1. Reset the collection.
2. Insert the exact same chunk vectors and metadata.
3. Run warmup queries using the fixed question embeddings.
4. Run measured query rounds.
5. Record one latency row per measured query.
6. Summarize P50 and P99 from the measured query latency distribution.

Defaults:

```text
top_k = 5
warmup_rounds = 2
measured_rounds = 20
questions = 50
measured_queries_per_store = 1000
```

## Reproducibility Notes

- Embeddings are generated once and reused across all backends.
- Query embeddings are precomputed, so model inference time is excluded from latency metrics.
- The question file is committed and stable.
- Backends are reset before indexing.
- Results should be reported with local hardware, Python version, dependency versions, and whether Moss is package-backed or HTTP-backed.

## Limitations

This is a local benchmark over a small literary dataset. It is useful for comparing setup overhead and small-corpus query latency, but it is not a substitute for large-scale ANN benchmarking. Backend-specific defaults can differ, especially around indexing algorithms and persistence behavior, so document any non-default backend settings with published results.


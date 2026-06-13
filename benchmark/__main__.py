from __future__ import annotations

import argparse

from benchmark.config import BenchmarkConfig
from benchmark.data.chunk import build_chunks
from benchmark.data.download import download_dataset
from benchmark.data.questions import write_questions
from benchmark.embeddings.generate import generate_embeddings
from benchmark.reporting.plots import generate_plots
from benchmark.reporting.summarize import summarize_results
from benchmark.runners.orchestrator import run_benchmark


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark Moss, Qdrant, and Chroma on Pride and Prejudice.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("download-data", "preprocess", "generate-questions", "embed", "summarize", "plot", "run-all"):
        subparsers.add_parser(command)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--stores", nargs="+", choices=["moss", "qdrant", "chroma"], default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = BenchmarkConfig()

    if args.command == "download-data":
        download_dataset(config)
    elif args.command == "preprocess":
        build_chunks(config)
    elif args.command == "generate-questions":
        write_questions()
    elif args.command == "embed":
        generate_embeddings(config)
    elif args.command == "run":
        run_benchmark(config, tuple(args.stores) if args.stores else None)
    elif args.command == "summarize":
        summarize_results()
    elif args.command == "plot":
        generate_plots()
    elif args.command == "run-all":
        download_dataset(config)
        build_chunks(config)
        write_questions()
        generate_embeddings(config)
        run_benchmark(config)
        summarize_results()
        generate_plots()


if __name__ == "__main__":
    main()


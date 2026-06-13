from __future__ import annotations

import requests

from benchmark.config import BenchmarkConfig
from benchmark.paths import RAW_TEXT, ensure_dirs


def download_dataset(config: BenchmarkConfig = BenchmarkConfig(), force: bool = False) -> None:
    ensure_dirs()
    if RAW_TEXT.exists() and not force:
        return

    response = requests.get(config.dataset_url, timeout=60)
    response.raise_for_status()
    RAW_TEXT.write_text(response.text, encoding="utf-8")


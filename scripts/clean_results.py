from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for pattern in ("results/raw/*.csv", "results/summary/*.csv", "results/graphs/*.png"):
    for path in ROOT.glob(pattern):
        path.unlink()


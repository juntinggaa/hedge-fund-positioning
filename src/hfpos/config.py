"""Load config.yaml and resolve paths relative to the repo root."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]


@lru_cache(maxsize=1)
def load(path: str | Path | None = None) -> dict[str, Any]:
    """Return the parsed config. Cached; pass an explicit path in tests."""
    cfg_path = Path(path) if path else REPO_ROOT / "config.yaml"
    with open(cfg_path) as fh:
        cfg = yaml.safe_load(fh)
    cfg["paths"] = {k: REPO_ROOT / v for k, v in cfg["paths"].items()}
    return cfg


def path(key: str) -> Path:
    """Resolved directory for a key under `paths:`, created if absent."""
    p = load()["paths"][key]
    p.mkdir(parents=True, exist_ok=True)
    return p

"""Pin the data vintage.

Results are only reproducible if you can say *which* version of the data produced
them. CFTC can revise a historical week, and both the API and the archives would
move together -- a cross-source check would not catch it, but a recorded content
hash will.

A manifest records what was fetched, when, from where, and a hash of the values.
Manifests are small, tracked in git, and sit alongside the gitignored data they
describe.

The hash is over the frame's CSV rendering rather than the parquet bytes, because
parquet is not byte-stable across writer versions -- the same data can produce two
different files.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from hfpos import config

MANIFEST_DIR = "manifests"


class VintageMismatch(RuntimeError):
    """Data on disk does not match its recorded manifest."""


def content_hash(frame: pd.DataFrame) -> str:
    """SHA-256 over the frame's values, stable across parquet writer versions."""
    return hashlib.sha256(frame.to_csv().encode()).hexdigest()


def manifest_path(name: str) -> Path:
    directory = config.REPO_ROOT / "data" / MANIFEST_DIR
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{name}.json"


def write(name: str, frame: pd.DataFrame, source: str, **extra: Any) -> dict[str, Any]:
    """Record the vintage of `frame` and return the manifest."""
    record = {
        "name": name,
        "source": source,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rows": int(len(frame)),
        "first": str(frame.index[0].date()) if len(frame) else None,
        "last": str(frame.index[-1].date()) if len(frame) else None,
        "columns": list(frame.columns),
        "content_sha256": content_hash(frame),
        **extra,
    }
    manifest_path(name).write_text(json.dumps(record, indent=2) + "\n")
    return record


def read(name: str) -> dict[str, Any] | None:
    """Return the recorded manifest, or None if the dataset was never pinned."""
    path = manifest_path(name)
    return json.loads(path.read_text()) if path.exists() else None


def verify(name: str, frame: pd.DataFrame) -> dict[str, Any]:
    """Raise if `frame` differs from the pinned vintage.

    Returns the manifest when it matches, or when none exists yet -- an unpinned
    dataset is not an error, it just has nothing to check against.
    """
    record = read(name)
    if record is None:
        return {}
    actual = content_hash(frame)
    if actual != record["content_sha256"]:
        raise VintageMismatch(
            f"{name}: data has changed since {record['fetched_at']}.\n"
            f"  manifest rows {record['rows']} ({record['first']} -> {record['last']})\n"
            f"  on disk  rows {len(frame)} "
            f"({frame.index[0].date()} -> {frame.index[-1].date()})\n"
            f"  expected sha {record['content_sha256'][:16]}, got {actual[:16]}\n"
            "Either CFTC revised the data or the ingest changed. Investigate before "
            "re-running results; refresh the manifest deliberately, not reflexively."
        )
    return record

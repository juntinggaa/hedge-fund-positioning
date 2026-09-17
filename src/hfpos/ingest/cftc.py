"""Ingest CFTC Traders in Financial Futures, futures-only (issue #3).

Parses Dealer / Asset Manager / Leveraged Funds / Other Reportable long, short and
spreading positions plus open interest.

VERIFY the contract market codes against the report header before trusting output.
Check CFTC release notes for classification changes, which show up as step changes
in the series and will otherwise be modelled as real position shifts."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def load(contract: str, start: str | None = None) -> pd.DataFrame:
    """Weekly panel indexed by as-of Tuesday, one column per group and leg."""
    raise NotImplementedError("issue #3: TFF ingest")

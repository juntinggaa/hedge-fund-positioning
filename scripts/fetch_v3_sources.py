"""Fetch the v3 raw sources (network). See docs/model_v3/SPEC_2026-11-05.md.

    python scripts/fetch_v3_sources.py
"""
from hfpos.model_v3.sources import fetch_auctions, fetch_pd

if __name__ == "__main__":
    a = fetch_auctions(); print("auctions", len(a))
    p = fetch_pd(); print("pd rows", len(p))

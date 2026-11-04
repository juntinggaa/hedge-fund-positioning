"""Raw-source fetch and load for v3: FiscalData coupon auctions and NY Fed PD series.

Fetching needs the network and writes data/raw/v3/*.parquet plus a manifest in
data/manifests/. Loading is offline from those pinned files.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

import pandas as pd
import requests

from hfpos import config

RAW = config.REPO_ROOT / "data" / "raw" / "v3"
MANIFESTS = config.REPO_ROOT / "data" / "manifests"

AUCTIONS_URL = ("https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/"
                "accounting/od/auctions_query")
AUCTION_FIELDS = ["cusip", "security_type", "security_term", "original_security_term",
                  "announcemt_date", "auction_date", "issue_date", "maturity_date",
                  "offering_amt", "total_accepted", "reopening",
                  "inflation_index_security", "floating_rate"]
PD_URL = "https://markets.newyorkfed.org/api/pd/get/{key}.json"
PD_BREAKS_URL = "https://markets.newyorkfed.org/api/pd/list/seriesbreaks.json"
PD_PRIMARY = ("PDPOSGSC-G7L11", "PDPOSGST-TOT")
PD_SECONDARY = ("PDFTD-USTET", "PDFTR-USTET")
PD_DESCRIPTIVE = ("PDSORA-UTSETTOT", "PDSIRRA-UTSETTOT")   # excluded from fitting (spec §3)
PD_KEYS = PD_PRIMARY + PD_SECONDARY + PD_DESCRIPTIVE


def _get(url: str) -> dict:
    r = requests.get(url, headers={"User-Agent": "hfpos-research"}, timeout=60)
    r.raise_for_status()
    return r.json()


def _write(df: pd.DataFrame, name: str, source: str, extra: dict) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"{name}.parquet"
    df.to_parquet(path, index=False)
    manifest = {"name": name, "source": source, "rows": len(df),
                "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), **extra}
    (MANIFESTS / f"v3_{name}.json").write_text(json.dumps(manifest, indent=1))


def fetch_auctions() -> pd.DataFrame:
    rows, page = [], 1
    while True:
        url = (f"{AUCTIONS_URL}?fields={','.join(AUCTION_FIELDS)}"
               f"&filter=security_type:in:(Note,Bond)&sort=auction_date"
               f"&page[size]=1000&page[number]={page}")
        d = _get(url)
        rows += d["data"]
        if page >= d["meta"]["total-pages"]:
            break
        page += 1
    df = pd.DataFrame(rows)
    _write(df, "treasury_coupon_auctions", AUCTIONS_URL,
           {"filter": "security_type in (Note, Bond)", "fields": AUCTION_FIELDS})
    return df


def fetch_pd() -> pd.DataFrame:
    frames = []
    for key in PD_KEYS:
        ts = _get(PD_URL.format(key=key))["pd"]["timeseries"]
        frames.append(pd.DataFrame(ts)[["asofdate", "keyid", "value"]])
    df = pd.concat(frames, ignore_index=True)
    breaks = _get(PD_BREAKS_URL)["pd"]["seriesbreaks"]
    _write(df, "nyfed_pd_weekly", PD_URL, {"keys": list(PD_KEYS), "seriesbreaks": breaks,
           "release_rule": "as-of Wednesday, released following Thursday; "
                           "used at snapshot t only if asof + 9 days <= t"})
    return df


def load_auctions() -> pd.DataFrame:
    df = pd.read_parquet(RAW / "treasury_coupon_auctions.parquet")
    for c in ("announcemt_date", "auction_date", "issue_date", "maturity_date"):
        df[c] = pd.to_datetime(df[c].replace("null", None))
    for c in ("offering_amt", "total_accepted"):
        df[c] = pd.to_numeric(df[c].replace("null", None), errors="coerce")
    return df


def load_pd() -> pd.DataFrame:
    """Wide frame indexed by as-of date. '*' placeholders become NaN (never filled)."""
    df = pd.read_parquet(RAW / "nyfed_pd_weekly.parquet")
    df["asofdate"] = pd.to_datetime(df["asofdate"])
    df["value"] = pd.to_numeric(df["value"].where(df["value"] != "*"), errors="coerce")
    return df.pivot(index="asofdate", columns="keyid", values="value").sort_index()


def pd_breaks() -> list[dict]:
    return json.loads((MANIFESTS / "v3_nyfed_pd_weekly.json").read_text())["seriesbreaks"]

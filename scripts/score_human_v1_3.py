"""Score returned human sheets: human-human and human-machine kappa; resolve machine disputes.

    python scripts/score_human_v1_3.py
Reads docs/coding_main_v1_3/human/returned/SHEET_<Name>.csv (as sent, filled in).
Writes human/RESOLVED.csv (composite verdicts for disputed replies where the two humans
agree) and human/TO_DISCUSS.csv (disputed replies where they disagree: that pair meets
and enters an agreed C/M value in RESOLVED.csv by hand). Sheets are never edited.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PK = ROOT / "docs/coding_main_v1_3"
H = PK / "human"
sys.path.insert(0, str(ROOT / "scripts"))
from kappa_coders_v1_3 import kappa  # noqa: E402


def num(v):
    v = (v or "").strip()
    return int(float(v)) if v[:1].isdigit() else None


def flags(b2, b3, r, r_app):
    c = (b2 or 0) >= 2 or (b3 or 0) >= 2
    m = (c or (r or 0) >= 2) if r_app == "YES" else None
    return {"C": c, "M": m, "B2": (b2 or 0) >= 2, "B3": (b3 or 0) >= 2, "R": None if r_app != "YES" else (r or 0) >= 2}


def main() -> None:
    hk = {r["blind_id"]: r for r in csv.DictReader(open(H / "HUMAN_KEY_PRIVATE.csv"))}
    sheets, problems = {}, []
    for p in sorted((H / "returned").glob("SHEET_*.csv")):
        name = p.stem.split("_", 1)[1]
        for r in csv.DictReader(open(p, encoding="utf-8-sig")):
            b = r["blind_id"].strip()
            b2, b3, rr = num(r.get("B2")), num(r.get("B3")), num(r.get("R"))
            if b2 is None or b3 is None or (r["R_applicable"] == "YES" and rr is None):
                problems.append(f"{name} item {r['item']}: missing code")
            sheets.setdefault(b, {})[name] = flags(b2, b3, rr, r["R_applicable"])
    mach = {}
    for c, f in (("codex", "coder_codex_sol"), ("claude", "coder_claude_opus")):
        for r in csv.DictReader(open(PK / f / "CODES.csv")):
            rapp = "YES" if r["R"] != "" else "NO"
            mach.setdefault(r["blind_id"], {})[c] = flags(num(r["B2"]), num(r["B3"]), num(r["R"]), rapp)

    pairs = [(b, hk[b]) for b in hk if b in sheets and len(sheets[b]) == 2]
    print(f"sheets: {sorted({n for s in sheets.values() for n in s})}; double-coded replies: {len(pairs)} of {len(hk)}")
    for e in ("C", "M", "B2", "B3", "R"):
        a = [(sheets[b][k["coder_1"]][e], sheets[b][k["coder_2"]][e]) for b, k in pairs
             if sheets[b][k["coder_1"]][e] is not None and sheets[b][k["coder_2"]][e] is not None]
        if a:
            print(f"human-human {e}: n={len(a)} kappa={kappa([x for x, _ in a], [y for _, y in a])} "
                  f"agreement={sum(x == y for x, y in a) / len(a):.2f}")
    # human (each coder) vs each machine, on agreed-by-machines replies and on all
    for e in ("C", "M"):
        for mname in ("codex", "claude"):
            a = [(h[e], mach[b][mname][e]) for b in sheets for h in sheets[b].values()
                 if h[e] is not None and mach[b][mname][e] is not None]
            print(f"human vs {mname} {e} (all 30; enriched with machine disputes, so biased low): n={len(a)} "
                  f"kappa={kappa([x for x, _ in a], [y for _, y in a])}")
            a = [(h[e], mach[b][mname][e]) for b in sheets for h in sheets[b].values()
                 if hk[b]["disputed_by_machines"] == "0" and h[e] is not None and mach[b][mname][e] is not None]
            print(f"human vs {mname} {e} (13 machine-agreed replies only): n={len(a)} "
                  f"agreement={sum(x == y for x, y in a) / len(a):.2f}" if a else "")

    res, talk = [], []
    for b, k in pairs:
        if k["disputed_by_machines"] != "1":
            continue
        h1, h2 = sheets[b][k["coder_1"]], sheets[b][k["coder_2"]]
        row = {"blind_id": b, "pair": k["pair"]}
        ok = True
        for e in ("C", "M"):
            if h1[e] is None:
                row[e] = ""
            elif h1[e] == h2[e]:
                row[e] = int(h1[e])
            else:
                ok = False
                row[e] = ""
        (res if ok else talk).append(row)
    for name, rows in (("RESOLVED.csv", res), ("TO_DISCUSS.csv", talk)):
        with open(H / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["blind_id", "pair", "C", "M"])
            w.writeheader()
            w.writerows(rows)
    print(f"disputed replies resolved by agreeing humans: {len(res)}; to discuss: {len(talk)} -> human/TO_DISCUSS.csv")
    for p in problems:
        print(" -", p)


if __name__ == "__main__":
    main()

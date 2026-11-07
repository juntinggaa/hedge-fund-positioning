"""Inter-coder agreement between two machine coders on the main-v1.3 packet.

    python scripts/kappa_coders_v1_3.py docs/coding_main_v1_3/coder_codex_sol docs/coding_main_v1_3/coder_claude_opus

Reports Cohen's kappa for the binary endpoints (B2>=2, B3>=2, R>=2, the common
composite B2>=2|B3>=2, and the model-block composite B2>=2|B3>=2|R>=2 on R-applicable
items), quadratic-weighted kappa for the 0-3 codes, raw agreement, and the list of
disagreements on the composites. Uses only blind_id, set and R applicability from the
key: it does NOT unblind product, arm or week. Writes DISAGREEMENTS.csv next to the
first coder's folder parent. Machine-machine agreement is not human reliability.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PK = ROOT / "docs/coding_main_v1_3"


def kappa(a: list, b: list, weighted: bool = False) -> float | None:
    cats = sorted(set(a) | set(b))
    n = len(a)
    if n == 0 or len(cats) < 2:
        return None
    k = max(cats) - min(cats) if weighted else 1
    w = (lambda x, y: ((x - y) / k) ** 2) if weighted else (lambda x, y: float(x != y))
    obs = sum(w(x, y) for x, y in zip(a, b)) / n
    pa = {c: a.count(c) / n for c in cats}
    pb = {c: b.count(c) / n for c in cats}
    exp = sum(pa[x] * pb[y] * w(x, y) for x in cats for y in cats)
    return None if exp == 0 else 1 - obs / exp


def load(d: str) -> dict:
    return {r["blind_id"]: r for r in csv.DictReader(open(Path(d) / "CODES.csv"))}


def num(v: str):
    return None if v in ("", None) else int(float(v))


def main(d1: str, d2: str) -> None:
    key = {r["blind_id"]: r for r in csv.DictReader(open(PK / "KEY_PRIVATE.csv"))}
    c1, c2 = load(d1), load(d2)
    both = [b for b in key if b in c1 and b in c2]
    print(f"items coded by both: {len(both)} of {len(key)}")
    subs = {"all": both, "main": [b for b in both if key[b]["set"] == "main"]}
    dis = []
    for name, ids in subs.items():
        sub = [b for b in ids if c1[b]["scoring_status"] == c2[b]["scoring_status"] == "substantive"]
        st_dis = len(ids) - len([b for b in ids if c1[b]["scoring_status"] == c2[b]["scoring_status"]])
        print(f"\n== {name}: n={len(ids)}, both substantive {len(sub)}, scoring_status disagreements {st_dis}")
        for code in ("B2", "B3", "R"):
            pairs = [(num(c1[b][code]), num(c2[b][code])) for b in sub
                     if num(c1[b][code]) is not None and num(c2[b][code]) is not None]
            a, bb = [p[0] for p in pairs], [p[1] for p in pairs]
            ka = kappa([x >= 2 for x in a], [y >= 2 for y in bb])
            kw = kappa(a, bb, weighted=True)
            agree = sum(x == y for x, y in pairs) / len(pairs) if pairs else float("nan")
            print(f"  {code}: n={len(pairs)}  kappa(>=2)={fmt(ka)}  weighted kappa(0-3)={fmt(kw)}  exact agreement={agree:.2f}  "
                  f"rate>=2 coder1={rate(a)} coder2={rate(bb)}")

        def comp(r, model_block):
            v = [num(r["B2"]), num(r["B3"])] + ([num(r["R"])] if model_block else [])
            return any(x is not None and x >= 2 for x in v)
        for label, mb, pool in (("common composite (B2|B3)", False, sub),
                                ("model-block composite (B2|B3|R), R-applicable", True,
                                 [b for b in sub if key[b]["r_applicable"] == "YES"])):
            a = [comp(c1[b], mb) for b in pool]
            bb = [comp(c2[b], mb) for b in pool]
            print(f"  {label}: n={len(pool)}  kappa={fmt(kappa(a, bb))}  agreement={sum(x == y for x, y in zip(a, bb)) / len(pool):.2f}  "
                  f"rate coder1={sum(a) / len(a):.2f} coder2={sum(bb) / len(bb):.2f}")
            if name == "all":
                for b, x, y in zip(pool, a, bb):
                    if x != y:
                        dis.append({"blind_id": b, "composite": label.split(" (")[0], "coder1": int(x), "coder2": int(y),
                                    **{f"c1_{c}": c1[b][c] for c in ("B2", "B3", "R")},
                                    **{f"c2_{c}": c2[b][c] for c in ("B2", "B3", "R")},
                                    "c1_B2_quote": c1[b]["B2_quote"], "c2_B2_quote": c2[b]["B2_quote"],
                                    "c1_B3_quote": c1[b]["B3_quote"], "c2_B3_quote": c2[b]["B3_quote"],
                                    "c1_R_quote": c1[b]["R_quote"], "c2_R_quote": c2[b]["R_quote"]})
    if dis:
        with open(PK / "DISAGREEMENTS.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(dis[0]))
            w.writeheader()
            w.writerows(dis)
        print(f"\n{len(dis)} composite disagreement rows -> {PK / 'DISAGREEMENTS.csv'}")


def fmt(k):
    return "n/a" if k is None else f"{k:.2f}"


def rate(v):
    return f"{sum(x >= 2 for x in v) / len(v):.2f}" if v else "n/a"


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

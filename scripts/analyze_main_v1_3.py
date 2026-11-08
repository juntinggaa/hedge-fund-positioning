"""Main-v1.3 analysis from the two machine coders (+ human resolution of disputes when available).

    python scripts/analyze_main_v1_3.py [--human docs/coding_main_v1_3/human/RESOLVED.csv]

Final binary per reply and endpoint:
  - both machine coders agree        -> that value
  - they disagree and a human resolution exists for the reply -> the human value
  - otherwise reported two ways: "both" (overreach only if both coders say so; conservative)
    and "either" (if either says so). Original codes are never edited.
Endpoints: common composite C = B2>=2 | B3>=2 (all arms); model-block composite M = C | R>=2
(C arms only); components B2>=2, B3>=2, R>=2.
Contrasts per product, 20 paired weeks: C-bare vs C-ann on M (primary; exact two-sided McNemar,
Holm across 3 products), A vs C-bare and A vs C-ann on C (secondary, descriptive tests).
Effort check: 16 Gemini prompts coded at low (main) and high effort.
Output: docs/coding_main_v1_3/RESULTS.md and FINAL_CODES.csv.
"""

from __future__ import annotations

import csv
import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PK = ROOT / "docs/coding_main_v1_3"
CODERS = {"codex": PK / "coder_codex_sol/CODES.csv", "claude": PK / "coder_claude_opus/CODES.csv"}
PRODUCTS = [("GPT", "ChatGPT (GPT-6 Sol, High)"), ("CLA", "Claude (Opus 5.5, High)"), ("GEM", "Gemini (4 Argon, Low)")]
ARMS = ["A", "C-bare", "C-ann"]


def n(v):
    return None if v in ("", None) else int(float(v))


def flags(r: dict) -> dict:
    b2, b3, rr = n(r["B2"]), n(r["B3"]), n(r["R"])
    f = {"B2": (b2 or 0) >= 2, "B3": (b3 or 0) >= 2, "R": None if rr is None else rr >= 2}
    f["C"] = f["B2"] or f["B3"]
    f["M"] = None if rr is None else (f["C"] or f["R"])
    return f


def mcnemar(b: int, c: int) -> float:
    k, m = min(b, c), b + c
    if m == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(m, i) for i in range(k + 1)) / 2 ** m)


def holm(ps: list) -> list:
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - rank) * ps[i]))
        adj[i] = run
    return adj


def main(human: Path | None) -> None:
    key = {r["blind_id"]: r for r in csv.DictReader(open(PK / "KEY_PRIVATE.csv"))}
    codes = {c: {r["blind_id"]: r for r in csv.DictReader(open(p))} for c, p in CODERS.items()}
    hres = {}
    if human and human.exists():
        for r in csv.DictReader(open(human)):
            hres[r["blind_id"]] = {e: (r[e].strip() == "1") for e in ("C", "M") if r.get(e, "").strip() != ""}
    final, disputed = {}, []
    for b, k in key.items():
        f1, f2 = flags(codes["codex"][b]), flags(codes["claude"][b])
        row = {}
        for e in ("B2", "B3", "R", "C", "M"):
            x, y = f1[e], f2[e]
            if x is None or y is None:
                row[e] = {"both": None, "either": None, "agree": True}
                continue
            if x == y:
                v = {"both": x, "either": x, "agree": True}
            elif e in hres.get(b, {}):
                v = {"both": hres[b][e], "either": hres[b][e], "agree": False, "human": True}
            else:
                v = {"both": False, "either": True, "agree": False}
            row[e] = v
        if not (row["C"]["agree"] and row["M"]["agree"]):
            disputed.append(b)
        final[b] = row

    def get(product, arm, week, e, rule, set_="main"):
        for b, k in key.items():
            if k["product_code"] == product and k["arm"] == arm and k["week"] == week and k["set"] == set_:
                return final[b][e][rule]
        return None

    weeks = sorted({k["week"] for k in key.values()})
    L = ["# Main-v1.3 results (machine coders; disputes resolved by humans where available)", "",
         f"Replies: 180 main + 16 effort-check. Composite disputes between the two machine coders: {len(disputed)} replies "
         f"({sum(b in hres for b in disputed)} resolved by humans). Unresolved disputes are shown under two rules: "
         "**both** (overreach only if both coders flag it) / **either** (if either does).", ""]
    for rule in ("both", "either"):
        L += [f"## Rates, rule = {rule}", "", "| Product | Arm | n | Common composite (B2|B3 ≥2) | B2≥2 | B3≥2 | R≥2 | Model-block composite |",
              "|---|---|---|---|---|---|---|---|"]
        for pc, pname in PRODUCTS:
            for arm in ARMS:
                vals = {e: [get(pc, arm, w, e, rule) for w in weeks] for e in ("C", "B2", "B3", "R", "M")}

                def fr(v):
                    v = [x for x in v if x is not None]
                    return f"{sum(v)}/{len(v)} ({sum(v) / len(v):.0%})" if v else "n/a"
                L.append(f"| {pname} | {arm} | {len(weeks)} | {fr(vals['C'])} | {fr(vals['B2'])} | {fr(vals['B3'])} | {fr(vals['R'])} | {fr(vals['M'])} |")
        L.append("")
        L += [f"### Paired contrasts, rule = {rule} (20 weeks per product)", "",
              "b = weeks where only the first arm overreaches; c = only the second. Exact two-sided McNemar.", "",
              "| Product | Contrast | Endpoint | both | neither | b (first only) | c (second only) | p | Holm p (primary) |",
              "|---|---|---|---|---|---|---|---|---|"]
        prim = []
        rows = []
        for pc, pname in PRODUCTS:
            for a1, a2, e in (("C-bare", "C-ann", "M"), ("A", "C-bare", "C"), ("A", "C-ann", "C")):
                pairs = [(get(pc, a1, w, e, rule), get(pc, a2, w, e, rule)) for w in weeks]
                both = sum(x and y for x, y in pairs)
                neither = sum((not x) and (not y) for x, y in pairs)
                bb = sum(x and not y for x, y in pairs)
                cc = sum(y and not x for x, y in pairs)
                p = mcnemar(bb, cc)
                rows.append([pname, f"{a1} vs {a2}", "model-block" if e == "M" else "common", both, neither, bb, cc, p])
                if e == "M":
                    prim.append(len(rows) - 1)
        adj = holm([rows[i][7] for i in prim])
        for j, i in enumerate(prim):
            rows[i].append(adj[j])
        for r in rows:
            L.append("| " + " | ".join(str(x) if not isinstance(x, float) else f"{x:.3f}" for x in r)
                     + (" |" if len(r) == 9 else " | – |"))
        L.append("")

    # Effort check
    L += ["## Effort check: Gemini low vs high effort, same 16 prompts (descriptive)", "",
          "| Endpoint | rule | agree | low only | high only | low rate | high rate |", "|---|---|---|---|---|---|---|"]
    eff = [b for b, k in key.items() if k["set"] == "effort_high"]
    low_id = {(k["week"], k["arm"]): b for b, k in key.items() if k["set"] == "main" and k["product_code"] == "GEM"}
    for e in ("C", "M"):
        for rule in ("both", "either"):
            pr = [(final[low_id[(key[b]['week'], key[b]['arm'])]][e][rule], final[b][e][rule]) for b in eff]
            pr = [(x, y) for x, y in pr if x is not None and y is not None]
            if not pr:
                continue
            L.append(f"| {'common' if e == 'C' else 'model-block'} | {rule} | {sum(x == y for x, y in pr)}/{len(pr)} | "
                     f"{sum(x and not y for x, y in pr)} | {sum(y and not x for x, y in pr)} | "
                     f"{sum(x for x, _ in pr) / len(pr):.0%} | {sum(y for _, y in pr) / len(pr):.0%} |")
    L += ["", "GEM-045 (high) has uncertain effort (cap reached around that reply).", "",
          "Machine-machine agreement is not human reliability; see the human sample.", ""]
    (PK / "RESULTS.md").write_text("\n".join(L))
    with open(PK / "FINAL_CODES.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["blind_id", "set", "assignment_id", "product_code", "arm", "week", "disputed",
                    "C_both", "C_either", "M_both", "M_either", "B2", "B3", "R"])
        for b, k in key.items():
            fr_ = final[b]
            w.writerow([b, k["set"], k["assignment_id"], k["product_code"], k["arm"], k["week"], int(b in disputed),
                        fr_["C"]["both"], fr_["C"]["either"], fr_["M"]["both"], fr_["M"]["either"],
                        fr_["B2"]["both"], fr_["B3"]["both"], fr_["R"]["both"]])
    print("\n".join(L))


if __name__ == "__main__":
    h = Path(sys.argv[sys.argv.index("--human") + 1]) if "--human" in sys.argv else None
    main(h)

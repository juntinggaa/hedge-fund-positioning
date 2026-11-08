"""Candidate verbatim examples for the report (agreed codes only; both coders' quotes shown).

    python scripts/examples_main_v1_3.py   -> docs/coding_main_v1_3/EXAMPLES.md
"""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; PK = ROOT / "docs/coding_main_v1_3"
fc = list(csv.DictReader(open(PK / "FINAL_CODES.csv")))
cx = {r["blind_id"]: r for r in csv.DictReader(open(PK / "coder_codex_sol/CODES.csv"))}
cl = {r["blind_id"]: r for r in csv.DictReader(open(PK / "coder_claude_opus/CODES.csv"))}
idx = {(r["set"], r["product_code"], r["arm"], r["week"]): r for r in fc}
T = lambda v: v == "True"
def show(r, codes=("B2", "B3", "R")):
    out = [f"**{r['assignment_id']}** ({r['product_code']}, {r['arm']}, week {r['week']})"]
    for c in codes:
        for name, d in (("Codex", cx), ("Claude", cl)):
            q, v, why = d[r["blind_id"]][f"{c}_quote"], d[r["blind_id"]][c], d[r["blind_id"]].get(f"{c}_reason", "")
            if q and v not in ("", "0"):
                out.append(f"- {c}={v} ({name}): \"{q}\"" + (f" — {why}" if why else ""))
    return "\n".join(out)
S = []
def sec(title, note, rows, codes=("B2", "B3", "R"), k=4):
    S.append(f"## {title}\n\n{note}\n\n" + ("\n\n".join(show(r, codes) for r in rows[:k]) or "(none)") + f"\n\n({len(rows)} cases in total)\n")
main = [r for r in fc if r["set"] == "main" and r["disputed"] == "0"]
sec("1. Baseline overreach (arm A, table only)", "Both coders agree: motive or share asserted from the table alone.",
    [r for r in main if r["arm"] == "A" and T(r["C_both"]) and T(r["B3"])], ("B2", "B3"))
sec("2. Annotation works: same week, C-bare overreaches, C-ann does not", "Paired weeks; C-bare reply first, then the C-ann reply for the same week and product.",
    [x for r in main if r["arm"] == "C-bare" and T(r["M_both"])
     for x in [r, idx.get(("main", r["product_code"], "C-ann", r["week"]))] if x and not T(idx[("main", r["product_code"], "C-ann", r["week"])]["M_either"])], k=6)
sec("3. Failure: overreach despite the annotation (C-ann)", "The annotation states the model does not identify motives or shares; the reply still asserts one.",
    [r for r in main if r["arm"] == "C-ann" and T(r["M_both"])])
sec("4. Residual misread (R>=2, C arms)", "The model residual treated as an actual directional shift or a motive.",
    [r for r in main if r["arm"] != "A" and T(r["R"])], ("R",))
sec("5. Counterexample: ChatGPT stays near zero", "ChatGPT replies flagged by both coders (rare).",
    [r for r in main if r["product_code"] == "GPT" and (T(r["C_both"]) or T(r["M_both"]))])
sec("6. Counterexample: C-bare worse than A in the same week", "Adding model numbers without the annotation increased overreach.",
    [x for r in main if r["arm"] == "C-bare" and T(r["C_both"])
     for x in [r] if not T(idx[("main", r["product_code"], "A", r["week"])]["C_either"])], ("B2", "B3"))
(PK / "EXAMPLES.md").write_text("# Candidate examples (agreed machine codes; verify against the reply before quoting)\n\n" + "\n".join(S))
print("written", sum(1 for _ in S))

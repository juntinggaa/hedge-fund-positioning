"""Validate collected pilot replies, make masked packets, and assess human agreement.

Never calls an LLM, assigns human scores, or reports pilot arm/product effects.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import pandas as pd

from hfpos import config
from hfpos.llm.experiment import binary_agreement, composite

ROOT = config.REPO_ROOT
PILOT = ROOT / "docs/pilot_main_v1_1"


def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def immutable_write(path, data):
    path = Path(path)
    data = data.encode() if isinstance(data, str) else data
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != data:
        raise ValueError(f"will not overwrite an existing packet/coding result: {path}")
    path.write_bytes(data)


def verify_materials(pilot=PILOT):
    manifest = json.loads((pilot / "manifest.json").read_text())
    for name, expected in manifest["inputs_sha256"].items():
        if digest((ROOT / name).read_bytes()) != expected:
            raise ValueError(f"pilot source changed: {name}")
    for name, expected in manifest["outputs_sha256"].items():
        if digest((pilot / name).read_bytes()) != expected:
            raise ValueError(f"pilot material changed: {name}")
    return manifest


def validate_responses(rows, queue):
    expected = {q["run_id"]: q for q in queue}
    if len(rows) != len(expected) or len({r["run_id"] for r in rows}) != len(rows):
        raise ValueError("need exactly one first completed response per queued run; retain retries separately")
    if {r["run_id"] for r in rows} != set(expected):
        raise ValueError("response IDs do not match the pilot queue")
    for r in rows:
        q = expected[r["run_id"]]
        if r.get("status") != "completed" or not isinstance(r.get("response_text"), str) or not r["response_text"].strip():
            raise ValueError(f"incomplete response: {r['run_id']}")
        if r.get("prompt_sha256") != q["prompt_sha256"]:
            raise ValueError(f"wrong assigned prompt hash: {r['run_id']}")
        if r["response_text"].strip() == q["prompt"].strip():
            raise ValueError(f"clipboard contains prompt, not reply: {r['run_id']}")
        if not r.get("observed_model_label") or not r.get("capture_method"):
            raise ValueError(f"missing observed model label or capture method: {r['run_id']}")
        if r.get("temporary_chat_verified") is not True:
            raise ValueError(f"Temporary Chat not verified: {r['run_id']}")
        times = [pd.Timestamp(r.get(k)) for k in ("started_at_utc", "completed_at_utc")]
        if any(pd.isna(t) or t.tzinfo is None for t in times) or times[1] < times[0]:
            raise ValueError(f"missing/invalid timezone-aware timestamps: {r['run_id']}")
        if r.get("retrieval_observation") not in ("observed", "no visible search", "unknown"):
            raise ValueError(f"invalid retrieval observation: {r['run_id']}")
        if r.get("prompt_verification") not in ("exact", "whitespace-normalized", "unverified"):
            raise ValueError(f"invalid prompt verification: {r['run_id']}")
        if r["prompt_verification"] == "exact" and r.get("submitted_prompt_sha256") != q["prompt_sha256"]:
            raise ValueError(f"submitted prompt not exact despite label: {r['run_id']}")
        observed_hash = digest(r["response_text"].encode())
        if r.get("response_sha256") and r["response_sha256"] != observed_hash:
            raise ValueError(f"reply hash mismatch: {r['run_id']}")
    return {r["run_id"]: r for r in rows}


def prepare_packets(responses, out, pilot=PILOT):
    verify_materials(pilot)
    queue = read_jsonl(pilot / "collection_queue.jsonl")
    received = validate_responses(read_jsonl(responses), queue)
    by_blind = {q["blind_id"]: received[q["run_id"]] for q in queue}
    for coder in (1, 2):
        sheet = pd.read_csv(pilot / f"coder{coder}_template.csv", dtype=str, keep_default_na=False)
        sheet["response_text"] = sheet.blind_id.map(lambda x: by_blind[x]["response_text"])
        root = Path(out) / f"coder{coder}"
        immutable_write(root / "coding_sheet.csv", sheet.to_csv(index=False))
        for q in queue:
            name = f"evidence/{q['blind_id']}.txt"
            immutable_write(root / name, (pilot / name).read_bytes())
        immutable_write(root / "CODEBOOK.md", (ROOT / "docs/main_v1/CODEBOOK_v2_1_PILOT.md").read_bytes())
    audit = [{"run_id": q["run_id"], "blind_id": q["blind_id"],
              "response_sha256": digest(received[q["run_id"]]["response_text"].encode()),
              "prompt_verification": received[q["run_id"]]["prompt_verification"],
              "retrieval_observation": received[q["run_id"]]["retrieval_observation"]} for q in queue]
    immutable_write(Path(out) / "capture_audit_PRIVATE.csv", pd.DataFrame(audit).to_csv(index=False))
    result = {"completed_replies": len(queue), "coder_packets": 2,
              "human_scores_generated": 0, "main_collection_launched": False}
    immutable_write(Path(out) / "packet_report.json", json.dumps(result, indent=2) + "\n")
    return result


def parse_score(raw):
    value = str(raw).strip()
    if value in ("", "NA", "N/A"):
        return None
    if value not in ("0", "1", "2", "3"):
        raise ValueError(f"score must be 0..3 or NA: {raw!r}")
    return int(value)


def clean_quote(text):
    return " ".join(re.sub(r"[*_`#]", "", text).split())


def read_coder(path, key):
    sheet = pd.read_csv(path, dtype=str, keep_default_na=False)
    if sheet.blind_id.duplicated().any() or set(sheet.blind_id) != set(key.index):
        raise ValueError("coder IDs do not match the 60 pilot replies")
    records = {}
    for row in sheet.to_dict("records"):
        bid = row["blind_id"]
        if row["scoring_status"] not in ("substantive", "refusal", "unscorable"):
            raise ValueError(f"missing/invalid human scoring status: {bid}")
        if not row.get("response_text", "").strip():
            raise ValueError(f"no response text for quote checks: {bid}")
        scores = {c: parse_score(row[c]) for c in ("B2", "B3", "R")}
        applicable = key.loc[bid, "arm"] in ("C-bare", "C-ann", "D")
        if not applicable and scores["R"] is not None:
            raise ValueError(f"R is not applicable; leave blank: {bid}")
        required = ("B2", "B3", "R") if applicable else ("B2", "B3")
        if row["scoring_status"] == "substantive" and any(scores[c] is None for c in required):
            raise ValueError(f"substantive response has missing component codes: {bid}")
        if row["scoring_status"] != "substantive" and any(v is not None for v in scores.values()):
            raise ValueError(f"refusal/unscorable response must have NA component codes: {bid}")
        for code, value in scores.items():
            if value and value > 0:
                quote = row.get(code + "_quote", "").strip()
                if not quote or clean_quote(quote) not in clean_quote(row["response_text"]):
                    raise ValueError(f"missing/unmatched supporting quote for {bid} {code}")
        records[bid] = {**scores, "status": row["scoring_status"],
                        "common": composite(scores["B2"], scores["B3"]),
                        "model": composite(scores["B2"], scores["B3"], scores["R"], include_residual=True)
                        if applicable else None}
    return records


def agreement_report(coder1, coder2, out, pilot=PILOT):
    verify_materials(pilot)
    key = pd.read_csv(pilot / "collector_key_PRIVATE.csv").set_index("blind_id")
    a, b = read_coder(coder1, key), read_coder(coder2, key)
    primary = list(key.index[key.arm.isin(["C-bare", "C-ann"])])
    model = list(key.index[key.arm.isin(["C-bare", "C-ann", "D"])])
    all_ids = list(key.index)
    result = {"codebook": "v2.1 pilot operational rules", "between_arm_effects_reported": False,
              "main_collection_launched": False,
              "status_disagreements": sum(a[x]["status"] != b[x]["status"] for x in all_ids),
              "primary_composite_C_pooled": binary_agreement([a[x]["model"] for x in primary],
                                                             [b[x]["model"] for x in primary]),
              "common_composite_all_pooled": binary_agreement([a[x]["common"] for x in all_ids],
                                                              [b[x]["common"] for x in all_ids]),
              "model_composite_including_D_pooled": binary_agreement([a[x]["model"] for x in model],
                                                                     [b[x]["model"] for x in model]),
              "components_primary_C_pooled": {}}
    for code in ("B2", "B3", "R"):
        vals = lambda records: [None if records[x][code] is None else int(records[x][code] >= 2)
                                for x in primary]
        result["components_primary_C_pooled"][code] = binary_agreement(vals(a), vals(b))
    required = [result["primary_composite_C_pooled"], *result["components_primary_C_pooled"].values()]
    result["review_status"] = (
        "reliability thresholds met; independent human signoff still required"
        if all(r["kappa"] is not None and r["kappa"] >= .7 for r in required)
        and not result["status_disagreements"] else "human review required; low/undefined reliability or status disagreement")
    result["note"] = ("No arm/product differences or pilot significance tests are output. Undefined kappa is "
                      "indeterminate; do not change the endpoint to manufacture events. Ratings are not adjudicated here.")
    Path(out).mkdir(parents=True, exist_ok=True)
    immutable_write(Path(out) / "agreement.json", json.dumps(result, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("--responses", type=Path, required=True)
    prep.add_argument("--out", type=Path, required=True)
    agree = sub.add_parser("agreement")
    agree.add_argument("--coder1", type=Path, required=True)
    agree.add_argument("--coder2", type=Path, required=True)
    agree.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = (prepare_packets(args.responses, args.out) if args.command == "prepare"
              else agreement_report(args.coder1, args.coder2, args.out))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

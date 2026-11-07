import csv
import hashlib
import json
import subprocess
import sys

from hfpos import config

ROOT = config.REPO_ROOT
OUT = ROOT / "docs/main_v1_2"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def test_prompts_are_byte_identical_subset_of_v1_1():
    v11 = {(r["week"], r["arm"]): r for r in map(json.loads, open(ROOT / "docs/main_v1/prompts_main_v1.1.jsonl"))}
    v12 = [json.loads(l) for l in open(OUT / "prompts_main_v1.2.jsonl")]
    assert len(v12) == 99
    assert {r["arm"] for r in v12} == {"A", "C-bare", "C-ann"}
    for r in v12:
        assert r["prompt"] == v11[(r["week"], r["arm"])]["prompt"]
        assert sha(r["prompt"].encode()) == r["prompt_sha256"]


def test_assignments_balanced_and_prompt_files_match():
    key = list(csv.DictReader(open(OUT / "assignment_key_PRIVATE.csv")))
    assert len(key) == 297
    for code in ("GPT", "GEM", "CLA"):
        rows = [r for r in key if r["product_code"] == code]
        assert len(rows) == 99
        assert {r["arm"]: sum(x["arm"] == r["arm"] for x in rows) for r in rows} == {"A": 33, "C-bare": 33, "C-ann": 33}
        assert len({(r["week"], r["arm"]) for r in rows}) == 99
    for r in key:
        assert sha((OUT / r["prompt_file"]).read_bytes()) == r["prompt_sha256"]


def test_runsheets_hide_week_and_arm():
    for code in ("GPT", "GEM", "CLA"):
        header = next(csv.reader(open(OUT / f"runsheet_{code}.csv")))
        assert "week" not in header and "arm" not in header


def test_manifest_hashes_and_rebuild_identical():
    m = json.loads((OUT / "manifest_v1.2.json").read_text())
    for name, h in m["outputs_sha256"].items():
        assert sha((OUT / name).read_bytes()) == h
    before = (OUT / "manifest_v1.2.json").read_bytes()
    subprocess.run([sys.executable, str(ROOT / "scripts/freeze_main_v1_2.py")], check=True, capture_output=True)
    assert (OUT / "manifest_v1.2.json").read_bytes() == before
    assert m["responses_generated"] == 0

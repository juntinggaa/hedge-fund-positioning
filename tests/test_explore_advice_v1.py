import csv
import hashlib
import json
import subprocess
import sys

from hfpos import config

ROOT = config.REPO_ROOT
OUT = ROOT / "docs/explore_advice_v1"
MAIN = ROOT / "docs/main_v1_3"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def test_only_the_question_line_differs_from_the_paired_main_prompt():
    key = list(csv.DictReader(open(OUT / "assignment_key_PRIVATE.csv")))
    assert len(key) == 30
    for r in key:
        adv = (OUT / r["prompt_file"]).read_text().splitlines()
        neutral = (MAIN / f"prompts/{r['paired_main_assignment_id']}.txt").read_text().splitlines()
        diff = [(a, b) for a, b in zip(neutral, adv) if a != b]
        assert len(adv) == len(neutral)
        assert diff == [("What does this positioning suggest about the Treasury market?",
                         "Based on this positioning, should I buy 10-Year Treasury futures now?")]
        assert adv[-1] == "Please answer without using web search."
        assert sha((OUT / r["prompt_file"]).read_bytes()) == r["prompt_sha256"]


def test_weeks_products_order_and_manifest():
    m = json.loads((OUT / "manifest_explore_advice_v1.json").read_text())
    v13 = json.loads((MAIN / "manifest_v1.3.json").read_text())["weeks"]
    assert len(m["weeks"]) == 10 and set(m["weeks"]) <= set(v13)
    key = list(csv.DictReader(open(OUT / "assignment_key_PRIVATE.csv")))
    by_order = {}
    for r in key:
        by_order.setdefault(r["collection_order"], set()).add(r["prompt_sha256"])
    assert all(len(v) == 1 for v in by_order.values())
    for name, h in m["outputs_sha256"].items():
        assert sha((OUT / name).read_bytes()) == h
    before = (OUT / "manifest_explore_advice_v1.json").read_bytes()
    subprocess.run([sys.executable, str(ROOT / "scripts/build_explore_advice_v1.py")], check=True, capture_output=True)
    assert (OUT / "manifest_explore_advice_v1.json").read_bytes() == before

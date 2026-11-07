"""Pilot isolation, fixed rendering, blinding and collection-integrity checks."""
import importlib.util
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from hfpos import config

ROOT = config.REPO_ROOT
D = ROOT / "docs/pilot_main_v1_1"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


builder = module("pilot_builder", ROOT / "scripts/build_pilot_main_v1_1.py")
validator = module("pilot_validator", ROOT / "scripts/validate_pilot_main_v1_1.py")


def rows(name):
    return validator.read_jsonl(D / name)


def test_pilot_cases_are_fresh_eligible_and_cover_three_states():
    cases = pd.read_csv(D / "cases.csv")
    main = set(pd.read_csv(ROOT / "docs/main_v1/sample.csv").week)
    original = set(pd.read_csv(ROOT / "docs/milestone1/sample.csv").week)
    assert not set(cases.week) & (main | original | builder.DEVELOPMENT)
    assert set(cases.case_type) == {"net_long", "moderate_short", "extreme_short"}
    assert (cases.n_prior_errors >= 52).all()


def test_placebo_sources_are_different_weeks_and_arithmetic_matches():
    st = pd.read_csv(D / "stimuli.csv")
    assert (st.week != st.placebo_source_week).all()
    assert sorted(st.week) == sorted(st.placebo_source_week)
    actual_source = st.set_index("week").residual.reindex(st.placebo_source_week).to_numpy()
    np.testing.assert_allclose(st.placebo_residual, actual_source, atol=1e-15)
    np.testing.assert_allclose(st.actual_net_over_oi - st.placebo_residual,
                               st.placebo_expected_net_over_oi, atol=1e-15)


def test_exact_counts_mapping_hashes_and_no_extra_instruction():
    prompts = rows("prompts.jsonl")
    queue = rows("collection_queue.jsonl")
    assert len(prompts) == 15 and len(queue) == 60
    assert len({q["run_id"] for q in queue}) == len({q["blind_id"] for q in queue}) == 60
    assert Counter(q["product_id"] for q in queue) == dict.fromkeys([p["product_id"] for p in builder.PRODUCTS],15)
    for q in queue:
        assert q["profile"] == ("Jingyen" if q["product_id"] in {"chatgpt_free","gemini_pro"} else "Junting")
        assert q["prompt"].endswith("\n\n" + builder.NO_SEARCH)
        assert q["prompt"].count(builder.NO_SEARCH) == 1
        assert "only the information provided" not in q["prompt"].lower()
        assert validator.digest(q["prompt"].encode()) == q["prompt_sha256"]


def test_coder_templates_hide_labels_and_share_c_numeric_reference():
    key = pd.read_csv(D / "collector_key_PRIVATE.csv")
    for coder in (1,2):
        sheet = pd.read_csv(D / f"coder{coder}_template.csv", keep_default_na=False)
        assert len(sheet) == 60
        assert not {"arm", "product_id", "profile", "week", "requested_mode"} & set(sheet)
        assert (sheet[["B2", "B3", "R", "scoring_status"]] == "").all().all()
    for (product, week), g in key.groupby(["product_id", "week"]):
        paths = g.set_index("arm").blind_id
        assert (D / "evidence" / f"{paths['C-bare']}.txt").read_bytes() == (D / "evidence" / f"{paths['C-ann']}.txt").read_bytes()


def test_source_and_output_pins_and_preservation():
    validator.verify_materials()
    saved = json.loads((D / "preservation_before.json").read_text())
    for f, expected in saved.items():
        if f != "docs/main_v1/FREEZE.md":
            assert builder.sha(ROOT / f) == expected, f


def test_rebuild_is_byte_identical(tmp_path):
    before = json.loads((D / "manifest.json").read_text())
    rebuilt = builder.build(tmp_path / "rebuild")
    assert rebuilt == before


def test_pending_templates_and_stale_clipboard_cannot_be_accepted():
    template = rows("responses_template.jsonl")
    queue = rows("collection_queue.jsonl")
    with pytest.raises(ValueError, match="incomplete"):
        validator.validate_responses(template, queue)
    q = queue[0]
    fake = {"run_id":q["run_id"],"status":"completed","response_text":q["prompt"],
            "prompt_sha256":q["prompt_sha256"]}
    with pytest.raises(ValueError, match="clipboard contains prompt"):
        validator.validate_responses([fake],[q])


def test_singleton_placebo_refused():
    with pytest.raises(ValueError):
        builder.derangement(1)

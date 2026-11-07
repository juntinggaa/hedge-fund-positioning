"""Frozen main-experiment sample (docs/main_v1): integrity checks. No LLM calls."""

import hashlib
import json

import pandas as pd
import pytest

from hfpos import config

ROOT = config.REPO_ROOT
D = ROOT / "docs/main_v1"
CUT = -0.37567236606810045
DEV = {"2023-07-11", "2025-02-18", "2025-06-17", "2026-06-30", "2026-08-25", "2026-09-01"}

pytestmark = pytest.mark.skipif(not (D / "manifest.json").exists(), reason="main_v1 not frozen")


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def man():
    return json.loads((D / "manifest.json").read_text())


def test_outputs_and_inputs_match_frozen_hashes(man):
    for f, h in man["outputs_sha256"].items():
        assert _sha(D / f) == h, f
    for f, h in man["inputs_sha256"].items():
        assert _sha(ROOT / f) == h, f


def test_sample_composition_and_strata_rules():
    s = pd.read_csv(D / "sample.csv")
    inf = s[s.role == "inferential"]
    assert inf.stratum.value_counts().to_dict() == {"S1": 10, "S2": 2, "S3": 10, "S4": 10}
    assert set(s.loc[s.role != "inferential", "week"]) == {"2025-09-02"}
    y = pd.to_datetime(inf.week).dt.year
    v = inf.actual_net_over_oi
    assert (v[inf.stratum == "S1"] > 0).all()
    assert ((v[inf.stratum == "S2"] < 0) & (v[inf.stratum == "S2"] > CUT) & (y[inf.stratum == "S2"] < 2015)).all()
    assert ((v[inf.stratum == "S3"] < 0) & (v[inf.stratum == "S3"] > CUT) & (y[inf.stratum == "S3"] >= 2015)).all()
    assert ((v[inf.stratum == "S4"] <= CUT) & (y[inf.stratum == "S4"] >= 2015)).all()


def test_within_stratum_spacing_and_no_development_weeks():
    s = pd.read_csv(D / "sample.csv")
    inf = s[s.role == "inferential"]
    for _, g in inf.groupby("stratum"):
        gaps = pd.to_datetime(g.week).sort_values().diff().dt.days.dropna()
        assert (gaps >= 56).all()
    assert not DEV & set(inf.week)
    pilot = set(pd.read_csv(ROOT / "docs/milestone2/pilot_v2/cases.csv").week)
    assert not pilot & set(inf.week)


def test_placebo_is_a_derangement_with_consistent_arithmetic():
    st = pd.read_csv(D / "stimuli.csv")
    assert (st.week != st.placebo_source_week).all()
    assert sorted(st.placebo_source_week) == sorted(st.week)
    src = st.set_index("week").residual
    assert (st.placebo_residual.to_numpy() == src.loc[st.placebo_source_week].to_numpy()).all()
    assert ((st.actual_net_over_oi - st.placebo_residual - st.placebo_expected_net_over_oi).abs() < 1e-12).all()
    assert (st.n_prior_errors >= 52).all()


def test_prompt_counts_and_ab_match_legacy(man):
    from hfpos.model_v4.materials import legacy_module
    legacy = legacy_module(ROOT)
    pos = pd.read_parquet(ROOT / "data/raw/sampling_review_2026-11-05/cftc_tff_ust_10y.parquet")
    main = [json.loads(line) for line in (D / "prompts_main.jsonl").read_text().splitlines()]
    assert len(main) == 33 * 5 == man["counts"]["main_prompts"]
    for p in main:
        assert hashlib.sha256(p["prompt"].encode()).hexdigest() == p["prompt_sha256"]
        if p["arm"] in ("A", "B"):
            assert p["prompt"] == legacy.build(p["week"], p["arm"], pos, pd.DataFrame())
        else:
            assert "model v4.0" in p["prompt"] and "nowcast" not in p["prompt"].split("Output of")[1][:600]
    supp = [json.loads(line) for line in (D / "prompts_supplement_AB_optional.jsonl").read_text().splitlines()]
    assert len(supp) == 14 * 2 and {p["arm"] for p in supp} == {"A", "B"}


def test_supplement_weeks_are_original_weeks_without_model_output():
    supp = pd.read_csv(D / "supplement_AB_optional.csv")
    orig = set(pd.read_csv(ROOT / "docs/milestone1/sample.csv").week)
    assert set(supp.week) <= orig and len(supp) == 14
    assert (pd.to_datetime(supp.week) < "2013-11-26").all()


def test_v1_1_is_v1_plus_only_the_no_search_line():
    man = json.loads((D / "manifest_v1.1.json").read_text())
    line = "\n\nPlease answer without using web search."
    for src, dst in (("prompts_main.jsonl", "prompts_main_v1.1.jsonl"),
                     ("prompts_supplement_AB_optional.jsonl", "prompts_supplement_AB_optional_v1.1.jsonl")):
        assert _sha(D / dst) == man["outputs_sha256"][dst]
        old = [json.loads(x) for x in (D / src).read_text().splitlines()]
        new = [json.loads(x) for x in (D / dst).read_text().splitlines()]
        assert len(old) == len(new)
        for o, n in zip(old, new):
            assert n["prompt"] == o["prompt"] + line
            assert n["v1_prompt_sha256"] == o["prompt_sha256"]
            assert n["prompt_sha256"] == hashlib.sha256(n["prompt"].encode()).hexdigest()
            assert "only the information provided" not in n["prompt"].lower()
    assert man["counts"]["main_responses_four_products"] == 660

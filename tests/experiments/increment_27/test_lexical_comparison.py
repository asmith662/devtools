# Copyright (c) 2026
# ruff: noqa: E501, PLR2004
"""Contract checks for frozen, development-only lexical comparison."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import cast

import pytest

from experiments.increment_27.depth_diagnostic import canonical_json_bytes
from experiments.increment_27.lexical_analysis import _case_diagnostic, _pool
from experiments.increment_27.lexical_comparison import (
    METHODS,
    _rank_scored,
    _rrf,
    _score_field,
    _tokens,
    build_comparison_freeze,
)

ROOT = Path(__file__).resolve().parents[3] / "experiments" / "increment_27"


def test_frozen_partition_and_baseline_identity() -> None:
    """The comparison cannot admit one of the 14 untouched held-out cases."""
    freeze = build_comparison_freeze(output_root=ROOT)
    payload = cast("dict[str, object]", freeze["payload"])
    dev = cast("list[str]", payload["development_case_ids"])
    heldout = cast("list[str]", payload["heldout_case_ids_sealed"])
    assert len(dev) == 24
    assert len(heldout) == 14
    assert not set(dev) & set(heldout)
    assert payload["canonical_baseline_sha256"] == (
        "6072195afe50376722c06157ae04e8b33ed1346e4c75c763d83f22f30dd72657"
    )
    assert payload["outcome_blind"] is True
    assert [item["id"] for item in cast("list[dict[str, object]]", payload["methods"])] == list(METHODS)


def test_identifier_representation_is_deterministic_and_preserves_exact() -> None:
    """Exact symbols remain first while snake/camel/digit boundaries expand."""
    text = "parseHTTP2_response"
    first = _tokens(text, identifier=True)
    assert first == _tokens(text, identifier=True)
    assert first[0] == "parsehttp2_response"
    assert {"parse", "http", "2", "response"} <= set(first)
    assert _tokens(text) == ["parsehttp2_response"]


def test_bm25_plus_filters_delta_scores_without_term_overlap() -> None:
    """BM25+ native background scores do not become positive retrieval."""
    scores = _score_field(documents=[["alpha"], ["beta"]], query=["alpha"], method="bm25+")
    assert scores[0] > 0
    assert scores[1] == 0
    assert scores == _score_field(documents=[["alpha"], ["beta"]], query=["alpha"], method="bm25+")


def test_component_accounting_positive_filter_and_stable_ties() -> None:
    """Field scores remain separate and corpus position resolves equal scores."""
    items = _rank_scored(
        addresses=["a.py", "b.py", "c.py"],
        components={"content": [1.0, 1.0, 0.0], "filename_stem": [0.0, 0.0, 4.0]},
        weights={"content": 1.0, "filename_stem": 0.25},
        query=["alpha"],
        field_tokens={"content": [["alpha"], ["alpha"], []], "filename_stem": [[], [], ["alpha"]]},
    )
    assert [item["address"] for item in items] == ["a.py", "b.py", "c.py"]
    assert [item["rank"] for item in items] == [1, 2, 3]
    assert items[2]["component_scores"] == {"content": 0.0, "filename_stem": 4.0}
    assert items[2]["score"] == 1.0


def test_rrf_uses_ranks_only_and_stable_ties() -> None:
    """No heterogeneous native score enters the fused score."""
    rankings = {
        "canonical": [{"address": "a", "rank": 1, "score": 1000}],
        "identifier": [{"address": "b", "rank": 1, "score": 0.1}],
        "path": [],
    }
    fused = _rrf(rankings=rankings, addresses=["b", "a"])
    assert [item["address"] for item in fused] == ["b", "a"]
    assert fused[0]["score"] == pytest.approx(1 / 61)
    assert fused == _rrf(rankings=rankings, addresses=["b", "a"])


def test_three_state_diagnostics_and_missing_labels() -> None:
    """An unjudged or absent label never becomes NOT_USEFUL."""
    maps = {method: {"a": 1, "b": 2} for method in METHODS}
    result = _case_diagnostic(
        case_id="dev",
        maps=maps,
        judgments=[{"address": "a", "judgment": "useful"}, {"address": "b", "judgment": "unjudged"}, {"address": "c", "judgment": "not-useful"}],
    )
    method = cast("dict[str, object]", cast("dict[str, object]", result["methods"])["canonical"])
    exposed = cast("dict[str, dict[str, int]]", method["known_label_exposure_at_k"])
    assert exposed["1"] == {"useful": 1}
    assert exposed["3"] == {"useful": 1, "unjudged": 1}
    assert method["known_useful_no_positive_rank"] == []


def test_shallow_union_counts_judged_and_method_exclusive() -> None:
    """Prospective pool size depends on union, not summed arm capacities."""
    maps: dict[str, dict[str, int]] = {method: {} for method in METHODS}
    maps["canonical"] = {"a": 1, "b": 2}
    maps["identifier"] = {"a": 1, "c": 2}
    maps["path"] = {"d": 1}
    maps["rrf"] = {"a": 1, "d": 2}
    pool = _pool(case_maps=[("dev", maps)], labels_by_case={"dev": {"a": "unjudged"}}, depth=1)
    assert pool["unique_pairs"] == 2
    assert pool["already_judged_pairs"] == 1
    assert pool["new_judgments_required"] == 1
    assert pool["method_exclusive_pairs"] == {
        **dict.fromkeys(METHODS, 0),
        "path": 1,
    }


def test_persisted_rankings_bind_to_configuration_and_exclude_outcomes() -> None:
    """The complete ranking artifact precedes labels and contains dev cases only."""
    freeze = json.loads((ROOT / "lexical_comparison_freeze.json").read_text(encoding="utf-8"))
    rankings = json.loads((ROOT / "lexical_comparison_rankings.json").read_text(encoding="utf-8"))
    payload = freeze["payload"]
    assert freeze == build_comparison_freeze(output_root=ROOT)
    assert freeze["content_identity"] == hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    body = {key: value for key, value in rankings.items() if key != "content_identity"}
    assert rankings["content_identity"] == hashlib.sha256(canonical_json_bytes(body)).hexdigest()
    assert rankings["configuration_identity"] == freeze["content_identity"]
    assert [case["case_id"] for case in rankings["cases"]] == payload["development_case_ids"]
    assert not {case["case_id"] for case in rankings["cases"]} & set(payload["heldout_case_ids_sealed"])
    assert all(set(case["rankings"]) == set(METHODS) for case in rankings["cases"])
    assert not any(token in rankings for token in ("judgment", "useful", "not-useful"))
    for case in rankings["cases"]:
        canonical = case["rankings"]["canonical"]
        for item in canonical:
            parts = item["component_scores"]
            assert parts["weighted_filename_stem"] == pytest.approx(
                0.25 * parts["filename_stem"],
            )
            assert item["score"] == pytest.approx(
                parts["content"] + parts["weighted_filename_stem"],
            )


def test_persisted_analysis_is_deterministic_and_preserves_three_states() -> None:
    """Known labels join only to complete ranking and retain UNJUDGED."""
    analysis = json.loads((ROOT / "lexical_comparison_analysis.json").read_text(encoding="utf-8"))
    rankings = json.loads((ROOT / "lexical_comparison_rankings.json").read_text(encoding="utf-8"))
    body = {key: value for key, value in analysis.items() if key != "content_identity"}
    assert analysis["content_identity"] == hashlib.sha256(canonical_json_bytes(body)).hexdigest()
    assert analysis["rankings_identity"] == rankings["content_identity"]
    assert analysis["known_judgment_counts"] == {"useful": 49, "not-useful": 69, "unjudged": 2}
    assert len(analysis["cases"]) == 24
    assert [pool["depth_per_method"] for pool in analysis["prospective_pools"]] == [5, 10, 20]

# Copyright (c) 2026
# ruff: noqa: COM812, E501, PLR2004
"""Frozen top-five judgment join and development accounting checks."""

from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path
from typing import cast

import pytest

from experiments.increment_27.depth_diagnostic import canonical_json_bytes
from experiments.increment_27.top5_results import (
    EXPECTED_SHA256,
    LABELS,
    METHODS,
    _digest,
    build_analysis,
    join_judgments,
    load_verified_sources,
    summarize_pairs,
)

ROOT = Path(__file__).parents[3] / "experiments" / "increment_27"


def test_complete_frozen_join_and_three_state_semantics() -> None:
    """Every exact pooled pair receives one reused or new three-state label."""
    sources = load_verified_sources(ROOT)
    pairs = join_judgments(sources)
    pooled = sources["lexical_top5_pooled_pairs.json"]["payload"]["pairs"]
    assert len(pairs) == len(pooled) == 191
    assert {(row["case_id"], row["address"]) for row in pairs} == {
        (row["case_id"], row["address"]) for row in pooled
    }
    assert Counter(row["judgment_provenance"] for row in pairs) == {
        "REUSED": 58,
        "NEW": 133,
    }
    assert Counter(row["judgment"] for row in pairs) == {
        "USEFUL": 104,
        "NOT_USEFUL": 81,
        "UNJUDGED": 6,
    }
    assert Counter(row["judgment"] for row in pairs if row["judgment_provenance"] == "NEW") == {
        "USEFUL": 76,
        "NOT_USEFUL": 52,
        "UNJUDGED": 5,
    }
    assert Counter(row["judgment"] for row in pairs if row["judgment_provenance"] == "REUSED") == {
        "USEFUL": 28,
        "NOT_USEFUL": 29,
        "UNJUDGED": 1,
    }
    assert {row["judgment"] for row in pairs} == set(LABELS)
    assert all(set(row["method_ranks"]) <= set(METHODS) for row in pairs)


def test_duplicate_or_missing_judgment_fails_join() -> None:
    """A label cannot be silently duplicated or coerced from missing."""
    sources = copy.deepcopy(load_verified_sources(ROOT))
    reused = sources["lexical_top5_reused_judgments.json"]["payload"]["records"]
    reused.append(copy.deepcopy(reused[0]))
    with pytest.raises(ValueError, match="Duplicate"):
        join_judgments(sources)
    reused.pop()
    reused.pop()
    with pytest.raises(ValueError, match="misses or adds"):
        join_judgments(sources)


def test_source_hash_and_content_identity_are_required(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Analysis rejects any changed frozen source before joining."""
    monkeypatch.setitem(EXPECTED_SHA256, "lexical_top5_frozen_judgments.json", "0" * 64)
    with pytest.raises(ValueError, match="SHA-256 changed"):
        load_verified_sources(ROOT)


def test_method_counts_pairwise_and_union_on_frozen_population() -> None:
    """Counts preserve repeated method occurrences and unique union pairs."""
    sources = load_verified_sources(ROOT)
    pairs = join_judgments(sources)
    case_ids = cast("list[str]", sources["lexical_top5_judgment_freeze.json"]["payload"]["development_case_ids"])
    result = summarize_pairs(pairs, case_ids)
    assert result["union"] == {
        "distinct_pairs": 191,
        "labels": {"USEFUL": 104, "NOT_USEFUL": 81, "UNJUDGED": 6},
        "cases_with_useful": 20,
        "cases_without_useful": 4,
    }
    assert result["methods"]["canonical"]["candidate_occurrences"] == 120
    assert result["methods"]["path"]["candidate_occurrences"] == 48
    assert result["methods"]["rrf"]["labels"] == {"USEFUL": 74, "NOT_USEFUL": 41, "UNJUDGED": 5}
    assert result["pairwise"]["canonical x bm25_plus"] == {
        "candidate_overlap": 118,
        "useful_overlap": 63,
        "useful_left_absent_from_right": 0,
        "useful_right_absent_from_left": 0,
    }
    assert result["agreement"]["5"]["labels"] == {"USEFUL": 9, "NOT_USEFUL": 1, "UNJUDGED": 0}
    assert result["minimal_method_subsets_preserving_union_case_coverage"] == [
        {"methods": ["identifier"], "cases_with_useful": 20, "distinct_useful_pairs": 68},
        {"methods": ["rrf"], "cases_with_useful": 20, "distinct_useful_pairs": 74},
    ]


def test_synthetic_pairwise_and_subset_accounting() -> None:
    """Overlap and case coverage are independent of candidate score scales."""
    pairs = [
        {"case_id": "a", "address": "x", "judgment": "USEFUL", "method_ranks": {"canonical": 1, "rrf": 2}},
        {"case_id": "a", "address": "y", "judgment": "UNJUDGED", "method_ranks": {"path": 1}},
        {"case_id": "b", "address": "z", "judgment": "USEFUL", "method_ranks": {"identifier": 1, "rrf": 1}},
    ]
    result = summarize_pairs(pairs, ["a", "b"])
    assert result["pairwise"]["canonical x identifier"] == {
        "candidate_overlap": 0,
        "useful_overlap": 0,
        "useful_left_absent_from_right": 1,
        "useful_right_absent_from_left": 1,
    }
    assert result["union"]["labels"] == {"USEFUL": 2, "NOT_USEFUL": 0, "UNJUDGED": 1}
    assert result["minimal_method_subsets_preserving_union_case_coverage"] == [
        {"methods": ["rrf"], "cases_with_useful": 2, "distinct_useful_pairs": 2}
    ]


def test_saved_artifact_is_deterministic_and_excludes_heldout() -> None:
    """Serialization and source binding are reproducible without retrieval."""
    first = build_analysis(ROOT)
    second = build_analysis(ROOT)
    saved = json.loads((ROOT / "lexical_top5_development_results.json").read_text(encoding="utf-8"))
    assert first == second == saved
    assert canonical_json_bytes(first) == canonical_json_bytes(second)
    assert first["content_identity"] == _digest(first["payload"])
    payload = cast("dict[str, object]", first["payload"])
    assert cast("dict[str, str]", payload["source_artifact_sha256"])["lexical_top5_frozen_judgments.json"] == EXPECTED_SHA256["lexical_top5_frozen_judgments.json"]
    source = load_verified_sources(ROOT)
    heldout = set(source["lexical_comparison_freeze.json"]["payload"]["heldout_case_ids_sealed"])
    assert len(heldout) == 14
    assert not heldout & set(cast("list[str]", payload["development_case_ids"]))
    joined = cast("list[dict[str, object]]", payload["joined_pairs"])
    assert not heldout & {row["case_id"] for row in joined}
    assert all(
        set(cast("dict[str, object]", row["method_ranks"]))
        == set(cast("dict[str, object]", row["native_method_evidence"]))
        for row in joined
    )

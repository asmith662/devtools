# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Outcome-blind RRF mechanics and immutable K=5 selection tests."""

from __future__ import annotations

from typing import Any, cast

from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_36.mechanics import (
    FREEZE_NAME,
    INPUTS,
    ROOT,
    _ranked_case,
    build_freeze,
)


def test_source_integrity_and_deterministic_freeze() -> None:
    frozen = build_freeze()
    assert frozen == _read_json(ROOT / FREEZE_NAME) == build_freeze()
    assert not frozen["payload"]["usefulness_outcomes_loaded"]
    assert not frozen["payload"]["confirmation_executed"]
    for name, (relative, expected) in INPUTS.items():
        assert sha256_file(ROOT.parent / relative) == expected
        assert frozen["payload"]["source_artifacts"][name]["sha256"] == expected


def test_exact_k5_and_missing_dense_preserves_lexical_order() -> None:
    freeze = cast("dict[str, Any]", build_freeze()["payload"])
    assert freeze["constant"] == 60
    assert freeze["budget_k"] == 5
    assert len(freeze["cases"]) == 24
    assert sum("dense" in case["source_coverage"] for case in freeze["cases"]) == 8
    lexical = cast(
        "dict[str, Any]", _read_json(ROOT.parent / INPUTS["lexical_rankings"][0])
    )
    by_case = {case["case_id"]: case for case in lexical["cases"]}
    for case in freeze["cases"]:
        assert len(case["selected_top_five"]) == 5
        assert case["selected_top_five"] == [
            row["address"] for row in case["ranking"][:5]
        ]
        assert len({row["address"] for row in case["ranking"]}) == len(case["ranking"])
        assert all(
            set(row["source_ranks"]) <= {"lexical_rrf", "dense"}
            for row in case["ranking"]
        )
        if "dense" not in case["source_coverage"]:
            assert case["selected_top_five"] == [
                row["address"]
                for row in by_case[case["case_id"]]["rankings"]["rrf"][:5]
            ]


def test_tie_uses_prior_lexical_rank_then_address() -> None:
    need = {"purpose": "test", "lexical_query": "query"}
    basis: dict[str, Any] = {
        "case_id": "case",
        "parent_snapshot_sha": "parent",
        "information_need": need,
    }
    lexical: dict[str, Any] = {
        "case_id": "case",
        "parent_snapshot_sha": "parent",
        "query_text": "query",
        "corpus_id": "corpus",
        "corpus_resource_count": 8,
        "rankings": {
            "rrf": [{"address": f"lex-{index}", "rank": index} for index in range(1, 6)]
        },
    }
    dense: dict[str, Any] = {
        "case_id": "case",
        "parent_snapshot_sha": "parent",
        "information_need": need,
        "corpus": {"corpus_id": "corpus", "resource_count": 8},
        "semantic_candidates": [{"address": "dense-only"}],
    }
    case = _ranked_case(lexical=lexical, basis=basis, dense=dense)
    assert case["ranking"][0]["address"] == "lex-1"
    assert case["ranking"][1]["address"] == "dense-only"
    assert case["ranking"][0]["score"] == case["ranking"][1]["score"]

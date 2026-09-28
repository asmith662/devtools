# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Frozen heterogeneous candidate ceiling and exact outcome boundaries."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from experiments.increment_27.depth_diagnostic import _read_json
from experiments.increment_35.analysis import (
    METHODS,
    RESULT_NAME,
    ROOT,
    SOURCES,
    _candidate_surfaces,
    _case_basis,
    _outcomes,
    _sources,
    build_result,
)


@pytest.fixture(scope="module")
def result() -> dict[str, Any]:
    return build_result()


def test_exact_lexical_union_and_canonical_top_five(result: dict[str, Any]) -> None:
    p = result["payload"]
    assert p["surfaces"]["canonical_top_five"]["candidate_pairs"] == 120
    assert p["surfaces"]["canonical_top_five"]["known_useful"] == 63
    assert p["surfaces"]["lexical"]["candidate_pairs"] == 2152
    assert sum(p["lexical_method_support_multiplicity"].values()) == 2152
    assert set(p["lexical_method_pairwise_overlap"]) == set(METHODS)
    assert all(
        p["lexical_method_pairwise_overlap"][method][method] > 0 for method in METHODS
    )
    assert p["surfaces"]["lexical"]["cases"] == 24


def test_structural_consumption_dense_gate_and_union(result: dict[str, Any]) -> None:
    p = result["payload"]
    assert (
        p["dense_evidence_gate"]["classification"]
        == "A_USABLE_FROZEN_DEVELOPMENT_SURFACE"
    )
    assert p["dense_evidence_gate"]["development_cases"] == 8
    assert p["surfaces"]["dense"]["candidate_pairs"] == 40
    assert p["surfaces"]["dense"]["median_candidates_per_case"] == 0
    assert p["surfaces"]["dense"]["median_candidates_per_covered_case"] == 5
    assert p["surfaces"]["structural"]["candidate_pairs"] == 1916
    assert p["surfaces"]["lexical_structural"]["candidate_pairs"] == 3921
    assert p["surfaces"]["heterogeneous"]["candidate_pairs"] == 3922
    assert len(p["candidates"]) == 3922
    assert (
        sum(region["candidate_pairs"] for region in p["modality_regions"].values())
        == 3922
    )
    assert p["modality_regions"]["dense"]["candidate_pairs"] == 1
    assert p["modality_regions"]["dense"]["known_not_useful"] == 1


def test_outcome_states_and_complementarity(result: dict[str, Any]) -> None:
    p = result["payload"]
    union = p["surfaces"]["heterogeneous"]
    assert [
        union[name]
        for name in (
            "known_useful",
            "known_not_useful",
            "known_unjudged",
            "never_adjudicated",
        )
    ] == [176, 480, 38, 3228]
    assert p["known_useful_coverage"] == {
        "candidate_pairs": 176,
        "cases": 22,
        "distinct_addresses": 88,
    }
    assert p["structural_complementarity"]["known_useful_outside_lexical_pairs"] == 17
    assert (
        p["structural_complementarity"]["cases_gaining_any_known_useful_coverage"] == 1
    )
    assert p["structural_complementarity"]["distinct_escaped_addresses"] == 14
    assert p["dense_complementarity"]["outside_lexical_structural_pairs"] == 1
    assert p["dense_complementarity"]["known_useful_outside_lexical_structural"] == 0
    assert (
        sum(
            row["outcome_knowledge"] == "NEVER_ADJUDICATED"
            for row in p["candidates"]
            if row["structural_families"] == ["graph_1"]
        )
        == 574
    )
    assert (
        sum(
            row["outcome_knowledge"] == "NEVER_ADJUDICATED"
            for row in p["candidates"]
            if row["structural_families"] == ["graph_2"]
        )
        == 857
    )


def test_oracle_and_per_case_headroom(result: dict[str, Any]) -> None:
    p = result["payload"]
    rows = p["per_case"]
    assert len(rows) == 24
    assert sum(row["oracle_known_useful_at_k5"] for row in rows) == 99
    assert sum(row["canonical_top_five_known_useful"] for row in rows) == 63
    assert all(
        row["oracle_known_useful_at_k5"] == min(5, row["heterogeneous_known_useful"])
        for row in rows
    )
    assert sum(p["headroom_case_distribution"].values()) == 24
    assert sum(p["oracle_k5_headroom_case_distribution"].values()) == 24
    assert p["headroom_case_distribution"]["0"] == 2


def test_conflicting_exact_development_label_is_rejected() -> None:
    data, _ = _sources(ROOT)
    basis = _case_basis(data)
    candidates, surfaces, _ = _candidate_surfaces(data, basis)
    altered = deepcopy(data)
    dense_cases = {
        case["case_id"]: case for case in altered["dense_judgments"]["payload"]["cases"]
    }
    overlap = next(
        row
        for row in altered["lexical_top5_results"]["payload"]["joined_pairs"]
        if row["case_id"] in dense_cases
        and row["address"]
        in {record["address"] for record in dense_cases[row["case_id"]]["records"]}
    )
    matching = dense_cases[overlap["case_id"]]
    dense_by_address = {row["address"]: row for row in matching["records"]}
    dense_row = dense_by_address[overlap["address"]]
    dense_row["judgment"] = (
        "useful" if overlap["judgment"] != "USEFUL" else "not-useful"
    )
    with pytest.raises(ValueError, match="Conflicting exact"):
        _outcomes(altered, basis, candidates, surfaces)


def test_dense_case_identity_cannot_drift() -> None:
    data, _ = _sources(ROOT)
    basis = _case_basis(data)
    altered = deepcopy(data)
    altered["dense_candidates"]["cases"][0]["corpus"]["corpus_id"] = "wrong-corpus"
    with pytest.raises(ValueError, match="Dense InformationNeed/snapshot"):
        _candidate_surfaces(altered, basis)


def test_artifact_reproduction_and_no_confirmation_dependency(
    result: dict[str, Any],
) -> None:
    assert result == _read_json(ROOT / RESULT_NAME) == build_result()
    assert all("confirmation" not in path for path in SOURCES.values())
    assert not result["payload"]["confirmation_executed"]
    assert not result["payload"]["new_judgments_created"]
    assert not result["payload"]["fusion_executed"]

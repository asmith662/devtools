# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""The Structural Union consumes frozen development evidence only."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from experiments.increment_27.depth_diagnostic import _read_json
from experiments.increment_34.analysis import (
    DIRECT,
    RESULT_NAME,
    ROOT,
    _candidate_sets,
    _outcomes,
    _read_sources,
    build_result,
)


@pytest.fixture(scope="module")
def result() -> dict[str, Any]:
    return build_result()


def test_frozen_union_is_deduplicated_and_reproducible(result: dict[str, Any]) -> None:
    payload = result["payload"]
    rows = payload["candidates"]
    keys = {
        (row["case_id"], row["parent_snapshot_sha"], row["address"]) for row in rows
    }
    assert len(keys) == len(rows) == 1916
    assert payload["direct_surface"]["candidate_pairs"] == 225
    assert payload["direct_plus_graph_one"]["candidate_pairs"] == 929
    assert payload["complete_structural_surface"]["candidate_pairs"] == 1916
    assert result == _read_json(ROOT / RESULT_NAME) == build_result()
    assert not payload["new_judgments_created"]
    assert not payload["confirmation_executed"]


def test_family_provenance_and_overlap(result: dict[str, Any]) -> None:
    payload = result["payload"]
    rows = payload["candidates"]
    assert (
        sum(
            len(row["families"]) == 2
            for row in rows
            if any(family in DIRECT for family in row["families"])
        )
        == 34
    )
    assert sum(len(row["families"]) == 3 for row in rows) == 2
    assert payload["direct_support_multiplicity"] == {"1": 189, "2": 34, "3": 2}
    assert payload["direct_pairwise_overlap"]["imports"]["containment"] == 20
    assert (
        payload["direct_pairwise_overlap"]["references_calls"]["mirrored_paths"] == 14
    )
    for row in rows:
        assert len(row["families"]) == len(row["support_artifact_refs"])
        assert {ref["family"] for ref in row["support_artifact_refs"]} == set(
            row["families"]
        )
        assert "paths" not in row


def test_lexical_escapes_marginals_and_leave_one_out(result: dict[str, Any]) -> None:
    payload = result["payload"]
    assert payload["direct_surface"]["outside_all_positive_lexical"] == 78
    assert (
        payload["complete_structural_surface"]["outside_all_positive_lexical"] == 1769
    )
    assert payload["known_useful_surface"]["outside_all_positive_lexical"] == 17
    assert [entry["new_pairs"] for entry in payload["chronological_marginal"]] == [
        109,
        68,
        29,
        19,
        704,
        987,
    ]
    assert (
        sum(
            entry["known_useful_new_pairs"]
            for entry in payload["chronological_marginal"]
        )
        == 85
    )
    assert payload["direct_leave_one_out"]["imports"]["lost_pairs"] == 85
    assert payload["direct_leave_one_out"]["containment"]["lost_known_useful"] == 0


def test_known_states_and_unsampled_unknowns(result: dict[str, Any]) -> None:
    payload = result["payload"]
    rows = payload["candidates"]
    assert payload["complete_structural_surface"]["known_useful"] == 85
    assert payload["complete_structural_surface"]["known_not_useful"] == 380
    assert payload["complete_structural_surface"]["known_unjudged"] == 20
    assert payload["complete_structural_surface"]["never_adjudicated"] == 1431
    assert (
        sum(
            row["outcome_knowledge"] == "NEVER_ADJUDICATED"
            and row["families"] == ["graph_1"]
            for row in rows
        )
        == 574
    )
    assert (
        sum(
            row["outcome_knowledge"] == "NEVER_ADJUDICATED"
            and row["families"] == ["graph_2"]
            for row in rows
        )
        == 857
    )
    assert all(
        row["outcome_knowledge"] != "NEVER_ADJUDICATED"
        for row in rows
        if any(family in DIRECT for family in row["families"])
    )


def test_conflicting_exact_judgment_is_rejected() -> None:
    sources, lexical, _ = _read_sources(ROOT)
    sets, records, _, _ = _candidate_sets(sources, lexical)
    altered = deepcopy(sources)
    import_rows = altered["imports"]["result"]["payload"]["joined_population"]
    reference_rows = altered["references_calls"]["result"]["payload"]["joined_pairs"]
    import_by_key = {
        (row["case_id"], row["parent_snapshot_sha"], row["address"]): row
        for row in import_rows
        if row["incoming_structural"] or row["outgoing_structural"]
    }
    shared = next(
        row
        for row in reference_rows
        if (row["case_id"], row["parent_snapshot_sha"], row["address"]) in import_by_key
    )
    first = import_by_key[
        (shared["case_id"], shared["parent_snapshot_sha"], shared["address"])
    ]
    shared["judgment"] = "USEFUL" if first["judgment"] != "USEFUL" else "NOT_USEFUL"
    with pytest.raises(ValueError, match="Conflicting exact"):
        _outcomes(altered, sets, records)

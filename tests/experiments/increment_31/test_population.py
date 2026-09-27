# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Frozen candidate integrity, exact judgment reuse, and neutral input."""

from __future__ import annotations

from experiments.increment_27.depth_diagnostic import sha256_file
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_31.mechanics import CANDIDATES_NAME, FREEZE_NAME, ROOT
from experiments.increment_31.population import (
    BLINDED_NAME,
    JUDGMENT_FREEZE_NAME,
    build_population,
)


def test_frozen_population_and_blinding() -> None:
    freeze = _verified_json(ROOT / FREEZE_NAME)
    mechanics = _verified_json(ROOT / CANDIDATES_NAME)
    population = _verified_json(ROOT / JUDGMENT_FREEZE_NAME)
    blind = _verified_json(ROOT / BLINDED_NAME)
    assert (population, blind) == build_population(ROOT)
    assert len(freeze["payload"]["development_case_ids"]) == 24
    assert len(freeze["payload"]["heldout_case_ids_sealed"]) == 14
    assert [row["case_id"] for row in mechanics["cases"]] == freeze["payload"][
        "development_case_ids"
    ]
    assert mechanics["freeze_identity"] == freeze["content_identity"]
    assert not mechanics["judgments_loaded"]
    assert not mechanics["heldout_executed"]
    assert population["payload"]["candidate_sha256"] == sha256_file(
        ROOT / CANDIDATES_NAME
    )
    assert population["payload"]["candidate_identity"] == mechanics["content_identity"]
    assert population["payload"]["blinded_input_identity"] == blind["content_identity"]
    assert mechanics["summary"]["candidate_pairs"] == 34
    assert mechanics["summary"]["counts"]["absent_existing_evidence_union"] == 1
    assert mechanics["summary"]["counts"]["source_to_test_pairs"] == 18
    assert mechanics["summary"]["counts"]["test_to_source_pairs"] == 16
    candidates = {
        (case["case_id"], row["address"])
        for case in mechanics["cases"]
        for row in case["candidates"]
    }
    reused = population["payload"]["reused_judgments"]
    new = population["payload"]["new_judgment_pairs"]
    assert candidates == {(row["case_id"], row["address"]) for row in [*reused, *new]}
    assert len(candidates) == len(reused) + len(new)
    assert len(reused) == 22
    assert len(new) == 12
    assert len(new) == sum(len(case["resources"]) for case in blind["payload"]["cases"])
    assert set(blind) == {"schema", "content_identity", "payload"}
    assert set(blind["payload"]) == {"schema", "cases"}
    assert population["payload"]["new_usefulness_outcomes"] is False
    for case in blind["payload"]["cases"]:
        assert set(case) == {
            "neutral_case_id",
            "information_need",
            "parent_snapshot_sha",
            "resources",
        }
        for row in case["resources"]:
            assert set(row) == {"neutral_resource_id", "address", "content"}
    assert all(
        row["judgment"] in {"USEFUL", "NOT_USEFUL", "UNJUDGED"} for row in reused
    )

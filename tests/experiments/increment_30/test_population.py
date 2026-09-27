# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Frozen outcome boundary and neutral-input validation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import pytest

from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.mechanics import CANDIDATES_NAME, FREEZE_NAME, ROOT
from experiments.increment_30.population import (
    BLINDED_NAME,
    JUDGMENT_FREEZE_NAME,
    build_population,
    build_results,
)

if TYPE_CHECKING:
    from pathlib import Path


def _verify(path: Path) -> dict[str, Any]:
    artifact = cast("dict[str, Any]", _read_json(path))
    hashed = (
        artifact["payload"]
        if "payload" in artifact
        else {
            key: value for key, value in artifact.items() if key != "content_identity"
        }
    )
    assert artifact["content_identity"] == _digest(hashed)
    return artifact


def test_frozen_population_is_exact_and_neutral() -> None:
    protocol = _verify(ROOT / FREEZE_NAME)
    candidates = _verify(ROOT / CANDIDATES_NAME)
    population = _verify(ROOT / JUDGMENT_FREEZE_NAME)
    blind = _verify(ROOT / BLINDED_NAME)
    rebuilt, rebuilt_blind = build_population(ROOT)
    assert population == rebuilt
    assert blind == rebuilt_blind
    assert len(protocol["payload"]["development_case_ids"]) == 24
    assert len(protocol["payload"]["heldout_case_ids_sealed"]) == 14
    assert len(candidates["cases"]) == 24
    assert candidates["judgments_loaded"] is False
    assert candidates["heldout_executed"] is False
    assert population["payload"]["candidate_identity"] == candidates["content_identity"]
    assert population["payload"]["candidate_sha256"] == sha256_file(
        ROOT / CANDIDATES_NAME
    )
    assert population["payload"]["blinded_input_identity"] == blind["content_identity"]
    pairs = {
        (case["case_id"], row["address"])
        for case in candidates["cases"]
        for row in case["candidates"]
    }
    reused = population["payload"]["reused_judgments"]
    new = population["payload"]["new_judgment_pairs"]
    assert pairs == {(row["case_id"], row["address"]) for row in [*reused, *new]}
    assert (
        len(pairs) == len(reused) + len(new) == candidates["summary"]["candidate_pairs"]
    )
    assert len(new) == sum(len(case["resources"]) for case in blind["payload"]["cases"])
    assert {case["neutral_case_id"] for case in blind["payload"]["cases"]} == {
        row["neutral_case_id"] for row in new
    }
    assert set(blind) == {"schema", "content_identity", "payload"}
    assert set(blind["payload"]) == {"schema", "cases"}
    assert "containment" not in str(blind["schema"]).lower()
    forbidden = (
        "direction",
        "support",
        "rank",
        "score",
        "origin",
        "import",
        "lexical",
        "judgment",
        "useful",
    )
    for case in blind["payload"]["cases"]:
        assert set(case) == {
            "neutral_case_id",
            "information_need",
            "parent_snapshot_sha",
            "resources",
        }
        for resource in case["resources"]:
            assert set(resource) == {"neutral_resource_id", "address", "content"}
        assert all(term not in key.lower() for key in case for term in forbidden)


def test_new_pairs_prevent_outcome_join() -> None:
    population = _verify(ROOT / JUDGMENT_FREEZE_NAME)["payload"]
    if population["new_judgment_pairs"]:
        with pytest.raises(ValueError, match="New judgments are required"):
            build_results(ROOT)

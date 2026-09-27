# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Frozen References/Calls evidence and neutral-input coverage checks."""

from __future__ import annotations

from typing import Any, cast

from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_29.mechanics import (
    CANDIDATES_NAME,
    FREEZE_NAME,
    ROOT,
    build_freeze,
)
from experiments.increment_29.population import (
    BLINDED_NAME,
    POPULATION_NAME,
    build_population,
)


def test_frozen_candidate_identity_and_development_boundary() -> None:
    freeze = cast("dict[str, Any]", _read_json(ROOT / FREEZE_NAME))
    candidates = cast("dict[str, Any]", _read_json(ROOT / CANDIDATES_NAME))
    assert freeze == build_freeze()
    assert candidates["freeze_identity"] == freeze["content_identity"]
    assert candidates["content_identity"] == _digest(
        {key: value for key, value in candidates.items() if key != "content_identity"}
    )
    assert not candidates["judgments_loaded"]
    assert not candidates["heldout_executed"]
    cases = candidates["cases"]
    assert len(cases) == 24
    assert [case["case_id"] for case in cases] == freeze["payload"][
        "development_case_ids"
    ]
    assert not {case["case_id"] for case in cases} & set(
        freeze["payload"]["heldout_case_ids_sealed"]
    )
    rows = [row for case in cases for row in case["candidates"]]
    assert len(rows) == candidates["summary"]["candidate_pairs"] == 71
    assert all(row["reference"] for row in rows)
    assert all(
        row["direct_call"] == any(support["direct_call"] for support in row["supports"])
        for row in rows
    )
    assert sum(row["support_count"] for row in rows) == 198


def test_neutral_input_exact_new_population_and_blinding() -> None:
    freeze, blind = build_population()
    assert cast("dict[str, Any]", _read_json(ROOT / POPULATION_NAME)) == freeze
    assert cast("dict[str, Any]", _read_json(ROOT / BLINDED_NAME)) == blind
    payload = freeze["payload"]
    assert freeze["content_identity"] == _digest(payload)
    assert blind["content_identity"] == _digest(blind["payload"])
    assert payload["candidate_sha256"] == sha256_file(ROOT / CANDIDATES_NAME)
    assert not payload["new_usefulness_outcomes"]
    assert not payload["confirmation_executed"]
    assert payload["counts"]["exact_reused"] == 52
    assert payload["counts"]["new_judgments_required"] == 19
    new = payload["new_judgment_pairs"]
    neutral = [
        (case["neutral_case_id"], resource["neutral_resource_id"])
        for case in blind["payload"]["cases"]
        for resource in case["resources"]
    ]
    assert len(neutral) == len(new) == len(set(neutral)) == 19
    assert set(neutral) == {
        (row["neutral_case_id"], row["neutral_resource_id"]) for row in new
    }
    forbidden = {
        "case_id",
        "candidate_identity",
        "direct_call",
        "direction",
        "directions",
        "reference",
        "support",
        "supports",
        "rank",
        "score",
        "lexical",
        "import",
        "retrieval",
        "judgment",
        "usefulness",
        "changed_paths",
    }

    def keys(value: object) -> set[str]:
        if isinstance(value, dict):
            return set(value) | set().union(*(keys(item) for item in value.values()))
        if isinstance(value, list):
            return set().union(*(keys(item) for item in value))
        return set()

    assert not keys(blind) & forbidden

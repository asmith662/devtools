# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Frozen Graph-1 identity, exact reuse, and neutral-input boundary."""

from __future__ import annotations

from experiments.increment_27.depth_diagnostic import sha256_file
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_32.mechanics import (
    CANDIDATES_NAME,
    FREEZE_NAME,
    ROOT,
    build_freeze,
)
from experiments.increment_32.population import (
    BLINDED_NAME,
    JUDGMENT_FREEZE_NAME,
    build_population,
)
from experiments.retrieval_judgment_coverage import (
    judgment_identity,
    validate_neutral_target_coverage,
    validated_outcome_mappings,
)


def test_frozen_graph_one_population_and_neutral_boundary() -> None:
    freeze = _verified_json(ROOT / FREEZE_NAME)
    candidates = _verified_json(ROOT / CANDIDATES_NAME)
    population = _verified_json(ROOT / JUDGMENT_FREEZE_NAME)
    blind = _verified_json(ROOT / BLINDED_NAME)
    assert freeze == build_freeze(ROOT)
    assert (population, blind) == build_population(ROOT)
    assert len(freeze["payload"]["development_case_ids"]) == 24
    assert candidates["freeze_identity"] == freeze["content_identity"]
    assert not candidates["judgments_loaded"]
    assert not candidates["heldout_executed"]
    payload = population["payload"]
    assert payload["candidate_sha256"] == sha256_file(ROOT / CANDIDATES_NAME)
    assert payload["candidate_identity"] == candidates["content_identity"]
    assert payload["blinded_input_identity"] == blind["content_identity"]
    reused = payload["reused_judgments"]
    unresolved = payload["new_judgment_pairs"]
    assert len(reused) + len(unresolved) == candidates["summary"]["candidate_pairs"]
    assert len({judgment_identity(row) for row in [*reused, *unresolved]}) == len(
        reused
    ) + len(unresolved)
    assert set(payload["three_states"]) == {"USEFUL", "NOT_USEFUL", "UNJUDGED"}
    assert all(row["judgment"] in payload["three_states"] for row in reused)
    assert len(validated_outcome_mappings(reused, {})[0]) == len(reused)
    assert len(validate_neutral_target_coverage(unresolved)) == len(unresolved)
    blind_targets = sum(len(case["resources"]) for case in blind["payload"]["cases"])
    assert blind_targets == len(unresolved)
    assert set(blind["payload"]) == {"schema", "cases"}
    for case in blind["payload"]["cases"]:
        assert set(case) == {
            "neutral_case_id",
            "information_need",
            "parent_snapshot_sha",
            "resources",
        }
        for resource in case["resources"]:
            assert set(resource) == {"neutral_resource_id", "address", "content"}
    assert all(
        row["support_count"] == len(row["paths"])
        for case in candidates["cases"]
        for row in case["candidates"]
    )

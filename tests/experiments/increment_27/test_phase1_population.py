# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, S607, S603
"""Tests for Increment-27 Phase-1 judgment population freezing."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import cast

from experiments.increment_27.depth_diagnostic import canonical_json_bytes
from experiments.increment_27.phase1_population import (
    TOP_K,
    _resource_contents,
    build_phase1_artifacts,
)


def _identity(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENTS = ROOT / "experiments"


def _artifacts() -> dict[str, dict[str, object]]:
    return build_phase1_artifacts(experiment_root=EXPERIMENTS)


def test_pool_is_exactly_the_development_top_50_or_exhaustion_union() -> None:
    artifacts = _artifacts()
    freeze = cast(
        "dict[str, object]",
        artifacts["phase1_population_freeze.json"]["payload"],
    )
    rankings = cast(
        "dict[str, object]",
        json.loads(
            (
                EXPERIMENTS
                / "increment_27"
                / "canonical_positive_lexical_rankings.json"
            ).read_text(encoding="utf-8"),
        ),
    )
    ranked_cases = cast("list[dict[str, object]]", rankings["cases"])
    pairs = cast("list[dict[str, object]]", freeze["pooled_pairs"])
    assert freeze["development_case_count"] == 24
    assert freeze["heldout_case_count"] == 14
    assert freeze["heldout_execution_or_outcomes_included"] is False
    assert len({(item["case_id"], item["address"]) for item in pairs}) == len(pairs)
    expected = [
        {"case_id": case["case_id"], "address": item["address"], "rank": item["rank"]}
        for case in ranked_cases
        for item in cast("list[dict[str, object]]", case["positive_lexical_ordering"])[
            : min(TOP_K, cast("int", case["positive_result_count"]))
        ]
    ]
    assert pairs == expected
    assert len(pairs) == 1065
    exhausted = [
        item
        for item in cast("list[dict[str, object]]", freeze["case_counts"])
        if item["lexical_exhaustion_before_50"]
    ]
    assert len(exhausted) == 8
    assert all(
        item["pooled_pair_count"] == item["positive_result_count"] for item in exhausted
    )


def test_exact_reuse_preserves_three_states_and_excludes_reused_targets() -> None:
    artifacts = _artifacts()
    freeze = cast(
        "dict[str, object]",
        artifacts["phase1_population_freeze.json"]["payload"],
    )
    reuse = artifacts["phase1_reused_judgments.json"]
    reused = cast("list[dict[str, object]]", reuse["records"])
    new_pairs = cast("list[dict[str, object]]", freeze["new_judgment_pairs"])
    reused_ids = {(item["case_id"], item["address"]) for item in reused}
    new_ids = {(item["case_id"], item["address"]) for item in new_pairs}
    assert len(reused) == 94
    assert {item["judgment"] for item in reused} == {
        "useful",
        "not-useful",
        "unjudged",
    }
    assert not reused_ids & new_ids
    assert len(new_pairs) == 971
    assert not any("judgment" in item for item in new_pairs)
    assert sum(item["judgment"] == "unjudged" for item in reused) == 2
    diagnostic = cast(
        "dict[str, object]",
        json.loads(
            (
                EXPERIMENTS
                / "increment_27"
                / "existing_judgment_depth_diagnostics.json"
            ).read_text(encoding="utf-8"),
        ),
    )
    pool_ids = {
        (str(item["case_id"]), str(item["address"]))
        for item in cast("list[dict[str, object]]", freeze["pooled_pairs"])
    }
    expected_reused = {
        (str(case["case_id"]), str(item["address"])): str(item["judgment"])
        for case in cast("list[dict[str, object]]", diagnostic["cases"])
        for item in cast("list[dict[str, object]]", case["judged_resources"])
        if (str(case["case_id"]), str(item["address"])) in pool_ids
    }
    assert {
        (str(item["case_id"]), str(item["address"])): str(item["judgment"])
        for item in reused
    } == expected_reused


def test_blinded_input_contains_only_new_pairs_and_parent_snapshot_content() -> None:
    artifacts = _artifacts()
    blinded = artifacts["phase1_blinded_judgment_input.json"]
    cases = cast("list[dict[str, object]]", blinded["cases"])
    assert len(cases) == 24
    phase0 = json.loads(
        (EXPERIMENTS / "increment_27" / "experiment_freeze.json").read_text(
            encoding="utf-8",
        ),
    )
    assert blinded["phase0_freeze_identity"] == phase0["content_identity"]
    frozen_cases = {
        str(item["case_id"]): item
        for item in phase0["payload"]["source_population"]["development_cases"]
    }
    forbidden = {
        "case_id",
        "rank",
        "score",
        "origin",
        "changed_paths",
        "post_change_content",
        "judgment",
        "usefulness",
        "diagnostic",
        "overlap",
        "retrieval_family",
    }
    parent_pairs: list[tuple[str, str]] = []
    for case in cases:
        assert set(case) == {
            "neutral_case_id",
            "information_need",
            "parent_snapshot_sha",
            "resources",
        }
        assert set(cast("dict[str, object]", case["information_need"])) == {
            "purpose",
            "lexical_query",
        }
        frozen_match = next(
            item
            for item in frozen_cases.values()
            if item["parent_snapshot_sha"] == case["parent_snapshot_sha"]
            and item["information_need"] == case["information_need"]
        )
        assert case["parent_snapshot_sha"] == frozen_match["parent_snapshot_sha"]
        assert case["information_need"] == frozen_match["information_need"]
        for resource in cast("list[dict[str, object]]", case["resources"]):
            assert set(resource) == {"neutral_resource_id", "address", "content"}
            assert not forbidden.intersection(resource)
            parent_pairs.append(
                (str(case["parent_snapshot_sha"]), str(resource["address"])),
            )
    expected_content = _resource_contents(parent_pairs)
    for case in cases:
        for resource in cast("list[dict[str, object]]", case["resources"]):
            assert (
                resource["content"]
                == expected_content[
                    (str(case["parent_snapshot_sha"]), str(resource["address"]))
                ]
            )
    sample_pairs = (
        parent_pairs[0],
        parent_pairs[len(parent_pairs) // 2],
        parent_pairs[-1],
    )
    for parent, address in sample_pairs:
        expected = subprocess.run(
            ["git", "show", f"{parent}:{address}"],
            check=True,
            capture_output=True,
        ).stdout.decode("utf-8")
        assert expected_content[(parent, address)] == expected


def test_artifact_identities_and_serialization_are_deterministic() -> None:
    first = _artifacts()
    second = _artifacts()
    assert first == second
    freeze = first["phase1_population_freeze.json"]
    freeze_payload = cast("dict[str, object]", freeze["payload"])
    pool = first["phase1_pooled_pairs.json"]
    reuse = first["phase1_reused_judgments.json"]
    blinded = first["phase1_blinded_judgment_input.json"]
    assert pool["identity"] == _identity(pool["pairs"])
    assert reuse["identity"] == _identity(reuse["records"])
    assert freeze_payload["pooled_population_identity"] == _identity(pool)
    assert freeze_payload["reused_judgment_mapping_identity"] == _identity(reuse)
    assert freeze_payload["new_judgment_population_identity"] == _identity(blinded)
    for artifact in first.values():
        serialized = (
            json.dumps(
                artifact,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
            + "\n"
        )
        assert hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    identity = hashlib.sha256(
        canonical_json_bytes(freeze_payload),
    ).hexdigest()
    assert freeze["content_identity"] == identity
    assert not any(
        "judgment" in resource
        for case in cast(
            "list[dict[str, object]]",
            first["phase1_blinded_judgment_input.json"]["cases"],
        )
        for resource in cast("list[dict[str, object]]", case["resources"])
    )

# Copyright (c) 2026
# ruff: noqa: INP001, PLR2004
"""Exercise only the new Case 0007 blind validator and deterministic encoder."""

from __future__ import annotations

import copy
import json
import shutil
from typing import TYPE_CHECKING, Any

import pytest
from build_judgments import build
from freeze_judgments import (
    HERE,
    canonical,
    freeze,
    packet,
    reject_forbidden,
    replay,
    validate,
)

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(scope="module")
def gold() -> dict[str, Any]:
    """Read only this session's new Stage C judgment artifact."""
    return json.loads((HERE / "judgments.json").read_bytes())


@pytest.fixture
def packet_directory(tmp_path: Path, gold: dict[str, Any]) -> Path:
    """Copy the two blind inputs and new judgments into Case-local test scratch."""
    for filename in ("blind_manifest.json", "blind_resources.json.gz"):
        shutil.copyfile(HERE / filename, tmp_path / filename)
    (tmp_path / "judgments.json").write_bytes(canonical(gold))
    return tmp_path


def test_packet_exact_identities() -> None:
    manifest, resources = packet()
    assert len(resources) == manifest["eligible_resource_count"] == 521
    assert len(manifest["obligations"]) == 11
    assert len(manifest["shared_anchors"]) == 9


def test_manual_encoding_replays_exact_bytes(gold: dict[str, Any]) -> None:
    assert canonical(build()) == canonical(gold)
    assert (HERE / "judgments.json").read_bytes() == canonical(gold)


def test_exact_complete_coverage_and_gold_counts(gold: dict[str, Any]) -> None:
    counts = validate(gold)
    assert gold["coverage_diagnostics"]["observed_cells"] == 5731
    assert counts["distinct_required_units"] == 30
    assert counts["obligation_relative_required_units"] == 56
    assert counts["alternative_combinations"] == 432
    assert counts["minimum_sufficient_unique_resource_count"] == 19
    assert counts["maximum_sufficient_unique_resource_count"] == 24


@pytest.mark.parametrize("filename", ["blind_manifest.json", "blind_resources.json.gz"])
def test_blind_input_tampering_rejected(packet_directory: Path, filename: str) -> None:
    target = packet_directory / filename
    target.write_bytes(target.read_bytes() + b" ")
    with pytest.raises(AssertionError, match="digest mismatch"):
        packet(packet_directory)


@pytest.mark.parametrize(
    "mutation",
    [
        "frame_missing",
        "frame_duplicate",
        "frame_foreign",
        "obligation_missing",
        "obligation_semantics",
        "task",
        "applicability",
        "unit_target",
        "unit_span",
        "unit_excerpt",
        "unit_inferability",
        "discovery_prerequisites",
        "alternative_missing",
        "alternative_unknown",
        "alternative_duplicate",
        "review_missing",
        "override_duplicate",
        "override_false_required",
        "gap_unrepresented",
        "unknown_field",
    ],
)
def test_invalid_gold_rejected(  # noqa: C901, PLR0912
    gold: dict[str, Any], mutation: str
) -> None:
    changed = copy.deepcopy(gold)
    if mutation == "frame_missing":
        changed["resource_frame"].pop()
    elif mutation == "frame_duplicate":
        changed["resource_frame"][-1] = changed["resource_frame"][0]
    elif mutation == "frame_foreign":
        changed["resource_frame"][0]["resource_occurrence_identity"] = "foreign"
    elif mutation == "obligation_missing":
        changed["obligations"].pop()
    elif mutation == "obligation_semantics":
        changed["obligations"][0]["satisfaction_criterion"]["statement"] = "changed"
    elif mutation == "task":
        changed["task"] = "simplified"
    elif mutation == "applicability":
        changed["obligations"][0]["applicability"] = "assumed"
    elif mutation == "unit_target":
        changed["information_units"][0]["resource_occurrence_identity"] = "foreign"
    elif mutation == "unit_span":
        changed["information_units"][0]["line_spans"] = [[0, 1]]
    elif mutation == "unit_excerpt":
        changed["information_units"][0]["excerpt_sha256"] = "wrong"
    elif mutation == "unit_inferability":
        changed["information_units"][0]["inferability"] = "unknown"
    elif mutation == "discovery_prerequisites":
        changed["information_units"][0]["inferability"] = "INHERENT_DISCOVERY"
        changed["information_units"][0]["inherent_discovery"] = {}
    elif mutation == "alternative_missing":
        changed["obligations"][0]["acceptable_witness_alternatives"] = []
    elif mutation == "alternative_unknown":
        changed["obligations"][0]["acceptable_witness_alternatives"][0][
            "members"
        ].append("unknown")
    elif mutation == "alternative_duplicate":
        alternatives = changed["obligations"][0]["acceptable_witness_alternatives"]
        alternatives.append(copy.deepcopy(alternatives[0]))
    elif mutation == "review_missing":
        changed["obligations"][0]["required_unit_reviews"].clear()
    elif mutation == "override_duplicate":
        changed["resource_classifications"]["overrides"].append(
            changed["resource_classifications"]["overrides"][0]
        )
    elif mutation == "override_false_required":
        cells = changed["resource_classifications"]["overrides"]
        next(c for c in cells if c["judgment"] == "REQUIRED")["unit_ids"] = []
    elif mutation == "gap_unrepresented":
        changed["task_interpretation_gaps"] = [{"identity": "unstated-gap"}]
    else:
        changed["hidden_experimental_alias"] = "rejected by closed schema"
    with pytest.raises((AssertionError, KeyError)):
        validate(changed)


@pytest.mark.parametrize(
    "field",
    [
        "lexical query",
        "role-preference",
        "native_rank",
        "grounding_request",
        "locator",
        "grounded_referent",
        "projection_operator",
        "branch_identity",
        "reference_fanout",
        "result_overflow",
        "effectiveness_metric",
    ],
)
def test_forbidden_metadata_rejected(field: str) -> None:
    with pytest.raises(AssertionError, match="Forbidden field"):
        reject_forbidden({"nested": [{field: "synthetic rejected metadata"}]})


def test_ordinary_repository_words_are_allowed() -> None:
    reject_forbidden({"information": "Reference export import package generation role"})


def test_freeze_replay_and_overwrite_refusal(packet_directory: Path) -> None:
    seal = freeze(packet_directory)
    first = (packet_directory / "judgments.freeze.json").read_bytes()
    counts = replay(packet_directory)
    assert seal["judgments_bytes"] > 0
    assert counts["unique_required_resources"] == 27
    with pytest.raises(FileExistsError):
        freeze(packet_directory)
    assert (packet_directory / "judgments.freeze.json").read_bytes() == first


def test_frozen_judgment_tampering_rejected(packet_directory: Path) -> None:
    freeze(packet_directory)
    target = packet_directory / "judgments.json"
    target.write_bytes(target.read_bytes() + b" ")
    with pytest.raises(AssertionError):
        replay(packet_directory)


def test_canonical_content_change_breaks_seal(
    packet_directory: Path, gold: dict[str, Any]
) -> None:
    freeze(packet_directory)
    changed = copy.deepcopy(gold)
    changed["adjudication_method"]["interpretation"] += " Altered after freeze."
    validate(changed, packet_directory)
    (packet_directory / "judgments.json").write_bytes(canonical(changed))
    with pytest.raises(AssertionError):
        replay(packet_directory)


def test_seal_tampering_rejected(packet_directory: Path) -> None:
    freeze(packet_directory)
    target = packet_directory / "judgments.freeze.json"
    seal = json.loads(target.read_bytes())
    seal["judgments_sha256"] = "0" * 64
    target.write_bytes(canonical(seal))
    with pytest.raises(AssertionError):
        replay(packet_directory)

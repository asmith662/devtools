# Copyright (c) 2026
# ruff: noqa: D103, S101, COM812, PLR2004, PT007, RUF043, ARG001 -- isolated case test conventions
"""Focused integrity tests for the blind Case 0009 packet."""

from __future__ import annotations

import gzip
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from experiments.codex_dogfood.case_0009.adjudication import build_packet
from experiments.codex_dogfood.case_0009.freeze import load_inputs


@pytest.fixture(scope="module")
def stage_a() -> dict[str, object]:
    return load_inputs()


def test_two_independent_renders_are_byte_identical(stage_a: dict[str, object]) -> None:
    first = build_packet.render(stage_a)
    second = build_packet.render(stage_a)
    assert first == second
    assert first["resources.json.gz"] == second["resources.json.gz"]
    assert gzip.decompress(first["resources.json.gz"]) == gzip.decompress(
        second["resources.json.gz"]
    )


def test_manifest_binds_payload_and_compressed_artifact(
    stage_a: dict[str, object],
) -> None:
    rendered = build_packet.render(stage_a)
    manifest = json.loads(rendered["manifest.json"])
    archive = rendered["resources.json.gz"]
    payload = gzip.decompress(archive)
    integrity = json.loads(rendered["integrity.json"])

    assert manifest["resources_payload_sha256"] == build_packet.sha256(payload)
    assert manifest["resources_archive_sha256"] == build_packet.sha256(archive)
    assert integrity["sha256"]["manifest.json"] == build_packet.sha256(
        rendered["manifest.json"]
    )
    assert integrity["sha256"]["resources.json.gz"] == build_packet.sha256(archive)
    assert manifest["resource_count"] == 531
    assert manifest["obligation_count"] == 9
    assert manifest["expected_cell_count"] == 4779


def test_render_matches_frozen_stage_a_frame_task_and_obligations(
    stage_a: dict[str, object],
) -> None:
    rendered = build_packet.render(stage_a)
    build_packet.validate_stage_a(stage_a, rendered)


@pytest.mark.parametrize(
    "field",
    (
        "arm",
        "arms",
        "arm_a",
        "arm_b",
        "arm_identity",
        "rank",
        "canonical_rank",
        "identifier_aware_rank",
        "score",
        "score_contributions",
        "score_contribution",
        "positive_result_membership",
        "positive_match",
        "identifier_analyzer_terms",
        "identifier_terms",
        "analyzer_terms",
        "rank_delta",
        "treatment_gain",
        "treatment_loss",
        "treatment_gains",
        "treatment_losses",
        "gains",
        "losses",
        "candidate_membership",
        "execution_cost",
        "treatment_cost",
        "effectiveness",
        "outcome",
    ),
)
def test_treatment_field_leakage_is_rejected(
    stage_a: dict[str, object], field: str
) -> None:
    rendered = build_packet.render(stage_a)
    manifest = json.loads(rendered["manifest.json"])
    archive = rendered["resources.json.gz"]
    resources = json.loads(gzip.decompress(archive))
    manifest[field] = 1
    with pytest.raises(ValueError, match="digest|whitelist|Treatment"):
        build_packet.validate_render(
            manifest, resources, gzip.decompress(archive), archive
        )


def test_existing_packet_overwrite_is_refused_by_default(
    stage_a: dict[str, object], monkeypatch: pytest.MonkeyPatch
) -> None:
    rendered = build_packet.render(stage_a)
    with TemporaryDirectory(
        prefix="case0009-packet-test-", dir=build_packet.CASE
    ) as temp:
        target_dir = Path(temp)
        target = target_dir / "manifest.json"
        target.write_text("preserve", encoding="utf-8")
        monkeypatch.setattr(build_packet, "PACKET", target_dir)

        with pytest.raises(FileExistsError, match="refusing overwrite"):
            build_packet.write_packet(rendered)
        assert target.read_text(encoding="utf-8") == "preserve"


def test_read_only_replay_matches_repaired_packet(stage_a: dict[str, object]) -> None:
    build_packet.verify_committed()

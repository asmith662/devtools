# Copyright (c) 2026
# ruff: noqa: ANN001, COM812, D103, INP001, SLF001, TC003
"""Allowlist, frame and overwrite checks for the blind packet builder."""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

import build_adjudication_packet as packet
import pytest


def _packet_values() -> tuple[dict, bytes]:
    provenance = {"source_identity": "source", "span": None, "explanation": "frozen"}
    resources = [
        {
            "identity": {
                "address": f"src/{index}.py",
                "content_identity": f"id-{index}",
            },
            "address": f"src/{index}.py",
            "content_identity": f"id-{index}",
            "content": f"content-{index}",
        }
        for index in range(packet.RESOURCE_COUNT)
    ]
    archive = packet._canonical(
        {
            "schema": "case-0006-blind-resources-v1",
            "case_identity": "case_0006",
            "repository_id": packet.REPOSITORY_ID,
            "repository_snapshot_id": packet.SNAPSHOT_ID,
            "eligible_frame_identity": packet.CORPUS_ID,
            "resources": resources,
        }
    )
    compressed = gzip.compress(archive, mtime=0)
    manifest = {
        "schema": "case-0006-blind-adjudication-v1",
        "case_identity": "case_0006",
        "task_identity": "task",
        "development_task": "task text",
        "purpose": "purpose",
        "repository_id": packet.REPOSITORY_ID,
        "repository_snapshot_id": packet.SNAPSHOT_ID,
        "eligible_frame_identity": packet.CORPUS_ID,
        "eligible_resource_count": packet.RESOURCE_COUNT,
        "shared_anchors": [
            {"identity": "a", "text": "anchor", "task_provenance": provenance}
        ],
        "obligations": [
            {
                "identity": f"o-{index}",
                "desired_information_predicate": "predicate",
                "anchor_references": ["a"],
                "task_provenance": provenance,
                "requirement": "mandatory",
                "applicability_condition": None,
                "satisfaction_criterion": {
                    "name": "criterion",
                    "statement": "statement",
                },
                "pre_execution_witness_alternatives": [],
            }
            for index in range(10)
        ],
        "adjudication_instructions": packet.INSTRUCTIONS,
        "resource_archive": packet.RESOURCES_NAME,
        "resource_archive_sha256": hashlib.sha256(compressed).hexdigest(),
    }
    return manifest, compressed


def test_blind_schema_allows_full_frame_without_treatment_fields() -> None:
    manifest, archive = _packet_values()
    packet._validate(manifest, archive)


def test_treatment_field_is_rejected_by_manifest_allowlist() -> None:
    manifest, archive = _packet_values()
    manifest["role_preference"] = []
    with pytest.raises(ValueError, match="explicit allowlist"):
        packet._validate(manifest, archive)


def test_treatment_field_is_rejected_by_resource_allowlist() -> None:
    manifest, archive = _packet_values()
    content = json.loads(gzip.decompress(archive))
    content["resources"][0]["rank"] = 1
    changed = gzip.compress(packet._canonical(content), mtime=0)
    manifest["resource_archive_sha256"] = hashlib.sha256(changed).hexdigest()
    with pytest.raises(ValueError, match="resource frame/schema"):
        packet._validate(manifest, changed)


def test_build_refuses_existing_packet_before_stage_a_read(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(packet, "ADJUDICATION", tmp_path)
    (tmp_path / packet.MANIFEST_NAME).write_text("existing", encoding="utf-8")

    def stage_a_must_not_be_read() -> None:
        pytest.fail("Existing packet must refuse before Stage A reads.")

    monkeypatch.setattr(packet, "_verify_stage_a", stage_a_must_not_be_read)
    with pytest.raises(FileExistsError, match="already exists"):
        packet.build()

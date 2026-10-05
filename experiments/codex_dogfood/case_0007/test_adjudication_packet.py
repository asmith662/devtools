# Copyright (c) 2026
# ruff: noqa: ANN202, D103, EM101, EM102, PLR2004, S101, SLF001, TRY003
"""Case-local tests for the Stage B.5 treatment-free packet builder."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import pytest

from devtools.context.localization import lexical
from devtools.context.localization.generation import generate, references
from devtools.context.localization.grounding import resolve
from devtools.context.localization.routing import derive
from experiments.codex_dogfood.case_0007 import build_adjudication_packet as packet


@pytest.fixture(scope="module")
def built_packet(tmp_path_factory: pytest.TempPathFactory) -> Path:
    destination = tmp_path_factory.mktemp("case-0007") / "adjudication"
    packet.build(destination)
    return destination


def test_packet_contains_exact_frozen_frame_and_allowlisted_semantics(
    built_packet: Path,
) -> None:
    manifest = json.loads((built_packet / packet.MANIFEST_NAME).read_text())
    rows = json.loads(
        gzip.decompress((built_packet / packet.RESOURCES_NAME).read_bytes()),
    )
    assert manifest["eligible_resource_count"] == len(rows) == 521
    assert len(manifest["shared_anchors"]) == 9
    assert len(manifest["obligations"]) == 11
    assert manifest["task"] == packet.EXPECTED_TASK
    assert set(manifest) == {
        "schema",
        "case_identity",
        "task_identity",
        "task",
        "purpose",
        "repository_id",
        "snapshot_id",
        "corpus_id",
        "eligible_resource_count",
        "shared_anchors",
        "obligations",
        "adjudication_instructions",
        "resource_archive",
    }
    assert all(
        set(row)
        == {"resource_occurrence_identity", "address", "content_identity", "content"}
        for row in rows
    )
    assert manifest["obligations"][-1]["identity"] == "validation"
    assert all(
        not obligation["pre_execution_accepted_witness_alternatives"]
        for obligation in manifest["obligations"]
    )


def test_forbidden_treatment_operations_and_stage_b_files_are_not_accessed(
    built_packet: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("A production treatment operation was invoked.")

    monkeypatch.setattr(lexical, "acquire_localization_lexical_evidence", forbidden)
    monkeypatch.setattr(derive, "route_localization_lexical_evidence", forbidden)
    monkeypatch.setattr(resolve, "ground_task_anchor", forbidden)
    monkeypatch.setattr(generate, "generate_witness_hypotheses", forbidden)
    monkeypatch.setattr(references, "project_referencing_resources", forbidden)

    forbidden_names = {
        "stage_b_raw.pkl.gz",
        "capture.pkl.gz",
        "retrieval.json",
        "routing.json",
        "grounding.json",
        "generation.json",
    }
    original_open = Path.open

    def guarded_open(path: Path, *args: object, **kwargs: object):
        if path.name in forbidden_names:
            raise AssertionError(f"Stage B semantic artifact opened: {path.name}")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_open)
    packet.verify(built_packet)


def test_deterministic_read_only_reconstruction_and_overwrite_refusal(
    built_packet: Path,
) -> None:
    before = packet.verify(built_packet)
    with pytest.raises(FileExistsError, match="refusing overwrite"):
        packet.build(built_packet)
    assert packet.verify(built_packet) == before


def test_tampering_is_detected(built_packet: Path) -> None:
    resource_file = built_packet / packet.RESOURCES_NAME
    original = resource_file.read_bytes()
    try:
        resource_file.write_bytes(original[:-1] + bytes([original[-1] ^ 1]))
        with pytest.raises(ValueError, match="deterministic Stage A reconstruction"):
            packet.verify(built_packet)
    finally:
        resource_file.write_bytes(original)


def test_blind_manifest_rejects_treatment_fields() -> None:
    invalid = {
        "schema": "case-0007-blind-adjudication-v1",
        "case_identity": "case_0007",
        "task_identity": "task",
        "task": packet.EXPECTED_TASK,
        "purpose": "purpose",
        "repository_id": packet.EXPECTED_REPOSITORY,
        "snapshot_id": packet.EXPECTED_SNAPSHOT,
        "corpus_id": packet.EXPECTED_CORPUS,
        "eligible_resource_count": 521,
        "shared_anchors": [],
        "obligations": [],
        "adjudication_instructions": "neutral",
        "resource_archive": {},
        "generation_outcome": "forbidden",
    }
    with pytest.raises(ValueError, match="allowlist"):
        packet._validate_manifest(invalid)

# Copyright (c) 2026
# ruff: noqa: ANN202, COM812, D103, EM102, INP001, PLR2004, PT018, RUF043, S101, SLF001, TRY003
"""Focused checks for the treatment-free Case 0008 packet builder."""

from __future__ import annotations

import builtins
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("build_adjudication_packet.py")
SPEC = importlib.util.spec_from_file_location("case_0008_blind_packet", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
packet = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(packet)

CASE = MODULE_PATH.parent
BLIND = CASE / "adjudication"
BLOCKED_NAMES = {
    "stage_b_raw.pkl.gz",
    "stage_b_generation_recovery_raw.pkl.gz",
    "capture.pkl.gz",
    "retrieval.json",
    "routing.json",
    "grounding.json",
    "generation.json",
    "stage_b.md",
    "stage_b_integrity.json",
    "stage_b_attempt_1.json",
    "stage_b_attempt_1.md",
    "stage_b_recovery.md",
    "recovery_authorization.json",
}


def test_packet_has_exact_frame_and_allowlisted_semantics() -> None:
    manifest_bytes, resources_bytes = packet.render_expected()
    manifest = json.loads(manifest_bytes)
    resources = json.loads(gzip.decompress(resources_bytes))

    assert len(resources["resources"]) == 523
    assert manifest["resource_count"] == 523
    assert len(manifest["shared_anchors"]) == 11
    assert len(manifest["obligations"]) == 13
    assert set(manifest) == packet.MANIFEST_KEYS
    assert all(set(row) == packet.RESOURCE_KEYS for row in resources["resources"])
    assert all(
        not item["pre_execution_accepted_witness_alternatives"]
        for item in manifest["obligations"]
    )
    assert resources["resources"][0]["address"] == "AGENTS.md"
    assert (
        manifest["blind_resources"]["sha256"]
        == hashlib.sha256(resources_bytes).hexdigest()
    )


def test_stage_b_paths_are_tripwired_during_reconstruction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_read_bytes = Path.read_bytes
    original_open = Path.open

    def guarded_read_bytes(path: Path) -> bytes:
        if path.name in BLOCKED_NAMES:
            raise AssertionError(f"Stage B semantic artifact accessed: {path.name}")
        return original_read_bytes(path)

    def guarded_open(path: Path, *args: object, **kwargs: object):
        if path.name in BLOCKED_NAMES:
            raise AssertionError(f"Stage B semantic artifact accessed: {path.name}")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_bytes", guarded_read_bytes)
    monkeypatch.setattr(Path, "open", guarded_open)
    packet.verify_packet()


def test_builder_has_no_treatment_operation_dependencies() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    forbidden_calls = {
        "acquire_localization_lexical_evidence",
        "route_localization_lexical_evidence",
        "build_anchor_grounding_view",
        "generate_witness_hypotheses",
        "project_referencing_resources",
        "project_direct_import_dependencies",
    }
    assert not any(name in source for name in forbidden_calls)
    assert "devtools.context.localization" not in source


def test_reconstruction_does_not_import_treatment_packages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_import = builtins.__import__

    def guarded_import(name: str, *args: object, **kwargs: object):
        if name.startswith("devtools.context.localization"):
            raise AssertionError(f"Treatment package imported: {name}")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    packet.render_expected()


def test_strict_schema_rejects_treatment_metadata() -> None:
    manifest_bytes, _ = packet.render_expected()
    manifest = json.loads(manifest_bytes)
    manifest["projection_operator"] = "REFERENCE"
    with pytest.raises(
        ValueError, match="strict allowlist|Forbidden treatment metadata"
    ):
        packet._validate_manifest(manifest)

    manifest.pop("projection_operator")
    manifest["blind_resources"]["recovery_metadata"] = {"present": False}
    with pytest.raises(
        ValueError, match="strict allowlist|Forbidden treatment metadata"
    ):
        packet._validate_manifest(manifest)


def test_deterministic_reconstruction_and_overwrite_refusal() -> None:
    expected_manifest, expected_resources = packet.render_expected()
    actual_manifest = (BLIND / packet.MANIFEST_NAME).read_bytes()
    actual_resources = (BLIND / packet.RESOURCES_NAME).read_bytes()
    assert actual_manifest == expected_manifest
    assert actual_resources == expected_resources
    before = (
        hashlib.sha256(actual_manifest).hexdigest(),
        hashlib.sha256(actual_resources).hexdigest(),
    )
    with pytest.raises(FileExistsError, match="refusing overwrite"):
        packet.build_packet()
    after = (
        hashlib.sha256((BLIND / packet.MANIFEST_NAME).read_bytes()).hexdigest(),
        hashlib.sha256((BLIND / packet.RESOURCES_NAME).read_bytes()).hexdigest(),
    )
    assert after == before


def test_tampered_archive_and_content_identity_mismatch_are_rejected(
    tmp_path: Path,
) -> None:
    manifest_bytes, resources_bytes = packet.render_expected()
    tampered_dir = tmp_path / "adjudication"
    tampered_dir.mkdir()
    (tampered_dir / packet.MANIFEST_NAME).write_bytes(manifest_bytes)
    resource_data = json.loads(gzip.decompress(resources_bytes))
    resource_data["resources"][0]["content_identity"] = "0" * 64
    resource_data["resources"][0]["occurrence_identity"]["content_identity"] = "0" * 64
    altered_bytes = gzip.compress(packet.json_bytes(resource_data), mtime=0)
    (tampered_dir / packet.RESOURCES_NAME).write_bytes(altered_bytes)
    with pytest.raises(
        ValueError, match="differs from deterministic Stage A reconstruction"
    ):
        packet.verify_packet(tampered_dir)

    treatment, pre, native, _ = packet._stage_a()
    changed_pre = json.loads(json.dumps(pre))
    changed_pre["resources"][0]["content_identity"] = "0" * 64
    with pytest.raises(
        ValueError, match="resource address/content identity correspondence differs"
    ):
        packet._project(treatment, changed_pre, native)


def test_forbidden_field_detector_checks_metadata_keys_only() -> None:
    packet._reject_forbidden_keys(
        {"safe": "repository text can mention generation and routing"}
    )
    with pytest.raises(ValueError, match="Forbidden treatment metadata field"):
        packet._reject_forbidden_keys({"grounding_request": 11})

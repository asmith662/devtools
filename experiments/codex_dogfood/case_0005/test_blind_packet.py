# Copyright (c) 2026
# ruff: noqa: ANN001, ANN002, ANN003, ANN201, ANN202, COM812, EM101, INP001, PLR2004, S101, TRY003
"""Check the Case 0005 blind schema and reconstruction without judgments."""

from __future__ import annotations

import gzip
import importlib.util
import json
import sys
from pathlib import Path

import pytest

CASE = Path(__file__).resolve().parent
sys.path.insert(0, str(CASE))
SPEC = importlib.util.spec_from_file_location(
    "case0005_blind_packet_test", CASE / "build_adjudication_packet.py"
)
assert SPEC is not None
assert SPEC.loader is not None
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)

ALLOWED_SOURCE = {
    "integrity.json",
    "treatment.json",
    "pre_retrieval.json",
    "inputs.pkl.gz",
    "freeze.py",
    "README.md",
    "test_freeze.py",
    "blind_manifest.json",
    "blind_resources.json.gz",
}


def test_read_only_packet_reconstruction_and_source_boundary(monkeypatch):
    """Reconstruction uses Stage A only and reproduces exact packet bytes."""
    original = builder.read_bytes
    seen = []

    def bounded(path, *args, **kwargs):
        seen.append(path.name)
        if path.name not in ALLOWED_SOURCE:
            raise AssertionError("A non-allowlisted source was read.")
        return original(path, *args, **kwargs)

    monkeypatch.setattr(builder, "read_bytes", bounded)
    result = builder.verify()
    assert result["resources"] == 515
    assert result["anchors"] == 6
    assert result["obligations"] == 9
    assert result["deterministic_reconstruction"] is True
    assert result["retrieval_or_routing_executed"] is False
    assert "inputs.pkl.gz" in seen
    assert not ({"capture.pkl.gz", "retrieval.json", "routing.json"} & set(seen))


def test_strict_allowlists_and_conditionality():
    """Only permitted fields appear, with applicability text preserved."""
    manifest = json.loads(builder.read_bytes(builder.MANIFEST))
    archive = json.loads(gzip.decompress(builder.read_bytes(builder.ARCHIVE)))
    resources = archive["resources"]
    builder.validate_schema(manifest, resources)
    assert set(manifest) == builder.MANIFEST_KEYS
    assert not any("preferred" in key.lower() for key in manifest)
    assert not any("query" in key.lower() or "lane" in key.lower() for key in manifest)
    assert all(set(item) == builder.RESOURCE_KEYS for item in resources)
    conditional = next(
        item
        for item in manifest["obligations"]
        if item["identity"] == "package-integration"
    )
    assert conditional["applicability_condition"] == (
        "Existing package/API conventions govern integration of the new "
        "association capability."
    )
    assert all(item["witness_alternatives"] == [] for item in manifest["obligations"])


def test_existing_packet_refuses_overwrite_without_changes(monkeypatch):
    """A repeated build exits before touching or replacing either artifact."""
    before = {
        path.name: builder.sha(builder.read_bytes(path))
        for path in (builder.MANIFEST, builder.ARCHIVE)
    }

    def forbidden(*_args, **_kwargs):
        raise AssertionError("Overwrite refusal must precede source reconstruction.")

    monkeypatch.setattr(builder, "_verify_stage_a", forbidden)
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        builder.build()
    after = {
        path.name: builder.sha(builder.read_bytes(path))
        for path in (builder.MANIFEST, builder.ARCHIVE)
    }
    assert before == after
    monkeypatch.undo()
    assert builder.verify()["deterministic_reconstruction"] is True


def test_forbidden_schema_field_is_rejected():
    """An unallowlisted query treatment field cannot enter the packet."""
    manifest = json.loads(builder.read_bytes(builder.MANIFEST))
    manifest["obligation_queries"] = []
    archive = json.loads(gzip.decompress(builder.read_bytes(builder.ARCHIVE)))
    with pytest.raises(ValueError, match="manifest keys differ"):
        builder.validate_schema(manifest, archive["resources"])

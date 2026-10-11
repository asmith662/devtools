# Copyright (c) 2026
# ruff: noqa: S101, PLR2004 -- packet tests without semantic judgments
"""Independent schema/leakage/tamper/overwrite guards, with no adjudication."""

from __future__ import annotations

import copy
import gzip
from pathlib import Path
from unittest.mock import patch

import pytest

from experiments.codex_dogfood.case_0014.stage_c import packet, validate_packet


def test_projection_and_native_identity_reconstruction() -> None:
    """Semantic projection retains all original text and native frame bindings."""
    payload = packet.payload()
    validate_packet.validate_payload(payload)
    assert len(payload["eligible_resources"]) == 515
    assert len(payload["obligations"]) == 6
    assert set(payload) == validate_packet.PAYLOAD
    assert packet.render(payload) == packet.render(payload)


@pytest.mark.parametrize(
    "field",
    [
        "queries",
        "roles",
        "weights",
        "generic_lexicon",
        "arms",
        "ranks",
        "scores",
        "contributions",
        "results",
        "metrics",
        "gates",
        "decision_rule",
        "cost",
        "timing",
    ],
)
def test_nested_treatment_metadata_rejected(field: str) -> None:
    """Every treatment category fails a deep metadata tripwire and allowlist."""
    payload = copy.deepcopy(packet.payload())
    payload["obligations"][0]["task_provenance"][field] = "leak"
    with pytest.raises(ValueError, match="provenance"):
        validate_packet.validate_payload(payload)
    with pytest.raises(ValueError, match="leakage"):
        validate_packet.tripwire({"nested": [{field: "leak"}]})


def test_initial_whitelist_physical_hash_tamper_and_overwrite(tmp_path: Path) -> None:
    """Authenticate a new packet, refuse replacement and reject byte tamper."""
    root = tmp_path / "packet"
    files = packet.render(packet.payload())
    packet.publish(root, files)
    assert validate_packet.validate(root)["status"] == "PASS; NO ADJUDICATION"
    with pytest.raises(FileExistsError):
        packet.publish(root, files)
    (root / "manifest.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="digest"):
        validate_packet.validate(root)
    (root / "manifest.json").write_bytes(files["manifest.json"])
    (root / ".local").mkdir()
    with pytest.raises(ValueError, match="whitelist"):
        validate_packet.validate(root)


def test_resource_and_obligation_tamper_rejected() -> None:
    """Hash-bound content and original obligation clause membership remain exact."""
    value = packet.payload()
    value["eligible_resources"][0]["content"] += "tamper"
    with pytest.raises(ValueError, match="identity"):
        validate_packet.validate_payload(value)
    value = packet.payload()
    value["obligations"][0]["task_provenance"]["end"] -= 1
    with pytest.raises(ValueError, match="membership"):
        validate_packet.validate_payload(value)
    archive = packet.render(packet.payload())["resources.json.gz"]
    assert gzip.decompress(archive) == validate_packet.canonical(packet.payload())


def test_relative_cli_publication_uses_explicit_canonical_base(tmp_path: Path) -> None:
    """Relative CLI destinations resolve before any exclusive file publication."""
    with patch.object(packet, "ROOT", tmp_path):
        packet.publish(Path("relative-packet"), packet.render(packet.payload()))
    assert (
        validate_packet.validate(tmp_path / "relative-packet")["status"]
        == "PASS; NO ADJUDICATION"
    )

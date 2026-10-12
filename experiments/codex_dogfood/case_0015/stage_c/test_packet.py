# Copyright (c) 2026
# ruff: noqa: S101 -- blind schema tests without semantic adjudication
"""Strict original-input metadata, byte/tamper/overwrite and leakage validation."""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0015.stage_b.execute import CAPTURE
from experiments.codex_dogfood.case_0015.stage_c import packet, validate_packet

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def value() -> dict[str, Any]:
    """Construct real semantic projection only after Stage B validation."""
    if not (CAPTURE / "validation.json").exists():
        pytest.skip("Stage B not fully captured/validated; no real packet construction")
    return packet.payload()


@pytest.mark.parametrize("field", sorted(validate_packet.FORBIDDEN))
def test_deep_leakage_tripwire(field: str) -> None:
    """Forbidden experimental keys fail even when nested in metadata containers."""
    with pytest.raises(ValueError, match="leakage"):
        validate_packet.tripwire({"nested": [{field: "secret"}]})


def test_projection_exact_bytes_and_whitelist(
    value: dict[str, Any],
    tmp_path: Path,
) -> None:
    """Preserve source semantics; refuse replacement and byte tamper."""
    validate_packet.validate_payload(value)
    files = packet.render(value)
    assert files == packet.render(value)
    root = tmp_path / "initial-packet"
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


def test_original_obligation_resource_frame_tamper(value: dict[str, Any]) -> None:
    """Reject task, obligation, content and frame identity mutations."""
    changed = copy.deepcopy(value)
    changed["eligible_resources"][0]["content"] += "tamper"
    with pytest.raises(ValueError, match="identity"):
        validate_packet.validate_payload(changed)
    changed = copy.deepcopy(value)
    changed["obligations"][0]["task_span"]["end"] -= 1
    with pytest.raises(ValueError, match="obligation"):
        validate_packet.validate_payload(changed)
    changed = copy.deepcopy(value)
    changed["obligations"][0]["hidden"] = {"df_union": 1}
    with pytest.raises(ValueError, match="obligation"):
        validate_packet.validate_payload(changed)
    changed = copy.deepcopy(value)
    changed["task_text"] += "changed"
    with pytest.raises(ValueError, match="task bytes"):
        validate_packet.validate_payload(changed)

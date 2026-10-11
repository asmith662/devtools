# Copyright (c) 2026
# ruff: noqa: COM812, D103 -- controlled standalone packet tests
"""Reject physical tamper, unknown metadata and reparse points before adjudication."""

from __future__ import annotations

import copy
import stat
from pathlib import Path
from types import SimpleNamespace

import pytest

from experiments.codex_dogfood.case_0013.stage_c import packet, validate_packet


def test_physical_packet_tamper(tmp_path: Path) -> None:
    root = tmp_path / "packet"
    packet.publish(root, packet.render(packet.payload()))
    target = root / "README.md"
    target.write_bytes(target.read_bytes() + b"tamper")
    with pytest.raises(ValueError, match="digest differs"):
        validate_packet.validate(root)


def test_reparse_lstat_is_rejected_without_following_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "packet"
    packet.publish(root, packet.render(packet.payload()))
    original = Path.lstat

    def observed(path: Path) -> object:
        if path == root:
            return SimpleNamespace(st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT)
        return original(path)

    monkeypatch.setattr(Path, "lstat", observed)
    with pytest.raises(ValueError, match="reparse point"):
        validate_packet.validate(root)


@pytest.mark.parametrize("where", ["payload", "obligation", "basis"])
def test_deep_metadata_allowlist(where: str) -> None:
    p = copy.deepcopy(packet.payload())
    if where == "payload":
        p["route_policy"] = "forbidden"
    elif where == "obligation":
        p["obligations"][0]["rank"] = 1
    else:
        p["obligations"][0]["task_basis"][0]["locator"] = "forbidden"
    with pytest.raises(ValueError, match=r"allowlist|leakage|metadata"):
        validate_packet.validate_payload(p)

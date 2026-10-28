# Copyright (c) 2026
# ruff: noqa: D103 -- public custody and exact admission boundary cases
"""Known source and caller-owned restoration, without a second filesystem writer."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding import CodingLimits, CodingProgress
from devtools.agents.coding import custody as owner
from devtools.agents.coding.custody import SourceCustody
from devtools.agents.coding.edits import CodingEditError, replace_exact_text
from devtools.context import RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.filesystem import TextFile, write

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    "fault",
    ["calls", "proposals", "actions", "call-time", "wall-time"],
)
def test_invalid_budget_refused_before_invocation(fault: str) -> None:
    with pytest.raises(ValueError, match="Coding limits"):
        CodingLimits(
            0 if fault == "calls" else 1,
            0 if fault == "proposals" else 1,
            -1 if fault == "actions" else 1,
            Duration.seconds(0 if fault == "call-time" else 1),
            Duration.seconds(0 if fault == "wall-time" else 1),
        )


def test_action_limit_charged_before_effect_and_not_refunded() -> None:
    progress = CodingProgress(
        CodingLimits(1, 1, 1, Duration.seconds(1), Duration.seconds(1)),
    )
    effect = progress.claim_action("native-1")
    assert progress.actions == 1
    assert effect.acknowledged is False
    with pytest.raises(ValueError, match="action budget"):
        progress.claim_action("native-2")
    assert progress.actions == 1
    assert len(progress.effects) == 1


def test_empty_or_unbounded_custody_refused(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="custody"):
        SourceCustody(resolve_path(tmp_path), {}, maximum_bytes=10)
    with pytest.raises(ValueError, match="custody"):
        SourceCustody(
            resolve_path(tmp_path),
            {RepositoryResourceAddress("a.py"): None},
            maximum_bytes=0,
        )


def test_absent_slot_and_unknown_capture_refusal(tmp_path: Path) -> None:
    address = RepositoryResourceAddress("new.txt")
    custody = SourceCustody(resolve_path(tmp_path), {address: None}, maximum_bytes=1024)
    assert custody.capture() == {address: None}
    with pytest.raises(TypeError):
        custody.baseline[address] = "changed"  # type: ignore[index]
    with pytest.raises(ValueError, match="outside"):
        custody.expect(RepositoryResourceAddress("other.txt"), "foreign")
    entries: list[object] = []
    refused = custody.restore_known({}, lambda *args: entries.append(args))
    assert refused.reconciliation_required
    assert entries == []
    custody.expect(address, "known")
    write(TextFile(resolve_path(tmp_path / "new.txt"), "known"))
    current = custody.capture()
    write(TextFile(resolve_path(tmp_path / "new.txt"), "later unknown"))
    refused = custody.restore_known(current, lambda *args: entries.append(args))
    assert refused.reconciliation_required
    assert (tmp_path / "new.txt").read_text() == "later unknown"
    assert entries == []


def test_failed_host_restoration_is_not_success(tmp_path: Path) -> None:
    address = RepositoryResourceAddress("a.txt")
    path = resolve_path(tmp_path / "a.txt")
    write(TextFile(path, "before"))
    custody = SourceCustody(
        resolve_path(tmp_path),
        {address: "before"},
        maximum_bytes=1024,
    )
    custody.expect(address, "after")
    write(TextFile(path, "after"))
    result = custody.restore_known(custody.capture(), lambda *_args: None)
    assert result.restored is False
    assert result.reconciliation_required is True
    assert path.value.read_text() == "after"


@pytest.mark.parametrize("target", ["root", "entry"])
def test_canonical_custody_change_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    target: str,
) -> None:
    address = RepositoryResourceAddress("a.txt")
    custody = SourceCustody(resolve_path(tmp_path), {address: None}, maximum_bytes=1024)
    original = resolve_path
    monkeypatch.setattr(
        owner,
        "resolve_path",
        lambda path: (
            original(tmp_path.parent)
            if target == "root" or path != tmp_path
            else original(path)
        ),
    )
    with pytest.raises(ValueError, match=r"changed|aliases"):
        custody.capture()


@pytest.mark.parametrize(
    ("source", "old", "new", "region", "cap"),
    [
        ("a", 1, "b", 10, 10),
        ("a", "a", None, 10, 10),
        ("a", "", "b", 10, 10),
        ("a", "a", "", 10, 10),
        ("a", "a", "\x00", 10, 10),
        ("a", "a", "a", 10, 10),
        ("a", "a", "bbb", 2, 10),
        ("a\r", "a", "b", 10, 10),
        ("a\r\nb\n", "a", "b", 10, 10),
        ("aa", "a", "b", 10, 10),
        ("a", "x", "b", 10, 10),
        ("a", "a", "bb", 10, 1),
        ("a\r\n", "a\n", "b\n", 2, 20),
        ("a\r\n", "a\r\n", "a\n", 20, 20),
    ],
)
def test_exact_edit_refusals_do_not_modify_source(
    source: str,
    old: object,
    new: object,
    region: int,
    cap: int,
) -> None:
    with pytest.raises(CodingEditError):
        replace_exact_text(source, old, new, region_bytes=region, source_bytes=cap)


def test_exact_crlf_and_explicit_deletion() -> None:
    assert replace_exact_text(
        "a\r\nb\r\n",
        "b\n",
        "c\n",
        region_bytes=10,
        source_bytes=20,
    ) == ("a\r\nc\r\n", 3, 6)
    assert replace_exact_text(
        "abc",
        "b",
        "",
        region_bytes=10,
        source_bytes=20,
        allow_empty_new=True,
    ) == ("ac", 1, 2)

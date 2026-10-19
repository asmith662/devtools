# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004, SLF001 -- tiny Git and source ownership fixtures
"""Ordinary branch ownership, forensic preservation and stopped-owner recovery."""

from __future__ import annotations

import asyncio
import json
from typing import Any

import pytest

from scripts.backlog.checkout import Checkout, recover
from scripts.backlog.coordinator import git
from tests.scripts.backlog.test_work import discovery
from tests.scripts.backlog.test_work import fixture as fixture  # noqa: PLC0414


def session(f: dict[str, Any]) -> Checkout:
    """Use only the authored tiny fixture, never the Devtools working source."""
    source = f["task"].source
    return Checkout(
        f["cycle"],
        "fixture-source-operation",
        "feat/fixture",
        f["task"].baseline_revision,
        files=[{"path": source, "text": (f["root"] / source).read_bytes().decode()}],
    )


def test_branch_lease_preserves_forensics_and_serializes(
    fixture: dict[str, Any],
) -> None:
    """A second source writer refuses and unrelated untracked bytes survive."""

    async def run() -> None:
        f = fixture
        forensic = f["root"] / " forensic-\u03c0.bin"
        forensic.write_bytes(b"\x00\xffhistoric\r\n")
        async with session(f) as owner:
            assert await git(f["root"], "branch", "--show-current") == "feat/fixture"
            with pytest.raises(PermissionError, match="Checkout owned"):
                async with session(f):
                    pytest.fail("Competing writer entered")
            with pytest.raises(PermissionError, match="backlog writes wait"):
                f["intake"].capture(discovery())
            owner.expect(f["task"].source, "# admitted temporary source\n")
            (f["root"] / f["task"].source).write_bytes(b"# admitted temporary source\n")
        assert await git(f["root"], "branch", "--show-current") == "coordinator"
        assert forensic.read_bytes() == b"\x00\xffhistoric\r\n"
        assert (
            await git(f["root"], "status", "--porcelain", "--untracked-files=no") == ""
        )
        assert (
            len(
                (await git(f["root"], "worktree", "list", "--porcelain")).split(
                    "worktree "
                )
            )
            == 2
        )

    asyncio.run(run())


def test_backlog_writer_prevents_branch_claim(fixture: dict[str, Any]) -> None:
    """Intake source writes and branch admission share one atomic writer gate."""

    async def run() -> None:
        f = fixture
        with (
            f["intake"]._writer(),
            pytest.raises(PermissionError, match="Checkout owned"),
        ):
            async with session(f):
                pytest.fail("Branch switching overlapped canonical administration")
        assert not (f["root"] / ".local/backlog/checkout-owner").exists()

    asyncio.run(run())


@pytest.mark.parametrize("kind", ["dirty", "staged", "operation", "stale", "collision"])
def test_incompatible_checkout_refuses(fixture: dict[str, Any], kind: str) -> None:
    """No stash, reset, overwrite or source-tree copy makes admission appear valid."""

    async def run() -> None:
        f = fixture
        owner = session(f)
        if kind in {"dirty", "staged"}:
            (f["root"] / f["task"].source).write_text("changed\n")
            if kind == "staged":
                await git(f["root"], "add", "--", f["task"].source)
        elif kind == "operation":
            (f["root"] / ".git/MERGE_HEAD").write_text(f["task"].baseline_revision)
        elif kind == "stale":
            await git(f["root"], "branch", "-m", "feat/fixture", "feat/replaced")
        else:
            await git(f["root"], "switch", "feat/fixture")
            (f["root"] / "collision.txt").write_text("tracked target\n")
            await git(f["root"], "add", "collision.txt")
            await git(f["root"], "commit", "-m", "target collision fixture")
            owner.revision = await git(f["root"], "rev-parse", "HEAD")
            await git(f["root"], "switch", "coordinator")
            (f["root"] / "collision.txt").write_text("untracked preserved\n")
        with pytest.raises(PermissionError):
            async with owner:
                pytest.fail("Incompatible checkout admitted")
        assert not owner.folder.exists()
        assert await git(f["root"], "branch", "--show-current") == "coordinator"

    asyncio.run(run())


def test_interrupted_operation_recovers_without_dispatch(
    fixture: dict[str, Any],
) -> None:
    """An abandoned known edit can be restored only by explicit host recovery."""

    async def run() -> None:
        f = fixture
        owner = session(f)
        await owner.__aenter__()
        owner.expect(f["task"].source, "# known interrupted edit\n")
        (f["root"] / f["task"].source).write_bytes(b"# known interrupted edit\n")
        with pytest.raises(PermissionError, match="Explicit"):
            await recover(f["cycle"], authorize=False)
        with pytest.raises(PermissionError, match="Checkout owned"):
            async with session(f):
                pytest.fail("Abandoned owner silently replaced")
        await recover(f["cycle"], authorize=True)
        assert await git(f["root"], "branch", "--show-current") == "coordinator"
        assert not owner.folder.exists()
        assert not list((f["root"] / ".local/backlog/work").glob("*/dispatch.json"))

    asyncio.run(run())


@pytest.mark.parametrize(
    "kind", ["unknown-bytes", "forensic-change", "corrupt-owner", "changed-head"]
)
def test_unknown_effects_retain_owner(fixture: dict[str, Any], kind: str) -> None:
    """Recovery never discards unreviewed effects or rewrites their provenance."""

    async def run() -> None:
        f = fixture
        forensic = f["root"] / "forensic.txt"
        forensic.write_text("preserved\n")
        owner = session(f)
        await owner.__aenter__()
        if kind == "unknown-bytes":
            (f["root"] / f["task"].source).write_text("unknown\n")
        elif kind == "forensic-change":
            forensic.write_text("externally modified\n")
        elif kind == "changed-head":
            await git(f["root"], "commit", "--allow-empty", "-m", "unexpected commit")
        else:
            path = owner.folder / "owner.json"
            value = json.loads(path.read_text())
            value["branch"] = "feat/forged"
            path.write_text(json.dumps(value))
        with pytest.raises(PermissionError):
            await recover(f["cycle"], authorize=True)
        assert owner.folder.exists()

    asyncio.run(run())

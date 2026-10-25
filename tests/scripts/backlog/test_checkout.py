# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004, SLF001 -- tiny Git and source ownership fixtures
"""Ordinary branch ownership, forensic preservation and stopped-owner recovery."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import pytest

from devtools.core.paths import resolve_path
from devtools.resources.commands import Command, CommandExecutor
from devtools.resources.filesystem.errors import FilesystemNotFoundError
from scripts.backlog import __main__ as cli
from scripts.backlog import checkout
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
            await recover(f["cycle"], authorize=False, expected_owner=identity(owner))
        with pytest.raises(PermissionError, match="Checkout owned"):
            async with session(f):
                pytest.fail("Abandoned owner silently replaced")
        await recover(f["cycle"], authorize=True, expected_owner=identity(owner))
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
            await recover(f["cycle"], authorize=True, expected_owner=identity(owner))
        assert owner.folder.exists()

    asyncio.run(run())


def identity(owner: Checkout) -> str:
    """Read the literal displayed journal identity, not a reconstructed expected ID."""
    return str(json.loads((owner.folder / "owner.json").read_text())["sha256"])


@pytest.mark.parametrize("action", ["recover", "finish", "expect"])
def test_stale_owner_cannot_affect_replacement(
    fixture: dict[str, Any], action: str
) -> None:
    """A retained old object/consent cannot overwrite or release a new owner."""

    async def run() -> None:
        f = fixture
        old = session(f)
        await old.__aenter__()
        displayed = identity(old)
        await recover(f["cycle"], authorize=True, expected_owner=displayed)
        new = session(f)
        await new.__aenter__()
        path = f["root"] / f["task"].source
        new.expect(f["task"].source, "# replacement admitted\n")
        path.write_bytes(b"# replacement admitted\n")
        journal = (new.folder / "owner.json").read_bytes()

        async def stale() -> None:
            if action == "recover":
                await recover(f["cycle"], authorize=True, expected_owner=displayed)
            elif action == "finish":
                await old.finish()
            else:
                old.expect(f["task"].source, "# stale write\n")

        with pytest.raises(PermissionError, match=r"identity mismatch|owner changed"):
            await stale()
        assert path.read_bytes() == b"# replacement admitted\n"
        assert (new.folder / "owner.json").read_bytes() == journal
        await new.finish()

    asyncio.run(run())


def test_recovery_fence_spans_restore_and_release(
    fixture: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The original R1/R2/B schedule is stopped before R2 or B can enter."""

    async def run() -> None:
        f = fixture
        owner = session(f)
        await owner.__aenter__()
        source = f["root"] / f["task"].source
        owner.expect(f["task"].source, "# interrupted A\n")
        source.write_bytes(b"# interrupted A\n")
        displayed = identity(owner)
        entered, resume = asyncio.Event(), asyncio.Event()
        real_git = git

        async def pause(root: Path, *args: str, trim: bool = True) -> str:
            if args[:2] == ("restore", "--source=HEAD"):
                entered.set()
                await resume.wait()
            return await real_git(root, *args, trim=trim)

        monkeypatch.setattr(checkout, "git", pause)
        first = asyncio.create_task(
            recover(f["cycle"], authorize=True, expected_owner=displayed)
        )
        await asyncio.wait_for(entered.wait(), timeout=20)
        try:
            with pytest.raises(PermissionError, match="transition in progress"):
                await recover(f["cycle"], authorize=True, expected_owner=displayed)
            with pytest.raises(PermissionError, match="transition in progress"):
                await session(f).__aenter__()
            assert source.read_bytes() == b"# interrupted A\n"
            assert identity(owner) == displayed
        finally:
            resume.set()
            await first
        replacement = session(f)
        await replacement.__aenter__()
        replacement.expect(f["task"].source, "# B\n")
        source.write_bytes(b"# B\n")
        with pytest.raises(PermissionError, match="identity mismatch"):
            await recover(f["cycle"], authorize=True, expected_owner=displayed)
        assert source.read_bytes() == b"# B\n"
        await replacement.finish()

    asyncio.run(run())


@pytest.mark.parametrize("change", ["unchanged", "replace", "disappear", "no"])
def test_cli_consent_is_for_displayed_owner_only(
    fixture: dict[str, Any], monkeypatch: pytest.MonkeyPatch, change: str
) -> None:
    """Actual CLI display/wait/recovery refuses stale consent, including live B."""

    async def run() -> None:
        f = fixture
        owner = session(f)
        await owner.__aenter__()
        shown = identity(owner)
        replacement: Checkout | None = None

        def answer(_prompt: str) -> str:
            nonlocal replacement
            if change in {"replace", "disappear"}:

                async def between() -> None:
                    nonlocal replacement
                    await recover(f["cycle"], authorize=True, expected_owner=shown)
                    if change == "replace":
                        replacement = session(f)
                        await replacement.__aenter__()
                        replacement.expect(f["task"].source, "# live B\n")
                        (f["root"] / f["task"].source).write_bytes(b"# live B\n")

                with ThreadPoolExecutor(max_workers=1) as pool:
                    pool.submit(lambda: asyncio.run(between())).result()
            return "n" if change == "no" else "y"

        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
        monkeypatch.setattr("builtins.input", answer)
        if change == "unchanged":
            result = await cli._work(
                argparse.Namespace(command="work-recover"), f["root"]
            )
            assert result == {
                "disposition": "CHECKOUT_RECOVERED",
                "dispatch_authorized": False,
            }
            assert not owner.folder.exists()
        else:
            with pytest.raises((PermissionError, FilesystemNotFoundError)) as error:
                await cli._work(argparse.Namespace(command="work-recover"), f["root"])
            assert type(error.value).__name__ in {
                "PermissionError",
                "FilesystemNotFoundError",
            }
            if replacement is not None:
                assert identity(replacement) != shown
                assert (f["root"] / f["task"].source).read_bytes() == b"# live B\n"
                # A new display and decision, not automatic yes propagation.
                monkeypatch.setattr("builtins.input", lambda _: "y")
                await cli._work(argparse.Namespace(command="work-recover"), f["root"])
            elif change == "no":
                assert identity(owner) == shown
                await owner.finish()

    asyncio.run(run())


@pytest.mark.parametrize(
    "kind",
    [
        "dangling",
        "file-link",
        "nested-link",
        "nested-dangling",
        "junction",
        "dangling-junction",
        "ignored-file",
        "noncolliding",
    ],
)
def test_ignored_entry_custody(  # noqa: C901, PLR0915 -- real platform custody matrix
    fixture: dict[str, Any], kind: str
) -> None:
    """Real links/reparse parents are preserved before any target Git switch."""

    async def run() -> None:  # noqa: C901, PLR0915 -- one explicit Git/link schedule
        f = fixture
        root = f["root"]
        (root / ".gitignore").write_text(
            ".local/\ncollision/\ncollision.txt\nunrelated-link\n", encoding="utf-8"
        )
        await git(root, "add", ".gitignore")
        await git(root, "commit", "-m", "Ignore authored custody entries")
        await git(root, "switch", "feat/fixture")
        (root / ".gitignore").write_text(
            ".local/\ncollision/\ncollision.txt\nunrelated-link\n", encoding="utf-8"
        )
        target = root / (
            "collision/member.txt"
            if kind
            in {"nested-link", "nested-dangling", "junction", "dangling-junction"}
            else "collision.txt"
        )
        target.parent.mkdir(exist_ok=True)
        target.write_text("tracked target\n", encoding="utf-8")
        await git(root, "add", "-f", str(target), ".gitignore")
        await git(root, "commit", "-m", "Authored collision target")
        revision = await git(root, "rev-parse", "HEAD")
        await git(root, "switch", "coordinator")
        link = root / (
            "collision"
            if kind
            in {"nested-link", "nested-dangling", "junction", "dangling-junction"}
            else "collision.txt"
        )
        if kind == "noncolliding":
            link = root / "unrelated-link"
        backing = root.parent / "backing"
        backing.mkdir()
        (backing / "member.txt").write_bytes(b"outside preserved\n")
        if kind == "ignored-file":
            link.write_bytes(b"ignored preserved\n")
        elif kind in {"junction", "dangling-junction"}:
            if os.name != "nt":
                pytest.skip("Windows junction capability only")
            destination = backing if kind == "junction" else root.parent / "missing-dir"
            result = await CommandExecutor().execute(
                Command("cmd")
                .args("/c", "mklink", "/J", str(link), str(destination))
                .cwd(resolve_path(root))
            )
            assert not result.failed, result.stderr
            assert link.is_junction()
        else:
            destination = backing if kind == "nested-link" else root / "missing-target"
            if kind == "file-link":
                destination = backing / "member.txt"
            try:
                link.symlink_to(
                    destination,
                    target_is_directory=kind in {"nested-link", "nested-dangling"},
                )
            except OSError as error:
                pytest.skip(f"OS symlink capability unavailable: {error}")
        before = link.lstat()
        owner = Checkout(f["cycle"], "entry-fixture", "feat/fixture", revision)
        if kind == "noncolliding":
            async with owner:
                assert link.is_symlink()
        else:
            with pytest.raises(PermissionError, match=r"collides|traverses"):
                await owner.__aenter__()
            assert await git(root, "branch", "--show-current") == "coordinator"
        assert link.lstat().st_ino == before.st_ino
        assert (backing / "member.txt").read_bytes() == b"outside preserved\n"
        if kind == "ignored-file":
            assert link.read_bytes() == b"ignored preserved\n"
        elif kind not in {"junction", "dangling-junction"}:
            assert link.is_symlink()
        if kind in {"junction", "dangling-junction"}:
            # Remove only this authored fixture junction, never its target.
            link.rmdir()

    asyncio.run(run())


@pytest.mark.parametrize("fault", ["cancel", "release"])
def test_recovery_failure_keeps_journal_and_releases_only_transition_lock(
    fixture: dict[str, Any], monkeypatch: pytest.MonkeyPatch, fault: str
) -> None:
    """Cancellation or failed release keeps custody and permits a fresh recovery."""

    async def run() -> None:
        f = fixture
        owner = session(f)
        await owner.__aenter__()
        owner.expect(f["task"].source, "# known A\n")
        source = f["root"] / f["task"].source
        source.write_bytes(b"# known A\n")
        real_rename = Path.rename

        async def cancel(root: Path, *args: str, trim: bool = True) -> str:
            if args[:2] == ("restore", "--source=HEAD"):
                raise asyncio.CancelledError
            return await git(root, *args, trim=trim)

        def fail_rename(path: Path, target: Path) -> Path:
            if path == owner.folder:
                message = "Authored release failure"
                raise PermissionError(message)
            return real_rename(path, target)

        if fault == "cancel":
            monkeypatch.setattr(checkout, "git", cancel)
            with pytest.raises(asyncio.CancelledError):
                await recover(
                    f["cycle"], authorize=True, expected_owner=identity(owner)
                )
            assert source.read_bytes() == b"# known A\n"
            monkeypatch.setattr(checkout, "git", git)
        else:
            monkeypatch.setattr(Path, "rename", fail_rename)
            with pytest.raises(PermissionError, match="Authored release failure"):
                await recover(
                    f["cycle"], authorize=True, expected_owner=identity(owner)
                )
            monkeypatch.setattr(Path, "rename", real_rename)
        assert (owner.folder / "owner.json").is_file()
        await recover(f["cycle"], authorize=True, expected_owner=identity(owner))
        assert not owner.folder.exists()
        assert await git(f["root"], "branch", "--show-current") == "coordinator"

    asyncio.run(run())


@pytest.mark.parametrize("boundary", ["restore", "return-switch"])
def test_crashed_recovery_retains_reconcilable_journal(
    fixture: dict[str, Any], boundary: str
) -> None:
    """A real child exits after an effect; a fresh decision reconciles known state."""

    async def run() -> None:
        f = fixture
        owner = session(f)
        await owner.__aenter__()
        owner.expect(f["task"].source, "# known crash edit\n")
        (f["root"] / f["task"].source).write_bytes(b"# known crash edit\n")
        code = """import asyncio,os,sys
sys.path.insert(0,sys.argv[1])
from pathlib import Path
from scripts.backlog import checkout
from scripts.backlog.work import WorkCycle
original=checkout.git
async def fault(root,*args,**kwargs):
 value=await original(root,*args,**kwargs)
 restore=sys.argv[4]=='restore' and args[:2]==('restore','--source=HEAD')
 returned=sys.argv[4]=='return-switch' and args[:2]==('switch','coordinator')
 if restore or returned:
  os._exit(23)
 return value
checkout.git=fault
asyncio.run(checkout.recover(WorkCycle(Path(sys.argv[2])),authorize=True,expected_owner=sys.argv[3]))
"""
        child = await CommandExecutor().execute(
            Command(sys.executable)
            .args(
                "-I",
                "-c",
                code,
                str(Path.cwd()),
                str(f["root"]),
                identity(owner),
                boundary,
            )
            .cwd(resolve_path(f["root"]))
        )
        assert child.exit_code == 23
        assert owner.folder.is_dir()
        assert (owner.folder / "owner.json").is_file()
        assert (f["root"] / f["task"].source).read_bytes() != b"# known crash edit\n"
        await recover(f["cycle"], authorize=True, expected_owner=identity(owner))
        assert not owner.folder.exists()
        assert await git(f["root"], "branch", "--show-current") == "coordinator"
        assert list(
            (owner.folder.parent / "checkout-history").glob("released-*/owner.json")
        )

    asyncio.run(run())


def test_legacy_journal_recovery_and_foreign_root_refusal(
    fixture: dict[str, Any],
) -> None:
    """Existing v1 owner records remain recoverable without inventing past epochs."""

    async def run() -> None:
        owner = session(fixture)
        await owner.__aenter__()
        path = owner.folder / "owner.json"
        value = json.loads(path.read_text())
        value.pop("sha256")
        value.pop("generation")
        # Deliberately authored legacy/foreign journals, not nominal native evidence.
        from scripts.backlog.intake import _digest  # noqa: PLC0415

        value["root"] = "foreign"
        path.write_text(
            json.dumps({**value, "sha256": _digest(value)}), encoding="utf-8"
        )
        with pytest.raises(PermissionError, match="identity mismatch"):
            await recover(
                fixture["cycle"], authorize=True, expected_owner=identity(owner)
            )
        value["root"] = str(fixture["root"])
        path.write_text(
            json.dumps({**value, "sha256": _digest(value)}), encoding="utf-8"
        )
        await recover(fixture["cycle"], authorize=True, expected_owner=identity(owner))
        assert not owner.folder.exists()

    asyncio.run(run())


def test_transition_excludes_threads_and_processes_and_releases_on_exit(
    fixture: dict[str, Any],
) -> None:
    """A real OS lease excludes another descriptor, not merely another task."""

    async def run() -> None:
        root = fixture["root"]
        code = """import os,sys
sys.path.insert(0,sys.argv[1])
from pathlib import Path
from scripts.backlog.checkout import _transition
try:
 with _transition(Path(sys.argv[2])):
  print('entered',flush=True)
  os._exit(0)
except PermissionError:
 print('refused',flush=True)
"""
        command = (
            Command(sys.executable)
            .args("-I", "-c", code, str(Path.cwd()), str(root))
            .cwd(resolve_path(root))
        )
        with checkout._transition(root):

            def compete() -> None:
                with (
                    pytest.raises(PermissionError, match="transition in progress"),
                    checkout._transition(root),
                ):
                    pytest.fail("Thread acquired a competing descriptor")

            with ThreadPoolExecutor(max_workers=1) as pool:
                pool.submit(compete).result()
            child = await CommandExecutor().execute(command)
            assert not child.failed
            assert child.stdout.strip() == b"refused"
        child = await CommandExecutor().execute(command)
        assert not child.failed
        assert child.stdout.strip() == b"entered"
        with checkout._transition(root):
            assert (root / ".local/backlog/checkout.lock").is_file()

    asyncio.run(run())

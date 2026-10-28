# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- independent literal machine-readable contracts
"""Real Git machine output and malformed/framing controls."""

from __future__ import annotations

import asyncio
import sys
from dataclasses import replace
from typing import TYPE_CHECKING, cast

import pytest

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands.availability import discover_executable
from devtools.tools import ToolRunner
from devtools.tools.errors import ToolInputError
from devtools.tools.repository import git as git_owner
from devtools.tools.repository.git import (
    GitInspectionError,
    GitInspectionTool,
    parse_porcelain,
)
from tests.tools.repository.fixtures import MODULE, ORIGIN, git, repository

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

    from devtools.resources.commands import Command, CommandExecution


def test_git_text_encoding_failure_is_a_domain_error(tmp_path: Path) -> None:
    async def run() -> None:
        _revision, scope = await repository(tmp_path)
        tool = GitInspectionTool(scope.root, origin=ORIGIN)
        actual = tool.executor.start

        def broken(command: Command) -> CommandExecution:
            return actual(
                replace(
                    command,
                    executable=sys.executable,
                    arguments=(
                        "-I",
                        "-c",
                        "import sys;sys.stdout.buffer.write(b'\\xff')",
                    ),
                ),
            )

        tool.executor.start = broken  # type: ignore[method-assign]
        with pytest.raises(GitInspectionError, match="encoding"):
            await ToolRunner().execute(tool, None)

    asyncio.run(run())


def test_missing_git_capability_never_enters_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tool = GitInspectionTool(resolve_path(tmp_path), origin=ORIGIN)
    absent = discover_executable("devtools-impossible-git-731f")
    monkeypatch.setattr(git_owner, "discover_executable", lambda _name: absent)
    with pytest.raises(GitInspectionError, match="unavailable"):
        asyncio.run(ToolRunner().execute(tool, None))
    assert tool.observations == []


def test_retained_git_observations_are_bounded(tmp_path: Path) -> None:
    async def run() -> None:
        _revision, scope = await repository(tmp_path)
        tool = GitInspectionTool(scope.root, origin=ORIGIN)
        for _ in range(25):
            assert (await ToolRunner().execute(tool, None)).stable
        with pytest.raises(GitInspectionError, match="bound"):
            await ToolRunner().execute(tool, None)
        assert len(tool.observations) == 128
        assert len({o.origin for o in tool.observations}) == 128

    asyncio.run(run())


def test_literal_names_and_rename_direction() -> None:
    result = parse_porcelain(
        b"M  staged name\0 M tab\tline\nname\0"
        b'?? quote"\\name\0R  dest\0original\0!! ignored\0',
    )
    assert [(x.path, x.index, x.worktree) for x in result[:3]] == [
        ("staged name", "M", " "),
        ("tab\tline\nname", " ", "M"),
        ('quote"\\name', "?", "?"),
    ]
    assert result[2].untracked
    assert not result[0].untracked
    assert result[3].path == "dest"
    assert result[3].original_path == "original"
    assert not result[4].untracked
    assert parse_porcelain(b"") == ()
    assert parse_porcelain(b"UU conflict\0")[0].unmerged
    assert not result[0].unmerged


@pytest.mark.parametrize(
    "data",
    [
        b" M a",
        b"\0",
        b"abc\0",
        b"ZZ name\0",
        b"   name\0",
        b"?M name\0",
        b"!M name\0",
        b"?? \0",
        b"R  new\0",
        b"R  new\0\0",
        b" M a\0 M a\0",
        b" M \xff\0",
    ],
)
def test_malformed_or_partial_status_refuses(data: bytes) -> None:
    with pytest.raises(GitInspectionError):
        parse_porcelain(data)


def test_real_git_paths_and_unchanged_index(tmp_path: Path) -> None:
    async def run() -> None:
        root = tmp_path / "space π & [root]"
        revision, scope = await repository(root)
        before = await git(root, "ls-files", "--stage", "-z")
        index_bytes = (root / ".git/index").read_bytes()
        tool = GitInspectionTool(scope.root, origin=ORIGIN)
        result = await ToolRunner().execute(tool, None)
        assert result.root == scope.root
        assert result.revision == revision
        assert result.stable
        assert {c.path: (c.index, c.worktree) for c in result.changes} == {
            MODULE: ("M", " "),
            "notes [new].txt": ("?", "?"),
            "readme.txt": (" ", "M"),
        }
        assert await git(root, "ls-files", "--stage", "-z") == before
        assert (root / ".git/index").read_bytes() == index_bytes
        assert len(tool.observations) == 5
        assert all(x.entered is True and x.exit_code == 0 for x in tool.observations)

    asyncio.run(run())


@pytest.mark.parametrize(
    "fault",
    [
        "input",
        "missing-root",
        "different-root",
        "output",
        "revision",
        "malformed",
        "drift",
    ],
)
def test_public_inspection_faults(tmp_path: Path, fault: str) -> None:
    async def run() -> None:
        _revision, scope = await repository(tmp_path)
        tool = GitInspectionTool(
            scope.root,
            origin=ORIGIN,
            maximum_bytes=1 if fault == "output" else 1 << 20,
        )
        if fault == "missing-root":
            tool.root = resolve_path(tmp_path / "missing")
        actual = tool.executor.start
        calls = []

        def corrupted(command: Command) -> CommandExecution:
            calls.append(command)
            code = None
            if fault == "different-root" and "--show-toplevel" in command.arguments:
                code = "print(" + repr(str(tmp_path.parent)) + ")"
            elif fault == "revision" and "--verify" in command.arguments:
                code = "print('not-an-object')"
            elif fault == "malformed" and "status" in command.arguments:
                code = "print('broken status')"
            elif fault == "drift" and len(calls) == 5:
                code = "import sys;sys.stdout.buffer.write(b'?? later\\x00')"
            return actual(
                replace(
                    command,
                    executable=sys.executable,
                    arguments=("-I", "-c", code),
                )
                if code
                else command,
            )

        tool.executor.start = corrupted  # type: ignore[method-assign]
        if fault == "drift":
            assert not (await ToolRunner().execute(tool, None)).stable
        else:
            with pytest.raises((GitInspectionError, ToolInputError)):
                await ToolRunner().execute(
                    cast("Any", tool),
                    "foreign" if fault == "input" else None,
                )
        if fault in {"input", "missing-root"}:
            assert calls == []

    asyncio.run(run())


@pytest.mark.parametrize("name", ["", " ", "x\x00y"])
def test_invalid_discovery(name: str) -> None:
    with pytest.raises(ValueError, match="Executable"):
        discover_executable(name)


def test_native_executable_discovery() -> None:
    assert discover_executable(sys.executable).path == resolve_path(sys.executable)
    assert discover_executable("devtools-impossible-executable-827c").path is None


@pytest.mark.parametrize("fault", ["time", "bytes", "origin"])
def test_inspection_bounds(tmp_path: Path, fault: str) -> None:
    with pytest.raises(ValueError, match="positive"):
        GitInspectionTool(
            resolve_path(tmp_path),
            origin=replace(ORIGIN, call="a" * 100) if fault == "origin" else ORIGIN,
            timeout=Duration.seconds(0 if fault == "time" else 1),
            maximum_bytes=0 if fault == "bytes" else 1024,
        )

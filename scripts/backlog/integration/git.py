# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- concrete integration Git checks
"""Git-native ancestry, exact-tree checks and compare-and-swap publication."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor
from scripts.backlog.coordinator import git

if TYPE_CHECKING:
    from pathlib import Path


async def remote_head(root: Path, remote: str, branch: str) -> str:
    """Observe one exact remote ref; absence is distinct from communication failure."""
    value = await git(root, "ls-remote", "--refs", remote, "refs/heads/" + branch)
    if not value:
        return ""
    rows = value.splitlines()
    if len(rows) != 1 or rows[0].split()[1] != "refs/heads/" + branch:
        raise ValueError("Ambiguous destination ref")
    return rows[0].split()[0]


async def blob(root: Path, revision: str, path: str) -> str:
    """Read Git source bytes without the administrative helper's whitespace trim."""
    result = await CommandExecutor().execute(
        Command("git")
        .args("show", revision + ":" + path)
        .cwd(resolve_path(root))
        .with_timeout(Duration.seconds(30))
    )
    if result.failed or result.stdout_truncated:
        raise ValueError("Cannot authenticate destination source")
    return result.stdout.decode("utf-8")


async def clean(root: Path) -> None:
    """Require a clean index and worktree without discarding anything."""
    if await git(root, "status", "--porcelain", "--untracked-files=no"):
        raise PermissionError("Integration checkout is not clean")


async def publish(
    root: Path, remote: str, branch: str, commit: str, expected: str
) -> None:
    """Push only an exact expected ref; replay of the same commit is idempotent."""
    current = await remote_head(root, remote, branch)
    if current == commit:
        return
    if current != expected:
        raise PermissionError("Remote advanced; replan/review instead of overwriting")
    await git(
        root,
        "push",
        "--porcelain",
        "--force-with-lease=refs/heads/" + branch + ":" + expected,
        remote,
        commit + ":refs/heads/" + branch,
    )
    if await remote_head(root, remote, branch) != commit:
        raise ValueError("Publication completion unknown; reconcile exact remote ref")

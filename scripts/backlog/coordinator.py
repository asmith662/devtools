# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812 -- repository-local single-writer boundary
"""Bind authoritative backlog writes to one checkout via shared local Git config."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

KEY = "devtools.backlogCoordinator"


async def git(root: Path, *arguments: str, missing_ok: bool = False) -> str:
    """Run bounded repository administration through canonical managed commands."""
    result = await CommandExecutor().execute(
        Command("git")
        .args(*arguments)
        .cwd(resolve_path(root))
        .with_timeout(Duration.seconds(30))
    )
    if missing_ok and result.exit_code == 1:
        return ""
    if result.failed or result.stdout_truncated or result.stderr_truncated:
        raise ValueError("Git inspection failed: " + " ".join(arguments))
    return result.stdout.decode("utf-8").strip()


async def common_directory(root: Path) -> Path:
    """Use Git's own worktree/common-directory resolution, never parse gitfiles."""
    return resolve_path(
        await git(root, "rev-parse", "--git-common-dir"), base_directory=root
    ).value


async def locate(root: Path) -> Path:
    """Require one existing designated checkout in the same Git repository."""
    value = await git(root, "config", "--local", "--get-all", KEY)
    if "\n" in value:
        raise ValueError("Multiple coordinators are configured")
    path = resolve_path(value).value
    if resolve_path(await git(path, "rev-parse", "--show-toplevel")).value != path:
        raise ValueError("Coordinator is not an exact Git checkout root")
    if await common_directory(root) != await common_directory(path):
        raise ValueError("Coordinator and target belong to different repositories")
    return path


async def designate(root: Path, *, authorize: Callable[[dict[str, Any]], bool]) -> Path:
    """Designate once under explicit host authority; never silently relocate it."""
    root = resolve_path(root).value
    if resolve_path(await git(root, "rev-parse", "--show-toplevel")).value != root:
        raise ValueError("Coordinator must be an exact checkout root")
    configured = await git(root, "config", "--local", "--get-all", KEY, missing_ok=True)
    if configured:
        if "\n" in configured:
            raise ValueError("Multiple coordinators are configured")
        if resolve_path(configured).value != root:
            raise PermissionError("A different coordinator is already designated")
        return await locate(root)
    request = {
        "operation": "designate-backlog-coordinator",
        "checkout": str(root),
        "common_git_directory": str(await common_directory(root)),
        "scope": "backlog administration only; no implementation grant",
    }
    if not authorize(request):
        raise PermissionError("Host authorization required for coordinator designation")
    await git(root, "config", "--local", KEY, str(root))
    return await locate(root)

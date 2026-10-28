# Copyright (c) 2026
"""Independently authored repositories and literal host-fixed checks."""

from __future__ import annotations

import asyncio
import sys
from typing import TYPE_CHECKING

from devtools.context import Repository, RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.observability.commands.models import CommandOrigin, CommandPattern
from devtools.resources.commands import Command, CommandExecutor
from devtools.resources.filesystem import TextFile, write
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from devtools.tools.repository.validation import (
    ChangeValidationPlan,
    CheckSelection,
    InspectAndValidateTool,
)
from devtools.tools.source import SourceScope

if TYPE_CHECKING:
    from pathlib import Path

SOURCE = "VALUE = 7\n"
MODULE = "module π & [x].py"
ORIGIN = CommandOrigin("independent", "authored-change", "run-1", "inspect")
CHECK = (
    "from pathlib import Path; import os,sys; assert "
    "os.environ['HOST_FIXED_TEST']=='PRIVATE_SENTINEL'; assert 'VALUE "
    "= 7' in Path(sys.argv[1]).read_text(encoding='utf-8'); "
    "p=Path('.local/count'); p.write_text(p.read_text()+'x' if "
    "p.exists() else 'x'); print('verified:7'); "
    "print('PRIVATE_SENTINEL')"
)


async def git(root: Path, *args: str) -> str:
    """Use the real managed subprocess owner for tiny authored fixture Git only."""
    result = await CommandExecutor().execute(
        Command("git")
        .args(*args)
        .cwd(resolve_path(root))
        .with_timeout(Duration.seconds(15)),
    )
    assert result.exit_code == 0, result.stderr.decode(errors="replace")
    return result.stdout.decode("utf-8").strip()


async def repository(root: Path) -> tuple[str, SourceScope]:
    """Create staged, unstaged and untracked literal paths without a project copy."""
    await asyncio.to_thread(root.mkdir, parents=True, exist_ok=True)
    for path, content in [
        (MODULE, "VALUE = 6\n"),
        ("readme.txt", "old\n"),
        (".gitignore", ".local/\n"),
    ]:
        write(TextFile(resolve_path(root / path), content))
    await git(root, "init", "-q", "-b", "main")
    await git(root, "config", "core.autocrlf", "false")
    await git(root, "add", "--", MODULE, "readme.txt", ".gitignore")
    await git(
        root,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-qm",
        "Authored procedure fixture",
    )
    revision = await git(root, "rev-parse", "HEAD")
    write(TextFile(resolve_path(root / MODULE), SOURCE))
    await git(root, "add", "--", MODULE)
    write(TextFile(resolve_path(root / "readme.txt"), "changed\n"))
    write(TextFile(resolve_path(root / "notes [new].txt"), "note\n"))
    (root / ".local").mkdir()
    scope = SourceScope.observe(
        root=resolve_path(root),
        repository=Repository.new(),
        addresses=(RepositoryResourceAddress(MODULE),),
    )
    return revision, scope


def procedure(  # noqa: PLR0913 -- explicit authored scope and fixed-check policy
    root: Path,
    revision: str,
    scope: SourceScope,
    *,
    code: str = CHECK,
    extra: bool = False,
    stop: bool = True,
) -> InspectAndValidateTool:
    """Bind an exact command/environment and deterministic applicability policy."""
    assert resolve_path(root) == scope.root
    command = (
        Command(sys.executable)
        .args("-I", "-B", "-c", code, MODULE)
        .cwd(scope.root)
        .with_timeout(Duration.seconds(5))
        .with_environment({"HOST_FIXED_TEST": "PRIVATE_SENTINEL"})
    )
    checks: tuple[FixedCheck, ...] = (FixedCheck("behavior", command),)
    if extra:
        checks += (FixedCheck("second", command),)
    plan = FixedCheckPlan(scope.root, checks, scope)
    selected = tuple(
        CheckSelection(
            c.name,
            frozenset(),
            CommandPattern(
                "check",
                c.name,
                ("script", "path"),
                ("python", sys.platform),
                "tools.checks.FixedCheckTool",
            ),
        )
        for c in checks
    )
    return InspectAndValidateTool(
        ChangeValidationPlan(
            plan,
            revision,
            frozenset(
                RepositoryResourceAddress(p)
                for p in (MODULE, "readme.txt", "notes [new].txt")
            ),
            selected,
            frozenset({"HOST_FIXED_TEST"}),
            stop,
        ),
        origin=ORIGIN,
    )

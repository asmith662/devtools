# Copyright (c) 2026
# ruff: noqa: INP001 -- repository developer entrypoint
"""Check root ownership and authenticate ordinary/linked Git metadata read-only."""

from __future__ import annotations

import asyncio
from pathlib import Path

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor


def _valid_git_entry(root: Path) -> bool:
    """Ask Git to resolve metadata, including a linked worktree's gitfile."""
    entry = root / ".git"
    if entry.is_symlink():
        return False
    result = asyncio.run(
        CommandExecutor().execute(
            Command("git")
            .args(
                "--no-optional-locks",
                "rev-parse",
                "--show-toplevel",
                "--is-inside-work-tree",
            )
            .cwd(resolve_path(root.resolve()))
            .with_timeout(Duration.seconds(10)),
        ),
    )
    values = result.stdout.decode("utf-8", errors="replace").splitlines()
    return (
        result.succeeded
        and len(values) == len(("root", "inside_work_tree"))
        and Path(values[0]).resolve() == root.resolve()
        and values[1] == "true"
    )


DIRECTORIES = frozenset(
    {
        ".git",
        ".local",
        ".venv",
        ".devtools",
        ".idea",
        ".vscode",
        ".agents",
        ".codex",
        ".aws",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".uv-cache-audit",
        "__pycache__",
        "htmlcov",
        "build",
        "dist",
        "apps",
        "src",
        "tests",
        "scripts",
        "docs",
        "experiments",
        "codex-handoff",
    },
)
FILES = frozenset(
    {
        "AGENTS.md",
        "README.md",
        "pyproject.toml",
        "uv.lock",
        ".gitignore",
        ".gitattributes",
        ".coverage",
        ".git",
    },
)


def violations(root: Path) -> list[str]:
    """Return unexpected root entries and forbidden secondary-checkout storage."""
    problems = [
        f"Unexpected root resource: {entry.name}"
        for entry in sorted(root.iterdir())
        if entry.name not in (DIRECTORIES if entry.is_dir() else FILES)
    ]
    if (root / ".local/worktrees").exists():
        problems.append("Secondary Devtools checkout storage: .local/worktrees")
    if (root / ".git").exists() and not _valid_git_entry(root):
        problems.append("Invalid Git repository metadata: .git")
    return problems


def main() -> int:
    """Report root-layout violations; zero means this bounded check passed."""
    problems = violations(Path(__file__).resolve().parents[1])
    for problem in problems:
        print(problem)  # noqa: T201 -- developer command
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())

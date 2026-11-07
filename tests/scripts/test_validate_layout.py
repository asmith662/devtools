# Copyright (c) 2026
"""The hygiene check rejects stray files without deleting user data."""

import asyncio
from pathlib import Path

from devtools.core.paths import resolve_path
from devtools.resources.commands import Command, CommandExecutor
from scripts.validate_layout import violations


def test_supported_layout_and_unexpected_resources(tmp_path: Path) -> None:
    """Supported roots pass, while miscellaneous root files are reported."""
    (tmp_path / "apps").mkdir()
    (tmp_path / "README.md").write_text("project")
    assert violations(tmp_path) == []
    (tmp_path / "scratch.py").write_text("private = True")
    assert violations(tmp_path) == ["Unexpected root resource: scratch.py"]
    assert (tmp_path / "scratch.py").read_text() == "private = True"


def test_worktree_storage_is_rejected(tmp_path: Path) -> None:
    """Ignored state does not excuse additional physical checkouts."""
    (tmp_path / ".local/worktrees").mkdir(parents=True)
    assert violations(tmp_path) == [
        "Secondary Devtools checkout storage: .local/worktrees",
    ]


def _git(root: Path, *arguments: str) -> None:
    result = asyncio.run(
        CommandExecutor().execute(
            Command("git").args(*arguments).cwd(resolve_path(root)),
        ),
    )
    assert result.succeeded, result.stderr


def test_normal_and_linked_git_metadata(tmp_path: Path) -> None:
    """Only tiny authored repositories are created; no Devtools source is copied."""
    source = tmp_path / "source"
    source.mkdir()
    _git(source, "init")
    _git(
        source,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "--allow-empty",
        "-m",
        "fixture",
    )
    assert violations(source) == []
    linked = tmp_path / "linked"
    _git(source, "worktree", "add", "-b", "fixture-linked", str(linked))
    assert (linked / ".git").is_file()
    assert violations(linked) == []


def test_invalid_git_file_and_directory(tmp_path: Path) -> None:
    """An arbitrary gitfile or empty metadata directory is not a repository."""
    entry = tmp_path / ".git"
    entry.write_text("gitdir: missing\n")
    assert violations(tmp_path) == ["Invalid Git repository metadata: .git"]
    entry.unlink()
    entry.mkdir()
    assert violations(tmp_path) == ["Invalid Git repository metadata: .git"]

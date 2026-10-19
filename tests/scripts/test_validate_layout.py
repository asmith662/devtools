# Copyright (c) 2026
"""The hygiene check rejects stray files without deleting user data."""

from pathlib import Path

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

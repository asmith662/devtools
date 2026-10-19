# Copyright (c) 2026
# ruff: noqa: INP001 -- repository developer entrypoint
"""Check canonical root ownership without modifying files or invoking Git."""

from __future__ import annotations

from pathlib import Path

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
    return problems


def main() -> int:
    """Report root-layout violations; zero means this bounded check passed."""
    problems = violations(Path(__file__).resolve().parents[1])
    for problem in problems:
        print(problem)  # noqa: T201 -- developer command
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())

# Copyright (c) 2026
# ruff: noqa: INP001
"""Run the repository's protected ordinary development test profile."""

from __future__ import annotations

from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def pytest_arguments(repository_root: Path = REPOSITORY_ROOT) -> list[str]:
    """Select ordinary tests while excluding the retained experiment tree."""
    tests = repository_root / "tests"
    experiments = tests / "experiments"
    return [str(tests), f"--ignore={experiments}"]


def main() -> int:
    """Run pytest and return its exit code unchanged."""
    return int(pytest.main(pytest_arguments()))


if __name__ == "__main__":
    raise SystemExit(main())

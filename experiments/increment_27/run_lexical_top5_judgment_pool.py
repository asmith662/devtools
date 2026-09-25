# Copyright (c) 2026
# ruff: noqa: T201
"""Freeze the Increment-27 top-five neutral lexical judgment population."""

from __future__ import annotations

from pathlib import Path

from experiments.increment_27.lexical_top5_judgment_pool import write_top5_artifacts


def main() -> None:
    """Write pool artifacts from persisted comparison rankings only."""
    repository_root = Path(__file__).resolve().parents[2]
    identities = write_top5_artifacts(experiment_root=repository_root / "experiments")
    for name, identity in identities.items():
        print(f"{name}: {identity}")


if __name__ == "__main__":
    main()

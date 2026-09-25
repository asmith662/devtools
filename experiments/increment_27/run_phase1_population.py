# Copyright (c) 2026
# ruff: noqa: T201
"""Freeze the Increment-27 development-only top-50 judgment population."""

from __future__ import annotations

from pathlib import Path

from experiments.increment_27.phase1_population import write_phase1_artifacts


def main() -> None:
    """Build artifacts from saved rankings without running retrieval."""
    repository_root = Path(__file__).resolve().parents[2]
    identities = write_phase1_artifacts(experiment_root=repository_root / "experiments")
    for name, identity in identities.items():
        print(f"{name}: {identity}")


if __name__ == "__main__":
    main()

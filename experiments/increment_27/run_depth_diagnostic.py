# Copyright (c) 2026
"""Execute the Increment-27 development-only lexical-depth diagnostic."""

from __future__ import annotations

from pathlib import Path

from experiments.increment_27.depth_diagnostic import run_diagnostic


def main() -> None:
    """Run exactly the frozen 24-case development population."""
    repository_root = Path(__file__).resolve().parents[2]
    experiment_root = repository_root / "experiments"
    output_root = Path(__file__).resolve().parent
    run_diagnostic(
        repository_root=repository_root,
        experiment_root=experiment_root,
        output_root=output_root,
    )


if __name__ == "__main__":
    main()

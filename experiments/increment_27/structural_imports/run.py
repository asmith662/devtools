# Copyright (c) 2026
"""Freeze, generate, then audit direct-import candidate cost in that order."""

from __future__ import annotations

import argparse
from pathlib import Path

from experiments.increment_27.structural_imports.analysis import write_results
from experiments.increment_27.structural_imports.cost import write_cost
from experiments.increment_27.structural_imports.mechanics import (
    freeze_protocol,
    run_mechanics,
)
from experiments.increment_27.structural_imports.population import write_population


def main() -> None:
    """Execute one explicitly requested, development-only checkpoint."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "phase", choices=("freeze", "mechanics", "cost", "population", "analysis"),
    )
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repository_root = args.repository_root.resolve()
    root = repository_root / "experiments" / "increment_27"
    if args.phase == "freeze":
        freeze_protocol(root)
    elif args.phase == "mechanics":
        run_mechanics(repository_root=repository_root, root=root)
    elif args.phase == "cost":
        write_cost(root)
    elif args.phase == "population":
        write_population(root)
    else:
        write_results(root)


if __name__ == "__main__":
    main()

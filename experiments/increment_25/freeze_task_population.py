# Copyright (c) 2026
"""Write the one approved Increment-25 task-population freeze artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from experiments.increment_25.task_population import (
    FREEZE_CHECKPOINT,
    build_freeze,
    collect_git_population,
    validate_freeze,
)


def main() -> None:
    """Collect Git-only metadata and write a validated, result-free freeze."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parsed = parser.parse_args()
    freeze = build_freeze(
        commits=collect_git_population(parsed.repository_root),
        checkpoint=FREEZE_CHECKPOINT,
    )
    if not validate_freeze(freeze):
        msg = "Refusing to write an invalid or outcome-bearing freeze artifact."
        raise RuntimeError(msg)
    parsed.output.write_text(
        json.dumps(freeze, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()

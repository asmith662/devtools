# Copyright (c) 2026
"""Execute all and only frozen Increment-25 development cases."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING

from experiments.increment_25.development import run_development, write_artifact

if TYPE_CHECKING:
    from collections.abc import Sequence


def parse_arguments(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse a development-only CLI with no confirmation/reserve mode."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--freeze",
        type=Path,
        default=Path("experiments/increment_25/task_population_freeze.json"),
    )
    parser.add_argument("--candidate-output", type=Path, required=True)
    parser.add_argument("--judgment-output", type=Path, required=True)
    return parser.parse_args(arguments)


def main(arguments: Sequence[str] | None = None) -> None:
    """Generate candidate evidence and a separately blinded judgment input."""
    parsed = parse_arguments(arguments)
    candidates, judgment = run_development(
        repository_root=parsed.repository_root,
        freeze_path=parsed.freeze,
    )
    write_artifact(path=parsed.candidate_output, payload=candidates)
    write_artifact(path=parsed.judgment_output, payload=judgment)


if __name__ == "__main__":
    main()

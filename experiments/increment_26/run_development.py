# Copyright (c) 2026
"""Execute only the frozen Increment-26 development partition."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING

from experiments.increment_26.development import run_development, write_artifact

if TYPE_CHECKING:
    from collections.abc import Sequence


def parse_arguments(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse a development-only command with no sealed-partition selector."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--increment-25-freeze",
        type=Path,
        default=Path("experiments/increment_25/task_population_freeze.json"),
    )
    parser.add_argument(
        "--increment-26-freeze",
        type=Path,
        default=Path("experiments/increment_26/experiment_freeze.json"),
    )
    parser.add_argument("--candidate-output", type=Path, required=True)
    parser.add_argument("--judgment-output", type=Path, required=True)
    parser.add_argument("--model-cache", type=Path)
    parser.add_argument(
        "--offline",
        action="store_true",
        help=(
            "Resolve the exact pinned model revision from the local Hugging Face "
            "cache only."
        ),
    )
    return parser.parse_args(arguments)


def main(arguments: Sequence[str] | None = None) -> None:
    """Write development evidence and blinded resources, without adjudication."""
    parsed = parse_arguments(arguments)
    evidence, judgment = run_development(
        repository_root=parsed.repository_root,
        increment_25_freeze_path=parsed.increment_25_freeze,
        increment_26_freeze_path=parsed.increment_26_freeze,
        cache_dir=parsed.model_cache,
        offline=parsed.offline,
    )
    write_artifact(path=parsed.candidate_output, payload=evidence)
    write_artifact(path=parsed.judgment_output, payload=judgment)


if __name__ == "__main__":
    main()

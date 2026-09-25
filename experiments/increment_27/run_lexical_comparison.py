# Copyright (c) 2026
"""Freeze, execute, or analyze the Increment-27 lexical development comparison."""

from __future__ import annotations

import argparse
from pathlib import Path

from experiments.increment_27.lexical_analysis import analyze_comparison
from experiments.increment_27.lexical_comparison import (
    freeze_comparison,
    run_comparison,
)


def main() -> None:
    """Require a distinct stage so labels cannot inform configuration or ranking."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("freeze", "rank", "analyze"))
    stage = parser.parse_args().stage
    repository_root = Path(__file__).resolve().parents[2]
    output_root = Path(__file__).resolve().parent
    if stage == "freeze":
        freeze_comparison(output_root=output_root)
    elif stage == "rank":
        run_comparison(repository_root=repository_root, output_root=output_root)
    else:
        analyze_comparison(output_root=output_root)


if __name__ == "__main__":
    main()

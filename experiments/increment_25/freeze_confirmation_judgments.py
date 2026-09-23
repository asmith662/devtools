# Copyright (c) 2026
"""Freeze completed Increment-25 confirmation judgments while still blinded."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import TYPE_CHECKING, cast

from experiments.increment_25.confirmation_judgments import (
    freeze_confirmation_judgments,
    write_json,
)

if TYPE_CHECKING:
    from collections.abc import Sequence


def main(arguments: Sequence[str] | None = None) -> None:
    """Read origin-hidden decisions and persist their immutable freeze."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blinded", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--frozen-output", type=Path, required=True)
    parser.add_argument("--mapping-output", type=Path, required=True)
    parsed = parser.parse_args(arguments)
    blinded = cast(
        "dict[str, object]",
        json.loads(parsed.blinded.read_text(encoding="utf-8")),
    )
    decisions = cast(
        "dict[str, object]",
        json.loads(parsed.decisions.read_text(encoding="utf-8")),
    )
    frozen, mapping = freeze_confirmation_judgments(
        blinded=blinded,
        decisions=decisions,
    )
    write_json(path=parsed.frozen_output, value=frozen)
    write_json(path=parsed.mapping_output, value=mapping)


if __name__ == "__main__":
    main()

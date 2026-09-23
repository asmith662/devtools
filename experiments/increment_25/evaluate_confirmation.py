# Copyright (c) 2026
"""Unblind frozen Increment-25 confirmation judgments and calculate results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import TYPE_CHECKING, cast

from experiments.increment_25.confirmation_judgments import (
    evaluate_confirmation,
    write_json,
)

if TYPE_CHECKING:
    from collections.abc import Sequence


def _load(path: Path) -> dict[str, object]:
    return cast("dict[str, object]", json.loads(path.read_text(encoding="utf-8")))


def main(arguments: Sequence[str] | None = None) -> None:
    """Join only validated frozen judgments to retained candidate origins."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--blinded", type=Path, required=True)
    parser.add_argument("--frozen", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parsed = parser.parse_args(arguments)
    result = evaluate_confirmation(
        candidates=_load(parsed.candidates),
        blinded=_load(parsed.blinded),
        frozen=_load(parsed.frozen),
        mapping=_load(parsed.mapping),
    )
    write_json(path=parsed.output, value=result)


if __name__ == "__main__":
    main()

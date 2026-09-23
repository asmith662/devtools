# Copyright (c) 2026
"""Write the Increment-26 pre-outcome configuration freeze only."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from experiments.increment_26.configuration import build_freeze, validate_freeze

if TYPE_CHECKING:
    from pathlib import Path


def write_freeze(*, increment_25_freeze_path: Path, output_path: Path) -> None:
    """Serialize configuration without loading an encoder or retrieval corpus."""
    freeze = build_freeze(increment_25_freeze_path=increment_25_freeze_path)
    if not validate_freeze(freeze):
        msg = "Refusing to write an invalid or outcome-bearing Increment-26 freeze."
        raise ValueError(msg)
    output_path.write_text(
        json.dumps(freeze, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

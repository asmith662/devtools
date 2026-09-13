# Copyright (c) 2026
"""Model-facing input for one model interaction."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Prompt:
    """Represent the currently supported single text chat input."""

    content: str
    role: str

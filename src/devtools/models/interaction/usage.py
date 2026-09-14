# Copyright (c) 2026
"""Provider-reported usage for one completed model interaction."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelUsage:
    """Retain optional provider-reported token counts without estimating them."""

    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None

    def __post_init__(self) -> None:
        """Reject impossible token counts while allowing partial provider reports."""
        for value, label in (
            (self.input_tokens, "Input token count"),
            (self.output_tokens, "Output token count"),
            (self.total_tokens, "Total token count"),
        ):
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int)
            ):
                msg = f"{label} must be an integer when supplied."
                raise TypeError(msg)
            if value is not None and value < 0:
                msg = f"{label} cannot be negative."
                raise ValueError(msg)

# Copyright (c) 2026
"""Coding request capacity and pressure facts, independent of provider adapters."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TokenCapacity:
    """Qualified provider capacity with explicit input and generation reservations.

    The host supplies a tokenizer measurement; bytes never estimate tokens.
    Unallocated tokens are a deliberate safety margin, not usable input capacity.
    """

    context_tokens: int
    input_tokens: int
    reserved_output_tokens: int

    def __post_init__(self) -> None:
        """Reject incompatible or nonfinite dimensions before request entry."""
        if (
            any(
                type(v) is not int or v <= 0
                for v in (
                    self.context_tokens,
                    self.input_tokens,
                    self.reserved_output_tokens,
                )
            )
            or self.input_tokens + self.reserved_output_tokens > self.context_tokens
        ):
            msg = "Input and output reservations exceed qualified token capacity."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class ContextPressure:
    """Presentation facts for one preparation; neither source nor approval.

    Observer consumers may persist these facts through their existing writer.
    A missing token count is unknown, not a byte-derived estimate.
    """

    original_bytes: int
    request_bytes: int
    ceiling_bytes: int
    warning_bytes: int
    warning: bool
    policy: str
    action: str
    measured_input_tokens: int | None
    token_capacity: TokenCapacity | None

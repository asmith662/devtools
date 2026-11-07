# Copyright (c) 2026
"""Concrete regression envelopes, separate from mathematical method settings."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegressionLimits:
    """Retain the declared RegressionLimits scientific values and invariants."""

    population_rows: int
    training_rows: int
    prediction_rows: int
    features: int
    training_cells: int
    distance_operations: int
    state_bytes: int
    text_bytes: int
    prediction_bytes: int


REGRESSION_V1 = RegressionLimits(512, 256, 128, 16, 4096, 2000000, 0, 0, 0)
REGRESSION_V2 = RegressionLimits(
    2048,
    2048,
    2048,
    16,
    32768,
    8000000,
    4 * 1024 * 1024,
    256 * 1024,
    8 * 1024 * 1024,
)
MAXIMUM_V2_SOURCE_ROWS = 4096


def version_limits(version: str, family: str) -> RegressionLimits:
    """Apply the explicit version limits contract within this owner."""
    if version == family + "-v1":
        return REGRESSION_V1
    if version == family + "-v2":
        return REGRESSION_V2
    msg = "unsupported explicit regression capacity version"
    raise ValueError(msg)


def check_text(values: tuple[str | None, ...]) -> None:
    """Apply the explicit check text contract within this owner."""
    if (
        sum(len(v.encode("utf-8")) for v in values if v is not None)
        > REGRESSION_V2.text_bytes
    ):
        msg = "bounded regression identity/schema text required"
        raise ValueError(msg)


def prediction_byte_bound(
    rows: tuple[str, ...],
    training_rows: tuple[str, ...],
    descriptions: tuple[str | None, ...],
    *,
    neighbors: bool,
) -> int:
    """Conservative canonical JSON bound, including repeated neighbor identities."""
    text = sum(len(s.encode("utf-8")) for s in (*rows, *descriptions) if s is not None)
    if neighbors:
        text += len(rows) * sum(
            sorted(len(s.encode("utf-8")) for s in training_rows)[-5:],
        )
    return text * 6 + len(rows) * 256 + 16384

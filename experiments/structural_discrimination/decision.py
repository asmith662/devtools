# Copyright (c) 2026
# ruff: noqa: EM101, TRY003 -- prospective ordinal diagnostic contract
"""Future blind-label local diagnostics; no ranking or production verdict."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Label(Enum):
    """Blind obligation-relative label vocabulary, ordered without scores."""

    REQUIRED = "REQUIRED"
    HELPFUL_ONLY = "HELPFUL_ONLY"
    UNNECESSARY = "UNNECESSARY"


UTILITY_ORDER = (Label.REQUIRED, Label.HELPFUL_ONLY, Label.UNNECESSARY)


@dataclass(frozen=True, slots=True)
class PairClassification:
    """A local directional diagnostic; no promotion has taken place."""

    direction: str
    strong_beneficial: bool
    strong_harmful: bool


def classify_pair(target: Label, predecessor: Label) -> PairClassification:
    """Compare ordinal categories only, never calculate a relevance score."""
    if not isinstance(target, Label) or not isinstance(predecessor, Label):
        raise TypeError("Unknown/unresolved blind label")
    target_position, predecessor_position = (
        UTILITY_ORDER.index(target),
        UTILITY_ORDER.index(predecessor),
    )
    direction = (
        "NEUTRAL"
        if target_position == predecessor_position
        else "BENEFICIAL"
        if target_position < predecessor_position
        else "HARMFUL"
    )
    return PairClassification(
        direction,
        target is Label.REQUIRED and predecessor is Label.UNNECESSARY,
        target is Label.UNNECESSARY and predecessor is Label.REQUIRED,
    )


def case_category(strong_beneficial: int, strong_harmful: int) -> str:
    """Apply the exact four prospective case categories, after contract checks."""
    if any(type(n) is not int or n < 0 for n in (strong_beneficial, strong_harmful)):
        raise ValueError("Counts must be nonnegative integers")
    if strong_beneficial and strong_harmful:
        return "MIXED_STRUCTURAL_DISCRIMINATION_SIGNAL"
    if strong_harmful:
        return "STRUCTURAL_DISCRIMINATION_CONTRADICTED"
    if strong_beneficial:
        return "STRUCTURAL_DISCRIMINATION_SIGNAL"
    return "NO_MATERIAL_STRUCTURAL_DISCRIMINATION_SIGNAL"

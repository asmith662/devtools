# Copyright (c) 2026
"""Caller-authored information obligations and their minimal witness algebra."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Hashable

    from devtools.context.localization.identity import (
        LocalizationAnchorIdentity,
        LocalizationObligationIdentity,
        TaskProvenance,
    )


class RequirementStatus(StrEnum):
    """Separate required task information from helpful information."""

    MANDATORY = "mandatory"
    HELPFUL = "helpful"


@dataclass(frozen=True, slots=True)
class SatisfactionCriterion:
    """Name a bounded rule for information satisfying an obligation."""

    name: str
    statement: str

    def __post_init__(self) -> None:
        """Require an explicit, human-readable criterion."""
        if not self.name.strip() or not self.statement.strip():
            msg = "Satisfaction criterion needs a name and statement."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class WitnessSet:
    """Describe information targets that must all be supported together."""

    members: tuple[Hashable, ...]

    def __post_init__(self) -> None:
        """Require distinct, hashable native or caller-owned target identities."""
        if not self.members:
            msg = "A witness set must contain at least one target."
            raise ValueError(msg)
        try:
            unique = set(self.members)
        except TypeError as error:
            msg = "Witness targets must be hashable identities."
            raise ValueError(msg) from error
        if len(unique) != len(self.members):
            msg = "A witness set must not repeat target identities."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class LocalizationObligation:
    """State what repository information must establish for one task."""

    identity: LocalizationObligationIdentity
    predicate: str
    anchors: tuple[LocalizationAnchorIdentity, ...]
    provenance: TaskProvenance
    requirement: RequirementStatus
    satisfaction: SatisfactionCriterion
    witness_alternatives: tuple[WitnessSet, ...]
    applicability_condition: str | None = None

    def __post_init__(self) -> None:
        """Keep scope, anchors, status, condition, and witness alternatives coherent."""
        if not self.predicate.strip():
            msg = "Localization obligation predicate must not be blank."
            raise ValueError(msg)
        if any(anchor.task != self.identity.task for anchor in self.anchors):
            msg = "Obligation anchors must belong to the same task."
            raise ValueError(msg)
        if len(set(self.anchors)) != len(self.anchors):
            msg = "Obligation must not repeat an anchor identity."
            raise ValueError(msg)
        if (
            self.applicability_condition is not None
            and not self.applicability_condition.strip()
        ):
            msg = "Applicability condition must not be blank when supplied."
            raise ValueError(msg)
        alternatives = [frozenset(item.members) for item in self.witness_alternatives]
        if len(set(alternatives)) != len(alternatives):
            msg = "Obligation must not repeat an equivalent witness alternative."
            raise ValueError(msg)

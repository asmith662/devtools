# Copyright (c) 2026
"""Immutable caller interpretations with shared task-local anchors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.context.localization.identity import (
        LocalizationAnchorIdentity,
        LocalizationTaskIdentity,
        TaskProvenance,
    )
    from devtools.context.localization.obligation import LocalizationObligation


@dataclass(frozen=True, slots=True)
class LocalizationAnchor:
    """Retain task text without claiming it resolves to a repository subject."""

    identity: LocalizationAnchorIdentity
    text: str
    provenance: TaskProvenance | None = None

    def __post_init__(self) -> None:
        """Require nonblank text for later caller-selected acquisition."""
        if not self.text.strip():
            msg = "Localization anchor text must not be blank."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class LocalizationTaskInterpretation:
    """Group explicit task anchors and obligations before selecting a snapshot."""

    identity: LocalizationTaskIdentity
    provenance: TaskProvenance
    anchors: tuple[LocalizationAnchor, ...]
    obligations: tuple[LocalizationObligation, ...]

    def __post_init__(self) -> None:
        """Validate deterministic task-local uniqueness and all anchor references."""
        anchor_ids = tuple(item.identity for item in self.anchors)
        obligation_ids = tuple(item.identity for item in self.obligations)
        if any(item.task != self.identity for item in anchor_ids) or any(
            item.task != self.identity for item in obligation_ids
        ):
            msg = "Task interpretation contains a foreign task-local identity."
            raise ValueError(msg)
        if len(set(anchor_ids)) != len(anchor_ids):
            msg = "Task interpretation contains duplicate anchor identities."
            raise ValueError(msg)
        if len(set(obligation_ids)) != len(obligation_ids):
            msg = "Task interpretation contains duplicate obligation identities."
            raise ValueError(msg)
        known_anchors = set(anchor_ids)
        if any(
            anchor not in known_anchors
            for obligation in self.obligations
            for anchor in obligation.anchors
        ):
            msg = "Obligation references an anchor outside its task interpretation."
            raise ValueError(msg)

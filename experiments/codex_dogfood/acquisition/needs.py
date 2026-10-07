# Copyright (c) 2026
"""Caller-authored experimental information purpose under one native obligation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.context.localization import (
        LocalizationAnchorIdentity,
        LocalizationObligationIdentity,
        TaskProvenance,
    )


@dataclass(frozen=True, slots=True)
class InformationNeed:
    """State what to learn, independently of query, evidence or accepted witness."""

    key: str
    obligation: LocalizationObligationIdentity
    statement: str
    reason: str
    provenance: TaskProvenance
    anchors: tuple[LocalizationAnchorIdentity, ...] = ()

    def __post_init__(self) -> None:
        """Validate task-local purpose without generating or routing anything."""
        if not all(s.strip() for s in (self.key, self.statement, self.reason)):
            msg = "Information need requires a key, statement and reason."
            raise ValueError(msg)
        if len(set(self.anchors)) != len(self.anchors) or any(
            a.task != self.obligation.task for a in self.anchors
        ):
            msg = "Information need anchors must be unique and in the owning task."
            raise ValueError(msg)

    @property
    def identity(self) -> str:
        """Retain a caller key in native task/obligation scope, without a UUID."""
        return f"{self.obligation.task.value}/{self.obligation.value}/{self.key}"

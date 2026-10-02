# Copyright (c) 2026
"""Stable caller-named identities and provenance for task interpretations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Hashable


@dataclass(frozen=True, slots=True)
class LocalizationTaskIdentity:
    """Identify a task interpretation using its caller-owned stable key."""

    value: str

    def __post_init__(self) -> None:
        """Reject empty task scope identities."""
        if not self.value.strip():
            msg = "Localization task identity must not be blank."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class LocalizationAnchorIdentity:
    """Name one task-local shared anchor without asserting repository identity."""

    task: LocalizationTaskIdentity
    value: str

    def __post_init__(self) -> None:
        """Reject empty local anchor keys."""
        if not self.value.strip():
            msg = "Localization anchor key must not be blank."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class LocalizationObligationIdentity:
    """Name one task-local information obligation."""

    task: LocalizationTaskIdentity
    value: str

    def __post_init__(self) -> None:
        """Reject empty local obligation keys."""
        if not self.value.strip():
            msg = "Localization obligation key must not be blank."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class TaskTextSpan:
    """Retain a caller-supplied half-open character span in task text."""

    start: int
    end: int

    def __post_init__(self) -> None:
        """Require a nonempty, nonnegative half-open interval."""
        if self.start < 0 or self.end <= self.start:
            msg = "Task text span must be a nonempty nonnegative interval."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class TaskProvenance:
    """Reference caller-owned task material without copying it into Localization."""

    source_identity: Hashable
    span: TaskTextSpan | None = None
    explanation: str | None = None

    def __post_init__(self) -> None:
        """Require a hashable source reference and useful optional explanation."""
        try:
            hash(self.source_identity)
        except TypeError as error:
            msg = "Task provenance source identity must be hashable."
            raise ValueError(msg) from error
        if self.explanation is not None and not self.explanation.strip():
            msg = "Task provenance explanation must not be blank when supplied."
            raise ValueError(msg)

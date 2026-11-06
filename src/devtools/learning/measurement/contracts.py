# Copyright (c) 2026
"""Immutable scalar measurement results and exact scientific evidence references."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from uuid import UUID


def nonempty(value: str) -> None:
    """Apply the explicit nonempty contract within this owner."""
    if type(value) is not str or not value.strip():
        msg = "measurement text identities/reasons must be nonempty"
        raise ValueError(msg)


def digest(value: str | None) -> None:
    """Apply the explicit digest contract within this owner."""
    if value is not None and (
        type(value) is not str or not re.fullmatch("[0-9a-f]{64}", value)
    ):
        msg = "measurement digest must be canonical SHA-256 or unknown"
        raise ValueError(msg)


class NonValueKind(Enum):
    """Retain the declared NonValueKind scientific values and invariants."""

    UNDEFINED = "undefined"
    NOT_APPLICABLE = "not_applicable"
    NOT_MEASURED = "not_measured"
    UNAVAILABLE = "unavailable"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True)
class Measured[V]:
    """A scalar result; the family operation and independent inspection establish meaning."""

    value: V


@dataclass(frozen=True, slots=True)
class NoValue:
    """Retain the declared NoValue scientific values and invariants."""

    kind: NonValueKind
    reason_code: str
    detail: str
    diagnostic_event_id: UUID | None = None

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.kind, NonValueKind):
            msg = "nonvalue kind must be explicit"
            raise TypeError(msg)
        nonempty(self.reason_code)
        nonempty(self.detail)
        if self.diagnostic_event_id is not None and (
            not isinstance(self.diagnostic_event_id, UUID)
        ):
            msg = "diagnostic reference must be a UUID or unknown"
            raise TypeError(msg)


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    """A named dependency/reference, with byte integrity when actually known."""

    relation: str
    identity: str
    sha256: str | None = None

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        nonempty(self.relation)
        nonempty(self.identity)
        digest(self.sha256)


def validate_references(values: tuple[EvidenceReference, ...]) -> None:
    """Validate immutable attributed references without inspecting their sources."""
    if type(values) is not tuple or any(
        not isinstance(value, EvidenceReference) for value in values
    ):
        msg = "references must be an immutable tuple of EvidenceReference"
        raise TypeError(msg)

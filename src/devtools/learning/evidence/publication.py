# Copyright (c) 2026
"""Small immutable publication contracts; filesystem/ledger mechanics live elsewhere."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from uuid import UUID, uuid5

from devtools.learning.evidence.events import Fact, _facts


def artifact_name(value: str) -> str:
    """Accept portable flat filenames, deliberately excluding nested paths/aliases."""
    if (
        not isinstance(value, str)
        or not re.fullmatch("[A-Za-z0-9][A-Za-z0-9._ -]{0,127}", value)
        or value != value.strip()
    ):
        msg = "artifact name must be a nonempty portable filename"
        raise ValueError(msg)
    if (
        value in (".", "..")
        or value.endswith((".", " "))
        or any(ord(c) < 32 or c in '/\\:<>"|?*' for c in value)
        or (value.casefold() in ("manifest.json", "intent.json", "current.json"))
        or (
            value.split(".", maxsplit=1)[0].upper()
            in {
                "CON",
                "PRN",
                "AUX",
                "NUL",
                *(f"COM{i}" for i in range(1, 10)),
                *(f"LPT{i}" for i in range(1, 10)),
            }
        )
    ):
        msg = "unsafe or reserved artifact filename"
        raise ValueError(msg)
    return value


def generation_name(created_at: datetime, publication_id: UUID) -> str:
    """Human-readable UTC timestamp and nominal publication identity."""
    if not isinstance(created_at, datetime) or created_at.utcoffset() != timedelta(0):
        msg = "publication timestamp must be timezone-aware UTC"
        raise ValueError(msg)
    if not isinstance(publication_id, UUID):
        msg = "publication identity must be a UUID"
        raise TypeError(msg)
    return created_at.strftime("%Y%m%dT%H%M%S%fZ") + "-" + str(publication_id)


def validate_generation_name(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(
        "\\d{8}T\\d{12}Z-[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}", value,
    ):
        msg = "invalid generation identity"
        raise ValueError(msg)
    return value


class PublicationStatus(StrEnum):
    """Observed filesystem availability, independent of execution outcome."""

    CURRENT = "current"
    AVAILABLE = "available"
    STAGED = "staged_valid"
    INCOMPLETE = "incomplete"
    CORRUPT = "corrupt"


class PublicationRecordingStatus(StrEnum):
    UNINSPECTED = "uninspected"
    UNMANAGED = "unmanaged"
    MISSING = "missing"
    INCOMPLETE = "incomplete"
    NOT_ACKNOWLEDGED = "not_acknowledged"
    ACKNOWLEDGED = "acknowledged"
    MISMATCH = "mismatch"


@dataclass(frozen=True, slots=True)
class ArtifactRecord:
    """An identified observation of one publication member, not a global cache key."""

    artifact_id: UUID
    name: str
    relative_path: str
    byte_size: int
    sha256: str

    def __post_init__(self) -> None:
        if not isinstance(self.artifact_id, UUID):
            msg = "artifact identity must be a UUID"
            raise TypeError(msg)
        artifact_name(self.name)
        if self.relative_path != self.name:
            msg = "the initial contract requires flat, name-matching paths"
            raise ValueError(msg)
        if type(self.byte_size) is not int or self.byte_size < 0:
            msg = "artifact size must be a nonnegative integer"
            raise ValueError(msg)
        _validate_sha256(self.sha256)


def _validate_sha256(value: str) -> None:
    if not isinstance(value, str) or not re.fullmatch("[0-9a-f]{64}", value):
        msg = "digest must be a canonical SHA-256 value"
        raise ValueError(msg)


def _validate_publication_request(
    publication_id: UUID,
    producing_execution_id: UUID,
    publication_execution_id: UUID | None,
    generation_id: str,
    created_at: datetime,
    expected_artifact_names: tuple[str, ...],
    dependencies: tuple[Fact, ...],
) -> tuple[str, ...]:
    """Validate intent without manufacturing artifact observations."""
    for identity in (publication_id, producing_execution_id):
        if not isinstance(identity, UUID):
            msg = "publication/producer identities must be UUIDs"
            raise TypeError(msg)
    if publication_execution_id is not None and (
        not isinstance(publication_execution_id, UUID)
    ):
        msg = "publication execution identity must be a UUID or unknown"
        raise TypeError(msg)
    if (
        publication_id in (producing_execution_id, publication_execution_id)
        or publication_execution_id == producing_execution_id
    ):
        msg = "publication and producing/publishing occurrences are distinct"
        raise ValueError(msg)
    if generation_id != generation_name(created_at, publication_id):
        msg = "generation identity disagrees with publication/timestamp"
        raise ValueError(msg)
    names = tuple(artifact_name(name) for name in expected_artifact_names)
    if not names or len({n.casefold() for n in names}) != len(names):
        msg = "expected artifact names must be nonempty and unique"
        raise ValueError(msg)
    _facts(dependencies)
    return tuple(sorted(names))


@dataclass(frozen=True, slots=True)
class PublicationManifest:
    """Complete generation membership and provenance, distinct from ledger success."""

    publication_id: UUID
    producing_execution_id: UUID
    generation_id: str
    created_at: datetime
    expected_artifact_names: tuple[str, ...]
    artifacts: tuple[ArtifactRecord, ...]
    dependencies: tuple[Fact, ...] = ()
    publication_execution_id: UUID | None = None
    schema_version: int = 1
    complete: bool = True

    def __post_init__(self) -> None:
        if (
            type(self.schema_version) is not int
            or self.schema_version != 1
            or self.complete is not True
        ):
            msg = "unsupported or incomplete publication manifest"
            raise ValueError(msg)
        names = _validate_publication_request(
            self.publication_id,
            self.producing_execution_id,
            self.publication_execution_id,
            self.generation_id,
            self.created_at,
            self.expected_artifact_names,
            self.dependencies,
        )
        values = tuple(self.artifacts)
        if any(not isinstance(value, ArtifactRecord) for value in values):
            msg = "artifacts must contain ArtifactRecord values"
            raise TypeError(msg)
        if sorted(v.name for v in values) != sorted(names):
            msg = "manifest membership differs from expected artifacts"
            raise ValueError(msg)
        if any(v.artifact_id != uuid5(self.publication_id, v.name) for v in values):
            msg = "artifact identity belongs to a different publication/member"
            raise ValueError(msg)
        object.__setattr__(self, "expected_artifact_names", tuple(sorted(names)))
        object.__setattr__(
            self, "artifacts", tuple(sorted(values, key=lambda v: v.name)),
        )

# Copyright (c) 2026
"""Identified repository snapshot state over observed resource occurrences."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.repository.resource import (
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
    _validate_sha256,
)

if TYPE_CHECKING:
    from devtools.context.repository.identity import RepositoryId


@dataclass(frozen=True, slots=True)
class RepositorySnapshotId:
    """Identify state observed under the bounded observation semantics."""

    value: str

    def __post_init__(self) -> None:
        """Validate the local SHA-256 hexadecimal representation."""
        _validate_sha256(self.value, label="Repository snapshot identity")

    def __str__(self) -> str:
        """Return the local hexadecimal identity representation."""
        return self.value


@dataclass(frozen=True, slots=True)
class RepositorySnapshot:
    """Represent complete state for an explicit required resource collection."""

    OBSERVATION_SEMANTICS: ClassVar[str] = "explicit-required-text-resources-sha256-v1"

    id: RepositorySnapshotId
    repository_id: RepositoryId
    resources: tuple[RepositoryResourceOccurrence, ...]

    @property
    def resource(self) -> RepositoryResourceOccurrence:
        """Return the sole occurrence for compatible single-resource consumers."""
        if len(self.resources) != 1:
            msg = "Repository snapshot does not contain exactly one resource."
            raise ValueError(msg)
        return self.resources[0]

    def resource_at(
        self,
        address: RepositoryResourceAddress,
    ) -> RepositoryResourceOccurrence:
        """Return the observed occurrence at one exact requested address."""
        for resource in self.resources:
            if resource.address == address:
                return resource
        msg = f"Repository snapshot does not contain resource address: {address}."
        raise ValueError(msg)

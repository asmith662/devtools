# Copyright (c) 2026
"""Explicit, immutable decisions about repository Context disclosure."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from devtools.context.planning.materialization import MaterializedDisclosureItem
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )


class PlannedDisclosure(Protocol):
    """One concrete, purpose-bound representation chosen by a caller."""

    @property
    def purpose(self) -> str:
        """Return the information purpose served by this choice."""
        ...

    @property
    def snapshot_id(self) -> RepositorySnapshotId:
        """Return the observed repository state this choice addresses."""
        ...

    @property
    def repository_id(self) -> RepositoryId:
        """Return the nominal repository identity."""
        ...

    @property
    def representation(self) -> str:
        """Name the concrete, implemented disclosure form."""
        ...

    @property
    def identity(self) -> str:
        """Identify this exact disclosure choice and its native support."""
        ...

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Realize the choice from retained, matching snapshot state."""
        ...


@dataclass(frozen=True, slots=True)
class DisclosurePlan:
    """Identify an ordered choice of disclosures for one explicit purpose.

    Construction is caller-directed. It neither retrieves nor estimates
    relevance, cost, or sufficiency.
    """

    purpose: str
    snapshot_id: RepositorySnapshotId
    repository_id: RepositoryId
    disclosures: tuple[PlannedDisclosure, ...]
    preceding_plan_identity: str | None = None

    def __post_init__(self) -> None:
        """Reject mixed purposes, snapshots, and repeated choices."""
        if not self.purpose.strip():
            msg = "Disclosure plan purpose must not be blank."
            raise ValueError(msg)
        if not self.disclosures:
            msg = "Disclosure plan needs at least one explicit disclosure."
            raise ValueError(msg)
        if any(
            item.purpose != self.purpose
            or item.snapshot_id != self.snapshot_id
            or item.repository_id != self.repository_id
            for item in self.disclosures
        ):
            msg = (
                "Disclosure plan contains an incompatible purpose or repository state."
            )
            raise ValueError(msg)
        if len({item.identity for item in self.disclosures}) != len(self.disclosures):
            msg = "Disclosure plan repeats an identical disclosure choice."
            raise ValueError(msg)

    @property
    def identity(self) -> str:
        """Identify purpose, applicability, ordered choices, and optional lineage."""
        return _digest(
            "explicit-repository-disclosure-plan-v1",
            self.purpose,
            str(self.snapshot_id),
            str(self.repository_id),
            self.preceding_plan_identity or "",
            *(
                value
                for item in self.disclosures
                for value in (item.representation, item.identity)
            ),
        )


def plan_disclosures(
    *,
    purpose: str,
    snapshot: RepositorySnapshot,
    disclosures: tuple[PlannedDisclosure, ...],
    preceding_plan_identity: str | None = None,
) -> DisclosurePlan:
    """Record caller-chosen representations without performing retrieval."""
    return DisclosurePlan(
        purpose=purpose,
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        disclosures=disclosures,
        preceding_plan_identity=preceding_plan_identity,
    )


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()

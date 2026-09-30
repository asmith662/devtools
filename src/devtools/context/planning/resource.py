# Copyright (c) 2026
"""Explicit whole-resource disclosure from retained repository state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.planning.materialization import (
    DisclosureMaterializationError,
    MaterializedDisclosureItem,
)
from devtools.context.planning.plan import _digest

if TYPE_CHECKING:
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )


@dataclass(frozen=True, slots=True)
class WholeResourceDisclosureOption:
    """Choose one exact observed resource, without inferring relevance."""

    purpose: str
    snapshot_id: RepositorySnapshotId
    repository_id: RepositoryId
    resource: RepositoryResourceOccurrence

    representation: ClassVar[str] = "whole-observed-resource-v1"

    @property
    def identity(self) -> str:
        """Identify this explicit representation of one observed occurrence."""
        return _digest(
            self.representation,
            self.purpose,
            str(self.snapshot_id),
            str(self.repository_id),
            str(self.resource.address),
            str(self.resource.content_identity),
        )

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Use exact retained content; reject stale, missing, or redirected state."""
        if (
            snapshot.id != self.snapshot_id
            or snapshot.repository_id != self.repository_id
        ):
            msg = "Whole-resource disclosure belongs to another snapshot."
            raise DisclosureMaterializationError(msg)
        try:
            observed = snapshot.resource_at(self.resource.address)
        except ValueError as error:
            msg = "Whole-resource disclosure source is missing."
            raise DisclosureMaterializationError(msg) from error
        if observed != self.resource:
            msg = "Whole-resource disclosure source differs from retained evidence."
            raise DisclosureMaterializationError(msg)
        text = "".join(
            (
                "Whole observed repository resource\n",
                f"Purpose: {self.purpose}\n",
                f"Snapshot identity: {self.snapshot_id}\n",
                f"Resource pointer: {observed.address}\n",
                f"Content identity: {observed.content_identity}\n",
                f"Exact source UTF-8 bytes: {len(observed.content.encode('utf-8'))}\n",
                "--- exact resource source begins ---\n",
                observed.content,
                "\n--- exact resource source ends ---\n",
            ),
        )
        return MaterializedDisclosureItem(
            option_identity=self.identity,
            representation=self.representation,
            resource_addresses=(observed.address,),
            content_identities=(observed.content_identity,),
            text=text,
            native_provenance=observed,
        )


def choose_whole_resource_disclosure(
    *,
    purpose: str,
    snapshot: RepositorySnapshot,
    resource_address: RepositoryResourceAddress,
) -> WholeResourceDisclosureOption:
    """Record an explicit coarse representation, without reading the filesystem."""
    if not purpose.strip():
        msg = "Whole-resource disclosure purpose must not be blank."
        raise ValueError(msg)
    return WholeResourceDisclosureOption(
        purpose=purpose,
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=snapshot.resource_at(resource_address),
    )

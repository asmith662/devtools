# Copyright (c) 2026
"""Explicit Context choice of one snapshot-bound source-search representation."""

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
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )
    from devtools.context.retrieval.source import RepositorySourceUnit


@dataclass(frozen=True, slots=True)
class SourceSearchDisclosureOption:
    """Choose exact source text after retrieval; ranking never selects disclosure."""

    purpose: str
    unit: RepositorySourceUnit

    representation: ClassVar[str] = "exact-source-search-unit-v1"

    @property
    def identity(self) -> str:
        """Bind the explicit choice, purpose and source representation."""
        return _digest(
            self.representation,
            self.purpose,
            str(self.unit.snapshot_id),
            str(self.unit.id),
        )

    @property
    def snapshot_id(self) -> RepositorySnapshotId:
        """Expose the source observation, not a moving checkout."""
        return self.unit.snapshot_id

    @property
    def repository_id(self) -> RepositoryId:
        """Retain the original nominal repository identity."""
        return self.unit.repository_id

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Reuse the existing disclosure pipeline without source reacquisition."""
        if (
            not self.purpose.strip()
            or snapshot.id != self.snapshot_id
            or snapshot.repository_id != self.repository_id
        ):
            msg = "Source disclosure purpose or snapshot is incompatible."
            raise DisclosureMaterializationError(msg)
        try:
            resource = snapshot.resource_at(self.unit.resource.address)
        except ValueError as error:
            msg = "Source disclosure parent resource is missing."
            raise DisclosureMaterializationError(msg) from error
        if resource != self.unit.resource:
            msg = "Source disclosure parent resource changed."
            raise DisclosureMaterializationError(msg)
        return MaterializedDisclosureItem(
            self.identity,
            self.representation,
            (self.unit.resource.address,),
            (self.unit.resource.content_identity,),
            "".join(
                (
                    f"Resource pointer: {resource.address}\n",
                    f"Snapshot identity: {snapshot.id}\n",
                    f"Content identity: {resource.content_identity}\n",
                    (
                        f"Representation: {self.unit.kind}; "
                        f"symbol: {self.unit.qualified_name or '-'}\n"
                    ),
                    (
                        f"Character span: [{self.unit.start}, {self.unit.end}); "
                        f"lines: {self.unit.start_line}-{self.unit.end_line}\n"
                    ),
                    "--- exact source begins ---\n",
                    self.unit.text,
                    "\n--- exact source ends ---\n",
                ),
            ),
            self.unit,
        )

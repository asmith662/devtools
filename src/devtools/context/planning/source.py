# Copyright (c) 2026
"""Explicit Context choice of one snapshot-bound source-search representation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.planning.materialization import (
    ContextDisclosure,
    DisclosureMaterializationError,
    MaterializedDisclosureItem,
    materialize_disclosure_plan,
)
from devtools.context.planning.plan import _digest, plan_disclosures

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


@dataclass(frozen=True, slots=True)
class SourceRangeDisclosureOption:
    """Choose a bounded exact character region within a retained source unit.

    Offsets are absolute within the parent decoded resource, including for
    symbol/window units. Budget truncation never splits a UTF-8 character and
    does not turn partial availability into complete disclosure.
    """

    purpose: str
    unit: RepositorySourceUnit
    start: int
    end: int
    maximum_bytes: int

    representation: ClassVar[str] = "exact-source-character-range-v1"

    def __post_init__(self) -> None:
        """Admit a finite budget and a supported half-open source range."""
        if (
            type(self.start) is not int
            or type(self.end) is not int
            or type(self.maximum_bytes) is not int
            or self.maximum_bytes <= 0
            or not (
                self.unit.start <= self.start < self.end <= self.unit.end
                or self.start == self.end == self.unit.start == self.unit.end == 0
            )
        ):
            msg = "Source range or byte budget is invalid."
            raise ValueError(msg)

    @property
    def snapshot_id(self) -> RepositorySnapshotId:
        """Retain the source snapshot identity."""
        return self.unit.snapshot_id

    @property
    def repository_id(self) -> RepositoryId:
        """Retain nominal repository identity."""
        return self.unit.repository_id

    @property
    def text(self) -> str:
        """Return only the exact budget-admitted text."""
        return (
            self.unit.resource.content[self.start : self.end]
            .encode("utf-8")[: self.maximum_bytes]
            .decode("utf-8", errors="ignore")
        )

    @property
    def span(self) -> tuple[int, int]:
        """Return the actually disclosed half-open character span."""
        return self.start, self.start + len(self.text)

    @property
    def truncated(self) -> bool:
        """Distinguish partial from complete requested acquisition."""
        return self.span[1] < self.end

    @property
    def identity(self) -> str:
        """Bind the source, requested range, purpose and budget."""
        return _digest(
            self.representation,
            self.purpose,
            str(self.snapshot_id),
            str(self.unit.id),
            str(self.start),
            str(self.end),
            str(self.maximum_bytes),
        )

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Authenticate existing source provenance before bounded disclosure."""
        SourceSearchDisclosureOption(self.purpose, self.unit).materialize(snapshot)
        return MaterializedDisclosureItem(
            self.identity,
            self.representation,
            (self.unit.resource.address,),
            (self.unit.resource.content_identity,),
            self.text,
            self,
        )


def materialize_source_range(
    snapshot: RepositorySnapshot,
    option: SourceRangeDisclosureOption,
) -> ContextDisclosure:
    """Reuse canonical planning/materialization for a selected exact region."""
    return materialize_disclosure_plan(
        plan=plan_disclosures(
            purpose=option.purpose,
            snapshot=snapshot,
            disclosures=(option,),
        ),
        snapshot=snapshot,
    )

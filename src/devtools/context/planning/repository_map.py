# Copyright (c) 2026
"""Caller-selected map metadata, faithfully realized through Context Planning."""

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
    from devtools.context.repository.resource import RepositoryResourceOccurrence
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )
    from devtools.context.retrieval.repository_map.view import (
        RepositoryMapSymbol,
        RepositoryMapView,
    )


def _selected_resources(
    snapshot: RepositorySnapshot,
    view: RepositoryMapView,
    symbols: tuple[RepositoryMapSymbol, ...],
) -> tuple[RepositoryResourceOccurrence, ...]:
    """Reuse canonical map admission, then authenticate the explicit selection."""
    # Defer the Retrieval import until Context's public package is initialized.
    from devtools.context.retrieval.repository_map.view import (  # noqa: PLC0415
        build_repository_map_view,
    )

    if view != build_repository_map_view(snapshot, core=view.core):
        msg = "Repository map differs from its canonical typed core projection."
        raise ValueError(msg)
    if not symbols or len({item.node.identity for item in symbols}) != len(symbols):
        msg = "Map disclosure requires a nonempty, distinct symbol selection."
        raise ValueError(msg)
    if any(item not in view.symbols for item in symbols):
        msg = "Selected map symbol is absent or differs from native map evidence."
        raise ValueError(msg)
    addresses = dict.fromkeys(item.node.resource_address for item in symbols)
    return tuple(snapshot.resource_at(address) for address in addresses)


@dataclass(frozen=True, slots=True)
class RepositoryMapDisclosureOption:
    """Choose compact orientation metadata without selecting source or relevance."""

    purpose: str
    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    view: RepositoryMapView
    symbols: tuple[RepositoryMapSymbol, ...]
    resources: tuple[RepositoryResourceOccurrence, ...]

    representation: ClassVar[str] = "selected-repository-map-metadata-v1"

    @property
    def identity(self) -> str:
        """Bind purpose, state and ordered exact native symbol evidence."""
        return _digest(
            self.representation,
            self.purpose,
            str(self.repository_id),
            str(self.snapshot_id),
            *(
                value
                for symbol in self.symbols
                for value in (
                    symbol.node.identity,
                    symbol.declaration.identity,
                    symbol.qualified_name,
                )
            ),
        )

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Authenticate retained dependencies and render metadata, never source."""
        if (
            not self.purpose.strip()
            or snapshot.repository_id != self.repository_id
            or snapshot.id != self.snapshot_id
        ):
            msg = "Map disclosure purpose or repository state is incompatible."
            raise DisclosureMaterializationError(msg)
        try:
            resources = _selected_resources(snapshot, self.view, self.symbols)
        except ValueError as error:
            msg = "Map disclosure native evidence is incompatible."
            raise DisclosureMaterializationError(msg) from error
        if resources != self.resources:
            msg = "Map disclosure resources differ from the retained selection."
            raise DisclosureMaterializationError(msg)
        parts = [
            "Caller-selected repository map metadata (not source or sufficiency)\n",
            f"Snapshot identity: {self.snapshot_id}\n",
        ]
        parts.extend(
            f"Resource pointer: {resource.address}; "
            f"content identity: {resource.content_identity}\n"
            for resource in resources
        )
        for symbol in self.symbols:
            span = symbol.declaration.support.source_range
            parts.append(
                f"{symbol.node.resource_address}: {symbol.node.kind.value} "
                f"{symbol.qualified_name}; "
                f"subject: {symbol.declaration.subject.identity}; "
                f"declaration range: {span.start_line}:{span.start_column_utf8}-"
                f"{span.end_line}:{span.end_column_utf8} "
                "(one-based lines, zero-based UTF-8 columns, exclusive end)\n",
            )
        return MaterializedDisclosureItem(
            option_identity=self.identity,
            representation=self.representation,
            resource_addresses=tuple(item.address for item in resources),
            content_identities=tuple(item.content_identity for item in resources),
            text="".join(parts),
            native_provenance=self.symbols,
        )


def choose_repository_map_disclosure(
    *,
    purpose: str,
    snapshot: RepositorySnapshot,
    view: RepositoryMapView,
    symbols: tuple[RepositoryMapSymbol, ...],
) -> RepositoryMapDisclosureOption:
    """Record the caller's ordered selection using existing map and plan owners."""
    if not purpose.strip():
        msg = "Map disclosure purpose must not be blank."
        raise ValueError(msg)
    return RepositoryMapDisclosureOption(
        purpose=purpose,
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        view=view,
        symbols=symbols,
        resources=_selected_resources(snapshot, view, symbols),
    )

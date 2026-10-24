# Copyright (c) 2026
"""Caller-selected map metadata, faithfully realized through Context Planning."""

from __future__ import annotations

from dataclasses import dataclass, replace
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
    from devtools.context.retrieval.source import (
        RepositorySourceUnit,
        SourceSearchIndex,
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


def _map_source_unit(
    snapshot: RepositorySnapshot,
    map_disclosure: RepositoryMapDisclosureOption,
    symbol: RepositoryMapSymbol,
    source_index: SourceSearchIndex,
) -> RepositorySourceUnit:
    """Compose native map admission, admitted source scope and exact RI bounds."""
    from io import StringIO  # noqa: PLC0415 -- bounded source adaptation

    from devtools.context.python.function.materialization import (  # noqa: PLC0415
        _absolute_byte_offset,
    )
    from devtools.context.retrieval.source.representation import (  # noqa: PLC0415
        _unit,
    )

    map_disclosure.materialize(snapshot)
    if symbol not in map_disclosure.symbols or source_index.snapshot != snapshot:
        msg = "Map source selection or source index belongs to another frame."
        raise ValueError(msg)
    files = tuple(
        unit
        for view in source_index.views
        if view.kind == "file"
        for unit in view.units
        if unit.resource.address == symbol.node.resource_address
    )
    if len(files) != 1:
        msg = "Selected source needs one admitted whole-resource source unit."
        raise ValueError(msg)
    file = files[0]
    if (
        file.resource != snapshot.resource_at(symbol.node.resource_address)
        or file.repository_id != snapshot.repository_id
        or file.snapshot_id != snapshot.id
        or file.kind != "file"
        or file.start != 0
        or file.end != len(file.resource.content)
    ):
        msg = "Admitted source unit differs from the retained resource frame."
        raise ValueError(msg)
    span = symbol.declaration.support.source_range
    lines = tuple(line.encode("utf-8") for line in StringIO(file.text, newline=""))
    encoded = file.text.encode("utf-8")
    start = _absolute_byte_offset(
        lines,
        line_number=span.start_line,
        column=span.start_column_utf8,
    )
    end = _absolute_byte_offset(
        lines,
        line_number=span.end_line,
        column=span.end_column_utf8,
    )
    return _unit(
        file,
        "symbol",
        len(encoded[:start].decode("utf-8")),
        len(encoded[:end].decode("utf-8")),
        qualified_name=symbol.qualified_name,
        symbol_kind=symbol.node.kind.value,
        occurrence=symbol.declaration.support,
        declaration=symbol.declaration,
    )


@dataclass(frozen=True, slots=True)
class RepositoryMapSourceDisclosureOption:
    """Retain an explicit map-to-source choice through existing materialization."""

    purpose: str
    map_disclosure: RepositoryMapDisclosureOption
    symbol: RepositoryMapSymbol
    source_index: SourceSearchIndex
    unit: RepositorySourceUnit

    representation: ClassVar[str] = "map-selected-exact-source-v1"

    @property
    def repository_id(self) -> RepositoryId:
        """Retain the map's nominal repository frame."""
        return self.map_disclosure.repository_id

    @property
    def snapshot_id(self) -> RepositorySnapshotId:
        """Retain the map's exact observed state."""
        return self.map_disclosure.snapshot_id

    @property
    def identity(self) -> str:
        """Bind purpose, original map choice and exact native source selection."""
        return _digest(
            self.representation,
            self.purpose,
            self.map_disclosure.identity,
            self.symbol.declaration.identity,
            str(self.unit.id),
        )

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Reauthenticate map/source coupling, then reuse exact-source rendering."""
        from devtools.context.planning.source import (  # noqa: PLC0415
            SourceSearchDisclosureOption,
        )

        expected = _map_source_unit(
            snapshot,
            self.map_disclosure,
            self.symbol,
            self.source_index,
        )
        if expected != self.unit:
            msg = "Map source unit differs from its original declaration range."
            raise DisclosureMaterializationError(msg)
        item = SourceSearchDisclosureOption(self.purpose, self.unit).materialize(
            snapshot,
        )
        return replace(
            item,
            option_identity=self.identity,
            representation=self.representation,
            native_provenance=(self.symbol, self.unit),
        )


def choose_repository_map_source_disclosure(
    *,
    purpose: str,
    snapshot: RepositorySnapshot,
    map_disclosure: RepositoryMapDisclosureOption,
    symbol: RepositoryMapSymbol,
    source_index: SourceSearchIndex,
) -> RepositoryMapSourceDisclosureOption:
    """Expand one represented native symbol within an admitted source index."""
    if not purpose.strip():
        msg = "Map source disclosure purpose must not be blank."
        raise ValueError(msg)
    return RepositoryMapSourceDisclosureOption(
        purpose=purpose,
        map_disclosure=map_disclosure,
        symbol=symbol,
        source_index=source_index,
        unit=_map_source_unit(snapshot, map_disclosure, symbol, source_index),
    )

# Copyright (c) 2026
"""Build independently scored file, Python-symbol, and line-window populations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.retrieval.composition import _require_snapshot_resource
from devtools.context.retrieval.lexical import (
    analyze_repository_text_document_collection,
    build_repository_text_lexical_inverted_index,
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.context.retrieval.source.representation import (
    RepositorySourceUnit,
    SourceDocumentCollection,
    SourceRepresentation,
    file_unit,
    symbol_units,
    window_units,
)

if TYPE_CHECKING:
    from devtools.context.repository.corpus import RepositoryTextCorpus
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.lexical import RepositoryTextLexicalInvertedIndex


@dataclass(frozen=True, slots=True)
class SourceSearchView:
    """One lexical population and explicit whole-file fallback diagnostics."""

    kind: SourceRepresentation
    units: tuple[RepositorySourceUnit, ...]
    lexical_index: RepositoryTextLexicalInvertedIndex
    fallbacks: tuple[tuple[RepositoryResourceAddress, str], ...] = ()


@dataclass(frozen=True, slots=True)
class SourceSearchIndex:
    """Retain immutable snapshot state and all available representation views."""

    snapshot: RepositorySnapshot
    views: tuple[SourceSearchView, ...]
    window_lines: int
    overlap_lines: int

    def expand(
        self,
        unit: RepositorySourceUnit,
        *,
        to: str = "file",
    ) -> RepositorySourceUnit:
        """Expand to a retained file or the nearest containing class."""
        units = {item.id: item for view in self.views for item in view.units}
        if units.get(unit.id) != unit:
            msg = "Source unit does not belong to this index."
            raise ValueError(msg)
        if to == "file":
            return next(
                item for item in self.views[0].units if item.resource == unit.resource
            )
        if to != "class":
            msg = "Expansion target must be file or class."
            raise ValueError(msg)
        classes = [
            item
            for item in units.values()
            if item.resource == unit.resource
            and item.symbol_kind == "class"
            and item.start <= unit.start
            and unit.end <= item.end
        ]
        if classes:
            return min(classes, key=lambda item: item.end - item.start)
        msg = "Source unit has no enclosing class."
        raise ValueError(msg)


def build_source_search_index(
    snapshot: RepositorySnapshot,
    *,
    corpus: RepositoryTextCorpus,
    window_lines: int = 80,
    overlap_lines: int = 20,
) -> SourceSearchIndex:
    """Index only explicitly admitted corpus resources, without filesystem reads."""
    if window_lines <= 0 or not 0 <= overlap_lines < window_lines:
        msg = (
            "Window lines must be positive and overlap must be smaller and nonnegative."
        )
        raise ValueError(msg)
    if corpus.definition.discovery.repository_id != snapshot.repository_id:
        msg = "Source corpus belongs to another repository."
        raise ValueError(msg)
    files: list[RepositorySourceUnit] = []
    symbols: list[RepositorySourceUnit] = []
    windows: list[RepositorySourceUnit] = []
    fallbacks = []
    for document in represent_repository_text_corpus(corpus=corpus).documents:
        _require_snapshot_resource(snapshot, document.resource)
        file = file_unit(snapshot, document)
        files.append(file)
        declarations, reason = symbol_units(snapshot, file)
        symbols.extend(declarations or (file,))
        if reason is not None:
            fallbacks.append((file.resource.address, reason))
        windows.extend(window_units(file, window_lines, overlap_lines))
    views = []
    populations: tuple[tuple[SourceRepresentation, list[RepositorySourceUnit]], ...] = (
        ("file", files),
        ("symbol", symbols),
        ("window", windows),
    )
    for kind, units in populations:
        population = SourceDocumentCollection(corpus, tuple(units))
        index = build_repository_text_lexical_inverted_index(
            corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
                collection_analysis=analyze_repository_text_document_collection(
                    document_collection=population,
                ),
            ),
        )
        views.append(
            SourceSearchView(
                kind,
                tuple(units),
                index,
                tuple(fallbacks) if kind == "symbol" else (),
            ),
        )
    return SourceSearchIndex(snapshot, tuple(views), window_lines, overlap_lines)

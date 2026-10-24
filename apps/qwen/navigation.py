# Copyright (c) 2026
# ruff: noqa: EM101, PLR2004, SLF001 -- same application owner helpers
"""Opt-in native navigation over canonical map and Planning representations.

Handles only select server-held Planning evidence. Source disclosure and editing
remain owned by ContextTools and its ordinary current observed-source contract.
"""

from __future__ import annotations

import time
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from apps.qwen.context_tools import ContextRequestError
from devtools.context.planning import (
    choose_repository_map_disclosure,
    choose_repository_map_source_disclosure,
)
from devtools.context.python.classes.declarations import (
    PythonClassDeclarationKnowledge,
    PythonMethodDeclarationKnowledge,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKnowledge,
)
from devtools.context.retrieval.graph import (
    PythonGraphProjection,
    build_python_graph_view,
)
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
)
from devtools.context.retrieval.repository_map import (
    build_repository_map_view,
    calculate_repository_map_importance,
    rank_repository_map,
)

if TYPE_CHECKING:
    from apps.qwen.context_tools import ContextTools
    from devtools.context.planning import RepositoryMapDisclosureOption
    from devtools.context.retrieval.repository_map import RepositoryMapSymbol


class RepositoryMapNavigation:
    """One task-local retained map frame, discarded after any admitted edit."""

    def __init__(self, tools: ContextTools) -> None:
        """Reuse existing admitted declarations and static reference derivation."""
        started = time.perf_counter()
        self.tools = tools
        declarations = {
            unit.declaration.identity: unit.declaration
            for view in tools.index.views
            for unit in view.units
            if unit.declaration is not None
        }.values()
        references = tuple(
            reference
            for address in tools.addresses
            if (analysis := tools._reference_analysis(address)) is not None
            for reference in analysis.references
        )
        self.view = build_repository_map_view(
            tools.snapshot,
            core=build_python_graph_view(
                tools.snapshot,
                projection=PythonGraphProjection.TYPED_CORE,
                functions=tuple(
                    d
                    for d in declarations
                    if isinstance(d, PythonFunctionDeclarationKnowledge)
                ),
                classes=tuple(
                    d
                    for d in declarations
                    if isinstance(d, PythonClassDeclarationKnowledge)
                ),
                methods=tuple(
                    d
                    for d in declarations
                    if isinstance(d, PythonMethodDeclarationKnowledge)
                ),
                references=references,
            ),
        )
        self.importance = calculate_repository_map_importance(
            tools.snapshot,
            view=self.view,
        )
        self.preparation_seconds = time.perf_counter() - started
        self.selections: dict[
            str,
            tuple[RepositoryMapDisclosureOption, RepositoryMapSymbol],
        ] = {}

    def orient(self, query: str, start: int) -> dict[str, Any]:
        """Rank using the existing map policy; disclose a bounded caller page."""
        tools = self.tools
        ranked = rank_repository_map(
            tools.snapshot,
            purpose=tools.task.objective,
            query=analyze_repository_text_lexical_query(text=query),
            importance=self.importance,
        ).symbols
        selected = tuple(row.symbol for row in ranked[start : start + 6])
        if not selected:
            return {
                "status": "NOT_FOUND",
                "symbols": [],
                "truncated": False,
                "preparation_seconds": self.preparation_seconds,
            }
        option = choose_repository_map_disclosure(
            purpose=tools.task.objective,
            snapshot=tools.snapshot,
            view=self.view,
            symbols=selected,
        )
        item = option.materialize(snapshot=tools.snapshot)
        rows = []
        for symbol in selected:
            handle = "map:" + option.identity + ":" + symbol.declaration.identity
            self.selections[handle] = option, symbol
            rows.append(
                {
                    "handle": handle,
                    "path": symbol.node.resource_address.value,
                    "kind": symbol.node.kind.value,
                    "name": symbol.qualified_name,
                    "declaration": symbol.declaration.identity,
                    "source_range": asdict(symbol.declaration.support.source_range),
                },
            )
        return {
            "status": "RETURNED",
            "symbols": rows,
            "orientation": item.text,
            "representation": option.representation,
            "disclosure": option.identity,
            "continuation_start": start + len(rows),
            "truncated": start + len(rows) < len(ranked),
            "preparation_seconds": self.preparation_seconds,
            "orientation_bytes": len(item.text.encode()),
            "scope": "ranked admitted declarations; metadata grants no edit authority",
        }

    def expand(self, handle: str) -> dict[str, Any]:
        """Materialize exactly one represented declaration, then observe its text."""
        if handle not in self.selections:
            raise ContextRequestError(
                "MAP_SELECTION_STALE_OR_UNKNOWN",
                "Select from current repository_map; edits invalidate old frames",
            )
        tools = self.tools
        orientation, symbol = self.selections[handle]
        option = choose_repository_map_source_disclosure(
            purpose=tools.task.objective,
            snapshot=tools.snapshot,
            map_disclosure=orientation,
            symbol=symbol,
            source_index=tools.index,
        )
        option.materialize(snapshot=tools.snapshot)
        unit = option.unit
        size = len(unit.text.encode())
        if size > 4096:
            raise ContextRequestError(
                "MAP_SOURCE_TOO_LARGE",
                f"Exact declaration is {size} UTF-8 bytes; limit=4096. "
                "Use bounded inspect_source for authorized path "
                + unit.resource.address.value,
            )
        result = tools._read(
            {
                "path": unit.resource.address.value,
                "version": str(unit.resource.content_identity),
                "start": unit.start,
                "end": unit.end,
            },
        )
        result.update(
            representation=option.representation,
            disclosure=option.identity,
            map_disclosure=orientation.identity,
            map_handle=handle,
            declaration=symbol.declaration.identity,
            source_range=asdict(symbol.declaration.support.source_range),
            selected_unit=str(unit.id),
        )
        return result

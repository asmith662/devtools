# Copyright (c) 2026
"""Native metadata and exact-unit selection over the existing source Tools."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, cast

from devtools.context import RepositoryResourceAddress
from devtools.tools import ToolDescriptor
from devtools.tools.source import SourceNavigationRequest, SourceReadRequest

if TYPE_CHECKING:
    from collections.abc import Mapping

    from devtools.context.retrieval.source import RepositorySourceUnit
    from devtools.context.retrieval.source.index import SourceSearchIndex
    from devtools.context.retrieval.source.representation import SourceSearchMode

FIND = ToolDescriptor(
    "find_source",
    "Search scoped file/symbol/window metadata. Without query, page the outline. "
    "Prefer small named units; read_source_unit acquires their exact source. "
    "Metadata is not a source witness. offset pages results; path narrows scope.",
    '{"type":"object","properties":{"query":{"type":"string","maxLength":256},'
    '"path":{"type":"string"},"mode":{"enum":["file","symbol","window","mixed"]},'
    '"offset":{"type":"integer","minimum":0}},"additionalProperties":false}',
)
READ_UNIT = ToolDescriptor(
    "read_source_unit",
    "Read an exact current unit from find_source. Partial results report the next "
    "Unicode offset; use read_source for adjacent ranges. Select enclosing/file "
    "IDs from metadata only when needed. Source and request byte limits still apply.",
    '{"type":"object","properties":{"unit_id":{"type":"string"},'
    '"snapshot_id":{"type":"string"}},"required":["unit_id","snapshot_id"],'
    '"additionalProperties":false}',
)


def navigation_request(values: Mapping[str, object]) -> SourceNavigationRequest:
    """Materialize only the host-admitted native selection fields."""
    return SourceNavigationRequest(
        cast("str", values.get("query", "")),
        RepositoryResourceAddress(cast("str", values["path"]))
        if "path" in values
        else None,
        cast("SourceSearchMode", values.get("mode", "symbol")),
        cast("int", values.get("offset", 0)),
    )


def unit_read_request(
    index: SourceSearchIndex,
    values: Mapping[str, object],
    *,
    purpose: str,
    maximum_bytes: int,
) -> SourceReadRequest:
    """Bind a model reference to the actual current index; no new source identity."""
    unit = next(
        (u for v in index.views for u in v.units if str(u.id) == values["unit_id"]),
        None,
    )
    if str(index.snapshot.id) != values["snapshot_id"] or unit is None:
        msg = "Source unit is foreign, stale or outside the admitted index."
        raise ValueError(msg)
    return SourceReadRequest(purpose, unit, unit.start, unit.end, maximum_bytes)


def navigation_feedback(
    units: tuple[RepositorySourceUnit, ...],
    index: SourceSearchIndex,
    *,
    offset: int,
    maximum_bytes: int,
    page_size: int = 8,
) -> dict[str, object]:
    """Bound metadata presentation without pretending it disclosed any source."""
    rows: list[dict[str, object]] = []
    result: dict[str, object] = {
        "repository_id": str(index.snapshot.repository_id),
        "snapshot_id": str(index.snapshot.id),
        "source_acquired": False,
        "coordinates": "half-open Unicode offsets; one-based physical lines",
        "units": rows,
        "next_offset": None,
        "partial": False,
    }
    for unit in units:
        row: dict[str, object] = {
            "unit_id": str(unit.id),
            "path": str(unit.resource.address),
            "version": str(unit.resource.content_identity),
            "kind": unit.kind,
            "name": unit.qualified_name,
            "span": [unit.start, unit.end],
            "lines": [unit.start_line, unit.end_line],
            "bytes": len(unit.text.encode()),
            "file_id": str(index.expand(unit).id),
            "parent_id": str(unit.parent_symbol_id) if unit.parent_symbol_id else None,
            "symbol_fallback": dict(index.views[1].fallbacks).get(
                unit.resource.address,
            ),
        }
        rows.append(row)
        # Reserve the bounded pagination fields before checking the next row.
        result["next_offset"] = offset + len(rows)
        result["partial"] = True
        if len(json.dumps(result, ensure_ascii=False).encode()) > maximum_bytes:
            rows.pop()
            break
    result["partial"] = len(rows) < len(units) or len(units) == page_size
    result["next_offset"] = offset + len(rows) if result["partial"] else None
    if (units and not rows) or len(
        json.dumps(result, ensure_ascii=False).encode(),
    ) > maximum_bytes:
        msg = "Source navigation metadata cannot fit its disclosure bound."
        raise ValueError(msg)
    return result

# Copyright (c) 2026
"""Native metadata and exact-unit selection over the existing source Tools."""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, cast

from devtools.agents.model_tools import execute_model_tool_call
from devtools.context import RepositoryResourceAddress
from devtools.context.retrieval.source.search import search_repository_source
from devtools.models.interaction import PromptMessage
from devtools.tools import ToolDescriptor, ToolRunner
from devtools.tools.source import (
    MAXIMUM_NAVIGATION_QUERY_CHARACTERS,
    ScopedSourceNavigationTool,
    SourceNavigationRequest,
    SourceReadRequest,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Mapping

    from devtools.agents.coding.models import CodingProgress
    from devtools.context.retrieval.source import RepositorySourceUnit
    from devtools.context.retrieval.source.index import SourceSearchIndex
    from devtools.context.retrieval.source.representation import SourceSearchMode
    from devtools.models.interaction import ModelToolCall
    from devtools.tools.source import SourceScope

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

TASK_FIND = replace(
    FIND,
    description=(
        "Search authorized source candidates for the task; omitted query uses the "
        "objective. Read a relevant unit with read_source_unit before editing. "
        "Refine query/path/mode when results are poor. browse=true explicitly pages "
        "an outline under the host allowance; next_offset is optional exploration, "
        "not an instruction to traverse every page. Metadata is not source."
    ),
    input_schema_json=FIND.input_schema_json.replace(
        '"properties":{',
        '"properties":{"browse":{"type":"boolean"},',
    ),
)


@dataclass(frozen=True, slots=True)
class NavigationPolicy:
    """Host-selected finite candidate presentation and optional outline allowance."""

    maximum_candidates: int = 6
    maximum_bytes: int = 6144
    outline_actions: int = 2

    def __post_init__(self) -> None:
        """Refuse invalid host bounds without changing execution budgets."""
        if (
            type(self.maximum_candidates) is not int
            or self.maximum_candidates <= 0
            or type(self.maximum_bytes) is not int
            or self.maximum_bytes <= 0
            or type(self.outline_actions) is not int
            or self.outline_actions < 0
        ):
            msg = (
                "Navigation policy requires positive presentation and finite outlines."
            )
            raise ValueError(msg)


def task_entry(
    index: SourceSearchIndex,
    objective: str,
    policy: NavigationPolicy,
) -> dict[str, object]:
    """Select file-first lexical candidates, not complete inventory or source."""
    files = search_repository_source(
        index,
        query=objective[:MAXIMUM_NAVIGATION_QUERY_CHARACTERS],
        mode="file",
        maximum_results=2,
    )
    hits = list(files.hits)
    for hit in files.hits:
        hits.extend(
            search_repository_source(
                index,
                query=objective[:MAXIMUM_NAVIGATION_QUERY_CHARACTERS],
                mode="symbol",
                maximum_results=2,
                resource_addresses=(hit.unit.resource.address,),
            ).hits,
        )
    unique = {hit.unit.id: hit for hit in hits}
    selected = list(unique.values())[: policy.maximum_candidates]
    while True:
        view = navigation_feedback(
            tuple(h.unit for h in selected),
            index,
            offset=0,
            maximum_bytes=policy.maximum_bytes,
        )
        rows = cast("list[dict[str, object]]", view["units"])
        for row, hit in zip(rows, selected, strict=False):
            row["retrieval"] = [
                {
                    "view": e.view,
                    "rank": e.rank,
                    "score": e.match.score,
                    "terms": [t.normalized_term for t in e.match.term_contributions][
                        :8
                    ],
                }
                for e in hit.evidence
            ]
        view.update(
            kind="task_candidates",
            complete_inventory=False,
            partial=len(rows) < len(unique),
            next_offset=None,
            selection="objective lexical file search, then scoped symbol search",
            query=objective[:MAXIMUM_NAVIGATION_QUERY_CHARACTERS],
            query_partial=len(objective) > MAXIMUM_NAVIGATION_QUERY_CHARACTERS,
            instruction=(
                "Candidates may be irrelevant. Choose read_source_unit using unit_id "
                "and snapshot_id for exact source; refine find_source query/path/mode "
                "or explicitly browse if inadequate. No source acquired."
            ),
        )
        if len(json.dumps(view, ensure_ascii=False).encode()) <= policy.maximum_bytes:
            return view
        if not selected:
            msg = "Task candidate metadata cannot fit the host presentation budget."
            raise ValueError(msg)
        selected.pop()


def prepare_navigation(
    messages: list[PromptMessage],
    index: SourceSearchIndex,
    objective: str,
    policy: NavigationPolicy | None,
) -> None:
    """Retain one host-selected initial view, without inventing native actions."""
    if policy is not None and len(messages) == 1:
        messages.append(
            PromptMessage(
                "user",
                json.dumps(task_entry(index, objective, policy), ensure_ascii=False),
            ),
        )


def task_selection(
    values: Mapping[str, object],
    objective: str,
) -> SourceNavigationRequest:
    """Default to task search; browsing requires explicit, unambiguous selection."""
    browse = values.get("browse", False)
    if type(browse) is not bool or (browse and values.get("query")):
        msg = "Select either a search query or explicit browse."
        raise ValueError(msg)
    return replace(
        navigation_request(values),
        query=""
        if browse
        else cast(
            "str",
            values.get("query") or objective[:MAXIMUM_NAVIGATION_QUERY_CHARACTERS],
        ),
    )


def outline_attempts(
    messages: list[PromptMessage],
    claimed_ids: frozenset[str | None],
) -> int:
    """Derive attempted outlines from original native calls and existing actions."""
    return sum(
        json.loads(c.arguments_json).get("browse") is True
        for m in messages
        for c in m.tool_calls
        if c.name == FIND.name and c.provider_call_id in claimed_ids
    )


async def acquire_candidates(  # noqa: PLR0913 -- explicit host composition inputs
    call: ModelToolCall,
    *,
    selection: SourceNavigationRequest,
    index: SourceSearchIndex,
    scope: SourceScope,
    admit: Callable[[ModelToolCall, SourceNavigationRequest], Awaitable[None]],
    maximum_bytes: int,
    policy: NavigationPolicy | None,
    messages: list[PromptMessage],
    progress: CodingProgress,
) -> dict[str, object]:
    """Admit one native navigation operation or acknowledge a bounded refusal."""
    attempts = outline_attempts(
        messages,
        frozenset(i for e in progress.effects for i in e.native_call_ids),
    )
    if policy and not selection.query and attempts > policy.outline_actions:
        return {
            "status": "REFUSED",
            "reason": "outline_allowance_exhausted",
            "source_acquired": False,
            "navigation_entered": False,
            "outline_attempts": attempts,
            "outline_limit": policy.outline_actions,
            "instruction": "Use a task query/path/mode or read a current unit.",
        }
    units = await execute_model_tool_call(
        call,
        invocation=_SelectedNavigation(TASK_FIND if policy else FIND, selection),
        tool=ScopedSourceNavigationTool(scope, index),
        admit=admit,
        runner=ToolRunner(),
    )
    result = navigation_feedback(
        units,
        index,
        offset=selection.offset,
        maximum_bytes=maximum_bytes - (512 if policy else 0),
    )
    if policy:
        result.update(
            outline_attempts=attempts,
            outline_limit=policy.outline_actions,
            instruction=(
                "This is a bounded candidate page, not an exhaustive traversal plan. "
                "Read a relevant unit or refine query/path/mode."
            ),
        )
    return result


@dataclass(frozen=True, slots=True)
class _SelectedNavigation:
    """Materialize the host's already parsed operation-specific input."""

    descriptor: ToolDescriptor
    selection: SourceNavigationRequest

    def materialize(self, _arguments: str) -> SourceNavigationRequest:
        """Return only the selected typed arguments before host admission."""
        return self.selection


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

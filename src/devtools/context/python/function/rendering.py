# Copyright (c) 2026
"""Deterministic text rendering for materialized Python function Context.

The renderer serializes only the existing bounded Context representation. Source
markers are visual framing, not a collision-free or machine-parseable protocol;
the recorded UTF-8 byte length identifies the unchanged source payload.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.python.function.materialization import (
        MaterializedPythonFunctionContext,
        MaterializedPythonFunctionDeclaration,
    )


@dataclass(frozen=True, slots=True)
class RenderedPythonFunctionContext:
    """Retain model-facing text and its source materialized Context."""

    materialized_context: MaterializedPythonFunctionContext
    text: str

    FORMAT: ClassVar[str] = "python-function-context-text-v1"


def render_materialized_python_function_context(
    context: MaterializedPythonFunctionContext,
) -> RenderedPythonFunctionContext:
    """Render the bounded Context without acquiring or inferring information."""
    query = context.disclosure.retrieval.query
    parts = [
        "Python function Context\n",
        f"Exact declared-name purpose: {query.declared_name}\n",
        "Selection: all exact-name matches in retrieval order\n",
        f"Selected declarations: {len(context.items)}\n",
        (
            "Bounded meaning: each item is established only as a direct "
            "module-body Python source occurrence that syntactically declares "
            "a snapshot-local function subject.\n"
        ),
    ]
    if not context.items:
        parts.append(
            "No declarations were selected from the supplied exact-name "
            "retrieval result.\n",
        )

    for ordinal, item in enumerate(context.items, start=1):
        parts.extend(_render_item(item, ordinal=ordinal))

    return RenderedPythonFunctionContext(
        materialized_context=context,
        text="".join(parts),
    )


def _render_item(
    item: MaterializedPythonFunctionDeclaration,
    *,
    ordinal: int,
) -> tuple[str, ...]:
    """Render metadata around one unchanged exact-source payload."""
    disclosure_item = item.disclosure_item
    occurrence = disclosure_item.source_occurrence
    source_range = occurrence.source_range
    source_length = len(item.source_text.encode("utf-8"))
    return (
        f"\nSelected declaration {ordinal}\n",
        f"Declared name: {disclosure_item.declared_name}\n",
        f"Declaration kind: {disclosure_item.declaration_kind.value}\n",
        f"Repository-relative resource: {occurrence.resource_address}\n",
        (
            "Source location: "
            f"{source_range.start_line}:{source_range.start_column_utf8}-"
            f"{source_range.end_line}:{source_range.end_column_utf8} "
            "(one-based lines; zero-based UTF-8 byte columns; exclusive end)\n"
        ),
        f"Bounded proposition: {disclosure_item.proposition}\n",
        f"Exact source UTF-8 byte length: {source_length}\n",
        "--- exact source begins ---\n",
        item.source_text,
        "\n--- exact source ends ---\n",
    )

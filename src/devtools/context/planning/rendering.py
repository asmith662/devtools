# Copyright (c) 2026
"""Deterministic presentation of a realized repository disclosure."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from devtools.models.interaction import ModelRequest, Prompt

if TYPE_CHECKING:
    from devtools.context.planning.materialization import ContextDisclosure


@dataclass(frozen=True, slots=True)
class RenderedContextDisclosure:
    """Retain text and the exact realized Context it presents."""

    disclosure: ContextDisclosure
    text: str


def render_context_disclosure(
    disclosure: ContextDisclosure,
) -> RenderedContextDisclosure:
    """Render planned item order without reselecting or changing information."""
    parts = [
        "Repository Context disclosure\n",
        f"Purpose: {disclosure.plan.purpose}\n",
        f"Plan identity: {disclosure.plan.identity}\n",
        f"Snapshot identity: {disclosure.plan.snapshot_id}\n",
        f"Items: {len(disclosure.items)}\n",
    ]
    for ordinal, item in enumerate(disclosure.items, start=1):
        parts.extend(
            (
                f"\nDisclosure item {ordinal}: {item.representation}\n",
                f"Option identity: {item.option_identity}\n",
                item.text,
            ),
        )
    return RenderedContextDisclosure(disclosure, "".join(parts))


def assemble_context_disclosure_model_request(
    *,
    task_request: ModelRequest,
    context: RenderedContextDisclosure,
) -> ModelRequest:
    """Place realized Context after the unchanged task and copy all settings."""
    task_text = task_request.prompt.content
    prompt_content = "".join(
        (
            f"Task/instruction UTF-8 byte length: {len(task_text.encode('utf-8'))}\n",
            "--- task/instruction begins ---\n",
            task_text,
            "\n--- task/instruction ends ---\n\n",
            (
                "Supporting repository Context UTF-8 byte length: "
                f"{len(context.text.encode('utf-8'))}\n"
            ),
            "--- supporting repository Context begins ---\n",
            context.text,
            "\n--- supporting repository Context ends ---\n",
        ),
    )
    return replace(
        task_request,
        prompt=Prompt(prompt_content, role=task_request.prompt.role),
    )

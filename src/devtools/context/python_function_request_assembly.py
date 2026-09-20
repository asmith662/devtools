# Copyright (c) 2026
"""Bounded model-request assembly for rendered Python function Context.

The caller's existing request supplies the task Prompt and every other request
semantic. Assembly changes only Prompt content, placing the unchanged rendered
Context after the unchanged task. Section markers are visual framing rather
than a universal or machine-parseable prompt protocol.
"""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

from devtools.models.interaction import ModelRequest, Prompt

if TYPE_CHECKING:
    from devtools.context.python_function_rendering import (
        RenderedPythonFunctionContext,
    )


def assemble_python_function_context_model_request(
    *,
    task_request: ModelRequest,
    context: RenderedPythonFunctionContext,
) -> ModelRequest:
    """Return a request preserving task and request semantics around Context."""
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
        prompt=Prompt(
            content=prompt_content,
            role=task_request.prompt.role,
        ),
    )

# Copyright (c) 2026
"""Explicit host composition of native model calls and executable Tools.

Neither model disclosure nor Tool validation grants execution authority. The
host selects the invocation and Tool and supplies admission for this call. Batch
identity, response provenance, budgets and feedback retention remain host-owned.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from devtools.models.interaction import ModelToolDefinition

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from devtools.models.interaction import ModelToolCall
    from devtools.tools import Tool, ToolDescriptor, ToolInvocation, ToolRunner


def normalize_tool_descriptor(descriptor: ToolDescriptor) -> ModelToolDefinition:
    """Project an explicit Tool disclosure into model-facing semantics only."""
    try:
        schema = json.loads(descriptor.input_schema_json)
    except json.JSONDecodeError as error:  # Defensive after descriptor validation.
        msg = "Tool descriptor input schema must be valid JSON."
        raise ValueError(msg) from error
    if not isinstance(schema, dict):  # Defensive after descriptor validation.
        msg = "Tool descriptor input schema must be a JSON object."
        raise TypeError(msg)
    return ModelToolDefinition(
        name=descriptor.name,
        description=descriptor.description,
        input_schema_json=json.dumps(schema, sort_keys=True, separators=(",", ":")),
    )


async def execute_model_tool_call[ArgumentsT, ResultT](
    call: ModelToolCall,
    *,
    invocation: ToolInvocation[ArgumentsT],
    tool: Tool[ArgumentsT, ResultT],
    admit: Callable[[ModelToolCall, ArgumentsT], Awaitable[None]],
    runner: ToolRunner,
) -> ResultT:
    """Materialize, host-admit and delegate one selected call exactly once.

    Bind the native operation to its selected invocation descriptor, not to the
    possibly multiplexing Tool's name. The materializer must be effect-free.
    Admission must raise to refuse; it is required and runs before ToolRunner's
    semantic validation and execution. The Tool-defined result is returned as-is
    for host correlation with ``call``. Nothing retries, catches cancellation,
    invents feedback or infers rollback from an exception. A failed invocation
    may already have effects; a repeated call is a new host decision.
    """
    if call.name != invocation.descriptor.name:
        msg = "Model Tool call does not match the host-selected invocation."
        raise ValueError(msg)
    arguments = invocation.materialize(call.arguments_json)
    await admit(call, arguments)
    return await runner.execute(tool, arguments)

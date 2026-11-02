# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, TRY301, TRY004, PLR0913, PLR0915 -- bounded administrative read batch
"""Acceptance-only read acquisition; preflight is not a transaction or authority."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, replace
from typing import TYPE_CHECKING, Any, cast

from devtools.agents.coding.projection import request_bytes, source_feedback
from devtools.agents.coding.protocol import READ, Invocation, read_request
from devtools.agents.model_tools import execute_model_tool_call
from devtools.models.interaction import Prompt, PromptMessage
from devtools.tools import ToolRunner
from devtools.tools.source import (
    ScopedSourceTool,
    SourceReadRefusal,
    select_source_read,
)
from scripts.backlog.intake import _digest

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from devtools.context.planning.materialization import ContextDisclosure
    from devtools.context.retrieval.source.index import SourceSearchIndex
    from devtools.models.interaction import ModelRequest, ModelResponse
    from devtools.tools import Tool
    from devtools.tools.source import SourceReadRequest, SourceScope
    from scripts.backlog.native.execution import Capture


async def acquire(  # noqa: C901 -- preflight, ordered entry, completion are distinct
    response: ModelResponse,
    request: ModelRequest,
    *,
    scope: SourceScope,
    index: SourceSearchIndex,
    reads: int,
    budgets: dict[str, int],
    messages: list[PromptMessage],
    references: dict[str, str],
    claimed: set[str],
    capture: Capture,
    guard: Callable[[], Awaitable[None]],
) -> int:
    """Validate the entire read-only batch before any ToolRunner entry.

    Snapshot metadata predicts exact disclosures, never fabricates completion.
    Reserve capture and the complete next request before entering any read.
    Recheck authority/currentness for each entry. A later operational failure
    retains completed results and an unresolved entry; nothing is retried.
    """
    calls = response.tool_calls
    try:
        if len(calls) > budgets["reads"] - reads:
            raise PermissionError("Review total acquisition allowance exceeded")
        ids = [c.provider_call_id for c in calls]
        if (
            any(c.name != READ.name or not c.provider_call_id for c in calls)
            or len(set(ids)) != len(ids)
            or claimed.intersection(ids)
        ):
            raise PermissionError(
                "Review Tool is not an authorized read or identity repeats",
            )
        tool = ScopedSourceTool(scope, maximum_bytes=32768)

        def decode(value: str) -> SourceReadRequest:
            return read_request(
                value,
                index=index,
                purpose="Independent native review of restored baseline",
                maximum_bytes=32768,
                by_unit=False,
            )

        invocation = Invocation(READ, decode)
        selected = []
        feedbacks = []
        pending: list[dict[str, Any]] = []
        assistant = PromptMessage(
            "assistant",
            response.content,
            tool_calls=calls,
            reasoning_content=response.reasoning_content,
        )
        exchange = [assistant]
        for number, call in enumerate(calls, reads + 1):
            argument = invocation.materialize(call.arguments_json)
            tool.validate(argument)
            option = select_source_read(argument)
            if isinstance(option, SourceReadRefusal):
                raise ValueError(
                    "Review source interval refused; request further evidence",
                )
            selected.append(option)
            feedback = source_feedback(option, option.text)
            feedbacks.append(feedback)
            name = f"read:{number}"
            pending.extend(
                (
                    {"kind": "review-read-intent", "call": asdict(call)},
                    {
                        "kind": "review-read-result",
                        "call": asdict(call),
                        "reference": name,
                        "identity": _digest(feedback),
                        "disclosure": feedback,
                    },
                ),
            )
            exchange.append(
                PromptMessage(
                    "tool",
                    json.dumps({"reference": name, **feedback}),
                    tool_call_id=call.provider_call_id,
                ),
            )
        next_request = replace(
            request,
            prompt=Prompt("", "messages", (*messages, *exchange)),
        )
        if request_bytes(next_request) > budgets["prompt_bytes"]:
            raise ValueError("Review batch cannot fit complete next request")
        # Conservative envelope/indentation/time allowance plus next request and
        # bounded response capture. This reserves capacity, not extra model calls.
        reserve = sum(len(json.dumps(p, indent=2).encode()) + 2048 for p in pending)
        reserve += len(json.dumps(asdict(next_request), indent=2).encode())
        reserve += 2 * budgets["response_bytes"] + 8192
        if capture.used + reserve > capture.maximum:
            raise ValueError("Review batch cannot fit remaining capture budget")
        await guard()
    except (Exception, asyncio.CancelledError) as error:
        capture.add(
            "review-tool-refused",
            {
                "calls": [asdict(c) for c in calls],
                "reason": type(error).__name__ + ": " + str(error),
                "tool_effect_entered": False,
            },
        )
        raise

    # No effects occurred above. These sequential operations are not atomic.
    messages.append(assistant)
    for call, option, expected in zip(calls, selected, feedbacks, strict=True):
        try:
            await guard()
            tool.validate(option)
        except (Exception, asyncio.CancelledError) as error:
            capture.add(
                "review-read-refused",
                {
                    "call": asdict(call),
                    "completed_acquisitions": reads,
                    "tool_effect_entered": False,
                    "reason": type(error).__name__ + ": " + str(error),
                },
            )
            raise

        async def admit(_call: Any, _argument: Any) -> None:  # noqa: ANN401
            await guard()
            capture.add("review-read-intent", {"call": asdict(_call)})

        claimed.add(cast("str", call.provider_call_id))
        try:
            disclosure = await execute_model_tool_call(
                call,
                invocation=invocation,
                tool=cast(
                    "Tool[SourceReadRequest, ContextDisclosure | SourceReadRefusal]",
                    tool,
                ),
                admit=admit,
                runner=ToolRunner(),
            )
        except (Exception, asyncio.CancelledError) as error:
            capture.add(
                "review-read-unresolved",
                {
                    "call": asdict(call),
                    "completed_acquisitions": reads,
                    "error": type(error).__name__ + ": " + str(error),
                    "entry": "claimed; completion unknown; no replay",
                },
            )
            raise
        if isinstance(disclosure, SourceReadRefusal):
            raise ValueError("Review source interval changed after preflight")
        feedback = source_feedback(option, disclosure.items[0].text)
        reads += 1
        name = f"read:{reads}"
        references[name] = _digest(feedback)
        capture.add(
            "review-read-result",
            {
                "call": asdict(call),
                "reference": name,
                "identity": references[name],
                "disclosure": feedback,
            },
        )
        if feedback != expected:
            raise ValueError("Review disclosure differs from authenticated preflight")
        messages.append(
            PromptMessage(
                "tool",
                json.dumps({"reference": name, **feedback}),
                tool_call_id=call.provider_call_id,
            ),
        )
    return reads

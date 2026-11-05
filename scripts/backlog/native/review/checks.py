# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, PLR0913 -- bounded read-only review evidence adapter
"""Select host-run fixed public observations; never execute worker code.

The trusted host runs FixedCheckTool under its own exact authorization and
freezes the result before review. The reviewer can only disclose that result.
"""

from __future__ import annotations

import json
from dataclasses import asdict, replace
from typing import TYPE_CHECKING, Any

from devtools.agents.coding.projection import request_bytes
from devtools.agents.coding.protocol import arguments
from devtools.context.repository.resource import ContentIdentity
from devtools.context.working import NoteScope
from devtools.models.interaction import ModelToolDefinition, Prompt, PromptMessage
from scripts.backlog.intake import _digest
from scripts.backlog.native.execution import check_data

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from devtools.models.interaction import ModelRequest, ModelResponse
    from devtools.tools.checks import FixedCheckPlan, FixedCheckResult
    from scripts.backlog.native.execution import Capture
    from scripts.backlog.native.review.notes import ReviewNotes

NAME = "inspect_public_check"
RECALL = "reopen_working_note"
SCHEMA = "review-public-observations-v1"
MAXIMUM_BYTES = 8192
MAXIMUM_OBSERVATIONS = 8


def observe(
    plan: FixedCheckPlan,
    result: FixedCheckResult,
    *,
    path: str,
    source: str,
    receipt: str,
) -> dict[str, Any]:
    """Freeze complete known output and exact declared inputs, not an explanation.

    This is a trusted host operation. The host is responsible for admitting the
    public definition and its dependency scope; the result alone cannot prove
    that an arbitrary command exercised a particular producer.
    """
    if (
        plan.source_scope is None
        or plan.select(result.check.name) != result.check
        or result.command_result.command != result.check.command
        or result.inputs_current is not True
        or result.input_error is not None
        or not receipt.strip()
        or source not in {"candidate", "baseline"}
    ):
        raise ValueError("Public observation needs a known source-bound fixed result")
    plan.source_scope.check_current()
    inputs = {
        str(r.address): str(r.content_identity)
        for r in plan.source_scope.snapshot.resources
    }
    command = result.check.command
    definition = {
        "name": result.check.name,
        "argv": list(command.argv),
        "cwd": str(command.working_directory),
        "timeout_seconds": command.timeout.total_seconds if command.timeout else None,
        "stdin_hex": command.stdin.hex() if command.stdin is not None else None,
        "environment": dict(command.environment) if command.environment else None,
        "success_exit_codes": sorted(command.success_exit_codes),
        "inputs": inputs,
    }
    outcome = check_data(result, "public-review-observation", receipt)
    # Preserve actual bytes as well as the ordinary human-readable diagnostics.
    outcome["stdout_hex"] = result.command_result.stdout.hex()
    outcome["stderr_hex"] = result.command_result.stderr.hex()
    if (
        path not in inputs
        or outcome["exit_code"] not in {0, 1}
        or outcome["outcome"] not in {"succeeded", "failed"}
        or outcome["stdout_truncated"]
        or outcome["stderr_truncated"]
        or outcome["events_dropped"]
    ):
        raise ValueError("Public observation is incomplete or has unknown effects")
    value = {
        "name": result.check.name,
        "source": source,
        "version": inputs[path],
        "resource": path,
        "definition": definition,
        "definition_sha256": _digest(definition),
        "receipt": receipt,
        "observation": outcome,
        "meaning": "Fixed public output only; explanations remain model claims.",
    }
    if len(json.dumps(value).encode()) > MAXIMUM_BYTES:
        raise ValueError("Public observation exceeds bounded disclosure")
    return value


def validate(packet: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Reauthenticate the host-frozen catalog against this exact review subject."""
    rows = packet.get("public_observations", {})
    if not isinstance(rows, dict) or len(rows) > MAXIMUM_OBSERVATIONS:
        raise ValueError("Finite public observation catalog required")
    for name, row in rows.items():
        evidence = packet["subject"]["evidence"]
        if (
            row["name"] != name
            or row["source"] not in {"candidate", "baseline"}
            or row["version"]
            != str(ContentIdentity.from_text(evidence[row["source"]]["text"]))
            or row["definition_sha256"] != _digest(row["definition"])
            or row["definition"]["inputs"].get(row["resource"]) != row["version"]
            or row["definition"]["name"] != name
            or row["definition"]["argv"] != row["observation"]["argv"]
            or row["observation"]["name"] != name
            or row["observation"]["inputs_current"] is not True
            or row["observation"]["exit_code"] not in {0, 1}
            or row["observation"]["outcome"] not in {"succeeded", "failed"}
            or row["observation"]["stdout_truncated"]
            or row["observation"]["stderr_truncated"]
            or row["observation"]["events_dropped"]
            or not row["receipt"].strip()
            or len(json.dumps(row).encode()) > MAXIMUM_BYTES
        ):
            raise PermissionError("Public observation source/definition/result differs")
    return rows


def tools(packet: dict[str, Any]) -> tuple[ModelToolDefinition, ...]:
    """Expose only a finite selector and optional retained-note recovery."""
    rows = validate(packet)
    if not rows:
        return ()
    properties = {
        "name": {"type": "string", "enum": list(rows)},
        "version": {
            "type": "string",
            "enum": sorted({r["version"] for r in rows.values()}),
        },
    }
    result = [
        ModelToolDefinition(
            NAME,
            "Inspect a host-run preauthorized fixed public check. Returns actual "
            "source-bound output; executes no code. Select a relevant check, "
            "test your hypothesis against its output, and cite public-check:<name>. "
            "A passed check is limited evidence, not full acceptance.",
            json.dumps(
                {
                    "type": "object",
                    "properties": properties,
                    "required": list(properties),
                    "additionalProperties": False,
                },
            ),
        ),
    ]
    if "working_notes" in packet:
        result.append(
            ModelToolDefinition(
                RECALL,
                "Reopen your retained note by sequence within this exact task, "
                "reviewer and episode; does not verify its interpretation.",
                json.dumps(
                    {
                        "type": "object",
                        "properties": {
                            "sequence": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 32,
                            },
                        },
                        "required": ["sequence"],
                        "additionalProperties": False,
                    },
                ),
            ),
        )
    return tuple(result)


async def acquire(
    packet: dict[str, Any],
    response: ModelResponse,
    request: ModelRequest,
    *,
    reads: int,
    messages: list[PromptMessage],
    references: dict[str, str],
    claimed: set[str],
    capture: Capture,
    guard: Callable[[], Awaitable[None]],
    memory: ReviewNotes | None,
) -> int:
    """Deliver one correlated immutable disclosure under existing read/call bounds."""
    await guard()
    rows = validate(packet)
    if len(response.tool_calls) != 1 or reads >= packet["policy"]["budgets"]["reads"]:
        raise PermissionError("Public observation acquisition bound exceeded")
    call = response.tool_calls[0]
    if (
        call.name not in {t.name for t in request.tools}
        or not call.provider_call_id
        or call.provider_call_id in claimed
    ):
        raise PermissionError("Undisclosed or repeated review evidence call")
    if call.name == NAME:
        args = arguments(call.arguments_json, {"name", "version"})
        if args["name"] not in rows or rows[args["name"]]["version"] != args["version"]:
            raise PermissionError("Public check not authorized for requested source")
        value = rows[args["name"]]
        reference = "public-check:" + args["name"]
    elif call.name == RECALL and memory is not None:
        expected = NoteScope(
            packet["subject"]["item"],
            "independent-reviewer:" + packet["policy"]["actor"],
            packet["sha256"],
        )
        if memory.scope != expected:
            raise PermissionError("Working note belongs to another reviewer episode")
        args = arguments(call.arguments_json, {"sequence"})
        sequence = args["sequence"]
        if type(sequence) is not int or not 1 <= sequence <= len(memory.book.notes):
            raise ValueError("Unavailable retained working note")
        note = memory.book.notes[sequence - 1]
        value = {
            "scope": asdict(memory.scope),
            "note": asdict(note),
            "status": memory.book.status(note),
        }
        reference = "working-note:" + str(sequence)
    else:
        raise PermissionError("Unsupported read-only review evidence request")
    identity = _digest(value)
    exchange = [
        PromptMessage(
            "assistant",
            response.content,
            tool_calls=response.tool_calls,
            reasoning_content=response.reasoning_content,
        ),
        PromptMessage(
            "tool",
            json.dumps({"reference": reference, **value}),
            tool_call_id=call.provider_call_id,
        ),
    ]
    following = replace(request, prompt=Prompt("", "messages", (*messages, *exchange)))
    reserve = (
        len(json.dumps(asdict(following)).encode())
        + 2 * packet["policy"]["budgets"]["response_bytes"]
        + 16384
    )
    if (
        request_bytes(following) > packet["policy"]["budgets"]["prompt_bytes"]
        or capture.used + reserve > capture.maximum
    ):
        raise ValueError("Review evidence cannot fit prompt/capture bounds")
    await guard()
    capture.add(
        "review-evidence-result",
        {
            "call": asdict(call),
            "reference": reference,
            "identity": identity,
            "disclosure": value,
        },
    )
    claimed.add(call.provider_call_id)
    references[reference] = identity
    messages.extend(exchange)
    return reads + 1

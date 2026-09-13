# Copyright (c) 2026
"""Parsing for the narrow Codex JSONL execution protocol."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from devtools.agents.integrations.codex.errors import CodexOutputError
from devtools.agents.integrations.codex.models import CodexTurnOutput


def parse_codex_turn_output(stdout: bytes) -> CodexTurnOutput:
    """Extract a completed Codex thread and final agent response from JSONL.

    Blank lines and unrelated events are ignored. A successful result requires
    ``thread.started``, at least one completed ``agent_message``, and
    ``turn.completed``. When Codex completes multiple agent messages, the last
    completed message is the final response.

    :param stdout: Complete untruncated JSONL stdout captured from Codex.
    :returns: The resumable Codex thread identifier and final agent message.
    :raises CodexOutputError: If the JSONL is malformed, explicitly failed, or
        missing required successful-turn values.
    """
    try:
        text = stdout.decode("utf-8")
    except UnicodeDecodeError as error:
        msg = "Codex JSONL stdout is not valid UTF-8."
        raise CodexOutputError(msg) from error

    state = _TurnState()

    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue

        event = _parse_event(line, line_number)
        _apply_event(event, line_number, state)

    if state.thread_id is None:
        msg = "Codex JSONL output did not include a thread.started identifier."
        raise CodexOutputError(msg)
    if state.final_message is None:
        msg = "Codex JSONL output did not include a completed agent message."
        raise CodexOutputError(msg)
    if not state.completed:
        msg = "Codex JSONL output did not include turn.completed."
        raise CodexOutputError(msg)

    return CodexTurnOutput(
        thread_id=state.thread_id,
        final_message=state.final_message,
    )


@dataclass(slots=True)
class _TurnState:
    """Accumulate just the recognized values from one Codex turn."""

    thread_id: str | None = None
    final_message: str | None = None
    completed: bool = False


def _apply_event(event: dict[str, Any], line_number: int, state: _TurnState) -> None:
    """Apply one recognized JSONL event to the current turn state."""
    event_type = event.get("type")
    if not isinstance(event_type, str):
        msg = f"Codex JSONL event {line_number} has no string type."
        raise CodexOutputError(msg)
    if event_type == "thread.started":
        state.thread_id = _required_thread_id(event, line_number)
    elif event_type == "item.completed":
        _apply_completed_item(event, line_number, state)
    elif event_type == "turn.failed":
        msg = f"Codex reported a failed turn at JSONL event {line_number}."
        raise CodexOutputError(msg)
    elif event_type == "turn.completed":
        state.completed = True


def _apply_completed_item(
    event: dict[str, Any],
    line_number: int,
    state: _TurnState,
) -> None:
    """Store a completed agent message, if this item represents one."""
    item = event.get("item")
    if not isinstance(item, dict):
        msg = f"Codex item.completed event {line_number} has no object item."
        raise CodexOutputError(msg)
    if item.get("type") == "agent_message":
        state.final_message = _required_string(item, "text", line_number)


def _parse_event(line: str, line_number: int) -> dict[str, Any]:
    """Parse one JSONL event object."""
    try:
        event = json.loads(line)
    except json.JSONDecodeError as error:
        msg = f"Codex JSONL event {line_number} is not valid JSON."
        raise CodexOutputError(msg) from error

    if not isinstance(event, dict):
        msg = f"Codex JSONL event {line_number} is not an object."
        raise CodexOutputError(msg)
    return event


def _required_thread_id(event: dict[str, Any], line_number: int) -> str:
    """Return a normalized nonblank thread identifier."""
    value = _required_string(event, "thread_id", line_number)
    if not value.strip():
        msg = f"Codex JSONL event {line_number} has a blank 'thread_id'."
        raise CodexOutputError(msg)
    if value != value.strip():
        msg = f"Codex JSONL event {line_number} has whitespace around 'thread_id'."
        raise CodexOutputError(msg)
    return value


def _required_string(event: dict[str, Any], field: str, line_number: int) -> str:
    """Return a string field required by a recognized event."""
    value = event.get(field)
    if not isinstance(value, str):
        msg = f"Codex JSONL event {line_number} has no string {field!r}."
        raise CodexOutputError(msg)
    return value

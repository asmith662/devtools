# Copyright (c) 2026
"""Usage-only Codex JSONL capture, independent of semantic-response acceptance."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Never

from devtools.agents.integrations.codex.errors import CodexOutputError
from devtools.models.interaction.usage import ModelUsage


@dataclass(frozen=True, slots=True)
class CodexUsage:
    """One reported turn aggregate; unknown request boundaries remain unknown."""

    thread_id: str | None
    turn_id: str | None
    ordinal: int
    counts: ModelUsage
    raw_json: str


def _invalid_usage() -> Never:
    """Reject an external event without obscuring the caller's capture boundary."""
    message = "Invalid Codex usage event"
    raise ValueError(message)


def capture_codex_usage(  # noqa: C901 -- one-pass external event state machine
    stdout: bytes,
) -> tuple[CodexUsage, ...]:
    """Retain completed-turn usage even when the process or artifact later fails.

    No completion event means no report, rather than a zero-token report.
    Duplicate completion without a new turn is ambiguous and rejected.
    This function never examines agent-message or reasoning content.
    """
    records: list[CodexUsage] = []
    thread: str | None = None
    turn: str | None = None
    completed = False
    identities: set[tuple[str | None, str]] = set()
    try:
        for line in stdout.decode("utf-8").splitlines():
            if not line.strip():
                continue
            event = json.loads(line)
            if not isinstance(event, dict):
                _invalid_usage()
            kind = event.get("type")
            if kind == "thread.started":
                thread = event.get("thread_id")
                if not isinstance(thread, str):
                    _invalid_usage()
            elif kind == "turn.started":
                turn = event.get("turn_id")
                if turn is not None and not isinstance(turn, str):
                    _invalid_usage()
                completed = False
            elif kind == "turn.completed":
                identity = (thread, turn)
                if completed or (turn is not None and identity in identities):
                    _invalid_usage()
                completed = True
                if turn is not None:
                    identities.add((thread, turn))
                raw = event.get("usage", {})
                if not isinstance(raw, dict):
                    _invalid_usage()
                counts = ModelUsage(
                    input_tokens=raw.get("input_tokens"),
                    cached_input_tokens=raw.get("cached_input_tokens"),
                    cache_write_tokens=raw.get("cache_write_input_tokens"),
                    output_tokens=raw.get("output_tokens"),
                    reasoning_tokens=raw.get("reasoning_output_tokens"),
                )
                records.append(
                    CodexUsage(
                        thread,
                        turn,
                        len(records) + 1,
                        counts,
                        json.dumps(raw, sort_keys=True, separators=(",", ":")),
                    ),
                )
    except (UnicodeError, ValueError, TypeError) as error:
        message = "Malformed or duplicate Codex usage stream"
        raise CodexOutputError(message) from error
    return tuple(records)

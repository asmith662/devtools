# Copyright (c) 2026
"""Bounded selection from the coding worker's captured native message history."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from devtools.models.interaction import PromptMessage

if TYPE_CHECKING:
    from collections.abc import Iterator


def _tool_results(messages: list[PromptMessage]) -> Iterator[dict[str, Any]]:
    """Inspect only archived host Tool results, not assistant claims."""
    for message in messages:
        if message.role != "tool":
            continue
        try:
            value = json.loads(message.content)
        except ValueError:
            continue
        if isinstance(value, dict):
            yield value


def _has_validation(messages: list[PromptMessage]) -> bool:
    """Recognize only host Tool-result validation fields, never infer a summary."""
    return any("validation" in value for value in _tool_results(messages))


def select_messages(
    history: list[PromptMessage],
    *,
    maximum_bytes: int = 24000,
    source_path: str | None = None,
) -> tuple[tuple[PromptMessage, ...], int]:
    """Retain the objective and newest complete exchanges, explicitly omit older ones.

    Full original messages remain in per-turn request/response/tools files. No
    synthesized summary or inferred memory replaces omitted source. Each boundary
    precedes an assistant message, so call/result groups are never split.
    """
    selected = list(history)
    omitted = 0
    while len(json.dumps([asdict(m) for m in selected]).encode()) > maximum_bytes:
        boundaries = [i for i, m in enumerate(selected) if m.role == "assistant"]
        if len(boundaries) < 2:  # noqa: PLR2004 -- keep the newest complete exchange
            msg = "Active structured Context byte budget exceeded."
            raise ValueError(msg)
        ranges = list(zip(boundaries, [*boundaries[1:], len(selected)], strict=True))
        latest_validation = next(
            (
                (start, end)
                for start, end in reversed(ranges)
                if _has_validation(selected[start:end])
            ),
            None,
        )
        protected = {latest_validation}
        observations = (
            [
                (start, end, value)
                for start, end in ranges
                for value in _tool_results(selected[start:end])
                if value.get("path") == source_path
                and isinstance(value.get("version"), str)
            ]
            if source_path is not None
            else []
        )
        if observations:
            version = observations[-1][2]["version"]
            reads = [
                (start, end, value)
                for start, end, value in observations
                if value["version"] == version and isinstance(value.get("text"), str)
            ]
            if reads:
                prefix = next(
                    (
                        (start, end)
                        for start, end, value in reversed(reads)
                        if value.get("span", [None])[0] == 0
                    ),
                    None,
                )
                # Native batches are indivisible; pinning every source-bearing
                # batch can itself exceed the byte budget. Prefer the current
                # prefix over later tails, otherwise retain the latest read.
                protected.add(prefix if prefix is not None else reads[-1][:2])
        removable = next(
            (
                (start, end)
                for start, end in ranges[:-1]
                if (start, end) not in protected
            ),
            None,
        )
        if removable is None:
            msg = (
                "Active structured Context byte budget cannot retain latest validation "
                "and selected current source reads."
            )
            raise ValueError(msg)
        first, following = removable
        omitted += following - first
        selected = [
            history[0],
            PromptMessage(
                "user",
                "HOST CONTEXT SELECTION: older complete exchanges omitted from this "
                "request for the byte budget. Exact originals remain in the run's "
                "turn-NN/request.json, response.json and tools.json. Re-read current "
                "source if needed; omitted observations do not establish "
                "current state.",
            ),
            *(selected[2:first] if selected[1].role == "user" else selected[1:first]),
            *selected[following:],
        ]
    return tuple(selected), omitted

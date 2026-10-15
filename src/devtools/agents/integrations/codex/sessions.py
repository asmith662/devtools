# Copyright (c) 2026
"""Metadata-only adapter for locally retained Codex usage records.

This external JSONL boundary streams past content events without decoding them.
Only token_usage_record metadata is decoded. Context metadata is extracted from
its scalar prefix before any instruction/content-bearing member; it is never
deserialized wholesale. Unsupported shapes remain unavailable, not inferred.
Streaming is necessary because generic filesystem.read is a bounded whole-file
operation and session logs can contain arbitrarily large private payloads.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, replace
from pathlib import Path

from devtools.agents.integrations.codex.usage import CodexUsage, capture_codex_usage
from devtools.core.time import Timestamp
from devtools.models.interaction.usage import ModelUsage

_KEY = re.compile(rb'(?<!\\)"([A-Za-z_]+)"\s*:')
_PRIVATE = re.compile(
    rb'(?<!\\)"(?:user_instructions|developer_instructions|base_instructions|instructions|messages|input|text|content|last_agent_message)"\s*:',
)
_FIELDS = {
    "timestamp",
    "ordinal",
    "type",
    "payload",
    "thread_id",
    "turn_id",
    "session_id",
    "root_turn_id",
    "response_id",
    "usage",
    "turn_token_usage",
    "thread_token_usage",
    "input_tokens",
    "cached_input_tokens",
    "cache_write_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
}


def _scalar(prefix: bytes, name: str) -> str | None:
    match = re.search(
        rb'(?<!\\)"' + name.encode() + rb'"\s*:\s*("(?:[^"\\]|\\.)*")',
        prefix,
    )
    return json.loads(match.group(1)) if match else None


def _counts(value: dict[str, int | None]) -> ModelUsage:
    return ModelUsage(
        input_tokens=value.get("input_tokens"),
        cached_input_tokens=value.get("cached_input_tokens"),
        cache_write_tokens=value.get("cache_write_input_tokens"),
        output_tokens=value.get("output_tokens"),
        reasoning_tokens=value.get("reasoning_output_tokens"),
        total_tokens=value.get("total_tokens"),
    )


@dataclass(frozen=True, slots=True)
class CodexSessionUsage:
    """One reported provider-response usage record, not an HTTP attempt count."""

    timestamp: Timestamp
    thread_id: str
    turn_id: str
    response_id: str
    usage: ModelUsage
    turn_usage: ModelUsage
    requested_model: str
    reasoning_effort: str
    project: str
    completed: bool | None
    metadata_digest: str


def read_session_usage(path: Path) -> tuple[CodexSessionUsage, ...]:  # noqa: C901 -- one-pass allowlisted external event state machine
    """Read allowlisted metadata only; no content-bearing event is deserialized."""
    rows = []
    model = effort = project = "UNKNOWN"
    provider = "UNKNOWN"
    completed: set[str] = set()
    with path.open("rb") as stream:
        for line in stream:
            header, separator, payload = line.partition(b'"payload"')
            kind = _scalar(header, "type")
            if not separator:
                continue
            if kind in {"session_meta", "turn_context", "event_msg"}:
                # Scalars following a private member are deliberately unavailable.
                private = _PRIVATE.search(payload)
                prefix = payload[: private.start()] if private else payload[:8192]
                if kind == "session_meta":
                    provider = _scalar(prefix, "model_provider") or "UNKNOWN"
                    cwd = _scalar(prefix, "cwd")
                    if cwd:
                        project = Path(cwd).name
                elif kind == "turn_context":
                    model = _scalar(prefix, "model") or model
                    effort = (
                        _scalar(prefix, "effort")
                        or _scalar(prefix, "reasoning_effort")
                        or effort
                    )
                elif _scalar(prefix, "type") == "task_complete":
                    turn_id = _scalar(prefix, "turn_id")
                    if turn_id:
                        completed.add(turn_id)
                continue
            if kind != "token_usage_record":
                continue
            # Reject unknown payload shapes before decoding. In particular, there
            # is no fallback that decodes prompts to find identity or usage.
            if not {k.decode() for k in _KEY.findall(line)} <= _FIELDS:
                continue
            value = json.loads(line)
            data = value["payload"]
            identities = [data.get(k) for k in ("thread_id", "turn_id", "response_id")]
            if not all(isinstance(v, str) and v for v in identities):
                continue
            if provider != "openai":
                message = "Unsupported or unreported local Codex provider"
                raise ValueError(message)
            rows.append(
                CodexSessionUsage(
                    Timestamp.from_isoformat(value["timestamp"]),
                    str(data["thread_id"]),
                    str(data["turn_id"]),
                    str(data["response_id"]),
                    _counts(data["usage"]),
                    _counts(data["turn_token_usage"]),
                    model,
                    effort,
                    project,
                    None,
                    hashlib.sha256(line).hexdigest(),
                ),
            )
    return tuple(
        replace(r, completed=True if r.turn_id in completed else None) for r in rows
    )


def read_exec_usage(path: Path) -> tuple[CodexUsage, ...]:
    """Project only allowlisted native exec metadata into the existing parser.

    Agent-message, reasoning and tool item lines are never deserialized. Event
    fields not supported by this narrow adapter fail closed rather than broaden
    the personal-data importer.
    """
    allowed = _FIELDS | {"id", "model"}
    retained = []
    with path.open("rb") as stream:
        for line in stream:
            kind = _scalar(line.partition(b'"item"')[0], "type")
            if kind not in {"thread.started", "turn.started", "turn.completed"}:
                continue
            if not {k.decode() for k in _KEY.findall(line)} <= allowed:
                message = "Unsupported exec usage metadata shape"
                raise ValueError(message)
            retained.append(line)
    return capture_codex_usage(b"\n".join(retained))

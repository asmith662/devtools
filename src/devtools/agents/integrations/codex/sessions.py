# Copyright (c) 2026
"""Metadata-only adapter for locally retained Codex usage records.

This external JSONL boundary streams past content events without decoding them.
Only bounded candidate metadata is decoded, then admitted by decoded member
names and shape. Rejected candidate values may exist transiently during parsing;
they are never returned or included in diagnostics. Context metadata is extracted
from its direct scalar prefix before an unsupported member; it is never decoded
wholesale. Unsupported shapes remain unavailable, not inferred.
Streaming is necessary because generic filesystem.read is a bounded whole-file
operation and session logs can contain arbitrarily large private payloads.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import TYPE_CHECKING

from devtools.agents.integrations.codex.usage import CodexUsage, capture_codex_usage
from devtools.core.time import Timestamp
from devtools.core.time.errors import TimestampParsingError
from devtools.models.interaction.usage import ModelUsage

_KEY = re.compile(rb'(?<!\\)"([A-Za-z_]+)"\s*:')
if TYPE_CHECKING:
    from collections.abc import Iterator

_MAX_METADATA_BYTES = 65536
_CONTEXT_FIELDS = {
    "model_provider",
    "cwd",
    "model",
    "effort",
    "reasoning_effort",
    "type",
    "turn_id",
}
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
    try:
        return json.loads(match.group(1)) if match else None
    except (UnicodeError, ValueError):
        return None


def _lines(path: Path) -> Iterator[tuple[bytes, bool]]:
    """Bound each allocation, draining oversized content without decoding it."""
    with path.open("rb") as stream:
        while line := stream.readline(_MAX_METADATA_BYTES + 1):
            oversized = len(line) > _MAX_METADATA_BYTES
            if oversized and not line.endswith(b"\n"):
                while tail := stream.readline(_MAX_METADATA_BYTES + 1):
                    if tail.endswith(b"\n"):
                        break
            yield line, oversized


def _context(prefix: bytes) -> dict[str, str]:
    """Project only direct allowed string members; stop before unknown values."""
    result: dict[str, str] = {}
    decoder = json.JSONDecoder()
    try:
        text = prefix[:8192].decode("utf-8").lstrip(" \t\r\n:{")
        while text:
            key, end = decoder.raw_decode(text)
            if key not in _CONTEXT_FIELDS:
                break
            if key in result:
                return {}
            text = text[end:].lstrip()
            if not text.startswith(":"):
                break
            text = text[1:].lstrip()
            if not text.startswith('"'):
                break
            value, end = decoder.raw_decode(text)
            result[key] = value
            text = text[end:].lstrip()
            if not text.startswith(","):
                break
            text = text[1:].lstrip()
    except (UnicodeError, ValueError, TypeError):
        pass  # An incomplete prefix cannot establish further metadata.
    return result


def _metadata(line: bytes, allowed: set[str]) -> dict[str, object] | None:
    """Decode bounded candidates with an authoritative closed member policy."""
    # Cheap rejection of obvious private fields precedes decoding. This is only
    # an optimization; escaped names are checked by the decoder below.
    if not {key.decode() for key in _KEY.findall(line)} <= allowed:
        return None

    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in items:
            if key not in allowed or key in result or isinstance(value, list):
                raise ValueError
            result[key] = value
        return result

    def constant(_value: str) -> object:
        raise ValueError

    try:
        value = json.loads(line, object_pairs_hook=pairs, parse_constant=constant)
        if isinstance(value, dict):
            return value
    except (UnicodeError, ValueError, TypeError, RecursionError):
        pass
    return None


def _counts(value: object) -> ModelUsage:
    if not isinstance(value, dict) or any(
        v is not None and (not isinstance(v, int) or isinstance(v, bool))
        for v in value.values()
    ):
        raise ValueError
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


def read_session_usage(path: Path) -> tuple[CodexSessionUsage, ...]:  # noqa: C901, PLR0912 -- one-pass allowlisted external event state machine
    """Read admitted metadata; content events and oversized usage are skipped."""
    rows = []
    model = effort = project = "UNKNOWN"
    provider = "UNKNOWN"
    completed: set[str] = set()
    for line, oversized in _lines(path):
        header, separator, payload = line.partition(b'"payload"')
        kind = _scalar(header, "type")
        if not separator:
            continue
        if kind in {"session_meta", "turn_context", "event_msg"}:
            prefix = _context(payload)
            if kind == "session_meta":
                provider = prefix.get("model_provider") or "UNKNOWN"
                cwd = prefix.get("cwd")
                if cwd:
                    project = Path(cwd).name
            elif kind == "turn_context":
                model = prefix.get("model") or model
                effort = (
                    prefix.get("effort") or prefix.get("reasoning_effort") or effort
                )
            elif prefix.get("type") == "task_complete":
                turn_id = prefix.get("turn_id")
                if turn_id:
                    completed.add(turn_id)
            continue
        if kind != "token_usage_record" or oversized:
            continue
        value = _metadata(line, _FIELDS)
        if value is None or not isinstance(data := value.get("payload"), dict):
            continue
        identities = [data.get(k) for k in ("thread_id", "turn_id", "response_id")]
        if not all(isinstance(v, str) and v for v in identities):
            continue
        if provider != "openai":
            message = "Unsupported or unreported local Codex provider"
            raise ValueError(message)
        try:
            row = CodexSessionUsage(
                Timestamp.from_isoformat(str(value["timestamp"])),
                str(data["thread_id"]),
                str(data["turn_id"]),
                str(data["response_id"]),
                _counts(data.get("usage")),
                _counts(data.get("turn_token_usage")),
                model,
                effort,
                project,
                None,
                hashlib.sha256(line).hexdigest(),
            )
        except (ValueError, TypeError, KeyError, TimestampParsingError):
            continue
        rows.append(row)
    return tuple(
        replace(r, completed=True if r.turn_id in completed else None) for r in rows
    )


def read_exec_usage(path: Path) -> tuple[CodexUsage, ...]:
    """Admit bounded metadata by decoded names before retaining parser input.

    Content events remain unparsed. Unknown/duplicate members, invalid encoding,
    unsupported values and oversized candidate lines refuse with sanitized text.
    Parsing a rejected candidate is not a promise of zero transient exposure.
    """
    allowed = _FIELDS | {"id", "model"}
    retained = []
    for line, oversized in _lines(path):
        kind = _scalar(line.partition(b'"item"')[0], "type")
        if kind not in {"thread.started", "turn.started", "turn.completed"}:
            continue
        value = None if oversized else _metadata(line, allowed)
        valid = value is not None
        if value is not None and kind == "turn.completed":
            try:
                _counts(value.get("usage", {}))
            except (ValueError, TypeError):
                valid = False
        if not valid:
            # Raise outside the decoder's exception handler: no raw document or
            # rejected value is retained through exception causes/context.
            message = "Unsupported exec usage metadata shape"
            raise ValueError(message)
        retained.append(json.dumps(value).encode("utf-8"))
    return capture_codex_usage(b"\n".join(retained))

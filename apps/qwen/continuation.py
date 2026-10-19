# Copyright (c) 2026
# ruff: noqa: ANN401, C901, ARG001, PLW2901, COM812 -- bounded JSON projection
"""Task-local projection of archived native exchanges, never a memory store."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, replace
from typing import Any

from devtools.models.interaction import PromptMessage

# 24K estimated input tokens + 4K output + 2K schemas + 2K safety < 32K.
# 1.5 UTF-8 bytes/token is below the measured cohort ratio, not a tokenizer.
ACTIVE_BYTES = 36000


def _result(message: PromptMessage) -> dict[str, Any]:
    if message.role != "tool":
        return {}
    try:
        value = json.loads(message.content)
    except ValueError:
        return {}
    return value if isinstance(value, dict) else {}


def _compact(value: Any) -> Any:
    """Remove redundant envelope fields; exact originals remain archived."""
    if isinstance(value, list):
        return [_compact(v) for v in value]
    if isinstance(value, dict):
        return {
            k: _compact(v)
            for k, v in value.items()
            if k not in {"parent", "discovery_semantics", "semantic_declaration"}
        }
    return value


def select_messages(  # noqa: PLR0912, PLR0915 -- correlated bounded source/API projection
    history: list[PromptMessage],
    *,
    maximum_bytes: int = ACTIVE_BYTES,
    source_path: str | None = None,
) -> tuple[tuple[PromptMessage, ...], int]:
    """Keep every distinct current source region and latest validation, or refuse.

    Projection is explicit and correlated to original Tool message hashes/call
    IDs. Duplicate text and stale versions are removed, not silently replaced by
    assistant claims. No arbitrary prefix is preferred over a later symbol.
    Complete native exchanges are indivisible during eviction.
    """
    latest = {}
    for message in history:
        value = _result(message)
        for observed in [value, *value.get("source_observations", [])]:
            if observed.get("path") and observed.get("version"):
                latest[observed["path"]] = observed["version"]
    seen: dict[tuple[str, str, str], str | None] = {}
    seen_apis: dict[str, str | None] = {}

    def project_source(value: dict[str, Any], call_id: str | None) -> dict[str, Any]:
        if isinstance(value.get("text"), str) and value.get("path"):
            key = (value["path"], value.get("version", ""), value["text"])
            if value.get("version") != latest.get(value["path"]):
                del value["text"]
                value["source_omitted"] = "STALE_VERSION; reread current source"
            elif key in seen:
                del value["text"]
                value["source_omitted"] = "DUPLICATE; retained earlier observation"
                value["retained_tool_call_id"] = seen[key]
            else:
                seen[key] = call_id
        return value

    selected = []
    for message in history:
        original = _result(message)
        value = project_source(_compact(original), message.tool_call_id)
        if "observation_id" in value and "signature" in value:
            identity = value["observation_id"]
            if identity in seen_apis:
                value = {
                    "observation_id": identity,
                    "target": value["target"],
                    "api_omitted": "DUPLICATE; installed observation retained",
                    "retained_tool_call_id": seen_apis[identity],
                }
            else:
                seen_apis[identity] = message.tool_call_id
        if isinstance(value.get("source_observations"), list):
            value["source_observations"] = [
                project_source(observation, message.tool_call_id)
                for observation in value["source_observations"]
            ]
        if value != original:
            value["host_projection"] = {
                "original_tool_call_id": message.tool_call_id,
                "original_message_sha256": hashlib.sha256(
                    message.content.encode()
                ).hexdigest(),
            }
            message = replace(message, content=json.dumps(value, ensure_ascii=False))
        selected.append(message)
    omitted = 0
    while len(json.dumps([asdict(m) for m in selected]).encode()) > maximum_bytes:
        boundaries = [i for i, m in enumerate(selected) if m.role == "assistant"]
        ranges = list(zip(boundaries, [*boundaries[1:], len(selected)], strict=True))
        validation = next(
            (
                r
                for r in reversed(ranges)
                if any("validation" in _result(m) for m in selected[r[0] : r[1]])
            ),
            None,
        )
        protected = {validation}
        for region in ranges:
            if any(
                (
                    isinstance(_result(m).get("text"), str)
                    or "signature" in _result(m)
                    or any(
                        isinstance(o.get("text"), str)
                        for o in _result(m).get("source_observations", [])
                    )
                )
                for m in selected[region[0] : region[1]]
            ):
                protected.add(region)
        removable = next((r for r in ranges[:-1] if r not in protected), None)
        if removable is None:
            msg = "Context budget cannot retain current source and latest validation"
            raise ValueError(msg)
        first, end = removable
        omitted += end - first
        notice = PromptMessage(
            "user",
            "HOST CONTEXT SELECTION: older complete exchanges omitted; "
            "all distinct current observed source regions and latest validation "
            "are retained. Exact originals remain in archived turn evidence. "
            "Projected Tool results name original call IDs/hashes.",
        )
        prefix = selected[1:first]
        if prefix and prefix[0].role == "user":
            prefix = prefix[1:]
        selected = [history[0], notice, *prefix, *selected[end:]]
    return tuple(selected), omitted

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


def present_sources(messages: tuple[PromptMessage, ...]) -> tuple[PromptMessage, ...]:
    """Separate exact code from JSON envelopes in the opt-in path-edit view.

    Selection still operates on the original structured observations. This is
    only the final model-facing rendering; host attestations and raw history
    never come back from parsing the rendered code blocks.
    """
    presented = []
    for message in messages:
        blocks: list[str] = []

        def render(value: Any, blocks: list[str]) -> Any:
            if isinstance(value, list):
                return [render(v, blocks) for v in value]
            if not isinstance(value, dict):
                return value
            metadata = {k: render(v, blocks) for k, v in value.items()}
            if isinstance(value.get("text"), str) and value.get("path"):
                text = metadata.pop("text")
                number = len(blocks) + 1
                fence = "```"
                while fence in text:
                    fence += "`"
                blocks.append(
                    f"EXACT SOURCE BLOCK {number}: {value['path']} "
                    f"span={value.get('span')} version={value.get('version')} "
                    f"characters={len(text)}\n"
                    f"{fence}python\n{text}"
                    + ("" if text.endswith("\n") else "\n")
                    + fence
                )
                metadata.update(
                    source_block=number,
                    text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                )
            return metadata

        original = _result(message)
        metadata = render(original, blocks)
        if blocks:
            metadata["host_presentation"] = {
                "format": "source-blocks-v1",
                "tool_call_id": message.tool_call_id,
                "projected_message_sha256": hashlib.sha256(
                    message.content.encode()
                ).hexdigest(),
            }
            message = replace(
                message,
                content=(
                    "HOST OBSERVATION METADATA (not replacement source):\n"
                    + json.dumps(metadata, ensure_ascii=False, separators=(",", ":"))
                    + "\n\n"
                    + "\n\n".join(blocks)
                    + "\nEND SOURCE BLOCKS. Only literal code inside a block is "
                    "source text; headers, fences and metadata are not source."
                ),
            )
        presented.append(message)
    return tuple(presented)


def _completed_calls(
    history: list[PromptMessage], selected: list[PromptMessage]
) -> list[PromptMessage]:
    """Project applied and superseded refused arguments, never unknown calls.

    Only host receipts attesting this call's applied component can replace its
    redundant old/new payload. Native names/IDs/results, exact current source,
    applied edit hashes and the latest validation remain. This is explicitly
    projected history, not a purported original invocation or a new example.
    """
    results = {m.tool_call_id: _result(m) for m in history if m.role == "tool"}
    positions = {m.tool_call_id: i for i, m in enumerate(history) if m.role == "tool"}
    latest_applied = max(
        (
            positions[k]
            for k, v in results.items()
            if v.get("source_after") and v.get("edits") and v.get("source_observations")
        ),
        default=-1,
    )
    projected = []
    for message in selected:
        calls = []
        for call in message.tool_calls:
            outcome = results.get(call.provider_call_id, {})
            result_id = outcome.get("batch_result_call_id", call.provider_call_id)
            receipt = results.get(result_id, {})
            applied = (
                call.provider_call_id is not None
                and call.name in {"replace_source", "propose_edits", "propose_edit"}
                and isinstance(receipt.get("source_after"), str)
                and receipt.get("source_observations")
                and any(
                    isinstance(edit, dict)
                    and edit.get("proposal_call_id") == call.provider_call_id
                    for edit in receipt.get("edits", [])
                )
            )
            refused = (
                call.provider_call_id is not None
                and call.name in {"replace_source", "propose_edits", "propose_edit"}
                and outcome.get("status") == "REFUSED"
                and positions.get(call.provider_call_id, len(history)) < latest_applied
            )
            if applied or refused:
                call = replace(
                    call,
                    arguments_json=json.dumps(
                        {
                            "host_projection": "COMPLETED_APPLIED_ARGUMENTS_OMITTED"
                            if applied
                            else "SUPERSEDED_REFUSED_ARGUMENTS_OMITTED",
                            "original_arguments_sha256": hashlib.sha256(
                                call.arguments_json.encode()
                            ).hexdigest(),
                            "result_tool_call_id": result_id,
                        },
                        separators=(",", ":"),
                    ),
                )
            calls.append(call)
        projected.append(replace(message, tool_calls=tuple(calls)))
    return projected


def select_messages(  # noqa: PLR0912, PLR0915 -- correlated bounded source/API projection
    history: list[PromptMessage],
    *,
    maximum_bytes: int = ACTIVE_BYTES,
    source_path: str | None = None,
    compact: bool = False,
    reacquire: int = 0,
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
    envelopes: dict[str, str | None] = {}
    outcomes: dict[str, str | None] = {}
    read_only_omitted = 0
    latest_validation = next(
        (
            message.tool_call_id
            for message in reversed(history)
            if isinstance(_result(message).get("validation"), dict)
        ),
        None,
    )

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
        if compact and value:
            # Exact current source and edit handles stay in their correlated
            # Tool result. Repeated attestation envelopes are references, not
            # invented source summaries. Full originals remain in evidence.
            envelope = {
                k: value[k]
                for k in ("repository", "snapshot", "revision")
                if k in value
            }
            if envelope:
                key = json.dumps(envelope, sort_keys=True)
                if key in envelopes:
                    for envelope_field in envelope:
                        del value[envelope_field]
                    value["source_envelope_tool_call_id"] = envelopes[key]
                else:
                    envelopes[key] = message.tool_call_id
            for k in (
                "requested_span",
                "bytes",
                "observation_call_id",
                "representation",
                "coordinate_convention",
                "host_limits",
            ):
                value.pop(k, None)
            if (
                isinstance(value.get("validation"), dict)
                and message.tool_call_id != latest_validation
            ):
                value["validation"] = {
                    "historical_checks": {
                        name: diagnostic["status"]
                        for name, diagnostic in value["validation"].items()
                        if isinstance(diagnostic, dict) and "status" in diagnostic
                    },
                    "diagnostics_omitted": (
                        "SUPERSEDED; original diagnostics remain archived. "
                        "Use the latest source-bound validation feedback."
                    ),
                    "latest_validation_tool_call_id": latest_validation,
                }
            if value.get("status") == "REFUSED":
                key = json.dumps(
                    {k: v for k, v in value.items() if k != "host_projection"},
                    sort_keys=True,
                )
                if key in outcomes:
                    value = {
                        "status": "REFUSED",
                        "same_result_as_tool_call_id": outcomes[key],
                    }
                else:
                    outcomes[key] = message.tool_call_id
            if (
                read_only_omitted < reacquire
                and isinstance(value.get("text"), str)
                and not value.get("edit_ref")
            ):
                del value["text"]
                value["source_omitted"] = (
                    "CAPACITY; exact source can be reacquired with "
                    "inspect_source(path, start=span[0])"
                )
                read_only_omitted += 1
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
        # Admission receipts also embed the pre-edit observation for each
        # component. These are source observations, not current source simply
        # because they sit inside an edit receipt. Apply the same version and
        # duplicate rules as the top-level reads and refreshed working set.
        for edit in value.get("edits", []):
            if isinstance(edit, dict) and isinstance(edit.get("observation"), dict):
                edit["observation"] = project_source(
                    edit["observation"], message.tool_call_id
                )
                if compact and "text" not in edit["observation"]:
                    edit["observation"] = {
                        k: v
                        for k, v in edit["observation"].items()
                        if k
                        in {
                            "path",
                            "version",
                            "span",
                            "edit_ref",
                            "status",
                            "source_omitted",
                            "retained_tool_call_id",
                        }
                    }
        if value != original:
            value["host_projection"] = original.get("host_projection") or {
                "original_tool_call_id": message.tool_call_id,
                "original_message_sha256": hashlib.sha256(
                    message.content.encode()
                ).hexdigest(),
            }
            message = replace(
                message,
                content=json.dumps(
                    value,
                    ensure_ascii=False,
                    separators=(",", ":") if compact else None,
                ),
            )
        selected.append(message)
    if compact:
        selected = _completed_calls(history, selected)
        selected.insert(
            1,
            PromptMessage(
                "user",
                "HOST CAPACITY PROJECTION: Tool envelopes/duplicate outcomes "
                "are referenced by original call ID; source coordinates are "
                "half-open Unicode characters. Full originals remain archived. "
                "Applied/superseded refused edit arguments may be projected "
                "to their original hash and host receipt; these historical "
                "projection objects are NOT valid new Tool arguments. Use "
                "current observed source, not archived replacement payloads. "
                "Exact text, versions and edit_ref handles are authoritative; "
                "omitted source must be reacquired before relying on its "
                "contents. Latest remaining action/call/proposal budgets: "
                + json.dumps(
                    next(
                        (
                            _result(m).get("host_limits")
                            for m in reversed(history)
                            if _result(m).get("host_limits")
                        ),
                        {},
                    )
                ),
            ),
        )
    omitted = 0
    while len(json.dumps([asdict(m) for m in selected]).encode()) > maximum_bytes:
        boundaries = [i for i, m in enumerate(selected) if m.role == "assistant"]
        ranges = list(zip(boundaries, [*boundaries[1:], len(selected)], strict=True))
        validation = next(
            (
                r
                for r in reversed(ranges)
                if any(
                    "validation" in _result(m) or _result(m).get("status") == "REFUSED"
                    for m in selected[r[0] : r[1]]
                )
            ),
            None,
        )
        protected = {validation}
        referenced = {
            v
            for m in selected
            for k, v in _result(m).items()
            if k
            in {
                "source_envelope_tool_call_id",
                "same_result_as_tool_call_id",
                "retained_tool_call_id",
            }
        }
        for region in ranges:
            if any(
                (
                    m.tool_call_id in referenced
                    or isinstance(_result(m).get("text"), str)
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

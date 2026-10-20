# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, PLR2004 -- explicit bounded application contract
"""Atomic proposal admission composed from the existing exact-edit primitive."""

from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING, Any

from apps.qwen.development_task import _source_patch, _structured_edit_patch
from apps.qwen.model_tool_composition import normalize_tool_descriptor
from apps.qwen.patch_proposal_worker import PatchProposalError
from apps.qwen.two_action_read_only_experiment import _object_without_duplicate_keys
from devtools.context import RepositoryResourceAddress
from devtools.models.interaction import ModelToolCall
from devtools.tools import ToolDescriptor

if TYPE_CHECKING:
    from pathlib import Path

    from apps.qwen.context_tools import ContextTools
    from devtools.models.interaction import ModelToolDefinition

MAX_TRANSACTION_EDITS = 16


def observed_definition() -> ModelToolDefinition:
    """Flat native strings; the host resolves path, version and API evidence."""
    return normalize_tool_descriptor(
        ToolDescriptor(
            "replace_source",
            "Propose an exact replacement using edit_ref from an actual source read "
            "or host feedback. No path/version hashes needed. old_text is an exact "
            "unique snippet inside that observation; empty means its whole region "
            "(or authorized absent file). new_text is literal Python source, never "
            "JSON syntax. Return multiple replace_source calls in ONE response for "
            "up to 16 coordinated regions/files: the host admits the entire batch "
            "atomically, then validates. Each old/new region is at most 4096 "
            "UTF-8 bytes; all old+new text totals at most 8192 bytes. "
            "No writes occur on refusal.",
            json.dumps(
                {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "reference": {"type": "string", "pattern": "^R[1-9][0-9]*$"},
                        "old_text": {"type": "string", "maxLength": 4096},
                        "new_text": {"type": "string", "maxLength": 4096},
                    },
                    "required": ["reference", "old_text", "new_text"],
                }
            ),
        )
    )


def admit_observed(  # noqa: C901 -- resolve references before the existing atomic admission
    root: Path,
    sources: dict[str, str],
    calls: tuple[ModelToolCall, ...],
    tools: ContextTools,
) -> tuple[dict[str, str], dict[str, str], list[dict[str, Any]], dict[str, Any]]:
    """Resolve observed references, then reuse the sole atomic admission engine."""
    if not 1 <= len(calls) <= MAX_TRANSACTION_EDITS:
        raise PatchProposalError("One to sixteen coordinated calls required")
    tools.check_current()
    rows = []
    refs = []
    for call in calls:
        try:
            value = json.loads(
                call.arguments_json, object_pairs_hook=_object_without_duplicate_keys
            )
        except (ValueError, TypeError) as error:
            raise PatchProposalError("Malformed observed replacement") from error
        if (
            call.name != "replace_source"
            or not isinstance(value, dict)
            or set(value) != {"reference", "old_text", "new_text"}
        ):
            raise PatchProposalError("Malformed observed replacement contract")
        if not all(isinstance(v, str) for v in value.values()):
            raise PatchProposalError("Replacement arguments must be strings")
        observation = tools.edit_references.get(value["reference"])
        if observation is None:
            raise PatchProposalError(
                "Unknown source observation reference; read source first"
            )
        path, version = observation["path"], observation["version"]
        old = value["old_text"] or observation["text"]
        if observation.get("status") != "ABSENT":
            resource = tools.snapshot.resource_at(RepositoryResourceAddress(path))
            if version != str(resource.content_identity):
                raise PatchProposalError(
                    "Stale source observation reference; read CURRENT source"
                )
            first, last = observation["span"]
            if (
                observation["text"] != sources[path][first:last]
                or not old
                or old.replace("\r\n", "\n")
                not in observation["text"].replace("\r\n", "\n")
            ):
                message = (
                    "Old text is outside referenced observed source: "
                    f"{value['reference']} ({path}, span [{first}, {last})). "
                    "Use the observation covering this exact anchor or inspect "
                    "that source region again; no component was applied."
                )
                raise PatchProposalError(message)
        elif value["old_text"]:
            raise PatchProposalError("Absent source requires empty old_text")
        rows.append(
            {
                "path": path,
                "version": version,
                "old_text": old,
                "new_text": value["new_text"],
            }
        )
        refs.append(
            {
                "reference": value["reference"],
                "observation": observation,
                "call_id": call.provider_call_id,
            }
        )
    composed = ModelToolCall(
        "propose_edits",
        json.dumps(
            {
                "plan": "Host resolved native observed replacements",
                "api_evidence": list(tools.api_observations),
                "edits": rows,
            }
        ),
        calls[0].provider_call_id,
    )
    patches, updated, metadata, plan = admit_transaction(root, sources, composed, tools)
    for item, ref in zip(metadata, refs, strict=True):
        item.update(
            proposal_call_id=ref["call_id"],
            observation_reference=ref["reference"],
            observation=ref["observation"],
        )
    plan["resolved_observations"] = refs
    return patches, updated, metadata, plan


def transaction_definition(
    paths: tuple[str, ...], *, api_required: bool = True
) -> ModelToolDefinition:
    """Describe bounded coordinated proposals; no mutation Tool is exposed."""
    text = {"type": "string", "minLength": 1, "maxLength": 4096}
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "plan": {
                "type": "string",
                "minLength": 1,
                "maxLength": 4096,
                "description": (
                    "Brief behavior/compatibility plan, coordinated regions, "
                    "API evidence and preserved invariants; not internal reasoning."
                ),
            },
            "api_evidence": {
                "type": "array",
                "maxItems": 8 if api_required else 0,
                "description": "Exact inspect_api observation IDs only. Use [] "
                "when no APIs are required; never cite prose or source hashes.",
                "items": {"type": "string", "minLength": 64, "maxLength": 64},
            },
            "edits": {
                "type": "array",
                "minItems": 1,
                "maxItems": MAX_TRANSACTION_EDITS,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "path": {"type": "string", "enum": list(paths)},
                        "version": {"type": "string", "minLength": 64, "maxLength": 64},
                        "old_text": {**text, "minLength": 0},
                        "new_text": {**text, "minLength": 0},
                    },
                    "required": ["path", "version", "old_text", "new_text"],
                },
            },
        },
        "required": ["plan", "api_evidence", "edits"],
    }
    return normalize_tool_descriptor(
        ToolDescriptor(
            "propose_edits",
            (
                "Propose one atomic implementation. Include imports, helpers "
                "and function changes together (up to 16 edits); CURRENT observed "
                "pre-edit versions. Any invalid/overlapping edit rejects the proposal. "
                "Total old+new UTF-8 text <=8192 bytes; each region <=4096. Cite "
                "host-required API observations. No writes or shell authority."
            ),
            json.dumps(schema),
        )
    )


def admit_transaction(  # noqa: C901, PLR0912, PLR0915 -- authenticate all edits before writes
    root: Path,
    sources: dict[str, str],
    call: ModelToolCall,
    tools: ContextTools,
) -> tuple[dict[str, str], dict[str, str], list[dict[str, Any]], dict[str, Any]]:
    """Return combined source/diffs and provenance only after complete admission."""
    try:
        values = json.loads(
            call.arguments_json, object_pairs_hook=_object_without_duplicate_keys
        )
    except (ValueError, TypeError) as error:
        raise PatchProposalError("Malformed edit transaction") from error
    if (
        call.name != "propose_edits"
        or not isinstance(values, dict)
        or set(values) != {"plan", "api_evidence", "edits"}
    ):
        raise PatchProposalError("Malformed edit transaction contract")
    if not isinstance(values["plan"], str) or not 1 <= len(values["plan"]) <= 4096:
        raise PatchProposalError("Bounded implementation plan required")
    refs = values["api_evidence"]
    if (
        not isinstance(refs, list)
        or len(refs) > 8
        or any(not isinstance(x, str) or x not in tools.api_observations for x in refs)
    ):
        raise PatchProposalError("Unverified API evidence")
    verified = {tools.api_observations[x]["target"] for x in refs}
    if not set(tools.task.api_targets) <= verified:
        raise PatchProposalError("Required API contracts not inspected")
    rows = values["edits"]
    if not isinstance(rows, list) or not 1 <= len(rows) <= MAX_TRANSACTION_EDITS:
        raise PatchProposalError("Transaction requires one to sixteen edits")
    tools.check_current()
    intervals: dict[str, list[dict[str, Any]]] = {}
    metadata = []
    total = 0
    for row in rows:
        if not isinstance(row, dict) or set(row) != {
            "path",
            "version",
            "old_text",
            "new_text",
        }:
            raise PatchProposalError("Malformed transaction component")
        path = row["path"]
        if (
            not isinstance(path, str)
            or path not in sources
            or path not in tools.task.sources
        ):
            raise PatchProposalError("Unauthorized transaction path")
        if path in tools.task.new_paths and not (root / path).exists():
            if (
                row["version"] != tools.absent_observations.get(path)
                or not row["version"]
                or row["old_text"] != ""
                or not isinstance(row["new_text"], str)
                or not 1 <= len(row["new_text"].encode()) <= 4096
                or path in intervals
            ):
                raise PatchProposalError(
                    "New source requires observed exact absence and bounded content"
                )
            total += len(row["new_text"].encode())
            if total > 8192:
                raise PatchProposalError(
                    "Transaction exceeds existing aggregate edit bytes"
                )
            item = {
                "path": path,
                "version": row["version"],
                "start": 0,
                "end": 0,
                "new_length": len(row["new_text"]),
                "new_text": row["new_text"],
                "old_text": "",
            }
            intervals[path] = [item]
            metadata.append(
                {k: v for k, v in item.items() if k not in {"old_text", "new_text"}}
                | {
                    "created": True,
                    "old_text_sha256": hashlib.sha256(b"").hexdigest(),
                    "new_text_sha256": hashlib.sha256(
                        row["new_text"].encode()
                    ).hexdigest(),
                    "proposal_call_id": call.provider_call_id,
                }
            )
            continue
        resource = tools.snapshot.resource_at(RepositoryResourceAddress(path))
        if row["version"] != str(resource.content_identity):
            raise PatchProposalError("Stale transaction source version")
        # Reuse all exact/unique/newline/size/path checks from the existing edit.
        legacy = ModelToolCall(
            "propose_edit",
            json.dumps({k: row[k] for k in ("path", "old_text", "new_text")}),
            call.provider_call_id,
        )
        _structured_edit_patch(
            root, sources[path], legacy, source_path=path, allow_empty_new=True
        )
        if not tools.observed(row["old_text"], path=path):
            raise PatchProposalError("Edit source was not observed at current version")
        newline = "\r\n" if "\r\n" in sources[path] else "\n"
        old = row["old_text"].replace("\r\n", "\n").replace("\n", newline)
        new = row["new_text"].replace("\r\n", "\n").replace("\n", newline)
        start = sources[path].index(old)
        end = start + len(old)
        total += len(old.encode()) + len(new.encode())
        if total > 8192:
            raise PatchProposalError(
                "Transaction exceeds existing aggregate edit bytes"
            )
        for previous in intervals.get(path, []):
            if start < previous["end"] and previous["start"] < end:
                raise PatchProposalError("Overlapping transaction anchors")
        item = {
            "path": path,
            "version": row["version"],
            "start": start,
            "end": end,
            "new_length": len(new),
            "old_text": old,
            "new_text": new,
        }
        intervals.setdefault(path, []).append(item)
        metadata.append(
            {k: v for k, v in item.items() if k not in {"old_text", "new_text"}}
            | {
                "old_text_sha256": hashlib.sha256(old.encode()).hexdigest(),
                "new_text_sha256": hashlib.sha256(new.encode()).hexdigest(),
                "proposal_call_id": call.provider_call_id,
            }
        )
    updated = {}
    patches = {}
    for path, changes in intervals.items():
        content = sources[path]
        for item in sorted(changes, key=lambda r: r["start"], reverse=True):
            content = (
                content[: item["start"]] + item["new_text"] + content[item["end"] :]
            )
        if len(content.encode()) > 32768:
            raise PatchProposalError("Combined source exceeds existing source bytes")
        updated[path] = content
        patches[path] = _source_patch(
            root,
            sources[path],
            content,
            source_path=path,
            new_file=not (root / path).exists(),
        )
    if sum(len(p.encode()) for p in patches.values()) > 16384:
        raise PatchProposalError("Combined patch exceeds existing patch bytes")
    return patches, updated, metadata, values

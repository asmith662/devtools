# Copyright (c) 2026
# ruff: noqa: INP001 -- non-installable experiment composition
"""Explicit task-local terminal capture; no arbitrary exception serialization.

Frozen historical runners remain unchanged. New experiments can use this
bounded projection of known coding-result fields; it is not a recovery record.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import TYPE_CHECKING

from devtools.agents.coding.projection import ProjectionCapacityError, ProjectionOutcome
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.agents.coding.models import CodingResult


def projection_record(outcome: ProjectionOutcome) -> dict[str, object]:
    """Retain decisions and identities, excluding Prompt/source payloads."""
    return {
        "status": outcome.status,
        "triggered": outcome.triggered,
        "original_bytes": outcome.original_bytes,
        "resulting_bytes": outcome.resulting_bytes,
        "target_bytes": outcome.target_bytes,
        "hard_bytes": outcome.hard_bytes,
        "selected_indices": outcome.selected_indices,
        "omitted_exchanges": outcome.omitted_exchanges,
        "shortened_indices": outcome.shortened_indices,
        "active_sources": [
            {
                "identity": o.identity,
                "snapshot": str(o.snapshot_id),
                "repository": str(o.repository_id),
                "version": str(o.unit.resource.content_identity),
                "path": str(o.unit.resource.address),
                "span": o.span,
            }
            for o in outcome.active_sources
        ],
        "invalidated_source_identities": outcome.invalidated_source_identities,
    }


def error_record(error: BaseException | None) -> dict[str, object] | None:
    """Record known safe capacity details; other messages are not privacy vetted."""
    if error is None:
        return None
    known = isinstance(error, ProjectionCapacityError)
    return {
        "class": type(error).__name__,
        "message": str(error) if known else "Unclassified exception; message withheld.",
        "message_policy": "known-capacity-only",
        "projection": projection_record(error.outcome)
        if isinstance(error, ProjectionCapacityError)
        else None,
        "other_details": "not captured; no exception internals or traceback locals",
    }


def result_record(result: CodingResult) -> dict[str, object]:
    """Enumerate known terminal, usage, effect and custody facts without deepcopy."""
    state = result.progress
    return {
        "disposition": result.disposition,
        "accepted": result.accepted,
        "candidate_validated": result.candidate_validated,
        "completed": result.completed,
        "failure_phase": result.failure_phase,
        "error": error_record(result.error),
        "completion_error": error_record(result.completion_error),
        "progress": {
            "limits": {
                "model_calls": state.limits.model_calls,
                "proposals": state.limits.proposals,
                "tool_actions": state.limits.tool_actions,
                "call_timeout_seconds": state.limits.call_timeout.total_seconds,
                "wall_timeout_seconds": state.limits.wall_timeout.total_seconds,
                "completion_check": state.limits.completion_check,
            },
            "number": state.number,
            "model_calls": state.model_calls,
            "proposals": state.proposals,
            "actions": state.actions,
            "phase": state.phase,
            "candidate_validated": state.candidate_validated,
            "effects": [
                {
                    "kind": e.kind,
                    "native_call_ids": e.native_call_ids,
                    "acknowledged": e.acknowledged,
                    "check_name": e.check_name,
                }
                for e in state.effects
            ],
            "usage": [asdict(u) if u is not None else None for u in state.usage],
        },
        "custody": {
            "restored": result.custody.restored,
            "reconciliation_required": result.custody.reconciliation_required,
            "error": error_record(result.custody.error),
        },
        "qualification": (
            "Unknown usage/custody remains null; "
            "unacknowledged effects are not failed effects."
        ),
    }


def save_result(path: Path, result: CodingResult) -> bool:
    """Write once, or a separate minimal capture-failure receipt, never success.

    If storage itself is unavailable the fallback can also fail; propagate that
    failure instead of claiming durable evidence or replaying the execution.
    """
    try:
        value = result_record(result)
        write(
            TextFile(resolve_path(path), json.dumps(value, indent=2) + "\n"),
            overwrite=False,
        )
    except Exception as error:  # noqa: BLE001 -- capture boundary; no execution retry
        minimal = {
            "capture": "failed",
            "capture_error_class": type(error).__name__,
            "coding_disposition": result.disposition,
            "coding_error_class": type(result.error).__name__ if result.error else None,
            "accepted": False,
            "qualification": (
                "Full result unavailable in this receipt; no inferred effects."
            ),
        }
        write(
            TextFile(
                resolve_path(path.with_suffix(".capture-failed.json")),
                json.dumps(minimal, indent=2) + "\n",
            ),
            overwrite=False,
        )
        return False
    return True

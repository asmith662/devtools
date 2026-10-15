# Copyright (c) 2026
# ruff: noqa: ANN401 -- explicit normalized invocation capture boundary
"""Mandatory acceptance accounting and provenance-preserving unique aggregation."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import require

CATEGORIES = (
    "input_tokens",
    "cached_input_tokens",
    "cache_write_tokens",
    "output_tokens",
    "reasoning_tokens",
)
SHA256_HEX_CHARACTERS = 64


def accept(capture: Any, domain: str) -> dict[str, Any]:
    """Return a separate acceptance projection; never rewrite the original capture."""
    measured = capture["measurement"]
    require(
        capture["usage_error"] is None
        and measured["completed"]
        and measured["validated"],
        "Completed validated usage capture required",
    )
    require(
        all(measured["usage"][key] is not None for key in CATEGORIES),
        "Mandatory scientific usage is UNKNOWN",
    )
    return {
        **capture,
        "measurement": {**measured, "accepted": True},
        "acceptance_domain": domain,
        "original_capture_sha256": digest(json_bytes(capture)),
    }


@dataclass(frozen=True)
class UsageTotals:
    """Separate provider categories; no overlapping total or subscription charge."""

    invocations: int
    input_tokens: int | None
    cached_input_tokens: int | None
    cache_write_tokens: int | None
    output_tokens: int | None
    reasoning_tokens: int | None


def aggregate(captures: tuple[dict[str, Any], ...]) -> UsageTotals:
    """Attribute an original invocation once, including adopted provenance views."""
    unique: dict[str, Any] = {}
    for capture in captures:
        measured = capture["measurement"]
        identity = measured["invocation_id"]
        comparable = {
            k: measured[k]
            for k in (
                "usage",
                "requested_model",
                "reasoning_effort",
                "disclosure_digest",
                "wall_seconds",
                "backend_thread_id",
            )
        }
        if identity in unique:
            require(
                comparable == unique[identity],
                "Conflicting original/adopted invocation usage",
            )
        else:
            unique[identity] = comparable
    totals = []
    for key in CATEGORIES:
        values = [value["usage"][key] for value in unique.values()]
        totals.append(
            sum(values) if all(value is not None for value in values) else None,
        )
    return UsageTotals(len(unique), *totals)


def adopted(capture: dict[str, Any], seal_sha256: str) -> dict[str, Any]:
    """Project immutable original usage without a new invocation or token charge."""
    require(
        len(seal_sha256) == SHA256_HEX_CHARACTERS
        and capture["measurement"]["accepted"],
        "Accepted original capture and branch seal required",
    )
    projected = deepcopy(capture)
    return {
        **projected,
        "measurement": {**projected["measurement"], "execution_origin": "ADOPTED"},
        "original_capture_sha256": digest(json_bytes(capture)),
        "branch_seal_sha256": seal_sha256,
    }

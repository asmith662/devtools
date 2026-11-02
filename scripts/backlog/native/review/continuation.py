# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, SLF001, C901, PLR2004 -- one closed prospective continuation
"""Authenticate one known legacy batch failure, never rank or retry judgments."""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any

from devtools.agents.coding.protocol import READ, arguments
from devtools.core.time import Timestamp
from devtools.models.interaction import ModelTermination
from scripts.backlog.intake import load_json
from scripts.backlog.work import _load

if TYPE_CHECKING:
    from pathlib import Path

    from scripts.backlog.native.review.actor import NativeReviewer

LEGACY_BATCH_FAILURE = "PermissionError: Review permits one bounded read per response"


def predecessor(
    reviewer: NativeReviewer,
    item: str,
    current: dict[str, Any],
) -> dict[str, Any]:
    """Require completed transport, zero Tool entries and no engineering judgment.

    Historical expiry does not erase a known valid completion. It never supplies
    current authority: the new subject requires a fresh independently bounded grant.
    Only the established legacy single-read batch barrier qualifies in this v2.
    """
    legacy = reviewer.owner.reviewer
    packet, grant, dispatch, proposal = (
        legacy.record(item, name)
        for name in ("subject", "authorization", "dispatch", "proposal")
    )
    if (
        packet["subject"] != current
        or packet["scope"] != reviewer.scope
        or grant["scope"] != reviewer.scope
        or grant["subject_sha256"] != packet["sha256"]
        or dispatch["subject_sha256"] != packet["sha256"]
        or dispatch["authorization_sha256"] != grant["sha256"]
        or proposal["subject_sha256"] != packet["sha256"]
        or proposal["authorization_sha256"] != grant["sha256"]
        or proposal["dispatch_sha256"] != dispatch["sha256"]
        or proposal["actor"] != packet["policy"]["actor"]
        or proposal["source"] != packet["policy"]["source"]
        or proposal["profile"] != packet["policy"]["profile"]
        or proposal["status"] != "blocked"
        or proposal["conclusion"] is not None
        or proposal["host_approved"] is not False
        or proposal["error"] != LEGACY_BATCH_FAILURE
        or proposal["model_calls"] != 1
        or proposal["reads"] != 0
        or proposal["references"] != current["references"]
        or len(proposal["observations"]) != 2
        or not current["evidence"]["acceptance"]["passed"]
        or not current["evidence"]["acceptance"]["inputs_current"]
    ):
        raise PermissionError(
            "Continuation requires the known unentered legacy batch failure",
        )
    observations = []
    for number, ref in enumerate(proposal["observations"]):
        if ref["file"] != f"observation-{number:04d}.json":
            raise PermissionError("Incomplete or ambiguous prior review effects")
        value = _load(
            legacy.folder(item) / ref["file"],
            "backlog-native-observation-v1",
        )
        if value["sha256"] != ref["sha256"]:
            raise PermissionError("Prior review observation changed")
        observations.append(value)
    intent, returned = observations
    if (
        intent["kind"] != "review-model-intent"
        or returned["kind"] != "review-model-returned"
    ):
        raise PermissionError("Prior review entry/completion is uncertain")
    response, request = returned["response"], intent["request"]
    calls = response["tool_calls"]
    disclosed = json.loads(request["prompt"]["messages"][1]["content"])
    if (
        response["source"]["value"] != packet["policy"]["source"]
        or response["termination"] != ModelTermination.TOOL_CALL
        or not 1 < len(calls) <= packet["policy"]["budgets"]["reads"]
        or any(c["name"] != READ.name or not c["provider_call_id"] for c in calls)
        or len({c["provider_call_id"] for c in calls}) != len(calls)
        or request["settings"] != packet["policy"]["settings"]
        or request["tools"] != packet["tools"]
        or request["conversation"] is not None
        or disclosed["subject"] != current
        or disclosed["review_scope"]["read_paths"] != packet["policy"]["read_paths"]
    ):
        raise PermissionError("Prior response does not prove the bounded batch barrier")
    for call in calls:
        values = arguments(
            call["arguments_json"],
            {"path", "start"},
            optional=frozenset({"end"}),
        )
        if (
            values["path"] not in packet["policy"]["read_paths"]
            or type(values["start"]) is not int
            or values["start"] < 0
            or (
                "end" in values
                and (type(values["end"]) is not int or values["end"] < values["start"])
            )
        ):
            raise PermissionError("Prior batch contained an unauthorized acquisition")
    times = [
        Timestamp.from_isoformat(v).value
        for v in (
            grant["issued_at"],
            dispatch["at"],
            intent["at"],
            returned["at"],
            grant["expires_at"],
        )
    ]
    if times != sorted(times) or times[-2] >= times[-1]:
        raise PermissionError("Prior completion lacks valid historical authority")
    # Any host judgment is consequential; do not shop for a replacement judgment.
    for path in reviewer.owner.cycle._folder(item).glob("review-*.json"):
        decision = read_decision(path)
        if (
            decision.get("proposal_sha256") == proposal["sha256"]
            or "proposal_sha256" not in decision
        ):
            raise PermissionError("A host-disposed review cannot be continued")
    return {
        "number": 2,
        "continuation_limit": 1,
        "previous_subject_sha256": packet["sha256"],
        "previous_authorization_sha256": grant["sha256"],
        "previous_dispatch_sha256": dispatch["sha256"],
        "previous_proposal_sha256": proposal["sha256"],
        "failure": "legacy-read-batch-limit-no-effects-v1",
    }


def validate(reviewer: NativeReviewer, item: str, packet: dict[str, Any]) -> None:
    """Reauthenticate the exact parent on new effects and downstream admission."""
    attempt = packet["attempt"]
    correction = attempt.get("correction_reference")
    if (
        not isinstance(correction, str)
        or not correction.strip()
        or len(correction) > 2048
        or attempt
        != {
            **predecessor(reviewer, item, packet["subject"]),
            "correction_reference": correction,
        }
    ):
        raise PermissionError("Review continuation binding differs")


def read_decision(path: Path) -> dict[str, Any]:
    """Select only the declared v1/v2 host record; never choose a favorable attempt."""
    schema = load_json(path)["schema"]
    if schema not in {"backlog-native-review-v1", "backlog-native-review-v2"}:
        raise ValueError("Unsupported native host review schema")
    decision = _load(path, schema)
    attempt = decision.get("review_subject_sha256")
    if schema.endswith("v2"):
        if (
            not isinstance(attempt, str)
            or not re.fullmatch(r"[a-f0-9]{64}", attempt)
            or not decision.get("proposal_sha256")
        ):
            raise PermissionError(
                "Versioned host review requires one exact attempt/proposal",
            )
    elif "review_subject_sha256" in decision:
        raise PermissionError("Legacy review cannot silently select a continuation")
    return decision

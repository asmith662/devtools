# Copyright (c) 2026
# ruff: noqa: ANN401 -- narrow experiment authority artifact, not framework governance
"""Separate a trusted maintainer grant from durable exact-run authorization."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from devtools.core.time import Timestamp
from devtools.core.time.errors import TimestampParsingError
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import require

SCHEMA = "experiment-execution-approval-v1"


@dataclass(frozen=True)
class ApprovalRequest:
    """Carry authority already granted by a maintainer at a trusted host boundary.

    Validation never produces this value. A future Agent tool must receive a
    host-issued grant; it must not expose this constructor or approve as a model
    capability. Python objects are not a security sandbox against arbitrary code
    with repository credentials. The host authenticates the principal/decision.
    """

    run_id: str
    principal: str
    reference: str
    kind: str = "TRUSTED_HOST"

    def validate(self, run_id: str) -> None:
        """Reject implicit, foreign or unidentified authority requests."""
        require(self.run_id == run_id, "Approval request names another run")
        require(
            self.kind in {"MAINTAINER_CLI", "TRUSTED_HOST"}
            and bool(self.principal.strip())
            and bool(self.reference.strip()),
            "Explicit maintainer authority required",
        )


@dataclass(frozen=True)
class ExecutionAuthorization:
    """Reference a committed authenticated approval, never mere plan validity."""

    run_id: str
    plan_sha256: str
    approval_sha256: str
    checkpoint: str


def approval(
    request: ApprovalRequest,
    binding: dict[str, Any],
    timestamp: str,
) -> dict[str, Any]:
    """Build a deterministic immutable receipt for a supplied audit timestamp."""
    request.validate(binding["run_id"])
    body = {
        "schema": SCHEMA,
        **binding,
        "authority": {
            "kind": request.kind,
            "principal": request.principal,
            "reference": request.reference,
            "action": "EXECUTE_EXACT_RUN_ONCE",
        },
        "approved_at": timestamp,
    }
    return {**body, "sha256": digest(json_bytes(body))}


def authenticate(value: Any, binding: dict[str, Any]) -> None:
    """Check exact schema, prospective binding, authority and self digest."""
    require(isinstance(value, dict), "Malformed execution approval")
    require(
        set(value) == {"schema", *binding, "authority", "approved_at", "sha256"}
        and value["schema"] == SCHEMA
        and all(value[name] == expected for name, expected in binding.items()),
        "Approval prospective binding differs",
    )
    authority = value["authority"]
    require(
        isinstance(authority, dict)
        and set(authority) == {"kind", "principal", "reference", "action"}
        and authority["action"] == "EXECUTE_EXACT_RUN_ONCE"
        and all(isinstance(v, str) for v in authority.values()),
        "Malformed approval authority",
    )
    ApprovalRequest(
        binding["run_id"],
        authority["principal"],
        authority["reference"],
        authority["kind"],
    ).validate(binding["run_id"])
    timestamp = value["approved_at"]
    require(isinstance(timestamp, str), "Malformed approval timestamp")
    try:
        canonical_timestamp = Timestamp.from_isoformat(timestamp).isoformat()
    except TimestampParsingError as error:
        message = "Malformed approval timestamp"
        raise ValueError(message) from error
    require(
        canonical_timestamp == timestamp,
        "Approval timestamp must be canonical aware UTC",
    )
    require(
        value["sha256"]
        == digest(json_bytes({k: v for k, v in value.items() if k != "sha256"})),
        "Approval artifact digest differs",
    )

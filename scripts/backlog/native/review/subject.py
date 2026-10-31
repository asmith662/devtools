# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, SLF001, E501 -- bounded administrative evidence projection
"""Authenticate native subjects and disclose an explicit review-only projection."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from scripts.backlog.intake import _digest, _read

if TYPE_CHECKING:
    from scripts.backlog.native.lifecycle import NativeMaintenance


async def subject(owner: NativeMaintenance, item: str) -> dict[str, Any]:
    """Keep private implementation, controls and worker reasoning undisclosed."""
    assignment, result = owner.record(item, "assignment"), owner.record(item, "result")
    if assignment["item"] != item or result["item"] != item:
        raise PermissionError("Review records belong to another task")
    await owner.validate(assignment)
    source, patch_hash = owner._candidate(assignment, result)
    facts, task = result["facts"], assignment["task"]
    checks = facts["checks"]
    if (
        not checks
        or not checks[-1]
        or any(
            not c["passed"]
            or not c["inputs_current"]
            or c["stdout_truncated"]
            or c["stderr_truncated"]
            or c["events_dropped"]
            for c in checks[-1]
        )
    ):
        raise PermissionError("Review requires complete final public check evidence")
    if (
        facts["completed"] is not True
        or facts["error"]
        or facts["completion_error"]
        or facts["acceptance_error"]
    ):
        raise PermissionError("Review requires known completion and acceptance")
    evidence = {
        "task": {"objective": task["objective"], "obligations": task["obligations"]},
        "scope": {
            "edit": task["source"],
            "read": list(assignment["inputs"]),
            "checks": task["tests"],
            "worker": task["worker"],
        },
        "baseline": {
            "path": task["source"],
            "text": assignment["baseline_source"],
            "identity": assignment["inputs"][task["source"]],
        },
        "candidate": {
            "path": task["source"],
            "text": source,
            "sha256": result["candidate_sha256"],
        },
        "diff": {
            "text": _read(owner.cycle._folder(item) / "candidate.patch"),
            "sha256": patch_hash,
        },
        "public-checks": checks,
        "acceptance": {
            k: facts["acceptance"][k]
            for k in ("passed", "exit_code", "seconds", "inputs_current")
        },
        "custody": {
            "restored": facts["restored"],
            "checkout_released": result["checkout_released"],
            "release": result["checkout_release"],
            "reconciliation_required": facts["reconciliation_required"],
        },
        "effects": facts["effects"],
        "information": {
            "readiness": facts["readiness"],
            "disclosures": facts["disclosures"],
        },
        "limits": {
            "environment": facts["environment_qualification"],
            "private_acceptance": "Outcome only; private implementation, controls and diagnostics withheld",
            "independence": "Host attestation, not proof from model labels or content hashes",
            "current_source": "Working source is restored baseline; candidate is archived, never installed for review",
        },
    }
    return {
        "item": item,
        "assignment_sha256": assignment["sha256"],
        "result_sha256": result["sha256"],
        "candidate_sha256": result["candidate_sha256"],
        "configuration": assignment["configuration"],
        "inputs": assignment["inputs"],
        "evidence": evidence,
        "references": {name: _digest(value) for name, value in evidence.items()},
    }

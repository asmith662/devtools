# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, C901, PLR0912, COM812 -- bounded administrative eligibility
"""Coding continuation eligibility; identities and execution remain native-owned."""

from __future__ import annotations

import difflib
import getpass
import hashlib
from typing import TYPE_CHECKING, Any

from devtools.core.time import Timestamp
from scripts.backlog.intake import _read
from scripts.backlog.work import _load

if TYPE_CHECKING:
    from scripts.backlog.checkout import Checkout
    from scripts.backlog.native.lifecycle import NativeMaintenance


async def predecessor(
    owner: NativeMaintenance,
    item: str,
    policy: str,
    checkout: Checkout | None = None,
    *,
    disclose_public: bool = False,
) -> dict[str, Any]:
    """Authenticate a known public failure, never infer safety from BLOCKED alone."""
    if type(disclose_public) is not bool:
        raise ValueError("Explicit public diagnostic disclosure selection required")
    active = owner.cycle.routine.active(policy, item)
    maximum = active["policy"].get("coding_attempts", 1)
    if not 1 < owner.attempt <= maximum:
        raise PermissionError("Coding attempt limit exhausted or not activated")
    parent = owner.select(owner.attempt - 1)
    assignment = parent.record(item, "assignment")
    if checkout is None:
        await parent.validate(assignment)
    grant = parent.record(item, "authorization")
    dispatch = parent.record(item, "dispatch")
    issued = Timestamp.from_isoformat(grant["issued_at"]).value
    expires = Timestamp.from_isoformat(grant["expires_at"]).value
    if (
        grant["assignment_sha256"] != assignment["sha256"]
        or grant["principal"] != getpass.getuser()
        or grant["scope"] != assignment["scope"]
        or not issued <= Timestamp.from_isoformat(dispatch["at"]).value < expires
    ):
        raise PermissionError("Prior execution lacks valid historical authority")
    execution = parent.record(item, "execution")
    result = parent.record(item, "result")
    facts = result["facts"]
    if (
        dispatch["assignment_sha256"] != assignment["sha256"]
        or dispatch["authorization_sha256"] != grant["sha256"]
        or result["assignment_sha256"] != assignment["sha256"]
        or result["authorization_sha256"] != grant["sha256"]
        or result["execution_sha256"] != execution["sha256"]
        or any(
            result[k] != v
            for k, v in execution.items()
            if k not in {"schema", "sha256", "seconds"}
        )
        or result["disposition"] != "BLOCKED"
        or result["execution_error"] is not None
        or not result["checkout_released"]
        or facts["coding_accepted"]
        or facts["coding_disposition"] != "proposal_limit"
        or not facts["completed"]
        or facts["error"] is not None
        or facts["completion_error"] is not None
        or facts["acceptance"] is not None
        or facts["acceptance_error"] is not None
        or facts["restored"] is not True
        or facts["reconciliation_required"]
        or not facts["effects"]
        or any(not effect["acknowledged"] for effect in facts["effects"])
    ):
        raise PermissionError(
            "Continuation requires known terminal public-validation failure"
        )
    releases = [
        _load(p, "backlog-checkout-owner-v1")
        for p in (owner.cycle.root / ".local/backlog/checkout-history").glob("*.json")
    ]
    if not any(
        r["sha256"] == result["checkout_release"]
        and r["operation"] == "native:" + assignment["sha256"]
        for r in releases
    ):
        raise PermissionError("Authenticated Checkout release required")
    checks = facts["checks"]
    if not checks or not checks[-1] or not any(not c["passed"] for c in checks[-1]):
        raise PermissionError("Final public failure required")
    for group in checks:
        for check in group:
            if (
                not check["inputs_current"]
                or check["stdout_truncated"]
                or check["stderr_truncated"]
                or check["events_dropped"]
                or check["exit_code"] not in (0, 1)
            ):
                raise PermissionError("Incomplete or uncertain public diagnostics")
    observed = []
    for ref in facts["observations"]:
        if (
            not ref["file"].startswith("observation-")
            or "/" in ref["file"]
            or "\\" in ref["file"]
        ):
            raise PermissionError("Invalid observation address")
        row = _load(
            parent.folder(item) / "worker" / ref["file"],
            "backlog-native-observation-v1",
        )
        if row["sha256"] != ref["sha256"]:
            raise PermissionError("Prior observation changed")
        if not issued <= Timestamp.from_isoformat(row["at"]).value < expires:
            raise PermissionError("Prior effect exceeded historical authority")
        if row["kind"] == "public-check-result":
            observed.append(row["checks"])
    if observed != checks:
        raise PermissionError("Public diagnostics lack authenticated observations")
    candidate = _read(parent.folder(item) / "worker/final-source.py")
    patch = _read(parent.folder(item) / "candidate.patch")
    expected = "".join(
        difflib.unified_diff(
            assignment["baseline_source"].splitlines(keepends=True),
            candidate.splitlines(keepends=True),
            fromfile="a/" + assignment["task"]["source"],
            tofile="b/" + assignment["task"]["source"],
        )
    )
    if (
        hashlib.sha256(candidate.encode()).hexdigest() != result["candidate_sha256"]
        or patch != expected
    ):
        raise PermissionError("Prior candidate/diff changed")
    return {
        "number": owner.attempt,
        "policy": policy,
        "assignment_sha256": assignment["sha256"],
        "result_sha256": result["sha256"],
        "failure": "terminal-public-validation-v1",
        "disclose_public": disclose_public,
        "feedback": {
            "failure": (
                "Previous candidate failed public validation; source was restored."
            ),
            "public_checks": [
                {k: c[k] for k in ("name", "exit_code", "stdout", "stderr")}
                for c in checks[-1]
            ]
            if disclose_public
            else [],
        },
    }


async def validate(
    owner: NativeMaintenance,
    assignment: dict[str, Any],
    checkout: Checkout | None = None,
) -> None:
    """Recheck eligibility and obligation identity at every governed boundary."""
    link = assignment.get("continuation")
    if owner.attempt == 1:
        if link is not None:
            raise PermissionError("Historical slot cannot become a continuation")
        return
    if not isinstance(link, dict) or link != await predecessor(
        owner,
        assignment["item"],
        link["policy"],
        checkout,
        disclose_public=link["disclose_public"],
    ):
        raise PermissionError("Continuation predecessor changed")
    original = owner.select(owner.attempt - 1).record(assignment["item"], "assignment")
    previous = {
        k: v
        for k, v in original["task"].items()
        if k not in {"worker", "settings", "budgets"}
    }
    current = {
        k: v
        for k, v in assignment["task"].items()
        if k not in {"worker", "settings", "budgets"}
    }
    if previous != current or original["inputs"] != assignment["inputs"]:
        raise PermissionError("Continuation task obligations or source drifted")

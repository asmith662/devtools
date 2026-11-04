# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, C901, PLR0912, COM812 -- bounded administrative eligibility
"""Coding continuation eligibility; identities and execution remain native-owned."""

from __future__ import annotations

import difflib
import getpass
import hashlib
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools.core.time import Timestamp
from scripts.backlog.checkout import restored_release
from scripts.backlog.intake import _digest, _read
from scripts.backlog.work import _load

if TYPE_CHECKING:
    from scripts.backlog.checkout import Checkout
    from scripts.backlog.native.lifecycle import NativeMaintenance

COLLECTION_ERROR_EXIT = 2


def _source_syntax_failure(check: dict[str, Any], source: str) -> bool:
    """Recognize only complete collection SyntaxErrors attributed to the edit target."""
    text = check["stdout"] + "\n" + check["stderr"]
    if any(
        word in text for word in ("KeyboardInterrupt", "INTERNALERROR", "UsageError")
    ):
        return False
    blocks = text.split("ERROR collecting ")[1:]
    if not blocks:
        return False
    for block in blocks:
        last_file = None
        syntax = False
        for line in block.splitlines():
            if 'File "' in line:
                last_file = line.split('File "', 1)[1].split('"', 1)[0]
            exception = re.match(r"\s*E\s+([A-Z][\w.]*):", line)
            if exception:
                if exception[1] != "SyntaxError" or last_file != source:
                    return False
                syntax = True
        if not syntax:
            return False
    return True


def public_failure(
    assignment: dict[str, Any],
    facts: dict[str, Any],
    rows: list[dict[str, Any]],
    candidate: str,
) -> None:
    """Bind final validation to the exact acknowledged candidate and edit chronology."""
    source = assignment["task"]["source"]
    current = _digest(assignment["baseline_source"])
    pending_edit: str | None = None
    pending_check: tuple[str, int] | None = None
    edits = 0
    checked: list[tuple[str, int, list[dict[str, Any]]]] = []
    for row in rows:
        kind = row["kind"]
        if kind == "edit-intent":
            changes = row["changes"]
            if (
                pending_edit is not None
                or pending_check is not None
                or len(changes) != 1
                or changes[0]["path"] != source
                or changes[0]["before_sha256"] != current
                or changes[0]["after_sha256"] == current
                or not isinstance(changes[0]["after_sha256"], str)
                or re.fullmatch(r"[a-f0-9]{64}", changes[0]["after_sha256"]) is None
            ):
                raise PermissionError("Uncertain prior edit chronology")
            pending_edit = changes[0]["after_sha256"]
        elif kind == "edit-completed":
            if pending_edit is None or row["paths"] != [source]:
                raise PermissionError("Prior edit lacks authenticated completion")
            current, pending_edit = pending_edit, None
            edits += 1
        elif kind == "public-check-intent":
            if (
                pending_edit is not None
                or pending_check is not None
                or not row.get("snapshot")
            ):
                raise PermissionError("Uncertain prior check chronology")
            pending_check = (current, edits)
        elif kind == "public-check-result":
            if pending_check != (current, edits):
                raise PermissionError("Prior public result lacks current check intent")
            checked.append((current, edits, row["checks"]))
            pending_check = None
    if (
        pending_edit is not None
        or pending_check is not None
        or not checked
        or checked[-1][:2] != (current, edits)
        or current != _digest(candidate)
        or edits != sum(e["kind"] == "edit" for e in facts["effects"])
        or len(checked) != sum(e["kind"] == "check" for e in facts["effects"])
    ):
        raise PermissionError(
            "Final candidate lacks complete current public validation"
        )
    final = checked[-1]
    if not final[2] or not any(c["exit_code"] == 1 for c in final[2]):
        raise PermissionError("Terminal ordinary public failure required")
    source_path = str(Path(assignment["coordinator"]) / source)
    for index, (identity, edit_count, group) in enumerate(checked):
        if not group:
            raise PermissionError("Empty prior public check group")
        for check in group:
            code = check["exit_code"]
            if type(code) is not int or check["name"] != "public":
                raise PermissionError("Unknown public check outcome")
            if code in (0, 1):
                if check["passed"] != (code == 0) or (
                    code == 1 and check["outcome"] != "failed"
                ):
                    raise PermissionError("Inconsistent public check outcome")
                continue
            if (
                code != COLLECTION_ERROR_EXIT
                or index == len(checked) - 1
                or edit_count == 0
                or edit_count >= final[1]
                or identity == final[0]
                or check["passed"]
                or check["outcome"] != "failed"
                or not _source_syntax_failure(check, source_path)
            ):
                raise PermissionError("Incomplete or uncertain public diagnostics")


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
    restored_release(
        owner.cycle,
        result["checkout_release"],
        operation="native:" + assignment["sha256"],
        branch=assignment["branch"],
        revision=assignment["base_head"],
    )
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
            ):
                raise PermissionError("Incomplete or uncertain public diagnostics")
    observed = []
    rows = []
    for number, ref in enumerate(facts["observations"]):
        if (
            ref["file"] != f"observation-{number:04d}.json"
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
        rows.append(row)
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
    public_failure(assignment, facts, rows, candidate)
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

# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, TRY301, PLR2004 -- fixed application-level validation composition
"""Scoped change reports for CodingCommands, not a validation or Git substrate."""

from __future__ import annotations

import asyncio
import json
import re
import time
from typing import TYPE_CHECKING, Any

from apps.qwen.commands import CHECKS, _bundle_state, _input_identity, _plan_identity
from apps.qwen.development_task import _hash, _save
from apps.qwen.patch_proposal_worker import _read_text
from devtools.resources.commands import CommandError
from devtools.tools import ToolRunner
from scripts.backlog.coordinator import git

if TYPE_CHECKING:
    from pathlib import Path

    from apps.qwen.commands import CodingCommands


async def git_state(tool: CodingCommands, plan: dict[str, Any]) -> dict[str, Any]:
    """Reuse managed Git; retain exact NUL-delimited scoped index/status output."""
    paths = sorted({*tool.task.sources, *plan["inputs"], *plan["configuration"]})
    # Validate host paths before passing literal pathspecs to Git. An absent
    # authorized new slot is legitimate; directory aliases and escapes are not.
    for path in paths:
        _input_identity(tool.root, path)
    head = await git(tool.root, "rev-parse", "HEAD")
    branch = await git(tool.root, "symbolic-ref", "--quiet", "HEAD")
    index = await git(
        tool.root,
        "--literal-pathspecs",
        "ls-files",
        "--stage",
        "-z",
        "--",
        *paths,
        trim=False,
    )
    status = await git(
        tool.root,
        "--literal-pathspecs",
        "status",
        "--porcelain=v1",
        "-z",
        "--no-renames",
        "--untracked-files=all",
        "--ignored=matching",
        "--",
        *paths,
        trim=False,
    )
    # Other tracked edits and new implementation/test files may be unauthorized
    # candidate effects. Unrelated untracked forensic artifacts are excluded.
    tracked = await git(
        tool.root,
        "status",
        "--porcelain=v1",
        "-z",
        "--no-renames",
        "--untracked-files=all",
        trim=False,
    )
    tracked = "\0".join(
        entry
        for entry in tracked.split("\0")
        if entry
        and (entry[:2] != "??" or entry[3:].startswith(("src/", "apps/", "tests/")))
    )
    return {
        "head": head,
        "branch": branch,
        "index": index,
        "status": status,
        "tracked_status": tracked,
    }


async def _state(tool: CodingCommands) -> tuple[dict[str, Any], list[str]]:
    sources, plan, errors = _bundle_state(tool.root, tool.folder, tool.task)
    try:
        observation = await git_state(tool, plan)
    except (CommandError, OSError, ValueError) as error:
        errors.append("Git observation unavailable: " + str(error))
        observation = {}
    after_sources, after_plan, issues = _bundle_state(tool.root, tool.folder, tool.task)
    errors.extend(issues)
    if (after_sources, after_plan) != (sources, plan):
        errors.append("Source/plan changed while observing Git state")
    state = {"source_sha256": sources, "plan": plan, "git": observation}
    if plan != tool._bound_plan:  # noqa: SLF001 -- same CodingCommands owner
        errors.append("Bound validation plan changed")
    return state, errors


def _changes(
    tool: CodingCommands, state: dict[str, Any], errors: list[str]
) -> dict[str, Any]:
    """Interpret Git's own status, preserving staged/unstaged distinctions."""
    observation = state["git"]
    changed: dict[str, Any] = {}
    if not observation:
        return changed
    for entry in filter(None, observation["status"].split("\0")):
        code, path = entry[:2], entry[3:]
        if path in tool.task.sources:
            changed[path] = {
                "index_status": code[0],
                "worktree_status": code[1],
                "sha256": state["source_sha256"][path],
                "present": state["source_sha256"][path] is not None,
                "new_slot": path in tool.task.new_paths,
            }
            if "D" in code or state["source_sha256"][path] is None:
                errors.append("Deletion is not authorized: " + path)
            if "U" in code or code in {"AA", "DD"}:
                errors.append("Unmerged Git index requires reconciliation: " + path)
        else:
            errors.append("Noneditable task/configuration resource changed: " + path)
    errors.extend(
        "Tracked/source/test change outside candidate edit scope: " + entry[3:]
        for entry in filter(None, observation["tracked_status"].split("\0"))
        if entry[3:] not in tool.task.sources
    )
    if observation["head"] != tool.task.baseline_revision:
        errors.append("Git HEAD differs from the task baseline")
    baseline = dict(tool.task.baseline_hashes)
    for path, identity in state["source_sha256"].items():
        if path not in changed and identity != baseline.get(path):
            changed[path] = {
                "index_status": " ",
                "worktree_status": "content differs",
                "sha256": identity,
                "present": identity is not None,
                "new_slot": path in tool.task.new_paths,
            }
    return changed


def _view(report: dict[str, Any]) -> dict[str, Any]:
    """Bound the model projection; full state and original logs remain on disk."""
    view = {k: v for k, v in report.items() if k not in {"before", "after", "bundle"}}
    view["diagnostics"] = [e[:1000] for e in report["diagnostics"][:8]]
    view["checks"] = {
        name: {
            **row,
            "stdout": row.get("stdout", "")[:3000],
            "stderr": row.get("stderr", "")[:3000],
            "truncated": row.get("truncated", False)
            or len(row.get("stdout", "")) > 3000
            or len(row.get("stderr", "")) > 3000,
        }
        for name, row in report["checks"].items()
    }
    return view


def _receipt_path(tool: CodingCommands) -> Path:
    tool.count += 1
    target = tool.folder / f"change-check-{tool.count:02d}.json"
    while target.exists():
        tool.count += 1
        target = tool.folder / f"change-check-{tool.count:02d}.json"
    return target


def _load(path: Path) -> dict[str, Any]:
    # Managed decoding, with the same explicit evidence owner as _save/_hash.
    from devtools.core.paths import resolve_path  # noqa: PLC0415

    value = json.loads(_read_text(resolve_path(path)).content)
    if not isinstance(value, dict):
        raise TypeError("Evidence must be an object")
    return value


def _attach_bundle(
    tool: CodingCommands, report: dict[str, Any], evidence: str
) -> dict[str, Any]:
    """Project an existing authoritative bundle without deriving check outcomes."""
    path = tool.folder / evidence
    raw: dict[str, Any] = _load(path)["result"]
    report.update(
        bundle=raw,
        checks={
            name: {
                **row,
                **(
                    {
                        "status": "BLOCKED",
                        "bundle_status": "NOT_RUN",
                        "stderr": "Not run: bundle integrity failure",
                    }
                    if row["status"] == "NOT_RUN"
                    else {}
                ),
            }
            for name, row in raw["checks"].items()
        },
        status=raw["status"],
        bundle_evidence=evidence,
        bundle_sha256=_hash(path),
    )
    return raw


async def check_changes(tool: CodingCommands) -> dict[str, Any]:  # noqa: C901, PLR0912, PLR0915 -- one fixed composition and durable interruption boundary
    """Bind the existing all-checks Tool invocation to current scoped Git state."""
    target = _receipt_path(tool)
    before, errors = await _state(tool)
    changed = _changes(tool, before, errors)
    if not tool.task.quality_checks or not tool.task.command_tools:
        errors.append("Full pre-review validation requires all five checks")
    report: dict[str, Any] = {
        "operation": "check_changes",
        "status": "BLOCKED",
        "ready_for_review": False,
        "changed": changed,
        "source_sha256": before["source_sha256"],
        "plan_sha256": _plan_identity(before["plan"]),
        "task_definition_sha256": tool.task.definition_sha256,
        "candidate_sha256": _plan_identity(before),
        "checked_candidate_sha256": None,
        "after_candidate_sha256": None,
        "checks": {
            name: {
                "status": "NOT_APPLICABLE",
                "elapsed_seconds": 0.0,
                "stdout": "",
                "stderr": "Checks not executed",
            }
            for name in CHECKS
        },
        "diagnostics": errors,
        "before": before,
        "after": None,
        "evidence": target.name,
        "complete": False,
        "current": False,
        "scope": {
            "editable": list(tool.task.sources),
            "inputs": list(before["plan"]["inputs"]),
            "configuration": list(before["plan"]["configuration"]),
            "unrelated_untracked": "excluded; no whole-repository cleanliness claim",
        },
        "authority": (
            "review eligibility only; WorkCycle retains independent review/publication"
        ),
    }
    started = time.perf_counter()
    cancellation: asyncio.CancelledError | None = None

    def journal() -> None:
        report["elapsed_seconds"] = time.perf_counter() - started
        try:
            _save(
                target,
                {"call": {"name": "check_changes", "arguments": {}}, "result": report},
                overwrite=target.exists(),
            )
        except OSError as error:
            if cancellation is None:
                raise
            cancellation.add_note("Incomplete change-report evidence: " + str(error))

    journal()
    try:
        if errors:
            for row in report["checks"].values():
                row.update(
                    status="BLOCKED", stderr="Candidate integrity/plan unavailable"
                )
        elif not changed:
            report["status"] = "NO_CHANGES"
            report["complete"] = True
        else:
            tool._change_git = before["git"]  # noqa: SLF001 -- nested bundle authenticates Git at every check boundary
            try:
                bundle = await ToolRunner().execute(
                    tool, ("run_check", {"check": "all"})
                )
            finally:
                tool._change_git = None  # noqa: SLF001
            # The all-checks owner alone constructs and executes validation.
            # Preserve its full journal, not just the bounded model projection.
            raw = _attach_bundle(tool, report, bundle["evidence"])
            errors.extend(raw["diagnostics"])
            report["checked_candidate_sha256"] = report["candidate_sha256"]
            if (
                raw["source_sha256"] != before["source_sha256"]
                or raw["plan_sha256"] != report["plan_sha256"]
            ):
                errors.append("Bundle checked a different source/plan state")
            report["complete"] = all(
                row["status"] in {"PASS", "FAIL"} for row in raw["checks"].values()
            )
    except asyncio.CancelledError as error:
        cancellation = error
        errors.append("Host cancellation; validation incomplete")
        try:
            _attach_bundle(tool, report, f"coding-command-{tool.count:02d}.json")
        except (OSError, ValueError, KeyError, TypeError) as evidence_error:
            error.add_note(
                "Interrupted bundle evidence unavailable: " + str(evidence_error)
            )
        report["status"] = "INTERRUPTED"
        raise
    except (CommandError, OSError, ValueError, KeyError, TypeError) as error:
        errors.append("Incomplete validation evidence: " + str(error))
    except Exception as error:
        errors.append("Host failure; validation incomplete: " + type(error).__name__)
        raise
    finally:
        after, issues = await _state(tool)
        errors.extend(issues)
        report.update(after=after, after_candidate_sha256=_plan_identity(after))
        report["current"] = before == after and not errors
        if not report["current"]:
            if before != after:
                errors.append(
                    "Source, Git/index or validation plan changed during checking"
                )
            if cancellation is None:
                report["status"] = "BLOCKED"
        report["ready_for_review"] = (
            report["current"] and report["complete"] and report["status"] == "PASS"
        )
        journal()
    return {**_view(report), "receipt_sha256": _hash(target)}


async def current_report(
    tool: CodingCommands, supplied: dict[str, Any]
) -> dict[str, Any]:
    """Authenticate host-owned evidence and compare freshly observed state only."""
    current = False
    status = "INVALID_REPORT"
    diagnostics: list[str] = []
    try:
        name = supplied.get("evidence", "")
        if not isinstance(name, str) or not re.fullmatch(
            r"change-check-[0-9]+\.json", name
        ):
            raise ValueError("Invalid report evidence reference")
        path = tool.folder / name
        identity = _input_identity(tool.folder, name)
        if identity != supplied.get("receipt_sha256") or identity is None:
            raise ValueError("Report evidence identity mismatch")
        record = _load(path)
        report = record["result"]
        expected = {**_view(report), "receipt_sha256": identity}
        if (
            record["call"] != {"name": "check_changes", "arguments": {}}
            or supplied != expected
            or report["task_definition_sha256"] != tool.task.definition_sha256
        ):
            raise ValueError("Report payload or task provenance mismatch")
        state, diagnostics = await _state(tool)
        if report.get("bundle_evidence"):
            bundle_name = report["bundle_evidence"]
            if not re.fullmatch(r"coding-command-[0-9]+\.json", bundle_name):
                raise ValueError("Invalid bundle evidence reference")
            if _input_identity(tool.folder, bundle_name) != report["bundle_sha256"]:
                diagnostics.append(
                    "Underlying validation evidence changed or unavailable"
                )
        current = (
            not diagnostics
            and report["complete"]
            and report["current"]
            and state == report["before"] == report["after"]
        )
        status = report["status"]
        if not current and not diagnostics:
            diagnostics.append("Validation evidence is incomplete or no longer current")
    except (
        CommandError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
        AttributeError,
    ) as error:
        diagnostics.append(str(error))
    return {
        "operation": "is_current",
        "current": bool(current),
        "status": status,
        "ready_for_review": bool(current and status == "PASS"),
        "diagnostics": [str(e)[:1000] for e in diagnostics[:8]],
        "authority": "freshness only; no independent review or publication authority",
    }

# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, TRY301, PLR2004 -- bounded consumer composition

"""Bounded configured coding worker: retrieved Context, proposal, tests and repair.

This consumer is task-local. It exposes fixed scoped command observations and
host-admitted edit proposals, not arbitrary shell or general Agent state.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import time
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from apps.qwen import validation as task_validation
from apps.qwen.commands import (
    CodingCommands,
    command_definitions,
    run_check,
)
from apps.qwen.context_tools import (
    context_tool_definitions,
)
from apps.qwen.continuation import ACTIVE_BYTES
from apps.qwen.development_task import (
    _command,
    _hash,
    _save,
    _structured_edit_definition,
)
from apps.qwen.edits import (
    observed_definition,
    transaction_definition,
)
from apps.qwen.patch_proposal_worker import _read_text
from apps.qwen.tasks import MARKDOWN, CodingTask
from apps.qwen.turns import run_turns
from devtools.context import (
    Repository,
    RepositoryResourceAddress,
    materialize_disclosure_plan,
    observe_repository_resources,
    plan_disclosures,
    render_context_disclosure,
)
from devtools.context.planning import SourceSearchDisclosureOption
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.retrieval import (
    build_source_search_index,
    search_repository_source,
)
from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.models.interaction import (
    ModelSettings,
)
from devtools.resources.filesystem import TextFile, write

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from apps.qwen.obligations import ObligationFrame
    from devtools.context.retrieval.source import SourceSearchMode
    from devtools.models.interaction import ModelInteraction
    from devtools.models.interaction.providers import LlamaCppRequestSettings


def _validation_feedback(
    validation: dict[str, Any],
    *,
    task: CodingTask | None = None,
    source_version: str | None = None,
    source_versions: dict[str, str | None] | None = None,
) -> dict[str, Any]:
    """Project bounded diagnostics; complete original command logs stay in evidence."""
    projected: dict[str, Any] = {}
    for name in ("oracle", "tests", "ruff", "format", "typing"):
        if name not in validation:
            continue
        result = validation[name]
        failures = [
            json.loads(line.removeprefix("QWEN_TEST_FAILURE "))
            for line in result["stderr"].splitlines()
            if line.startswith("QWEN_TEST_FAILURE ")
        ]
        details = {}
        for field in ("stdout", "stderr"):
            text = result[field]
            if failures:
                if field == "stderr":
                    text = "\n".join(
                        line
                        for line in text.splitlines()
                        if not line.startswith("QWEN_TEST_FAILURE ")
                    )
                elif len(text) > 600:
                    text = (
                        "[PYTEST TRACEBACKS OMITTED: see primary_failures; "
                        "complete log archived]\n" + text[-600:]
                    )
            details[field] = (
                text
                if len(text) <= 2000
                else text[:1000] + "\n[TRUNCATED]\n" + text[-1000:]
            )
            details[field + "_truncated"] = len(text) > 2000 or text != result[field]
        category = {
            "oracle": "behavior",
            "tests": "regression",
            "ruff": "lint",
            "format": "formatting",
            "typing": "typing",
        }[name]
        behavior_passed = name == "oracle" and (
            result["exit_code"] == 0 or "QWEN_BEHAVIOR_PASSED" in result["stdout"]
        )
        if name == "oracle" and behavior_passed and result["exit_code"] != 0:
            category = "typing"
        projected[name] = {
            "category": category,
            "status": "PASS" if result["exit_code"] == 0 else "FAIL",
            "behavior_passed": behavior_passed if name == "oracle" else None,
            "exit_code": result["exit_code"],
            "primary_failures": failures[:8],
            "primary_failures_truncated": len(failures) > 8,
            "reporting_failure": "INTERNALERROR" in result["stdout"]
            or "_pytest/" in result["stderr"].replace("\\", "/"),
            **details,
        }
    if task is not None:
        projected["repair_contract"] = {
            "source_version": source_version,
            "source_versions": source_versions or {task.source: source_version},
            "frozen_requirements": task.objective,
            "passed_checks": [
                name for name, result in projected.items() if result["status"] == "PASS"
            ],
            "failed_checks": [
                name for name, result in projected.items() if result["status"] == "FAIL"
            ],
            "independent_behavior_passed": projected["oracle"]["behavior_passed"],
            "invariants": (
                "All required checks must pass together on the same source version. "
                "Preserve already-passing behavior and regressions "
                "while repairing failures. "
                "A null source version denotes an authorized still-absent new slot, "
                "not empty source or an editable source observation. "
                "A lint recommendation is not permission to change a frozen public API "
                "or exception contract. Seek a compatible implementation; do not trade "
                "behavioral correctness for style or typing. If requirements conflict, "
                "report the precise conflict rather than silently redefining success. "
                "Do not modify host tests, acceptance criteria or validation commands."
            ),
        }
    return projected


def acquire_context(
    root: Path,
    repository: Repository,
    *,
    task: CodingTask = MARKDOWN,
    mode: SourceSearchMode | None = None,
) -> tuple[str, list[dict[str, Any]]]:
    """Search the two explicitly admitted resources and disclose exact expansions.

    The source's module constants and imports are required surrounding Context;
    expand a ranked symbol to its file. Tests are a separately selected file.
    No repository-wide disclosure or automatic sufficiency claim is made.
    """
    addresses = tuple(
        RepositoryResourceAddress(path)
        for path in (task.source, *task.tests, *task.read_paths)
    )
    discovery = discover_repository_resource_addresses(
        repository=repository,
        root=resolve_path(root),
        maximum_resource_count=32,
        maximum_traversal_entry_count=512,
        requested_addresses=addresses,
    )
    snapshot = observe_repository_resources(
        repository=repository,
        root=resolve_path(root),
        addresses=addresses,
        maximum_resource_bytes=32768,
    )
    corpus = realize_repository_text_corpus(
        definition=define_repository_text_corpus(
            discovery=discovery,
            selected_addresses=addresses,
        ),
        snapshot=snapshot,
    )
    index = build_source_search_index(
        snapshot, corpus=corpus, window_lines=40, overlap_lines=10
    )
    choices = []
    details = []
    for path, query, configured_view, expansion in task.context:
        view = mode if path == task.source and mode is not None else configured_view
        result = search_repository_source(
            index, query=query, mode=view, maximum_results=100
        )
        hit = next(
            (hit for hit in result.hits if hit.unit.resource.address.value == path),
            None,
        )
        if hit is None:
            raise ValueError("Required task resource not retrieved: " + path)
        unit = hit.unit if expansion == "none" else index.expand(hit.unit, to=expansion)
        choices.append(SourceSearchDisclosureOption(task.prompt, unit))
        details.append(
            {
                "path": path,
                "query": query,
                "mode": view,
                "selected_kind": hit.unit.kind,
                "selected_unit": str(hit.unit.id),
                "qualified_name": hit.unit.qualified_name,
                "selected_span": [hit.unit.start, hit.unit.end],
                "rank": hit.rank,
                "materialized_kind": unit.kind,
                "unit": str(unit.id),
                "repository": str(unit.repository_id),
                "snapshot": str(snapshot.id),
                "content_identity": str(unit.resource.content_identity),
                "span": [unit.start, unit.end],
                "bytes": len(unit.text.encode()),
                "tokens": None,
            }
        )
    plan = plan_disclosures(
        purpose=task.prompt, snapshot=snapshot, disclosures=tuple(choices)
    )
    return render_context_disclosure(
        materialize_disclosure_plan(
            plan=plan,
            snapshot=snapshot,
        )
    ).text, details


async def validate_workspace(
    root: Path,
    folder: Path,
    *,
    task: CodingTask = MARKDOWN,
    commands: CodingCommands | None = None,
) -> dict[str, Any]:
    """Preserve the public worker signature and legacy report projection."""
    return await task_validation.validate_task(
        root, folder, task=task, commands=commands
    )


async def preflight_coding_task(
    root: Path,
    folder: Path,
    *,
    task: CodingTask,
) -> dict[str, Any]:
    """Check a frozen baseline without inference; engineering review stays explicit.

    This verifies reproduction, regression/quality baselines and exact input
    identities. It does not prove specifications satisfiable or authorize work.
    The trusted caller must separately review public/exception contracts, lint
    compatibility, alternatives and independent success criteria before freezing.
    """
    await asyncio.to_thread(folder.mkdir, parents=True, exist_ok=False)
    _prepare_workspace(root, folder, task)
    await _authenticate_inputs(root, root, task)
    validation = await validate_workspace(root, folder, task=task)
    typing = await run_check(root, folder, task, "typing")
    await _authenticate_inputs(root, root, task)
    accepted = (
        validation["oracle"]["failed"]
        and "AssertionError" in validation["oracle"]["stderr"]
        and all(
            not value["failed"]
            for name, value in validation.items()
            if isinstance(value, dict) and name != "oracle"
        )
        and not typing["failed"]
    )
    result = {
        "task_definition_sha256": task.definition_sha256,
        "baseline_revision": task.baseline_revision,
        "validation": validation,
        "typing": typing,
        "disposition": "PREFLIGHT_CHECKS_PASS_REVIEW_REQUIRED"
        if accepted
        else "PREFLIGHT_REFUSED",
        "model_calls": 0,
        "review_required": [
            "public behavior and exception compatibility",
            "lint/format/typing compatibility",
            "legitimate alternatives",
            "independent acceptance coverage",
        ],
        "satisfiability_proof": False,
    }
    _save(folder / "preflight.json", result)
    return result


async def _authenticate_inputs(root: Path, workspace: Path, task: CodingTask) -> None:
    """Authenticate configured immutable inputs in the selected ordinary branch.

    Git LF/CRLF candidates must identify the frozen input; current source/test
    bytes must independently match it. This function never rewrites inputs.
    """
    for path in task.new_paths:
        if (workspace / path).exists() or not (workspace / path).parent.is_dir():
            raise ValueError("New source is not absent under existing parent")
        probe = await _command(
            root, "git", "ls-tree", "--name-only", task.baseline_revision, "--", path
        )
        if probe["failed"] or probe["stdout"].strip():
            raise ValueError("New source exists in baseline")
    for path, digest in task.baseline_hashes:
        target = workspace / path
        result = await _command(
            root, "git", "show", task.baseline_revision + ":" + path
        )
        if result["failed"]:
            raise ValueError("Cannot authenticate frozen baseline: " + path)
        text = result["stdout"].replace("\r\n", "\n")
        candidates = (text, text.replace("\n", "\r\n"))
        matched = next(
            (
                value
                for value in candidates
                if hashlib.sha256(value.encode()).hexdigest() == digest
            ),
            None,
        )
        if matched is None:
            raise ValueError("Frozen baseline identity mismatch: " + path)
        if _hash(target) != digest:
            raise ValueError(
                "Select the exact ordinary baseline branch before execution: " + path
            )


def _prepare_workspace(root: Path, folder: Path, task: CodingTask = MARKDOWN) -> Path:
    """Preserve the existing import contract through the host policy adapter."""
    return task_validation.prepare_task_validation(root, folder, task)


async def _turns(  # noqa: PLR0913 -- one bounded worker loop
    workspace: Path,
    folder: Path,
    interaction: ModelInteraction,
    report: dict[str, Any],
    *,
    maximum_calls: int,
    task: CodingTask,
    admit_edit: Callable[[str, str], None] | None = None,
    thinking_enabled: bool = False,
    coordinated_edits: bool = False,
    observed_edits: bool = False,
    reasoning_effort: str | None = None,
    request_settings: LlamaCppRequestSettings | None = None,
    check_changes_before_completion: bool = False,
    commands: CodingCommands | None = None,
    obligation_frame: ObligationFrame | None = None,
) -> None:
    """Delegate turns while preserving the stable lifecycle/acquisition seams."""
    await run_turns(
        workspace,
        folder,
        interaction,
        report,
        acquire_context=acquire_context,
        validate_workspace=validate_workspace,
        validation_feedback=_validation_feedback,
        maximum_calls=maximum_calls,
        task=task,
        admit_edit=admit_edit,
        thinking_enabled=thinking_enabled,
        coordinated_edits=coordinated_edits,
        observed_edits=observed_edits,
        reasoning_effort=reasoning_effort,
        request_settings=request_settings,
        check_changes_before_completion=check_changes_before_completion,
        commands=commands,
        obligation_frame=obligation_frame,
    )


async def run_coding_task(  # noqa: C901, PLR0912, PLR0913, PLR0915 -- one bounded worker and conservative terminal accounting
    root: Path,
    folder: Path,
    interaction: ModelInteraction,
    *,
    maximum_calls: int | None = None,
    task: CodingTask = MARKDOWN,
    provenance: dict[str, Any] | None = None,
    admit_edit: Callable[[str, str], None] | None = None,
    thinking_enabled: bool = False,
    coordinated_edits: bool = False,
    observed_edits: bool = False,
    reasoning_effort: str | None = None,
    request_settings: LlamaCppRequestSettings | None = None,
    check_changes_before_completion: bool = False,
    obligation_frame: ObligationFrame | None = None,
) -> dict[str, Any]:
    """Run one bounded engineering task; preserve evidence and discard all edits.

    A trusted local development invocation supplies evaluation authority; it
    confers no production publication or WorkCycle authority. Reusing an output
    directory is refused before any invocation. Terminal acceptance requires
    successful worker completion, not just a validated candidate. A fatal error
    revokes acceptance while preserving candidate/check facts and known effects.
    """
    if type(thinking_enabled) is not bool:
        raise ValueError("thinking_enabled must be an explicit host boolean")
    if obligation_frame is not None:
        obligation_frame.validate(task)
    if type(check_changes_before_completion) is not bool or (
        check_changes_before_completion
        and (not task.command_tools or not task.quality_checks or not observed_edits)
    ):
        raise ValueError(
            "Change-check completion requires native observed edits and all checks"
        )
    maximum_calls = task.maximum_calls if maximum_calls is None else maximum_calls
    if not 1 <= maximum_calls <= task.maximum_calls:
        raise ValueError("Model call bound exceeds the authenticated task limit")
    original_hashes: dict[str, str | None] = {
        path: _hash(root / path) for path, _ in task.baseline_hashes
    }
    if (
        type(coordinated_edits) is not bool
        or type(observed_edits) is not bool
        or (observed_edits and not coordinated_edits)
        or (task.path_edits and not observed_edits)
        or (coordinated_edits and task.context_mode != "on-demand")
        or ((task.additional_edit_paths or task.new_paths) and not coordinated_edits)
    ):
        raise ValueError("Coordinated edits require explicit native scoped operation")
    original_sources = {
        p: _read_text(resolve_path(root / p)).content if (root / p).exists() else None
        for p in task.sources
    }
    original_hashes.update(dict.fromkeys(task.new_paths))
    folder = resolve_path(folder).value
    await asyncio.to_thread(folder.mkdir, parents=True, exist_ok=False)
    started = time.perf_counter()
    report: dict[str, Any] = {
        "schema": "qwen-coding-loop-v2",
        "started_at": str(Timestamp.now()),
        "accepted": False,
        "check_changes_before_completion": check_changes_before_completion,
        "disposition": "PREPARING",
        "turns": [],
        "limits": {
            "model_calls": maximum_calls,
            "output_tokens": task.output_tokens,
            "wall_seconds": task.wall_seconds,
            "per_call_seconds": task.call_seconds,
            "context_actions": task.tool_actions
            if task.context_mode == "on-demand"
            else 0,
            "proposals": min(maximum_calls, task.maximum_proposals),
            "active_messages_bytes": ACTIVE_BYTES
            if task.context_mode == "on-demand"
            else 60000,
        },
        "task_name": task.name,
        "task_definition": asdict(task),
        "task_definition_sha256": task.definition_sha256,
        "baseline": dict(task.baseline_hashes),
        "oracle_sha256": task.oracle_sha256,
        "coordination_usage": "UNKNOWN",
        "provenance": provenance,
        "execution_location": "selected-canonical-checkout; no source-tree copy",
        "edit_protocol": "observed-path-batch-v1"
        if observed_edits and task.path_edits
        else "observed-flat-batch-v1"
        if observed_edits
        else "observed-transaction-v1"
        if coordinated_edits
        else "single-edit-legacy",
    }
    workspace: Path | None = None
    validation_commands: CodingCommands | None = None
    if obligation_frame is not None:
        report["obligation_frame_sha256"] = obligation_frame.sha256
        _save(folder / "obligation-frame.json", obligation_frame.to_dict())
    try:
        async with asyncio.timeout(task.wall_seconds):
            workspace = _prepare_workspace(root, folder, task)
            await _authenticate_inputs(root, workspace, task)
            validation_commands = CodingCommands(workspace, folder, task)
            report["baseline_validation"] = await validate_workspace(
                workspace, folder, task=task, commands=validation_commands
            )
            baseline = report["baseline_validation"]
            if (
                not baseline["oracle"]["failed"]
                or baseline["tests"]["failed"]
                or baseline["integrity"]["failed"]
                or "AssertionError" not in baseline["oracle"]["stderr"]
            ):
                raise ValueError("Baseline must pass existing tests and fail oracle")
            _save(
                folder / "freeze.json",
                {
                    **report,
                    "task": task.objective if coordinated_edits else task.prompt,
                    "tool": asdict(
                        observed_definition(path_based=task.path_edits)
                        if observed_edits
                        else transaction_definition(
                            task.sources, api_required=bool(task.api_targets)
                        )
                        if coordinated_edits
                        else _structured_edit_definition(source_path=task.source)
                    ),
                    "context_tools": [
                        asdict(t)
                        for t in context_tool_definitions(
                            task.api_targets,
                            task.new_paths,
                            direct_reads=observed_edits,
                            map_navigation=task.map_navigation,
                        )
                        + command_definitions(task)
                    ]
                    if task.context_mode == "on-demand"
                    else [],
                    "settings": asdict(
                        ModelSettings(
                            task.output_tokens, thinking_enabled=thinking_enabled
                        )
                    ),
                },
            )
            await _turns(
                workspace,
                folder,
                interaction,
                report,
                maximum_calls=maximum_calls,
                task=task,
                admit_edit=admit_edit,
                thinking_enabled=thinking_enabled,
                coordinated_edits=coordinated_edits,
                observed_edits=observed_edits,
                reasoning_effort=reasoning_effort,
                request_settings=request_settings,
                check_changes_before_completion=check_changes_before_completion,
                commands=validation_commands,
                obligation_frame=obligation_frame,
            )
    except asyncio.CancelledError:
        report.update(
            accepted=False,
            disposition="CANCELLED_COMPLETION_UNKNOWN_NO_RETRY"
            if report["turns"] and report["turns"][-1]["phase"] == "MODEL_REQUEST"
            else "HOST_CANCELLED",
        )
        raise
    except TimeoutError:
        report.update(
            accepted=False,
            disposition=(
                "TIMEOUT_COMPLETION_UNKNOWN_NO_RETRY"
                if report["turns"] and report["turns"][-1]["phase"] == "MODEL_REQUEST"
                else "HOST_TIMEOUT"
            ),
        )
    except Exception as error:  # noqa: BLE001 -- retain terminal failures without redispatch
        phase = report["turns"][-1]["phase"] if report["turns"] else "PREPARATION"
        if isinstance(error, ValueError) and str(error) in {
            "Context budget cannot retain current source and latest validation",
            "Bounded Context byte allowance exceeded",
            "Measured input plus output/safety exceeds actual 32K capacity",
        }:
            phase = "CONTEXT_BUDGET"
        report.update(
            accepted=False,
            disposition=phase + "_FAILED",
            error=f"{type(error).__name__}: {error}",
        )
    finally:
        if workspace is not None:
            candidates = []
            restorable = True
            for path in task.sources:
                current = (
                    _read_text(resolve_path(root / path)).content
                    if (root / path).exists()
                    else ""
                )
                target = (
                    folder / "final-source.py"
                    if path == task.source
                    else folder / "final-sources" / path
                )
                target.parent.mkdir(parents=True, exist_ok=True)
                write(TextFile(resolve_path(target), current))
                candidates.append(
                    {
                        "path": path,
                        "evidence": str(target.relative_to(folder)).replace("\\", "/"),
                        "sha256": _hash(root / path)
                        if (root / path).exists()
                        else None,
                    }
                )
                known = {original_hashes[path]}
                for stage in report["turns"]:
                    for key in ("sources_after", "proposed_sources"):
                        if path in stage.get(key, {}):
                            known.add(stage[key][path])
                    if path == task.source and "source_after" in stage:
                        known.add(stage["source_after"])
                restorable = (
                    restorable
                    and (_hash(root / path) if (root / path).exists() else None)
                    in known
                )
            report["candidates"] = candidates
            if restorable:
                for path, text in original_sources.items():
                    if text is None:
                        (root / path).unlink(missing_ok=True)
                    else:
                        write(TextFile(resolve_path(root / path), text))
            else:
                report.update(
                    accepted=False, disposition="CLEANUP_RECONCILIATION_REQUIRED"
                )
        report.update(
            finished_at=str(Timestamp.now()),
            elapsed_seconds=time.perf_counter() - started,
            workspace_removed=not (folder / "workspace").exists(),
            source_restored=all(
                (_hash(root / p) if (root / p).exists() else None) == original_hashes[p]
                for p in task.sources
            ),
            original_unchanged=all(
                (_hash(root / path) if (root / path).exists() else None) == digest
                for path, digest in original_hashes.items()
            ),
        )
        if report["accepted"] and (
            not report["original_unchanged"]
            or validation_commands is None
            or not validation_commands.inputs_current()
        ):
            report.update(accepted=False, disposition="INPUT_INTEGRITY_FAILED")
        for stage in report["turns"]:
            if stage["disposition"] == "DISPATCH_ATTEMPTED":
                stage.update(
                    disposition=report["disposition"],
                    finished_at=str(Timestamp.now()),
                    elapsed_seconds=time.perf_counter() - stage["started_monotonic"],
                )
                _save(
                    folder / f"turn-{stage['number']:02d}" / "stage.json",
                    stage,
                    overwrite=True,
                )
        report["repair_cycles"] = max(
            0, sum(bool(s.get("proposal_valid")) for s in report["turns"]) - 1
        )
        report["context_actions_attempted"] = sum(
            e.get("dispatched", True)
            for s in report["turns"]
            for e in s.get("context_tools", ())
        )
        report["context_actions_requested"] = sum(
            s.get("context_actions_requested", 0) for s in report["turns"]
        )
        report["context_actions_accepted"] = sum(
            e["status"] == "RETURNED"
            for s in report["turns"]
            for e in s.get("context_tools", ())
        )
        report["context_bytes_disclosed"] = sum(
            s["context_bytes"] for s in report["turns"]
        )
        report["source_text_bytes_disclosed"] = sum(
            e.get("result", {}).get("bytes", 0)
            for s in report["turns"]
            for e in s.get("context_tools", ())
        )
        report["model_calls_attempted"] = len(report["turns"])
        report["proposals_attempted"] = sum(
            bool(stage.get("proposal_attempted")) for stage in report["turns"]
        )
        report["proposal_refusals"] = sum(
            bool(stage.get("proposal_attempted"))
            and not stage.get("proposal_valid", False)
            for stage in report["turns"]
        )
        report["proposals_admitted"] = sum(
            bool(stage.get("proposal_valid")) for stage in report["turns"]
        )
        report["usage_totals"] = {}
        report["validation_seconds"] = sum(
            result["elapsed_seconds"]
            for validation in (
                report.get("baseline_validation", {}),
                *(stage.get("validation", {}) for stage in report["turns"]),
            )
            for key, result in validation.items()
            if key in {"oracle", "tests"}
        )
        for category in (
            "input_tokens",
            "output_tokens",
            "cached_input_tokens",
            "cache_write_tokens",
            "reasoning_tokens",
        ):
            values = [
                (stage.get("usage") or {}).get(category) for stage in report["turns"]
            ]
            report["usage_totals"][category] = (
                sum(value for value in values if value is not None)
                if values and all(value is not None for value in values)
                else None
            )
        _save(folder / "result.json", report)
    return report

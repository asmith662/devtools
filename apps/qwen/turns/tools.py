# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- bounded consumer composition

"""Authorized read/check dispatch and correlated native Tool feedback."""

from __future__ import annotations

import json
import time
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from apps.qwen.commands import COMMAND_TOOL_NAMES
from apps.qwen.context_tools import ContextRequestError
from apps.qwen.development_task import _save
from apps.qwen.patch_proposal_worker import PatchProposalError
from devtools.core.time import Timestamp
from devtools.models.interaction import PromptMessage
from devtools.tools import ToolRunner

if TYPE_CHECKING:
    from pathlib import Path

    from apps.qwen.commands import CodingCommands
    from apps.qwen.context_tools import ContextTools
    from apps.qwen.tasks import CodingTask
    from devtools.models.interaction import ModelToolCall


async def dispatch_context_calls(  # noqa: C901, PLR0913 -- one admitted native batch
    calls: tuple[ModelToolCall, ...],
    *,
    task: CodingTask,
    tools: ContextTools,
    commands: CodingCommands,
    turn: Path,
    stage: dict[str, Any],
    report: dict[str, Any],
    history: list[PromptMessage],
    context_actions: int,
    maximum_calls: int,
    number: int,
    proposals: int,
    started: float,
    check_changes_before_completion: bool,
) -> int:
    """Dispatch once, retain known effects, and return the consumed action count.

    The loop passes its actual history/stage/report objects; this owner neither
    copies session state nor retries failed or uncertain effects. Acceptance from
    shared checks remains provisional until the lifecycle coordinator finalizes.
    """
    stage["phase"] = "CONTEXT_TOOL_EXECUTION"
    stage["context_actions_requested"] = len(calls)
    stage["context_tools"] = []
    checked_this_turn = False
    _save(turn / "stage.json", stage, overwrite=True)
    if 0 < task.tool_actions - context_actions < len(calls):
        result: dict[str, Any] = {
            "status": "REFUSED",
            "error": "CONTEXT_BATCH_EXCEEDS_REMAINING",
            "instruction": (
                "No Tool was dispatched. Select at most "
                f"{task.tool_actions - context_actions} read/API actions; "
                "use narrow ranges and avoid redundant acquisition."
            ),
            "host_limits": {
                "context_actions_remaining": task.tool_actions - context_actions,
                "model_calls_remaining": maximum_calls - number,
                "proposals_remaining": task.maximum_proposals - proposals,
            },
        }
        for call in calls:
            stage["context_tools"].append(
                {
                    "call": asdict(call),
                    "status": "REFUSED",
                    "dispatched": False,
                    "result": result,
                    "elapsed_seconds": 0,
                }
            )
            history.append(
                PromptMessage(
                    "tool",
                    json.dumps(result),
                    tool_call_id=call.provider_call_id,
                )
            )
        stage.update(
            disposition="CONTEXT_BATCH_REFUSED",
            finished_at=str(Timestamp.now()),
            elapsed_seconds=time.perf_counter() - started,
        )
        _save(turn / "tools.json", stage["context_tools"], overwrite=True)
        _save(turn / "stage.json", stage, overwrite=True)
        return context_actions
    for call in calls:
        if context_actions >= task.tool_actions:
            raise PatchProposalError("Context action budget exhausted")
        context_actions += 1
        event: dict[str, Any] = {
            "call": asdict(call),
            "status": "ATTEMPTED",
            "started_at": str(Timestamp.now()),
        }
        acquisition_started = time.perf_counter()
        stage["context_tools"].append(event)
        _save(turn / "tools.json", stage["context_tools"], overwrite=True)
        try:
            result = await (
                commands.dispatch(call)
                if call.name in COMMAND_TOOL_NAMES
                else tools.dispatch(call)
            )
        except Exception as error:
            event.update(status="REFUSED", error=f"{type(error).__name__}: {error}")
            event["elapsed_seconds"] = time.perf_counter() - acquisition_started
            _save(turn / "tools.json", stage["context_tools"], overwrite=True)
            if not isinstance(error, ContextRequestError):
                raise
            result = tools.refusal(call, error)
        else:
            event["status"] = (
                "REFUSED" if result.get("status") == "REFUSED" else "RETURNED"
            )
        event["result"] = result
        event["elapsed_seconds"] = time.perf_counter() - acquisition_started
        limits = {
            "context_actions_remaining": task.tool_actions - context_actions,
            "model_calls_remaining": maximum_calls - number,
            "proposals_remaining": task.maximum_proposals - proposals,
        }
        if call.name in {"check_changes", "is_current"}:
            # A report is an authenticated payload. Do not change it
            # merely to present conversation-budget metadata.
            event["host_limits"] = limits
        else:
            result["host_limits"] = limits
        if (
            check_changes_before_completion
            and proposals
            and call.name == "check_changes"
        ):
            report["change_check"] = result
            checked_this_turn = True
        history.append(
            PromptMessage(
                "tool",
                json.dumps(result, ensure_ascii=False),
                tool_call_id=call.provider_call_id,
            )
        )
        _save(turn / "tools.json", stage["context_tools"], overwrite=True)
    if checked_this_turn and report["change_check"].get("ready_for_review"):
        freshness = await ToolRunner().execute(
            commands, ("is_current", {"report": report["change_check"]})
        )
        report["change_check_freshness"] = {
            **freshness,
            "invoked_by": "host verification, not model invocation",
        }
        if freshness["current"] and freshness["ready_for_review"]:
            report.update(accepted=True, disposition="ACCEPTED")
    stage.update(
        disposition="CONTEXT_RETURNED",
        finished_at=str(Timestamp.now()),
        elapsed_seconds=time.perf_counter() - started,
        context_bytes=sum(
            len(json.dumps(e.get("result", {}), ensure_ascii=False).encode())
            for e in stage["context_tools"]
        ),
        context=[
            {
                k: v
                for k, v in e.get("result", {}).items()
                if k
                in {
                    "path",
                    "version",
                    "span",
                    "snapshot",
                    "unit",
                    "kind",
                    "truncated",
                    "bytes",
                }
            }
            for e in stage["context_tools"]
        ],
    )
    _save(turn / "stage.json", stage, overwrite=True)
    return context_actions

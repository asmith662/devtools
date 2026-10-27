# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, TRY301, T201 -- bounded consumer composition

"""Operational turn sequencing, model admission, edits and repair feedback."""

from __future__ import annotations

import asyncio
import hashlib
import json
import time
from dataclasses import asdict, replace
from typing import TYPE_CHECKING, Any

from apps.qwen.commands import (
    COMMAND_TOOL_NAMES,
    CodingCommands,
    command_definitions,
    format_sources,
)
from apps.qwen.context_tools import (
    CONTEXT_TOOL_NAMES,
    ContextTools,
)
from apps.qwen.continuation import ACTIVE_BYTES, present_sources, select_messages
from apps.qwen.development_task import (
    _hash,
    _save,
    _structured_edit_definition,
    _structured_edit_patch_from_calls,
    apply_source_patches,
)
from apps.qwen.edits import (
    admit_observed,
    admit_transaction,
    observed_definition,
    transaction_definition,
)
from apps.qwen.obligations import NativeObligations, ReadinessRefusalError
from apps.qwen.patch_proposal_worker import PatchProposalError, _read_text
from devtools.context import (
    Repository,
    RepositoryResourceAddress,
)
from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.models.interaction import (
    ModelRequest,
    ModelSettings,
    ModelTermination,
    Prompt,
    PromptMessage,
)
from devtools.models.interaction.providers import (
    LlamaCppInteraction,
    LlamaCppRequestSettings,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from pathlib import Path

    from apps.qwen.obligations import ObligationFrame
    from apps.qwen.tasks import CodingTask
    from devtools.models.interaction import ModelInteraction

from .prompt import fit_capacity, initial_history
from .tools import dispatch_context_calls


async def run_turns(  # noqa: C901, PLR0912, PLR0913, PLR0915 -- one bounded worker loop
    workspace: Path,
    folder: Path,
    interaction: ModelInteraction,
    report: dict[str, Any],
    *,
    acquire_context: Callable[..., tuple[str, list[dict[str, Any]]]],
    validate_workspace: Callable[..., Awaitable[dict[str, Any]]],
    validation_feedback: Callable[..., dict[str, Any]],
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
    """Execute bounded turns using the coordinator's acquisition/check adapters.

    Turn history, counters and journal objects remain local to this invocation.
    Task preflight, candidate custody and terminal accounting stay with the caller.
    """
    measured_capacity = isinstance(interaction, LlamaCppInteraction)
    active_limit = (
        131072
        if measured_capacity
        else min(ACTIVE_BYTES, int((32768 - task.output_tokens - 4096) * 1.5))
    )
    repository = Repository.new()
    feedback: dict[str, Any] = {"disposition": "INITIAL_PROPOSAL"}
    prepared_at = time.perf_counter()
    tools = (
        ContextTools(workspace, task, direct_reads=observed_edits)
        if task.context_mode == "on-demand"
        else None
    )
    commands = (
        commands if commands is not None else CodingCommands(workspace, folder, task)
    )
    obligations = (
        NativeObligations(obligation_frame, tools)
        if obligation_frame is not None and tools is not None
        else None
    )
    report["context_preparation_seconds"] = time.perf_counter() - prepared_at
    history = initial_history(
        task,
        maximum_calls=maximum_calls,
        coordinated_edits=coordinated_edits,
        observed_edits=observed_edits,
        tools=tools,
        check_changes_before_completion=check_changes_before_completion,
    )
    context_actions = 0
    proposals = 0
    for number in range(1, maximum_calls + 1):
        turn = folder / f"turn-{number:02d}"
        turn.mkdir()
        resources: list[dict[str, Any]] = []
        omitted = 0
        if tools is None:
            context, resources = acquire_context(workspace, repository, task=task)
            prompt = (
                task.prompt
                + "\nHOST FEEDBACK:\n"
                + json.dumps(feedback)
                + "\n"
                + context
            )
            model_prompt = Prompt(prompt, role="user")
        else:
            tools.check_current()
            # Same native Prompt contract as request.prompt, archived before
            # projection. This preserves exact Tool content strings/digests;
            # the full archive is never sent merely to simulate memory.
            _save(
                turn / "unprojected-prompt.json",
                asdict(Prompt("", role="messages", messages=tuple(history))),
            )
            active_bytes = active_limit
            if measured_capacity:
                active_bytes = max(
                    active_bytes,
                    len(json.dumps([asdict(m) for m in history]).encode()) + 2000,
                )
            messages, omitted = select_messages(
                history, source_path=task.source, maximum_bytes=active_bytes
            )
            if obligations is not None:
                messages = obligations.project(messages)
            if task.path_edits:
                messages = present_sources(messages)
            model_prompt = Prompt("", role="messages", messages=messages)
            prompt = json.dumps(asdict(model_prompt))
            context = ""  # Disclosed only on demand in correlated Tool results.
        if not (measured_capacity and tools is not None) and len(prompt.encode()) > (
            active_limit + 2000 if tools is not None else 60000
        ):
            raise ValueError("Bounded Context byte allowance exceeded")
        request = ModelRequest(
            prompt=model_prompt,
            provider_settings=replace(
                request_settings or LlamaCppRequestSettings(),
                reasoning_effort=reasoning_effort,
            )
            if reasoning_effort
            else request_settings,
            settings=ModelSettings(
                maximum_output_tokens=task.output_tokens,
                thinking_enabled=thinking_enabled,
            ),
            tools=(
                (
                    observed_definition(path_based=task.path_edits)
                    if observed_edits
                    else transaction_definition(
                        task.sources, api_required=bool(task.api_targets)
                    )
                    if coordinated_edits
                    else _structured_edit_definition(source_path=task.source)
                ),
                *(
                    (*tools.definitions, *command_definitions(task))
                    if tools is not None and context_actions < task.tool_actions
                    else ()
                ),
            ),
        )
        _save(turn / "request.json", asdict(request))
        measured_tokens = None
        if isinstance(interaction, LlamaCppInteraction):
            request, prompt, omitted, measured_tokens = await fit_capacity(
                interaction,
                request,
                task=task,
                history=history,
                on_demand=tools is not None,
                active_bytes=active_bytes if tools is not None else active_limit,
                context_actions=context_actions,
                number=number,
                maximum_calls=maximum_calls,
                proposals=proposals,
                thinking_enabled=thinking_enabled,
                observed_edits=observed_edits,
                obligations=obligations,
                turn=turn,
                prompt=prompt,
                omitted=omitted,
                select_messages=select_messages,
            )
        source_hash = _hash(workspace / task.source)
        selected_source = interaction.source
        stage: dict[str, Any] = {
            "number": number,
            "selected_source": str(selected_source),
            "input_tokens_measured": measured_tokens,
            "capacity_safety_tokens": 2048 if measured_capacity else None,
            "started_at": str(Timestamp.now()),
            "started_monotonic": time.perf_counter(),
            "source_before": source_hash,
            "context": resources,
            "prompt_bytes": len(prompt.encode()),
            "context_bytes": len(context.encode()),
            "disposition": "DISPATCH_ATTEMPTED",
            "phase": "MODEL_REQUEST",
            "messages_omitted_from_active_context": omitted,
        }
        report["turns"].append(stage)
        if obligations is not None:
            obligations.retain(stage, report)
        stage["request_sha256"] = _hash(turn / "request.json")
        _save(turn / "stage.json", stage)
        print(
            f"{stage['started_at']} turn {number}/{maximum_calls}: model request; "
            f"Context {stage['context_bytes']} bytes",
            flush=True,
        )
        started = time.perf_counter()
        # No repeat after provider failure, unknown completion, or malformed call.
        async with asyncio.timeout(task.call_seconds):
            response = await interaction.send(request)
        stage.update(
            model_seconds=time.perf_counter() - started,
            usage=asdict(response.usage) if response.usage else None,
            termination=response.termination,
            tool_calls=len(response.tool_calls),
            context_utilization=(
                response.usage.input_tokens / 32768
                if response.usage and response.usage.input_tokens is not None
                else None
            ),
            phase="RESPONSE_VALIDATION",
            response_source=str(response.source),
        )
        _save(turn / "response.json", asdict(response))
        stage["response_sha256"] = _hash(turn / "response.json")
        if response.source != selected_source:
            raise ValueError(
                "Model response source does not match model interaction source."
            )
        stage["phase"] = "PROPOSAL_ADMISSION"
        if response.termination == ModelTermination.OUTPUT_LIMIT:
            raise PatchProposalError("Output limit: no repair dispatch")
        if _hash(workspace / task.source) != source_hash:
            raise PatchProposalError("Source changed while proposal pending")
        if tools is not None:
            history.append(
                PromptMessage(
                    "assistant",
                    response.content,
                    response.tool_calls,
                    reasoning_content=response.reasoning_content
                    if thinking_enabled
                    else None,
                )
            )
            if not response.tool_calls:
                disposition = (
                    "MODEL_COMPLETED_WITHOUT_CHANGE_CHECK"
                    if check_changes_before_completion and proposals
                    else "MODEL_COMPLETED_WITHOUT_EDIT"
                )
                stage["disposition"] = disposition
                report["disposition"] = disposition
                _save(turn / "stage.json", stage, overwrite=True)
                return
            ids = [c.provider_call_id for c in response.tool_calls]
            if any(not identity for identity in ids) or len(set(ids)) != len(ids):
                raise PatchProposalError("Native calls require distinct nonempty IDs")
            if all(
                c.name in (*CONTEXT_TOOL_NAMES, *COMMAND_TOOL_NAMES)
                for c in response.tool_calls
            ):
                context_actions = await dispatch_context_calls(
                    response.tool_calls,
                    task=task,
                    tools=tools,
                    commands=commands,
                    turn=turn,
                    stage=stage,
                    report=report,
                    history=history,
                    context_actions=context_actions,
                    maximum_calls=maximum_calls,
                    number=number,
                    proposals=proposals,
                    started=started,
                    check_changes_before_completion=check_changes_before_completion,
                )
                if report.get("accepted"):
                    return
                continue
            if any(
                c.name
                not in (
                    {"replace_source"}
                    if observed_edits
                    else {"propose_edits"}
                    if coordinated_edits
                    else {"propose_edit"}
                )
                for c in response.tool_calls
            ):
                raise PatchProposalError("Do not mix Context calls with edit proposals")
        if proposals >= task.maximum_proposals:
            raise PatchProposalError("Edit proposal budget exhausted")
        proposals += 1
        stage["proposal_attempted"] = True
        transaction = bool(
            coordinated_edits
            and (
                observed_edits
                or (
                    len(response.tool_calls) == 1
                    and response.tool_calls[0].name == "propose_edits"
                )
            )
        )
        sources = {
            path: _read_text(resolve_path(workspace / path)).content
            if (workspace / path).exists()
            else ""
            for path in task.sources
        }
        plan: dict[str, Any] = {}
        try:
            if obligations is not None:
                obligations.admit(stage, report)
            if transaction:
                if tools is None:
                    raise PatchProposalError(
                        "Transactions require native observed Context"
                    )
                call = response.tool_calls[0]
                if observed_edits:
                    patches, updates, edits, plan = admit_observed(
                        workspace, sources, response.tool_calls, tools
                    )
                    _save(turn / "resolved-proposal.json", plan)
                else:
                    patches, updates, edits, plan = admit_transaction(
                        workspace, sources, call, tools
                    )
            else:
                call, patch, updated = _structured_edit_patch_from_calls(
                    workspace,
                    sources[task.source],
                    response.tool_calls,
                    source_path=task.source,
                )
                if tools is not None and not tools.observed(
                    json.loads(call.arguments_json)["old_text"]
                ):
                    raise PatchProposalError(
                        "Edit source was not observed at current version"
                    )
                values = json.loads(call.arguments_json)
                newline = "\r\n" if "\r\n" in sources[task.source] else "\n"
                old = values["old_text"].replace("\r\n", "\n").replace("\n", newline)
                replacement = (
                    values["new_text"].replace("\r\n", "\n").replace("\n", newline)
                )
                first = sources[task.source].index(old)
                patches, updates = {task.source: patch}, {task.source: updated}
                edits = [
                    {
                        "path": task.source,
                        "start": first,
                        "end": first + len(old),
                        "new_length": len(replacement),
                        "proposal_call_id": call.provider_call_id,
                    }
                ]
        except PatchProposalError as error:
            if (
                tools is None
                or "Unauthorized" in str(error)
                or (
                    not transaction
                    and not isinstance(error, ReadinessRefusalError)
                    and str(error)
                    not in {
                        "Old text must match exactly one source region",
                        "Edit source was not observed at current version",
                    }
                )
            ):
                raise
            # Admission failed before any write. Do not guess an edit or relax
            # uniqueness. Let the same bounded conversation correct its proposal.
            result: dict[str, Any] = {
                "status": "REFUSED",
                "error": (
                    "SOURCE_NOT_OBSERVED"
                    if "not observed" in str(error)
                    else "TRANSACTION_REFUSED"
                    if transaction
                    else "OLD_TEXT_NOT_UNIQUE"
                ),
                "diagnostic": str(error),
                "instruction": (
                    "No edit was applied. If the plan was refused, provide brief "
                    "text of at most 4096 characters; that is a metadata failure, "
                    "not evidence that the source anchors are wrong. "
                    "If API evidence failed, cite exact "
                    "inspect_api observation IDs; use [] when no APIs are required. "
                    "Never substitute source hashes or prose. Otherwise copy "
                    "old_text exactly from CURRENT "
                    "source, including indentation. Re-read the relevant range "
                    "if needed; do not invent helpers or approximate a match."
                ),
                "host_limits": {
                    "proposals_remaining": task.maximum_proposals - proposals,
                    "context_actions_remaining": task.tool_actions - context_actions,
                    "model_calls_remaining": maximum_calls - number,
                },
            }
            if error.details:
                result["details"] = error.details
                result["diagnostic"] += (
                    f" [{error.details['code']}; component "
                    f"{error.details.get('component_index', 'transaction')}; "
                    f"{error.details.get('path', 'authorized scope')}]. "
                    "See structured details; the entire transaction was refused."
                )
            call = response.tool_calls[0]
            if observed_edits:
                result["instruction"] = (
                    "No source was changed. Supply the authorized repository path "
                    "and nonempty literal old_text from a CURRENT source block; "
                    "the host resolves observed spans, not reference IDs. "
                    "Reinspect missing source. Headers, metadata and fences are "
                    "not Python source. The entire batch was rejected; preserve "
                    "all task requirements."
                    if task.path_edits
                    else "No source was changed. Use a current edit_ref from a read or "
                    "host feedback, and literal Python replacement text. No hashes, "
                    "arrays or JSON closing syntax belong in old_text/new_text. "
                    "The entire batch was rejected. Preserve all task requirements."
                )
            if isinstance(error, ReadinessRefusalError):
                result.update(error="CONTEXT_NOT_READY", instruction=str(error))
            history.extend(
                PromptMessage(
                    "tool",
                    json.dumps(result),
                    tool_call_id=native_call.provider_call_id,
                )
                for native_call in response.tool_calls
            )
            stage.update(
                disposition="PROPOSAL_REFUSED",
                proposal_valid=False,
                finished_at=str(Timestamp.now()),
                elapsed_seconds=time.perf_counter() - started,
            )
            _save(
                turn / "tools.json",
                [
                    {"call": asdict(c), "status": "REFUSED", "result": result}
                    for c in response.tool_calls
                ],
            )
            _save(turn / "stage.json", stage, overwrite=True)
            if proposals >= task.maximum_proposals:
                report["disposition"] = "PROPOSAL_ADMISSION_FAILED"
                return
            continue
        stage.update(
            proposal_valid=True,
            proposal_id=call.provider_call_id,
            phase="PATCH_APPLICATION",
            edits=edits,
            implementation_plan={k: v for k, v in plan.items() if k != "edits"},
            sources_before={
                p: _hash(workspace / p) if (workspace / p).exists() else None
                for p in updates
            },
            proposed_sources={
                p: hashlib.sha256(text.encode()).hexdigest()
                for p, text in updates.items()
            },
        )
        # Durable source expectations precede the one Git apply operation.
        if admit_edit is not None:
            for path, text in updates.items():
                admit_edit(path, text)
        _save(turn / "stage.json", stage, overwrite=True)
        await apply_source_patches(workspace, turn, patches)
        for path, text in updates.items():
            if _read_text(resolve_path(workspace / path)).content != text:
                raise PatchProposalError(
                    "Applied source differs from admitted transaction"
                )
        stage["sources_after"] = {p: _hash(workspace / p) for p in updates}
        stage["source_after"] = _hash(workspace / task.source)
        if tools is not None:
            tools.accept_transaction(updates, edits, call_id=call.provider_call_id)
        if task.mechanical_format:
            formatted = await format_sources(workspace, turn, task, admit_edit)
            if formatted:
                formatter_edits = [
                    {
                        "path": p,
                        "start": 0,
                        "end": len(updates.get(p, sources[p])),
                        "new_length": len(text),
                    }
                    for p, text in formatted.items()
                ]
                if tools is not None:
                    tools.accept_transaction(
                        formatted, formatter_edits, call_id=call.provider_call_id
                    )
                stage["mechanical_format"] = {
                    p: _hash(workspace / p) for p in formatted
                }
                stage["sources_after"].update(stage["mechanical_format"])
                stage["source_after"] = _hash(workspace / task.source)
        stage["phase"] = "VALIDATION"
        _save(turn / "stage.json", stage, overwrite=True)
        print(
            f"{Timestamp.now()} turn {number}: edit admitted; focused validation",
            flush=True,
        )
        validation = await validate_workspace(
            workspace, folder, task=task, commands=commands
        )
        stage.update(
            validation=validation,
            elapsed_seconds=time.perf_counter() - started,
            finished_at=str(Timestamp.now()),
            disposition=("ACCEPTED" if validation["accepted"] else "TESTS_FAILED"),
        )
        if validation["integrity"]["failed"]:
            _save(turn / "stage.json", stage, overwrite=True)
            raise ValueError("Validation source or frozen inputs changed")
        if tools is not None:
            tools.check_current()
            if observed_edits:
                tools.observations = [tools.reference(o) for o in tools.observations]
            result = {
                "status": stage["disposition"],
                "source_after": stage["source_after"],
                "path": task.source,
                "version": str(
                    tools.snapshot.resource_at(
                        RepositoryResourceAddress(task.source)
                    ).content_identity
                ),
                "validation": validation_feedback(
                    validation,
                    task=task,
                    source_version=(
                        str(
                            tools.snapshot.resource_at(
                                RepositoryResourceAddress(task.source)
                            ).content_identity
                        )
                        if tools is not None
                        else stage["source_after"]
                    ),
                    source_versions={
                        p: (
                            None
                            if p in task.new_paths
                            and RepositoryResourceAddress(p) not in tools.addresses
                            else str(
                                tools.snapshot.resource_at(
                                    RepositoryResourceAddress(p)
                                ).content_identity
                            )
                        )
                        for p in task.sources
                    },
                ),
                "source_observations": [
                    {
                        key: value
                        for key, value in o.items()
                        if key
                        in {
                            "path",
                            "version",
                            "span",
                            "text",
                            "derived_from",
                            "observation_call_id",
                            "edit_ref",
                        }
                    }
                    for o in tools.observations
                    if o["path"] in updates
                ],
                "edits": edits,
                "sources_after": stage["sources_after"],
                "host_limits": {
                    "proposals_remaining": task.maximum_proposals - proposals,
                    "context_actions_remaining": task.tool_actions - context_actions,
                    "model_calls_remaining": maximum_calls - number,
                },
                "instruction": (
                    "Host retained the edit. Revise CURRENT source after failure; "
                    "read it again if needed."
                ),
            }
            if not transaction:
                result.update(text=replacement, span=[first, first + len(replacement)])
                result["source_observations"] = [
                    o
                    for o in result["source_observations"]
                    if o.get("observation_call_id") != call.provider_call_id
                ]
            for index, native_call in enumerate(response.tool_calls):
                payload = (
                    result
                    if index == 0
                    else {
                        "status": result["status"],
                        "batch_result_call_id": call.provider_call_id,
                        "instruction": "See the first correlated Tool result for "
                        "full validation and current observations.",
                    }
                )
                history.append(
                    PromptMessage(
                        "tool",
                        json.dumps(payload, ensure_ascii=False),
                        tool_call_id=native_call.provider_call_id,
                    )
                )
            _save(
                turn / "tools.json",
                [
                    {
                        "call": asdict(c),
                        "status": "RETURNED",
                        "result": result
                        if i == 0
                        else {
                            "status": result["status"],
                            "batch_result_call_id": call.provider_call_id,
                        },
                    }
                    for i, c in enumerate(response.tool_calls)
                ],
            )
        _save(turn / "stage.json", stage, overwrite=True)
        print(
            f"{stage['finished_at']} turn {number}: {stage['disposition']}; "
            f"elapsed {stage['elapsed_seconds']:.2f}s",
            flush=True,
        )
        if validation["accepted"] and not check_changes_before_completion:
            report.update(accepted=True, disposition="ACCEPTED")
            return
        if proposals >= task.maximum_proposals and not validation["accepted"]:
            report["disposition"] = "REPAIR_BUDGET_EXHAUSTED"
            return
        # One latest state, not an ever-growing transcript; full assistant output
        # remains in response.json, with its useful content correlated here.
        feedback = {
            "turn": number,
            "proposal_id": call.provider_call_id,
            "proposal": asdict(call),
            "assistant_content": response.content[:4096],
            "source_after": stage["source_after"],
            "disposition": "EDIT_RETAINED_IN_ISOLATED_WORKSPACE; REVISE_CURRENT_SOURCE",
            "validation": validation_feedback(
                validation,
                task=task,
                source_version=(
                    str(
                        tools.snapshot.resource_at(
                            RepositoryResourceAddress(task.source)
                        ).content_identity
                    )
                    if tools is not None
                    else stage["source_after"]
                ),
            ),
        }
    report["disposition"] = (
        "REPAIR_BUDGET_EXHAUSTED"
        if tools is None or proposals >= task.maximum_proposals
        else "MODEL_CALL_BUDGET_EXHAUSTED"
    )

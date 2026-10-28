# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, TRY301, T201 -- bounded consumer composition

"""Operational turn sequencing, model admission, edits and repair feedback."""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, replace
from typing import TYPE_CHECKING, Any, Literal

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
from devtools.agents.coding import process as coding_process
from devtools.agents.coding.models import (
    CodingCompletion,
    CodingLimitError,
    CodingLimits,
    CodingProgress,
    CodingResult,
)
from devtools.context import (
    Repository,
    RepositoryResourceAddress,
)
from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Timestamp
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
    from devtools.models.interaction import (
        ModelInteraction,
        ModelResponse,
        ModelToolCall,
    )

from .prompt import fit_capacity, initial_history
from .tools import dispatch_context_calls


class _LegacyHost:
    """Legacy request, admission and journal policy; no model/repair loop."""

    def __init__(  # noqa: PLR0913 -- legacy public options retained
        self,
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
        self.workspace = workspace
        self.folder = folder
        self.interaction = interaction
        self.report = report
        self.acquire_context = acquire_context
        self.validate_workspace = validate_workspace
        self.validation_feedback = validation_feedback
        self.maximum_calls = maximum_calls
        self.task = task
        self.admit_edit = admit_edit
        self.thinking_enabled = thinking_enabled
        self.coordinated_edits = coordinated_edits
        self.observed_edits = observed_edits
        self.reasoning_effort = reasoning_effort
        self.request_settings = request_settings
        self.check_changes_before_completion = check_changes_before_completion
        self.commands = commands
        self.obligation_frame = obligation_frame
        self.measured_capacity = isinstance(self.interaction, LlamaCppInteraction)
        self.active_limit = (
            131072
            if self.measured_capacity
            else min(ACTIVE_BYTES, int((32768 - self.task.output_tokens - 4096) * 1.5))
        )
        self.repository = Repository.new()
        self.feedback_payload: dict[str, Any] = {"disposition": "INITIAL_PROPOSAL"}
        prepared_at = time.perf_counter()
        self.tools = (
            ContextTools(self.workspace, self.task, direct_reads=self.observed_edits)
            if self.task.context_mode == "on-demand"
            else None
        )
        self.commands = (
            self.commands
            if self.commands is not None
            else CodingCommands(self.workspace, self.folder, self.task)
        )
        self.obligations = (
            NativeObligations(self.obligation_frame, self.tools)
            if self.obligation_frame is not None and self.tools is not None
            else None
        )
        self.report["context_preparation_seconds"] = time.perf_counter() - prepared_at
        self.history = initial_history(
            self.task,
            maximum_calls=self.maximum_calls,
            coordinated_edits=self.coordinated_edits,
            observed_edits=self.observed_edits,
            tools=self.tools,
            check_changes_before_completion=self.check_changes_before_completion,
        )
        self.progress: CodingProgress
        self.turn: Path
        self.request: ModelRequest
        self.stage: dict[str, Any]
        self.started: float
        self.response: ModelResponse
        self.sources: dict[str, str]
        self.patches: dict[str, str]
        self.updates: dict[str, str]
        self.edits: list[dict[str, Any]]
        self.call: ModelToolCall
        self.plan: dict[str, Any]
        self.transaction: bool
        self.first: int
        self.replacement: str
        self.validation: dict[str, Any]
        self.native_feedback = self.tools is not None

    async def prepare(self, progress: CodingProgress) -> ModelRequest:
        self.progress = progress
        self.turn = self.folder / f"turn-{self.progress.number:02d}"
        self.turn.mkdir()
        self.resources: list[dict[str, Any]] = []
        self.omitted = 0
        if self.tools is None:
            self.context, self.resources = self.acquire_context(
                self.workspace, self.repository, task=self.task
            )
            self.prompt = (
                self.task.prompt
                + "\nHOST FEEDBACK:\n"
                + json.dumps(self.feedback_payload)
                + "\n"
                + self.context
            )
            self.model_prompt = Prompt(self.prompt, role="user")
        else:
            self.tools.check_current()
            _save(
                self.turn / "unprojected-prompt.json",
                asdict(Prompt("", role="messages", messages=tuple(self.history))),
            )
            self.active_bytes = self.active_limit
            if self.measured_capacity:
                self.active_bytes = max(
                    self.active_bytes,
                    len(json.dumps([asdict(m) for m in self.history]).encode()) + 2000,
                )
            self.messages, self.omitted = select_messages(
                self.history,
                source_path=self.task.source,
                maximum_bytes=self.active_bytes,
            )
            if self.obligations is not None:
                self.messages = self.obligations.project(self.messages)
            if self.task.path_edits:
                self.messages = present_sources(self.messages)
            self.model_prompt = Prompt("", role="messages", messages=self.messages)
            self.prompt = json.dumps(asdict(self.model_prompt))
            self.context = ""
        if not (self.measured_capacity and self.tools is not None) and len(
            self.prompt.encode()
        ) > (self.active_limit + 2000 if self.tools is not None else 60000):
            raise ValueError("Bounded Context byte allowance exceeded")
        self.request = ModelRequest(
            prompt=self.model_prompt,
            provider_settings=replace(
                self.request_settings or LlamaCppRequestSettings(),
                reasoning_effort=self.reasoning_effort,
            )
            if self.reasoning_effort
            else self.request_settings,
            settings=ModelSettings(
                maximum_output_tokens=self.task.output_tokens,
                thinking_enabled=self.thinking_enabled,
            ),
            tools=(
                observed_definition(path_based=self.task.path_edits)
                if self.observed_edits
                else transaction_definition(
                    self.task.sources, api_required=bool(self.task.api_targets)
                )
                if self.coordinated_edits
                else _structured_edit_definition(source_path=self.task.source),
                *(
                    (*self.tools.definitions, *command_definitions(self.task))
                    if self.tools is not None
                    and self.progress.actions < self.task.tool_actions
                    else ()
                ),
            ),
        )
        _save(self.turn / "request.json", asdict(self.request))
        self.measured_tokens = None
        if isinstance(self.interaction, LlamaCppInteraction):
            (
                self.request,
                self.prompt,
                self.omitted,
                self.measured_tokens,
            ) = await fit_capacity(
                self.interaction,
                self.request,
                task=self.task,
                history=self.history,
                on_demand=self.tools is not None,
                active_bytes=self.active_bytes
                if self.tools is not None
                else self.active_limit,
                context_actions=self.progress.actions,
                number=self.progress.number,
                maximum_calls=self.maximum_calls,
                proposals=self.progress.proposals,
                thinking_enabled=self.thinking_enabled,
                observed_edits=self.observed_edits,
                obligations=self.obligations,
                turn=self.turn,
                prompt=self.prompt,
                omitted=self.omitted,
                select_messages=select_messages,
            )
        self.source_hash = _hash(self.workspace / self.task.source)
        self.selected_source = self.interaction.source
        self.stage = {
            "number": self.progress.number,
            "selected_source": str(self.selected_source),
            "input_tokens_measured": self.measured_tokens,
            "capacity_safety_tokens": 2048 if self.measured_capacity else None,
            "started_at": str(Timestamp.now()),
            "started_monotonic": time.perf_counter(),
            "source_before": self.source_hash,
            "context": self.resources,
            "prompt_bytes": len(self.prompt.encode()),
            "context_bytes": len(self.context.encode()),
            "disposition": "DISPATCH_ATTEMPTED",
            "phase": "MODEL_REQUEST",
            "messages_omitted_from_active_context": self.omitted,
        }
        self.report["turns"].append(self.stage)
        if self.obligations is not None:
            self.obligations.retain(self.stage, self.report)
        self.stage["request_sha256"] = _hash(self.turn / "request.json")
        _save(self.turn / "stage.json", self.stage)
        print(
            f"{self.stage['started_at']} turn "
            f"{self.progress.number}/{self.maximum_calls}: model request; "
            f"Context {self.stage['context_bytes']} bytes",
            flush=True,
        )
        self.started = time.perf_counter()
        return self.request

    async def receive(self, response: ModelResponse) -> None:
        self.response = response
        self.stage.update(
            model_seconds=time.perf_counter() - self.started,
            usage=asdict(self.response.usage) if self.response.usage else None,
            termination=self.response.termination,
            tool_calls=len(self.response.tool_calls),
            context_utilization=self.response.usage.input_tokens / 32768
            if self.response.usage and self.response.usage.input_tokens is not None
            else None,
            phase="RESPONSE_VALIDATION",
            response_source=str(self.response.source),
        )
        _save(self.turn / "response.json", asdict(self.response))
        self.stage["response_sha256"] = _hash(self.turn / "response.json")

    def classify(self, response: ModelResponse) -> Literal["acquire", "edit", "stop"]:
        del response
        self.stage["phase"] = "PROPOSAL_ADMISSION"
        if self.response.termination == ModelTermination.OUTPUT_LIMIT:
            raise PatchProposalError("Output limit: no repair dispatch")
        if _hash(self.workspace / self.task.source) != self.source_hash:
            raise PatchProposalError("Source changed while proposal pending")
        if self.tools is not None:
            self.history.append(
                PromptMessage(
                    "assistant",
                    self.response.content,
                    self.response.tool_calls,
                    reasoning_content=self.response.reasoning_content
                    if self.thinking_enabled
                    else None,
                )
            )
            if not self.response.tool_calls:
                disposition = (
                    "MODEL_COMPLETED_WITHOUT_CHANGE_CHECK"
                    if self.check_changes_before_completion and self.progress.proposals
                    else "MODEL_COMPLETED_WITHOUT_EDIT"
                )
                self.stage["disposition"] = disposition
                self.report["disposition"] = disposition
                _save(self.turn / "stage.json", self.stage, overwrite=True)
                return "stop"
            ids = [c.provider_call_id for c in self.response.tool_calls]
            if any(not identity for identity in ids) or len(set(ids)) != len(ids):
                raise PatchProposalError("Native calls require distinct nonempty IDs")
            if all(
                c.name in (*CONTEXT_TOOL_NAMES, *COMMAND_TOOL_NAMES)
                for c in self.response.tool_calls
            ):
                return "acquire"
            if any(
                c.name
                not in (
                    {"replace_source"}
                    if self.observed_edits
                    else {"propose_edits"}
                    if self.coordinated_edits
                    else {"propose_edit"}
                )
                for c in self.response.tool_calls
            ):
                raise PatchProposalError("Do not mix Context calls with edit proposals")
        return "edit"

    async def acquire(self, response: ModelResponse) -> bool:
        del response
        if self.tools is None or self.commands is None:
            raise ValueError("Native Tool host is unavailable")
        progress = self.progress
        await dispatch_context_calls(
            self.response.tool_calls,
            task=self.task,
            tools=self.tools,
            commands=self.commands,
            turn=self.turn,
            stage=self.stage,
            report=self.report,
            history=self.history,
            context_actions=self.progress.actions,
            maximum_calls=self.maximum_calls,
            number=self.progress.number,
            proposals=self.progress.proposals,
            started=self.started,
            check_changes_before_completion=self.check_changes_before_completion,
            progress=progress,
        )
        return bool(self.report.get("accepted"))

    async def propose(  # noqa: C901, PLR0912 -- retained legacy admission policy
        self, response: ModelResponse
    ) -> tuple[dict[str, str], dict[str, str]] | None:
        del response
        self.stage["proposal_attempted"] = True
        self.transaction = bool(
            self.coordinated_edits
            and (
                self.observed_edits
                or (
                    len(self.response.tool_calls) == 1
                    and self.response.tool_calls[0].name == "propose_edits"
                )
            )
        )
        self.sources = {
            path: _read_text(resolve_path(self.workspace / path)).content
            if (self.workspace / path).exists()
            else ""
            for path in self.task.sources
        }
        self.plan = {}
        try:
            if self.obligations is not None:
                self.obligations.admit(self.stage, self.report)
            if self.transaction:
                if self.tools is None:
                    raise PatchProposalError(
                        "Transactions require native observed Context"
                    )
                self.call = self.response.tool_calls[0]
                if self.observed_edits:
                    self.patches, self.updates, self.edits, self.plan = admit_observed(
                        self.workspace,
                        self.sources,
                        self.response.tool_calls,
                        self.tools,
                    )
                    _save(self.turn / "resolved-proposal.json", self.plan)
                else:
                    self.patches, self.updates, self.edits, self.plan = (
                        admit_transaction(
                            self.workspace, self.sources, self.call, self.tools
                        )
                    )
            else:
                self.call, patch, updated = _structured_edit_patch_from_calls(
                    self.workspace,
                    self.sources[self.task.source],
                    self.response.tool_calls,
                    source_path=self.task.source,
                )
                if self.tools is not None and (
                    not self.tools.observed(
                        json.loads(self.call.arguments_json)["old_text"]
                    )
                ):
                    raise PatchProposalError(
                        "Edit source was not observed at current version"
                    )
                values = json.loads(self.call.arguments_json)
                newline = "\r\n" if "\r\n" in self.sources[self.task.source] else "\n"
                old = values["old_text"].replace("\r\n", "\n").replace("\n", newline)
                self.replacement = (
                    values["new_text"].replace("\r\n", "\n").replace("\n", newline)
                )
                self.first = self.sources[self.task.source].index(old)
                self.patches, self.updates = (
                    {self.task.source: patch},
                    {self.task.source: updated},
                )
                self.edits = [
                    {
                        "path": self.task.source,
                        "start": self.first,
                        "end": self.first + len(old),
                        "new_length": len(self.replacement),
                        "proposal_call_id": self.call.provider_call_id,
                    }
                ]
        except PatchProposalError as error:
            if (
                self.tools is None
                or "Unauthorized" in str(error)
                or (
                    not self.transaction
                    and (not isinstance(error, ReadinessRefusalError))
                    and (
                        str(error)
                        not in {
                            "Old text must match exactly one source region",
                            ("Edit source was not observed at current version"),
                        }
                    )
                )
            ):
                raise
            result: dict[str, Any] = {
                "status": "REFUSED",
                "error": "SOURCE_NOT_OBSERVED"
                if "not observed" in str(error)
                else "TRANSACTION_REFUSED"
                if self.transaction
                else "OLD_TEXT_NOT_UNIQUE",
                "diagnostic": str(error),
                "instruction": (
                    "No edit was applied. If the plan was refused, "
                    "provide brief text of at most 4096 characters; "
                    "that is a metadata failure, not evidence that the "
                    "source anchors are wrong. If API evidence failed, "
                    "cite exact inspect_api observation IDs; use [] "
                    "when no APIs are required. Never substitute "
                    "source hashes or prose. Otherwise copy old_text "
                    "exactly from CURRENT source, including "
                    "indentation. Re-read the relevant range if needed;"
                    " do not invent helpers or approximate a match."
                ),
                "host_limits": {
                    "proposals_remaining": self.task.maximum_proposals
                    - self.progress.proposals,
                    "context_actions_remaining": self.task.tool_actions
                    - self.progress.actions,
                    "model_calls_remaining": self.maximum_calls - self.progress.number,
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
            self.call = self.response.tool_calls[0]
            if self.observed_edits:
                result["instruction"] = (
                    (
                        "No source was changed. Supply the authorized "
                        "repository path and nonempty literal old_text "
                        "from a CURRENT source block; the host "
                        "resolves observed spans, not reference IDs. "
                        "Reinspect missing source. Headers, metadata "
                        "and fences are not Python source. The entire "
                        "batch was rejected; preserve all task "
                        "requirements."
                    )
                    if self.task.path_edits
                    else (
                        "No source was changed. Use a current edit_ref "
                        "from a read or host feedback, and literal "
                        "Python replacement text. No hashes, arrays or "
                        "JSON closing syntax belong in "
                        "old_text/new_text. The entire batch was "
                        "rejected. Preserve all task requirements."
                    )
                )
            if isinstance(error, ReadinessRefusalError):
                result.update(error="CONTEXT_NOT_READY", instruction=str(error))
            self.history.extend(
                PromptMessage(
                    "tool",
                    json.dumps(result),
                    tool_call_id=native_call.provider_call_id,
                )
                for native_call in self.response.tool_calls
            )
            self.stage.update(
                disposition="PROPOSAL_REFUSED",
                proposal_valid=False,
                finished_at=str(Timestamp.now()),
                elapsed_seconds=time.perf_counter() - self.started,
            )
            _save(
                self.turn / "tools.json",
                [
                    {"call": asdict(c), "status": "REFUSED", "result": result}
                    for c in self.response.tool_calls
                ],
            )
            _save(self.turn / "stage.json", self.stage, overwrite=True)
            if self.progress.proposals >= self.task.maximum_proposals:
                self.report["disposition"] = "PROPOSAL_ADMISSION_FAILED"
                return None
            return None
        self.stage.update(
            proposal_valid=True,
            proposal_id=self.call.provider_call_id,
            phase="PATCH_APPLICATION",
            edits=self.edits,
            implementation_plan={k: v for k, v in self.plan.items() if k != "edits"},
            sources_before={
                p: _hash(self.workspace / p) if (self.workspace / p).exists() else None
                for p in self.updates
            },
            proposed_sources={
                p: hashlib.sha256(text.encode()).hexdigest()
                for p, text in self.updates.items()
            },
        )
        return self.patches, self.updates

    async def apply(self, proposal: tuple[dict[str, str], dict[str, str]]) -> None:
        if proposal[0] is not self.patches:
            raise ValueError("Proposal differs from admitted source")
        if self.admit_edit is not None:
            for path, text in self.updates.items():
                self.admit_edit(path, text)
        _save(self.turn / "stage.json", self.stage, overwrite=True)
        await apply_source_patches(self.workspace, self.turn, self.patches)
        for path, text in self.updates.items():
            if _read_text(resolve_path(self.workspace / path)).content != text:
                raise PatchProposalError(
                    "Applied source differs from admitted transaction"
                )
        self.stage["sources_after"] = {
            p: _hash(self.workspace / p) for p in self.updates
        }
        self.stage["source_after"] = _hash(self.workspace / self.task.source)
        if self.tools is not None:
            self.tools.accept_transaction(
                self.updates, self.edits, call_id=self.call.provider_call_id
            )
        if self.task.mechanical_format:
            formatted = await format_sources(
                self.workspace, self.turn, self.task, self.admit_edit
            )
            if formatted:
                formatter_edits = [
                    {
                        "path": p,
                        "start": 0,
                        "end": len(self.updates.get(p, self.sources[p])),
                        "new_length": len(text),
                    }
                    for p, text in formatted.items()
                ]
                if self.tools is not None:
                    self.tools.accept_transaction(
                        formatted, formatter_edits, call_id=self.call.provider_call_id
                    )
                self.stage["mechanical_format"] = {
                    p: _hash(self.workspace / p) for p in formatted
                }
                self.stage["sources_after"].update(self.stage["mechanical_format"])
                self.stage["source_after"] = _hash(self.workspace / self.task.source)

    async def check(self, proposal: tuple[dict[str, str], dict[str, str]]) -> bool:
        del proposal
        self.stage["phase"] = "VALIDATION"
        _save(self.turn / "stage.json", self.stage, overwrite=True)
        print(
            f"{Timestamp.now()} turn {self.progress.number}: "
            "edit admitted; focused validation",
            flush=True,
        )
        self.validation = await self.validate_workspace(
            self.workspace, self.folder, task=self.task, commands=self.commands
        )
        self.stage.update(
            validation=self.validation,
            elapsed_seconds=time.perf_counter() - self.started,
            finished_at=str(Timestamp.now()),
            disposition="ACCEPTED" if self.validation["accepted"] else "TESTS_FAILED",
        )
        if self.validation["integrity"]["failed"]:
            _save(self.turn / "stage.json", self.stage, overwrite=True)
            raise ValueError("Validation source or frozen inputs changed")
        return bool(self.validation["accepted"])

    async def feedback(
        self,
        response: ModelResponse,
        proposal: tuple[dict[str, str], dict[str, str]],
        *,
        passed: bool,
    ) -> None:
        del response, proposal, passed
        if self.tools is not None:
            self.tools.check_current()
            if self.observed_edits:
                self.tools.observations = [
                    self.tools.reference(o) for o in self.tools.observations
                ]
            result = {
                "status": self.stage["disposition"],
                "source_after": self.stage["source_after"],
                "path": self.task.source,
                "version": str(
                    self.tools.snapshot.resource_at(
                        RepositoryResourceAddress(self.task.source)
                    ).content_identity
                ),
                "validation": self.validation_feedback(
                    self.validation,
                    task=self.task,
                    source_version=str(
                        self.tools.snapshot.resource_at(
                            RepositoryResourceAddress(self.task.source)
                        ).content_identity
                    )
                    if self.tools is not None
                    else self.stage["source_after"],
                    source_versions={
                        p: None
                        if p in self.task.new_paths
                        and RepositoryResourceAddress(p) not in self.tools.addresses
                        else str(
                            self.tools.snapshot.resource_at(
                                RepositoryResourceAddress(p)
                            ).content_identity
                        )
                        for p in self.task.sources
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
                    for o in self.tools.observations
                    if o["path"] in self.updates
                ],
                "edits": self.edits,
                "sources_after": self.stage["sources_after"],
                "host_limits": {
                    "proposals_remaining": self.task.maximum_proposals
                    - self.progress.proposals,
                    "context_actions_remaining": self.task.tool_actions
                    - self.progress.actions,
                    "model_calls_remaining": self.maximum_calls - self.progress.number,
                },
                "instruction": (
                    "Host retained the edit. Revise CURRENT source "
                    "after failure; read it again if needed."
                ),
            }
            if not self.transaction:
                result.update(
                    text=self.replacement,
                    span=[self.first, self.first + len(self.replacement)],
                )
                result["source_observations"] = [
                    o
                    for o in result["source_observations"]
                    if o.get("observation_call_id") != self.call.provider_call_id
                ]
            for index, native_call in enumerate(self.response.tool_calls):
                payload = (
                    result
                    if index == 0
                    else {
                        "status": result["status"],
                        "batch_result_call_id": self.call.provider_call_id,
                        "instruction": (
                            "See the first correlated Tool result for "
                            "full validation and current observations."
                        ),
                    }
                )
                self.history.append(
                    PromptMessage(
                        "tool",
                        json.dumps(payload, ensure_ascii=False),
                        tool_call_id=native_call.provider_call_id,
                    )
                )
            _save(
                self.turn / "tools.json",
                [
                    {
                        "call": asdict(c),
                        "status": "RETURNED",
                        "result": result
                        if i == 0
                        else {
                            "status": result["status"],
                            "batch_result_call_id": self.call.provider_call_id,
                        },
                    }
                    for i, c in enumerate(self.response.tool_calls)
                ],
            )
        _save(self.turn / "stage.json", self.stage, overwrite=True)
        print(
            f"{self.stage['finished_at']} turn {self.progress.number}: "
            f"{self.stage['disposition']}; "
            f"elapsed {self.stage['elapsed_seconds']:.2f}s",
            flush=True,
        )
        if self.validation["accepted"] and (not self.check_changes_before_completion):
            self.report.update(accepted=True, disposition="ACCEPTED")
            return
        if self.progress.proposals >= self.task.maximum_proposals and (
            not self.validation["accepted"]
        ):
            self.report["disposition"] = "REPAIR_BUDGET_EXHAUSTED"
            return
        self.feedback_payload = {
            "turn": self.progress.number,
            "proposal_id": self.call.provider_call_id,
            "proposal": asdict(self.call),
            "assistant_content": self.response.content[:4096],
            "source_after": self.stage["source_after"],
            "disposition": "EDIT_RETAINED_IN_ISOLATED_WORKSPACE; REVISE_CURRENT_SOURCE",
            "validation": self.validation_feedback(
                self.validation,
                task=self.task,
                source_version=str(
                    self.tools.snapshot.resource_at(
                        RepositoryResourceAddress(self.task.source)
                    ).content_identity
                )
                if self.tools is not None
                else self.stage["source_after"],
            ),
        }

    async def finish(self, result: CodingResult) -> CodingCompletion:
        if result.error is None:
            if result.accepted:
                self.report.update(accepted=True, disposition="ACCEPTED")
            elif result.disposition == "proposal_limit":
                self.report["disposition"] = (
                    "REPAIR_BUDGET_EXHAUSTED"
                    if self.stage.get("proposal_valid")
                    else "PROPOSAL_ADMISSION_FAILED"
                )
            elif result.disposition == "model_limit":
                self.report["disposition"] = (
                    "REPAIR_BUDGET_EXHAUSTED"
                    if self.tools is None
                    or self.progress.proposals >= self.task.maximum_proposals
                    else "MODEL_CALL_BUDGET_EXHAUSTED"
                )
        return CodingCompletion()


async def run_turns(  # noqa: PLR0913 -- preserved public compatibility signature
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
    """Preserve legacy policy and journals through the shared bounded coding Agent."""
    host = _LegacyHost(
        workspace,
        folder,
        interaction,
        report,
        acquire_context=acquire_context,
        validate_workspace=validate_workspace,
        validation_feedback=validation_feedback,
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
    result = await coding_process.run_coding_agent(
        interaction,
        limits=CodingLimits(
            maximum_calls,
            task.maximum_proposals,
            task.tool_actions if host.native_feedback else 0,
            Duration.seconds(task.call_seconds),
            Duration.seconds(task.wall_seconds),
            check_changes_before_completion,
        ),
        host=host,
    )
    if result.error is not None:
        if isinstance(result.error, CodingLimitError):
            raise PatchProposalError(str(result.error)) from result.error
        raise result.error

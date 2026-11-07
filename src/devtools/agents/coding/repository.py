# Copyright (c) 2026
"""A neutral repository coding host, not an application-specific task schema."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, replace
from functools import partial
from typing import TYPE_CHECKING, Literal, cast

from devtools.agents.coding import notes as working
from devtools.agents.coding.capacity import ContextPressure, TokenCapacity
from devtools.agents.coding.compaction.operation import SemanticCompactor
from devtools.agents.coding.custody import SourceCustody
from devtools.agents.coding.edits import (
    CodingEditError,
    admit_source_batch,
)
from devtools.agents.coding.edits import (
    EditLimits as EditLimits,  # noqa: PLC0414 -- maintained import facade
)
from devtools.agents.coding.edits import (
    SourceChange as SourceChange,  # noqa: PLC0414 -- maintained import facade
)
from devtools.agents.coding.models import (
    CodingCompletion,
    CodingEffect,
    CodingProgress,
    CodingResult,
)
from devtools.agents.coding.navigation import (
    FIND,
    READ_UNIT,
    TASK_FIND,
    NavigationPolicy,
    acquire_candidates,
    initial_messages,
    navigation_refusal,
    navigation_request,
    prepare_inventory,
    prepare_navigation,
    task_selection,
)
from devtools.agents.coding.projection import (
    ProjectionCapacityError,
    ProjectionOutcome,
    ProjectionPolicy,
    project_request,
    request_bytes,
    source_feedback,
)
from devtools.agents.coding.protocol import (
    CHECK,
    EDIT,
    READ,
    Invocation,
    arguments,
    capacity_refusal,
    classify_calls,
    read_request,
    source_refusal,
)
from devtools.agents.model_tools import (
    execute_model_tool_call,
    normalize_tool_descriptor,
)
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.planning.source import (
    SourceRangeDisclosureOption,
    materialize_source_range,
)
from devtools.context.repository.corpus import realize_repository_text_corpus
from devtools.context.retrieval import build_source_search_index
from devtools.context.working import NoteScope, WorkingNotes
from devtools.core.paths import resolve_path
from devtools.models.interaction import (
    ModelRequest,
    ModelResponse,
    ModelSettings,
    ModelToolCall,
    Prompt,
    PromptMessage,
)
from devtools.resources.filesystem import TextFile, write
from devtools.tools import ToolRunner
from devtools.tools.checks import FixedCheckPlan, FixedCheckResult, FixedCheckTool
from devtools.tools.source import (
    ScopedSourceTool,
    SourceReadRefusal,
    SourceReadRequest,
    SourceScope,
    select_source_read,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Mapping

    from devtools.agents.coding.compaction import SummaryCompaction
    from devtools.context.planning.materialization import ContextDisclosure
    from devtools.context.repository.corpus import RepositoryTextCorpusDefinition
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.core.paths import ResolvedPath
    from devtools.tools import Tool

_SETTINGS = ModelSettings()


@dataclass(frozen=True, slots=True)
class CodingObjective:
    """One bounded existing-text repair, with explicit host scope and checks.

    This concrete profile does not mandate Python, repository layout, provider,
    task JSON, public API oracle language, evidence storage or publication.
    """

    text: str
    scope: SourceScope
    editable: tuple[RepositoryResourceAddress, ...]
    checks: FixedCheckPlan
    edits: EditLimits
    disclosure_bytes: int
    prompt_bytes: int

    def __post_init__(self) -> None:
        """Require a finite editable subset of the authenticated host frame."""
        addresses = {r.address for r in self.scope.snapshot.resources}
        if (
            not self.text.strip()
            or not isinstance(self.editable, tuple)
            or (addresses and not self.editable)
            or len(set(self.editable)) != len(self.editable)
            or not set(self.editable) <= addresses
            or min(self.disclosure_bytes, self.prompt_bytes) <= 0
            or self.checks.root != self.scope.root
            or (
                self.checks.source_scope is not None
                and self.checks.source_scope != self.scope
            )
        ):
            msg = "Coding objective has an invalid or foreign source/check scope."
            raise ValueError(msg)


def write_source_changes(root: ResolvedPath, changes: tuple[SourceChange, ...]) -> None:
    """Host-selectable effect using existing atomic Resource writes, not a transaction.

    Call only with an admitted batch. Earlier per-file effects may survive a
    later failure. Checkout serialization and permission belong to the host.
    """
    for change in changes:
        write(
            TextFile(
                resolve_path(change.address.value, base_directory=root.value),
                change.after,
            ),
        )


class _ChangeTool:
    """Execute an already admitted source batch once through a host effect owner."""

    name = "apply_admitted_source"
    description = "Apply one host-admitted exact source batch."

    def __init__(
        self,
        scope: SourceScope,
        changes: tuple[SourceChange, ...],
        effect: Callable[[tuple[SourceChange, ...]], Awaitable[None]],
    ) -> None:
        self.scope, self.changes, self.effect = scope, changes, effect

    def validate(self, arguments: tuple[SourceChange, ...]) -> None:
        """Recheck admitted identities before invoking the host, never grant scope."""
        if arguments is not self.changes:
            msg = "Source batch is not the admitted proposal."
            raise ValueError(msg)
        self.scope.check_current()

    async def execute(self, arguments: tuple[SourceChange, ...]) -> None:
        """Invoke once; any exception can follow a completed external effect."""
        await self.effect(arguments)


class RepositoryCodingHost:
    """Operational source/edit/check host for the shared bounded coding process.

    Native continuation is transient, not a restart checkpoint. Required host
    callbacks supply effect authority, application/archive and restoration;
    readiness may reuse existing Localization without mandating one frame form.
    """

    native_feedback = True

    def __init__(  # noqa: PLR0913, PLR0915 -- explicit scope, effects and custody collaborators
        self,
        objective: CodingObjective,
        *,
        corpus: RepositoryTextCorpusDefinition,
        authorize: Callable[[ModelToolCall, object], Awaitable[None]],
        apply_changes: Callable[[tuple[SourceChange, ...]], Awaitable[None]],
        archive: Callable[[Mapping[RepositoryResourceAddress, str | None]], None],
        restore: Callable[[RepositoryResourceAddress, str | None], None],
        readiness: Callable[
            [RepositorySnapshot, tuple[SourceRangeDisclosureOption, ...]],
            None,
        ]
        | None = None,
        settings: ModelSettings = _SETTINGS,
        projection: ProjectionPolicy | None = None,
        summary: SummaryCompaction | None = None,
        navigation: bool = False,
        navigation_policy: NavigationPolicy | None = None,
        token_capacity: TokenCapacity | None = None,
        measure_input: Callable[[ModelRequest], Awaitable[int]] | None = None,
        warning_bytes: int | None = None,
        observe_context: Callable[[ContextPressure], None] | None = None,
        working_scope: NoteScope | None = None,
        observe_working: Callable[[dict[str, object]], None] | None = None,
        contract_sources: tuple[SourceRangeDisclosureOption, ...] = (),
    ) -> None:
        """Bind host authority and the existing Context/Tool/Resource substrates."""
        if corpus.discovery.repository_id != objective.scope.snapshot.repository_id:
            msg = "Coding corpus belongs to a foreign repository."
            raise ValueError(msg)
        self.objective, self.scope, self.corpus = objective, objective.scope, corpus
        warning = objective.prompt_bytes if warning_bytes is None else warning_bytes
        if (
            type(warning) is not int
            or not 0 < warning <= objective.prompt_bytes
            or (token_capacity is None) != (measure_input is None)
            or (
                token_capacity is not None
                and (
                    settings.maximum_output_tokens is None
                    or settings.maximum_output_tokens
                    > token_capacity.reserved_output_tokens
                )
            )
        ):
            msg = "Invalid coding request capacity or measurement qualification."
            raise ValueError(msg)
        self.token_capacity, self.measure_input = token_capacity, measure_input
        self.warning_bytes, self.observe_context = warning, observe_context
        self.context_pressure: list[ContextPressure] = []
        self._original_bytes = 0
        if projection is not None and projection.trigger_bytes > objective.prompt_bytes:
            msg = "Projection watermarks exceed the host byte ceiling."
            raise ValueError(msg)
        self.projection = projection
        self.navigation = navigation
        if navigation_policy is not None and not navigation:
            msg = "Task navigation policy requires native navigation."
            raise ValueError(msg)
        self.navigation_policy = navigation_policy
        if summary is not None and projection is None:
            msg = "Semantic compaction requires active Context projection."
            raise ValueError(msg)
        self.compaction = SemanticCompactor(summary) if summary is not None else None
        self.authorize, self.effect = authorize, apply_changes
        self.archive, self.restore, self.readiness, self.settings = (
            archive,
            restore,
            readiness,
            settings,
        )
        self.custody = SourceCustody(
            self.scope.root,
            {
                r.address: r.content
                for r in self.scope.snapshot.resources
                if r.address in objective.editable
            },
            maximum_bytes=self.scope.maximum_resource_bytes,
        )
        self.messages = initial_messages(objective.text)
        if (
            working_scope is not None
            and (
                not working_scope.role.startswith("coding-worker:")
                or not working_scope.role.removeprefix("coding-worker:").strip()
            )
        ) or (observe_working is not None and working_scope is None):
            msg = "Coding working Context requires its own coding-worker scope."
            raise ValueError(msg)
        self.working = WorkingNotes(working_scope, {}) if working_scope else None
        self.observe_working = observe_working
        self.working_refusal: str | None = None
        if self.working is not None:
            self.messages = [
                PromptMessage("system", working.PROCEDURE),
                self.messages[1],  # Preserve the existing inventory/navigation slot.
                self.messages[0],
                PromptMessage("user", ""),
            ]
        self.disclosures: list[SourceRangeDisclosureOption] = []
        self.source_results: list[ContextDisclosure] = []
        self.active_disclosures: tuple[SourceRangeDisclosureOption, ...] = ()
        self.projection_outcomes: list[ProjectionOutcome] = []
        self.projection_error: BaseException | None = None
        self._source_messages: dict[int, tuple[SourceRangeDisclosureOption, ...]] = {}
        self._check_feedback: set[int] = set()
        self.requests: list[ModelRequest] = []
        self.responses: list[ModelResponse] = []
        self.check_results: list[tuple[FixedCheckResult, ...]] = []
        self.last_completion = CodingCompletion()
        self._index()
        if (
            not isinstance(contract_sources, tuple)
            or len(contract_sources) > working.MAXIMUM_CONTRACT_SOURCES
            or len({o.identity for o in contract_sources}) != len(contract_sources)
            or any(o.snapshot_id != self.scope.snapshot.id for o in contract_sources)
        ):
            msg = (
                "Coding contract witnesses require distinct current source selections."
            )
            raise ValueError(msg)
        self.contract_sources = contract_sources
        self._contract_index = len(self.messages) if contract_sources else None
        if contract_sources:
            message, current = working.contract_message(
                contract_sources,
                self.scope.snapshot,
            )
            self.messages.append(message)
            self._source_messages[len(self.messages) - 1] = current
            self.disclosures.extend(current)
            self.source_results.extend(
                materialize_source_range(self.scope.snapshot, o) for o in current
            )

    def _index(self) -> None:
        self.index = build_source_search_index(
            self.scope.snapshot,
            corpus=realize_repository_text_corpus(
                definition=self.corpus,
                snapshot=self.scope.snapshot,
            ),
        )

    def build_request(self, messages: tuple[PromptMessage, ...]) -> ModelRequest:
        """Assemble all host-selected schemas before complete-input accounting.

        Hosts exposing additional operations override this pure assembly seam,
        not append schemas after preparation has checked its byte ceiling.
        """
        return ModelRequest(
            Prompt("", "messages", messages),
            settings=self.settings,
            tools=tuple(
                normalize_tool_descriptor(d)
                for d in (
                    READ,
                    EDIT,
                    CHECK,
                    *(
                        (TASK_FIND if self.navigation_policy else FIND, READ_UNIT)
                        if self.navigation
                        else ()
                    ),
                )
            ),
        )

    async def prepare(self, progress: CodingProgress) -> ModelRequest:
        """Measure bytes and optional provider tokens before acting-model entry.

        Pressure observers receive facts even for an impossible protected minimum.
        Observer or tokenizer failure stops entry; neither operation is retried.
        """
        self._original_bytes = 0
        prior_outcomes = len(self.projection_outcomes)
        measured = None
        request = None
        action = "refused"
        try:
            request = await self._prepare(progress)
            if self.token_capacity is not None and self.measure_input is not None:
                history = tuple(self.messages)
                count = await self.measure_input(request)
                self.scope.check_current()
                if tuple(self.messages) != history:
                    msg = "History changed during input token measurement."
                    raise ValueError(msg)
                if type(count) is not int or count < 0:
                    msg = "Input token measurement is invalid."
                    raise ValueError(msg)
                measured = count
                if measured > self.token_capacity.input_tokens:
                    msg = (
                        "Measured input exceeds the qualified token allowance "
                        "or is invalid."
                    )
                    raise ValueError(msg)
            action = "ready"
            return request
        finally:
            if self._original_bytes:
                outcome = (
                    self.projection_outcomes[-1]
                    if len(self.projection_outcomes) > prior_outcomes
                    else None
                )
                size = (
                    request_bytes(request)
                    if request is not None
                    else (
                        outcome.resulting_bytes
                        if outcome is not None
                        else self._original_bytes
                    )
                )
                fact = ContextPressure(
                    self._original_bytes,
                    size,
                    self.objective.prompt_bytes,
                    self.warning_bytes,
                    max(self._original_bytes, size) >= self.warning_bytes,
                    (
                        "adaptive"
                        if self.compaction.config.adaptive is not None
                        else "semantic"
                    )
                    if self.compaction is not None
                    else ("deterministic" if self.projection is not None else "strict"),
                    "reduced"
                    if action == "ready" and size < self._original_bytes
                    else action,
                    measured,
                    self.token_capacity,
                )
                self.context_pressure.append(fact)
                if self.observe_context is not None:
                    self.observe_context(fact)

    async def _prepare(self, progress: CodingProgress) -> ModelRequest:  # noqa: C901, PLR0912, PLR0915 -- atomic projection and currentness guards
        """Authenticate source and atomically install a valid active projection."""
        self.progress = progress
        self.scope.check_current()
        if self._contract_index is not None:
            message, current = working.contract_message(
                self.contract_sources,
                self.scope.snapshot,
            )
            self.messages[self._contract_index] = message
            self._source_messages[self._contract_index] = current
        if self.working is not None:
            working.refresh_sources(
                self.working,
                self.scope.snapshot,
                tuple(self.disclosures),
            )
            self.messages[3] = working.message(self.working, self.working_refusal)
            if self.observe_working is not None:
                self.observe_working(self.working.checkpoint())
        prepare_inventory(
            self.messages,
            self.scope,
            self.objective.editable,
            self.objective.prompt_bytes,
        )
        prepare_navigation(
            self.messages,
            self.index,
            self.objective.text,
            self.navigation_policy,
            has_inventory=True,
        )
        request = self.build_request(tuple(self.messages))
        self._original_bytes = request_bytes(request)
        if self.projection is not None:
            policy = self.projection
            try:
                if any(not e.acknowledged for e in progress.effects):
                    msg = "Unacknowledged effects require reconciliation."
                    raise ValueError(msg)  # noqa: TRY301 -- retain original preparation failure
                protected = frozenset(self._check_feedback) | (
                    frozenset(
                        i
                        for i, values in self._source_messages.items()
                        if any(o.snapshot_id == self.scope.snapshot.id for o in values)
                    )
                    if self.readiness is not None
                    else frozenset()
                )
                if self._contract_index is not None:
                    protected |= frozenset({self._contract_index})
                if self.compaction is not None:
                    protected |= self.compaction.protect(request.prompt.messages)
                outcome = project_request(
                    request,
                    policy=self.projection,
                    hard_bytes=self.objective.prompt_bytes,
                    snapshot=self.scope.snapshot,
                    sources=self._source_messages,
                    protected_indices=protected,
                    previous_sources=self.active_disclosures,
                )
                self.projection_outcomes.append(outcome)
                if self.compaction is not None:

                    def summarized(
                        indices: frozenset[int],
                        note: PromptMessage,
                    ) -> ProjectionOutcome:
                        self.scope.check_current()
                        if tuple(self.messages) != request.prompt.messages:
                            msg = "Original history changed during semantic compaction."
                            raise ValueError(msg)  # noqa: TRY301 -- no stale projection
                        return project_request(
                            request,
                            policy=policy,
                            hard_bytes=self.objective.prompt_bytes,
                            snapshot=self.scope.snapshot,
                            sources=self._source_messages,
                            protected_indices=protected,
                            previous_sources=self.active_disclosures,
                            summarized_indices=indices,
                            summary=note,
                        )

                    selected = await self.compaction.project(
                        request,
                        outcome,
                        protected=protected,
                        sources=self._source_messages,
                        snapshot=str(self.scope.snapshot.id),
                        project=summarized,
                    )
                    # Also recheck after optional failure: a fallback is not safe
                    # if an external actor changed source during the await.
                    self.scope.check_current()
                    if tuple(self.messages) != request.prompt.messages:
                        msg = "Original history changed during semantic compaction."
                        raise ValueError(msg)  # noqa: TRY301 -- no stale fallback installation
                    if selected is not outcome:
                        self.projection_outcomes.append(selected)
                    outcome = selected
                if outcome.status == "insufficient":
                    raise ProjectionCapacityError(outcome)  # noqa: TRY301 -- no partial active-state installation
            except (Exception, asyncio.CancelledError) as error:
                self.projection_error = error
                raise
            request = outcome.request
            self.active_disclosures = outcome.active_sources
            self.projection_error = None
        elif request_bytes(request) > self.objective.prompt_bytes:
            msg = "Coding Prompt byte budget exceeded."
            raise ValueError(msg)
        self.requests.append(request)
        return request

    def request_compaction(self) -> None:
        """Request one host-authorized auxiliary strategy at the next preparation.

        This is not a model Tool, a budget reset, or permission to disclose all
        history. The configured selector and finite envelope remain authoritative.
        """
        if self.compaction is None:
            msg = "No semantic compaction interaction is authorized."
            raise ValueError(msg)
        self.compaction.pending = True

    async def receive(self, response: ModelResponse) -> None:
        """Retain normalized response facts; the shared process authenticates source."""
        self.responses.append(response)

    def classify(self, response: ModelResponse) -> Literal["acquire", "edit", "stop"]:
        """Refuse mixed/unavailable operations before any partial batch executes."""
        self.scope.check_current()
        if self.working is not None:
            working.refresh_sources(
                self.working,
                self.scope.snapshot,
                tuple(self.disclosures),
            )
            try:
                admitted = working.accept(self.working, response.content)
            except ValueError as error:
                self.working_refusal = str(error)[:256]
            else:
                if admitted:
                    self.working_refusal = None
                    if self.observe_working is not None:
                        self.observe_working(self.working.checkpoint())
        self.messages.append(
            PromptMessage(
                "assistant",
                response.content,
                response.tool_calls,
                reasoning_content=response.reasoning_content
                if self.settings.thinking_enabled
                else None,
            ),
        )
        return classify_calls(response.tool_calls, navigation=self.navigation)

    def _feedback(
        self,
        call: ModelToolCall,
        value: object,
        *,
        sources: tuple[SourceRangeDisclosureOption, ...] = (),
    ) -> None:
        if sources:
            self._source_messages[len(self.messages)] = sources
        self.messages.append(
            PromptMessage(
                "tool",
                json.dumps(value, ensure_ascii=False),
                tool_call_id=call.provider_call_id,
            ),
        )

    def _acquisition_fits(
        self,
        pending: tuple[PromptMessage, ...],
        options: tuple[SourceRangeDisclosureOption | None, ...] = (),
    ) -> bool:
        """Reserve complete replies; preview only the host's existing projection.

        No auxiliary model, active-state installation or history mutation occurs.
        Existing opt-in projection retains its source shortening/provenance and
        protects mandatory instructions, check feedback and readiness.
        """
        request = self.build_request((*self.messages, *pending))
        if self.projection is None:
            return request_bytes(request) <= self.objective.prompt_bytes
        sources = dict(self._source_messages)
        sources.update(
            {
                len(self.messages) + i: (option,)
                for i, option in enumerate(options)
                if option is not None
            },
        )
        protected = frozenset(self._check_feedback)
        if self.readiness is not None:
            protected |= frozenset(
                i
                for i, values in sources.items()
                if any(o.snapshot_id == self.scope.snapshot.id for o in values)
            )
        if self.compaction is not None:
            protected |= self.compaction.protect(request.prompt.messages)
        return (
            project_request(
                request,
                policy=self.projection,
                hard_bytes=self.objective.prompt_bytes,
                snapshot=self.scope.snapshot,
                sources=sources,
                protected_indices=protected,
                previous_sources=self.active_disclosures,
            ).status
            != "insufficient"
        )

    def _feedback_fits(
        self,
        call: ModelToolCall,
        value: object,
        pending: tuple[PromptMessage, ...],
        option: SourceRangeDisclosureOption | None = None,
    ) -> bool:
        """Charge this exact feedback plus every remaining correlated reservation."""
        return self._acquisition_fits(
            (
                PromptMessage(
                    "tool",
                    json.dumps(value, ensure_ascii=False),
                    tool_call_id=call.provider_call_id,
                ),
                *pending,
            ),
            (option,),
        )

    def _source_batch_fits(self, response: ModelResponse) -> bool:
        """Preflight an exact read/check batch before unrelated reads enter Tools.

        Malformed pure arguments keep their existing per-call refusal/failure
        boundary. Operational errors are never caught or reclassified here.
        """
        if len(response.tool_calls) == 1 or any(
            c.name not in {READ.name, READ_UNIT.name, CHECK.name}
            for c in response.tool_calls
        ):
            return True
        pending: list[PromptMessage] = []
        options: list[SourceRangeDisclosureOption | None] = []
        for call in response.tool_calls:
            option = None
            value: object = {"passed": False}
            if call.name != CHECK.name:
                try:
                    requested = read_request(
                        call.arguments_json,
                        index=self.index,
                        purpose=self.objective.text,
                        maximum_bytes=self.objective.disclosure_bytes,
                        by_unit=call.name == READ_UNIT.name,
                    )
                except (TypeError, ValueError):
                    return True
                selected = select_source_read(requested)
                option = None if isinstance(selected, SourceReadRefusal) else selected
                value = (
                    source_refusal(selected.request)
                    if isinstance(selected, SourceReadRefusal)
                    else source_feedback(selected, selected.text)
                )
            options.append(option)
            pending.append(
                PromptMessage(
                    "tool",
                    json.dumps(value, ensure_ascii=False),
                    tool_call_id=call.provider_call_id,
                ),
            )
        return self._acquisition_fits(tuple(pending), tuple(options))

    async def _acquire_source(
        self,
        call: ModelToolCall,
        pending: tuple[PromptMessage, ...],
        effect: CodingEffect,
        *,
        batch_fits: bool,
    ) -> None:
        """Admit exact known source feedback before Tool entry, never retry errors."""
        tool: Tool[SourceReadRequest, ContextDisclosure | SourceReadRefusal] = (
            ScopedSourceTool(
                self.scope,
                maximum_bytes=self.objective.disclosure_bytes,
            )
        )
        requested = read_request(
            call.arguments_json,
            index=self.index,
            purpose=self.objective.text,
            maximum_bytes=self.objective.disclosure_bytes,
            by_unit=call.name == READ_UNIT.name,
        )
        tool.validate(requested)
        selected = select_source_read(requested)
        expected = (
            source_refusal(selected.request)
            if isinstance(selected, SourceReadRefusal)
            else source_feedback(selected, selected.text)
        )
        option = None if isinstance(selected, SourceReadRefusal) else selected
        if not batch_fits or not self._feedback_fits(call, expected, pending, option):
            await self.authorize(call, requested)
            tool.validate(requested)
            refusal = capacity_refusal()
            fits = self._feedback_fits(call, refusal, pending)
            self._feedback(call, refusal)
            effect.acknowledged = True
            if not fits:
                msg = (
                    "Coding capacity: correlated refusal feedback cannot fit; "
                    "source Tool not entered."
                )
                raise ValueError(msg)
            return
        if isinstance(selected, SourceReadRefusal):
            await self.authorize(call, requested)
            tool.validate(requested)
            self._feedback(call, expected)
            return
        disclosure = await execute_model_tool_call(
            call,
            invocation=Invocation[SourceReadRequest](
                READ_UNIT if call.name == READ_UNIT.name else READ,
                partial(
                    read_request,
                    index=self.index,
                    purpose=self.objective.text,
                    maximum_bytes=self.objective.disclosure_bytes,
                    by_unit=call.name == READ_UNIT.name,
                ),
            ),
            tool=tool,
            admit=self.authorize,
            runner=ToolRunner(),
        )
        # Returned results are known completions; exceptions above stay unknown.
        effect.acknowledged = True
        if isinstance(disclosure, SourceReadRefusal):
            self._feedback(
                call,
                {
                    **source_refusal(disclosure.request),
                    "tool_operation_entered": True,
                },
            )
            msg = (
                "Source Tool completed with a different range refusal after preflight."
            )
            raise TypeError(msg)
        option = cast(
            "SourceRangeDisclosureOption",
            disclosure.items[0].native_provenance,
        )
        self.source_results.append(disclosure)
        actual = source_feedback(option, disclosure.items[0].text)
        if actual != expected:
            self._feedback(
                call,
                {
                    "status": "UNDISCLOSED",
                    "tool_operation_entered": True,
                    "source_disclosure_entered": True,
                    "payload": actual,
                },
            )
            msg = (
                "Completed source feedback differs from capacity preflight; "
                "payload retained, no edit witness."
            )
            raise ValueError(msg)
        self.disclosures.append(option)
        self._feedback(call, actual, sources=(option,))

    async def acquire(self, response: ModelResponse) -> bool:
        """Use shared composition and retain each bounded Tool result."""
        ready = False
        pending = [
            PromptMessage(
                "tool",
                "\\" * (self.objective.disclosure_bytes + 1024)
                if call.name == FIND.name
                else json.dumps(
                    {"passed": False}
                    if call.name == CHECK.name
                    else capacity_refusal(),
                    ensure_ascii=False,
                ),
                tool_call_id=call.provider_call_id,
            )
            for call in response.tool_calls
        ]
        if (
            len(response.tool_calls)
            > self.progress.limits.tool_actions - self.progress.actions
        ):
            for call in response.tool_calls:
                self._feedback(call, {"status": "REFUSED", "reason": "action_budget"})
            return False
        batch_fits = self._source_batch_fits(response)
        for call in response.tool_calls:
            effect = self.progress.claim_action(call.provider_call_id)
            pending.pop(0)

            if self.navigation and call.name == FIND.name:
                try:
                    values = arguments(
                        call.arguments_json,
                        set(),
                        optional=frozenset({"path", "query", "mode", "offset"})
                        | (
                            frozenset({"browse"})
                            if self.navigation_policy
                            else frozenset()
                        ),
                    )
                    policy = self.navigation_policy
                    selection = (
                        task_selection(values, self.objective.text)
                        if policy
                        else navigation_request(values)
                    )
                except (TypeError, ValueError):
                    self._feedback(call, navigation_refusal())
                    effect.acknowledged = True
                    continue
                result = await acquire_candidates(
                    call,
                    selection=selection,
                    index=self.index,
                    scope=self.scope,
                    admit=self.authorize,
                    maximum_bytes=self.objective.disclosure_bytes,
                    policy=policy,
                    messages=self.messages,
                    progress=self.progress,
                )
                self._feedback(call, result)
            elif call.name in {READ.name, READ_UNIT.name}:
                await self._acquire_source(
                    call,
                    tuple(pending),
                    effect,
                    batch_fits=batch_fits,
                )
            else:
                arguments(call.arguments_json, set())
                await self.authorize(call, self.objective.checks)
                passed = await self.check(())
                self.progress.candidate_validated = passed
                ready = passed and self.progress.proposals > 0
                self._check_feedback = {len(self.messages)}
                self._feedback(call, {"passed": passed})
            effect.acknowledged = True
        return ready

    async def propose(self, response: ModelResponse) -> tuple[SourceChange, ...] | None:
        """Admit all exact, observed, current, nonoverlapping source anchors first."""
        self.pending_calls = response.tool_calls
        try:
            self.scope.check_current()
            available = (
                self.active_disclosures
                if self.projection is not None
                else tuple(self.disclosures)
            )
            if self.readiness is not None:
                self.readiness(self.scope.snapshot, available)
            if len(response.tool_calls) > self.objective.edits.operations:
                msg = "Edit operation limit exceeded."
                raise CodingEditError(msg)
            return admit_source_batch(
                (
                    arguments(call.arguments_json, {"path", "old_text", "new_text"})
                    for call in response.tool_calls
                ),
                snapshot=self.scope.snapshot,
                editable=self.objective.editable,
                available=available,
                limits=self.objective.edits,
            )
        except (ValueError, TypeError) as error:
            for call in response.tool_calls:
                self._feedback(call, {"status": "REFUSED", "reason": str(error)})
            return None

    async def apply(self, proposal: tuple[SourceChange, ...]) -> None:
        """Record expected source before effects and verify installed bytes."""
        call = self.pending_calls[0]

        async def admit(
            selected_call: ModelToolCall,
            changes: tuple[SourceChange, ...],
        ) -> None:
            await self.authorize(selected_call, changes)
            for change in changes:
                self.custody.expect(change.address, change.after)

        def selected(serialized: str) -> tuple[SourceChange, ...]:
            if serialized != call.arguments_json:
                msg = "Edit call differs from admitted arguments."
                raise ValueError(msg)
            return proposal

        await execute_model_tool_call(
            call,
            invocation=Invocation(EDIT, selected),
            tool=_ChangeTool(self.scope, proposal, self.effect),
            admit=admit,
            runner=ToolRunner(),
        )
        observed = SourceScope.observe(
            root=self.scope.root,
            repository=Repository(self.scope.snapshot.repository_id),
            addresses=tuple(r.address for r in self.scope.snapshot.resources),
            maximum_resource_bytes=self.scope.maximum_resource_bytes,
        )
        expected = {r.address: r.content for r in self.scope.snapshot.resources}
        expected.update({c.address: c.after for c in proposal})
        if {r.address: r.content for r in observed.snapshot.resources} != expected:
            msg = "Installed source differs from the admitted candidate."
            raise ValueError(msg)
        self.scope = observed
        self.active_disclosures = ()
        self._index()
        self.disclosures = []
        for change in proposal:
            unit = next(
                u
                for u in self.index.views[0].units
                if u.resource.address == change.address
            )
            option = SourceRangeDisclosureOption(
                self.objective.text,
                unit,
                0,
                unit.end,
                self.objective.disclosure_bytes,
            )
            # The exact after-image is already known; materialize it through Context.
            disclosure = await ToolRunner().execute(
                ScopedSourceTool(
                    self.scope,
                    maximum_bytes=self.objective.disclosure_bytes,
                ),
                option,
            )
            self.source_results.append(disclosure)
            self.disclosures.append(option)

    async def check(self, proposal: tuple[SourceChange, ...]) -> bool:
        """Execute the unchanged host plan and preserve each known result in order."""
        del proposal
        tool = FixedCheckTool(replace(self.objective.checks, source_scope=self.scope))
        results: list[FixedCheckResult] = []
        self.check_results.append(())
        for check in tool.plan.checks:
            effect = CodingEffect("check", (), check_name=check.name)
            self.progress.effects.append(effect)
            result = await ToolRunner().execute(tool, check.name)
            effect.acknowledged = True
            results.append(result)
            self.check_results[-1] = tuple(results)
        return all(r.passed for r in results)

    async def feedback(
        self,
        response: ModelResponse,
        proposal: tuple[SourceChange, ...],
        *,
        passed: bool,
    ) -> None:
        """Return bounded actual diagnostics under native call IDs."""
        del proposal
        value = {
            "passed": passed,
            "checks": [
                {
                    "name": r.check.name,
                    "exit_code": r.command_result.exit_code,
                    "stdout": r.command_result.stdout.decode(errors="replace"),
                    "stderr": r.command_result.stderr.decode(errors="replace"),
                    "current": r.inputs_current,
                }
                for r in self.check_results[-1]
            ],
            "sources": [
                {
                    "path": str(o.unit.resource.address),
                    "text": o.text,
                    "span": o.span,
                    "version": str(o.unit.resource.content_identity),
                }
                for o in self.disclosures
            ],
        }
        self._check_feedback = set()
        for call in response.tool_calls:
            self._check_feedback.add(len(self.messages))
            self._feedback(call, value, sources=tuple(self.disclosures))

    async def finish(self, result: CodingResult) -> CodingCompletion:
        """Archive and restore known source, retaining secondary failures."""
        del result
        current = self.custody.capture()
        error: BaseException | None = None
        try:
            self.archive(current)
        except (Exception, asyncio.CancelledError) as failure:  # noqa: BLE001 -- retain known candidate and still attempt authorized cleanup
            error = failure
        try:
            self.last_completion = self.custody.restore_known(current, self.restore)
        except (Exception, asyncio.CancelledError) as failure:  # noqa: BLE001 -- no retry or false restoration fact
            error = error or failure
        return replace(self.last_completion, error=error)

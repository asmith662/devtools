# Copyright (c) 2026
"""A neutral repository coding host, not an application-specific task schema."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Literal, cast

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
    navigation_feedback,
    navigation_request,
    unit_read_request,
)
from devtools.agents.coding.projection import (
    ProjectionCapacityError,
    ProjectionOutcome,
    ProjectionPolicy,
    project_request,
    request_bytes,
    source_feedback,
)
from devtools.agents.model_tools import (
    execute_model_tool_call,
    normalize_tool_descriptor,
)
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.context.repository.corpus import realize_repository_text_corpus
from devtools.context.retrieval import build_source_search_index
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
from devtools.tools import ToolDescriptor, ToolRunner
from devtools.tools.checks import FixedCheckPlan, FixedCheckResult, FixedCheckTool
from devtools.tools.source import (
    ScopedSourceNavigationTool,
    ScopedSourceTool,
    SourceNavigationRequest,
    SourceReadRefusal,
    SourceReadRequest,
    SourceScope,
    source_read_bounds,
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
_READ = ToolDescriptor(
    "read_source",
    "Read half-open Unicode offsets; omit end for a byte-bounded remaining prefix.",
    (
        '{"type":"object","properties":{"path":{"type":"string"},'
        '"start":{"type":"integer"},"end":{"type":"integer"}},'
        '"required":["path","start"],"additionalProperties":'
        "false}"
    ),
)
_EDIT = ToolDescriptor(
    "replace_source",
    ("Propose an exact unique observed replacement; host admission is required."),
    (
        '{"type":"object","properties":{"path":{"type":"string"},'
        '"old_text":{"type":"string"},"new_text":{"type":"string"}},'
        '"required":["path","old_text","new_text"],'
        '"additionalProperties":false}'
    ),
)
_CHECK = ToolDescriptor(
    "validate_candidate",
    "Request the host-fixed candidate checks.",
    '{"type":"object","maxProperties":0}',
)


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
            or not self.editable
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


@dataclass(frozen=True, slots=True)
class _Invocation[Input]:
    """One explicitly selected native operation, not a Tool registry."""

    descriptor: ToolDescriptor
    decode: Callable[[str], Input]

    def materialize(self, serialized_arguments: str) -> Input:
        """Delegate effect-free materialization to the selected host operation."""
        return self.decode(serialized_arguments)


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


def _arguments(
    serialized: str,
    fields: set[str],
    *,
    optional: frozenset[str] = frozenset(),
) -> dict[str, object]:
    """Validate this host's small native argument object, not arbitrary JSON Schema."""

    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        value = dict(items)
        if len(value) != len(items):
            msg = "Duplicate coding argument member."
            raise ValueError(msg)
        return value

    value = json.loads(serialized, object_pairs_hook=pairs)
    if not isinstance(value, dict) or not fields <= set(value) <= fields | optional:
        msg = "Coding arguments do not match the admitted operation."
        raise ValueError(msg)
    return value


class RepositoryCodingHost:
    """Operational source/edit/check host for the shared bounded coding process.

    Native continuation is transient, not a restart checkpoint. Required host
    callbacks supply effect authority, application/archive and restoration;
    readiness may reuse existing Localization without mandating one frame form.
    """

    native_feedback = True

    def __init__(  # noqa: PLR0913 -- explicit scope, effects and custody collaborators
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
    ) -> None:
        """Bind host authority and the existing Context/Tool/Resource substrates."""
        if corpus.discovery.repository_id != objective.scope.snapshot.repository_id:
            msg = "Coding corpus belongs to a foreign repository."
            raise ValueError(msg)
        self.objective, self.scope, self.corpus = objective, objective.scope, corpus
        if projection is not None and projection.trigger_bytes > objective.prompt_bytes:
            msg = "Projection watermarks exceed the host byte ceiling."
            raise ValueError(msg)
        self.projection = projection
        self.navigation = navigation
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
        self.messages = [PromptMessage("user", objective.text)]
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
                    _READ,
                    _EDIT,
                    _CHECK,
                    *((FIND, READ_UNIT) if self.navigation else ()),
                )
            ),
        )

    async def prepare(self, progress: CodingProgress) -> ModelRequest:  # noqa: C901 -- atomic projection and currentness guards
        """Authenticate source and atomically install a valid active projection."""
        self.progress = progress
        self.scope.check_current()
        request = self.build_request(tuple(self.messages))
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
                if self.compaction is not None:
                    protected |= self.compaction.protect(request.prompt.messages)
                outcome = project_request(
                    request,
                    policy=self.projection,
                    hard_bytes=self.objective.prompt_bytes,
                    snapshot=self.scope.snapshot,
                    sources=self._source_messages,
                    protected_indices=protected,
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
        if not response.tool_calls:
            return "stop"
        if all(
            c.name in {_READ.name, _CHECK.name}
            or (self.navigation and c.name in {FIND.name, READ_UNIT.name})
            for c in response.tool_calls
        ):
            return "acquire"
        if all(c.name == _EDIT.name for c in response.tool_calls):
            return "edit"
        msg = "Coding response contains an unadmitted or mixed operation."
        raise ValueError(msg)

    def _read(self, serialized: str) -> SourceReadRequest:
        values = _arguments(serialized, {"path", "start"}, optional=frozenset({"end"}))
        unit = next(
            (
                u
                for u in self.index.views[0].units
                if u.resource.address.value == values["path"]
            ),
            None,
        )
        if unit is None:
            msg = "Source path is outside the admitted corpus."
            raise ValueError(msg)
        return SourceReadRequest(
            self.objective.text,
            unit,
            cast("int", values["start"]),
            cast("int | None", values.get("end", unit.end)),
            self.objective.disclosure_bytes,
        )

    def _read_unit(self, serialized: str) -> SourceReadRequest:
        return unit_read_request(
            self.index,
            _arguments(serialized, {"unit_id", "snapshot_id"}),
            purpose=self.objective.text,
            maximum_bytes=self.objective.disclosure_bytes,
        )

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

    async def acquire(self, response: ModelResponse) -> bool:
        """Use shared composition and retain each bounded Tool result."""
        ready = False
        if (
            len(response.tool_calls)
            > self.progress.limits.tool_actions - self.progress.actions
        ):
            for call in response.tool_calls:
                self._feedback(call, {"status": "REFUSED", "reason": "action_budget"})
            return False
        for call in response.tool_calls:
            effect = self.progress.claim_action(call.provider_call_id)
            if self.navigation and call.name == FIND.name:
                selection = navigation_request(
                    _arguments(
                        call.arguments_json,
                        set(),
                        optional=frozenset({"path", "query", "mode", "offset"}),
                    ),
                )

                def selected_navigation(
                    _: str,
                    selected: SourceNavigationRequest = selection,
                ) -> SourceNavigationRequest:
                    return selected

                units = await execute_model_tool_call(
                    call,
                    invocation=_Invocation(FIND, selected_navigation),
                    tool=ScopedSourceNavigationTool(self.scope, self.index),
                    admit=self.authorize,
                    runner=ToolRunner(),
                )
                self._feedback(
                    call,
                    navigation_feedback(
                        units,
                        self.index,
                        offset=selection.offset,
                        maximum_bytes=self.objective.disclosure_bytes,
                    ),
                )
            elif call.name in {_READ.name, READ_UNIT.name}:
                tool: Tool[SourceReadRequest, ContextDisclosure | SourceReadRefusal] = (
                    ScopedSourceTool(
                        self.scope,
                        maximum_bytes=self.objective.disclosure_bytes,
                    )
                )
                disclosure = await execute_model_tool_call(
                    call,
                    invocation=_Invocation[SourceReadRequest](
                        READ_UNIT if call.name == READ_UNIT.name else _READ,
                        self._read_unit if call.name == READ_UNIT.name else self._read,
                    ),
                    tool=tool,
                    admit=self.authorize,
                    runner=ToolRunner(),
                )
                if isinstance(disclosure, SourceReadRefusal):
                    self._feedback(
                        call,
                        {
                            "status": "REFUSED",
                            "error": "SOURCE_RANGE_OUT_OF_BOUNDS",
                            "source_disclosure_entered": False,
                            "path": str(disclosure.request.unit.resource.address),
                            "snapshot": str(disclosure.request.unit.snapshot_id),
                            "version": str(
                                disclosure.request.unit.resource.content_identity,
                            ),
                            **source_read_bounds(disclosure.request),
                            "instruction": (
                                "Select a new valid interval; "
                                "this call disclosed no source."
                            ),
                        },
                    )
                    effect.acknowledged = True
                    continue
                option = cast(
                    "SourceRangeDisclosureOption",
                    disclosure.items[0].native_provenance,
                )
                self.source_results.append(disclosure)
                self.disclosures.append(option)
                self._feedback(
                    call,
                    source_feedback(option, disclosure.items[0].text),
                    sources=(option,),
                )
            else:
                _arguments(call.arguments_json, set())
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
                    _arguments(call.arguments_json, {"path", "old_text", "new_text"})
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
            invocation=_Invocation(_EDIT, selected),
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

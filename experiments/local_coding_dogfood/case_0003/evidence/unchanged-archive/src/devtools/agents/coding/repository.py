# Copyright (c) 2026
"""A neutral repository coding host, not an application-specific task schema."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, dataclass, replace
from typing import TYPE_CHECKING, Literal, cast

from devtools.agents.coding.custody import SourceCustody
from devtools.agents.coding.edits import CodingEditError, replace_exact_text
from devtools.agents.coding.models import (
    CodingCompletion,
    CodingEffect,
    CodingProgress,
    CodingResult,
)
from devtools.agents.model_tools import (
    execute_model_tool_call,
    normalize_tool_descriptor,
)
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.context.repository.corpus import realize_repository_text_corpus
from devtools.context.repository.resource import ContentIdentity
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
from devtools.tools.source import ScopedSourceTool, SourceScope

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Mapping

    from devtools.context.planning.materialization import ContextDisclosure
    from devtools.context.repository.corpus import RepositoryTextCorpusDefinition
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.core.paths import ResolvedPath

_SETTINGS = ModelSettings()
_READ = ToolDescriptor(
    "read_source",
    "Read an admitted exact current source region.",
    (
        '{"type":"object","properties":{"path":{"type":"string"},'
        '"start":{"type":"integer"},"end":{"type":"integer"}},'
        '"required":["path","start","end"],"additionalProperties":'
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
class EditLimits:
    """Host-selected region/source/transaction ceilings, without Qwen defaults."""

    region_bytes: int
    source_bytes: int
    aggregate_bytes: int
    operations: int

    def __post_init__(self) -> None:
        """Refuse unbounded admission before effects."""
        if (
            min(
                self.region_bytes,
                self.source_bytes,
                self.aggregate_bytes,
                self.operations,
            )
            <= 0
        ):
            msg = "Edit limits must be positive."
            raise ValueError(msg)


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


@dataclass(frozen=True, slots=True)
class SourceChange:
    """Admitted whole after-image with its original addressed source and span."""

    address: RepositoryResourceAddress
    before: str
    after: str
    start: int
    end: int


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


def _arguments(serialized: str, fields: set[str]) -> dict[str, object]:
    """Validate this host's small native argument object, not arbitrary JSON Schema."""

    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        value = dict(items)
        if len(value) != len(items):
            msg = "Duplicate coding argument member."
            raise ValueError(msg)
        return value

    value = json.loads(serialized, object_pairs_hook=pairs)
    if not isinstance(value, dict) or set(value) != fields:
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
    ) -> None:
        """Bind host authority and the existing Context/Tool/Resource substrates."""
        if corpus.discovery.repository_id != objective.scope.snapshot.repository_id:
            msg = "Coding corpus belongs to a foreign repository."
            raise ValueError(msg)
        self.objective, self.scope, self.corpus = objective, objective.scope, corpus
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

    async def prepare(self, progress: CodingProgress) -> ModelRequest:
        """Authenticate the active source and build a native complete-input Prompt."""
        self.progress = progress
        self.scope.check_current()
        request = ModelRequest(
            Prompt("", "messages", tuple(self.messages)),
            settings=self.settings,
            tools=tuple(normalize_tool_descriptor(d) for d in (_READ, _EDIT, _CHECK)),
        )
        if (
            len(json.dumps(asdict(request), ensure_ascii=False).encode())
            > self.objective.prompt_bytes
        ):
            msg = "Coding Prompt byte budget exceeded."
            raise ValueError(msg)
        self.requests.append(request)
        return request

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
        if all(c.name in {_READ.name, _CHECK.name} for c in response.tool_calls):
            return "acquire"
        if all(c.name == _EDIT.name for c in response.tool_calls):
            return "edit"
        msg = "Coding response contains an unadmitted or mixed operation."
        raise ValueError(msg)

    def _read(self, serialized: str) -> SourceRangeDisclosureOption:
        values = _arguments(serialized, {"path", "start", "end"})
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
        return SourceRangeDisclosureOption(
            self.objective.text,
            unit,
            cast("int", values["start"]),
            cast("int", values["end"]),
            self.objective.disclosure_bytes,
        )

    def _feedback(self, call: ModelToolCall, value: object) -> None:
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
            if call.name == _READ.name:
                disclosure: ContextDisclosure = await execute_model_tool_call(
                    call,
                    invocation=_Invocation(_READ, self._read),
                    tool=ScopedSourceTool(
                        self.scope,
                        maximum_bytes=self.objective.disclosure_bytes,
                    ),
                    admit=self.authorize,
                    runner=ToolRunner(),
                )
                option = cast(
                    "SourceRangeDisclosureOption",
                    disclosure.items[0].native_provenance,
                )
                self.disclosures.append(option)
                self._feedback(
                    call,
                    {
                        "text": disclosure.items[0].text,
                        "path": str(option.unit.resource.address),
                        "snapshot": str(option.snapshot_id),
                        "version": str(option.unit.resource.content_identity),
                        "span": option.span,
                        "partial": option.truncated,
                    },
                )
            else:
                _arguments(call.arguments_json, set())
                await self.authorize(call, self.objective.checks)
                passed = await self.check(())
                self.progress.candidate_validated = passed
                ready = passed and self.progress.proposals > 0
                self._feedback(call, {"passed": passed})
            effect.acknowledged = True
        return ready

    async def propose(self, response: ModelResponse) -> tuple[SourceChange, ...] | None:  # noqa: C901 -- admit every component before effects
        """Admit all exact, observed, current, nonoverlapping source anchors first."""
        self.pending_calls = response.tool_calls
        try:
            self.scope.check_current()
            if self.readiness is not None:
                self.readiness(self.scope.snapshot, tuple(self.disclosures))
            if len(response.tool_calls) > self.objective.edits.operations:
                msg = "Edit operation limit exceeded."
                raise CodingEditError(msg)
            changes: list[SourceChange] = []
            total = 0
            for call in response.tool_calls:
                values = _arguments(
                    call.arguments_json,
                    {"path", "old_text", "new_text"},
                )
                address = RepositoryResourceAddress(cast("str", values["path"]))
                if address not in self.objective.editable:
                    msg = "Edit path is outside the admitted editing surface."
                    raise CodingEditError(msg)
                before = self.scope.snapshot.resource_at(address).content
                after, start, end = replace_exact_text(
                    before,
                    values["old_text"],
                    values["new_text"],
                    region_bytes=self.objective.edits.region_bytes,
                    source_bytes=self.objective.edits.source_bytes,
                    allow_empty_new=True,
                )
                if not any(
                    o.unit.resource.address == address
                    and o.unit.resource.content_identity
                    == ContentIdentity.from_text(before)
                    and o.span[0] <= start
                    and end <= o.span[1]
                    for o in self.disclosures
                ):
                    msg = "Exact current edit source was not acquired."
                    raise CodingEditError(msg)
                if any(
                    c.address == address and start < c.end and c.start < end
                    for c in changes
                ):
                    msg = "Edit anchors overlap."
                    raise CodingEditError(msg)
                total += len(before[start:end].encode()) + len(
                    cast("str", values["new_text"]).encode(),
                )
                if total > self.objective.edits.aggregate_bytes:
                    msg = "Aggregate edit byte limit exceeded."
                    raise CodingEditError(msg)
                changes.append(SourceChange(address, before, after, start, end))
            # Combine admitted same-file anchors against the one original version.
            combined = []
            for address in dict.fromkeys(c.address for c in changes):
                original = self.scope.snapshot.resource_at(address).content
                after = original
                for c in sorted(
                    (c for c in changes if c.address == address),
                    key=lambda c: c.start,
                    reverse=True,
                ):
                    inserted = c.after[c.start : len(c.after) - (len(c.before) - c.end)]
                    after = after[: c.start] + inserted + after[c.end :]
                if len(after.encode()) > self.objective.edits.source_bytes:
                    msg = "Combined source byte limit exceeded."
                    raise CodingEditError(msg)
                combined.append(
                    SourceChange(address, original, after, 0, len(original)),
                )
            return tuple(combined)
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
            await ToolRunner().execute(
                ScopedSourceTool(
                    self.scope,
                    maximum_bytes=self.objective.disclosure_bytes,
                ),
                option,
            )
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
        for call in response.tool_calls:
            self._feedback(call, value)

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

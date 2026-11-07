# Copyright (c) 2026
"""One bounded parent/investigator learning composition; Runtime stays unchanged."""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import asdict, dataclass, field
from typing import TYPE_CHECKING

from devtools.agents.learning.policy import (
    PROFILE,
    best_index,
    decision,
    support_profile,
)
from devtools.agents.model_tools import (
    execute_model_tool_call,
    normalize_tool_descriptor,
)
from devtools.core.identity import Identity
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.learning.classification.linear import BinaryLinearTraining, _hash
from devtools.learning.integrations.local.classification.codec import document
from devtools.learning.integrations.local.inspection import (
    InspectedLearning,
    inspect_learning,
)
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.investigation.plans import (
    METHODS,
    BinaryProblem,
    LearningPlan,
    canonical,
)
from devtools.learning.investigation.proposals import LearningFeedback, LearningProposal
from devtools.learning.measurement.contracts import EvidenceReference, Measured
from devtools.models.interaction import (
    ModelInteraction,
    ModelRequest,
    ModelToolCall,
    Prompt,
    PromptMessage,
)
from devtools.resources.filesystem import TextFile, write
from devtools.tools import ToolRunner
from devtools.tools.learning.invocation import LearningInvocation, LearningTool

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.agents.learning.budgets import LearningBudget
    from devtools.tools.learning import ManagedLearningWorker


class LearningGrantIdentity(Identity):
    """One host-issued learning authority occurrence, separate from a native call."""


@dataclass(frozen=True, slots=True)
class AdmittedLearningTask:
    """Caller-owned data handles; confirmation values are never model disclosure."""

    identity: str
    family: str
    metric: str
    methods: tuple[str, ...]
    online_problem_json: str = field(repr=False)
    final_problem_json: str = field(repr=False)
    source_json: str = field(repr=False)
    source_authority: EvidenceReference

    def __post_init__(self) -> None:
        """Verify the exact admitted method menu and protected-role correspondence."""
        if (
            self.family not in METHODS
            or type(self.methods) is not tuple
            or (not self.methods)
            or (len(set(self.methods)) != len(self.methods))
            or any(m not in METHODS[self.family] for m in self.methods)
            or (not isinstance(self.source_authority, EvidenceReference))
        ):
            msg = "admitted finite learning task/source authority required"
            raise ValueError(msg)
        online = self.plan(self.methods[0], "online", "admission-online")
        final = self.plan(self.methods[0], "final", "admission-final")
        a, online_held = online.populations()
        b, final_held = final.populations()
        if document(asdict(a)) != document(asdict(b)):
            msg = "final evaluation cannot change the original fitting population"
            raise ValueError(msg)
        online_rows = (
            online_held.row_ids
            if isinstance(online_held, BinaryProblem)
            else online_held.inputs.row_ids
        )
        final_rows = (
            final_held.row_ids
            if isinstance(final_held, BinaryProblem)
            else final_held.inputs.row_ids
        )
        if set(online_rows) & set(final_rows):
            msg = "online and protected final memberships must be disjoint"
            raise ValueError(msg)

    @property
    def source_handle(self) -> str:
        """Expose a bounded admitted handle, without source paths or final targets."""
        return "learning-source:" + _hash(
            (self.source_json, asdict(self.source_authority)),
        )

    def plan(self, method: str, phase: str, invocation: str) -> LearningPlan:
        """Select caller-admitted data roles without proposal data or code."""
        source = json.loads(self.source_json)
        source["parent_source_admission"] = document(asdict(self.source_authority))
        return LearningPlan(
            self.identity,
            self.family,
            method,
            self.metric,
            phase,
            self.online_problem_json if phase == "online" else self.final_problem_json,
            canonical(source),
            invocation,
        )

    def semantics(self) -> tuple[str, str]:
        """Identify schema and units without exposing raw protected observations."""
        training, _held = self.plan(
            self.methods[0],
            "online",
            "semantics",
        ).populations()
        if isinstance(training, BinaryLinearTraining):
            return (
                _hash(
                    (
                        training.features.feature_names,
                        training.features.feature_value_kinds,
                        training.target_identity,
                    ),
                ),
                _hash(("integer-binary-0/1", training.target_identity)),
            )
        return (
            training.inputs.schema_identity,
            _hash((asdict(training.target), training.inputs.feature_units)),
        )


@dataclass(frozen=True, slots=True)
class InvestigationResult:
    """Inspect the declared scientific contract.

    Terminal choice, original inspected observations and an optional final
    artifact.
    """

    terminal: str
    observations: tuple[LearningFeedback, ...]
    artifact: InspectedLearning | None
    trace: tuple[dict[str, object], ...]
    seal_identity: str


async def investigate(  # noqa: PLR0913 -- explicit scientific provenance/custody; see release qualification review
    model: ModelInteraction,
    task: AdmittedLearningTask,
    worker: ManagedLearningWorker,
    budget: LearningBudget,
    root: Path,
    *,
    profile: str,
) -> InvestigationResult:
    """Compose real native model calls, independent host grants and inspected fits."""
    if profile != PROFILE:
        msg = "the caller must select the B-0096 engineering profile explicitly"
        raise ValueError(msg)
    await asyncio.to_thread(root.mkdir)
    async with asyncio.timeout(min(3600, budget.remaining_seconds())):
        return await _Investigation(model, task, worker, budget, root).run()


def _validate_call(call: ModelToolCall, used_calls: set[str], *, occupied: bool) -> str:
    """Require one fresh, identified native call before proposal admission."""
    if (
        occupied
        or call.provider_call_id is None
        or (
            not re.fullmatch("[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", call.provider_call_id)
        )
        or (call.provider_call_id in used_calls)
    ):
        msg = "foreign, duplicate or malformed native learning call"
        raise ValueError(msg)
    return call.provider_call_id


def _validate_proposal(
    task: AdmittedLearningTask,
    proposal: LearningProposal,
    state_identity: str,
    evidence: tuple[str, ...],
    expected: tuple[str, str | None],
) -> None:
    """Check exact source, semantics and acknowledged evidence."""
    schema, units = task.semantics()
    if (
        proposal.task_identity,
        proposal.source_handle,
        proposal.family,
        proposal.metric,
        proposal.schema_identity,
        proposal.unit_identity,
        proposal.role,
        proposal.state_identity,
        proposal.evidence,
    ) != (
        task.identity,
        task.source_handle,
        task.family,
        task.metric,
        schema,
        units,
        "online",
        state_identity,
        tuple(evidence),
    ) or (proposal.action, proposal.method) != expected:
        msg = (
            "learning proposal has stale/foreign/unsupported source, "
            "semantics, evidence or action"
        )
        raise ValueError(msg)


def _issue_grant(
    task: AdmittedLearningTask,
    proposal: LearningProposal,
    budget: LearningBudget,
    call_id: str,
) -> tuple[LearningPlan | None, ExecutionAuthorization | None]:
    """Reserve host budget and issue exact fitting authority."""
    plan = None
    grant = None
    if proposal.action == "CHECK_SUPPORT":
        budget.reserve(None)
    elif proposal.action == "EVALUATE":
        if proposal.method not in task.methods:
            msg = "unadmitted learning method"
            raise ValueError(msg)
        plan = task.plan(str(proposal.method), "online", call_id)
        budget.reserve(plan)
        grant = ExecutionAuthorization(
            plan.identity,
            (plan.method,),
            EvidenceReference(
                "learning_execution_grant-v1",
                str(LearningGrantIdentity.new()),
                plan.identity,
            ),
        )
    return (plan, grant)


def _check_support(
    task: AdmittedLearningTask,
    root: Path,
    state_identity: str,
) -> tuple[dict[str, object], LearningFeedback]:
    """Inspect admitted online support without fitting."""
    training, held = task.plan(task.methods[0], "online", "support").populations()
    a = (
        training.features
        if isinstance(training, BinaryLinearTraining)
        else training.inputs.features
    )
    b = held.features if isinstance(held, BinaryProblem) else held.inputs.features
    support = support_profile(a, b)
    identity = "learning-support:" + _hash(
        (task.source_handle, support, state_identity),
    )
    write(
        TextFile(
            resolve_path(root / "support.json"),
            canonical(
                {
                    "task": task.identity,
                    "source": task.source_handle,
                    "support": support,
                    "evidence_identity": identity,
                },
            ),
        ),
        overwrite=False,
    )
    return (
        support,
        LearningFeedback("CHECK_SUPPORT", None, task.metric, None, identity),
    )


async def _fit_feedback(
    plan: LearningPlan,
    grant: ExecutionAuthorization,
    worker: ManagedLearningWorker,
    budget: LearningBudget,
    root: Path,
) -> LearningFeedback:
    """Accept feedback only after independent scientific inspection."""
    reference = await worker.execute(
        plan,
        grant,
        root,
        operation_limit=Duration.seconds(min(300, budget.remaining_seconds())),
    )
    inspected = inspect_learning(reference, plan, grant)
    value = inspected.quality.value if isinstance(inspected.quality, Measured) else None
    return LearningFeedback(
        "EVALUATE",
        plan.method,
        plan.metric,
        value,
        reference.manifest_sha256,
        None
        if isinstance(inspected.quality, Measured)
        else inspected.quality.reason_code,
    )


class _Investigation:
    """Private state of this learning agent; no new runtime or persistence contract."""

    def __init__(
        self,
        model: ModelInteraction,
        task: AdmittedLearningTask,
        worker: ManagedLearningWorker,
        budget: LearningBudget,
        root: Path,
    ) -> None:
        """Own one bounded use of existing model, Tool and resource owners."""
        self.model = model
        self.task = task
        self.worker = worker
        self.budget = budget
        self.root = root
        self.observations: list[LearningFeedback] = []
        self.support: dict[str, object] | None = None
        self.evidence: list[str] = []
        self.trace: list[dict[str, object]] = []
        self.used_calls: set[str] = set()
        self.messages: list[PromptMessage] = [
            PromptMessage(
                "system",
                (
                    "Propose one closed learning action using the disclosed "
                    "finite engineering profile. Proposals do not authorize "
                    "execution. Confirmation labels and grants are private."
                ),
            ),
        ]
        self.schema, self.units = self.task.semantics()
        self.state_identity = ""
        self.expected: tuple[str, str | None] = ("CHECK_SUPPORT", None)
        self.pending: (
            tuple[LearningProposal, LearningPlan | None, ExecutionAuthorization | None]
            | None
        ) = None
        self.invocation = LearningInvocation()

    def validate(self, proposal: LearningProposal) -> None:
        """Require the exact trusted pending proposal before Tool execution."""
        if self.pending is None or self.pending[0] != proposal:
            msg = "learning Tool has no matching trusted pending admission"
            raise ValueError(msg)

    async def admit(self, call: ModelToolCall, proposal: LearningProposal) -> None:
        """Validate without effects, reserve host budget and issue an exact grant."""
        call_id = _validate_call(
            call,
            self.used_calls,
            occupied=self.pending is not None,
        )
        _validate_proposal(
            self.task,
            proposal,
            self.state_identity,
            tuple(self.evidence),
            self.expected,
        )
        plan, grant = _issue_grant(self.task, proposal, self.budget, call_id)
        self.used_calls.add(call_id)
        self.pending = (proposal, plan, grant)

    async def perform(self, proposal: LearningProposal) -> LearningFeedback:
        """Consume admission before an awaited effect, with no automatic retry."""
        self.validate(proposal)
        if self.pending is None:
            msg = "missing learning admission"
            raise ValueError(msg)
        _selected, plan, grant = self.pending
        self.pending = None  # Consume before awaiting; never retry uncertain effects.
        if proposal.action == "CHECK_SUPPORT":
            self.support, feedback = _check_support(
                self.task,
                self.root,
                self.state_identity,
            )
            identity = feedback.evidence_identity
            self.evidence.append(identity)
            return feedback
        if proposal.action in {"STOP", "ABSTAIN"}:
            return LearningFeedback(
                proposal.action,
                None,
                self.task.metric,
                None,
                "learning-terminal:" + self.state_identity,
            )
        if plan is None or grant is None:
            msg = "learning fit has no exact grant"
            raise ValueError(msg)
        feedback = await _fit_feedback(
            plan,
            grant,
            self.worker,
            self.budget,
            self.root / f"operation-{len(self.observations)}",
        )
        self.observations.append(feedback)
        self.evidence.append(feedback.evidence_identity)
        return feedback

    async def run(self) -> InvestigationResult:
        """Drive this finite native ModelInteraction and Tool composition."""
        tool = LearningTool(self.validate, self.perform)
        terminal = "ABSTAIN"
        for turn in range(len(self.task.methods) + 2):
            self.expected = decision(
                self.task.family,
                self.task.methods,
                self.observations,
                self.support,
                profile=PROFILE,
            )
            self.state_identity = _hash(
                (
                    self.task.identity,
                    self.task.source_handle,
                    self.support,
                    [asdict(o) for o in self.observations],
                    self.budget.consumed,
                ),
            )
            frame = {
                "task_identity": self.task.identity,
                "source_handle": self.task.source_handle,
                "family": self.task.family,
                "metric": self.task.metric,
                "schema_identity": self.schema,
                "unit_identity": self.units,
                "role": "online",
                "state_identity": self.state_identity,
                "evidence": list(self.evidence),
                "methods": list(self.task.methods),
                "profile": PROFILE,
                "support": self.support,
                "observations": [asdict(o) for o in self.observations],
                "consumed": dict(self.budget.consumed),
                "turn": turn,
            }
            self.messages.append(PromptMessage("user", canonical(frame)))
            selected_source = self.model.source
            response = await self.model.send(
                ModelRequest(
                    Prompt("", "messages", tuple(self.messages)),
                    tools=(normalize_tool_descriptor(self.invocation.descriptor),),
                ),
            )
            if response.source != selected_source or len(response.tool_calls) != 1:
                msg = "one source-correlated native learning call required"
                raise ValueError(msg)
            call = response.tool_calls[0]
            write(
                TextFile(
                    resolve_path(self.root / f"proposal-{turn}.json"),
                    canonical(
                        {
                            "model_source": str(response.source),
                            "call_id": call.provider_call_id,
                            "arguments_json": call.arguments_json,
                            "state_identity": self.state_identity,
                        },
                    ),
                ),
                overwrite=False,
            )
            feedback = await execute_model_tool_call(
                call,
                invocation=self.invocation,
                tool=tool,
                admit=self.admit,
                runner=ToolRunner(),
            )
            write(
                TextFile(
                    resolve_path(self.root / f"feedback-{turn}.json"),
                    canonical(document(asdict(feedback))),
                ),
                overwrite=False,
            )
            self.messages.extend(
                (
                    PromptMessage("assistant", response.content, tool_calls=(call,)),
                    PromptMessage(
                        "tool",
                        canonical(document(asdict(feedback))),
                        tool_call_id=call.provider_call_id,
                    ),
                ),
            )
            self.trace.append(
                {
                    "call_id": call.provider_call_id,
                    "model_source": str(response.source),
                    "arguments_json": call.arguments_json,
                    "state_identity": self.state_identity,
                    "action": feedback.action,
                    "method": feedback.method,
                    "evidence_identity": feedback.evidence_identity,
                    "value": feedback.value,
                },
            )
            if feedback.action in {"STOP", "ABSTAIN"}:
                terminal = feedback.action
                break
        else:
            msg = (
                "finite learning decision envelope exhausted without a terminal choice"
            )
            raise ValueError(msg)
        selected = (
            best_index(self.task.family, self.observations)
            if terminal == "STOP"
            else None
        )
        seal = {
            "task": self.task.identity,
            "terminal": terminal,
            "selected": selected,
            "observations": [asdict(o) for o in self.observations],
            "trace": self.trace,
        }
        seal_identity = _hash(seal)
        write(
            TextFile(resolve_path(self.root / "selection.json"), canonical(seal)),
            overwrite=False,
        )
        artifact = await self._final(selected, seal_identity)
        return InvestigationResult(
            terminal,
            tuple(self.observations),
            artifact,
            tuple(self.trace),
            seal_identity,
        )

    async def _final(
        self,
        selected: int | None,
        seal_identity: str,
    ) -> InspectedLearning | None:
        """Evaluate protected rows only after terminal selection has been sealed."""
        artifact = None
        if selected is not None:
            method = self.observations[selected].method
            if method is None:
                msg = "sealed terminal choice has no fitted method"
                raise ValueError(msg)
            final = self.task.plan(method, "final", "protected-final:" + seal_identity)
            self.budget.reserve(final)
            grant = ExecutionAuthorization(
                final.identity,
                (method,),
                EvidenceReference(
                    "learning_execution_grant-v1",
                    str(LearningGrantIdentity.new()),
                    final.identity,
                ),
            )
            reference = await self.worker.execute(
                final,
                grant,
                self.root / "protected-final",
                operation_limit=Duration.seconds(
                    min(300, self.budget.remaining_seconds()),
                ),
            )
            artifact = inspect_learning(reference, final, grant)
        return artifact

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
            or not self.methods
            or len(set(self.methods)) != len(self.methods)
            or any(m not in METHODS[self.family] for m in self.methods)
            or not isinstance(self.source_authority, EvidenceReference)
        ):
            msg = "admitted finite learning task/source authority required"
            raise ValueError(msg)
        online = self.plan(self.methods[0], "online", "admission-online")
        final = self.plan(self.methods[0], "final", "admission-final")
        a, online_held = online.populations()
        b, final_held = final.populations()
        if document(asdict(a)) != document(asdict(b)):
            msg = "final evaluation cannot change the original fitting population"
            raise ValueError(
                msg,
            )
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
            return _hash(
                (
                    training.features.feature_names,
                    training.features.feature_value_kinds,
                    training.target_identity,
                ),
            ), _hash(("integer-binary-0/1", training.target_identity))
        return training.inputs.schema_identity, _hash(
            (asdict(training.target), training.inputs.feature_units),
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


async def investigate(
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
        raise ValueError(
            msg,
        )
    root.mkdir()
    async with asyncio.timeout(min(3600, budget.remaining_seconds())):
        return await _investigate(model, task, worker, budget, root, profile)


async def _investigate(
    model: ModelInteraction,
    task: AdmittedLearningTask,
    worker: ManagedLearningWorker,
    budget: LearningBudget,
    root: Path,
    profile: str,
) -> InvestigationResult:
    observations: list[LearningFeedback] = []
    support: dict[str, object] | None = None
    evidence: list[str] = []
    trace: list[dict[str, object]] = []
    used_calls: set[str] = set()
    messages: list[PromptMessage] = [
        PromptMessage(
            "system",
            (
                "Propose one closed learning action using the disclosed finite en"
                "gineering profile. Proposals do not authorize execution. Confirm"
                "ation labels and grants are private."
            ),
        ),
    ]
    schema, units = task.semantics()
    state_identity = ""
    expected: tuple[str, str | None] = ("CHECK_SUPPORT", None)
    pending: (
        tuple[LearningProposal, LearningPlan | None, ExecutionAuthorization | None]
        | None
    ) = None
    invocation = LearningInvocation()

    def validate(proposal: LearningProposal) -> None:
        if pending is None or pending[0] != proposal:
            msg = "learning Tool has no matching trusted pending admission"
            raise ValueError(msg)

    async def admit(call: ModelToolCall, proposal: LearningProposal) -> None:
        nonlocal pending
        if (
            pending is not None
            or call.provider_call_id is None
            or not re.fullmatch(
                r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}",
                call.provider_call_id,
            )
            or call.provider_call_id in used_calls
        ):
            msg = "foreign, duplicate or malformed native learning call"
            raise ValueError(msg)
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
                "learning proposal has stale/foreign/unsupported source, semantic"
                "s, evidence or action"
            )
            raise ValueError(
                msg,
            )
        plan = None
        grant = None
        if proposal.action == "CHECK_SUPPORT":
            budget.reserve(None)
        elif proposal.action == "EVALUATE":
            if proposal.method not in task.methods:
                msg = "unadmitted learning method"
                raise ValueError(msg)
            plan = task.plan(str(proposal.method), "online", call.provider_call_id)
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
        used_calls.add(call.provider_call_id)
        pending = (proposal, plan, grant)

    async def perform(proposal: LearningProposal) -> LearningFeedback:
        nonlocal pending, support
        validate(proposal)
        if pending is None:
            msg = "missing learning admission"
            raise ValueError(msg)
        _selected, plan, grant = pending
        pending = None  # Consume before an awaited effect; failures never refund/retry.
        if proposal.action == "CHECK_SUPPORT":
            training, held = task.plan(
                task.methods[0],
                "online",
                "support",
            ).populations()
            a = (
                training.features
                if isinstance(training, BinaryLinearTraining)
                else training.inputs.features
            )
            b = (
                held.features
                if isinstance(held, BinaryProblem)
                else held.inputs.features
            )
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
            evidence.append(identity)
            return LearningFeedback("CHECK_SUPPORT", None, task.metric, None, identity)
        if proposal.action in {"STOP", "ABSTAIN"}:
            return LearningFeedback(
                proposal.action,
                None,
                task.metric,
                None,
                "learning-terminal:" + state_identity,
            )
        if plan is None or grant is None:
            msg = "learning fit has no exact grant"
            raise ValueError(msg)
        reference = await worker.execute(
            plan,
            grant,
            root / f"operation-{len(observations)}",
            timeout=Duration.seconds(min(300, budget.remaining_seconds())),
        )
        inspected = inspect_learning(reference, plan, grant)
        value = (
            inspected.quality.value if isinstance(inspected.quality, Measured) else None
        )
        feedback = LearningFeedback(
            "EVALUATE",
            plan.method,
            plan.metric,
            value,
            reference.manifest_sha256,
            None
            if isinstance(inspected.quality, Measured)
            else inspected.quality.reason_code,
        )
        observations.append(feedback)
        evidence.append(feedback.evidence_identity)
        return feedback

    tool = LearningTool(validate, perform)
    terminal = "ABSTAIN"
    for turn in range(len(task.methods) + 2):
        expected = decision(
            task.family,
            task.methods,
            observations,
            support,
            profile=profile,
        )
        state_identity = _hash(
            (
                task.identity,
                task.source_handle,
                support,
                [asdict(o) for o in observations],
                budget.consumed,
            ),
        )
        frame = {
            "task_identity": task.identity,
            "source_handle": task.source_handle,
            "family": task.family,
            "metric": task.metric,
            "schema_identity": schema,
            "unit_identity": units,
            "role": "online",
            "state_identity": state_identity,
            "evidence": list(evidence),
            "methods": list(task.methods),
            "profile": profile,
            "support": support,
            "observations": [asdict(o) for o in observations],
            "consumed": dict(budget.consumed),
            "turn": turn,
        }
        messages.append(PromptMessage("user", canonical(frame)))
        selected_source = model.source
        response = await model.send(
            ModelRequest(
                Prompt("", "messages", tuple(messages)),
                tools=(normalize_tool_descriptor(invocation.descriptor),),
            ),
        )
        if response.source != selected_source or len(response.tool_calls) != 1:
            msg = "one source-correlated native learning call required"
            raise ValueError(msg)
        call = response.tool_calls[0]
        write(
            TextFile(
                resolve_path(root / f"proposal-{turn}.json"),
                canonical(
                    {
                        "model_source": str(response.source),
                        "call_id": call.provider_call_id,
                        "arguments_json": call.arguments_json,
                        "state_identity": state_identity,
                    },
                ),
            ),
            overwrite=False,
        )
        feedback = await execute_model_tool_call(
            call,
            invocation=invocation,
            tool=tool,
            admit=admit,
            runner=ToolRunner(),
        )
        write(
            TextFile(
                resolve_path(root / f"feedback-{turn}.json"),
                canonical(document(asdict(feedback))),
            ),
            overwrite=False,
        )
        messages.extend(
            (
                PromptMessage("assistant", response.content, tool_calls=(call,)),
                PromptMessage(
                    "tool",
                    canonical(document(asdict(feedback))),
                    tool_call_id=call.provider_call_id,
                ),
            ),
        )
        trace.append(
            {
                "call_id": call.provider_call_id,
                "model_source": str(response.source),
                "arguments_json": call.arguments_json,
                "state_identity": state_identity,
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
        msg = "finite learning decision envelope exhausted without a terminal choice"
        raise ValueError(
            msg,
        )
    selected = best_index(task.family, observations) if terminal == "STOP" else None
    seal = {
        "task": task.identity,
        "terminal": terminal,
        "selected": selected,
        "observations": [asdict(o) for o in observations],
        "trace": trace,
    }
    seal_identity = _hash(seal)
    write(
        TextFile(resolve_path(root / "selection.json"), canonical(seal)),
        overwrite=False,
    )
    artifact = None
    if selected is not None:
        method = observations[selected].method
        if method is None:
            msg = "sealed terminal choice has no fitted method"
            raise ValueError(msg)
        final = task.plan(method, "final", "protected-final:" + seal_identity)
        budget.reserve(final)
        grant = ExecutionAuthorization(
            final.identity,
            (method,),
            EvidenceReference(
                "learning_execution_grant-v1",
                str(LearningGrantIdentity.new()),
                final.identity,
            ),
        )
        reference = await worker.execute(
            final,
            grant,
            root / "protected-final",
            timeout=Duration.seconds(min(300, budget.remaining_seconds())),
        )
        artifact = inspect_learning(reference, final, grant)
    return InvestigationResult(
        terminal,
        tuple(observations),
        artifact,
        tuple(trace),
        seal_identity,
    )

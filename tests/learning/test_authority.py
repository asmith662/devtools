# Copyright (c) 2026
"""Native correlation, exact caller grants and finite pre-effect refusals."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.learning.budgets import LIMITS, LearningBudget
from devtools.agents.learning.policy import PROFILE
from devtools.agents.learning.process import investigate
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.investigation.plans import canonical
from devtools.learning.investigation.proposals import LearningProposal
from devtools.learning.measurement.contracts import EvidenceReference
from devtools.models.interaction import InteractionSource, ModelRequest, ModelResponse
from devtools.tools.learning import ManagedLearningWorker
from tests.learning.fixtures import ScriptedInvestigator, authored_task

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class FaultyInteraction(ScriptedInvestigator):
    """Emit deliberately inconsistent native envelopes around valid proposal JSON."""

    fault: str = "missing-id"

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Keep the real materializer/admission/Tool boundary in the fault path."""
        response = await super().send(request)
        call = response.tool_calls[0]
        if self.fault == "foreign-source":
            return replace(response, source=InteractionSource("other-model"))
        if self.fault == "multiple-calls":
            return replace(response, tool_calls=(call, call))
        call = replace(
            call,
            provider_call_id=None if self.fault == "missing-id" else "duplicate-id",
        )
        return replace(response, tool_calls=(call,))


@pytest.mark.parametrize(
    "fault",
    ["missing-id", "foreign-source", "multiple-calls", "duplicate-id"],
)
def test_bad_native_correlation_never_fits(tmp_path: Path, fault: str) -> None:
    """A valid JSON proposal cannot repair a foreign or repeated native envelope."""
    worker = ManagedLearningWorker.current()
    account = LearningBudget()
    with pytest.raises(ValueError, match="native|source|call"):
        asyncio.run(
            investigate(
                FaultyInteraction(fault=fault),
                authored_task("classification"),
                worker,
                account,
                tmp_path / "native-refusal",
                profile=PROFILE,
            ),
        )
    assert not worker.receipts
    assert account.consumed["invocations"] == 0


def test_exhausted_account_refuses_before_issuing_fit(tmp_path: Path) -> None:
    """A support observation does not replenish the caller's numerical account."""
    account = LearningBudget(limits={**LIMITS, "invocations": 0})
    worker = ManagedLearningWorker.current()
    with pytest.raises(ValueError, match="budget exhausted"):
        asyncio.run(
            investigate(
                ScriptedInvestigator(),
                authored_task("classification"),
                worker,
                account,
                tmp_path / "no-fit-slot",
                profile=PROFILE,
            ),
        )
    assert account.consumed["actions"] == 1
    assert account.consumed["invocations"] == 0
    assert not worker.receipts


@pytest.mark.parametrize("bad_field", ["plan", "method", "relation", "digest"])
def test_exact_grant_refuses_without_creating_operation(
    tmp_path: Path,
    bad_field: str,
) -> None:
    """All exact authority coordinates bind independently, before packet writes."""
    plan = authored_task("classification").plan("knn7", "online", "exact-grant")
    grant = ExecutionAuthorization(
        "different-plan" if bad_field == "plan" else plan.identity,
        ("square-logistic",) if bad_field == "method" else (plan.method,),
        EvidenceReference(
            "model-proposal"
            if bad_field == "relation"
            else "learning_execution_grant-v1",
            "trusted-caller-occurrence",
            "0" * 64 if bad_field == "digest" else plan.identity,
        ),
    )
    worker = ManagedLearningWorker.current()
    root = tmp_path / "unauthorized-operation"
    with pytest.raises(ValueError, match="exact caller-issued"):
        asyncio.run(worker.execute(plan, grant, root))
    assert not root.exists()
    assert not worker.receipts


@pytest.mark.parametrize(
    "bad",
    [
        '{"task_identity":"a","task_identity":"b"}',
        "x" * 16385,
        canonical({"arbitrary_code": "execute"}),
    ],
)
def test_closed_proposal_rejects_ambiguous_or_unbounded_json(bad: str) -> None:
    """Duplicate meanings, excess disclosure and executable extensions refuse."""
    with pytest.raises(ValueError, match="duplicate|large|unsupported"):
        LearningProposal.materialize(bad)


def test_untrusted_rationale_is_never_new_evidence(tmp_path: Path) -> None:
    """A hypothesis does not acquire a source/evidence identity merely by wording."""
    worker = ManagedLearningWorker.current()
    account = LearningBudget()
    model = ScriptedInvestigator({"evidence": ["model rationale proves improvement"]})
    with pytest.raises(ValueError, match="stale|foreign"):
        asyncio.run(
            investigate(
                model,
                authored_task("classification"),
                worker,
                account,
                tmp_path / "rationale",
                profile=PROFILE,
            ),
        )
    assert not worker.receipts
    assert account.consumed["actions"] == 0
    assert json.loads(model.requests[0].prompt.messages[-1].content)["evidence"] == []

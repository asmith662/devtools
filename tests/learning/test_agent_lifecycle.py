# Copyright (c) 2026
"""Admitted task and bounded-agent failure semantics without scientific effects."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from devtools.agents.learning import process
from devtools.agents.learning.budgets import LearningBudget
from devtools.agents.learning.process import _Investigation, _issue_grant, investigate
from devtools.learning.investigation.plans import canonical
from devtools.learning.investigation.proposals import LearningFeedback, LearningProposal
from devtools.tools.learning import ManagedLearningWorker
from tests.learning.fixtures import ScriptedInvestigator, authored_task

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.agents.learning.process import AdmittedLearningTask


def _proposal(task: AdmittedLearningTask, action: str = "EVALUATE") -> LearningProposal:
    schema, units = task.semantics()
    return LearningProposal(
        task.identity,
        task.source_handle,
        task.family,
        task.metric,
        schema,
        units,
        "online",
        "state",
        (),
        action,
        "knn7",
        "control",
    )


@pytest.mark.parametrize("fault", ["menu", "training", "protected"])
def test_admitted_task_cannot_change_training_or_expose_online_rows_as_final(
    fault: str,
) -> None:
    """Task constructors reject role overlap and changed original training values."""
    task = authored_task("classification")
    if fault == "menu":
        changes: dict[str, Any] = {"methods": ("unadmitted",)}
    elif fault == "protected":
        changes = {"final_problem_json": task.online_problem_json}
    else:
        data = json.loads(task.final_problem_json)
        data["training"]["targets"][0] = 1
        changes = {"final_problem_json": canonical(data)}
    with pytest.raises(ValueError, match=r"admitted|fitting population|disjoint"):
        replace(task, **changes)


def test_profile_and_unadmitted_method_refuse_without_worker_entry(
    tmp_path: Path,
) -> None:
    """Refuse unsupported profiles and methods before execution authority."""
    task = authored_task("classification")
    worker = ManagedLearningWorker.current()
    budget = LearningBudget()
    with pytest.raises(ValueError, match="profile explicitly"):
        asyncio.run(
            investigate(
                ScriptedInvestigator(),
                task,
                worker,
                budget,
                tmp_path / "operation",
                profile="universal",
            ),
        )
    with pytest.raises(ValueError, match="unadmitted learning method"):
        _issue_grant(task, replace(_proposal(task), method="histogram"), budget, "call")
    assert worker.receipts == []
    assert not tuple(tmp_path.iterdir())


@pytest.mark.parametrize("fault", ["pending", "grant", "validator"])
def test_missing_tool_admission_or_grant_has_zero_execution_effects(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """A simulated faulty validator cannot create an exact pending fitting grant."""
    task = authored_task("classification")
    worker = ManagedLearningWorker.current()
    agent = _Investigation(
        ScriptedInvestigator(),
        task,
        worker,
        LearningBudget(),
        tmp_path,
    )
    proposal = _proposal(task)
    if fault == "grant":
        agent.pending = (proposal, None, None)
    elif fault == "validator":
        monkeypatch.setattr(agent, "validate", lambda _: None)
    with pytest.raises(
        ValueError,
        match=r"pending admission|missing learning|exact grant",
    ):
        asyncio.run(agent.perform(proposal))
    assert worker.receipts == []


@pytest.mark.parametrize("fault", ["no-progress", "unfitted-terminal"])
def test_faulty_tool_component_cannot_exhaust_forever_or_select_an_unfitted_method(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """Exercise native scripted calls against explicit result-component faults."""
    task = authored_task("classification")
    worker = ManagedLearningWorker.current()
    agent = _Investigation(
        ScriptedInvestigator(),
        task,
        worker,
        LearningBudget(),
        tmp_path,
    )

    async def reported(_: LearningProposal) -> LearningFeedback:
        agent.pending = None
        return LearningFeedback(
            "STOP" if fault == "unfitted-terminal" else "CHECK_SUPPORT",
            None,
            task.metric,
            None,
            "control",
        )

    monkeypatch.setattr(agent, "perform", reported)
    if fault == "unfitted-terminal":
        agent.observations.append(
            LearningFeedback("EVALUATE", None, task.metric, 1.0, "control"),
        )
        monkeypatch.setattr(process, "best_index", lambda *_: 0)
    with pytest.raises(ValueError, match=r"envelope exhausted|no fitted method"):
        asyncio.run(agent.run())
    assert worker.receipts == []

# Copyright (c) 2026
"""Real scripted native ModelInteraction/Tool, numerical inspection and parent use."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.learning.budgets import LearningBudget
from devtools.agents.learning.policy import PROFILE
from devtools.agents.learning.process import investigate
from devtools.learning.investigation.plans import BinaryProblem
from devtools.learning.regression.state import RegressionPredictions
from devtools.tools.learning import ManagedLearningWorker
from tests.learning.fixtures import (
    ScriptedInvestigator,
    authored_task,
    authored_tie_task,
)

if TYPE_CHECKING:
    from pathlib import Path

_PARENT_QUERY_ROWS = 2


@pytest.mark.parametrize("family", ["classification", "regression"])
def test_native_investigator_and_actual_parent_prediction(
    tmp_path: Path,
    family: str,
) -> None:
    """Run real granted fits, independent publications and protected parent use."""
    task = authored_task(family)
    worker = ManagedLearningWorker.current()
    model = ScriptedInvestigator()
    result = asyncio.run(
        investigate(
            model,
            task,
            worker,
            LearningBudget(),
            tmp_path / "investigation",
            profile=PROFILE,
        ),
    )
    assert result.terminal == "STOP"
    assert result.artifact is not None
    _training, held = result.artifact.plan.populations()
    features = held.features if family == "classification" else held.inputs  # type: ignore[union-attr]
    predicted = result.artifact.predict(features)
    assert (
        len(
            predicted.values
            if isinstance(predicted, RegressionPredictions)
            else predicted,
        )
        == _PARENT_QUERY_ROWS
    )
    publication = result.artifact.reference
    saved = json.loads(
        (
            publication.root.value
            / "publication/generations"
            / publication.generation_id
            / "result.json"
        ).read_bytes(),
    )
    assert (
        list(predicted.values) == saved["predictions"]["values"]
        if isinstance(predicted, RegressionPredictions)
        else list(predicted) == saved["predictions"]
    )
    assert all(
        request.tools[0].name == "learning_investigate" for request in model.requests
    )
    assert result.trace[0]["action"] == "CHECK_SUPPORT"
    assert result.trace[-1]["action"] == "STOP"
    assert result.artifact.plan.phase == "final"
    assert len(worker.receipts) == len(result.observations) + 1


@pytest.mark.parametrize(
    "changed",
    [
        {"source_handle": "foreign"},
        {"family": "ranking"},
        {"metric": "wrong"},
        {"schema_identity": "wrong"},
        {"unit_identity": "wrong"},
        {"role": "final"},
        {"state_identity": "stale"},
        {"evidence": ["foreign"]},
        {"method": "arbitrary-python"},
        {"code": "print('escape')"},
    ],
)
def test_untrusted_request_refuses_before_fitting(
    tmp_path: Path,
    changed: dict[str, object],
) -> None:
    """Bad proposals neither reserve numerical work nor launch a process."""
    worker = ManagedLearningWorker.current()
    budget = LearningBudget()
    with pytest.raises(ValueError):
        asyncio.run(
            investigate(
                ScriptedInvestigator(changed),
                authored_task("classification"),
                worker,
                budget,
                tmp_path / "refused",
                profile=PROFILE,
            ),
        )
    assert worker.receipts == []
    assert budget.consumed["invocations"] == 0


@pytest.mark.parametrize(("nonvalue", "unsupported"), [(True, False), (False, True)])
def test_nonvalue_and_unsupported_abstain(
    tmp_path: Path,
    nonvalue: bool,
    unsupported: bool,
) -> None:
    """A nonvalue or new constant-coordinate variation cannot authorize continuation."""
    task = authored_task("classification", nonvalue=nonvalue, unsupported=unsupported)
    result = asyncio.run(
        investigate(
            ScriptedInvestigator(),
            task,
            ManagedLearningWorker.current(),
            LearningBudget(),
            tmp_path / "abstain",
            profile=PROFILE,
        ),
    )
    assert result.terminal == "ABSTAIN"
    assert result.artifact is None
    assert len(result.observations) == 1


def test_explicit_margin_menu(tmp_path: Path) -> None:
    """Qualify the admitted margin backend even when the longer profile stops early."""
    task = replace(authored_task("classification"), methods=("square-margin",))
    result = asyncio.run(
        investigate(
            ScriptedInvestigator(),
            task,
            ManagedLearningWorker.current(),
            LearningBudget(),
            tmp_path / "margin",
            profile=PROFILE,
        ),
    )
    assert result.terminal == "STOP"
    assert result.artifact is not None
    assert result.artifact.plan.method == "square-margin"
    _training, held = result.artifact.plan.populations()
    assert isinstance(held, BinaryProblem)
    assert result.artifact.predict(held.features) == (0, 1)


def test_native_knn_boundary_retains_deterministic_truth(tmp_path: Path) -> None:
    """Inspect the declared scientific contract.

    Keep the original row-order tie truth and refuse a stronger native-parity
    claim.
    """
    result = asyncio.run(
        investigate(
            ScriptedInvestigator(),
            authored_tie_task(),
            ManagedLearningWorker.current(),
            LearningBudget(),
            tmp_path / "ties",
            profile=PROFILE,
        ),
    )
    assert result.artifact is not None
    artifact = result.artifact
    _training, held = artifact.plan.populations()
    from devtools.learning.regression.contracts import RegressionPopulation

    assert isinstance(held, RegressionPopulation)
    predicted = artifact.predict(held.inputs)
    assert isinstance(predicted, RegressionPredictions)
    assert predicted.values == (7.0,)
    reference = artifact.reference
    saved = json.loads(
        (
            reference.root.value
            / "publication/generations"
            / reference.generation_id
            / "result.json"
        ).read_bytes(),
    )
    assert saved["native_correspondence"]["unqualified_row_ids"] == ["final-tie"]
    assert saved["native_correspondence"]["qualified_row_ids"] == []

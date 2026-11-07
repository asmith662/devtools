# Copyright (c) 2026
"""Genuine authored binary fits followed by explicit retained-state fault injection."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

from devtools.learning.classification.linear import (
    BinaryLinearTraining,
    FittedBinaryLinearClassifier,
)
from devtools.learning.classification.margin import FittedMarginClassifier
from devtools.learning.integrations.local.inspection import inspect_learning
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.measurement.contracts import EvidenceReference
from devtools.tools.learning import ManagedLearningWorker
from tests.learning.fixtures import authored_task

if TYPE_CHECKING:
    from collections.abc import Callable

type State = FittedBinaryLinearClassifier | FittedMarginClassifier
type Witness = tuple[State, BinaryLinearTraining]


@pytest.fixture(scope="module")
def fitted(tmp_path_factory: pytest.TempPathFactory) -> Callable[[str], Witness]:
    """Fit each selected linear family once when an active test requests it."""
    root = tmp_path_factory.mktemp("binary-state")
    cache: dict[str, Witness] = {}

    def get(method: str) -> Witness:
        if method not in cache:
            plan = authored_task("classification").plan(
                method,
                "online",
                "binary-state-control",
            )
            grant = ExecutionAuthorization(
                plan.identity,
                (method,),
                EvidenceReference(
                    "learning_execution_grant-v1",
                    "state-control",
                    plan.identity,
                ),
            )
            publication = asyncio.run(
                ManagedLearningWorker.current().execute(plan, grant, root / method),
            )
            inspected = inspect_learning(publication, plan, grant)
            assert isinstance(
                inspected.state,
                (FittedBinaryLinearClassifier, FittedMarginClassifier),
            )
            assert inspected.binary_training is not None
            cache[method] = inspected.state, inspected.binary_training
        return cache[method]

    return get

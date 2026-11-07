# Copyright (c) 2026
"""Genuine authored fitted-state witnesses, lazily acquired within active tests."""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING

import pytest

from devtools.learning.integrations.local.inspection import inspect_learning
from devtools.learning.integrations.local.regression.codec import state as decode_state
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.measurement.contracts import EvidenceReference
from devtools.learning.regression.contracts import RegressionPopulation
from devtools.tools.learning import ManagedLearningWorker
from tests.learning.fixtures import authored_task

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.learning.regression.state import FittedRegression


@pytest.fixture(scope="module")
def fitted_states(
    tmp_path_factory: pytest.TempPathFactory,
) -> Callable[[str], tuple[FittedRegression, RegressionPopulation]]:
    """Lazily fit each authored method once, under the active per-test collector."""
    root = tmp_path_factory.mktemp("states")
    cache: dict[str, tuple[FittedRegression, RegressionPopulation]] = {}

    def get(method: str) -> tuple[FittedRegression, RegressionPopulation]:
        if method not in cache:
            plan = authored_task("regression").plan(
                method,
                "online",
                "state-control-" + method,
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
            reference = asyncio.run(
                ManagedLearningWorker.current().execute(plan, grant, root / method),
            )
            inspected = inspect_learning(reference, plan, grant)
            saved = json.loads(
                next(
                    (reference.root.value / "publication/generations").glob(
                        "*/result.json",
                    ),
                ).read_bytes(),
            )
            state = decode_state(saved["state"])
            assert inspected.state == state
            training, _ = plan.populations()
            assert isinstance(training, RegressionPopulation)
            cache[method] = state, training
        return cache[method]

    return get

# Copyright (c) 2026
# ruff: noqa: S101, D103 -- bounded deterministic spend/entry fixtures
"""All partition calls are reserved before any journal or model may enter."""

import pytest

from experiments.orchestration.semantic_limits import InvocationBudget, InvocationLimits
from experiments.orchestration.workers.semantic import preflight_input


@pytest.mark.parametrize("scope", ["stage", "case", "cohort"])
def test_excess_reservation_is_atomic_and_cannot_enter(scope: str) -> None:
    limits = InvocationLimits(
        {"A1": 1 if scope == "stage" else 5},
        {"case": 1 if scope == "case" else 5},
        1 if scope == "cohort" else 5,
    )
    budget = InvocationBudget(limits)
    with pytest.raises(ValueError, match="SEMANTIC_INVOCATION_BUDGET"):
        budget.reserve("A1", "case", "partition", ("one", "two"))
    assert budget.reserved == {}
    with pytest.raises(ValueError, match="not reserved"):
        budget.enter("one", lambda: None, lambda: pytest.fail("must not enter"))


def test_exact_preentry_and_dead_operation_no_retry() -> None:
    budget = InvocationBudget(InvocationLimits({"A2": 2}, {"case": 2}, 2))
    budget.reserve("A2", "case", "frozen-partition", ("one", "two"))
    order = []
    budget.enter(
        "one",
        lambda: order.append("exact input check"),
        lambda: order.append("ENTERED"),
    )
    assert order == ["exact input check", "ENTERED"]
    with pytest.raises(ValueError, match="already entered"):
        budget.enter("one", lambda: None, lambda: None)
    with pytest.raises(ValueError, match="Duplicate"):
        budget.reserve("A2", "case", "other", ("two",))
    with pytest.raises(ValueError, match="too large"):
        budget.enter(
            "two",
            lambda: (_ for _ in ()).throw(ValueError("too large")),
            lambda: pytest.fail("must not enter"),
        )
    assert "two" not in budget.entered


def test_actual_runtime_input_rejection_precedes_scientific_entry() -> None:
    budget = InvocationBudget(InvocationLimits({"A2": 1}, {"case": 1}, 1))
    budget.reserve("A2", "case", "partition", ("one",))
    contract = {"type": "string", "enum": ["synthetic"]}
    with pytest.raises(ValueError, match="WORKLOAD_CAPACITY_LIMIT"):
        budget.enter(
            "one",
            lambda: preflight_input({}, b"x" * 700001, contract, engineering=True),
            lambda: pytest.fail("no ENTERED on exact budget failure"),
        )
    assert not budget.entered


def test_resume_retains_spend_and_dead_identities() -> None:
    limits = InvocationLimits({"A2": 2}, {"case": 2}, 2)
    budget = InvocationBudget(limits)
    budget.reserve("A2", "case", "partition", ("one", "two"))
    budget.enter("one", lambda: None, lambda: None)
    resumed = InvocationBudget.restore(limits, budget.snapshot())
    assert resumed.snapshot() == budget.snapshot()
    with pytest.raises(ValueError, match="already entered"):
        resumed.enter("one", lambda: None, lambda: pytest.fail("no retry"))
    with pytest.raises(ValueError, match="SEMANTIC_INVOCATION_BUDGET"):
        resumed.reserve("A2", "case", "new-partition", ("three",))
    with pytest.raises(ValueError, match="resume binding"):
        InvocationBudget.restore(
            InvocationLimits({"A2": 3}, {"case": 3}, 3),
            budget.snapshot(),
        )

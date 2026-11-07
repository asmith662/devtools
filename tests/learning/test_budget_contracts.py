# Copyright (c) 2026
"""Finite host-account arithmetic, with no numerical execution effects."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from devtools.agents.learning import budgets
from devtools.agents.learning.budgets import LIMITS, LearningBudget
from devtools.core.time import Duration
from tests.learning.fixtures import authored_task


@pytest.mark.parametrize(
    "limits",
    [
        {},
        {**LIMITS, "actions": -1},
        {**LIMITS, "native_fits": 10},
        {**LIMITS, "actions": True},
    ],
)
def test_invalid_or_expanded_account_cannot_be_admitted(limits: dict[str, int]) -> None:
    """The root profile is finite and cannot silently acquire larger native limits."""
    with pytest.raises(ValueError, match="fresh bounded"):
        LearningBudget(limits=limits)
    with pytest.raises(ValueError, match="fresh bounded"):
        LearningBudget(consumed={**dict.fromkeys(LIMITS, 0), "actions": 1})


@pytest.mark.parametrize("menus", [((),), (("mean", "mean"),)])
def test_empty_or_duplicate_menus_refuse(menus: tuple[tuple[str, ...], ...]) -> None:
    """A finite envelope enumerates unique eligible candidates once."""
    with pytest.raises(ValueError, match="finite unique"):
        LearningBudget().admit_envelope(menus)


def test_exact_first_slice_envelope_and_refused_reservation_are_atomic() -> None:
    """Include final scoring in the worst case and never refund a consumed slot."""
    account = LearningBudget()
    maximum = account.admit_envelope(
        (("knn7", "square-logistic", "square-margin"), ("mean", "ridge", "knn-v2")),
    )
    assert maximum == {
        "native_fits": 7,
        "states": 8,
        "preparations": 7,
        "squares": 3,
        "actions": 8,
        "invocations": 8,
    }
    limited = LearningBudget(limits={**LIMITS, "native_fits": 0})
    before = dict(limited.consumed)
    plan = authored_task("regression").plan("ridge", "online", "budget-control")
    with pytest.raises(ValueError, match="budget exhausted"):
        limited.reserve(plan)
    assert limited.consumed == before
    with pytest.raises(ValueError, match="reviewed count envelope"):
        limited.admit_envelope((("ridge",),))


@pytest.mark.parametrize("method", ["mean", "ridge", "knn-v2", "square-logistic"])
def test_reserved_operations_have_exact_family_cost_coordinates(method: str) -> None:
    """Reserve preparations and native fits independently of their outcomes."""
    family = "classification" if method.startswith("square-") else "regression"
    task = authored_task(family)
    account = LearningBudget()
    plan = task.plan(method, "online", "reserve-online")
    account.reserve(plan)
    assert account.consumed == {
        "native_fits": int(method != "mean"),
        "preparations": int(method != "mean"),
        "states": 1,
        "squares": int(method.startswith("square-")),
        "actions": 1,
        "invocations": 1,
    }
    account.reserve(task.plan(method, "final", "reserve-final"))
    assert account.consumed["actions"] == 1
    account.reserve(None)
    expected_actions = 2
    assert account.consumed["actions"] == expected_actions


def test_expired_account_cannot_reserve_more_effects() -> None:
    """A simulated clock qualifies deadline refusal without elapsed real time."""
    account = LearningBudget()
    vars(account)["_clock"] = SimpleNamespace(elapsed=Duration.seconds(7201))
    assert account.remaining_seconds() == 0
    with pytest.raises(ValueError, match="budget exhausted"):
        account.reserve(None)
    assert account.consumed == dict.fromkeys(LIMITS, 0)


def test_invalid_future_storage_profile_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate a larger count profile only to exercise independent storage refusal.

    No fit, grant or study runs under these invalid limits. Reviewed production
    bounds remain unchanged and are restored automatically after this control.
    """
    invalid = {**LIMITS, "invocations": 9, "actions": 9}
    monkeypatch.setattr(budgets, "LIMITS", invalid)
    account = LearningBudget(limits=invalid)
    menu = ("mean", "a", "b", "c", "d", "e", "f", "g")
    with pytest.raises(ValueError, match="storage envelope"):
        account.admit_envelope((menu,))

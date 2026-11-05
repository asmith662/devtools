# Copyright (c) 2026
# ruff: noqa: F811, COM812 -- exact bounded deterministic fixtures
"""Revocable local work and delegation never widen their parent's permissions."""

from __future__ import annotations

import asyncio
import copy
from typing import TYPE_CHECKING

import pytest

from devtools.core.time import Duration, Timestamp
from scripts.backlog.routine.policy import EXCEPTIONS
from tests.scripts.backlog.routine.test_authority import assessment, provider
from tests.scripts.backlog.routine.test_local import (
    Model,
    activate,
    measured,
    qualified,
    request,
    scope,
)
from tests.scripts.backlog.test_native import repository  # noqa: F401

if TYPE_CHECKING:
    from scripts.backlog.work import WorkCycle


@pytest.mark.parametrize("exception", sorted(EXCEPTIONS))
def test_exception_precedes_resource_disclosure(
    repository: tuple[WorkCycle, str], monkeypatch: pytest.MonkeyPatch, exception: str
) -> None:
    """Every exceptional operation remains outside automatic consent."""
    cycle, _ = repository

    async def run() -> None:
        identity = await activate(cycle)
        selected = scope(cycle)
        assessment_value = assessment()
        assessment_value[exception] = True
        monkeypatch.setattr(
            "scripts.backlog.routine.local.SourceScope.observe",
            lambda **_: pytest.fail("Source acquired before exceptional decision"),
        )
        with pytest.raises(PermissionError, match="escalation"):
            await cycle.routine.local.authorize(
                identity, selected, assessment=assessment_value, provider=provider()
            )

    asyncio.run(run())


@pytest.mark.parametrize(
    "limit", ["input_tokens", "total_output_tokens", "capture_bytes", "wall_seconds"]
)
def test_each_runtime_limit_stops_before_model(
    repository: tuple[WorkCycle, str], monkeypatch: pytest.MonkeyPatch, limit: str
) -> None:
    """Measured Context, reserved output, capture and wall bounds fail closed."""
    cycle, _ = repository

    async def run() -> None:
        identity = await activate(cycle)
        selected = scope(cycle)
        selected["budgets"][limit] = {
            "input_tokens": 99,
            "total_output_tokens": 511,
            "capture_bytes": 1,
            "wall_seconds": 1,
        }[limit]
        grant = await cycle.routine.local.authorize(
            identity, selected, assessment=assessment(), provider=provider()
        )
        model = Model()
        now = Timestamp.now()
        if limit == "wall_seconds":
            monkeypatch.setattr(
                Timestamp, "now", classmethod(lambda _: now + Duration.seconds(2))
            )
        with pytest.raises(PermissionError):
            await cycle.routine.local.interact(
                grant["reference"],
                request(),
                interaction=model,
                qualify=qualified,
                measure=measured,
            )
        assert not model.requests
        assert not cycle.routine.local.records(grant["reference"])

    asyncio.run(run())


def test_new_actor_and_role_use_same_model_neutral_contract(
    repository: tuple[WorkCycle, str],
) -> None:
    """An authorized planner adapter can consume a bounded child grant."""
    cycle, _ = repository

    async def run() -> None:
        identity = await activate(cycle)
        selected = scope(cycle)
        parent = await cycle.routine.local.authorize(
            identity, selected, assessment=assessment(), provider=provider()
        )
        child = copy.deepcopy(selected)
        child.update(actor="fixture-planner", role="planner", roles=[])
        child["budgets"].update(
            model_calls=1,
            total_output_tokens=512,
            reads=0,
            checks=0,
            capture_bytes=524288,
            delegations=0,
        )
        grant = await cycle.routine.local.authorize(
            identity,
            child,
            assessment=assessment(),
            provider=provider(),
            parent=parent["reference"],
        )
        model = Model()
        model.source = type(model.source)("fixture-planner")
        response = await cycle.routine.local.interact(
            grant["reference"],
            request(),
            interaction=model,
            qualify=qualified,
            measure=measured,
        )
        assert str(response.source) == "fixture-planner"
        assert len(model.requests) == 1

    asyncio.run(run())


def test_unknown_fixed_check_and_completion_tampering_refused(
    repository: tuple[WorkCycle, str],
) -> None:
    """Neither an absent definition nor a changed entry is usable authority."""
    cycle, _ = repository

    async def run() -> None:
        identity = await activate(cycle)
        grant = await cycle.routine.local.authorize(
            identity, scope(cycle), assessment=assessment(), provider=provider()
        )
        local = cycle.routine.local
        ref = grant["reference"]
        with pytest.raises(PermissionError):
            local.enter(ref, "check", {"name": "absent", "definition_sha256": None})
        entry = local.enter(
            ref, "check", {"name": "focused", "definition_sha256": "b" * 64}
        )
        forged = copy.deepcopy(entry)
        forged["payload"]["name"] = "another-command"
        with pytest.raises(PermissionError, match="authentic"):
            local.complete(ref, forged, {"exit_code": 0})
        local.complete(ref, entry, {"exit_code": 0})
        with pytest.raises(FileExistsError):
            local.complete(ref, entry, {"exit_code": 0})

    asyncio.run(run())


def test_direct_delegation_entry_cannot_expand_budget(
    repository: tuple[WorkCycle, str],
) -> None:
    """Calling the consumed-entry boundary directly cannot inject negative credit."""
    cycle, _ = repository

    async def run() -> None:
        identity = await activate(cycle)
        selected = scope(cycle)
        grant = await cycle.routine.local.authorize(
            identity, selected, assessment=assessment(), provider=provider()
        )
        bad = copy.deepcopy(selected)
        bad["budgets"]["model_calls"] = -1
        with pytest.raises(PermissionError):
            cycle.routine.local.enter(
                grant["reference"], "delegate", {"scope": bad}, provider=provider()
            )
        assert not cycle.routine.local.records(grant["reference"])

    asyncio.run(run())

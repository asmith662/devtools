# Copyright (c) 2026
# ruff: noqa: F811, D103, COM812, PLR2004 -- bounded synthetic authority fixtures
"""Prospective provider enrollment, never real inference or service authority."""

from __future__ import annotations

import asyncio
import copy
from typing import TYPE_CHECKING, Any

import pytest

from scripts.backlog.routine.local import eligible
from scripts.backlog.routine.policy import validate
from tests.scripts.backlog.routine.test_authority import assessment, provider
from tests.scripts.backlog.routine.test_local import (
    Model,
    local_policy,
    measured,
    request,
    scope,
)
from tests.scripts.backlog.test_native import repository  # noqa: F401

if TYPE_CHECKING:
    from scripts.backlog.work import WorkCycle


def enrolled() -> dict[str, Any]:
    value = local_policy()
    value["schema"] = "routine-development-policy-v4"
    value["local"]["profiles"].append("alternate-review-v1")
    value["local"]["provider_profiles"] = {
        name: {
            "provider": copy.deepcopy(value["provider"]),
            "roles": list(value["local"]["roles"]),
            "budgets": dict(value["local"]["budgets"]),
        }
        for name in value["local"]["profiles"]
    }
    entry = value["local"]["provider_profiles"]["alternate-review-v1"]
    entry["provider"].update(
        endpoint="http://127.0.0.1:8081",
        model="neutral-alternate",
        context_tokens=32768,
    )
    entry["roles"] = ["supervisor", "reviewer"]
    entry["budgets"].update(call_seconds=600)
    return value


def selected(cycle: WorkCycle) -> dict[str, Any]:
    result = scope(cycle)
    result.update(profile="alternate-review-v1", roles=["reviewer"])
    result["budgets"].update(
        output_tokens=8192, total_output_tokens=16384, call_seconds=600
    )
    return result


def qualified() -> dict[str, Any]:
    return {
        "configuration": enrolled()["local"]["provider_profiles"][
            "alternate-review-v1"
        ]["provider"],
        "healthy": True,
        "idle": True,
    }


@pytest.mark.parametrize("change", ["missing", "shape", "endpoint", "role", "budget"])
def test_enrollment_is_closed(change: str) -> None:
    value = enrolled()
    entry = value["local"]["provider_profiles"]["alternate-review-v1"]
    if change == "missing":
        del value["local"]["provider_profiles"]["review-script-v1"]
    elif change == "shape":
        entry["shell"] = True
    elif change == "endpoint":
        entry["provider"]["endpoint"] = "https://paid.example"
    elif change == "role":
        entry["roles"] = ["installer"]
    else:
        entry["budgets"]["call_seconds"] = 601
    with pytest.raises((ValueError, PermissionError)):
        validate(value)


def test_v3_and_native_provider_cannot_inherit_enrollment() -> None:
    value = enrolled()
    validate(value)
    assert value["provider"] == provider()["configuration"]
    assert value["output_tokens"] == 2048
    value["provider"]["endpoint"] = "http://127.0.0.1:8081"
    with pytest.raises(ValueError, match="pinned"):
        validate(value)
    value = enrolled()
    value["schema"] = "routine-development-policy-v3"
    with pytest.raises(ValueError, match="Closed local"):
        validate(value)
    validate(local_policy())


@pytest.mark.parametrize(
    "change", ["provider", "role", "delegated-role", "budget", "context"]
)
def test_exact_profile_limits(repository: tuple[WorkCycle, str], change: str) -> None:
    cycle, _ = repository
    value, chosen, runtime = enrolled(), selected(cycle), qualified()
    if change == "provider":
        runtime = provider()
    elif change == "role":
        chosen["role"] = "coding"
    elif change == "delegated-role":
        chosen["roles"] = ["planner"]
    elif change == "budget":
        chosen["budgets"]["call_seconds"] = 601
    else:
        chosen["budgets"]["input_tokens"] = 32768
    with pytest.raises(PermissionError):
        eligible(
            value, {"operation": "authorize-routine-local", "scope": chosen}, runtime
        )


def test_fresh_grants_recheck_profile_and_revocation(
    repository: tuple[WorkCycle, str],
) -> None:
    cycle, _ = repository

    async def run() -> None:
        historical = await cycle.routine.control(
            "activate",
            policy=local_policy(),
            reference="fixture://v3",
            authorize=lambda _: True,
        )
        history_bytes = (cycle.routine.folder / "control-0001.json").read_bytes()
        active = await cycle.routine.control(
            "activate",
            policy=enrolled(),
            reference="fixture://explicit-enrollment",
            authorize=lambda _: True,
        )
        chosen = selected(cycle)
        parent = await cycle.routine.local.authorize(
            active["sha256"], chosen, assessment=assessment(), provider=qualified()
        )
        child = copy.deepcopy(chosen)
        child["profile"] = "review-script-v1"
        child["budgets"] = scope(cycle)["budgets"]
        with pytest.raises(PermissionError, match="Delegation"):
            await cycle.routine.local.authorize(
                active["sha256"],
                child,
                assessment=assessment(),
                provider=provider(),
                parent=parent["reference"],
            )
        model = Model()

        async def runtime() -> dict[str, Any]:
            return qualified()

        await cycle.routine.local.interact(
            parent["reference"],
            request(),
            interaction=model,
            qualify=runtime,
            measure=measured,
        )
        assert len(model.requests) == 1
        await cycle.routine.control(
            "revoke", reference="fixture://stop", authorize=lambda _: True
        )
        with pytest.raises(PermissionError, match="revoked"):
            cycle.routine.local.check(parent["reference"])
        assert historical["policy"]["schema"].endswith("v3")
        assert (
            cycle.routine.folder / "control-0001.json"
        ).read_bytes() == history_bytes

    asyncio.run(run())

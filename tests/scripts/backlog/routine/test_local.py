# Copyright (c) 2026
# ruff: noqa: F811, D103, PLR2004, COM812 -- independent finite authority fixtures
"""Deterministic standing local-work authority, never live inference evidence."""

from __future__ import annotations

import asyncio
import copy
from typing import TYPE_CHECKING, Any

import pytest

from devtools.context import Repository, RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Timestamp
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelSettings,
    Prompt,
)
from devtools.tools.source import SourceScope
from scripts.backlog.routine.policy import LOCAL, LOCAL_TOOLS, PURPOSES, ROLES, validate
from tests.scripts.backlog.routine.test_authority import assessment, policy, provider
from tests.scripts.backlog.test_native import SOURCE, repository  # noqa: F401

if TYPE_CHECKING:
    from scripts.backlog.work import WorkCycle


def local_policy() -> dict[str, Any]:
    value = policy()
    value.update(schema="routine-development-policy-v3", coding_attempts=2)
    value["operations"].append("local")
    value["local"] = {
        "profiles": list(value["profiles"]),
        "roles": sorted(ROLES),
        "purposes": sorted(PURPOSES),
        "read_roots": ["src/", "tests/", "docs/", ".local/"],
        "tools": sorted(LOCAL_TOOLS),
        "budgets": dict(LOCAL),
    }
    return value


async def activate(cycle: WorkCycle) -> str:
    control = await cycle.routine.control(
        "activate",
        policy=local_policy(),
        reference="fixture://one-policy-activation",
        authorize=lambda _: True,
    )
    return str(control["sha256"])


def scope(cycle: WorkCycle) -> dict[str, Any]:
    source = SourceScope.observe(
        root=resolve_path(cycle.root),
        repository=Repository.new(),
        addresses=(RepositoryResourceAddress(SOURCE),),
    )
    return {
        "subject": "existing-engineering-obligation",
        "plan_sha256": "a" * 64,
        "repository": str(source.snapshot.repository_id),
        "actor": "fixture-reviewer",
        "role": "reviewer",
        "roles": ["reviewer", "planner"],
        "purpose": "calibration",
        "profile": "review-script-v1",
        "inputs": {
            str(r.address): str(r.content_identity) for r in source.snapshot.resources
        },
        "tools": ["read_source"],
        "checks": {"focused": "b" * 64},
        "private_oracle": False,
        "budgets": {
            **LOCAL,
            "model_calls": 2,
            "input_tokens": 4096,
            "output_tokens": 512,
            "total_output_tokens": 1024,
            "reads": 2,
            "checks": 1,
            "delegations": 1,
            "wall_seconds": 600,
            "capture_bytes": 2097152,
        },
    }


class Model:
    """A neutral simulated adapter, not Qwen evidence."""

    def __init__(self) -> None:
        """Track only deterministic fixture requests."""
        self.requests: list[ModelRequest] = []
        self.source = InteractionSource("fixture-reviewer")

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Return simulated content without provider access."""
        self.requests.append(request)
        return ModelResponse("simulated conclusion, not host acceptance", self.source)


async def qualified() -> dict[str, Any]:
    return provider()


async def measured(_request: ModelRequest) -> int:
    return 100


def request() -> ModelRequest:
    return ModelRequest(
        Prompt("public fixture only", "user"),
        settings=ModelSettings(maximum_output_tokens=512),
    )


@pytest.mark.parametrize("purpose", sorted(PURPOSES))
def test_fresh_routine_grants_without_console(
    repository: tuple[WorkCycle, str], monkeypatch: pytest.MonkeyPatch, purpose: str
) -> None:
    cycle, _ = repository
    monkeypatch.setattr(
        "builtins.input", lambda *_: pytest.fail("Per-run approval requested")
    )

    async def run() -> None:
        identity = await activate(cycle)
        selected = scope(cycle)
        selected["purpose"] = purpose
        one = await cycle.routine.local.authorize(
            identity, selected, assessment=assessment(), provider=provider()
        )
        two = await cycle.routine.local.authorize(
            identity, selected, assessment=assessment(), provider=provider()
        )
        assert one["reference"] != two["reference"]
        assert one["decision"]["policy_version"] == identity
        assert one["decision"]["request"]["scope"] == selected
        assert cycle.routine.callback(one["reference"])(
            {**one["decision"]["request"], "reference": one["reference"]}
        )
        model = Model()
        result = await cycle.routine.local.interact(
            one["reference"],
            request(),
            interaction=model,
            qualify=qualified,
            measure=measured,
        )
        assert result.source == model.source
        assert len(model.requests) == 1
        assert len(cycle.routine.local.records(one["reference"])) == 1
        assert not (cycle.root / ".local/backlog/checkout-owner").exists()

    asyncio.run(run())


def test_revocation_during_call_preserves_return_but_stops_authority(
    repository: tuple[WorkCycle, str],
) -> None:
    cycle, _ = repository

    class Revoking(Model):
        async def send(self, request: ModelRequest) -> ModelResponse:
            result = await super().send(request)
            await cycle.routine.control(
                "revoke", reference="fixture://stop", authorize=lambda _: True
            )
            return result

    async def run() -> None:
        identity = await activate(cycle)
        grant = await cycle.routine.local.authorize(
            identity, scope(cycle), assessment=assessment(), provider=provider()
        )
        model = Revoking()
        with pytest.raises(PermissionError, match="revoked"):
            await cycle.routine.local.interact(
                grant["reference"],
                request(),
                interaction=model,
                qualify=qualified,
                measure=measured,
            )
        assert len(model.requests) == 1
        folder = cycle.routine.folder / "local" / grant["decision"]["sha256"]
        assert len(list(folder.glob("*-result.json"))) == 1

    asyncio.run(run())


def test_source_drift_expiry_provider_and_limits(
    repository: tuple[WorkCycle, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    cycle, _ = repository

    async def run() -> None:
        identity = await activate(cycle)
        selected = scope(cycle)
        selected["budgets"]["model_calls"] = 1
        grant = await cycle.routine.local.authorize(
            identity, selected, assessment=assessment(), provider=provider()
        )
        model = Model()
        await cycle.routine.local.interact(
            grant["reference"],
            request(),
            interaction=model,
            qualify=qualified,
            measure=measured,
        )
        with pytest.raises(PermissionError, match="exhausted"):
            await cycle.routine.local.interact(
                grant["reference"],
                request(),
                interaction=model,
                qualify=qualified,
                measure=measured,
            )
        assert len(model.requests) == 1
        actual = provider()
        actual["idle"] = False
        with pytest.raises(PermissionError, match="provider"):
            await cycle.routine.local.authorize(
                identity, scope(cycle), assessment=assessment(), provider=actual
            )
        now = Timestamp.now()
        with monkeypatch.context() as patch:
            patch.setattr(
                Timestamp, "now", classmethod(lambda _: now + Duration.hours(2))
            )
            with pytest.raises(PermissionError, match="expired"):
                cycle.routine.local.check(grant["reference"])
        (cycle.root / SOURCE).write_text("def value(): return 99\n")
        with pytest.raises(PermissionError, match="drift"):
            cycle.routine.local.check(grant["reference"])

    asyncio.run(run())


@pytest.mark.parametrize(
    "change", ["private", "secret", "tool", "path", "budget", "actor", "output"]
)
def test_exceptions_and_scope_expansion_refused(
    repository: tuple[WorkCycle, str], change: str
) -> None:
    cycle, _ = repository

    async def run() -> None:
        identity = await activate(cycle)
        selected = scope(cycle)
        assess = assessment()
        if change == "private":
            selected["private_oracle"] = True
        if change == "secret":
            assess["secrets"] = True
        if change == "tool":
            selected["tools"].append("shell")
        if change == "path":
            selected["inputs"] = {".local/backlog/private.json": "c" * 64}
        if change == "budget":
            selected["budgets"]["model_calls"] = 999
        if change in {"actor", "output"}:
            grant = await cycle.routine.local.authorize(
                identity, selected, assessment=assess, provider=provider()
            )
            model = Model()
            if change == "actor":
                model.source = InteractionSource("other-actor")
            req = (
                request()
                if change == "actor"
                else ModelRequest(
                    Prompt("fixture", "user"),
                    settings=ModelSettings(maximum_output_tokens=513),
                )
            )
            with pytest.raises(PermissionError):
                await cycle.routine.local.interact(
                    grant["reference"],
                    req,
                    interaction=model,
                    qualify=qualified,
                    measure=measured,
                )
            assert not model.requests
        else:
            with pytest.raises(PermissionError):
                await cycle.routine.local.authorize(
                    identity, selected, assessment=assess, provider=provider()
                )

    asyncio.run(run())


def test_delegation_carves_parent_budget_and_inherits_revocation(
    repository: tuple[WorkCycle, str],
) -> None:
    cycle, _ = repository

    async def run() -> None:
        identity = await activate(cycle)
        selected = scope(cycle)
        selected["budgets"]["model_calls"] = 1
        root = await cycle.routine.local.authorize(
            identity, selected, assessment=assessment(), provider=provider()
        )
        child = copy.deepcopy(selected)
        child["budgets"].update(
            total_output_tokens=512,
            reads=0,
            checks=0,
            capture_bytes=524288,
            delegations=0,
        )
        child["roles"] = []
        grant = await cycle.routine.local.authorize(
            identity,
            child,
            assessment=assessment(),
            provider=provider(),
            parent=root["reference"],
        )
        assert grant["decision"]["expires_at"] == root["decision"]["expires_at"]
        assert grant["decision"]["request"]["parent"] == root["reference"]
        with pytest.raises(PermissionError, match="exhausted"):
            await cycle.routine.local.interact(
                root["reference"],
                request(),
                interaction=Model(),
                qualify=qualified,
                measure=measured,
            )
        await cycle.routine.local.interact(
            grant["reference"],
            request(),
            interaction=Model(),
            qualify=qualified,
            measure=measured,
        )
        await cycle.routine.control(
            "deny",
            subject=selected["subject"],
            reference="fixture://deny",
            authorize=lambda _: True,
        )
        with pytest.raises(PermissionError, match="denied"):
            cycle.routine.local.check(grant["reference"])

    asyncio.run(run())


@pytest.mark.parametrize(
    "change", ["plan", "subject", "inputs", "roles", "tools", "budget"]
)
def test_delegation_cannot_expand_authority(
    repository: tuple[WorkCycle, str], change: str
) -> None:
    cycle, _ = repository

    async def run() -> None:
        identity = await activate(cycle)
        selected = scope(cycle)
        root = await cycle.routine.local.authorize(
            identity, selected, assessment=assessment(), provider=provider()
        )
        child = copy.deepcopy(selected)
        if change == "plan":
            child["plan_sha256"] = "f" * 64
        if change == "subject":
            child["subject"] = "another-obligation"
        if change == "inputs":
            child["inputs"] = {}
        if change == "roles":
            child["role"] = "researcher"
        if change == "tools":
            child["tools"].append("submit_review_proposal")
        if change == "budget":
            child["budgets"]["model_calls"] += 1
        if change == "inputs":
            child["inputs"] = {"src/devtools/unknown.py": "d" * 64}
        with pytest.raises((PermissionError, OSError, ValueError)):
            await cycle.routine.local.authorize(
                identity,
                child,
                assessment=assessment(),
                provider=provider(),
                parent=root["reference"],
            )
        assert not cycle.routine.local.records(root["reference"])

    asyncio.run(run())


def test_unknown_effect_is_consumed_and_not_retried(
    repository: tuple[WorkCycle, str],
) -> None:
    cycle, _ = repository

    class Failing(Model):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            message = "Unknown provider effect"
            raise ConnectionError(message)

    async def run() -> None:
        identity = await activate(cycle)
        grant = await cycle.routine.local.authorize(
            identity, scope(cycle), assessment=assessment(), provider=provider()
        )
        model = Failing()
        with pytest.raises(ConnectionError):
            await cycle.routine.local.interact(
                grant["reference"],
                request(),
                interaction=model,
                qualify=qualified,
                measure=measured,
            )
        with pytest.raises(PermissionError, match="reconciliation"):
            await cycle.routine.local.interact(
                grant["reference"],
                request(),
                interaction=model,
                qualify=qualified,
                measure=measured,
            )
        assert len(model.requests) == 1

    asyncio.run(run())


def test_fixed_reads_checks_and_immutable_history(
    repository: tuple[WorkCycle, str],
) -> None:
    cycle, _ = repository

    async def run() -> None:
        previous = await cycle.routine.control(
            "activate",
            policy=policy(),
            reference="fixture://historical",
            authorize=lambda _: True,
        )
        path = cycle.routine.folder / "control-0001.json"
        original = path.read_bytes()
        identity = await activate(cycle)
        assert path.read_bytes() == original
        assert previous["policy"]["schema"].endswith("v1")
        grant = await cycle.routine.local.authorize(
            identity, scope(cycle), assessment=assessment(), provider=provider()
        )
        local = cycle.routine.local
        ref = grant["reference"]
        entry = local.enter(ref, "read", {"path": SOURCE, "maximum_bytes": 100})
        local.complete(ref, entry, {"status": "completed by existing source Tool"})
        check = local.enter(
            ref, "check", {"name": "focused", "definition_sha256": "b" * 64}
        )
        local.complete(ref, check, {"exit_code": 0})
        with pytest.raises(PermissionError):
            local.enter(ref, "check", {"name": "other", "definition_sha256": "b" * 64})
        with pytest.raises(PermissionError):
            local.enter(ref, "edit", {})
        assert len(local.records(ref)) == 2
        validate(policy())
        v2 = policy()
        v2.update(schema="routine-development-policy-v2", coding_attempts=2)
        validate(v2)
        assert path.read_bytes() == original

    asyncio.run(run())

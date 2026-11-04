# Copyright (c) 2026
# ruff: noqa: F811, SLF001, PLR2004, ASYNC240, COM812 -- authored filesystem fixtures
"""Deterministic native continuation; no live model competence claims."""

from __future__ import annotations

import asyncio
import copy
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from scripts.backlog.routine.policy import validate
from tests.scripts.backlog.routine.test_authority import assessment, policy, provider
from tests.scripts.backlog.test_native import (
    Scripted,
    edit,
    read_call,
    repository,  # noqa: F401 -- pytest fixture
    task,
)

if TYPE_CHECKING:
    from scripts.backlog.work import WorkCycle


async def failed(cycle: WorkCycle, item: str) -> str:
    """Exercise a real edit/public failure/terminal restoration with a fake model."""
    config = policy()
    config.update(schema="routine-development-policy-v2", coding_attempts=2)
    active = await cycle.routine.control(
        "activate",
        policy=config,
        reference="fixture://operator",
        authorize=lambda _: True,
    )
    packet = task()
    packet["budgets"]["proposals"] = 1
    await cycle.native.prepare(
        item,
        branch="feat/native-work",
        task=packet,
        supervisor="fixture supervisor",
    )
    grant = await cycle.routine.authorize_native(
        active["sha256"],
        item,
        assessment=assessment(),
        provider=provider(),
    )
    result = await cycle.native.execute(
        item,
        interaction=Scripted("neutral-script-a", [read_call(), edit(1, 2, "bad")]),
        profile="scripted-v1",
        authorize=cycle.routine.callback(grant["reference"]),
    )
    assert result["disposition"] == "BLOCKED"
    assert result["facts"]["coding_disposition"] == "proposal_limit"
    return str(active["sha256"])


def test_fresh_attempt_and_alternate_adapter(repository: tuple[WorkCycle, str]) -> None:
    """Check the real administrative and coding boundary with simulated models."""
    cycle, item = repository

    async def run() -> None:
        version = await failed(cycle, item)
        original = {
            p.relative_to(cycle._folder(item)): p.read_bytes()
            for p in cycle._folder(item).rglob("*")
            if p.is_file()
        }
        packet = copy.deepcopy(cycle.native.record(item, "assignment")["task"])
        packet["worker"].update(
            actor="alternate actor",
            source="alternate-neutral-model",
        )
        child = await cycle.native.prepare_continuation(
            item,
            attempt=2,
            policy=version,
            branch="feat/native-work",
            task=packet,
            supervisor="trusted decision to disclose public failure",
            disclose_public=True,
        )
        owner = cycle.native.select(2)
        assert child["sha256"] != cycle.native.record(item, "assignment")["sha256"]
        assert child["continuation"]["number"] == 2
        with pytest.raises((FileExistsError, PermissionError)):
            await cycle.native.prepare_continuation(
                item,
                attempt=2,
                policy=version,
                branch="feat/native-work",
                task=packet,
                supervisor="duplicate",
            )
        grant = await cycle.routine.authorize_native(
            version,
            item,
            attempt=2,
            assessment=assessment(),
            provider=provider(),
        )
        assert grant["assignment_sha256"] == child["sha256"]
        model = Scripted("alternate-neutral-model", [read_call(), edit(1, 3, "fixed")])
        result = await owner.execute(
            item,
            interaction=model,
            profile="scripted-v1",
            authorize=cycle.routine.callback(grant["reference"]),
        )
        assert result["disposition"] == "REVIEW_CANDIDATE", result
        assert result["facts"]["acceptance"]["passed"]
        assert result["checkout_released"]
        assert all(
            (cycle._folder(item) / name).read_bytes() == data
            for name, data in original.items()
        )
        assert cycle.intake.approved_item(item)["status"] == "BACKLOG"
        disclosed = str(model.requests)
        assert "Previous candidate failed public validation" in disclosed
        assert "assert 2 == 3" in disclosed
        assert "assert module.value() == 3" not in disclosed
        assert "withheld.py" not in disclosed
        with pytest.raises(PermissionError, match="limit"):
            await cycle.native.prepare_continuation(
                item,
                attempt=3,
                policy=version,
                branch="feat/native-work",
                task=packet,
                supervisor="over budget",
            )
        with pytest.raises(PermissionError, match="Consumed"):
            await cycle.routine.authorize_native(
                version,
                item,
                attempt=2,
                assessment=assessment(),
                provider=provider(),
            )

    asyncio.run(run())


@pytest.mark.parametrize(
    "change",
    ["source", "candidate", "obligations", "revoked", "unknown", "closed", "expired"],
)
def test_continuation_refuses_unsafe_predecessor(
    repository: tuple[WorkCycle, str],
    change: str,
) -> None:
    """Check the real administrative and coding boundary with simulated models."""
    cycle, item = repository

    async def run() -> None:
        version = await failed(cycle, item)
        packet = copy.deepcopy(cycle.native.record(item, "assignment")["task"])
        if change == "source":
            (cycle.root / packet["source"]).write_text("tampered\n")
        elif change == "candidate":
            (cycle._folder(item) / "worker/final-source.py").write_text("tampered\n")
        elif change == "obligations":
            packet["objective"] = "different engineering obligation"
        elif change == "revoked":
            await cycle.routine.control(
                "revoke",
                reference="fixture stop",
                authorize=lambda _: True,
            )
        elif change == "closed":
            binding = cycle.intake.approved_item(item)

            path = Path(binding["path"])
            path.write_text(
                path.read_text().replace("status: BACKLOG", "status: CLOSED"),
            )
        else:
            # Authenticated but inconsistent/expired records must still be refused.
            name = "result" if change == "unknown" else "authorization"
            row = cycle.native.record(item, name)
            path = cycle._folder(item) / (name + ".json")
            path.unlink()
            row.pop("sha256")
            if change == "unknown":
                row["facts"]["effects"][0]["acknowledged"] = False
                execution = cycle.native.record(item, "execution")
                execution.pop("sha256")
                execution["facts"] = row["facts"]
                execution_path = cycle._folder(item) / "execution.json"
                execution_path.unlink()
                row["execution_sha256"] = cycle._save(execution_path, execution)[
                    "sha256"
                ]
            else:
                row["expires_at"] = row["issued_at"]
            cycle._save(path, row)
        with pytest.raises((PermissionError, ValueError)):
            await cycle.native.prepare_continuation(
                item,
                attempt=2,
                policy=version,
                branch="feat/native-work",
                task=packet,
                supervisor="supervisor",
            )

    asyncio.run(run())


@pytest.mark.parametrize("maximum", [0, True, 101, "2"])
def test_policy_requires_finite_attempt_limit(maximum: object) -> None:
    """Reject nonfinite or noninteger attempt limits."""
    config = policy()
    config.update(schema="routine-development-policy-v2", coding_attempts=maximum)
    with pytest.raises(ValueError, match="Finite"):
        validate(config)


def test_historical_policy_stays_one_slot() -> None:
    """Keep the original policy readable without expanding its authority."""
    validate(policy())
    assert policy().get("coding_attempts", 1) == 1
    config = policy()
    config.update(schema="routine-development-policy-v2", coding_attempts=3)
    validate(config)


@pytest.mark.parametrize("change", ["source", "revoked", "expired"])
def test_child_boundaries_recheck_authority_and_source(
    repository: tuple[WorkCycle, str], change: str
) -> None:
    """A prepared child never establishes lasting authority or source custody."""
    cycle, item = repository

    async def run() -> None:
        version = await failed(cycle, item)
        packet = cycle.native.record(item, "assignment")["task"]
        child = await cycle.native.prepare_continuation(
            item,
            attempt=2,
            policy=version,
            branch="feat/native-work",
            task=packet,
            supervisor="trusted supervisor withholding public output",
        )
        assert child["continuation"]["feedback"]["public_checks"] == []
        grant = await cycle.routine.authorize_native(
            version, item, attempt=2, assessment=assessment(), provider=provider()
        )
        owner = cycle.native.select(2)
        if change == "source":
            (cycle.root / packet["source"]).write_text("unrecognized source\n")
        elif change == "revoked":
            await cycle.routine.control(
                "revoke", reference="fixture stop", authorize=lambda _: True
            )
        else:
            path = owner.folder(item) / "authorization.json"
            path.unlink()
            grant.pop("sha256")
            grant["expires_at"] = grant["issued_at"]
            cycle._save(path, grant)
        model = Scripted("neutral-script-a")
        with pytest.raises(PermissionError):
            await owner.execute(
                item,
                interaction=model,
                profile="scripted-v1",
                authorize=cycle.routine.callback(grant["reference"]),
            )
        assert model.requests == []
        assert not (owner.folder(item) / "dispatch.json").exists()

    asyncio.run(run())


def test_existing_backlog_readiness_uses_intake_owner(
    repository: tuple[WorkCycle, str],
) -> None:
    """Activate an existing investigation only after an explicit readiness decision."""
    cycle, _ = repository
    path = cycle.root / "docs/backlog/items/B-0009-existing.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# B-0009 Existing\n\n- status: DEFERRED\n")
    overview = cycle.root / "docs/backlog/overview.md"
    overview.write_text(
        overview.read_text().replace("Existing | BACKLOG", "Existing | DEFERRED"),
    )
    with pytest.raises(PermissionError, match="Explicit"):
        cycle.intake.activate_existing(
            "B-0009",
            reference="fixture operator",
            rationale="Ready bounded consumer",
        )
    receipt = cycle.intake.activate_existing(
        "B-0009",
        reference="fixture operator",
        rationale="Ready bounded consumer",
        authorize=lambda _: True,
    )
    assert receipt["item"] == "B-0009"
    assert "status: ACTIVE" in path.read_text()
    assert "Existing | ACTIVE" in overview.read_text()

# Copyright (c) 2026
# ruff: noqa: S101, D103, ANN401, PLC0415 -- synthetic authority contracts
"""Prove authority transitions using only temporary repositories and fake workers."""

from __future__ import annotations

import asyncio
import json
import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

import pytest

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.authority import (
    ApprovalRequest,
    ExecutionAuthorization,
    approval,
    authenticate,
)
from experiments.orchestration.model import LEGACY_SCHEMA, RunPlan
from experiments.orchestration.publication import Repository
from experiments.orchestration.storage import load, save
from experiments.orchestration.tests.test_controller import FixtureController, fixture


def grant(controller: Any) -> ApprovalRequest:
    return ApprovalRequest(
        controller.run_id,
        "synthetic-maintainer",
        "explicit test decision",
    )


def no_entry(controller: Any) -> None:
    assert not list(controller.science.glob("journal/*/*/ENTERED.json"))


def test_unapproved_validation_and_callable_authority(tmp_path: Path) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work", approved=False)
        identity, raw = c.run_id, c.plan.canonical
        head = await c.repository.git("rev-parse", "HEAD")
        assert c.status()["status"] == "PLANNED"
        again = await FixtureController.from_plan(
            c.repository.root,
            "plan.json",
            c.work_root,
        )
        assert again.run_id == identity
        assert again.plan_report()["execution_authorized"] == "NO"
        assert again.plan_report()["status"] == "PLAN_VALID"
        assert not (c.science / "authorization").exists()
        with pytest.raises(ValueError, match="authorization value required"):
            await again.run()
        with pytest.raises(ValueError, match="approval absent"):
            await again.run(
                ExecutionAuthorization(identity, digest(raw), "0" * 64, "0" * 40),
            )
        assert await c.repository.git("rev-parse", "HEAD") == head
        no_entry(c)
        token = await c.approve(grant(c))
        assert c.plan.canonical == raw
        assert c.run_id == identity
        assert c.status()["status"] == "APPROVED"
        assert token == await again.execution_authorization()
        assert again.status()["status"] == "APPROVED"
        assert token.plan_sha256 == digest(raw)
        receipt = load(c.science / "authorization/approval.json")
        assert receipt["run_id"] == identity
        assert receipt["stage_a_checkpoint"] == c.value["stage_a"]["checkpoint"]
        assert receipt["plan_checkpoint"] == c.plan_checkpoint
        assert receipt["review_checkpoint"] == head.decode().strip()
        assert await c.repository.git(
            "show",
            token.checkpoint + ":" + c.approval_prefix + "/approval.json",
        ) == json_bytes(receipt)
        with pytest.raises(ValueError, match="authorization value required"):
            await again.run()
        with pytest.raises(ValueError, match="durable approval"):
            await again.run(
                ExecutionAuthorization(
                    identity,
                    digest(raw),
                    "f" * 64,
                    token.checkpoint,
                ),
            )
        with pytest.raises(ValueError, match=r"advancement|immutable"):
            await c.approve(grant(c))
        no_entry(c)

    asyncio.run(run())


@pytest.mark.parametrize(
    "field",
    [
        "schema",
        "plan_sha256",
        "run_id",
        "stage_a_checkpoint",
        "controller_sha256",
        "plan_path",
        "plan_checkpoint",
        "review_checkpoint",
        "sha256",
        "authority",
        "approved_at",
    ],
)
def test_approval_binding_rejects_mutation(tmp_path: Path, field: str) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work", approved=False)
        binding = c.approval_binding(c.validated_head)
        value = approval(grant(c), binding, "2026-10-13T12:00:00+00:00")
        assert value == approval(grant(c), binding, "2026-10-13T12:00:00+00:00")
        authenticate(value, binding)
        value[field] = {} if field == "authority" else "foreign"
        # Re-signing a mutated payload cannot repair its frozen prospective binding.
        if field != "sha256":
            value["sha256"] = digest(
                json_bytes({k: v for k, v in value.items() if k != "sha256"}),
            )

        async def publish_only(*_args: Any) -> None:
            return

        await c.repository.commit(
            "APPROVAL",
            c.approval_prefix,
            {"approval.json": json_bytes(value)},
            "Synthetic invalid authority",
            publish_only,
        )
        with pytest.raises((ValueError, TypeError)):
            await c.execution_authorization()
        no_entry(c)

    asyncio.run(run())


def test_uncommitted_approval_and_local_handoff_are_not_authority(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work", approved=False)
        value = approval(
            grant(c),
            c.approval_binding(c.validated_head),
            "2026-10-13T12:00:00+00:00",
        )
        save(c.operational / "approval.json", value)
        with pytest.raises(ValueError, match="approval absent"):
            await c.execution_authorization()
        save(c.science / "authorization/approval.json", value)
        with pytest.raises(ValueError, match="committed once"):
            await c.execution_authorization()
        no_entry(c)

    asyncio.run(run())


def test_changed_plan_and_controller_reject_existing_authority(tmp_path: Path) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        value = c.plan.value
        value["attempt"] += 1
        changed = RunPlan.parse(value)
        (c.repository.root / "plan.json").write_bytes(changed.canonical)
        await c.repository.git("add", "plan.json")
        await c.repository.git("commit", "-m", "Synthetic changed attempt")
        with pytest.raises(ValueError, match="binding differs"):
            await c.execution_authorization()
        new = await FixtureController.from_plan(
            c.repository.root,
            "plan.json",
            c.work_root,
        )
        assert new.run_id != c.run_id
        with pytest.raises(ValueError, match="another run"):
            await new.approve(grant(c))
        with pytest.raises(ValueError, match="approval absent"):
            await new.execution_authorization()
        value["controller_implementation"] = {"changed.py": "0" * 64}
        (c.repository.root / "plan.json").write_bytes(RunPlan.parse(value).canonical)
        await c.repository.git("add", "plan.json")
        await c.repository.git("commit", "-m", "Synthetic changed controller")
        with pytest.raises(ValueError, match="implementation differs"):
            await FixtureController.from_plan(
                c.repository.root,
                "plan.json",
                c.work_root,
            )
        no_entry(c)

    asyncio.run(run())


async def remote_fixture(tmp_path: Path) -> tuple[Any, Repository]:
    c = await fixture(tmp_path / "repo", tmp_path / "work", approved=False)
    bare = tmp_path / "remote.git"
    bare.mkdir()
    remote = Repository(bare, push=False)
    await remote.git("init", "--bare", "--initial-branch=main")
    await c.repository.git("remote", "add", "origin", str(bare))
    value = c.plan.value
    value["publication"]["push"] = True
    (c.repository.root / "plan.json").write_bytes(RunPlan.parse(value).canonical)
    await c.repository.git("add", "plan.json")
    await c.repository.git("commit", "-m", "Synthetic remote-durable plan")
    await c.repository.git("push", "-u", "origin", "main")
    return await FixtureController.from_plan(
        c.repository.root,
        "plan.json",
        c.work_root,
    ), remote


@pytest.mark.parametrize("operation", ["commit", "push"])
def test_approval_publication_failure_never_enters(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    operation: str,
) -> None:
    async def run() -> None:
        c, remote = await remote_fixture(tmp_path)
        before = await remote.git("rev-parse", "main")
        original = c.repository.git

        async def fail(*args: str) -> bytes:
            if args[0] == operation:
                raise ValueError("Synthetic approval " + operation + " failure")
            return bytes(await original(*args))

        monkeypatch.setattr(c.repository, "git", fail)
        with pytest.raises(ValueError, match="Synthetic approval"):
            await c.approve(grant(c))
        assert c.status()["execution_authorized"] == "NO"
        assert await remote.git("rev-parse", "main") == before
        with pytest.raises(ValueError, match=r"tracked|origin/main"):
            await c.execution_authorization()
        no_entry(c)

    asyncio.run(run())


def test_remote_divergence_blocks_approval_and_execution(tmp_path: Path) -> None:
    async def run() -> None:
        c, remote = await remote_fixture(tmp_path)
        await remote.git(
            "update-ref",
            "refs/heads/main",
            c.value["stage_a"]["checkpoint"],
        )
        with pytest.raises(ValueError, match="Actual remote"):
            await c.approve(grant(c))
        no_entry(c)
        await remote.git("update-ref", "refs/heads/main", c.validated_head)
        await c.approve(grant(c))
        await remote.git("update-ref", "refs/heads/main", c.validated_head)
        with pytest.raises(ValueError, match="Actual remote"):
            await c.execution_authorization()
        no_entry(c)

    asyncio.run(run())


def test_legacy_plan_is_readable_but_boolean_approval_cannot_execute(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work", approved=False)
        value = c.plan.value
        value.update(schema=LEGACY_SCHEMA, approval="approval.json")
        plan = RunPlan.parse(value)
        assert RunPlan.parse(json.loads(plan.canonical)).canonical == plan.canonical
        (c.repository.root / "plan.json").write_bytes(plan.canonical)
        save(c.repository.root / "approval.json", {"approved": True})
        await c.repository.git("add", ".")
        await c.repository.git("commit", "-m", "Synthetic legacy receipt")
        old = await FixtureController.from_plan(
            c.repository.root,
            "plan.json",
            c.work_root,
        )
        assert old.plan_report()["status"] == "PLAN_VALID"
        with pytest.raises(ValueError, match="read-only"):
            await old.approve(grant(old))
        with pytest.raises(ValueError, match="read-only"):
            await old.execution_authorization()
        no_entry(old)

    asyncio.run(run())


def test_authority_inspection_does_not_revoke_active_grant(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        token = await c.execution_authorization()
        entered, release = asyncio.Event(), asyncio.Event()
        original = c.repository.git

        async def pause(*args: str) -> bytes:
            if args == ("rev-parse", "HEAD"):
                entered.set()
                await release.wait()
            return await original(*args)

        monkeypatch.setattr(c.repository, "git", pause)
        pending = asyncio.create_task(c.execution_authorization())
        await entered.wait()
        observed = c.status()
        release.set()
        assert await pending == token
        assert observed["status"] == "APPROVED"
        assert observed["execution_authorized"] == "YES"
        no_entry(c)

    asyncio.run(run())


def test_resume_rejects_foreign_approval_context(tmp_path: Path) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        save(
            c.science / "run.json",
            {
                "run_id": c.run_id,
                "plan": c.value,
                "implementation": c.value["controller_implementation"],
                "approval_checkpoint": c.value["stage_a"]["checkpoint"],
            },
        )
        with pytest.raises(ValueError, match="Resume approval context differs"):
            await c.run(await c.execution_authorization(), resume=True)
        no_entry(c)

    asyncio.run(run())


def test_cli_plan_status_and_approval_then_fake_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    from experiments.orchestration import __main__ as cli

    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work", approved=False)
        monkeypatch.setattr(cli, "Controller", FixtureController)
        base = [
            "controller",
            "plan",
            "plan.json",
            "--repository",
            str(c.repository.root),
            "--work-root",
            str(c.work_root),
        ]
        monkeypatch.setattr(sys, "argv", base)
        await cli.main()
        preview = json.loads(capsys.readouterr().out)
        assert preview["status"] == "PLAN_VALID"
        assert preview["execution_authorized"] == "NO"
        assert not (c.science / "authorization").exists()
        base[1] = "status"
        await cli.main()
        assert json.loads(capsys.readouterr().out)["status"] == "PLANNED"
        base[1] = "run"
        with pytest.raises(ValueError, match="approval absent"):
            await cli.main()
        no_entry(c)
        monkeypatch.setattr(sys, "argv", [*base, "--approve", c.run_id])
        await cli.main()
        completed = json.loads(capsys.readouterr().out)
        assert completed["status"].startswith("COMPLETE")
        assert completed["run_id"] == preview["run_id"]
        receipt = load(c.science / "authorization/approval.json")
        assert receipt["authority"]["kind"] == "MAINTAINER_CLI"
        base[1] = "verify-approval"
        monkeypatch.setattr(sys, "argv", base)
        await cli.main()
        assert json.loads(capsys.readouterr().out)["status"] == "APPROVAL_VALID"

    asyncio.run(run())

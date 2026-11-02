# Copyright (c) 2026
# ruff: noqa: F811, COM812 -- imported pytest fixture, formatter compatibility

"""Standing consent composes real native owners; scripted models prove mechanics."""

from __future__ import annotations

import asyncio
import copy
import json
from typing import TYPE_CHECKING, Any

import pytest

from devtools.core.time import Duration, Timestamp
from scripts.backlog.coordinator import git
from scripts.backlog.routine.policy import CODING, EXCEPTIONS, REVIEW, validate
from tests.scripts.backlog.test_native import (
    ReviewModel,
    Scripted,
    repository,  # noqa: F401 -- maintained independently authored repository fixture
    reviewer_policy,
    task,
)

if TYPE_CHECKING:
    from scripts.backlog.work import WorkCycle


def policy() -> dict[str, Any]:
    """Use a pinned synthetic provider; never enter a real model or container."""
    return {
        "schema": "routine-development-policy-v1",
        "categories": ["bug", "enhancement", "refactor"],
        "edit_roots": ["src/devtools/"],
        "read_roots": ["src/devtools/", "tests/"],
        "profiles": ["scripted-v1", "review-script-v1"],
        "provider": {
            "endpoint": "http://127.0.0.1:8080",
            "model": "fixture-only",
            "image": "0" * 64,
            "artifact_sha256": "1" * 64,
            "context_tokens": 65536,
        },
        "coding": dict(CODING),
        "review": dict(REVIEW),
        "output_tokens": 2048,
        "grant_seconds": 3600,
        "operations": [
            "intake",
            "coding",
            "acceptance-review",
            "diagnostic-review",
            "host-review",
            "integration-plan",
            "git",
        ],
        "git": {"remote": "origin", "branches": ["main"], "force": False},
        "validation": "protected-development-100-percent-v1",
    }


def assessment() -> dict[str, Any]:
    """Explicit host semantic assessment; task prose alone never grants authority."""
    return {
        "reference": "fixture://independent-supervisor-assessment",
        **dict.fromkeys(EXCEPTIONS, False),
    }


def provider() -> dict[str, Any]:
    """Qualify only the fixture's configured neutral scripted provider."""
    return {"configuration": policy()["provider"], "healthy": True, "idle": True}


async def activate(cycle: WorkCycle) -> str:
    """Simulate one operator decision only inside a tiny authored repository."""
    record = await cycle.routine.control(
        "activate",
        policy=policy(),
        reference="fixture://one-human-policy-decision",
        authorize=lambda _: True,
    )
    return str(record["sha256"])


async def prepare(cycle: WorkCycle, item: str) -> None:
    """Prepare without the legacy fixture helper's manual grant."""
    await cycle.native.prepare(
        item,
        branch="feat/native-work",
        task=task(),
        supervisor="Fixture trusted supervisor",
    )


def test_real_native_review_and_plan_use_one_policy(
    repository: tuple[WorkCycle, str],
) -> None:
    """No per-task console; actual read/edit/fail/repair/check/private/review/plan."""
    cycle, item = repository

    async def run() -> None:
        identity = await activate(cycle)
        await prepare(cycle, item)
        grant = await cycle.routine.authorize_native(
            identity, item, assessment=assessment(), provider=provider()
        )
        assert identity in grant["reference"]
        result = await cycle.native.execute(
            item,
            interaction=Scripted("neutral-script-a"),
            profile="scripted-v1",
            authorize=cycle.routine.callback(grant["reference"]),
        )
        assert result["disposition"] == "REVIEW_CANDIDATE"
        assert result["facts"]["acceptance"]["passed"]
        await cycle.native.reviewer.prepare(item, reviewer=reviewer_policy())
        review_grant = await cycle.routine.authorize_reviewer(
            identity, item, assessment=assessment(), provider=provider()
        )
        proposal = await cycle.native.reviewer.execute(
            item,
            interaction=ReviewModel(),
            profile="review-script-v1",
            authorize=cycle.routine.callback(review_grant["reference"]),
        )
        assert proposal["status"] == "proposed"
        review = await cycle.routine.host_review(
            identity,
            item,
            proposal=proposal["sha256"],
            accept=True,
            rationale="Host checked the source and finite acceptance evidence",
            assessment=assessment(),
        )
        await git(cycle.root, "branch", "main")
        await git(cycle.root, "push", "origin", "main")
        await git(cycle.root, "switch", "main")
        spec = {
            "remote": "origin",
            "destination": "main",
            "feature": "feat/integrated",
            "checkout": str(cycle.root),
            "additions": [],
            "parent_complete": False,
            "remaining": ["Separately authorize installation and protected validation"],
            "rationale": "Read-only authenticated candidate plan",
            "validation_seconds": 60,
        }
        plan = await cycle.routine.plan(
            identity, item, review["sha256"], spec, assessment=assessment()
        )
        assert plan["candidate_kind"] == "native-v1"
        assert plan["accepted_review"] == review["sha256"]
        assert await git(cycle.root, "branch", "--show-current") == "main"
        assert not (cycle.root / ".local/backlog/checkout-owner").exists()
        with pytest.raises(PermissionError, match="Consumed"):
            await cycle.routine.authorize_native(
                identity, item, assessment=assessment(), provider=provider()
            )
        await cycle.routine.control(
            "revoke", reference="fixture://operator-stop", authorize=lambda _: True
        )
        with pytest.raises(PermissionError, match="revoked"):
            cycle.integration.candidate(item, review["sha256"])

    asyncio.run(run())


def test_multiple_tasks_share_policy_and_no_interactive_consent(
    repository: tuple[WorkCycle, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """One policy may review another real proposal and issue distinct exact grants."""
    cycle, item = repository
    monkeypatch.setattr(
        "builtins.input", lambda *_: pytest.fail("Unexpected interactive consent")
    )

    async def run() -> None:
        identity = await activate(cycle)
        payload = copy.deepcopy(cycle.intake.approved_item(item)["proposal"]["payload"])
        payload["title"] = "Another independently reviewed authored obligation"
        proposal = cycle.intake.capture(payload)
        review = cycle.routine.intake_review(
            identity,
            proposal,
            assessment=assessment(),
            decision="APPROVED",
            rationale="A distinct bounded obligation",
            duplicate_disposition="Shared source, independent task",
            domain="agents",
        )
        other = review["publication"]["id"]
        await git(cycle.root, "add", "docs")
        await git(cycle.root, "commit", "-m", "Publish authored second obligation")
        # Tiny fixture branch is not active or owned; ordinary non-force advance.
        await git(cycle.root, "branch", "-d", "feat/native-work")
        await git(cycle.root, "branch", "feat/native-work")
        for selected in (item, other):
            await prepare(cycle, selected)
            grant = await cycle.routine.authorize_native(
                identity, selected, assessment=assessment(), provider=provider()
            )
            assert identity in grant["reference"]
            decision = cycle.routine.check_reference(grant["reference"])
            assert decision is not None
            assert decision["subject"] == selected
        assert (
            cycle.native.record(item, "authorization")["reference"]
            != cycle.native.record(other, "authorization")["reference"]
        )

    asyncio.run(run())


def test_expiry_denial_and_replacement_override_grants(
    repository: tuple[WorkCycle, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Standing consent persists; finite individual grants and revocation still bind."""
    cycle, item = repository

    async def run() -> None:
        identity = await activate(cycle)
        await prepare(cycle, item)
        grant = await cycle.routine.authorize_native(
            identity, item, assessment=assessment(), provider=provider()
        )
        now = Timestamp.now()
        with monkeypatch.context() as patch:
            patch.setattr(
                Timestamp, "now", classmethod(lambda _: now + Duration.hours(2))
            )
            assert cycle.routine.active(identity)["sha256"] == identity
            with pytest.raises(PermissionError, match="expired"):
                cycle.native.authority(cycle.native.record(item, "assignment"), grant)
        await cycle.routine.control(
            "deny",
            subject=item,
            reference="fixture://explicit-denial",
            authorize=lambda _: True,
        )
        with pytest.raises(PermissionError, match="denied"):
            cycle.native.authority(cycle.native.record(item, "assignment"), grant)
        newer = await activate(cycle)
        assert newer != identity
        with pytest.raises(PermissionError, match="changed"):
            cycle.routine.check_reference(grant["reference"])
        with pytest.raises(PermissionError, match="denied"):
            cycle.routine.active(newer, item)
        with pytest.raises(PermissionError, match="operator"):
            await cycle.routine.control(
                "revoke", reference="No consent", authorize=lambda _: False
            )
        await cycle.routine.control(
            "revoke", reference="fixture://stop", authorize=lambda _: True
        )
        with pytest.raises(PermissionError, match="revoked"):
            cycle.routine.active()

    asyncio.run(run())


@pytest.mark.parametrize("exception", sorted(EXCEPTIONS))
def test_exceptional_work_escalates(exception: str) -> None:
    """No task label or ignored prompt makes an exceptional action routine."""
    from scripts.backlog.routine.policy import qualification  # noqa: PLC0415

    value = assessment()
    value[exception] = True
    with pytest.raises(PermissionError, match="escalation"):
        qualification(value)


def test_policy_limits_and_control_integrity(repository: tuple[WorkCycle, str]) -> None:
    """Reject provider drift, over-budget work, unsafe Git and altered records."""
    cycle, item = repository

    async def run() -> None:
        with pytest.raises(PermissionError, match="operator"):
            await cycle.routine.control(
                "activate", policy=policy(), reference="not-consent"
            )
        identity = await activate(cycle)
        await prepare(cycle, item)
        actual = provider()
        actual["idle"] = False
        with pytest.raises(PermissionError, match="provider"):
            await cycle.routine.authorize_native(
                identity, item, assessment=assessment(), provider=actual
            )
        a = cycle.native.record(item, "assignment")
        bad = copy.deepcopy(a)
        bad["task"]["budgets"]["model_calls"] = 99
        with pytest.raises(PermissionError, match="allowance"):
            cycle.routine.eligible(
                policy(),
                "coding",
                {"operation": "authorize-native-maintenance", "assignment": bad},
                provider(),
            )
        bad["task"]["source"] = "src/devtools/agents/sensitive.py"
        with pytest.raises(PermissionError, match="source"):
            cycle.routine.eligible(
                policy(),
                "coding",
                {"operation": "authorize-native-maintenance", "assignment": bad},
                provider(),
            )
        with pytest.raises(PermissionError):
            cycle.routine.approve(
                identity,
                "git",
                {
                    "operation": "git",
                    "argv": ["push", "--force"],
                    "validation_reference": "fixture://passed",
                },
                assessment=assessment(),
            )
        reference = cycle.routine.approve(
            identity,
            "git",
            {
                "operation": "git",
                "argv": ["push", "origin", "main"],
                "validation_reference": "fixture://protected-inputs",
                "git_inputs": {
                    "head": "a" * 40,
                    "index_sha256": "b" * 64,
                    "paths": ["src/devtools/sample.py"],
                },
            },
            assessment=assessment(),
        )
        decision = cycle.routine.check_reference(reference)
        assert decision is not None
        assert decision["policy_version"] == identity
        assert cycle.routine.check_reference("historical-human-reference") is None
        with pytest.raises(PermissionError, match="Malformed"):
            cycle.routine.check_reference("routine-v1:invalid")
        path = cycle.routine.folder / "control-0001.json"
        value = json.loads(path.read_bytes())
        value["policy"]["output_tokens"] += 1
        path.write_text(json.dumps(value), encoding="utf-8")
        with pytest.raises(ValueError, match="identity"):
            cycle.routine.active()

    asyncio.run(run())
    value = policy()
    value["coding"]["model_calls"] = 99
    with pytest.raises(ValueError, match="limits"):
        validate(value)
    value = policy()
    value["git"]["force"] = True
    with pytest.raises(PermissionError):
        validate(value)


def test_revocation_during_model_return_stops_effects(
    repository: tuple[WorkCycle, str],
) -> None:
    """A returned proposal cannot enter its Tool after operator revocation."""
    cycle, item = repository

    class Revoking(Scripted):
        async def send(self, request: Any) -> Any:  # noqa: ANN401 -- fixture override
            response = await super().send(request)
            await cycle.routine.control(
                "revoke",
                reference="fixture://stop-during-call",
                authorize=lambda _: True,
            )
            return response

    async def run() -> None:
        identity = await activate(cycle)
        await prepare(cycle, item)
        grant = await cycle.routine.authorize_native(
            identity,
            item,
            assessment=assessment(),
            provider=provider(),
        )
        model = Revoking("neutral-script-a")
        result = await cycle.native.execute(
            item,
            interaction=model,
            profile="scripted-v1",
            authorize=cycle.routine.callback(grant["reference"]),
        )
        assert result["disposition"] == "BLOCKED"
        assert len(model.requests) == 1
        assert (cycle.root / ".local/backlog/work" / item / "dispatch.json").exists()
        assert not (cycle.root / ".local/backlog/checkout-owner").exists()

    asyncio.run(run())


def test_proposal_denial_and_wrong_grant_reference_are_refused(
    repository: tuple[WorkCycle, str],
) -> None:
    """Bind proposal/task denial and reject another operation's reference."""
    cycle, item = repository

    async def run() -> None:
        identity = await activate(cycle)
        await prepare(cycle, item)
        grant = await cycle.routine.authorize_native(
            identity,
            item,
            assessment=assessment(),
            provider=provider(),
        )
        with pytest.raises(PermissionError, match="mismatched"):
            cycle.routine.check_reference(grant["reference"], kind="host-review")
        with pytest.raises(PermissionError, match="mismatched"):
            cycle.routine.check_reference(grant["reference"], subject="B-9999")
        altered = copy.deepcopy(cycle.native.record(item, "assignment"))
        altered["task"]["objective"] = "Another task"
        assert not cycle.routine.callback(grant["reference"])(
            {
                "operation": "dispatch-native-maintenance",
                "assignment": altered,
                "grant": grant,
            },
        )
        proposal = cycle.intake.approved_item(item)["proposal"]["id"]
        await cycle.routine.control(
            "deny",
            subject=proposal,
            reference="fixture://deny-original-proposal",
            authorize=lambda _: True,
        )
        with pytest.raises(PermissionError, match="denied"):
            cycle.native.authority(cycle.native.record(item, "assignment"), grant)

    asyncio.run(run())

# Copyright (c) 2026
# ruff: noqa: D102, D103, D107, PLR2004, SLF001 -- finite authored authority controls
"""One explicit review continuation, unchanged candidate, exact host/plan consumers."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

import pytest

from devtools.core.time import Duration, Timestamp
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
)
from scripts.backlog.coordinator import git
from scripts.backlog.intake import _digest
from scripts.backlog.native.review.continuation import LEGACY_BATCH_FAILURE
from tests.scripts.backlog.routine.test_authority import activate, assessment, provider
from tests.scripts.backlog.test_native import (
    PUBLIC,
    SOURCE,
    conclusion,
    native_candidate,
    review_response,
    reviewer_policy,
)
from tests.scripts.backlog.test_native import (
    repository as repository,  # noqa: PLC0414 -- maintained tiny-repository fixture
)

if TYPE_CHECKING:
    from pathlib import Path

    from scripts.backlog.work import WorkCycle


class BatchModel:
    """Select two existing read Tools, then a closed grounded conclusion."""

    source = InteractionSource("neutral-review-a")

    def __init__(self) -> None:
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        self.requests.append(request)
        serialized = json.dumps(asdict(request))
        assert "assert module.value()" not in serialized
        assert "withheld.py" not in serialized
        if len(self.requests) == 1:
            return ModelResponse(
                "",
                self.source,
                termination=ModelTermination.TOOL_CALL,
                tool_calls=tuple(
                    ModelToolCall(
                        "read_source",
                        json.dumps({"path": p, "start": 0}),
                        f"read-{n}",
                    )
                    for n, p in enumerate((SOURCE, PUBLIC))
                ),
            )
        assert [m.tool_call_id for m in request.prompt.messages if m.role == "tool"][
            -2:
        ] == [
            "read-0",
            "read-1",
        ]
        value = conclusion()
        value["findings"] = []
        value["evidence"].extend(["read:1", "read:2"])
        return review_response(request, self.source, value)


async def legacy_failure(
    cycle: WorkCycle,
    item: str,
    monkeypatch: pytest.MonkeyPatch,
) -> dict[str, Any]:
    """Reproduce the old host branch only in a tiny authored repository."""
    await native_candidate(cycle, item)
    config = reviewer_policy()
    config["read_paths"] = [SOURCE, PUBLIC]
    await cycle.native.reviewer.prepare(item, reviewer=config)
    path = cycle.native.reviewer.folder(item) / "subject.json"
    packet = json.loads(path.read_bytes())
    packet.pop("sha256")
    packet.pop("completion")
    packet.pop("delivery")
    packet["sha256"] = _digest(packet)
    path.write_text(json.dumps(packet), encoding="utf-8")
    await cycle.native.reviewer.authorize(
        item,
        reference="authored-legacy-review",
        expires=Timestamp.now() + Duration.minutes(5),
        authorize=lambda _: True,
    )

    async def old_batch(*_args: Any, **_kwargs: Any) -> int:  # noqa: ANN401
        raise PermissionError(LEGACY_BATCH_FAILURE.removeprefix("PermissionError: "))

    with monkeypatch.context() as patch:
        patch.setattr("scripts.backlog.native.review.actor.acquire", old_batch)
        proposal = await cycle.native.reviewer.execute(
            item,
            interaction=BatchModel(),
            profile=config["profile"],
            authorize=lambda _: True,
        )
    assert proposal["status"] == "blocked"
    assert proposal["reads"] == 0
    return proposal


def fresh() -> dict[str, Any]:
    config = reviewer_policy()
    config["read_paths"] = [SOURCE, PUBLIC]
    config["independence"]["session"] = "fresh-continuation-session"
    return config


def reseal(path: Path, change: dict[str, Any]) -> dict[str, Any]:
    """Inject closed-boundary faults only into authored fixture records."""
    value: dict[str, Any] = json.loads(path.read_bytes())
    value.pop("sha256")
    value.update(change)
    value["sha256"] = _digest(value)
    path.write_text(json.dumps(value), encoding="utf-8")
    return value


def test_continuation_refusals_and_one_concurrent_claim(
    repository: tuple[WorkCycle, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Refuse judgment retries, uncertainty and source drift; one concurrent claim."""

    async def run() -> None:
        c, item = repository
        version = await activate(c)
        old = await legacy_failure(c, item, monkeypatch)
        owner = c.native.reviewer
        proposal_path = owner.folder(item) / "proposal.json"
        original = proposal_path.read_bytes()
        failures: list[dict[str, Any]] = [
            {"status": "proposed", "conclusion": conclusion("reject"), "error": None},
            {"conclusion": conclusion("insufficient-evidence")},
            {"error": "TimeoutError: unknown model completion"},
            {"reads": 1},
            {"model_calls": 2},
            {"observations": old["observations"][:1]},
            {"dispatch_sha256": "0" * 64},
            {"host_approved": True},
        ]
        for change in failures:
            value = reseal(proposal_path, change)
            with pytest.raises(PermissionError):
                await owner.prepare_continuation(
                    item,
                    previous=value["sha256"],
                    reviewer=fresh(),
                    correction_reference="fixture://batch-fix",
                )
            proposal_path.write_bytes(original)
        for path in (
            c.root / SOURCE,
            c._folder(item) / "worker/final-source.py",
            c.root / PUBLIC,
        ):
            data = path.read_bytes()
            path.write_bytes(data + b"\n# changed\n")
            with pytest.raises(PermissionError):
                await owner.prepare_continuation(
                    item,
                    previous=old["sha256"],
                    reviewer=fresh(),
                    correction_reference="fixture://fix",
                )
            path.write_bytes(data)
        for previous, config, correction in (
            ("0" * 64, fresh(), "fixture://fix"),
            (old["sha256"], reviewer_policy(), "fixture://fix"),
            (old["sha256"], fresh(), ""),
        ):
            with pytest.raises(PermissionError):
                await owner.prepare_continuation(
                    item,
                    previous=previous,
                    reviewer=config,
                    correction_reference=correction,
                )
        outcomes = await asyncio.gather(
            *(
                owner.prepare_continuation(
                    item,
                    previous=old["sha256"],
                    reviewer=fresh(),
                    correction_reference="fixture://batch-fix",
                )
                for _ in range(2)
            ),
            return_exceptions=True,
        )
        assert sum(isinstance(v, dict) for v in outcomes) == 1
        assert sum(isinstance(v, FileExistsError) for v in outcomes) == 1
        packet = next(v for v in outcomes if isinstance(v, dict))
        actor = owner.select(packet["sha256"])
        assert actor.select(None).folder(item) == owner.folder(item)
        with pytest.raises(PermissionError):
            await actor.prepare_continuation(
                item,
                previous=old["sha256"],
                reviewer=fresh(),
                correction_reference="fixture://third",
            )
        with pytest.raises((PermissionError, ValueError)):
            await c.native.diagnostic_reviewer.prepare_continuation(
                item,
                previous=old["sha256"],
                reviewer=fresh(),
                correction_reference="fixture://wrong-purpose",
            )
        grant = await c.routine.authorize_reviewer(
            version,
            item,
            attempt=packet["sha256"],
            assessment=assessment(),
            provider=provider(),
        )
        assert grant["schema"] == "backlog-native-review-authorization-v2"
        expired = Timestamp.from_isoformat(grant["expires_at"]) + Duration.seconds(1)
        model = BatchModel()
        with monkeypatch.context() as patch:
            patch.setattr(Timestamp, "now", classmethod(lambda _cls: expired))
            with pytest.raises(PermissionError):
                await actor.execute(
                    item,
                    interaction=model,
                    profile="review-script-v1",
                    authorize=c.routine.callback(grant["reference"]),
                )
        assert not model.requests
        assert not (actor.folder(item) / "dispatch.json").exists()
        assert proposal_path.read_bytes() == original

    asyncio.run(run())


def test_policy_continuation_to_exact_host_and_plan(
    repository: tuple[WorkCycle, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No console; actual qualified candidate, batch, independent host and plan."""

    async def run() -> None:
        c, item = repository
        version = await activate(c)
        old = await legacy_failure(c, item, monkeypatch)
        owner = c.native.reviewer
        before = {p: p.read_bytes() for p in owner.folder(item).glob("*.json")}
        before.update(
            {
                c._folder(item) / n: (c._folder(item) / n).read_bytes()
                for n in (
                    "assignment.json",
                    "authorization.json",
                    "dispatch.json",
                    "result.json",
                    "candidate.patch",
                    "worker/final-source.py",
                )
            },
        )
        packet = await owner.prepare_continuation(
            item,
            previous=old["sha256"],
            reviewer=fresh(),
            correction_reference="fixture://tested-batch-correction",
        )
        assert packet["schema"] == "backlog-native-review-subject-v2"
        assert packet["subject"] == owner.record(item, "subject")["subject"]
        assert packet["sha256"] != owner.record(item, "subject")["sha256"]
        with pytest.raises(PermissionError):
            await owner.select("0" * 64).current(item)
        actor = owner.select(packet["sha256"])
        with pytest.raises(FileExistsError):
            await owner.prepare_continuation(
                item,
                previous=old["sha256"],
                reviewer=fresh(),
                correction_reference="fixture://another",
            )
        grant = await c.routine.authorize_reviewer(
            version,
            item,
            attempt=packet["sha256"],
            assessment=assessment(),
            provider=provider(),
        )
        model = BatchModel()
        proposal = await actor.execute(
            item,
            interaction=model,
            profile="review-script-v1",
            authorize=c.routine.callback(grant["reference"]),
        )
        assert proposal["status"] == "proposed", proposal
        assert proposal["schema"] == "backlog-native-review-proposal-v2"
        assert proposal["reads"] == 2
        assert proposal["model_calls"] == 2
        with pytest.raises(FileExistsError):
            await actor.execute(
                item,
                interaction=model,
                profile="review-script-v1",
                authorize=c.routine.callback(grant["reference"]),
            )
        with pytest.raises(PermissionError):
            await c.routine.host_review(
                version,
                item,
                proposal=proposal["sha256"],
                accept=True,
                rationale="Wrong default slot",
                assessment=assessment(),
            )
        review = await c.routine.host_review(
            version,
            item,
            attempt=packet["sha256"],
            proposal=proposal["sha256"],
            accept=True,
            rationale="Host inspected task, both disclosures and fixed checks",
            assessment=assessment(),
        )
        assert review["schema"] == "backlog-native-review-v2"
        assert review["review_subject_sha256"] == packet["sha256"]
        assert c.native.candidate(item, review["sha256"])["review"] == review
        await git(c.root, "branch", "main")
        await git(c.root, "push", "origin", "main")
        plan = await c.routine.plan(
            version,
            item,
            review["sha256"],
            {
                "remote": "origin",
                "destination": "main",
                "feature": "feat/continued-reviewed",
                "checkout": str(c.root),
                "additions": [],
                "parent_complete": False,
                "remaining": ["Separate installation/publication authority"],
                "rationale": "Exact continuation proposal and host disposition",
                "validation_seconds": 60,
            },
            assessment=assessment(),
        )
        assert plan["review_subject_sha256"] == packet["sha256"]
        assert plan["accepted_review"] == review["sha256"]
        assert plan["candidate_result"] == c.native.record(item, "result")["sha256"]
        assert not (
            c.integration.folder(item, plan["sha256"]) / "install.json"
        ).exists()
        for change in (
            {"review_subject_sha256": "0" * 64},
            {"schema": "backlog-native-review-v1"},
        ):
            invalid = {k: v for k, v in review.items() if k != "sha256"}
            invalid.update(change)
            invalid["sha256"] = _digest(invalid)
            path = c._folder(item) / ("review-" + invalid["sha256"] + ".json")
            path.write_text(json.dumps(invalid), encoding="utf-8")
            with pytest.raises((PermissionError, ValueError)):
                c.native.candidate(item, invalid["sha256"])
            path.unlink()
        assert all(path.read_bytes() == data for path, data in before.items())
        assert len(model.requests) == 2

    asyncio.run(run())

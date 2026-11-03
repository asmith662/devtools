# Copyright (c) 2026
# ruff: noqa: D102, D107, SLF001, PLR2004, PLR0915 -- finite authored lifecycle scenarios
"""Recover actual historical batch shapes, never replay live dispatches."""

from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path
from typing import TYPE_CHECKING

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
from tests.scripts.backlog.routine.test_authority import activate, assessment, provider
from tests.scripts.backlog.test_native import PUBLIC, SOURCE, conclusion
from tests.scripts.backlog.test_native import (
    repository as repository,  # noqa: PLC0414
)
from tests.scripts.backlog.test_review_continuation import fresh, legacy_failure, reseal

if TYPE_CHECKING:
    from scripts.backlog.work import WorkCycle


def historical_batch(number: int) -> tuple[ModelToolCall, ...]:
    """Authenticate original provider IDs and shape; map only fixture resources."""
    rows = json.loads(
        Path(
            "docs/research/code-audit/native-review-continuation-20261102/native-attempt.json",
        ).read_bytes(),
    )
    row = next(r for r in rows if r["path"].endswith(f"observation-{number:04d}.json"))
    assert hashlib.sha256(row["utf8_text"].encode()).hexdigest() == row["sha256"]
    record = json.loads(row["utf8_text"])
    identity = record.pop("sha256")
    assert _digest(record) == identity
    return tuple(
        ModelToolCall(
            c["name"],
            json.dumps({"path": path, "start": 0}),
            c["provider_call_id"],
        )
        for c, path in zip(
            record["response"]["tool_calls"],
            (SOURCE, PUBLIC),
            strict=True,
        )
    )


class RecoveryModel:
    """Exercise bounded recovery without entering a provider."""

    source = InteractionSource("neutral-review-a")

    def __init__(self, mode: str = "accept", *, historical: bool = False) -> None:
        self.requests: list[ModelRequest] = []
        self.mode, self.historical = mode, historical

    async def send(self, request: ModelRequest) -> ModelResponse:
        self.requests.append(request)
        n = len(self.requests)
        if not self.historical:
            view = json.loads(request.prompt.messages[-1].content)
            assert view["model_calls_remaining_including_this_call"] == 5 - n
            assert view["supplied_source"][1]["complete_text_in_subject"]
        if n <= 2:
            calls = historical_batch(1 if n == 1 else 7)
        elif n == 3:
            feedback = [
                json.loads(m.content)
                for m in request.prompt.messages
                if m.role == "tool"
            ][-2:]
            assert all(
                v["tool_effect_entered"] is False
                and v["acquisitions_remaining"] == 1
                and v["model_calls_remaining"] == 2
                for v in feedback
            )
            assert view["acquisitions_remaining"] == 1
            calls = (
                ModelToolCall(
                    "read_source",
                    json.dumps({"path": SOURCE, "start": 0, "end": 1}),
                    "bounded-third-read",
                ),
            )
        else:
            assert n == 4
            assert not request.tools
            assert view["phase"] == "synthesis"
            assert view["acquisitions_remaining"] == 0
            if self.mode == "tool-final":
                return ModelResponse(
                    "",
                    self.source,
                    termination=ModelTermination.TOOL_CALL,
                    tool_calls=(
                        ModelToolCall(
                            "read_source",
                            json.dumps({"path": SOURCE, "start": 0}),
                            "forbidden-final",
                        ),
                    ),
                )
            value = conclusion(
                self.mode if self.mode == "insufficient-evidence" else "accept",
            )
            value["findings"] = []
            value["evidence"].extend(["read:1", "read:2", "read:3"])
            if self.mode == "insufficient-evidence":
                value["outstanding"] = [
                    "External contract not inspected in this bounded fixture",
                ]
            if self.mode == "malformed":
                value["unsupported"] = True
            return ModelResponse(json.dumps(value), self.source)
        return ModelResponse(
            "",
            self.source,
            termination=ModelTermination.TOOL_CALL,
            tool_calls=calls,
        )


@pytest.mark.parametrize(
    "mode",
    ["accept", "insufficient-evidence", "malformed", "tool-final", "revoked"],
)
def test_historical_budget_recovery_and_exact_attempt(
    repository: tuple[WorkCycle, str],
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
) -> None:
    """Bind a new subject to failed history, then finish within approved limits."""

    async def run() -> None:
        c, item = repository
        first = await legacy_failure(c, item, monkeypatch)
        config = fresh()
        config["budgets"].update(reads=3, model_calls=4)
        second = await c.native.reviewer.prepare_continuation(
            item,
            previous=first["sha256"],
            reviewer=config,
            correction_reference="authored batch fix",
        )
        actor = c.native.reviewer.select(second["sha256"])
        # Materialize the historical v2 policy before it had recoverable feedback.
        path = actor.folder(item) / "subject.json"
        packet = json.loads(path.read_bytes())
        packet.pop("sha256")
        packet.pop("completion")
        packet["sha256"] = _digest(packet)
        path.write_text(json.dumps(packet), encoding="utf-8")
        actor = c.native.reviewer.select(packet["sha256"])
        await actor.authorize(
            item,
            reference="authored historical review",
            expires=Timestamp.now() + Duration.minutes(5),
            authorize=lambda _: True,
        )
        old = await actor.execute(
            item,
            interaction=RecoveryModel(historical=True),
            profile=config["profile"],
            authorize=lambda _: True,
        )
        assert old["model_calls"] == 2
        assert old["reads"] == 2
        assert old["conclusion"] is None
        before = {p: p.read_bytes() for p in c._folder(item).rglob("*") if p.is_file()}
        config["independence"]["session"] = "third-independent-session"
        for fault in (
            {"status": "proposed"},
            {"conclusion": conclusion("reject")},
            {"observations": old["observations"][:-1]},
            {"reads": 1},
            {"error": "unknown"},
        ):
            p = actor.folder(item) / "proposal.json"
            original = p.read_bytes()
            reseal(p, fault)
            with pytest.raises((PermissionError, ValueError)):
                await c.native.reviewer.prepare_continuation(
                    item,
                    attempt=packet["sha256"],
                    previous=old["sha256"],
                    reviewer=config,
                    correction_reference="authored recovery",
                )
            p.write_bytes(original)
        third = await c.native.reviewer.prepare_continuation(
            item,
            attempt=packet["sha256"],
            previous=old["sha256"],
            reviewer=config,
            correction_reference="authored recovery",
        )
        selected = c.native.reviewer.select(third["sha256"])
        assert selected.folder(item).name == third["sha256"]
        assert third["subject"] == second["subject"]
        with pytest.raises(FileExistsError):
            await c.native.reviewer.prepare_continuation(
                item,
                attempt=packet["sha256"],
                previous=old["sha256"],
                reviewer=config,
                correction_reference="authored recovery",
            )
        with pytest.raises(PermissionError):
            await c.native.reviewer.prepare_continuation(
                item,
                attempt=third["sha256"],
                previous=old["sha256"],
                reviewer=config,
                correction_reference="no chaining",
            )
        version = await activate(c)
        grant = await c.routine.authorize_reviewer(
            version,
            item,
            attempt=third["sha256"],
            assessment=assessment(),
            provider=provider(),
        )
        model = RecoveryModel(mode)
        if mode == "revoked":
            await c.routine.control(
                "deny",
                reference="authored denial",
                subject=item,
                authorize=lambda _: True,
            )
            with pytest.raises(PermissionError):
                await selected.execute(
                    item,
                    interaction=model,
                    profile=config["profile"],
                    authorize=c.routine.callback(grant["reference"]),
                )
            assert not model.requests
            return
        grant_path = selected.folder(item) / "authorization.json"
        original_grant = grant_path.read_bytes()
        reseal(grant_path, {"expires_at": str(Timestamp.now() - Duration.seconds(1))})
        with pytest.raises(PermissionError):
            await selected.execute(
                item,
                interaction=model,
                profile=config["profile"],
                authorize=c.routine.callback(grant["reference"]),
            )
        assert not model.requests
        grant_path.write_bytes(original_grant)
        source_path = c.root / SOURCE
        source_bytes = source_path.read_bytes()
        source_path.write_text("def value():\n    return 99\n", encoding="utf-8")
        with pytest.raises(PermissionError):
            await selected.execute(
                item,
                interaction=model,
                profile=config["profile"],
                authorize=c.routine.callback(grant["reference"]),
            )
        source_path.write_bytes(source_bytes)
        assert not model.requests
        proposal = await selected.execute(
            item,
            interaction=model,
            profile=config["profile"],
            authorize=c.routine.callback(grant["reference"]),
        )
        assert len(model.requests) == 4
        assert proposal["reads"] == 3
        assert proposal["status"] == (
            "proposed" if mode in {"accept", "insufficient-evidence"} else "blocked"
        )
        assert all(p.read_bytes() == v for p, v in before.items())
        with pytest.raises(FileExistsError):
            await selected.execute(
                item,
                interaction=model,
                profile=config["profile"],
                authorize=c.routine.callback(grant["reference"]),
            )
        assert len(model.requests) == 4
        if mode == "accept":
            decision = await c.routine.host_review(
                version,
                item,
                attempt=third["sha256"],
                proposal=proposal["sha256"],
                accept=True,
                rationale="Independent authored source/check assessment",
                assessment=assessment(),
            )
            candidate = c.native.candidate(item, decision["sha256"])
            assert candidate["review"]["review_subject_sha256"] == third["sha256"]
            await git(c.root, "branch", "main")
            await git(c.root, "push", "origin", "main")
            plan = await c.routine.plan(
                version,
                item,
                decision["sha256"],
                {
                    "remote": "origin",
                    "destination": "main",
                    "feature": "feat/recovered-review",
                    "checkout": str(c.root),
                    "additions": [],
                    "parent_complete": False,
                    "remaining": ["Separate installation authority"],
                    "rationale": "Exact v3 review after known refusal recovery",
                    "validation_seconds": 60,
                },
                assessment=assessment(),
            )
            assert plan["review_subject_sha256"] == third["sha256"]
            assert plan["accepted_review"] == decision["sha256"]
        else:
            with pytest.raises(PermissionError):
                selected.admit(item, proposal["sha256"], config["actor"], accept=True)
        assert not (selected.folder(item) / "install.json").exists()

    asyncio.run(run())

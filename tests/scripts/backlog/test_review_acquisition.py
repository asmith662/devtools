# Copyright (c) 2026
# ruff: noqa: D102, D107, C901, PLR0912, PLR2004, EM101, TRY003, PLR0915 -- authored boundary controls
"""Read-only batch preflight, exact correlation and partial completion evidence."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import pytest

from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.retrieval import build_source_search_index
from devtools.core.paths import resolve_path
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelToolCall,
    Prompt,
    PromptMessage,
)
from devtools.tools.errors import ToolInputError
from devtools.tools.source import ScopedSourceTool, SourceReadRequest, SourceScope
from scripts.backlog.intake import _digest
from scripts.backlog.native.execution import Capture
from scripts.backlog.native.review.acquisition import (
    ReadBatchRefusalError,
    acquire,
    refusal_feedback,
)
from tests.scripts.backlog.test_native import (
    PUBLIC,
    SOURCE,
    approve_reviewer,
    conclusion,
    native_candidate,
    review_response,
    reviewer_policy,
)
from tests.scripts.backlog.test_native import (
    repository as repository,  # noqa: PLC0414 -- shared authored-repository fixture
)

if TYPE_CHECKING:
    from devtools.context.planning.materialization import ContextDisclosure
    from devtools.context.planning.source import SourceRangeDisclosureOption
    from devtools.tools.source import SourceReadRefusal
    from scripts.backlog.work import WorkCycle


class MemoryCapture(Capture):
    """Keep unit observations in memory; end-to-end tests use the real writer."""

    def __init__(self) -> None:
        self.used, self.maximum = 0, 524288
        self.values: list[dict[str, Any]] = []

    def add(self, kind: str, value: dict[str, Any]) -> None:
        self.values.append({"kind": kind, **value})


def historical_calls() -> tuple[ModelToolCall, ...]:
    """Use actual preserved IDs/arguments without replaying a live interaction."""
    path = Path(
        "docs/research/code-audit/routine-authority-20261102/native-records/reviewer/observation-0001.json",
    )
    record = json.loads(path.read_bytes())
    identity = record.pop("sha256")
    assert identity == _digest(record)
    assert (
        identity == "53b838703666782203e3649bfe256d004bf8c72d22213ea9ce89586a0f20fda6"
    )
    return tuple(ModelToolCall(**c) for c in record["response"]["tool_calls"])


@pytest.mark.parametrize("fault", [None, "prompt", "capture", "calls", "duplicate"])
def test_refusal_feedback_capacity_and_correlation(fault: str | None) -> None:
    """A refusal adds no source authority and cannot exceed remaining capacity."""
    calls = historical_calls()
    response = ModelResponse("", InteractionSource("bounded-review"), tool_calls=calls)
    messages = [PromptMessage("system", "Mandatory instructions")]
    request = ModelRequest(Prompt("", "messages", tuple(messages)))
    capture = MemoryCapture()
    packet: dict[str, Any] = {
        "policy": {
            "read_paths": [],
            "budgets": {
                "model_calls": 4,
                "reads": 3,
                "prompt_bytes": 65536,
                "response_bytes": 1024,
            },
        },
        "subject": {
            "inputs": {},
            "evidence": {
                "baseline": {"path": "source.py", "identity": "baseline"},
                "candidate": {"path": "source.py", "sha256": "candidate"},
            },
        },
    }
    claimed = (
        {cast("str", calls[0].provider_call_id)} if fault == "duplicate" else set()
    )
    if fault == "prompt":
        packet["policy"]["budgets"]["prompt_bytes"] = 1
    if fault == "capture":
        capture.maximum = 1
    if fault:
        with pytest.raises((PermissionError, ValueError)):
            refusal_feedback(
                packet,
                4 if fault == "calls" else 2,
                2,
                response,
                request,
                "batch exceeds remaining one read",
                messages,
                claimed,
                capture,
            )
        assert len(messages) == 1
        return
    refusal_feedback(
        packet,
        2,
        2,
        response,
        request,
        "batch exceeds remaining one read",
        messages,
        claimed,
        capture,
    )
    assert [m.tool_call_id for m in messages if m.role == "tool"] == [
        c.provider_call_id for c in calls
    ]
    assert all(
        json.loads(m.content)["acquisitions_remaining"] == 1
        for m in messages
        if m.role == "tool"
    )
    assert set(claimed) == {c.provider_call_id for c in calls}


@pytest.mark.parametrize(
    "fault",
    [
        None,
        "budget",
        "mixed",
        "foreign",
        "malformed",
        "range",
        "duplicate",
        "missing-id",
        "replay",
        "prompt",
        "capture",
        "stale",
        "unknown-first",
        "unknown-second",
        "revoke-second",
        "changed-result",
        "persist",
    ],
)
@pytest.mark.parametrize("recover", [False, True])
def test_historical_batch_preflight_and_effects(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str | None,
    *,
    recover: bool,
) -> None:
    """Retain authentic batch shape over small authored source, never live refs."""
    calls = historical_calls()
    for call in calls:
        path = tmp_path / json.loads(call.arguments_json)["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes("# café\r\ndef value():\r\n    return 'π'\r\n".encode())
    addresses = tuple(
        RepositoryResourceAddress(json.loads(c.arguments_json)["path"]) for c in calls
    )
    scope = SourceScope.observe(
        root=resolve_path(tmp_path),
        repository=Repository.new(),
        addresses=addresses,
    )
    corpus = realize_repository_text_corpus(
        snapshot=scope.snapshot,
        definition=define_repository_text_corpus(
            discovery=discover_repository_resource_addresses(
                repository=Repository(scope.snapshot.repository_id),
                root=scope.root,
                requested_addresses=addresses,
                maximum_resource_count=2,
                maximum_traversal_entry_count=16,
            ),
            selected_addresses=addresses,
        ),
    )
    index = build_source_search_index(scope.snapshot, corpus=corpus)
    if fault == "mixed":
        calls = (calls[0], replace(calls[1], name="replace_source"))
    if fault == "foreign":
        calls = (
            calls[0],
            replace(calls[1], arguments_json='{"path":"secret.py","start":0}'),
        )
    if fault == "malformed":
        calls = (calls[0], replace(calls[1], arguments_json='{"start":0}'))
    if fault == "range":
        calls = (
            calls[0],
            replace(
                calls[1],
                arguments_json=json.dumps({"path": addresses[1].value, "start": -1}),
            ),
        )
    if fault == "duplicate":
        calls = (
            calls[0],
            replace(calls[1], provider_call_id=calls[0].provider_call_id),
        )
    if fault == "missing-id":
        calls = (calls[0], replace(calls[1], provider_call_id=None))
    response = ModelResponse("", InteractionSource("authored-review"), tool_calls=calls)
    messages = [
        PromptMessage("system", "Read-only; candidate is archived."),
        PromptMessage("user", "Task evidence"),
    ]
    request = ModelRequest(Prompt("", "messages", tuple(messages)))
    capture = MemoryCapture()
    references: dict[str, str] = {}
    budgets = reviewer_policy()["budgets"]
    if fault == "budget":
        budgets["reads"] = 1
    if fault == "prompt":
        budgets["prompt_bytes"] = 100
    if fault == "capture":
        capture.maximum = 4096
    if fault == "stale":
        (tmp_path / addresses[1].value).write_text("changed\n", encoding="utf-8")
    entered = []
    original = ScopedSourceTool.execute

    async def execute(
        tool: ScopedSourceTool,
        argument: SourceRangeDisclosureOption | SourceReadRequest,
    ) -> ContextDisclosure | SourceReadRefusal:
        entered.append(argument)
        if fault == "unknown-first" or (
            fault == "unknown-second" and len(entered) == 2
        ):
            raise OSError("authored uncertain source operation")
        result = await original(tool, argument)
        if fault == "changed-result":
            result = cast("ContextDisclosure", result)
            return replace(
                result,
                items=(replace(result.items[0], text="unpredicted"),),
            )
        return result

    monkeypatch.setattr(ScopedSourceTool, "execute", execute)

    async def guard() -> None:
        if fault == "revoke-second" and entered:
            raise PermissionError("authored revocation")

    if fault == "persist":
        add = capture.add

        def fail(kind: str, value: dict[str, Any]) -> None:
            if kind == "review-read-result":
                raise OSError("authored persistence failure")
            add(kind, value)

        monkeypatch.setattr(capture, "add", fail)
    claimed = {cast("str", calls[0].provider_call_id)} if fault == "replay" else set()

    async def run() -> int:
        return await acquire(
            response,
            request,
            scope=scope,
            index=index,
            reads=0,
            budgets=budgets,
            messages=messages,
            references=references,
            claimed=claimed,
            capture=capture,
            guard=guard,
            recover=recover,
        )

    if fault:
        with pytest.raises(
            (ValueError, PermissionError, OSError, ToolInputError),
        ) as failure:
            asyncio.run(run())
        expected_entries = {
            "unknown-first": 1,
            "unknown-second": 2,
            "revoke-second": 1,
            "changed-result": 1,
            "persist": 1,
        }
        assert len(entered) == expected_entries.get(fault, 0)
        if entered or fault == "stale":
            assert not isinstance(failure.value, ReadBatchRefusalError)
        if not entered:
            assert capture.values[-1]["tool_effect_entered"] is False
            assert not references
        if fault == "unknown-second":
            assert list(references) == ["read:1"]
            assert capture.values[-1]["kind"] == "review-read-unresolved"
            assert capture.values[-1]["completed_acquisitions"] == 1
        return
    assert asyncio.run(run()) == 2
    assert len(entered) == 2
    assert len(messages) == 5
    assert [m.tool_call_id for m in messages[-2:]] == [
        c.provider_call_id for c in calls
    ]
    for value in (v for v in capture.values if v["kind"] == "review-read-result"):
        assert value["identity"] == _digest(value["disclosure"])
        assert "π" in value["disclosure"]["text"]
        assert "\r\n" in value["disclosure"]["text"]
        assert value["disclosure"]["snapshot"] == str(scope.snapshot.id)
    ModelRequest(Prompt("", "messages", tuple(messages)))


@pytest.mark.parametrize("fault", [None, "unknown-second"])
def test_batch_review_to_plan_and_no_consumed_replay(
    repository: tuple[WorkCycle, str],
    monkeypatch: pytest.MonkeyPatch,
    fault: str | None,
) -> None:
    """Actual candidate/read/check/review/host/plan consumers, never live models."""

    async def run() -> None:
        cycle, item = repository
        await native_candidate(cycle, item)
        config = reviewer_policy()
        config["read_paths"] = [SOURCE, PUBLIC]
        await approve_reviewer(cycle, item, config)
        actor = cycle.native.reviewer
        entered = 0
        original = ScopedSourceTool.execute

        async def execute(
            tool: ScopedSourceTool,
            argument: SourceRangeDisclosureOption | SourceReadRequest,
        ) -> ContextDisclosure | SourceReadRefusal:
            nonlocal entered
            entered += 1
            if fault == "unknown-second" and entered == 2:
                raise OSError("authored uncertain second read")
            return await original(tool, argument)

        monkeypatch.setattr(ScopedSourceTool, "execute", execute)

        class Model:
            source = InteractionSource("neutral-review-a")
            calls = 0

            async def send(self, request: ModelRequest) -> ModelResponse:
                self.calls += 1
                if self.calls == 1:
                    return ModelResponse(
                        "",
                        self.source,
                        tool_calls=tuple(
                            ModelToolCall(
                                "read_source",
                                json.dumps({"path": p, "start": 0}),
                                f"batch-{n}",
                            )
                            for n, p in enumerate(config["read_paths"])
                        ),
                    )
                assert [
                    m.tool_call_id for m in request.prompt.messages if m.role == "tool"
                ][-2:] == [
                    "batch-0",
                    "batch-1",
                ]
                assert "assert module.value()" not in json.dumps(
                    asdict(request),
                )
                answer = conclusion()
                answer["findings"] = []
                return review_response(request, self.source, answer)

        model = Model()
        proposal = await actor.execute(
            item,
            interaction=model,
            profile=config["profile"],
            authorize=lambda _: True,
        )
        if fault:
            assert proposal["status"] == "blocked"
            assert proposal["reads"] == 1
            assert proposal["model_calls"] == 1
            assert "uncertain second read" in proposal["error"]
            with pytest.raises(PermissionError):
                await actor.decide(
                    item,
                    proposal=proposal["sha256"],
                    accept=True,
                    reference="fixture://not-authority",
                    rationale="Must refuse",
                    authorize=lambda _: True,
                )
            assert not list(cycle._folder(item).glob("review-*.json"))  # noqa: SLF001
            with pytest.raises(FileExistsError):
                await actor.execute(
                    item,
                    interaction=model,
                    profile=config["profile"],
                    authorize=lambda _: True,
                )
            assert model.calls == 1
            return
        assert proposal["status"] == "proposed", proposal
        assert proposal["reads"] == 2
        assert proposal["model_calls"] == 2
        with pytest.raises(FileExistsError):
            await actor.prepare(item, reviewer=config)
        with pytest.raises(FileExistsError):
            await actor.execute(
                item,
                interaction=model,
                profile=config["profile"],
                authorize=lambda _: True,
            )
        assert model.calls == 2
        with pytest.raises(PermissionError, match="Consumed review slot"):
            await cycle.routine.authorize_reviewer(
                "unused",
                item,
                assessment={},
                provider={},
            )
        review = await actor.decide(
            item,
            proposal=proposal["sha256"],
            accept=True,
            reference="fixture://independent-host",
            rationale="Exact two disclosures and task inspected",
            authorize=lambda _: True,
        )
        plan = await cycle.integration.plan(
            item,
            review["sha256"],
            {
                "remote": "origin",
                "destination": "release",
                "feature": "feat/batch-reviewed",
                "checkout": str(cycle.root),
                "additions": [],
                "parent_complete": False,
                "remaining": ["Separate installation authority"],
                "rationale": "Read-only plan",
                "validation_seconds": 60,
            },
        )
        assert plan["candidate_kind"] == "native-v1"
        assert not (
            cycle.integration.folder(item, plan["sha256"]) / "install.json"
        ).exists()

    asyncio.run(run())

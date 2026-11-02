# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, SLF001, PT018, EM101, TRY003 -- authored historical and authority controls
"""Blocked native history can inform diagnostics, never acceptance or integration."""

from __future__ import annotations

import asyncio
import copy
import hashlib
import json
from typing import TYPE_CHECKING, Any

import pytest

from devtools.core.time import Duration, Timestamp
from devtools.models.interaction import (
    InteractionSource,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
)
from devtools.resources.filesystem import FilesystemError
from scripts.backlog.intake import _digest
from scripts.backlog.native.review.actor import NativeReviewer
from scripts.backlog.native.review.diagnostic import budget_view, parse
from scripts.backlog.work import _load
from tests.scripts.backlog.test_native import (
    BASE,
    PUBLIC,
    SOURCE,
    Scripted,
    edit,
    prepared,
    read_call,
    reviewer_policy,
    task,
)
from tests.scripts.backlog.test_native import (
    repository as repository,  # noqa: PLC0414 -- pytest fixture
)

if TYPE_CHECKING:
    from devtools.models.interaction import ModelRequest
    from scripts.backlog.work import WorkCycle


@pytest.fixture
def failed(repository: tuple[WorkCycle, str]) -> tuple[WorkCycle, str, str]:
    """Produce authentic failed private acceptance in a tiny authored repository."""

    async def run() -> tuple[WorkCycle, str, str]:
        c, item = repository
        packet = task()
        packet["oracle"] = "assert module.value() == 99  # hidden diagnostic sentinel\n"
        await prepared(c, item, packet)
        result = await c.native.execute(
            item,
            interaction=Scripted("neutral-script-a", [read_call(), edit(1, 3, "edit")]),
            profile="scripted-v1",
            authorize=lambda _: True,
        )
        assert (
            result["disposition"] == "BLOCKED"
            and not result["facts"]["acceptance"]["passed"]
        )
        folder = c._folder(item)
        # bytes.decode preserves CRLF; Path.read_text would normalize the witness.
        source = (folder / "worker/final-source.py").read_bytes().decode()
        patch = (folder / "candidate.patch").read_bytes().decode()
        artifact = {
            "source_text": source,
            "candidate_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "native_patch_text": patch,
            "native_patch_sha256": hashlib.sha256(patch.encode()).hexdigest(),
        }
        path = ".local/diagnostic-artifact.json"
        (c.root / path).write_text(json.dumps(artifact), encoding="utf-8")
        return c, item, path

    return asyncio.run(run())


def answer(candidate: str) -> dict[str, Any]:
    return {
        "schema": "native-diagnostic-conclusion-v1",
        "scope": "diagnostic-only",
        "candidate_sha256": candidate,
        "disposition": "findings",
        "summary": "One attributed diagnostic finding, not acceptance.",
        "evidence": ["candidate", "public-checks"],
        "findings": [
            {
                "kind": "inference",
                "message": "Public coverage may not establish the full obligation.",
                "evidence": ["public-checks"],
                "locations": [],
            },
        ],
        "outstanding": ["Unknown private implementation remains withheld"],
        "requests": ["Supervisor may authorize additional independent validation"],
    }


def assert_observation_envelopes(
    reviewer: NativeReviewer,
    item: str,
    proposal: dict[str, Any],
) -> None:
    for reference in proposal["observations"]:
        observation = _load(
            reviewer.folder(item) / reference["file"],
            "backlog-native-observation-v1",
        )
        assert observation["sha256"] == reference["sha256"]
        if observation["kind"] == "review-budget":
            assert observation["budget"]["schema"] == "native-diagnostic-budget-v1"


class DiagnosticModel:
    """Select read-only operations and attributed findings without live inference."""

    def __init__(self, candidate: str, fault: str = "") -> None:
        """Retain requests and one predetermined neutral response behavior."""
        self.source = InteractionSource("neutral-review-a")
        self.candidate, self.fault = candidate, fault
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Assert private controls stay absent and return a scripted operation."""
        self.requests.append(request)
        text = json.dumps(request.prompt.messages[1].content)
        assert (
            "hidden diagnostic sentinel" not in text
            and "module.value() == 99" not in text
        )
        assert request.conversation is None and request.provider_settings is None
        assert {t.name for t in request.tools} == {
            "read_source",
            "find_source",
            "read_source_unit",
        }
        if self.fault == "unknown":
            raise TimeoutError("Provider completion unknown; no replay")
        if self.fault == "malformed":
            return ModelResponse("approved; safe to merge", self.source)
        value = answer(self.candidate)
        if self.fault == "refused":
            value.update(
                disposition="refused",
                findings=[],
                outstanding=["Cannot responsibly diagnose"],
            )
        if self.fault == "unsupported":
            value["findings"][0]["message"] = (
                "The implementation always executes an external shell."
            )
        if self.fault == "output":
            return ModelResponse(
                json.dumps(value),
                self.source,
                termination=ModelTermination.OUTPUT_LIMIT,
            )
        if self.fault in {"edit", "unauthorized"}:
            return ModelResponse(
                "",
                self.source,
                tool_calls=(
                    ModelToolCall(
                        "replace_source" if self.fault == "edit" else "read_source",
                        json.dumps({"path": "secret.py", "start": 0}),
                        "forbidden",
                    ),
                ),
            )
        if len(self.requests) == 1 or self.fault == "calls":
            return ModelResponse(
                "Inspect exact public source independently",
                self.source,
                tool_calls=(
                    ModelToolCall(
                        "read_source",
                        json.dumps({"path": SOURCE, "start": 0}),
                        "current-read",
                    ),
                ),
            )
        return ModelResponse(json.dumps(value), self.source)


async def ready(c: WorkCycle, item: str, archive: str) -> dict[str, Any]:
    config = reviewer_policy()
    config["read_paths"] = [SOURCE]
    reviewer = c.native.diagnostic_reviewer
    packet = await reviewer.prepare(item, reviewer=config, archive=archive)
    await reviewer.authorize(
        item,
        reference="fixture://separate-diagnostic-grant",
        expires=Timestamp.now() + Duration.minutes(5),
        authorize=lambda _: True,
    )
    return packet


def test_blocked_diagnostic_is_read_only_and_not_integration(
    failed: tuple[WorkCycle, str, str],
) -> None:
    async def run() -> None:
        c, item, archive = failed
        before = {p: p.read_bytes() for p in c._folder(item).glob("*.json")}
        with pytest.raises(PermissionError, match="candidate/result/approval"):
            await c.native.reviewer.prepare(item, reviewer=reviewer_policy())
        packet = await ready(c, item, archive)
        assert packet["subject"]["evidence"]["acceptance"]["passed"] is False
        model = DiagnosticModel(packet["subject"]["candidate_sha256"])
        p = await c.native.diagnostic_reviewer.execute(
            item,
            interaction=model,
            profile="review-script-v1",
            authorize=lambda _: True,
        )
        assert (
            p["status"] == "proposed"
            and not p["host_approved"]
            and len(model.requests) == 2
        )
        assert p["schema"] == "backlog-native-diagnostic-proposal-v1"
        with pytest.raises(PermissionError, match="Diagnostic"):
            c.native.diagnostic_reviewer.admit(
                item,
                p["sha256"],
                "reviewer",
                accept=True,
            )
        with pytest.raises(PermissionError, match="Diagnostic"):
            await c.native.diagnostic_reviewer.decide(
                item,
                proposal=p["sha256"],
                accept=True,
                reference="none",
                rationale="none",
                authorize=lambda _: True,
            )
        with pytest.raises((PermissionError, FilesystemError)):
            await c.integration.plan(item, p["sha256"], {})
        assert all(path.read_bytes() == content for path, content in before.items())
        assert (c.root / SOURCE).read_text() == BASE
        assert not list(c._folder(item).glob("review-*.json"))

    asyncio.run(run())


@pytest.mark.parametrize(
    ("calls", "reads", "phase", "remaining"),
    [
        (0, 0, "inspection", 3),
        (1, 1, "inspection", 2),
        (2, 1, "synthesis", 1),
        (1, 2, "synthesis", 2),
    ],
)
def test_remaining_diagnostic_budget(
    calls: int,
    reads: int,
    phase: str,
    remaining: int,
) -> None:
    packet = {
        "policy": reviewer_policy(),
        "subject": {
            "inputs": {SOURCE: "baseline-id", PUBLIC: "other-id"},
            "evidence": {
                "baseline": {"path": SOURCE, "identity": "baseline-id"},
                "candidate": {"path": SOURCE, "sha256": "c" * 64},
            },
        },
    }
    view = budget_view(packet, calls, reads)
    assert view["phase"] == phase
    assert view["model_calls_remaining_including_this_call"] == remaining
    assert view["acquisitions_remaining"] == 2 - reads
    assert view["current_resources"][0]["matches_supplied_baseline"]
    assert not view["current_resources"][1]["matches_supplied_baseline"]
    assert all(s["complete_text_in_subject"] for s in view["supplied_source"])
    with pytest.raises(ValueError, match="exhausted before synthesis"):
        budget_view(packet, 3, reads)


@pytest.mark.parametrize(
    "scenario",
    [
        "finish",
        "insufficient",
        "one-call",
        "early",
        "batch",
        "legacy-total",
        "final-tool",
        "total-tool",
        "final-malformed",
        "final-unsupported",
        "marker",
    ],
)
def test_budgeted_diagnostic_continuation(  # noqa: C901 -- finite lifecycle fault matrix
    failed: tuple[WorkCycle, str, str],
    scenario: str,
) -> None:
    config: dict[str, Any] = {}

    class BudgetModel(DiagnosticModel):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            if scenario == "legacy-total":
                view = None
            else:
                view = json.loads(request.prompt.messages[-1].content)
                assert (
                    view["model_calls_remaining_including_this_call"]
                    == config["budgets"]["model_calls"] - len(self.requests) + 1
                )
                assert bool(request.tools) == view["source_tools_permitted"]
            final = view is not None and view["phase"] == "synthesis"
            if (
                final and scenario not in {"final-tool", "total-tool"}
            ) or scenario == "early":
                assert not request.tools or scenario == "early"
                if scenario == "final-malformed":
                    return ModelResponse("cannot provide JSON", self.source)
                value = answer(self.candidate)
                if scenario == "insufficient":
                    value.update(
                        disposition="insufficient-evidence",
                        findings=[],
                        outstanding=["Dependency behavior not inspected"],
                    )
                if scenario == "final-unsupported":
                    value["findings"][0]["evidence"] = ["hidden-oracle"]
                return ModelResponse(json.dumps(value), self.source)
            call = ModelToolCall(
                "read_source",
                json.dumps({"path": SOURCE, "start": 0}),
                f"read-{len(self.requests)}",
            )
            return ModelResponse(
                "",
                self.source,
                tool_calls=(call, call) if scenario == "batch" else (call,),
            )

    async def run() -> None:
        nonlocal config
        c, item, archive = failed
        config = reviewer_policy()
        config["read_paths"] = [SOURCE]
        if scenario in {"insufficient", "total-tool"}:
            config["budgets"].update(model_calls=4, reads=1)
        if scenario == "one-call":
            config["budgets"]["model_calls"] = 1
        if scenario == "final-tool":
            config["budgets"]["reads"] = 3
        reviewer = c.native.diagnostic_reviewer
        packet = await reviewer.prepare(item, reviewer=config, archive=archive)
        if scenario in {"legacy-total", "marker"}:
            if scenario == "marker":
                packet["continuation"]["reserved_model_calls"] = 2
            else:
                del packet["continuation"]
            packet["sha256"] = _digest(
                {k: v for k, v in packet.items() if k != "sha256"},
            )
            (reviewer.folder(item) / "subject.json").write_text(
                json.dumps(packet),
                encoding="utf-8",
            )
        if scenario == "marker":
            with pytest.raises(PermissionError, match="stale"):
                await reviewer.current(item)
            return
        await reviewer.authorize(
            item,
            reference="fixture://exact-budgeted-grant",
            expires=Timestamp.now() + Duration.minutes(5),
            authorize=lambda _: True,
        )
        model = BudgetModel(packet["subject"]["candidate_sha256"])
        proposal = await reviewer.execute(
            item,
            interaction=model,
            profile=config["profile"],
            authorize=lambda _: True,
        )
        assert len(model.requests) <= config["budgets"]["model_calls"]
        assert proposal["subject_sha256"] == packet["sha256"]
        assert_observation_envelopes(reviewer, item, proposal)
        expected = {
            "batch": "REVIEW_TOOL_BATCH_LIMIT",
            "legacy-total": "REVIEW_ACQUISITION_BUDGET_EXHAUSTED",
            "total-tool": "REVIEW_ACQUISITION_BUDGET_EXHAUSTED",
            "final-tool": "REVIEW_FINALIZATION_TOOLS_UNAVAILABLE",
        }
        if scenario in expected:
            assert expected[scenario] in proposal["error"]
            assert proposal["reads"] == (
                0 if scenario == "batch" else 1 if scenario == "total-tool" else 2
            )
            observations = [
                json.loads((reviewer.folder(item) / x["file"]).read_bytes())
                for x in proposal["observations"]
            ]
            refusal = next(
                o for o in observations if o["kind"] == "review-tool-refused"
            )
            assert refusal["tool_effect_entered"] is False
        else:
            assert proposal["status"] == (
                "blocked" if scenario.startswith("final-") else "proposed"
            ), proposal
        if scenario in {"one-call", "early"}:
            assert proposal["model_calls"] == 1 and proposal["reads"] == 0
        if scenario == "insufficient":
            assert (
                proposal["model_calls"] == 2
                and proposal["conclusion"]["disposition"] == "insufficient-evidence"
            )
        assert not proposal["host_approved"]
        assert c.native.record(item, "result")["disposition"] == "BLOCKED"
        assert (c.root / SOURCE).read_text() == BASE

    asyncio.run(run())


@pytest.mark.parametrize(
    "fault",
    [
        "malformed",
        "output",
        "unknown",
        "edit",
        "unauthorized",
        "calls",
        "refused",
        "unsupported",
    ],
)
def test_diagnostic_model_boundaries(
    failed: tuple[WorkCycle, str, str],
    fault: str,
) -> None:
    async def run() -> None:
        c, item, archive = failed
        packet = await ready(c, item, archive)
        model = DiagnosticModel(packet["subject"]["candidate_sha256"], fault)
        p = await c.native.diagnostic_reviewer.execute(
            item,
            interaction=model,
            profile="review-script-v1",
            authorize=lambda _: True,
        )
        assert p["status"] == (
            "proposed" if fault in {"refused", "unsupported"} else "blocked"
        )
        assert (
            not p["host_approved"]
            and c.native.record(item, "result")["disposition"] == "BLOCKED"
        )
        calls = len(model.requests)
        with pytest.raises((FilesystemError, FileExistsError)):
            await c.native.diagnostic_reviewer.execute(
                item,
                interaction=model,
                profile="review-script-v1",
                authorize=lambda _: True,
            )
        assert len(model.requests) == calls

    asyncio.run(run())


@pytest.mark.parametrize(
    "fault",
    ["candidate", "patch", "baseline", "observation", "release", "ambiguous", "hashes"],
)
def test_diagnostic_historical_tampering(
    failed: tuple[WorkCycle, str, str],
    fault: str,
) -> None:
    async def run() -> None:
        c, item, archive = failed
        if fault in {"ambiguous", "hashes"}:
            p = c.root / archive
            value = json.loads(p.read_bytes())
            if fault == "hashes":
                value["source_sha256"] = "f" * 64
                text = json.dumps(value)
            else:
                text = '{"source_text":"wrong",' + json.dumps(value)[1:]
            p.write_text(text, encoding="utf-8")
        elif fault in {"candidate", "patch"}:
            p = c.root / archive
            v = json.loads(p.read_bytes())
            v["source_text" if fault == "candidate" else "native_patch_text"] += "\n"
            p.write_text(json.dumps(v), encoding="utf-8")
        elif fault == "baseline":
            p = c._folder(item) / "assignment.json"
            v = json.loads(p.read_bytes())
            v["baseline_source"] += "# mismatched identity\n"
            v["sha256"] = _digest({k: x for k, x in v.items() if k != "sha256"})
            p.write_text(json.dumps(v), encoding="utf-8")
        else:
            result = c.native.record(item, "result")
            p = (
                c._folder(item) / "worker" / result["facts"]["observations"][0]["file"]
                if fault == "observation"
                else c.root
                / ".local/backlog/checkout-history"
                / (result["checkout_release"] + ".json")
            )
            p.write_text("{}", encoding="utf-8")
        config = reviewer_policy()
        config["read_paths"] = [SOURCE]
        with pytest.raises((PermissionError, ValueError)):
            await c.native.diagnostic_reviewer.prepare(
                item,
                reviewer=config,
                archive=archive,
            )
        assert not c.native.diagnostic_reviewer.folder(item).exists()

    asyncio.run(run())


def test_missing_historical_input_and_stale_current_source(
    failed: tuple[WorkCycle, str, str],
) -> None:
    async def run() -> None:
        c, item, archive = failed
        (c.root / PUBLIC).unlink()
        packet = await ready(c, item, archive)
        availability = packet["subject"]["evidence"]["availability"]
        assert any(
            p["path"] == PUBLIC and p["status"].startswith("missing")
            for p in availability["historical_inputs"]
        )
        (c.root / SOURCE).write_text(BASE + "# changed now\n", encoding="utf-8")
        with pytest.raises(PermissionError, match="stale"):
            await c.native.diagnostic_reviewer.current(item)

    asyncio.run(run())


def test_navigation_and_unit_acquisition(failed: tuple[WorkCycle, str, str]) -> None:
    class NavigationModel(DiagnosticModel):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            if len(self.requests) == 1:
                call = ModelToolCall(
                    "find_source",
                    json.dumps({"path": SOURCE, "mode": "symbol", "query": "value"}),
                    "find",
                )
            elif len(self.requests) == 2:
                data = json.loads(
                    next(
                        m.content
                        for m in reversed(request.prompt.messages)
                        if m.role == "tool"
                    ),
                )
                unit = data["units"][0]
                call = ModelToolCall(
                    "read_source_unit",
                    json.dumps(
                        {
                            "unit_id": unit["unit_id"],
                            "snapshot_id": data["snapshot_id"],
                        },
                    ),
                    "unit",
                )
            else:
                return ModelResponse(json.dumps(answer(self.candidate)), self.source)
            return ModelResponse("", self.source, tool_calls=(call,))

    async def run() -> None:
        c, item, archive = failed
        packet = await ready(c, item, archive)
        model = NavigationModel(packet["subject"]["candidate_sha256"])
        p = await c.native.diagnostic_reviewer.execute(
            item,
            interaction=model,
            profile="review-script-v1",
            authorize=lambda _: True,
        )
        assert p["status"] == "proposed", p
        assert p["reads"] == 2 and p["references"]["read:2"]

    asyncio.run(run())


@pytest.mark.parametrize(
    "fault",
    ["candidate", "disposition", "scope", "reference", "location", "empty"],
)
def test_diagnostic_conclusion_cannot_accept(fault: str) -> None:
    v = copy.deepcopy(answer("a" * 64))
    refs = dict.fromkeys(v["evidence"], "b" * 64)
    if fault in {"candidate", "disposition", "scope"}:
        v[
            {
                "candidate": "candidate_sha256",
                "disposition": "disposition",
                "scope": "scope",
            }[fault]
        ] = "accept"
    elif fault == "reference":
        v["findings"][0]["evidence"] = ["hidden-oracle"]
    elif fault == "location":
        v["findings"][0]["locations"] = [
            {
                "reference": "public-checks",
                "path": SOURCE,
                "start_line": 0,
                "end_line": 2,
            },
        ]
    else:
        v["findings"] = []
    with pytest.raises(ValueError, match=r"[Dd]iagnostic|[Ii]nvalid"):
        parse(json.dumps(v), refs, "a" * 64)


def test_unknown_effects_and_missing_acceptance_remain_qualified(
    failed: tuple[WorkCycle, str, str],
) -> None:
    """Incomplete recorded effects are diagnostic facts, never eligibility."""

    async def run() -> None:
        c, item, archive = failed
        folder = c._folder(item)
        execution = c.native.record(item, "execution")
        result = c.native.record(item, "result")
        facts = copy.deepcopy(result["facts"])
        facts["effects"][0]["acknowledged"] = False
        facts["acceptance"] = None
        facts["reconciliation_required"] = True
        for name, value in (("execution", execution), ("result", result)):
            value["facts"] = facts
            if name == "result":
                value["execution_sha256"] = execution["sha256"]
            value["sha256"] = _digest({k: v for k, v in value.items() if k != "sha256"})
            (folder / (name + ".json")).write_text(json.dumps(value), encoding="utf-8")
        packet = await ready(c, item, archive)
        evidence = packet["subject"]["evidence"]
        assert evidence["effects"][0]["acknowledged"] is False
        assert evidence["acceptance"] == {"status": "not executed"}
        assert evidence["custody"]["reconciliation_required"] is True
        with pytest.raises(PermissionError, match="candidate/result/approval"):
            await c.native.reviewer.prepare(item, reviewer=reviewer_policy())

    asyncio.run(run())


def test_expired_diagnostic_grant_and_persistence_failure_do_not_replay(
    failed: tuple[WorkCycle, str, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No dispatch follows expired consent; uncertain persistence keeps the claim."""

    async def run() -> None:
        c, item, archive = failed
        packet = await ready(c, item, archive)
        reviewer = c.native.diagnostic_reviewer
        with pytest.raises(PermissionError, match="unexpired"):
            await reviewer.authorize(
                item,
                reference="expired",
                expires=Timestamp.from_isoformat("2000-01-01T00:00:00+00:00"),
                authorize=lambda _: True,
            )
        model = DiagnosticModel(packet["subject"]["candidate_sha256"])
        original = NativeReviewer.save

        def fail_proposal(
            self: NativeReviewer,
            identity: str,
            name: str,
            value: dict[str, Any],
        ) -> dict[str, Any]:
            if name == "proposal":
                raise OSError("Authored diagnostic persistence uncertainty")
            return original(self, identity, name, value)

        monkeypatch.setattr(NativeReviewer, "save", fail_proposal)
        with pytest.raises(OSError, match="persistence"):
            await reviewer.execute(
                item,
                interaction=model,
                profile="review-script-v1",
                authorize=lambda _: True,
            )
        assert (reviewer.folder(item) / "dispatch.json").exists()
        assert not (reviewer.folder(item) / "proposal.json").exists()
        count = len(model.requests)
        with pytest.raises((FilesystemError, FileExistsError)):
            await reviewer.execute(
                item,
                interaction=model,
                profile="review-script-v1",
                authorize=lambda _: True,
            )
        assert len(model.requests) == count

    asyncio.run(run())

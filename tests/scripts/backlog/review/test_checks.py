# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, PLC0414, ANN401 -- deterministic admission controls
"""Source-bound public observations, not a semantic approval oracle."""

from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import ContentIdentity
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelToolCall,
    Prompt,
    PromptMessage,
)
from devtools.resources.commands import Command
from devtools.tools import ToolRunner
from devtools.tools.checks import FixedCheck, FixedCheckPlan, FixedCheckTool
from devtools.tools.source import SourceScope
from scripts.backlog.native.review import checks, delivery
from scripts.backlog.native.review.notes import ReviewNotes
from tests.scripts.backlog.review.test_notes import note, payload, setup
from tests.scripts.backlog.test_native import (
    conclusion,
    native_candidate,
    review_response,
    reviewer_policy,
)
from tests.scripts.backlog.test_native import repository as repository

ROOT = Path(__file__).resolve().parents[4]
CANDIDATE = "tests/context/working/fixtures/p3-candidate.txt"
PROBE = "tests/scripts/backlog/review/public_probe.py"


def observation() -> tuple[dict[str, Any], FixedCheckPlan, Any]:
    scope = SourceScope.observe(
        root=resolve_path(ROOT),
        repository=Repository(RepositoryId.new()),
        addresses=tuple(RepositoryResourceAddress(p) for p in (CANDIDATE, PROBE)),
        maximum_resource_bytes=32768,
    )
    fixed = FixedCheck(
        "public-heading-producer",
        Command(sys.executable)
        .args("-B", "-m", "tests.scripts.backlog.review.public_probe", CANDIDATE)
        .cwd(scope.root)
        .with_timeout(Duration.seconds(15)),
    )
    plan = FixedCheckPlan(scope.root, (fixed,), scope)
    result = asyncio.run(ToolRunner().execute(FixedCheckTool(plan), fixed.name))
    row = checks.observe(
        plan,
        result,
        path=CANDIDATE,
        source="candidate",
        receipt="authenticated-test-result",
    )
    return row, plan, result


def packet(row: dict[str, Any]) -> dict[str, Any]:
    value, _, _ = setup()
    value["subject"]["evidence"]["candidate"]["text"] = (
        (ROOT / CANDIDATE).read_bytes().decode("utf-8")
    )
    value["public_observations"] = {row["name"]: row}
    value["policy"]["budgets"] = {
        "reads": 3,
        "prompt_bytes": 131072,
        "response_bytes": 65536,
    }
    return value


def test_real_fixed_public_observation_distinguishes_empty_heading() -> None:
    row, plan, result = observation()
    assert result.passed
    assert row["version"] == str(
        ContentIdentity.from_text((ROOT / CANDIDATE).read_bytes().decode("utf-8")),
    )
    outputs = json.loads(row["observation"]["stdout"])["outputs"]
    assert outputs[-1] == {"input": "# ##", "observed_title": "##"}
    # Public closing-hash contract requires empty title; execution success is
    # not semantic acceptance. Ordinary attached/closing cases still work.
    assert outputs[-1]["observed_title"] != ""
    assert [r["observed_title"] for r in outputs[:-1]] == ["C#", "C#", "Title"]
    assert checks.validate(packet(row))[row["name"]] == row
    assert len(checks.tools(packet(row))) == 1
    with pytest.raises(ValueError, match="known source-bound"):
        checks.observe(
            replace(plan, source_scope=None),
            result,
            path=CANDIDATE,
            source="candidate",
            receipt="result",
        )
    with pytest.raises(ValueError, match="unknown effects"):
        checks.observe(plan, result, path="other", source="candidate", receipt="result")


@pytest.mark.parametrize(
    "fault",
    ["source", "definition", "output", "identity", "private", "receipt"],
)
def test_stale_unapproved_or_incomplete_observation_refused(fault: str) -> None:
    row, _, _ = observation()
    value = packet(row)
    if fault == "source":
        value["subject"]["evidence"]["candidate"]["text"] += "drift"
    elif fault == "definition":
        row["definition"]["argv"].append("worker-generated")
    elif fault == "output":
        row["observation"]["stdout_truncated"] = True
    elif fault == "identity":
        row["version"] = "wrong"
    elif fault == "private":
        row["source"] = "private-oracle"
    else:
        row["receipt"] = ""
    with pytest.raises(PermissionError, match="differs"):
        checks.validate(value)


def test_correlated_selection_recall_and_isolation() -> None:
    row, _, _ = observation()
    value, snapshot, capture = setup()
    value["public_observations"] = {row["name"]: row}
    # Use the actual candidate source binding for this independent episode.
    value["subject"]["evidence"]["candidate"]["text"] = (
        (ROOT / CANDIDATE).read_bytes().decode("utf-8")
    )
    value["working_notes"] = {"enabled": True}
    value["policy"]["budgets"] = {
        "reads": 3,
        "prompt_bytes": 131072,
        "response_bytes": 65536,
    }
    memory = ReviewNotes(value, snapshot, capture)
    memory.accept(payload(note(support=[])), "model-response:one")
    request = ModelRequest(
        Prompt("", "messages", (PromptMessage("user", "Independent task"),)),
        tools=checks.tools(value),
    )
    messages: list[PromptMessage] = []
    refs: dict[str, str] = {}
    claimed: set[str] = set()
    calls: list[str] = []

    async def guard() -> None:
        calls.append("guard")

    def acquire(name: str, args: dict[str, Any], identity: str = "fresh") -> int:
        response = ModelResponse(
            "",
            InteractionSource("neutral"),
            tool_calls=(ModelToolCall(name, json.dumps(args), identity),),
        )
        return asyncio.run(
            checks.acquire(
                value,
                response,
                request,
                reads=0,
                messages=messages,
                references=refs,
                claimed=claimed,
                capture=capture,
                guard=guard,
                memory=memory,
            ),
        )

    assert acquire(checks.NAME, {"name": row["name"], "version": row["version"]}) == 1
    assert messages[-1].tool_call_id == "fresh"
    assert refs["public-check:" + row["name"]]
    assert acquire(checks.RECALL, {"sequence": 1}, "next") == 1
    recalled = json.loads(messages[-1].content)
    assert recalled["status"] == "provisional"
    assert recalled["scope"] == memory.book.checkpoint()["scope"]
    assert len(calls) == 4
    for name, args, identity in [
        (checks.NAME, {"name": "private", "version": row["version"]}, "unknown"),
        (checks.NAME, {"name": row["name"], "version": "wrong"}, "wrong-version"),
        (checks.NAME, {"name": row["name"], "version": row["version"]}, "fresh"),
        (checks.RECALL, {"sequence": 2}, "unread"),
    ]:
        with pytest.raises((ValueError, PermissionError)):
            acquire(name, args, identity)
    assert len(messages) == 4
    previous = memory.scope
    memory.scope = replace(previous, episode="another-episode")
    with pytest.raises(PermissionError, match="another reviewer"):
        acquire(checks.RECALL, {"sequence": 1}, "cross-episode")
    memory.scope = previous
    value["policy"]["budgets"]["prompt_bytes"] = 1
    with pytest.raises(ValueError, match="fit"):
        acquire(checks.RECALL, {"sequence": 1}, "too-large")
    # Legacy fixtures do not gain Tools or missing structural evidence.
    assert not checks.tools({})
    assert {"acceptance", "custody"}.isdisjoint(refs)
    assert delivery.NAME not in {t.name for t in checks.tools(value)}


def test_native_reviewer_public_observation_and_host_readback(repository: Any) -> None:
    cycle, item = repository

    class Reviewer:
        source = InteractionSource("neutral-review-a")
        calls = 0

        async def send(self, request: ModelRequest) -> ModelResponse:
            self.calls += 1
            if self.calls == 1:
                schema = json.loads(
                    next(
                        t for t in request.tools if t.name == checks.NAME
                    ).input_schema_json,
                )
                return ModelResponse(
                    "",
                    self.source,
                    tool_calls=(
                        ModelToolCall(
                            checks.NAME,
                            json.dumps(
                                {
                                    "name": schema["properties"]["name"]["enum"][0],
                                    "version": schema["properties"]["version"]["enum"][
                                        0
                                    ],
                                },
                            ),
                            "public-read",
                        ),
                    ),
                )
            observed = json.loads(
                next(m.content for m in request.prompt.messages if m.role == "tool"),
            )
            assert observed["observation"]["stdout"].strip() == "3"
            value = conclusion()
            value["evidence"].append("public-check:public-constant")
            return review_response(request, self.source, value)

    async def run() -> None:
        await native_candidate(cycle, item)
        path = (
            (cycle.native.folder(item) / "worker/final-source.py")
            .relative_to(cycle.root)
            .as_posix()
        )
        scope = SourceScope.observe(
            root=resolve_path(cycle.root),
            repository=Repository(RepositoryId.new()),
            addresses=(RepositoryResourceAddress(path),),
            maximum_resource_bytes=32768,
        )
        fixed = FixedCheck(
            "public-constant",
            Command(sys.executable)
            .args(
                "-B",
                "-c",
                "import ast,sys;from pathlib import Path;"
                "p=ast.parse(Path(sys.argv[1]).read_text());"
                "print(ast.literal_eval(p.body[0].body[0].value))",
                path,
            )
            .cwd(scope.root)
            .with_timeout(Duration.seconds(10)),
        )
        plan = FixedCheckPlan(scope.root, (fixed,), scope)
        result = await ToolRunner().execute(FixedCheckTool(plan), fixed.name)
        row = checks.observe(
            plan,
            result,
            path=path,
            source="candidate",
            receipt="fixture://known-public-command",
        )
        await cycle.native.reviewer.prepare(
            item,
            reviewer=reviewer_policy(),
            working_notes=True,
            public_observations={fixed.name: row},
        )
        from devtools.core.time import Timestamp  # noqa: PLC0415

        await cycle.native.reviewer.authorize(
            item,
            reference="fixture://independent-review",
            expires=Timestamp.now() + Duration.minutes(5),
            authorize=lambda _: True,
        )
        model = Reviewer()
        proposal = await cycle.native.reviewer.execute(
            item,
            interaction=model,
            profile="review-script-v1",
            authorize=lambda _: True,
        )
        assert proposal["status"] == "proposed", proposal
        assert proposal["reads"] == 1
        assert model.calls == 2
        assert not proposal["host_approved"]
        # Normal host readback reauthenticates the delivered catalog observation.
        admitted = cycle.native.reviewer.admit(
            item,
            proposal["sha256"],
            "independent-review-actor",
            accept=True,
        )
        assert admitted

    asyncio.run(run())

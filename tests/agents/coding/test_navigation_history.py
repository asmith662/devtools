# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- immutable trace and literal source expectations
"""Frozen churn reconstruction and separate, real-host deterministic fixtures."""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from devtools.agents.coding import CodingLimits, run_coding_agent
from devtools.agents.coding.models import CodingProgress
from devtools.agents.coding.projection import ProjectionCapacityError, request_bytes
from devtools.core.time import Duration
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelSettings,
    ModelToolCall,
    ModelToolDefinition,
    Prompt,
    PromptMessage,
)
from devtools.models.interaction.providers.llama_cpp_request_settings import (
    LlamaCppRequestSettings,
)
from devtools.resources.commands import Command
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from tests.agents.coding.test_navigation import navigation_host
from tests.agents.coding.test_repository import call

CASE = Path(__file__).resolve().parents[3] / "experiments/local_maintenance_cohesion"
PATH = "src/devtools/agents/coding/repository.py"
NAMES = (
    "RepositoryCodingHost.__init__",
    "RepositoryCodingHost.build_request",
    "RepositoryCodingHost.prepare",
)


def test_original_broad_source_cannot_all_fit_and_search_had_coordinates() -> None:
    data = json.loads((CASE / "evidence/result.json").read_text(encoding="utf-8"))
    raw = json.loads((CASE / "evidence/request-8.json").read_text(encoding="utf-8"))[
        "request"
    ]
    messages = tuple(
        PromptMessage(
            **{**m, "tool_calls": tuple(ModelToolCall(**c) for c in m["tool_calls"])},
        )
        for m in data["messages"][:16]
    )
    request = ModelRequest(
        Prompt("", "messages", messages),
        settings=ModelSettings(**raw["settings"]),
        tools=tuple(ModelToolDefinition(**d) for d in raw["tools"]),
        provider_settings=LlamaCppRequestSettings(
            **{k: v for k, v in raw["provider_settings"].items() if k != "provider"},
        ),
    )
    assert request_bytes(request) == 64711
    assert (
        request_bytes(
            replace(
                request,
                prompt=Prompt("", "messages", (messages[0], *messages[6:])),
            ),
        )
        == 52210
    )
    assert (
        request_bytes(
            replace(
                request,
                prompt=Prompt("", "messages", (messages[0], *messages[10:])),
            ),
        )
        == 35067
    )
    hit = next(
        h
        for a in data["acquisitions"]
        if a["kind"] == "retrieval"
        for h in a["result"]["hits"]
        if h["qualified_name"] == "RepositoryCodingHost.build_request"
    )
    assert hit["span"] == [11205, 11747]
    assert hit["path"] == PATH
    for n, span in [(8, [0, 8192]), (9, [8192, 16384]), (10, [16384, 24576])]:
        p = data["projections"][n - 1]
        active = [
            json.loads(m["content"])
            for m in p["request"]["prompt"]["messages"]
            if m["role"] == "tool" and '"text"' in m["content"]
        ]
        assert not any(x["path"] == PATH and x["span"] == span for x in active)
        response = data["requests"][n - 1]["response"]["tool_calls"][0]
        assert json.loads(response["arguments_json"]) == {
            "path": PATH,
            "start": span[0],
            "end": span[1],
        }


class Investigation:
    """Predeclared selection, not evidence that a live model chooses these units."""

    source = InteractionSource("independent-frozen-navigation")

    def __init__(self, *, precise: bool) -> None:
        """Choose exactly one finite deterministic treatment."""
        self.precise = precise
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Consume actual Tool feedback and request the next frozen operation."""
        self.requests.append(request)
        n = len(self.requests)
        calls: tuple[ModelToolCall, ...]
        if not self.precise:
            calls = (
                ()
                if n == 4
                else (
                    call(
                        "read_source",
                        {"path": PATH, "start": 8192 * (n - 1), "end": 8192 * n},
                        f"broad-{n}",
                    ),
                )
            )
        elif n == 1:
            calls = tuple(
                call(
                    "find_source",
                    {"path": PATH, "query": name, "mode": "symbol"},
                    f"find-{i}",
                )
                for i, name in enumerate(NAMES)
            )
        elif n == 2:
            results = [
                json.loads(m.content)
                for m in request.prompt.messages
                if m.role == "tool"
            ]
            assert len(results) == 3
            calls = tuple(
                call(
                    "read_source_unit",
                    {
                        "unit_id": next(
                            u["unit_id"] for u in result["units"] if u["name"] == name
                        ),
                        "snapshot_id": result["snapshot_id"],
                    },
                    f"unit-{i}",
                )
                for i, (name, result) in enumerate(zip(NAMES, results, strict=True))
            )
        else:
            texts = [
                json.loads(m.content)["text"]
                for m in request.prompt.messages
                if m.role == "tool" and '"text"' in m.content
            ]
            assert len(texts) == 3
            assert any("def build_request(" in text for text in texts)
            calls = (
                call(
                    "replace_source",
                    {
                        "path": PATH,
                        "old_text": "return ModelRequest(",
                        "new_text": "# exact navigation witness\r\n"
                        "        return ModelRequest(",
                    },
                    "edit",
                ),
            )
        return ModelResponse("", self.source, tool_calls=calls)


@pytest.mark.parametrize("precise", [False, True])
def test_actual_host_broad_vs_exact_working_set(
    tmp_path: Path,
    *,
    precise: bool,
) -> None:
    frozen = json.loads((CASE / "freeze.json").read_text(encoding="utf-8"))
    original = bytes.fromhex(frozen["baseline_raw"][PATH]).decode()
    host = navigation_host(tmp_path, {PATH: original})
    host.objective = replace(host.objective, text=frozen["objective"])
    host.messages = [PromptMessage("user", frozen["objective"])]
    command = (
        Command(sys.executable)
        .args(
            "-I",
            "-c",
            "from pathlib import Path; assert '# exact navigation witness' "
            f"in Path({PATH!r}).read_text()",
        )
        .cwd(host.scope.root)
        .with_timeout(Duration.seconds(10))
    )
    host.objective = replace(
        host.objective,
        checks=FixedCheckPlan(
            host.scope.root,
            (FixedCheck("literal-witness", command),),
            host.scope,
        ),
    )
    model = Investigation(precise=precise)
    limits = CodingLimits(4, 1, 8, Duration.seconds(10), Duration.seconds(40))
    before = hashlib.sha256((CASE / "freeze.json").read_bytes()).hexdigest()
    result = asyncio.run(run_coding_agent(model, limits=limits, host=host))
    assert hashlib.sha256((CASE / "freeze.json").read_bytes()).hexdigest() == before
    assert (tmp_path / PATH).read_bytes().decode() == original
    assert result.custody.restored
    assert all(request_bytes(q) <= 32768 for q in model.requests)
    assert all(
        q.prompt.messages[0].content == frozen["objective"] for q in model.requests
    )
    if precise:
        assert result.accepted, result.error
        assert len(model.requests) == 3
        # Three exact selected method disclosures remain together before the edit.
        active = host.projection_outcomes[2].active_sources
        assert {o.unit.qualified_name for o in active} == set(NAMES)
        assert sum(len(o.text.encode()) for o in active) < 12000
        assert all(not o.truncated for o in active)
        assert not host.projection_outcomes[2].invalidated_source_identities
        assert host.check_results[0][0].passed
    else:
        assert not result.accepted
        assert len(model.requests) == 4
        assert any(
            x[2] == "source-capacity"
            for x in host.projection_outcomes[-1].omitted_exchanges
        )
        assert host.projection_outcomes[-1].invalidated_source_identities
        assert not host.check_results


def test_impossible_mandatory_source_is_qualified_capacity_failure(
    tmp_path: Path,
) -> None:
    host = navigation_host(
        tmp_path,
        {"module.py": "def answer():\n    return 6\n" + "# fill\n" * 800},
    )
    host.readiness = lambda _snapshot, _available: None
    progress = CodingProgress(
        CodingLimits(3, 1, 3, Duration.seconds(10), Duration.seconds(30)),
    )

    async def prepare() -> None:
        await host.prepare(progress)
        response = ModelResponse(
            "",
            InteractionSource("required"),
            tool_calls=(
                call("read_source", {"path": "module.py", "start": 0}, "read"),
            ),
        )
        host.classify(response)
        await host.acquire(response)
        retained = tuple(host.messages)
        host.objective = replace(host.objective, prompt_bytes=4000)
        assert host.projection is not None
        host.projection = replace(
            host.projection,
            trigger_bytes=3500,
            target_bytes=3000,
        )
        with pytest.raises(ProjectionCapacityError) as raised:
            await host.prepare(progress)
        assert raised.value.outcome.status == "insufficient"
        assert tuple(host.messages) == retained
        assert host.active_disclosures == ()
        assert len(host.source_results) == 1

    asyncio.run(prepare())

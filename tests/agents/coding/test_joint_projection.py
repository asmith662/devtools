# Copyright (c) 2026
# ruff: noqa: D103, SLF001, PLR2004 -- independent host and literal safety assertions
"""Joint disclosure affordability through the neutral coding process."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding import run_coding_agent
from devtools.agents.coding.models import CodingProgress
from devtools.agents.coding.projection import (
    ProjectionCapacityError,
    ProjectionPolicy,
    native_exchange_ranges,
    project_request,
    request_bytes,
    source_feedback,
)
from devtools.agents.coding.repository import RepositoryCodingHost
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.core.paths import resolve_path
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    PromptMessage,
)
from devtools.resources.filesystem import TextFile, write
from devtools.tools import ToolRunner
from devtools.tools.source import ScopedSourceTool
from tests.agents.coding.fixtures import SOURCE
from tests.agents.coding.test_repository import EDIT, LIMITS, Script, call, host_at

if TYPE_CHECKING:
    from pathlib import Path


def fixture(root: Path) -> RepositoryCodingHost:
    initial = host_at(root)
    text = "# padding\n" * 600 + SOURCE
    write(TextFile(resolve_path(root / "module.py"), text))
    scope = initial.scope.observe(
        root=initial.scope.root,
        repository=Repository(initial.scope.snapshot.repository_id),
        addresses=initial.objective.editable,
    )
    plan = replace(
        initial.objective.checks,
        source_scope=scope,
        checks=(
            replace(
                initial.objective.checks.checks[0],
                command=initial.objective.checks.checks[0].command.with_args(
                    "-I",
                    "-c",
                    "from pathlib import Path; ns={}; "
                    "exec(Path('module.py').read_text(),ns); "
                    "assert ns['answer']() == 7; print('checked')",
                ),
            ),
        ),
    )
    return RepositoryCodingHost(
        replace(
            initial.objective,
            scope=scope,
            checks=plan,
            edits=replace(initial.objective.edits, source_bytes=8192),
            disclosure_bytes=8192,
            prompt_bytes=9000,
        ),
        corpus=initial.corpus,
        authorize=initial.authorize,
        apply_changes=initial.effect,
        archive=initial.archive,
        restore=initial.restore,
        projection=ProjectionPolicy(8500, 8000),
    )


async def host_source(host: RepositoryCodingHost, start: int, end: int) -> None:
    unit = host.index.views[0].units[0]
    option = SourceRangeDisclosureOption("Host working set", unit, start, end, 8192)
    disclosure = await ToolRunner().execute(
        ScopedSourceTool(host.scope, maximum_bytes=8192),
        option,
    )
    host.source_results.append(disclosure)
    host.disclosures.append(option)
    host._source_messages[len(host.messages)] = (option,)
    host.messages.append(
        PromptMessage(
            "user",
            json.dumps(
                {
                    **source_feedback(option, disclosure.items[0].text),
                    "restriction": "Only the authorized return value may change.",
                },
            ),
        ),
    )


def test_joint_reduction_continues_through_real_edit_check_and_restoration(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = fixture(tmp_path)
        original = (tmp_path / "module.py").read_bytes()
        await host_source(host, 0, 3000)
        await host_source(host, 3000, 6000)
        host.messages.append(PromptMessage("user", "Never change checks or scope."))
        retained = tuple(host.messages)
        archived: dict[RepositoryResourceAddress, str | None] = {}
        host.archive = archived.update

        class Worker(Script):
            async def send(self, request: object) -> ModelResponse:
                assert isinstance(request, ModelRequest)
                native_exchange_ranges(request.prompt.messages)
                assert request_bytes(request) <= 9000
                if self.entries == 1:
                    outcome = host.projection_outcomes[-1]
                    assert outcome.original_bytes > 13000
                    assert len(outcome.shortened_indices) >= 2
                    assert host.projection is not None
                    for index in (1, 2):
                        single = project_request(
                            host.build_request(tuple(host.messages)),
                            policy=host.projection,
                            hard_bytes=9000,
                            snapshot=host.scope.snapshot,
                            sources=host._source_messages,
                            protected_indices=frozenset(host._source_messages)
                            - {index},
                        )
                        assert single.status == "insufficient"
                        assert single.resulting_bytes > 9000
                    assert outcome.resulting_bytes <= 9000
                    assert retained[-1] in request.prompt.messages
                    for message in request.prompt.messages:
                        if '"restriction"' in message.content:
                            assert json.loads(message.content)["restriction"] == (
                                "Only the authorized return value may change."
                            )
                    assert "return 6" in request.prompt.messages[-1].content
                    assert tuple(host.messages[: len(retained)]) == retained
                return await super().send(request)

        model = Worker(
            [
                (
                    call(
                        "read_source",
                        {"path": "module.py", "start": 0, "end": 3000},
                        "a",
                    ),
                    call(
                        "read_source",
                        {
                            "path": "module.py",
                            "start": 6000,
                            "end": len(original.decode()),
                        },
                        "b",
                    ),
                ),
                (EDIT,),
            ],
        )
        result = await run_coding_agent(model, limits=LIMITS, host=host)
        assert result.accepted, result.error
        assert model.entries == 2
        assert result.progress.actions == 2
        assert all(e.acknowledged for e in result.progress.effects)
        assert len(host.check_results) == 1
        candidate = next(iter(archived.values()))
        assert candidate is not None
        assert "return 7" in candidate
        assert (tmp_path / "module.py").read_bytes() == original
        assert len(host.source_results) >= 4

    asyncio.run(run())


@pytest.mark.parametrize("hard", [2000, 9000])
def test_joint_reduction_failure_or_success_preserves_bound_history(
    tmp_path: Path,
    hard: int,
) -> None:
    async def run() -> None:
        host = fixture(tmp_path)
        for _ in range(3):
            await host_source(host, 0, 3000)
        host.objective = replace(host.objective, prompt_bytes=hard)
        host.projection = ProjectionPolicy(hard, hard)
        original = tuple(host.messages)
        if hard == 2000:
            with pytest.raises(ProjectionCapacityError) as caught:
                await host.prepare(CodingProgress(LIMITS))
            assert caught.value.outcome.status == "insufficient"
            assert caught.value.outcome.shortened_indices == (1, 2, 3)
            assert host.active_disclosures == ()
        else:
            await host.prepare(CodingProgress(LIMITS))
            first = host.projection_outcomes[-1]
            await host.prepare(CodingProgress(LIMITS))
            assert first == host.projection_outcomes[-1]
            assert first.shortened_indices
            assert all(o.span[1] <= 3000 for o in host.active_disclosures)
        assert tuple(host.messages) == original

    asyncio.run(run())


def test_shortened_host_source_does_not_authorize_omitted_anchor(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = fixture(tmp_path)
        await host_source(
            host,
            0,
            len((tmp_path / "module.py").read_text(encoding="utf-8")),
        )
        host.objective = replace(host.objective, prompt_bytes=5000)
        host.projection = ProjectionPolicy(4500, 4000)
        await host.prepare(CodingProgress(LIMITS))
        assert host.projection_outcomes[-1].shortened_indices == (1,)
        assert all("return 6" not in o.text for o in host.active_disclosures)
        response = ModelResponse(
            "edit",
            InteractionSource("neutral"),
            tool_calls=(EDIT,),
        )
        assert host.classify(response) == "edit"
        assert await host.propose(response) is None
        assert "return 6" in (tmp_path / "module.py").read_text()

    asyncio.run(run())


def test_bound_source_does_not_remove_mixed_or_standalone_instructions(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = fixture(tmp_path)
        await host_source(host, 0, 3000)
        value = json.loads(host.messages[-1].content)
        value["instruction"] = "mandatory " * 2000
        host.messages[-1] = replace(host.messages[-1], content=json.dumps(value))
        host.messages.append(PromptMessage("user", "never publish"))
        original = tuple(host.messages)
        with pytest.raises(ProjectionCapacityError) as caught:
            await host.prepare(CodingProgress(LIMITS))
        projected = caught.value.outcome.request.prompt.messages
        assert json.loads(projected[1].content)["instruction"] == value["instruction"]
        assert projected[-1] == original[-1]
        assert tuple(host.messages) == original
        assert host.active_disclosures == ()

    asyncio.run(run())

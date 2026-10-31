# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- literal independent native schedules
"""Task-entry metadata drives the real shared source/edit/check process."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding import CodingLimits, run_coding_agent
from devtools.agents.coding.models import CodingProgress
from devtools.agents.coding.navigation import NavigationPolicy, task_selection
from devtools.agents.coding.projection import ProjectionPolicy, request_bytes
from devtools.agents.coding.repository import RepositoryCodingHost
from devtools.models.interaction import InteractionSource, ModelResponse
from tests.agents.coding.test_navigation import navigation_host
from tests.agents.coding.test_repository import call

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

    from devtools.models.interaction import ModelRequest

from devtools.core.time import Duration


def limits() -> CodingLimits:
    return CodingLimits(7, 2, 8, Duration.seconds(10), Duration.seconds(60))


def candidate_view(request: ModelRequest) -> dict[str, Any]:
    """Locate the candidate view without reserving other host metadata slots."""
    entries = []
    for message in request.prompt.messages:
        try:
            value = json.loads(message.content)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and value.get("kind") == "task_candidates":
            entries.append(value)
    assert len(entries) == 1
    return entries[0]


class Worker:
    """Choose exact source from actual candidate/Tool feedback without app code."""

    source = InteractionSource("task-entry-independent")

    def __init__(self, *, browse: bool = False, read: bool = True) -> None:
        """Select a finite schedule; effects remain in the actual shared host."""
        self.requests: list[ModelRequest] = []
        self.browse = browse
        self.read = read

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Consume candidate metadata and return a separately selected native call."""
        self.requests.append(request)
        n = len(self.requests)
        entry = candidate_view(request)
        assert entry["kind"] == "task_candidates"
        assert entry["complete_inventory"] is False
        assert entry["source_acquired"] is False
        assert "resources" not in entry
        assert request.prompt.messages[0].content.startswith("Make answer")
        assert request_bytes(request) <= 32768
        if self.browse and n <= 3:
            if n == 3:
                assert (
                    json.loads(request.prompt.messages[-1].content)["outline_attempts"]
                    == 2
                )
            selected = call("find_source", {"browse": True}, f"outline-{n}")
        elif self.browse and n == 4:
            result = json.loads(request.prompt.messages[-1].content)
            assert result["reason"] == "outline_allowance_exhausted"
            assert result["navigation_entered"] is False
            selected = call("find_source", {}, "task-default")
        elif self.read and n == (5 if self.browse else 1):
            data = (
                json.loads(request.prompt.messages[-1].content)
                if self.browse
                else entry
            )
            unit = next(u for u in data["units"] if u["name"] == "answer")
            assert unit["span"] == [0, 26]
            selected = call(
                "read_source_unit",
                {
                    "unit_id": unit["unit_id"],
                    "snapshot_id": data["snapshot_id"],
                },
                "exact",
            )
        else:
            if self.read:
                feedback = json.loads(request.prompt.messages[-1].content)
                assert feedback["text"] == "def answer():\n    return 6"
                assert request.prompt.messages[-1].tool_call_id == "exact"
            selected = call(
                "replace_source",
                {
                    "path": "module.py",
                    "old_text": "return 6",
                    "new_text": "return 7",
                },
                f"edit-{n}",
            )
        return ModelResponse("", self.source, tool_calls=(selected,))


@pytest.mark.parametrize("browse", [False, True])
def test_task_entry_to_exact_edit_and_real_check(
    tmp_path: Path,
    *,
    browse: bool,
) -> None:
    host = navigation_host(
        tmp_path,
        {
            "module.py": "def answer():\n    return 6\n",
            "noise.py": "def unrelated():\n    return 'answer documentation'\n",
        },
    )
    host.navigation_policy = NavigationPolicy(outline_actions=2)
    worker = Worker(browse=browse)
    result = asyncio.run(run_coding_agent(worker, limits=limits(), host=host))
    assert result.accepted, result.error
    assert result.custody.restored
    assert result.progress.model_calls == (6 if browse else 2)
    assert result.progress.actions == (5 if browse else 1)
    assert host.check_results[0][0].passed
    assert len(host.source_results) == 2  # selected read, admitted after-image
    assert (tmp_path / "module.py").read_text() == "def answer():\n    return 6\n"
    assert (
        tmp_path / "candidate-module.py"
    ).read_text() == "def answer():\n    return 7\n"
    first = worker.requests[0]
    assert all(m.role == "user" for m in first.prompt.messages)
    entry = candidate_view(first)
    assert any(u["retrieval"][0]["terms"] for u in entry["units"])
    assert not any("return 6" in m.content for m in first.prompt.messages)
    assert all(e.acknowledged for e in result.progress.effects)


def test_candidate_metadata_cannot_authorize_edit(tmp_path: Path) -> None:
    host = navigation_host(tmp_path, {"module.py": "def answer():\n    return 6\n"})
    host.navigation_policy = NavigationPolicy()
    result = asyncio.run(
        run_coding_agent(Worker(read=False), limits=limits(), host=host),
    )
    assert not result.accepted
    assert not host.source_results
    assert not host.check_results
    assert not host.active_disclosures
    assert "not acquired" in host.messages[-1].content


@pytest.mark.parametrize("objective", ["zzqxunmatched", "Make answer return 7"])
def test_generic_and_unmatched_candidate_view(tmp_path: Path, objective: str) -> None:
    host = navigation_host(tmp_path, {"notes π.txt": "answer\r\nsecond\r\n"})
    host.navigation_policy = NavigationPolicy()
    host.objective = replace(host.objective, text=objective)
    host.messages[0] = replace(host.messages[0], content=objective)
    first = asyncio.run(host.prepare(CodingProgress(limits())))
    second = asyncio.run(host.prepare(CodingProgress(limits())))
    assert first == second
    entry = candidate_view(first)
    assert not host.disclosures
    if objective == "zzqxunmatched":
        assert entry["units"] == []
    else:
        assert entry["units"][0]["symbol_fallback"] == "unsupported-language"
        assert entry["units"][0]["path"] == "notes π.txt"


@pytest.mark.parametrize("bound", [1, 600, 1000, 2200])
def test_presentation_budget_and_complete_input(tmp_path: Path, bound: int) -> None:
    host = navigation_host(tmp_path, {"module.py": "def answer():\n    return 6\n"})
    host.navigation_policy = NavigationPolicy(maximum_bytes=bound)
    host.objective = replace(host.objective, prompt_bytes=500)
    host.projection = None
    with pytest.raises(ValueError, match=r"budget|fit"):
        asyncio.run(host.prepare(CodingProgress(limits())))
    assert not host.requests
    assert not host.source_results


@pytest.mark.parametrize(
    "values",
    [{"browse": "yes"}, {"browse": True, "query": "answer"}],
)
def test_ambiguous_selection_refused(values: dict[str, object]) -> None:
    with pytest.raises(ValueError, match="either"):
        task_selection(values, "objective")


def test_long_objective_query_is_explicitly_bounded(tmp_path: Path) -> None:
    host = navigation_host(tmp_path, {"module.py": "def answer():\n    return 6\n"})
    host.navigation_policy = NavigationPolicy()
    host.objective = replace(host.objective, text="answer " * 80)
    request = asyncio.run(host.prepare(CodingProgress(limits())))
    data = candidate_view(request)
    assert data["query_partial"]
    assert data["query"] == host.objective.text[:256]
    assert len(task_selection({}, host.objective.text).query) == 256


def test_candidate_minimum_with_long_query_cannot_fit(tmp_path: Path) -> None:
    host = navigation_host(tmp_path, {"module.py": "def answer():\n    return 6\n"})
    host.navigation_policy = NavigationPolicy(maximum_bytes=850)
    host.objective = replace(host.objective, text="answer " * 80)
    with pytest.raises(ValueError, match="Task candidate metadata cannot fit"):
        asyncio.run(host.prepare(CodingProgress(limits())))
    assert not host.requests


@pytest.mark.parametrize(
    "values",
    [
        {"maximum_candidates": 0},
        {"maximum_bytes": 0},
        {"outline_actions": -1},
        {"outline_actions": True},
    ],
)
def test_invalid_host_policy(values: dict[str, int]) -> None:
    with pytest.raises(ValueError, match="policy requires"):
        NavigationPolicy(**values)


def test_policy_requires_native_navigation(tmp_path: Path) -> None:
    host = navigation_host(tmp_path, {"module.py": "value=1\n"})
    with pytest.raises(ValueError, match="requires native"):
        RepositoryCodingHost(
            host.objective,
            corpus=host.corpus,
            authorize=host.authorize,
            apply_changes=host.effect,
            archive=host.archive,
            restore=host.restore,
            navigation_policy=NavigationPolicy(),
        )


@pytest.mark.parametrize("fault", ["partial", "foreign", "stale", "evicted"])
def test_task_candidate_read_keeps_existing_source_authority(
    tmp_path: Path,
    fault: str,
) -> None:
    host = navigation_host(tmp_path, {"module.py": "def answer():\n    return 6\n"})
    host.navigation_policy = NavigationPolicy()
    state = CodingProgress(limits())

    async def scenario() -> None:
        initial = await host.prepare(state)
        view = candidate_view(initial)
        unit = next(u for u in view["units"] if u["name"] == "answer")
        args = {"unit_id": unit["unit_id"], "snapshot_id": view["snapshot_id"]}
        if fault == "foreign":
            args["unit_id"] = "foreign"
        if fault == "stale":
            args["snapshot_id"] = "old"
        if fault == "partial":
            host.objective = replace(host.objective, disclosure_bytes=7)
        response = ModelResponse(
            "",
            Worker.source,
            tool_calls=(call("read_source_unit", args, "select"),),
        )
        host.classify(response)
        if fault in {"foreign", "stale"}:
            with pytest.raises(ValueError, match="foreign, stale"):
                await host.acquire(response)
            assert not host.disclosures
            return
        await host.acquire(response)
        await host.prepare(state)
        if fault == "partial":
            assert json.loads(host.messages[-1].content)["text"] == "def ans"
            assert host.active_disclosures[0].span == (0, 7)
        else:
            # The mandatory entry fits, but adding the complete source exchange
            # cannot fit this separately selected operational capacity.
            navigation = ModelResponse(
                "",
                Worker.source,
                tool_calls=(call("find_source", {"query": "zzqxunmatched"}, "later"),),
            )
            host.classify(navigation)
            await host.acquire(navigation)
            hard = (
                request_bytes(
                    host.build_request(
                        tuple(
                            host.messages[:3] + host.messages[-2:],
                        ),
                    ),
                )
                + 1
            )
            host.objective = replace(host.objective, prompt_bytes=hard)
            host.projection = ProjectionPolicy(hard, hard - 1)
            await host.prepare(state)
            assert not host.active_disclosures
            assert host.disclosures  # historical acquisition retained
            edit = ModelResponse(
                "",
                Worker.source,
                tool_calls=(
                    call(
                        "replace_source",
                        {
                            "path": "module.py",
                            "old_text": "return 6",
                            "new_text": "return 7",
                        },
                        "no-witness",
                    ),
                ),
            )
            assert await host.propose(edit) is None

    asyncio.run(scenario())

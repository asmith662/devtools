# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- literal independent interaction expectations
"""Active-source metadata informs choices without fabricating agent progress."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding import CodingLimits, run_coding_agent
from devtools.agents.coding.models import CodingProgress
from devtools.agents.coding.projection import (
    ProjectionCapacityError,
    ProjectionPolicy,
    request_bytes,
)
from devtools.context import Repository, RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.models.interaction import InteractionSource, ModelRequest, ModelResponse
from devtools.resources.filesystem import TextFile, write
from tests.agents.coding.test_navigation import navigation_host
from tests.agents.coding.test_projection import acquire, configured
from tests.agents.coding.test_repository import call

if TYPE_CHECKING:
    from pathlib import Path


def status(request: ModelRequest) -> dict[str, object]:
    """Check host information without accepting a synthetic Tool response."""
    message = request.prompt.messages[-1]
    assert message.role == "user"
    assert not message.tool_calls
    assert message.tool_call_id is None
    value: dict[str, object] = json.loads(message.content)
    assert value["kind"] == "active_source_status"
    return value


class ChoosingModel:
    """Choose investigation, duplicate disclosure, then edit or a truthful stop."""

    source = InteractionSource("independent-working-set-consumer")

    def __init__(self, mode: str) -> None:
        """Retain independently selected next actions and actual requests."""
        self.mode = mode
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Choose one action without applying any effect in the double."""
        self.requests.append(request)
        number = len(self.requests)
        state = status(request)
        if number == 1:
            assert state["active_ranges"] == []
            assert state["latest_current_disclosure"] is None
            selected = call("find_source", {"query": "answer"}, "find")
        elif number == 2:
            assert state["active_ranges"] == []  # metadata alone is not a witness
            result = json.loads(request.prompt.messages[-2].content)
            unit = next(u for u in result["units"] if u["name"] == "answer")
            assert unit["span"] == [0, 26]
            selected = call(
                "read_source_unit",
                {"unit_id": unit["unit_id"], "snapshot_id": result["snapshot_id"]},
                "exact",
            )
        else:
            latest = state["latest_current_disclosure"]
            assert isinstance(latest, dict)
            assert latest["span"] == [0, 26]
            assert latest["earlier_same_range_disclosures"] == number - 3
            assert latest["covered_by_one_previous_disclosure"] is (number > 3)
            if number == 3 or self.mode == "repeat":
                selected = call(
                    "read_source",
                    {"path": "module.py", "start": 0, "end": 26},
                    f"chosen-read-{number}",
                )
            elif self.mode == "stop":
                return ModelResponse(
                    "Blocked: need another behavioral obligation.",
                    self.source,
                )
            else:
                selected = call(
                    "replace_source",
                    {
                        "path": "module.py",
                        "old_text": "return 6",
                        "new_text": "return 7",
                    },
                    "chosen-edit",
                )
        return ModelResponse("", self.source, tool_calls=(selected,))


@pytest.mark.parametrize("mode", ["edit", "repeat", "stop"])
def test_model_choices_reach_real_checks_or_honest_noncompletion(
    tmp_path: Path,
    mode: str,
) -> None:
    original = "def answer():\n    return 6\n"
    host = navigation_host(tmp_path, {"module.py": original})
    assert host.projection is not None
    host.projection = replace(host.projection, report_source_state=True)
    model = ChoosingModel(mode)
    result = asyncio.run(
        run_coding_agent(
            model,
            host=host,
            limits=CodingLimits(4, 1, 5, Duration.seconds(10), Duration.seconds(30)),
        ),
    )
    assert len(model.requests) == 4
    assert result.custody.restored
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == original
    assert all("active_source_status" not in m.content for m in host.messages)
    assert len({c.provider_call_id for m in host.messages for c in m.tool_calls}) == (
        3 if mode == "stop" else 4
    )
    if mode == "edit":
        assert result.accepted
        assert host.check_results[0][0].command_result.exit_code == 0
        assert b"checked:7" in host.check_results[0][0].command_result.stdout
        assert (tmp_path / "candidate-module.py").read_text(
            encoding="utf-8",
        ) == original.replace("6", "7")
    else:
        assert not result.accepted
        assert not host.check_results
        assert result.progress.proposals == 0
        assert result.disposition == ("stopped" if mode == "stop" else "model_limit")
        assert len(host.source_results) == (2 if mode == "stop" else 3)


def test_bounded_status_accounts_bytes_and_does_not_claim_all_ranges_listed(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = configured(tmp_path, hard=10000)
        host.progress.limits = replace(host.progress.limits, tool_actions=6)
        assert host.projection is not None
        host.projection = replace(host.projection, report_source_state=True)
        for index in range(6):
            await acquire(host, str(index), index, index + 1)
        original = tuple(host.messages)
        request = await host.prepare(host.progress)
        value = status(request)
        assert value["active_list_partial"] is True
        ranges = value["active_ranges"]
        assert isinstance(ranges, list)
        assert [r["span"] for r in ranges] == [[2, 3], [3, 4], [4, 5], [5, 6]]
        assert len(host.active_disclosures) == 6
        assert value["omitted_current_disclosure_records"] == 0
        assert request_bytes(request) == host.projection_outcomes[-1].resulting_bytes
        assert tuple(host.messages) == original

    asyncio.run(run())


def test_status_overhead_triggers_reduction_and_truthful_partial_availability(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = configured(tmp_path)
        await acquire(host, "first", 0, 7)
        await acquire(host, "second", 7, 29)
        original = tuple(host.messages)
        # The original request fits; enabling the status is also charged.
        before = request_bytes(host.build_request(original))
        host.objective = replace(host.objective, prompt_bytes=before + 500)
        host.projection = ProjectionPolicy(
            before + 400,
            before + 300,
            report_source_state=True,
        )
        request = await host.prepare(host.progress)
        outcome = host.projection_outcomes[-1]
        assert outcome.triggered
        assert outcome.omitted_exchanges == ((1, 3, "source-capacity"),)
        assert status(request)["omitted_current_disclosure_records"] == 1
        assert request_bytes(request) <= before + 500
        assert tuple(host.messages) == original
        await acquire(host, "restored", 0, 7)
        request = await host.prepare(host.progress)
        latest = status(request)["latest_current_disclosure"]
        assert isinstance(latest, dict)
        assert latest["earlier_same_range_disclosures"] == 1
        assert latest["covered_by_one_previous_disclosure"] is False
        assert (0, 7) in [o.span for o in host.active_disclosures]

    asyncio.run(run())


def test_protected_minimum_includes_status_and_failure_keeps_history(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = configured(tmp_path)
        await acquire(host)
        original = tuple(host.messages)
        host.objective = replace(host.objective, prompt_bytes=1000)
        host.projection = ProjectionPolicy(950, 900, report_source_state=True)
        with pytest.raises(ProjectionCapacityError) as caught:
            await host.prepare(host.progress)
        assert caught.value.outcome.resulting_bytes > 1000
        assert tuple(host.messages) == original
        assert host.active_disclosures == ()
        assert host.requests == []
        assert len(host.source_results) == 1

    asyncio.run(run())


def test_invalid_status_policy_is_not_truthy_coerced() -> None:
    with pytest.raises(ValueError, match="policy"):
        ProjectionPolicy(1000, 900, report_source_state=1)  # type: ignore[arg-type]


def test_status_tracks_partial_text_and_changed_snapshot_without_witness_credit(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        text = "# " + "x" * 4000 + "\ndef answer():\n    return 6\n"
        host = navigation_host(tmp_path, {"module.py": text})
        host.objective = replace(host.objective, prompt_bytes=6000)
        host.projection = ProjectionPolicy(5500, 5000, report_source_state=True)
        host.progress = CodingProgress(
            CodingLimits(4, 1, 4, Duration.seconds(5), Duration.seconds(20)),
        )
        await acquire(host, "large", 0, len(text))
        original = tuple(host.messages)
        request = await host.prepare(host.progress)
        outcome = host.projection_outcomes[-1]
        assert outcome.shortened_indices
        feedback = json.loads(request.prompt.messages[-2].content)
        assert feedback["partial"] is True
        assert feedback["text"] == text[: feedback["span"][1]]
        value = status(request)
        ranges = value["active_ranges"]
        assert isinstance(ranges, list)
        assert ranges[0]["span"] == feedback["span"]
        latest = value["latest_current_disclosure"]
        assert isinstance(latest, dict)
        assert latest["span"] == [0, len(text)]
        assert request_bytes(request) <= 6000
        assert tuple(host.messages) == original
        # Full acquisition metadata cannot authorize its omitted tail.
        proposal = ModelResponse(
            "",
            ChoosingModel.source,
            tool_calls=(
                call(
                    "replace_source",
                    {
                        "path": "module.py",
                        "old_text": "return 6",
                        "new_text": "return 7",
                    },
                    "tail-edit",
                ),
            ),
        )
        host.classify(proposal)
        assert await host.propose(proposal) is None
        assert "not acquired" in host.messages[-1].content
        # Refresh the observation after an independently admitted host change.
        write(
            TextFile(
                resolve_path(tmp_path / "module.py"),
                "def answer():\n    return 9\n",
            ),
        )
        host.scope = host.scope.observe(
            root=host.scope.root,
            repository=Repository(host.scope.snapshot.repository_id),
            addresses=(RepositoryResourceAddress("module.py"),),
        )
        host._index()  # noqa: SLF001 -- authorized fixture refresh, not stale-witness reuse
        request = await host.prepare(host.progress)
        assert status(request)["active_ranges"] == []
        assert status(request)["latest_current_disclosure"] is None
        assert host.active_disclosures == ()
        assert len(host.source_results) == 1  # never automatically reread

    asyncio.run(run())

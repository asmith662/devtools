# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- independent literal lifecycle expectations
"""Known range refusals are not unknown Tool effects or source witnesses."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding import run_coding_agent
from devtools.models.interaction import ModelRequest

if TYPE_CHECKING:
    from devtools.models.interaction import ModelResponse
from devtools.tools.source import ScopedSourceTool
from tests.agents.coding import test_repository as fixture_owner
from tests.agents.coding.fixtures import GOOD, SOURCE
from tests.agents.coding.test_repository import EDIT, LIMITS, Script, call, host_at

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context import RepositoryResourceAddress


def test_exact_663_range_failure_recovers_in_shared_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(fixture_owner, "SOURCE", "#" + "x" * 662)
    host = host_at(tmp_path)
    worker = Script(
        [
            (
                call(
                    "read_source",
                    {"path": "module.py", "start": 439, "end": 878},
                    "bad",
                ),
            ),
            (
                call(
                    "read_source",
                    {"path": "module.py", "start": 439, "end": 663},
                    "fixed",
                ),
            ),
            (),
        ],
    )
    result = asyncio.run(run_coding_agent(worker, limits=LIMITS, host=host))
    assert result.disposition == "stopped"
    assert result.error is None
    assert worker.entries == 3
    assert json.loads(host.messages[2].content)["valid_range"] == [0, 663]
    assert json.loads(host.messages[4].content)["text"] == "x" * 224
    assert host.messages[2].tool_call_id == "bad"
    assert host.messages[4].tool_call_id == "fixed"
    assert len(host.source_results) == 1


def test_explicit_null_is_not_omitted_end(tmp_path: Path) -> None:
    host = host_at(tmp_path)
    worker = Script(
        [
            (
                call(
                    "read_source",
                    {"path": "module.py", "start": 0, "end": None},
                    "null",
                ),
            ),
        ],
    )
    result = asyncio.run(run_coding_agent(worker, limits=LIMITS, host=host))
    assert isinstance(result.error, ValueError)
    assert "explicit source end" in str(result.error)
    assert host.source_results == []


@pytest.mark.parametrize("end", [878, 100000, 0, -1])
def test_refused_then_independently_corrected_read_edit_check(
    tmp_path: Path,
    end: int,
) -> None:
    host = host_at(tmp_path)
    archived: dict[RepositoryResourceAddress, str | None] = {}
    host.archive = archived.update
    bad = call("read_source", {"path": "module.py", "start": 0, "end": end}, "bad")
    good = call("read_source", {"path": "module.py", "start": 0}, "corrected")

    class Worker(Script):
        async def send(self, request: object) -> ModelResponse:
            assert isinstance(request, ModelRequest)
            if self.entries == 1:
                message = request.prompt.messages[-1]
                assert message.tool_call_id == "bad"
                value = json.loads(message.content)
                assert value["status"] == "REFUSED"
                assert value["source_disclosure_entered"] is False
                assert value["valid_range"] == [0, len(SOURCE)]
                assert host.disclosures == []
                assert host.source_results == []
                assert host.progress.effects[0].acknowledged
            if self.entries == 2:
                value = json.loads(request.prompt.messages[-1].content)
                assert value["text"] == SOURCE
                assert value["remaining_range"] == [len(SOURCE), len(SOURCE)]
                assert "Unicode offsets" in request.tools[0].description
            return await super().send(request)

    worker = Worker([(bad,), (good,), (EDIT,)])
    result = asyncio.run(run_coding_agent(worker, limits=LIMITS, host=host))
    assert result.accepted
    assert worker.entries == 3
    assert result.progress.actions == 2
    assert result.progress.proposals == 1
    assert list(archived.values()) == [GOOD]
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == SOURCE
    assert [e.native_call_ids for e in result.progress.effects[:2]] == [
        ("bad",),
        ("corrected",),
    ]


@pytest.mark.parametrize(
    "failure",
    [ValueError("late range error"), asyncio.CancelledError()],
)
def test_post_entry_error_is_not_recoverable_range_feedback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: BaseException,
) -> None:
    host = host_at(tmp_path)
    entries = []

    async def execute(_self: object, _request: object) -> None:
        entries.append("entered")
        raise failure

    monkeypatch.setattr(ScopedSourceTool, "execute", execute)
    worker = Script([(call("read_source", {"path": "module.py", "start": 0}, "one"),)])
    result = asyncio.run(run_coding_agent(worker, limits=LIMITS, host=host))
    assert entries == ["entered"]
    assert worker.entries == 1
    assert not result.accepted
    assert result.error is failure
    assert not result.progress.effects[0].acknowledged
    assert not any(m.role == "tool" for m in host.messages)


def test_stale_before_corrected_request_does_not_reauthorize(tmp_path: Path) -> None:
    host = host_at(tmp_path)

    class Worker(Script):
        async def send(self, request: object) -> ModelResponse:
            assert isinstance(request, ModelRequest)
            if self.entries == 1:
                (tmp_path / "module.py").write_text("unknown installed bytes")
            return await super().send(request)

    worker = Worker(
        [
            (
                call(
                    "read_source",
                    {"path": "module.py", "start": 0, "end": 9999},
                    "bad",
                ),
            ),
            (call("read_source", {"path": "module.py", "start": 0}, "retry"),),
        ],
    )
    result = asyncio.run(run_coding_agent(worker, limits=LIMITS, host=host))
    assert result.custody.reconciliation_required
    assert not result.accepted
    assert host.disclosures == []
    assert worker.entries == 2
    assert (tmp_path / "module.py").read_text(
        encoding="utf-8",
    ) == "unknown installed bytes"


def test_refusals_consume_ordinary_action_budget(tmp_path: Path) -> None:
    host = host_at(tmp_path)
    worker = Script(
        [
            (
                call(
                    "read_source",
                    {"path": "module.py", "start": 0, "end": 9999},
                    "bad",
                ),
            ),
            (call("read_source", {"path": "module.py", "start": 0}, "next"),),
            (),
        ],
    )
    result = asyncio.run(
        run_coding_agent(worker, limits=replace(LIMITS, tool_actions=1), host=host),
    )
    assert not result.accepted
    assert result.progress.actions == 1
    assert host.disclosures == []
    assert '"action_budget"' in host.messages[-2].content


def test_refusal_never_supplies_an_edit_witness(tmp_path: Path) -> None:
    host = host_at(tmp_path)
    worker = Script(
        [
            (
                call(
                    "read_source",
                    {"path": "module.py", "start": 0, "end": 9999},
                    "bad",
                ),
            ),
            (EDIT,),
        ],
    )
    result = asyncio.run(
        run_coding_agent(worker, limits=replace(LIMITS, model_calls=2), host=host),
    )
    assert not result.accepted
    assert host.source_results == []
    assert "not acquired" in host.messages[-1].content
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == SOURCE

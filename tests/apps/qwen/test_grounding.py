# Copyright (c) 2026
# ruff: noqa: D103, COM812, PLR2004, F811 -- task-local regression fixtures
"""Source working-set and quality-feedback regressions, never live inference."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, replace
from typing import TYPE_CHECKING

import pytest

from apps.qwen import coding_loop
from apps.qwen.continuation import select_messages
from apps.qwen.tasks import MARKDOWN
from devtools.models.interaction import (
    ModelResponse,
    ModelToolCall,
    Prompt,
    PromptMessage,
)
from tests.apps.qwen.test_coding_loop import GOOD, OLD, Scripted, proposal
from tests.apps.qwen.test_context_tools import (  # noqa: F401
    Investigating,
    call,
    dispatch,
    tools,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from pathlib import Path

    from apps.qwen.context_tools import ContextTools
    from apps.qwen.tasks import CodingTask
    from devtools.models.interaction import ModelRequest


def exchange(identity: str, value: Mapping[str, object]) -> list[PromptMessage]:
    return [
        PromptMessage("assistant", "", (ModelToolCall("read_source", "{}", identity),)),
        PromptMessage("tool", json.dumps(value), tool_call_id=identity),
    ]


def test_tail_multiple_regions_duplicates_and_stale_versions() -> None:
    source = "src/devtools/example.py"
    first = {"path": source, "version": "v1", "span": [0, 1000], "text": "a" * 1000}
    tail = {"path": source, "version": "v1", "span": [9000, 10000], "text": "z" * 1000}
    history = [PromptMessage("user", "objective")]
    history += exchange("prefix", first)
    history += exchange("metadata", {"matches": [{"noise": "n" * 6000}]})
    history += exchange("tail", tail)
    history += exchange("repeat", tail)
    selected, omitted = select_messages(history, maximum_bytes=4300, source_path=source)
    assert omitted == 2
    assert Prompt("", "messages", selected)
    text = json.dumps([asdict(m) for m in selected])
    assert len(text.encode()) <= 4300
    assert text.count("z" * 1000) == 1
    assert "a" * 1000 in text
    assert "original_message_sha256" in text
    assert "retained_tool_call_id" in text
    assert history[-1].content == json.dumps(tail)  # originals immutable
    history += exchange(
        "edit", {"path": source, "version": "v2", "validation": "FAILED"}
    )
    selected, _ = select_messages(history, maximum_bytes=4300)
    assert all(
        "STALE_VERSION" in m.content
        for m in selected
        if m.tool_call_id in {"prefix", "tail"}
    )
    assert "z" * 1000 not in json.dumps([asdict(m) for m in selected])
    with pytest.raises(ValueError, match="budget"):
        select_messages(history[:3], maximum_bytes=100)


def test_capacity_projection_keeps_edit_sources_and_correlated_refusal() -> None:
    history = [PromptMessage("user", "frozen objective and invariants")]
    common = {"repository": "repo", "snapshot": "snapshot", "revision": "head"}
    history += exchange(
        "dependency",
        {
            **common,
            "path": "tests/example.py",
            "version": "t1",
            "span": [0, 100],
            "text": "dependency" * 10,
        },
    )
    for i in range(5):
        history += exchange(
            str(i),
            {
                **common,
                "path": f"src/devtools/{i}.py",
                "version": "v1",
                "span": [0, 4],
                "text": "code",
                "edit_ref": f"R{i}",
            },
        )
    history += exchange(
        "failure",
        {
            "status": "REFUSED",
            "diagnostic": "sixteen components maximum",
            "host_limits": {"proposals_remaining": 2},
        },
    )
    history += exchange(
        "same-failure",
        {
            "status": "REFUSED",
            "diagnostic": "sixteen components maximum",
            "host_limits": {"proposals_remaining": 2},
        },
    )
    original = json.dumps([asdict(m) for m in history])
    selected, omitted = select_messages(
        history, maximum_bytes=131072, compact=True, reacquire=1
    )
    Prompt("", "messages", selected)
    assert omitted == 0
    assert selected[0] == history[0]
    results = {
        m.tool_call_id: json.loads(m.content) for m in selected if m.role == "tool"
    }
    assert "text" not in results["dependency"]
    assert "CAPACITY" in results["dependency"]["source_omitted"]
    assert results["dependency"]["repository"] == "repo"
    for i in range(5):
        assert results[str(i)]["edit_ref"] == f"R{i}"
        assert results[str(i)]["text"] == "code"
        assert results[str(i)]["version"] == "v1"
        assert results[str(i)]["source_envelope_tool_call_id"] == "dependency"
    assert results["failure"]["diagnostic"] == "sixteen components maximum"
    assert results["same-failure"]["same_result_as_tool_call_id"] == "failure"
    assert "proposals_remaining" in selected[1].content
    assert json.dumps([asdict(m) for m in history]) == original


def test_grounding_union_drift_and_actionable_bounds(tools: ContextTools) -> None:
    hit = dispatch(tools, "lookup_symbol", name="helper")["matches"][0]
    args = {"path": hit["path"], "version": hit["version"]}
    result = dispatch(tools, "read_source", **args, start=0, end=9999)
    assert result["error"] == "SOURCE_RANGE_OUT_OF_BOUNDS"
    assert result["source_length"] > 0
    assert not tools.observed("def helper")
    dispatch(tools, "read_source", **args, start=0, end=10)
    dispatch(tools, "read_source", **args, start=10, end=26)
    assert tools.observed("def helper():\n    return 1")
    assert not tools.observed("def helper():\n  return 1")
    original = tools.snapshot.resource_at(tools.addresses[0]).content
    updated = original.replace("return 1", "return 2")
    (tools.root / tools.task.source).write_text(updated, encoding="utf-8", newline="")
    tools.accept_source(updated)
    assert not tools.observed("def helper")
    with pytest.raises(ValueError, match="SOURCE_VERSION_MISMATCH"):
        dispatch(tools, "read_source", **args, start=0, end=10)


def test_quality_failure_is_native_repair_feedback(
    captured_inputs: Callable[[CodingTask], Path], tmp_path: Path
) -> None:
    class QualityRepair(Investigating):
        async def send(self, request: ModelRequest) -> ModelResponse:
            turn = len(self.requests) + 1
            if turn <= 2:
                return await super().send(request)
            self.requests.append(request)
            if turn == 3:
                return proposal(OLD, GOOD)
            result = json.loads(request.prompt.messages[-1].content)
            assert result["validation"]["oracle"]["exit_code"] == 0
            assert result["validation"]["format"]["exit_code"] != 0
            return proposal(
                GOOD,
                "if (\n"
                "                    fence[0] == active_fence[0]\n"
                "                    and len(fence) >= len(active_fence)\n"
                "                    and not line[fence_match.end() :].strip()\n"
                "                ):",
            )

    root = captured_inputs(MARKDOWN)
    task = replace(
        MARKDOWN, context_mode="on-demand", maximum_calls=6, quality_checks=True
    )
    result = asyncio.run(
        coding_loop.run_coding_task(
            root, tmp_path / "quality", QualityRepair([]), task=task
        )
    )
    assert result["accepted"], result
    assert result["repair_cycles"] == 1
    assert result["source_restored"]
    assert not result["turns"][2]["validation"]["accepted"]


def test_legacy_task_identity_and_quality_contract() -> None:
    assert (
        replace(MARKDOWN, quality_checks=False).definition_sha256
        == MARKDOWN.definition_sha256
    )
    assert (
        replace(MARKDOWN, quality_checks=True).definition_sha256
        != MARKDOWN.definition_sha256
    )
    with pytest.raises(ValueError, match="boolean"):
        replace(MARKDOWN, quality_checks="yes")  # type: ignore[arg-type]


def test_range_refusal_recovers_in_same_native_conversation(
    captured_inputs: Callable[[CodingTask], Path], tmp_path: Path
) -> None:

    class RangeRepair(Scripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            turn = len(self.requests)
            if turn == 1:
                native = call("search_source", query="MarkdownFile", mode="file")
            elif turn == 2:
                hit = next(
                    h
                    for h in json.loads(request.prompt.messages[-1].content)["matches"]
                    if h["path"] == MARKDOWN.source
                )
                native = call(
                    "read_source",
                    path=hit["path"],
                    version=hit["version"],
                    start=0,
                    end=20000,
                )
            elif turn == 3:
                result = json.loads(request.prompt.messages[-1].content)
                assert result["error"] == "SOURCE_RANGE_OUT_OF_BOUNDS"
                length = result["source_length"]
                native = call(
                    "read_source",
                    path=result["path"],
                    version=result["version"],
                    start=max(0, length - 4096),
                    end=length,
                )
            else:
                return proposal(OLD, GOOD)
            return ModelResponse("", self.source, tool_calls=(native,))

    root = captured_inputs(MARKDOWN)
    result = asyncio.run(
        coding_loop.run_coding_task(
            root,
            tmp_path / "range-recovery",
            RangeRepair([]),
            task=replace(MARKDOWN, context_mode="on-demand", maximum_calls=4),
        )
    )
    assert result["accepted"], result
    assert result["context_actions_attempted"] == 3
    assert result["context_actions_accepted"] == 2
    assert result["source_restored"]

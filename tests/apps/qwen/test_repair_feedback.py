# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, COM812, SLF001, F811 -- bounded application fixtures
"""Requirement preservation and verified source refresh, no live inference."""

from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen import coding_loop
from apps.qwen.context_tools import ContextTools
from apps.qwen.continuation import select_messages
from apps.qwen.development_task import _timed_command
from apps.qwen.tasks import MARKDOWN
from devtools.models.interaction import ModelToolCall, Prompt, PromptMessage
from scripts.qwen import coding_worker as cli
from tests.apps.qwen.test_context_tools import (  # noqa: F401
    Investigating,
    dispatch,
    tools,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from apps.qwen.tasks import CodingTask
    from devtools.models.interaction import ModelRequest, ModelResponse


def validation(*, typing_failed: bool = False) -> dict[str, Any]:
    return {
        name: {
            "exit_code": 1
            if name == "ruff" or (name == "oracle" and typing_failed)
            else 0,
            "stdout": "QWEN_BEHAVIOR_PASSED\n"
            if name == "oracle"
            else "TRY004 prefer TypeError"
            if name == "ruff"
            else "passed",
            "stderr": "",
        }
        for name in ("oracle", "tests", "ruff", "format")
    }


def test_passing_behavior_is_not_overridden_by_lint_advice() -> None:
    task = replace(
        MARKDOWN, objective="PUBLIC CONTRACT: retain ValueError compatibility."
    )
    original = validation()
    feedback = coding_loop._validation_feedback(
        original, task=task, source_version="exact-v2"
    )
    repair = feedback["repair_contract"]
    assert repair["frozen_requirements"] == task.objective
    assert repair["source_version"] == "exact-v2"
    assert repair["passed_checks"] == ["oracle", "tests", "format"]
    assert repair["failed_checks"] == ["ruff"]
    assert repair["independent_behavior_passed"]
    assert "not permission" in repair["invariants"]
    assert feedback["ruff"]["category"] == "lint"
    assert original == validation()
    assert task.oracle not in json.dumps(feedback)


def test_typing_failure_preserves_already_passing_behavior() -> None:
    feedback = coding_loop._validation_feedback(
        validation(typing_failed=True), task=MARKDOWN, source_version="v"
    )
    assert feedback["oracle"]["category"] == "typing"
    assert feedback["oracle"]["behavior_passed"]
    assert feedback["oracle"]["status"] == "FAIL"
    assert "oracle" in feedback["repair_contract"]["failed_checks"]


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_only_exact_unchanged_observed_regions_refresh(
    tools: ContextTools, *, newline: str
) -> None:
    path = tools.root / tools.task.source
    source = path.read_text(encoding="utf-8").replace("\n", newline)
    path.write_bytes(source.encode())
    tools = ContextTools(tools.root, tools.task)
    hit = dispatch(tools, "lookup_symbol", name="helper")["matches"][0]
    full = dispatch(tools, "expand_source", unit=hit["unit"], to="file")
    read = dispatch(
        tools,
        "read_source",
        path=hit["path"],
        version=hit["version"],
        start=0,
        end=full["span"][1],
    )
    before = tools.snapshot.resource_at(tools.addresses[0]).content
    start = before.index("return 1")
    updated = before[:start] + "return 222" + before[start + len("return 1") :]
    path.write_bytes(updated.encode())
    tools.accept_source(
        updated, replaced_span=(start, start + len("return 1")), edit_call_id="edit-1"
    )
    assert tools.observed("class Demo")
    assert tools.observed("def caller")
    assert not tools.observed("return 1")
    assert not tools.observed("return 222")  # caller separately admits replacement
    for observation in tools.observations:
        assert observation["version"] != read["version"]
        assert observation["text"] == updated[slice(*observation["span"])]
        assert observation["derived_from"]["admitted_edit_call_id"] == "edit-1"
    assert (
        tools.observations[0]["derived_from"]["observation_call_id"] == "fixture-call"
    )


def test_projected_refresh_keeps_native_correlation_without_stale_text() -> None:
    path = "src/devtools/example.py"
    old = {"path": path, "version": "old", "span": [0, 3], "text": "old"}
    current = {
        "path": path,
        "version": "new",
        "text": "edit",
        "span": [0, 4],
        "validation": {"tests": "FAILED"},
        "source_observations": [
            {
                "path": path,
                "version": "new",
                "span": [4, 12],
                "text": "retained",
                "derived_from": {"admitted_edit_call_id": "edit"},
            }
        ],
    }
    history = [PromptMessage("user", "objective")]
    for identity, value in (("read", old), ("edit", current)):
        history += [
            PromptMessage(
                "assistant",
                "",
                (
                    ModelToolCall(
                        "read_source" if identity == "read" else "propose_edit",
                        "{}",
                        identity,
                    ),
                ),
            ),
            PromptMessage("tool", json.dumps(value), tool_call_id=identity),
        ]
    selected, _ = select_messages(history)
    assert Prompt("", "messages", selected)
    assert "STALE_VERSION" in selected[2].content
    assert "retained" in selected[-1].content
    assert history[2].content == json.dumps(old)


def test_native_repair_receives_versioned_contract_and_thinking_setting(
    captured_inputs: Callable[[CodingTask], Path], tmp_path: Path
) -> None:
    class Reviewed(Investigating):
        async def send(self, request: ModelRequest) -> ModelResponse:
            assert request.settings.thinking_enabled is True
            if len(self.requests) == 3:
                result = json.loads(request.prompt.messages[-1].content)
                repair = result["validation"]["repair_contract"]
                assert repair["source_version"] == result["version"]
                assert repair["frozen_requirements"] == MARKDOWN.objective
                assert "oracle" in repair["failed_checks"]
                assert result["source_observations"]
            return await super().send(request)

    root = captured_inputs(MARKDOWN)
    folder = tmp_path / "repair"
    result = asyncio.run(
        coding_loop.run_coding_task(
            root,
            folder,
            Reviewed([]),
            task=replace(MARKDOWN, context_mode="on-demand", maximum_calls=6),
            thinking_enabled=True,
        )
    )
    assert result["accepted"], result
    assert result["repair_cycles"] == 1
    assert result["source_restored"]
    assert (
        json.loads((folder / "freeze.json").read_text(encoding="utf-8"))["settings"][
            "thinking_enabled"
        ]
        is True
    )


def test_invalid_thinking_setting_has_no_source_effect(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="host boolean"):
        asyncio.run(
            coding_loop.run_coding_task(
                tmp_path,
                tmp_path / "unused",
                Investigating([]),
                thinking_enabled="yes",  # type: ignore[arg-type]
            )
        )
    assert not (tmp_path / "unused").exists()


def test_preflight_checks_exact_inputs_without_inference(
    captured_inputs: Callable[[CodingTask], Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = captured_inputs(MARKDOWN)
    actual = _timed_command

    async def command(root: Path, *args: str) -> dict[str, Any]:
        if "mypy" in args:
            return {
                "failed": False,
                "exit_code": 0,
                "stdout": "fixture typing pass",
                "stderr": "",
            }
        return await actual(root, *args)

    monkeypatch.setattr(coding_loop, "_timed_command", command)
    result = asyncio.run(
        coding_loop.preflight_coding_task(root, tmp_path / "preflight", task=MARKDOWN)
    )
    assert result["disposition"] == "PREFLIGHT_CHECKS_PASS_REVIEW_REQUIRED"
    assert result["model_calls"] == 0
    assert not result["satisfiability_proof"]
    assert result["review_required"]
    assert result["validation"]["oracle"]["failed"]
    assert not result["validation"]["tests"]["failed"]


@pytest.mark.parametrize("mode", ["preflight", "thinking"])
def test_cli_preflight_and_explicit_reasoning_are_not_new_approval_gates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, mode: str
) -> None:

    async def preflight(
        _root: Path, _folder: Path, *, task: CodingTask
    ) -> dict[str, Any]:
        assert mode == "preflight"
        assert task == MARKDOWN
        return {"disposition": "PREFLIGHT_CHECKS_PASS_REVIEW_REQUIRED"}

    async def run(_root: Path, _folder: Path, **kwargs: object) -> dict[str, Any]:
        assert mode == "thinking"
        assert kwargs["thinking_enabled"] is True
        return {
            "disposition": "ACCEPTED",
            "accepted": True,
            "turns": [],
            "elapsed_seconds": 0,
        }

    monkeypatch.setattr(cli, "preflight_coding_task", preflight)
    monkeypatch.setattr(cli, "run_local_task", run)
    flags = ["--preflight-only"] if mode == "preflight" else ["--thinking", "enabled"]
    monkeypatch.setattr(
        sys,
        "argv",
        ["coding_worker", "--report-directory", str(tmp_path / "report"), *flags],
    )
    assert asyncio.run(cli.main()) == 0

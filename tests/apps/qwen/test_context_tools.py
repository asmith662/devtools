# Copyright (c) 2026
# ruff: noqa: PLR2004, COM812 -- bounded consumer regression fixtures
"""Actual RI/Context acquisition and native coding continuation, no inference."""

from __future__ import annotations

import asyncio
import hashlib
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen import coding_loop
from apps.qwen.context_tools import ContextTools
from apps.qwen.continuation import select_messages
from apps.qwen.tasks import MARKDOWN, CodingTask
from devtools.models.interaction import (
    ModelRequest,
    ModelResponse,
    ModelToolCall,
    Prompt,
    PromptMessage,
)
from tests.apps.qwen.test_coding_loop import GOOD, OLD, Scripted, proposal

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


def call(operation: str, **arguments: object) -> ModelToolCall:
    """Return a native provider call with untrusted serialized arguments."""
    return ModelToolCall(operation, json.dumps(arguments), "fixture-call")


def dispatch(
    tools: ContextTools, operation: str, **arguments: object
) -> dict[str, Any]:
    """Use real materialization, ToolRunner validation and existing RI operations."""
    return asyncio.run(tools.dispatch(call(operation, **arguments)))


@pytest.fixture
def tools(tmp_path: Path) -> ContextTools:
    """Tiny independently authored source, not a Devtools source-tree copy."""
    source = "src/devtools/demo.py"
    tests = "tests/test_demo.py"
    text = (
        "def helper():\n    return 1\n\n"
        "class Demo:\n    async def method(self):\n        return helper()\n"
        "\ndef caller():\n    return helper()\n"
    )
    for path, content in (
        (source, text),
        (tests, "from devtools.demo import helper\nhelper()\n"),
    ):
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="")
    task = CodingTask(
        "fixture",
        "Inspect demo",
        source,
        (tests,),
        "0" * 40,
        tuple(
            (p, hashlib.sha256((tmp_path / p).read_bytes()).hexdigest())
            for p in (source, tests)
        ),
        ((source, "helper", "symbol", "none"), (tests, "helper", "file", "none")),
        "assert False",
        context_mode="on-demand",
        maximum_calls=6,
    )
    return ContextTools(tmp_path, task)


def test_search_lookup_read_expand_and_relationships(tools: ContextTools) -> None:
    """Native tools preserve exact source units, version and bounded static facts."""
    assert len(tools.definitions) == 5
    found = dispatch(tools, "search_source", query="helper", mode="mixed")
    assert found["matches"]
    matches = dispatch(tools, "lookup_symbol", name="Demo.method")["matches"]
    assert len(matches) == 1
    method = matches[0]
    assert method["kind"] == "symbol"
    enclosing = dispatch(tools, "expand_source", unit=method["unit"], to="class")
    assert enclosing["qualified_name"] == "Demo"
    parent = dispatch(tools, "expand_source", unit=method["unit"], to="symbol")
    assert parent["unit"] == enclosing["unit"]
    full = dispatch(tools, "expand_source", unit=method["unit"], to="file")
    read = dispatch(
        tools,
        "read_source",
        path=method["path"],
        version=method["version"],
        start=method["span"][0],
        end=method["span"][1],
    )
    original = tools.snapshot.resource_at(tools.addresses[0]).content
    assert read["text"] == original[slice(*method["span"])]
    assert read["span"] == method["span"]
    assert not read["truncated"]
    assert read["parent"]["unit"] == full["unit"]
    assert read["parent"]["span"] == full["span"]
    assert read["representation"] == "exact-character-range"
    assert full["span"] == [0, len(original)]
    relations = dispatch(
        tools, "source_relationships", path=method["path"], version=method["version"]
    )
    assert any(r["direct_call"] for r in relations["references"])
    assert relations["assessed"] >= relations["resolved"]
    assert relations["derivation"]


@pytest.mark.parametrize(
    ("name", "arguments"),
    [
        ("shell", {}),
        ("search_source", {"query": "helper", "mode": "embedding"}),
        ("search_source", {"query": "", "mode": "file"}),
        ("search_source", {"query": 1, "mode": "file"}),
        ("search_source", {"query": "helper", "mode": "file", "extra": "x"}),
        ("search_source", []),
        ("read_source", {"path": "../secret", "version": "x", "start": 0, "end": 1}),
        (
            "read_source",
            {"path": "src/devtools/outside.py", "version": "x", "start": 0, "end": 1},
        ),
        (
            "read_source",
            {"path": "src/devtools/demo.py", "version": "stale", "start": 0, "end": 1},
        ),
        (
            "read_source",
            {"path": "src/devtools/demo.py", "version": "x", "start": True, "end": 1},
        ),
        ("expand_source", {"unit": "stale", "to": "file"}),
    ],
)
def test_unauthorized_or_malformed_tools_refuse(
    tools: ContextTools, name: str, arguments: object
) -> None:
    """Disclosure schemas do not grant paths, types, write or shell authority."""
    with pytest.raises((ValueError, TypeError)):
        asyncio.run(tools.dispatch(ModelToolCall(name, json.dumps(arguments), "x")))


def test_source_drift_and_refreshed_unit_identity(tools: ContextTools) -> None:
    """Only exact host-admitted replacement can refresh source applicability."""
    unit = dispatch(tools, "lookup_symbol", name="helper")["matches"][0]
    target = tools.root / tools.task.source
    updated = target.read_text(encoding="utf-8") + "\n# admitted\n"
    target.write_text(updated, encoding="utf-8", newline="")
    with pytest.raises(ValueError, match="SOURCE_DRIFT"):
        dispatch(tools, "lookup_symbol", name="helper")
    with pytest.raises(ValueError, match="SOURCE_DRIFT"):
        tools.accept_source("not admitted")
    tools.accept_source(updated)
    with pytest.raises(ValueError, match="stale"):
        dispatch(tools, "expand_source", unit=unit["unit"], to="file")
    (tools.root / tools.task.tests[0]).write_text("# changed test", encoding="utf-8")
    with pytest.raises(ValueError, match="SOURCE_DRIFT"):
        tools.accept_source(updated)


def test_read_bounds_unicode_truncation_and_invalid_python(tools: ContextTools) -> None:
    """UTF-8-safe truncation and invalid-Python file fallback remain explicit."""
    updated = "# " + "é" * 5000 + "\nthis is not valid python!\n"
    target = tools.root / tools.task.source
    target.write_text(updated, encoding="utf-8", newline="")
    tools.accept_source(updated)
    version = str(tools.snapshot.resource_at(tools.addresses[0]).content_identity)
    result = dispatch(
        tools,
        "read_source",
        path=tools.task.source,
        version=version,
        start=0,
        end=len(updated),
    )
    assert result["truncated"]
    assert result["text"] == updated[slice(*result["span"])]
    assert result["bytes"] <= 4096
    for start, end in ((0, 0), (1, 0), (0, len(updated) + 1)):
        with pytest.raises(ValueError, match="range"):
            dispatch(
                tools,
                "read_source",
                path=tools.task.source,
                version=version,
                start=start,
                end=end,
            )
    relations = dispatch(
        tools, "source_relationships", path=tools.task.source, version=version
    )
    assert relations["status"] == "UNPARSEABLE_PYTHON"
    found = dispatch(tools, "search_source", query="python", mode="symbol")
    assert found["matches"][0]["kind"] == "file"


def test_parent_symbol_absence_is_explicit(tools: ContextTools) -> None:
    """Top-level declarations never invent an enclosing symbol."""
    unit = dispatch(tools, "lookup_symbol", name="helper")["matches"][0]
    with pytest.raises(ValueError, match="no parent"):
        dispatch(tools, "expand_source", unit=unit["unit"], to="symbol")


def test_path_alias_and_oversized_tool_result_refuse(
    tools: ContextTools,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No path aliases or unbounded Tool payload bypass the host boundary."""
    original = tools.root / tools.task.source
    original.unlink()
    external = tmp_path / "other.py"
    external.write_text("value = 1", encoding="utf-8")
    original.symlink_to(external)
    with pytest.raises(ValueError, match="aliases"):
        tools.check_current()
    original.unlink()
    original.write_text(
        tools.snapshot.resource_at(tools.addresses[0]).content,
        encoding="utf-8",
        newline="",
    )

    async def oversized(_arguments: object) -> dict[str, str]:
        return {"text": "x" * 13000}

    monkeypatch.setattr(tools, "execute", oversized)
    with pytest.raises(ValueError, match="byte budget"):
        dispatch(tools, "lookup_symbol", name="helper")


def test_explicit_budget_selection_keeps_complete_recent_exchange() -> None:
    """Pruning is explicit and never separates assistant calls from results."""
    history = [PromptMessage("user", "objective")]
    for number in range(3):
        native = ModelToolCall("read_source", "{}", str(number))
        history += [
            PromptMessage("assistant", "intent", (native,)),
            PromptMessage("tool", "x" * 1000, tool_call_id=str(number)),
        ]
    selected, omitted = select_messages(history, maximum_bytes=2400)
    assert omitted
    assert selected[0] == history[0]
    assert selected[-1] == history[-1]
    assert "omitted" in selected[1].content
    assert Prompt("", "messages", selected)

    assert len(history) == 7  # archived history was not modified
    with pytest.raises(ValueError, match="budget"):
        select_messages(history[:3], maximum_bytes=50)


def test_context_eviction_retains_latest_actual_validation_feedback() -> None:
    """Later read activity cannot evict the latest host test failure/current edit."""
    history = [PromptMessage("user", "objective")]
    for number in range(4):
        native = ModelToolCall(
            "propose_edit" if number == 0 else "read_source", "{}", str(number)
        )
        result = (
            json.dumps({"validation": "TESTS_FAILED", "source_after": "version"})
            if number == 0
            else "x" * 1000
        )
        history += [
            PromptMessage("assistant", "intent", (native,)),
            PromptMessage("tool", result, tool_call_id=str(number)),
        ]
    selected, omitted = select_messages(history, maximum_bytes=2300)
    assert omitted
    assert any("TESTS_FAILED" in m.content for m in selected)
    assert selected[-1] == history[-1]
    assert Prompt("", "messages", selected)
    with pytest.raises(ValueError, match="latest validation"):
        select_messages(history, maximum_bytes=1000)


def test_version_refusal_is_correlated_and_can_be_corrected(
    captured_inputs: Callable[[CodingTask], Path], tmp_path: Path
) -> None:
    """A bad version is refused, not guessed; Qwen receives bounded feedback."""
    root = captured_inputs(MARKDOWN)

    class Recovering(Scripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            number = len(self.requests)
            if number == 1:
                native = call(
                    "read_source",
                    path=MARKDOWN.source,
                    version="CURRENT",
                    start=0,
                    end=10,
                )
            elif number == 2:
                message = request.prompt.messages[-1]
                result = json.loads(message.content)
                assert message.role == "tool"
                assert message.tool_call_id == "fixture-call"
                assert result["status"] == "REFUSED"
                assert result["error"] == "SOURCE_VERSION_MISMATCH"
                assert result["host_limits"]["context_actions_remaining"] == 7
                assert "text" not in result
                native = call("search_source", query="MarkdownFile", mode="file")
            elif number == 3:
                result = json.loads(request.prompt.messages[-1].content)
                hit = next(h for h in result["matches"] if h["path"] == MARKDOWN.source)
                native = call(
                    "read_source",
                    path=hit["path"],
                    version=hit["version"],
                    start=0,
                    end=10,
                )
            else:
                assert "text" in json.loads(request.prompt.messages[-1].content)
                return proposal(OLD, GOOD)
            return ModelResponse("", self.source, tool_calls=(native,))

    model = Recovering([])
    result = asyncio.run(
        coding_loop.run_coding_task(
            root,
            tmp_path / "refusal",
            model,
            task=replace(MARKDOWN, context_mode="on-demand", maximum_calls=4),
        )
    )
    assert result["accepted"]
    assert result["source_restored"]
    assert result["context_actions_attempted"] == 3
    assert result["context_actions_accepted"] == 2
    event = result["turns"][0]["context_tools"][0]
    assert event["status"] == "REFUSED"
    assert event["result"]["status"] == "REFUSED"
    assert len(model.requests) == 4


def test_version_refusals_cannot_expand_action_allowance(
    captured_inputs: Callable[[CodingTask], Path], tmp_path: Path
) -> None:
    """Repeated refusals consume the same eight actions and never acquire source."""
    root = captured_inputs(MARKDOWN)
    native = call(
        "read_source", path=MARKDOWN.source, version="CURRENT", start=0, end=1
    )
    model = Scripted([ModelResponse("", Scripted.source, tool_calls=(native,))] * 9)
    result = asyncio.run(
        coding_loop.run_coding_task(
            root,
            tmp_path / "exhausted",
            model,
            task=replace(MARKDOWN, context_mode="on-demand", maximum_calls=10),
        )
    )
    assert result["disposition"] == "CONTEXT_TOOL_EXECUTION_FAILED"
    assert result["context_actions_attempted"] == 8
    assert result["context_actions_accepted"] == 0
    assert len(model.requests) == 9
    assert [t.name for t in model.requests[-1].tools] == ["propose_edit"]
    assert result["source_restored"]


def test_unmatched_proposal_gets_bounded_no_effect_feedback(
    captured_inputs: Callable[[CodingTask], Path], tmp_path: Path
) -> None:
    """No guessed patch is applied; the same native exchange can correct it."""
    root = captured_inputs(MARKDOWN)

    class Correcting(Scripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            if len(self.requests) == 1:
                return proposal("invented helper that is absent", "replacement")
            message = request.prompt.messages[-1]
            result = json.loads(message.content)
            assert message.role == "tool"
            assert result["error"] == "OLD_TEXT_NOT_UNIQUE"
            assert result["host_limits"]["proposals_remaining"] == 2
            assert OLD in (root / MARKDOWN.source).read_text(encoding="utf-8")
            return proposal(OLD, GOOD)

    model = Correcting([])
    result = asyncio.run(
        coding_loop.run_coding_task(
            root,
            tmp_path / "corrected",
            model,
            task=replace(MARKDOWN, context_mode="on-demand"),
        )
    )
    assert result["accepted"]
    assert result["proposal_refusals"] == 1
    assert result["proposals_attempted"] == 2
    assert result["proposals_admitted"] == 1
    assert result["original_unchanged"]
    assert result["turns"][0]["disposition"] == "PROPOSAL_REFUSED"
    exhausted = Scripted([proposal("absent", "replacement")] * 4)
    result = asyncio.run(
        coding_loop.run_coding_task(
            root,
            tmp_path / "exhausted-proposals",
            exhausted,
            task=replace(MARKDOWN, context_mode="on-demand", maximum_calls=5),
        )
    )
    assert result["disposition"] == "PROPOSAL_ADMISSION_FAILED"
    assert result["proposal_refusals"] == 3
    assert result["proposals_admitted"] == 0
    assert len(exhausted.requests) == 3
    assert result["source_restored"]


def test_selection_retains_current_edit_source_before_search_metadata() -> None:
    """CSV's observed code eviction cannot recur for the pinned prefix/tail."""
    path = "src/devtools/example.py"

    def exchange(identity: str, value: dict[str, Any]) -> list[PromptMessage]:
        return [
            PromptMessage(
                "assistant",
                "",
                tool_calls=(ModelToolCall("read_source", "{}", identity),),
            ),
            PromptMessage("tool", json.dumps(value), tool_call_id=identity),
        ]

    prefix = {"path": path, "version": "a", "text": "prefix" * 200, "span": [0, 1200]}
    tail = {"path": path, "version": "a", "text": "tail" * 200, "span": [1200, 2000]}
    history = [PromptMessage("user", "Task")]
    history += exchange("prefix", prefix)
    history += exchange("search", {"matches": [{"metadata": "x" * 5000}]})
    history += exchange("tail", tail)
    history += exchange("tests", {"path": "tests/example.py", "text": "test" * 200})
    selected, omitted = select_messages(history, maximum_bytes=4500, source_path=path)
    assert omitted == 2
    assert any(m.content == json.dumps(prefix) for m in selected)
    assert any(m.content == json.dumps(tail) for m in selected)
    assert (
        len(json.dumps([{"role": m.role, "content": m.content} for m in selected]))
        < 4500
    )
    assert Prompt("", "messages", selected)
    history += exchange(
        "validation", {"path": path, "version": "b", "validation": "TESTS_FAILED"}
    )
    history += exchange("latest", {"text": "latest" * 200})
    selected, _ = select_messages(history, maximum_bytes=3500, source_path=path)
    assert not any(m.content == json.dumps(prefix) for m in selected)
    assert not any(m.content == json.dumps(tail) for m in selected)
    assert any("TESTS_FAILED" in m.content for m in selected)


class Investigating(Scripted):
    """Script actions using actual earlier Tool results, then propose and repair."""

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Inspect native correlated results before selecting the next scripted call."""
        self.requests.append(request)
        turn = len(self.requests)
        if turn == 1:
            assert "class MarkdownFile" not in request.prompt.messages[0].content
            native = call("search_source", query="MarkdownFile", mode="symbol")
        elif turn == 2:
            result = json.loads(request.prompt.messages[-1].content)
            hit = next(h for h in result["matches"] if h["path"] == MARKDOWN.source)
            native = call(
                "read_source",
                path=hit["path"],
                version=hit["version"],
                start=hit["span"][0],
                end=hit["span"][1],
            )
        else:
            if turn == 3:
                assert "class MarkdownFile" in request.prompt.messages[-1].content
                return proposal(OLD, OLD + " and True")
            assert "TESTS_FAILED" in request.prompt.messages[-1].content
            assert "oracle" in request.prompt.messages[-1].content
            return proposal(OLD + " and True", GOOD)
        return ModelResponse(
            "I will inspect this source.", self.source, tool_calls=(native,)
        )


def test_investigation_then_edit_and_repair_uses_same_worker(
    captured_inputs: Callable[[CodingTask], Path],
    tmp_path: Path,
) -> None:
    """Actual retrieval, native history, proposal application, tests and oracle."""
    root = captured_inputs(MARKDOWN)
    task = replace(MARKDOWN, context_mode="on-demand", maximum_calls=6)
    model = Investigating([])
    result = asyncio.run(
        coding_loop.run_coding_task(root, tmp_path / "run", model, task=task)
    )
    assert result["accepted"], result
    assert result["model_calls_attempted"] == 4
    assert result["context_actions_attempted"] == 2
    assert result["repair_cycles"] == 1
    assert result["original_unchanged"]
    assert result["source_restored"]
    assert result["context_bytes_disclosed"] > 0
    for request in model.requests:
        assert request.prompt.role == "messages"
        assert len(request.tools) == 6
    assert [m.role for m in model.requests[1].prompt.messages] == [
        "user",
        "assistant",
        "tool",
    ]
    assert (tmp_path / "run/turn-04/tools.json").is_file()


@pytest.mark.parametrize(
    ("responses", "disposition"),
    [
        ([proposal(OLD, GOOD)], "ACCEPTED"),
        (
            [ModelResponse("Cannot solve", Scripted.source)],
            "MODEL_COMPLETED_WITHOUT_EDIT",
        ),
        ([RuntimeError("provider unavailable")], "MODEL_REQUEST_FAILED"),
        (
            [
                ModelResponse(
                    "",
                    Scripted.source,
                    tool_calls=(
                        call(
                            "read_source", path="../secret", version="x", start=0, end=1
                        ),
                    ),
                )
            ],
            "CONTEXT_TOOL_EXECUTION_FAILED",
        ),
        (
            [
                ModelResponse(
                    "",
                    Scripted.source,
                    tool_calls=(call("search_source", query="headings", mode="file"),),
                )
            ],
            "MODEL_CALL_BUDGET_EXHAUSTED",
        ),
    ],
)
def test_dynamic_terminal_outcomes_without_extra_calls(
    captured_inputs: Callable[[CodingTask], Path],
    tmp_path: Path,
    responses: list[ModelResponse | Exception],
    disposition: str,
) -> None:
    """No unnecessary calls, fallback, hidden retry or unauthorized source effects."""
    root = captured_inputs(MARKDOWN)
    model = Scripted(responses)
    result = asyncio.run(
        coding_loop.run_coding_task(
            root,
            tmp_path / "run",
            model,
            task=replace(MARKDOWN, context_mode="on-demand"),
            maximum_calls=1,
        )
    )
    assert result["disposition"] == disposition, result
    assert len(model.requests) == 1
    assert result["original_unchanged"]


def test_dynamic_repair_and_action_bounds_stop_before_extra_effects(
    captured_inputs: Callable[[CodingTask], Path],
    tmp_path: Path,
) -> None:
    """Three proposals or eight read actions never become unlimited model repair."""
    root = captured_inputs(MARKDOWN)
    task = replace(MARKDOWN, context_mode="on-demand", maximum_calls=6)
    model = Scripted(
        [
            proposal(OLD, OLD + " and True"),
            proposal(OLD + " and True", OLD + " and True and True"),
            proposal(OLD + " and True and True", OLD + " and True and True and True"),
        ]
    )
    result = asyncio.run(
        coding_loop.run_coding_task(root, tmp_path / "repairs", model, task=task)
    )
    assert result["disposition"] == "REPAIR_BUDGET_EXHAUSTED"
    assert len(model.requests) == 3
    assert result["source_restored"]
    calls = tuple(
        ModelToolCall("search_source", '{"query":"MarkdownFile","mode":"file"}', str(i))
        for i in range(9)
    )
    model = Scripted([ModelResponse("", Scripted.source, tool_calls=calls)])
    result = asyncio.run(
        coding_loop.run_coding_task(root, tmp_path / "actions", model, task=task)
    )
    assert result["disposition"] == "CONTEXT_TOOL_EXECUTION_FAILED"
    assert result["context_actions_attempted"] == 8
    assert len(model.requests) == 1
    assert result["source_restored"]


@pytest.mark.parametrize("kind", ["duplicate", "mixed", "missing_id", "cancel"])
def test_dynamic_invalid_exchange_and_cancellation_are_terminal(
    captured_inputs: Callable[[CodingTask], Path],
    tmp_path: Path,
    kind: str,
) -> None:
    """Never redispatch an ambiguous call or invent a missing native association."""
    root = captured_inputs(MARKDOWN)
    search = call("search_source", query="MarkdownFile", mode="file")
    model: Scripted
    if kind == "cancel":

        class Cancelled(Scripted):
            async def send(self, request: ModelRequest) -> ModelResponse:
                self.requests.append(request)
                raise asyncio.CancelledError

        model = Cancelled([])
    else:
        calls = {
            "duplicate": (search, search),
            "mixed": (search, proposal(OLD, GOOD).tool_calls[0]),
            "missing_id": (ModelToolCall("search_source", search.arguments_json),),
        }[kind]
        model = Scripted([ModelResponse("", Scripted.source, tool_calls=calls)])
    folder = tmp_path / kind

    async def run() -> dict[str, Any]:
        return await coding_loop.run_coding_task(
            root, folder, model, task=replace(MARKDOWN, context_mode="on-demand")
        )

    if kind == "cancel":
        with pytest.raises(asyncio.CancelledError):
            asyncio.run(run())
        result = json.loads((folder / "result.json").read_text(encoding="utf-8"))
        assert result["disposition"] == "CANCELLED_COMPLETION_UNKNOWN_NO_RETRY"
    else:
        result = asyncio.run(run())
        assert result["disposition"] == "PROPOSAL_ADMISSION_FAILED"
    assert result["source_restored"]
    assert len(model.requests) == 1

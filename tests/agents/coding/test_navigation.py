# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- independent literal native schedules
"""The real neutral coding loop consumes navigation, exact source and fixed checks."""

from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding import CodingLimits, run_coding_agent
from devtools.agents.coding.models import CodingProgress
from devtools.agents.coding.navigation import NavigationPolicy
from devtools.agents.coding.projection import ProjectionPolicy
from devtools.agents.coding.repository import (
    CodingObjective,
    EditLimits,
    RepositoryCodingHost,
    SourceChange,
    write_source_changes,
)
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.corpus import define_repository_text_corpus
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.models.interaction import InteractionSource, ModelRequest, ModelResponse
from devtools.resources.commands import Command
from devtools.resources.filesystem import TextFile, write
from devtools.tools import ToolInputError
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from devtools.tools.source import ScopedSourceNavigationTool, SourceScope
from tests.agents.coding.test_repository import call

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from devtools.models.interaction import ModelToolCall


def navigation_host(root: Path, sources: dict[str, str]) -> RepositoryCodingHost:
    """Supply scope and effects without application types or another coding loop."""
    addresses = tuple(RepositoryResourceAddress(p) for p in sources)
    for p, content in sources.items():
        target = root / p
        target.parent.mkdir(parents=True, exist_ok=True)
        write(TextFile(resolve_path(target), content))
    repository = Repository.new()
    scope = SourceScope.observe(
        root=resolve_path(root),
        repository=repository,
        addresses=addresses,
    )
    corpus = define_repository_text_corpus(
        discovery=discover_repository_resource_addresses(
            repository=repository,
            root=scope.root,
            requested_addresses=addresses,
            maximum_resource_count=16,
            maximum_traversal_entry_count=128,
        ),
        selected_addresses=addresses,
    )
    command = (
        Command(sys.executable)
        .args(
            "-I",
            "-c",
            "import runpy; assert runpy.run_path('module.py')['answer']()==7; "
            "print('checked:7')",
        )
        .cwd(scope.root)
        .with_timeout(Duration.seconds(10))
    )
    plan = FixedCheckPlan(scope.root, (FixedCheck("answer", command),), scope)
    objective = CodingObjective(
        "Make answer return 7. Do not edit unadmitted files.",
        scope,
        addresses,
        plan,
        EditLimits(4096, 32768, 8192, 2),
        8192,
        32768,
    )

    async def authorize(_call: ModelToolCall, _arguments: object) -> None:
        assert _call.name in {
            "find_source",
            "read_source_unit",
            "read_source",
            "replace_source",
            "validate_candidate",
        }

    async def effect(changes: tuple[SourceChange, ...]) -> None:
        write_source_changes(scope.root, changes)

    def archive(values: Mapping[RepositoryResourceAddress, str | None]) -> None:
        for address, content in values.items():
            assert content is not None
            write(
                TextFile(
                    resolve_path(
                        root / ("candidate-" + address.value.replace("/", "_")),
                    ),
                    content,
                ),
            )

    def restore(address: RepositoryResourceAddress, content: str | None) -> None:
        assert content is not None
        write(TextFile(resolve_path(root / address.value), content))

    return RepositoryCodingHost(
        objective,
        corpus=corpus,
        authorize=authorize,
        apply_changes=effect,
        archive=archive,
        restore=restore,
        navigation=True,
        projection=ProjectionPolicy(24576, 20000, frozenset({"find_source"})),
    )


class NativeModel:
    """Three selected native decisions; all effects occur in the framework."""

    source = InteractionSource("independent-source-navigation")

    def __init__(self, *, read: bool = True, fault: str = "") -> None:
        """Retain a literal finite schedule and received Prompts."""
        self.requests: list[ModelRequest] = []
        self.read = read
        self.fault = fault

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Select native operations without executing them in the model double."""
        self.requests.append(request)
        number = len(self.requests)
        if number == 1:
            selected = call(
                "find_source",
                {"query": "answer", "path": "module.py"},
                "find",
            )
        elif number == 2 and self.read:
            result = json.loads(request.prompt.messages[-1].content)
            assert request.prompt.messages[-1].tool_call_id == "find"
            assert result["source_acquired"] is False
            unit = next(u for u in result["units"] if u["name"] == "answer")
            assert unit["span"] == [4, 30]
            selected = call(
                "read_source_unit",
                {
                    "unit_id": unit["unit_id"]
                    if self.fault != "foreign"
                    else "foreign",
                    "snapshot_id": result["snapshot_id"]
                    if self.fault != "stale"
                    else "stale",
                },
                "unit",
            )
        else:
            if self.read:
                result = json.loads(request.prompt.messages[-1].content)
                assert request.prompt.messages[-1].tool_call_id == "unit"
                assert result["text"] == "def answer():\n    return 6"
                assert result["span"] == [4, 30]
                assert not result["partial"]
            selected = call(
                "replace_source",
                {"path": "module.py", "old_text": "return 6", "new_text": "return 7"},
                "edit",
            )
        return ModelResponse("", self.source, tool_calls=(selected,))


@pytest.mark.parametrize("fault", ["", "metadata", "foreign", "stale", "disabled"])
def test_actual_native_navigation_edit_validation_and_authority(
    tmp_path: Path,
    fault: str,
) -> None:
    original = "# π\ndef answer():\n    return 6\n"
    host = navigation_host(tmp_path, {"module.py": original})
    if fault == "disabled":
        host.navigation = False
    model = NativeModel(read=fault != "metadata", fault=fault)
    limits = CodingLimits(
        2 if fault == "metadata" else 3,
        1,
        4,
        Duration.seconds(10),
        Duration.seconds(30),
    )
    result = asyncio.run(run_coding_agent(model, limits=limits, host=host))
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == original
    assert result.custody.restored
    if not fault:
        assert result.accepted
        expected = b"checked:7\r\n" if sys.platform == "win32" else b"checked:7\n"
        assert host.check_results[0][0].command_result.stdout == expected
        assert (tmp_path / "candidate-module.py").read_text(
            encoding="utf-8",
        ) == original.replace("return 6", "return 7")
        assert (
            len(host.source_results) == 2
        )  # one selected read; one admitted after-image
        assert result.progress.model_calls == 3
        assert result.progress.actions == 2
    else:
        assert not result.accepted
        assert not host.check_results
        assert not host.source_results
        assert (tmp_path / "candidate-module.py").read_text(
            encoding="utf-8",
        ) == original
        if fault == "metadata":
            assert "not acquired" in host.messages[-1].content
        else:
            assert result.error is not None


def test_nonpython_outline_window_partial_and_path_space(tmp_path: Path) -> None:
    host = navigation_host(tmp_path, {"data π.txt": "first\r\nsecond\r\nthird\r\n"})

    progress = CodingProgress(
        CodingLimits(4, 1, 5, Duration.seconds(5), Duration.seconds(20)),
    )

    async def inspect() -> None:
        await host.prepare(progress)
        response = ModelResponse(
            "",
            InteractionSource("generic"),
            tool_calls=(call("find_source", {"path": "data π.txt"}, "find"),),
        )
        assert host.classify(response) == "acquire"
        await host.acquire(response)
        result = json.loads(host.messages[-1].content)
        assert result["units"][0]["kind"] == "file"
        assert result["units"][0]["name"] is None
        assert result["units"][0]["symbol_fallback"] == "unsupported-language"
        assert not host.disclosures
        host.objective = replace(host.objective, disclosure_bytes=7)
        response = ModelResponse(
            "",
            InteractionSource("generic"),
            tool_calls=(
                call(
                    "read_source_unit",
                    {
                        "unit_id": result["units"][0]["unit_id"],
                        "snapshot_id": result["snapshot_id"],
                    },
                    "read",
                ),
            ),
        )
        host.classify(response)
        await host.acquire(response)
        value = json.loads(host.messages[-1].content)
        assert value["text"] == "first\r\n"
        assert value["partial"]
        assert value["span"] == [0, 7]
        assert value["remaining_range"] == [7, 22]
        await host.prepare(progress)
        assert host.active_disclosures[0].span == (0, 7)

    asyncio.run(inspect())


@pytest.mark.parametrize("cancel", [False, True])
def test_navigation_boundary_fault_is_not_replayed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    cancel: bool,
) -> None:
    host = navigation_host(
        tmp_path,
        {"module.py": "# π\ndef answer():\n    return 6\n"},
    )
    entered: list[object] = []

    async def lost_result(_self: object, selected: object) -> object:
        entered.append(selected)
        if cancel:
            raise asyncio.CancelledError
        message = "navigation result unavailable"
        raise OSError(message)

    monkeypatch.setattr(ScopedSourceNavigationTool, "execute", lost_result)
    model = NativeModel()
    result = asyncio.run(
        run_coding_agent(
            model,
            limits=CodingLimits(3, 1, 4, Duration.seconds(10), Duration.seconds(30)),
            host=host,
        ),
    )
    assert len(entered) == len(model.requests) == 1
    assert not result.accepted
    assert not host.source_results
    assert not host.check_results
    assert not host.progress.effects[0].acknowledged
    assert result.custody.restored


def test_changed_source_between_metadata_and_read_is_not_disclosed(
    tmp_path: Path,
) -> None:
    host = navigation_host(tmp_path, {"module.py": "def answer():\n    return 6\n"})
    progress = CodingProgress(
        CodingLimits(3, 1, 4, Duration.seconds(10), Duration.seconds(30)),
    )

    async def changed() -> None:
        await host.prepare(progress)
        response = ModelResponse(
            "",
            InteractionSource("currentness"),
            tool_calls=(call("find_source", {"path": "module.py"}, "find"),),
        )
        host.classify(response)
        await host.acquire(response)
        metadata = json.loads(host.messages[-1].content)
        (tmp_path / "module.py").write_text("unexpected bytes", encoding="utf-8")
        read = ModelResponse(
            "",
            InteractionSource("currentness"),
            tool_calls=(
                call(
                    "read_source_unit",
                    {
                        "unit_id": metadata["units"][0]["unit_id"],
                        "snapshot_id": metadata["snapshot_id"],
                    },
                    "read",
                ),
            ),
        )
        with pytest.raises(ToolInputError, match="no longer current"):
            host.classify(read)
        assert not host.source_results
        assert not host.disclosures
        assert host.messages[-1].tool_call_id == "find"
        assert (tmp_path / "module.py").read_text() == "unexpected bytes"

    asyncio.run(changed())


@pytest.mark.parametrize(
    "values",
    [
        {"path": "src"},
        {"path": "private.py"},
        {"path": []},
        {"path": "../outside"},
        {"query": []},
        {"mode": []},
        {"offset": True},
        {"unexpected": "field"},
    ],
)
def test_native_navigation_argument_refusal_is_bounded_and_preexecution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    values: dict[str, object],
) -> None:
    host = navigation_host(tmp_path, {"module.py": "def answer(): return 6"})
    entered: list[object] = []

    async def forbidden(_self: object, arguments: object) -> object:
        entered.append(arguments)
        raise AssertionError

    monkeypatch.setattr(ScopedSourceNavigationTool, "execute", forbidden)

    class RepeatingModel:
        source = InteractionSource("neutral-invalid-navigation")

        async def send(self, _request: ModelRequest) -> ModelResponse:
            return ModelResponse(
                "",
                self.source,
                tool_calls=(call("find_source", values, str(len(host.responses))),),
            )

    result = asyncio.run(
        run_coding_agent(
            RepeatingModel(),
            host=host,
            limits=CodingLimits(3, 1, 2, Duration.seconds(5), Duration.seconds(20)),
        ),
    )
    feedback = [json.loads(m.content) for m in host.messages if m.role == "tool"]
    assert len(feedback) == 3
    assert feedback[-1]["reason"] == "action_budget"
    assert result.progress.actions == 2
    assert all(e.acknowledged for e in result.progress.effects)
    assert result.progress.model_calls == 3
    assert not entered
    assert not host.disclosures
    assert not host.source_results
    assert not host.active_disclosures
    assert result.custody.restored
    for row in feedback[:2]:
        assert row["status"] == "REFUSED"
        assert row["tool_operation_entered"] is False
        assert row["source_acquired"] is False
        assert row["edit_witness_granted"] is False
        assert "omit path" in row["instruction"]
    assert [m.tool_call_id for m in host.messages if m.role == "tool"] == [
        "0",
        "1",
        "2",
    ]


def test_real_neutral_process_corrects_search_then_reads_edits_checks(
    tmp_path: Path,
) -> None:
    original = "# \u03c0\ndef answer():\n    return 6\n"
    host = navigation_host(tmp_path, {"module.py": original})

    class CorrectingModel:
        source = NativeModel.source

        def __init__(self) -> None:
            self.delegate = NativeModel()
            self.requests: list[ModelRequest] = []

        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            if len(self.requests) == 1:
                return ModelResponse(
                    "",
                    self.source,
                    tool_calls=(
                        call(
                            "find_source",
                            {"query": "answer", "path": "src"},
                            "invalid",
                        ),
                    ),
                )
            if len(self.requests) == 2:
                message = request.prompt.messages[-1]
                assert message.tool_call_id == "invalid"
                assert json.loads(message.content)["tool_operation_entered"] is False
            return await self.delegate.send(request)

    model = CorrectingModel()
    result = asyncio.run(
        run_coding_agent(
            model,
            host=host,
            limits=CodingLimits(4, 1, 3, Duration.seconds(10), Duration.seconds(40)),
        ),
    )
    assert result.accepted
    assert result.custody.restored
    assert len(model.requests) == 4
    assert result.progress.actions == 3
    assert all(e.acknowledged for e in result.progress.effects)
    assert host.check_results[0][0].command_result.exit_code == 0
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == original
    assert "return 7" in (tmp_path / "candidate-module.py").read_text(encoding="utf-8")


@pytest.mark.parametrize("error", [ToolInputError, PermissionError])
def test_postentry_or_authorization_errors_are_not_refusals(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    error: type[Exception],
) -> None:
    host = navigation_host(tmp_path, {"module.py": "def answer(): return 6"})
    entered: list[object] = []

    async def fail(_self: object, arguments: object) -> object:
        entered.append(arguments)
        message = "after possible entry"
        raise error(message)

    monkeypatch.setattr(ScopedSourceNavigationTool, "execute", fail)
    result = asyncio.run(
        run_coding_agent(
            NativeModel(),
            host=host,
            limits=CodingLimits(3, 1, 3, Duration.seconds(5), Duration.seconds(20)),
        ),
    )
    assert len(entered) == result.progress.model_calls == 1
    assert isinstance(result.error, error)
    assert not result.progress.effects[0].acknowledged
    assert not any(m.role == "tool" for m in host.messages)
    assert result.custody.restored


def test_native_batch_refusal_then_scopewide_search(tmp_path: Path) -> None:
    host = navigation_host(tmp_path, {"module.py": "def answer(): return 6"})

    async def run() -> None:
        await host.prepare(
            CodingProgress(
                CodingLimits(
                    2,
                    1,
                    2,
                    Duration.seconds(5),
                    Duration.seconds(20),
                ),
            ),
        )
        response = ModelResponse(
            "",
            InteractionSource("neutral-batch"),
            tool_calls=(
                call("find_source", {"path": "src"}, "bad"),
                call("find_source", {"query": "answer"}, "corrected"),
            ),
        )
        host.classify(response)
        await host.acquire(response)
        assert [m.tool_call_id for m in host.messages[-2:]] == ["bad", "corrected"]
        assert json.loads(host.messages[-2].content)["status"] == "REFUSED"
        assert json.loads(host.messages[-1].content)["units"]
        assert host.progress.actions == 2
        assert all(e.acknowledged for e in host.progress.effects)
        assert not host.disclosures

    asyncio.run(run())


def test_navigation_admission_failure_is_not_argument_feedback(tmp_path: Path) -> None:
    host = navigation_host(tmp_path, {"module.py": "def answer(): return 6"})
    admissions: list[object] = []

    async def denied(selected: ModelToolCall, _arguments: object) -> None:
        admissions.append(selected)
        message = "host authorization refused"
        raise ToolInputError(message)

    host.authorize = denied
    result = asyncio.run(
        run_coding_agent(
            NativeModel(),
            host=host,
            limits=CodingLimits(2, 1, 2, Duration.seconds(5), Duration.seconds(20)),
        ),
    )
    assert len(admissions) == 1
    assert isinstance(result.error, ToolInputError)
    assert not result.progress.effects[0].acknowledged
    assert not any(m.role == "tool" for m in host.messages)
    assert not host.disclosures


@pytest.mark.parametrize("query", [None, [], 0])
def test_task_navigation_never_substitutes_for_invalid_query(
    tmp_path: Path,
    query: object,
) -> None:
    host = navigation_host(tmp_path, {"module.py": "def answer(): return 6"})
    host.navigation_policy = NavigationPolicy()

    class InvalidQueryModel:
        source = InteractionSource("typed-query-control")

        async def send(self, _request: ModelRequest) -> ModelResponse:
            return ModelResponse(
                "",
                self.source,
                tool_calls=(call("find_source", {"query": query}, "invalid-query"),),
            )

    result = asyncio.run(
        run_coding_agent(
            InvalidQueryModel(),
            host=host,
            limits=CodingLimits(1, 1, 1, Duration.seconds(5), Duration.seconds(20)),
        ),
    )
    assert result.error is None
    assert result.progress.effects[0].acknowledged
    assert host.messages[-1].tool_call_id == "invalid-query"
    assert json.loads(host.messages[-1].content)["status"] == "REFUSED"
    assert not host.disclosures

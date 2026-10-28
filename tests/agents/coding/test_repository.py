# Copyright (c) 2026
# ruff: noqa: D103 -- explicit public admission and effect-boundary controls
"""Literal scope, budget and typed execution faults on the real repository host."""

from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from devtools.agents.coding import CodingLimits, run_coding_agent
from devtools.agents.coding import repository as owner
from devtools.agents.coding.repository import (
    CodingObjective,
    EditLimits,
    RepositoryCodingHost,
    write_source_changes,
)
from devtools.agents.model_tools import execute_model_tool_call
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.corpus import define_repository_text_corpus
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.models.interaction import InteractionSource, ModelResponse, ModelToolCall
from devtools.resources.commands import Command
from devtools.resources.filesystem import TextFile, write
from devtools.tools import ToolRunner
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from devtools.tools.source import SourceScope
from tests.agents.coding.fixtures import GOOD, SOURCE

if TYPE_CHECKING:
    from pathlib import Path


def host_at(root: Path) -> RepositoryCodingHost:
    address = RepositoryResourceAddress("module.py")
    write(TextFile(resolve_path(root / address.value), SOURCE))
    repo = Repository.new()
    scope = SourceScope.observe(
        root=resolve_path(root),
        repository=repo,
        addresses=(address,),
    )
    corpus = define_repository_text_corpus(
        discovery=discover_repository_resource_addresses(
            repository=repo,
            root=scope.root,
            requested_addresses=(address,),
            maximum_resource_count=4,
            maximum_traversal_entry_count=128,
        ),
        selected_addresses=(address,),
    )
    plan = FixedCheckPlan(
        scope.root,
        (
            FixedCheck(
                "fixed",
                Command(sys.executable)
                .args("-I", "-c", "pass")
                .cwd(scope.root)
                .with_timeout(Duration.seconds(5)),
            ),
        ),
        scope,
    )
    objective = CodingObjective(
        "Return 7",
        scope,
        (address,),
        plan,
        EditLimits(1024, 1024, 2048, 4),
        1024,
        32768,
    )

    async def admit(_call: object, _arguments: object) -> None:
        return

    async def apply(changes: Any) -> None:  # noqa: ANN401 -- explicit admitted Tool boundary
        write_source_changes(scope.root, changes)

    def restore(selected: RepositoryResourceAddress, text: str | None) -> None:
        assert text is not None
        write(TextFile(resolve_path(root / selected.value), text))

    return RepositoryCodingHost(
        objective,
        corpus=corpus,
        authorize=admit,
        apply_changes=apply,
        archive=lambda _: None,
        restore=restore,
    )


def call(name: str, values: object, identity: str) -> ModelToolCall:
    return ModelToolCall(name, json.dumps(values), identity)


READ = call(
    "read_source",
    {"path": "module.py", "start": 0, "end": len(SOURCE)},
    "read",
)
EDIT = call(
    "replace_source",
    {"path": "module.py", "old_text": "return 6", "new_text": "return 7"},
    "edit",
)
LIMITS = CodingLimits(4, 1, 4, Duration.seconds(5), Duration.seconds(20))


class Script:
    """Fixed native responses, with actual provider entry counts."""

    source = InteractionSource("independent-admission-controls")

    def __init__(self, calls: list[tuple[ModelToolCall, ...]]) -> None:
        """Retain a finite independently authored schedule."""
        self.calls = calls
        self.entries = 0

    async def send(self, _request: object) -> ModelResponse:
        """Return one normalized response without executing any Tool or edit."""
        selected = self.calls[self.entries]
        self.entries += 1
        return ModelResponse("literal", self.source, tool_calls=selected)


@pytest.mark.parametrize(
    "field",
    ["region_bytes", "source_bytes", "aggregate_bytes", "operations"],
)
def test_nonpositive_edit_policy_refused(field: str) -> None:
    with pytest.raises(ValueError, match="positive"):
        replace(EditLimits(10, 100, 100, 2), **{field: 0})


@pytest.mark.parametrize(
    "fault",
    ["empty", "duplicate", "foreign", "budget", "check-scope"],
)
def test_invalid_objective_refused_before_model(tmp_path: Path, fault: str) -> None:
    host = host_at(tmp_path)
    value = host.objective
    changed: dict[str, Any] = (
        {"text": " "}
        if fault == "empty"
        else (
            {"editable": value.editable * 2}
            if fault == "duplicate"
            else {"editable": (RepositoryResourceAddress("other.py"),)}
            if fault == "foreign"
            else {"prompt_bytes": 0}
            if fault == "budget"
            else {
                "checks": replace(
                    value.checks,
                    source_scope=replace(
                        value.scope,
                        snapshot=replace(
                            value.scope.snapshot,
                            id=type(value.scope.snapshot.id)("0" * 64),
                        ),
                    ),
                ),
            }
        )
    )
    with pytest.raises(ValueError, match="scope"):
        replace(value, **changed)


def test_foreign_corpus_refused(tmp_path: Path) -> None:
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir()
    b.mkdir()
    first, second = host_at(a), host_at(b)
    with pytest.raises(ValueError, match="foreign repository"):
        RepositoryCodingHost(
            first.objective,
            corpus=second.corpus,
            authorize=first.authorize,
            apply_changes=first.effect,
            archive=first.archive,
            restore=first.restore,
        )


@pytest.mark.parametrize(
    "fault",
    ["prompt", "stop", "operation", "mixed", "members", "range"],
)
def test_request_and_native_admission(tmp_path: Path, fault: str) -> None:
    host = host_at(tmp_path)
    values = {
        "prompt": (READ,),
        "stop": (),
        "operation": (call("arbitrary_shell", {}, "unadmitted"),),
        "mixed": (READ, EDIT),
        "members": (call("read_source", {"path": "module.py"}, "members"),),
        "range": (
            call(
                "read_source",
                {"path": "module.py", "start": -1, "end": 100},
                "range",
            ),
        ),
    }
    if fault == "prompt":
        host.objective = replace(host.objective, prompt_bytes=1)
    model = Script([values[fault]])
    result = asyncio.run(run_coding_agent(model, limits=LIMITS, host=host))
    assert not result.accepted
    assert result.progress.proposals == 0
    assert result.progress.effects == [] or all(
        not e.acknowledged for e in result.progress.effects
    )
    assert result.disposition == ("stopped" if fault == "stop" else "failed")
    assert model.entries == (0 if fault == "prompt" else 1)
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == SOURCE


@pytest.mark.parametrize("fault", ["operations", "aggregate", "combined"])
def test_entire_edit_batch_admitted_before_any_effect(
    tmp_path: Path,
    fault: str,
) -> None:
    host = host_at(tmp_path)
    calls = (
        EDIT,
        call(
            "replace_source",
            {
                "path": "module.py",
                "old_text": "# \u03c0",
                "new_text": "# longer comment",
            },
            "comment",
        ),
    )
    policy = replace(
        host.objective.edits,
        **(
            {"operations": 1}
            if fault == "operations"
            else {"aggregate_bytes": 1}
            if fault == "aggregate"
            else {"source_bytes": len(GOOD.encode()) + 10}
        ),
    )
    # Individual replacements fit; only the combined after-image exceeds the cap.
    if fault == "combined":
        calls = (
            call(
                "replace_source",
                {
                    "path": "module.py",
                    "old_text": "return 6",
                    "new_text": "return 77777777",
                },
                "edit",
            ),
            call(
                "replace_source",
                {"path": "module.py", "old_text": "# \u03c0", "new_text": "# longer"},
                "comment",
            ),
        )
    host.objective = replace(host.objective, edits=policy)
    result = asyncio.run(
        run_coding_agent(Script([(READ,), calls]), limits=LIMITS, host=host),
    )
    assert result.disposition == "proposal_limit"
    assert result.error is None
    assert len(result.progress.effects) == 1  # the acquired source, no edit dispatch
    reason = json.loads(host.messages[-1].content)["reason"]
    assert {
        "operations": "operation",
        "aggregate": "Aggregate",
        "combined": "Combined",
    }[fault] in reason
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == SOURCE


@pytest.mark.parametrize("fault", ["arguments", "typed-payload"])
def test_composition_detects_corruption_before_effect(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    host = host_at(tmp_path)
    actual = execute_model_tool_call

    class CorruptRunner(ToolRunner):
        async def execute(self, tool: Any, arguments: Any) -> Any:  # noqa: ANN401 -- controlled ToolRunner boundary fault
            copied = tuple(list(arguments))  # noqa: C414 -- deliberately different tuple identity
            return await super().execute(tool, copied)

    async def boundary(selected: ModelToolCall, **kwargs: Any) -> Any:  # noqa: ANN401 -- transparent shared composition fault
        if selected.name == "replace_source":
            if fault == "arguments":
                selected = replace(selected, arguments_json="{}")
            else:
                kwargs["runner"] = CorruptRunner()
        return await actual(selected, **kwargs)

    monkeypatch.setattr(owner, "execute_model_tool_call", boundary)
    result = asyncio.run(
        run_coding_agent(Script([(READ,), (EDIT,)]), limits=LIMITS, host=host),
    )
    assert result.disposition == "failed"
    assert result.failure_phase == "application"
    assert isinstance(result.error, ValueError)
    assert "admitted" in str(result.error)
    assert result.progress.effects[-1].acknowledged is False
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == SOURCE

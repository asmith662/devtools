# Copyright (c) 2026
# ruff: noqa: D103, SLF001, PLR2004 -- actual native-boundary regressions
"""Codex qualification of map navigation; scripted calls are not Qwen evidence."""

from __future__ import annotations

import asyncio
import hashlib
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen import coding_loop
from apps.qwen.context_tools import ContextRequestError, ContextTools
from apps.qwen.edits import admit_observed
from apps.qwen.patch_proposal_worker import PatchProposalError
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelToolCall,
)
from devtools.models.interaction.providers import LlamaCppInteraction
from tests.apps.qwen.test_coding_loop import Scripted
from tests.apps.qwen.test_context_tools import dispatch
from tests.apps.qwen.test_context_tools import tools as tools  # noqa: PLC0414
from tests.apps.qwen.test_observed_edits import by_path

if TYPE_CHECKING:
    from pathlib import Path


def enabled(tools: ContextTools) -> ContextTools:
    return ContextTools(
        tools.root,
        replace(tools.task, map_navigation=True, path_edits=True),
        direct_reads=True,
    )


def test_opt_in_and_legacy_identity(tools: ContextTools) -> None:
    assert "repository_map" not in {d.name for d in tools.definitions}
    before = tools.task.definition_sha256
    assert replace(tools.task, map_navigation=False).definition_sha256 == before
    assert replace(tools.task, map_navigation=True).definition_sha256 != before
    with pytest.raises(ValueError, match="boolean"):
        replace(tools.task, map_navigation="yes")  # type: ignore[arg-type]
    with pytest.raises(ContextRequestError, match="disclosed"):
        dispatch(tools, "repository_map", query="helper", start=0)
    assert (
        dispatch(
            enabled(tools),
            "repository_map",
            query="notrepresentedanywhere",
            start=0,
        )["status"]
        == "NOT_FOUND"
    )


def test_map_metadata_is_not_edit_authority_and_exact_source_is(
    tools: ContextTools,
) -> None:
    tools = enabled(tools)
    orientation = dispatch(tools, "repository_map", query="helper", start=0)
    selected = next(s for s in orientation["symbols"] if s["name"] == "helper")
    assert orientation["representation"] == "selected-repository-map-metadata-v1"
    assert "return 1" not in orientation["orientation"]
    assert not tools.observations
    source = tools.snapshot.resource_at(tools.addresses[0]).content
    call = by_path(tools.task.source, "return 1", "return 2")
    with pytest.raises(PatchProposalError):
        admit_observed(tools.root, {tools.task.source: source}, (call,), tools)
    observed = dispatch(tools, "expand_source", unit=selected["handle"], to="source")
    assert observed["text"] == "def helper():\n    return 1"
    assert observed["representation"] == "map-selected-exact-source-v1"
    assert not observed["truncated"]
    assert observed["observation_call_id"] == "fixture-call"
    assert observed["edit_ref"]
    _, updates, edits, _ = admit_observed(
        tools.root,
        {tools.task.source: source},
        (call,),
        tools,
    )
    (tools.root / tools.task.source).write_bytes(updates[tools.task.source].encode())
    tools.accept_transaction(updates, edits, call_id="edit")
    with pytest.raises(ContextRequestError, match="invalidate"):
        dispatch(tools, "expand_source", unit=selected["handle"], to="source")
    refreshed = dispatch(tools, "repository_map", query="helper", start=0)
    selected = next(s for s in refreshed["symbols"] if s["name"] == "helper")
    assert (
        "return 2"
        in dispatch(tools, "expand_source", unit=selected["handle"], to="source")[
            "text"
        ]
    )
    assert refreshed["snapshot"] != orientation["snapshot"]


@pytest.mark.parametrize("ending", ["\n", "\r\n", ""])
def test_native_ranges_unicode_and_forged_selection(
    tools: ContextTools,
    ending: str,
) -> None:
    raw = '@decorate\nasync def caf\u00e9():\n    return "\u00e9"'
    text = raw.replace("\n", "\r\n" if ending == "\r\n" else "\n") + ending
    (tools.root / tools.task.source).write_bytes(text.encode())
    tools = enabled(tools)
    result = dispatch(tools, "repository_map", query="caf\u00e9", start=0)
    row = next(r for r in result["symbols"] if r["name"] == "caf\u00e9")
    exact = dispatch(tools, "expand_source", unit=row["handle"], to="source")
    assert exact["text"] == text[text.index("async") :].rstrip("\r\n")
    assert exact["source_range"]["start_line"] == 2
    assert exact["text"] == text[slice(*exact["span"])]
    with pytest.raises(ContextRequestError, match="current"):
        dispatch(tools, "expand_source", unit=row["handle"] + "forged", to="source")
    foreign = enabled(tools)
    with pytest.raises(ContextRequestError):
        dispatch(foreign, "expand_source", unit=row["handle"], to="source")
    (tools.root / tools.task.source).write_bytes((text + "# drift").encode())
    with pytest.raises(ValueError, match="SOURCE_DRIFT"):
        dispatch(tools, "repository_map", query="caf\u00e9", start=0)


def test_large_symbol_is_refused_without_disclosing_or_truncating(
    tools: ContextTools,
) -> None:
    (tools.root / tools.task.source).write_text(
        'def huge():\n    return "' + "x" * 5000 + '"\n',
        encoding="utf-8",
    )
    tools = enabled(tools)
    result = dispatch(tools, "repository_map", query="huge", start=0)
    with pytest.raises(ContextRequestError) as failure:
        dispatch(
            tools,
            "expand_source",
            unit=result["symbols"][0]["handle"],
            to="source",
        )
    assert failure.value.code == "MAP_SOURCE_TOO_LARGE"
    assert not tools.observations


@pytest.mark.parametrize("name", ["Demo", "Demo.method"])
def test_class_and_direct_async_method_remain_native_selections(
    tools: ContextTools,
    name: str,
) -> None:
    tools = enabled(tools)
    page = dispatch(tools, "repository_map", query=name, start=0)
    selected = next(row for row in page["symbols"] if row["name"] == name)
    source = dispatch(tools, "expand_source", unit=selected["handle"], to="source")
    assert source["declaration"] == selected["declaration"]
    assert source["source_range"] == selected["source_range"]
    assert "async def method" in source["text"]
    assert "def caller" not in source["text"]
    assert source["bytes"] <= 4096
    assert not source["truncated"]


def test_bounded_pages_and_unauthorized_files(tools: ContextTools) -> None:
    text = "\n".join(f"def repeated_{i}(): return {i}" for i in range(20))
    (tools.root / tools.task.source).write_bytes(text.encode())
    (tools.root / "src/devtools/hidden.py").write_text("def hidden(): pass\n")
    tools = enabled(tools)
    pages = []
    start = 0
    while True:
        page = dispatch(tools, "repository_map", query="demo.py", start=start)
        assert len(page["symbols"]) <= 6
        assert len(json.dumps(page).encode()) < 12000
        pages.extend(page["symbols"])
        if not page["truncated"]:
            break
        start = page["continuation_start"]
    assert len(pages) == 20
    assert len({row["handle"] for row in pages}) == 20
    assert not dispatch(tools, "repository_map", query="hidden", start=0)["symbols"]
    assert not tools.observations


def test_new_file_absence_then_map_refresh(tools: ContextTools) -> None:
    path = "src/devtools/created.py"
    task = replace(tools.task, new_paths=(path,), map_navigation=True, path_edits=True)
    tools = ContextTools(tools.root, task, direct_reads=True)
    absence = dispatch(tools, "inspect_source", path=path, start=0)
    assert absence["status"] == "ABSENT"
    text = "def created(): return 7"  # exact no-final-newline contract
    _, updates, edits, _ = admit_observed(
        tools.root,
        {task.source: (tools.root / task.source).read_text(), path: ""},
        (by_path(path, "", text),),
        tools,
    )
    (tools.root / path).write_bytes(text.encode())
    tools.accept_transaction(updates, edits, call_id="create")
    page = dispatch(tools, "repository_map", query="created", start=0)
    row = next(r for r in page["symbols"] if r["path"] == path)
    source = dispatch(tools, "expand_source", unit=row["handle"], to="source")
    assert source["text"] == text
    assert source["edit_ref"]


def test_investigation_can_use_measured_2242_tokens_but_initial_edit_keeps_floor(
    tools: ContextTools,
    tmp_path: Path,
) -> None:
    class Measured(LlamaCppInteraction):
        calls = 0

        async def count_input_tokens(self, _request: ModelRequest) -> int:
            return 2000 if self.calls == 0 else 28478

        async def send(self, request: ModelRequest) -> ModelResponse:
            self.calls += 1
            if self.calls == 1:
                return ModelResponse(
                    "Inspect",
                    self.source,
                    tool_calls=(
                        ModelToolCall(
                            "inspect_source",
                            json.dumps({"path": tools.task.source, "start": 0}),
                            "read",
                        ),
                    ),
                )
            assert request.settings.maximum_output_tokens == 2242
            return ModelResponse("Stop", self.source)

    folder = tmp_path / "capacity"
    folder.mkdir()
    model = Measured(
        endpoint="http://127.0.0.1:8080",
        model="fixture",
        source=InteractionSource("capacity-fixture"),
    )
    asyncio.run(
        coding_loop._turns(
            tools.root,
            folder,
            model,
            {"turns": []},
            maximum_calls=2,
            task=replace(tools.task, output_tokens=8192),
            coordinated_edits=True,
            observed_edits=True,
        ),
    )
    capacity = json.loads((folder / "turn-02/capacity.json").read_text())
    assert capacity["minimum_continuation_output_tokens"] == 2048
    assert capacity["safety_tokens"] == 2048


def test_scripted_native_map_source_edit_and_shared_checks(tmp_path: Path) -> None:
    from tests.apps.qwen.test_change_checks import _contract  # noqa: PLC0415

    _, ns = _contract()
    root = tmp_path.resolve()
    task, folder = asyncio.run(ns["fixture"](root))
    # Genuine independent tiny source + real fixed checks, not a Devtools copy.
    path = task.source
    original = (root / path).read_text()
    (root / path).write_text(
        original + "\n\ndef selected() -> int:\n    return VALUE\n",
        encoding="utf-8",
    )
    from scripts.backlog.coordinator import git  # noqa: PLC0415

    asyncio.run(git(root, "add", "--", path))
    asyncio.run(git(root, "commit", "-m", "Independent navigation fixture"))
    task = replace(
        task,
        baseline_revision=asyncio.run(git(root, "rev-parse", "HEAD")),
        baseline_hashes=tuple(
            (p, hashlib.sha256((root / p).read_bytes()).hexdigest())
            for p, _ in task.baseline_hashes
        ),
        map_navigation=True,
        maximum_calls=6,
        tool_actions=8,
    )
    coding_loop._prepare_workspace(root, folder, task)

    class Navigation(Scripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            n = len(self.requests)
            if n == 1:
                name, args = "repository_map", {"query": "selected", "start": 0}
            elif n == 2:
                data = json.loads(request.prompt.messages[-1].content)
                row = next(s for s in data["symbols"] if s["name"] == "selected")
                name, args = "expand_source", {"unit": row["handle"], "to": "source"}
            elif n == 3:
                name, args = (
                    "replace_source",
                    {
                        "path": path,
                        "old_text": "return VALUE",
                        "new_text": "return VALUE + 0",
                    },
                )
            elif n == 4:
                name, args = "inspect_source", {"path": path, "start": 0}
            elif n == 5:
                name, args = (
                    "replace_source",
                    {
                        "path": path,
                        "old_text": "VALUE: int = 1",
                        "new_text": "VALUE: int = 2",
                    },
                )
            else:
                name, args = "check_changes", {}
            return ModelResponse(
                "Scripted",
                self.source,
                tool_calls=(ModelToolCall(name, json.dumps(args), f"map-{n}"),),
            )

    model = Navigation([])
    report: dict[str, Any] = {"turns": [], "accepted": False}
    asyncio.run(
        coding_loop._turns(
            root,
            folder,
            model,
            report,
            maximum_calls=6,
            task=task,
            coordinated_edits=True,
            observed_edits=True,
            check_changes_before_completion=True,
        ),
    )
    assert report["accepted"], report
    assert report["change_check_freshness"]["current"]

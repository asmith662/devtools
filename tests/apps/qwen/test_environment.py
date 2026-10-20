# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004, PT018 -- concrete task-scoped regressions
"""Coding commands and atomic creation exercise existing owners without inference."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen import coding_loop, commands
from apps.qwen.api_contracts import inspect_contract
from apps.qwen.commands import CodingCommands, format_sources
from apps.qwen.context_tools import ContextTools
from apps.qwen.development_task import apply_source_patches
from apps.qwen.edits import admit_transaction, transaction_definition
from apps.qwen.patch_proposal_worker import PatchProposalError
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelToolCall,
)
from devtools.models.interaction.providers import LlamaCppInteraction
from tests.apps.qwen.test_context_tools import dispatch
from tests.apps.qwen.test_context_tools import tools as tools  # noqa: PLC0414

if TYPE_CHECKING:
    from pathlib import Path


def test_quality_checks_only_defer_explicit_absent_new_slots(
    tools: ContextTools,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Existing missing files remain errors; a new file is checked once created."""
    task = replace(tools.task, new_paths=("src/devtools/new.py",))
    calls: list[tuple[str, ...]] = []

    async def execute(_root: Path, *args: str) -> dict[str, Any]:
        calls.append(args)
        return {"exit_code": 0, "failed": False}

    monkeypatch.setattr(commands, "_timed_command", execute)
    asyncio.run(commands.run_check(tools.root, tools.root, task, "typing"))
    assert task.source in calls[-1]
    assert task.new_paths[0] not in calls[-1]
    (tools.root / task.new_paths[0]).write_bytes(b"value = 1\n")
    asyncio.run(commands.run_check(tools.root, tools.root, task, "typing"))
    assert task.new_paths[0] in calls[-1]


def test_actual_capacity_refusal_retains_pending_request_without_model_dispatch(
    tools: ContextTools, tmp_path: Path
) -> None:
    class FullWindow(LlamaCppInteraction):
        async def count_input_tokens(self, request: ModelRequest) -> int:
            assert request.tools
            return 32768

        async def send(self, _request: ModelRequest) -> ModelResponse:
            pytest.fail("Capacity refusal must precede inference")

    model = FullWindow(
        endpoint="http://127.0.0.1:8080",
        model="fixture",
        source=InteractionSource("capacity-fixture"),
    )
    folder = tmp_path / "capacity"
    folder.mkdir()
    report: dict[str, Any] = {"turns": []}
    with pytest.raises(ValueError, match="actual 32K"):
        asyncio.run(
            coding_loop._turns(  # noqa: SLF001 -- exercise the real pre-dispatch boundary
                tools.root,
                folder,
                model,
                report,
                maximum_calls=1,
                task=tools.task,
                coordinated_edits=True,
            )
        )
    assert not report["turns"]
    assert (folder / "turn-01/request.json").exists()
    assert (
        json.loads((folder / "turn-01/capacity.json").read_text())["input_tokens"]
        == 32768
    )


def test_installed_dependencies_are_observed_without_model_import_selection() -> None:
    for target, package in (
        ("pytest.main", "pytest"),
        ("huggingface_hub.hf_hub_download", "huggingface-hub"),
    ):
        observed = inspect_contract(target, (target,))
        assert observed["package"] == package
        assert observed["package_version"]
        assert observed["signature"]
        assert len(observed["observation_id"]) == 64


def test_plan_metadata_does_not_reject_an_observed_edit_for_an_old_768_char_limit(
    tools: ContextTools,
) -> None:
    resource = tools.snapshot.resources[0]
    dispatch(
        tools,
        "read_source",
        path=tools.task.source,
        version=str(resource.content_identity),
        start=0,
        end=len(resource.content),
    )
    values = {
        "plan": "p" * 962,
        "api_evidence": [],
        "edits": [
            {
                "path": tools.task.source,
                "version": str(resource.content_identity),
                "old_text": "return 1",
                "new_text": "return 2",
            }
        ],
    }
    sources = {tools.task.source: resource.content}
    call = ModelToolCall("propose_edits", json.dumps(values), "plan")
    _, updated, _, _ = admit_transaction(tools.root, sources, call, tools)
    assert "return 2" in updated[tools.task.source]
    values["plan"] = "p" * 4097
    with pytest.raises(PatchProposalError, match="plan"):
        admit_transaction(
            tools.root, sources, replace(call, arguments_json=json.dumps(values)), tools
        )


def test_observed_creation_atomic_application_refresh_and_refusal(
    tools: ContextTools, tmp_path: Path
) -> None:
    new = "src/devtools/added.py"
    task = replace(tools.task, new_paths=(new,))
    scoped = ContextTools(tools.root, task)
    absence = dispatch(scoped, "inspect_new_source", path=new)
    resource = scoped.snapshot.resources[0]
    dispatch(
        scoped,
        "read_source",
        path=resource.address.value,
        version=str(resource.content_identity),
        start=0,
        end=len(resource.content),
    )
    values: dict[str, Any] = {
        "plan": "Add a scoped helper and use an observed change",
        "api_evidence": [],
        "edits": [
            {
                "path": new,
                "version": absence["version"],
                "old_text": "",
                "new_text": "def added() -> int:\n    return 2\n",
            },
            {
                "path": task.source,
                "version": str(resource.content_identity),
                "old_text": "return 1",
                "new_text": "return 2",
            },
        ],
    }
    call = ModelToolCall("propose_edits", json.dumps(values), "create")
    source = {task.source: resource.content, new: ""}
    bad = json.loads(call.arguments_json)
    bad["edits"][1]["old_text"] = "invented"
    with pytest.raises(PatchProposalError):
        admit_transaction(
            scoped.root, source, replace(call, arguments_json=json.dumps(bad)), scoped
        )
    assert not (scoped.root / new).exists()
    patch, updates, metadata, _ = admit_transaction(scoped.root, source, call, scoped)
    folder = tmp_path / "patch"
    folder.mkdir()
    asyncio.run(apply_source_patches(scoped.root, folder, patch))
    scoped.accept_transaction(updates, metadata, call_id="create")
    assert scoped.observed("return 2", path=new)
    scoped.check_current()
    assert (scoped.root / new).read_bytes() == values["edits"][0]["new_text"].encode()
    with pytest.raises(ValueError, match="absent"):
        dispatch(scoped, "inspect_new_source", path=new)
    assert (
        json.loads(
            transaction_definition(task.sources, api_required=False).input_schema_json
        )["properties"]["api_evidence"]["maxItems"]
        == 0
    )


@pytest.mark.parametrize("failure", ["unobserved", "stale", "oversized", "collision"])
def test_creation_refuses_without_mutation(tools: ContextTools, failure: str) -> None:
    path = "src/devtools/added.py"
    scoped = ContextTools(tools.root, replace(tools.task, new_paths=(path,)))
    absence = dispatch(scoped, "inspect_new_source", path=path)
    if failure == "unobserved":
        scoped.absent_observations.clear()
    if failure == "collision":
        (scoped.root / path).write_bytes(b"# unrelated\n")
    row = {
        "path": path,
        "version": "f" * 64 if failure == "stale" else absence["version"],
        "old_text": "",
        "new_text": "x" * 4097 if failure == "oversized" else "# new\n",
    }
    call = ModelToolCall(
        "propose_edits",
        json.dumps({"plan": "create", "api_evidence": [], "edits": [row]}),
        "new",
    )
    with pytest.raises((ValueError, PatchProposalError)):
        admit_transaction(scoped.root, {path: ""}, call, scoped)
    assert (
        (scoped.root / path).read_bytes() == b"# unrelated\n"
        if failure == "collision"
        else not (scoped.root / path).exists()
    )


def test_command_surface_confines_arguments_archives_and_returns_failures(
    tools: ContextTools, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    task = replace(tools.task, command_tools=True)
    seen = []

    async def execute(_root: Path, *argv: str) -> dict[str, Any]:
        seen.append(argv)
        return {
            "exit_code": 1,
            "failed": True,
            "stdout": "x" * 4000,
            "stderr": "primary failure",
            "elapsed_seconds": 0.01,
        }

    monkeypatch.setattr(commands, "_timed_command", execute)
    adapter = CodingCommands(tools.root, tmp_path, task)
    for operation in ("status", "diff", "history"):
        result = asyncio.run(
            adapter.dispatch(
                ModelToolCall(
                    "git_inspect",
                    json.dumps({"operation": operation, "path": task.source}),
                    "git",
                )
            )
        )
        assert result["truncated"] and result["source_sha256"]
    for check in commands.CHECKS:
        result = asyncio.run(
            adapter.dispatch(
                ModelToolCall("run_check", json.dumps({"check": check}), "check")
            )
        )
        assert result["status"] == "FAIL" and result["stderr"] == "primary failure"
    assert len(list(tmp_path.glob("coding-command-*.json"))) == 8
    for name, args in [
        ("run_check", {"check": "shell"}),
        ("git_inspect", {"operation": "diff", "path": "../private"}),
        ("run_check", {"check": "tests", "args": "--write"}),
        ("shell", {}),
    ]:
        with pytest.raises(
            ValueError, match=r"operation|New|Task|Tool|resource|boolean"
        ):
            asyncio.run(
                adapter.dispatch(ModelToolCall(name, json.dumps(args), "refuse"))
            )
    assert all("shell" not in a for a in seen)


def test_mechanical_format_is_ast_preserving_and_journaled_before_source_write(
    tools: ContextTools, tmp_path: Path
) -> None:
    target = tools.root / tools.task.source
    target.write_bytes(b"def helper( )->int:\n return 1\n")
    (tools.root / "pyproject.toml").write_text("[tool.ruff]\nline-length=88\n")
    original = target.read_bytes()
    journal = []

    def admit(path: str, text: str) -> None:
        assert target.read_bytes() == original
        journal.append((path, text))

    updated = asyncio.run(format_sources(tools.root, tmp_path, tools.task, admit))
    assert (
        journal
        and updated
        and target.read_bytes().decode() == updated[tools.task.source]
    )


def test_task_defaults_preserve_historical_hashes_and_reasoning_limits(
    tools: ContextTools,
) -> None:
    legacy = tools.task
    assert (
        legacy.definition_sha256
        == replace(
            legacy, tool_actions=8, command_tools=False, new_paths=()
        ).definition_sha256
    )
    assert replace(legacy, output_tokens=12288, call_seconds=600).output_tokens == 12288
    for changes in (
        {"tool_actions": 33},
        {"new_paths": ("../no.py",)},
        {"new_paths": (legacy.source,)},
        {"command_tools": "yes"},
    ):
        with pytest.raises(
            ValueError, match=r"operation|New|Task|Tool|resource|boolean"
        ):
            replace(legacy, **changes)

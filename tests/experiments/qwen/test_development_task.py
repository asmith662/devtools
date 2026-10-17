# Copyright (c) 2026
# ruff: noqa: SLF001, COM812, PLR2004 -- fixed bounds and experiment internals
"""Deterministic native-call and patch confinement tests; no live inference."""

from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from devtools.core.paths import resolve_path
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
)
from devtools.resources.filesystem import TextFile
from devtools.tools import ToolInvocation, ToolRunner
from devtools.tools.filesystem import ReadRepositoryFileTool
from experiments.qwen import development_task as task
from experiments.qwen.patch_proposal_worker import PatchProposalError


def _workspace(tmp_path: Path) -> Path:
    for name, text in ((task.SOURCE, "old\n"), (task.TESTS, "# existing tests\n")):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="")
    return tmp_path


def _patch() -> str:
    return f"--- a/{task.SOURCE}\n+++ b/{task.SOURCE}\n@@ -1 +1 @@\n-old\n+new\n"


def test_native_call_materializes_and_executes_existing_tool(tmp_path: Path) -> None:
    """A real native argument object reaches ToolRunner and the filesystem Tool."""
    root = _workspace(tmp_path)
    invocation: ToolInvocation[Any] = task._ReadInvocation(resolve_path(root))
    call = ModelToolCall("read_repository_file", json.dumps({"path": task.TESTS}))
    value = asyncio.run(
        ToolRunner().execute(
            ReadRepositoryFileTool(resolve_path(root)),
            invocation.materialize(call.arguments_json),
        )
    )
    assert isinstance(value, TextFile)
    assert value.content == "# existing tests\n"
    assert invocation.descriptor.name == call.name


def test_upfront_context_contains_complete_source_and_tests_without_tools(
    tmp_path: Path,
) -> None:
    """Both frozen resources arrive in one disclosure-bound request."""
    root = _workspace(tmp_path)
    request, details = task._upfront_context(root)
    assert request.tools == ()
    assert request.settings.maximum_output_tokens == 1_500
    assert request.settings.thinking_enabled is False
    assert task.SOURCE in request.prompt.content
    assert task.TESTS in request.prompt.content
    assert "old\n" in request.prompt.content
    assert "# existing tests\n" in request.prompt.content
    assert details["resources"] == [task.SOURCE, task.TESTS]
    assert details["resource_bytes"] == {task.SOURCE: 4, task.TESTS: 17}


def test_upfront_context_output_allowance_does_not_change_disclosure(
    tmp_path: Path,
) -> None:
    """The comparison changes output capacity while keeping prompt/context fixed."""
    root = _workspace(tmp_path)
    _, baseline_details = task._upfront_context(root)
    expanded, expanded_details = task._upfront_context(
        root, maximum_output_tokens=4_096
    )
    assert task.SOURCE in expanded.prompt.content
    assert task.TESTS in expanded.prompt.content
    assert expanded_details["resources"] == baseline_details["resources"]
    assert expanded_details["resource_bytes"] == baseline_details["resource_bytes"]
    assert expanded.settings.maximum_output_tokens == 4_096
    assert expanded.settings.thinking_enabled is False
    assert expanded.tools == ()


def test_upfront_context_worker_makes_one_no_tool_request(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """One malformed answer is retained and rejected without a retry or Tool."""
    root = _workspace(tmp_path)
    folder = _frozen(root, monkeypatch)
    frozen = json.loads((folder / "freeze.json").read_text(encoding="utf-8"))
    request, _ = task._upfront_context(root)
    oracle = folder / "acceptance.py"
    frozen.update(
        root=str(root),
        harness_sha256=task._hash(Path(task.__file__)),
        oracle_path=str(oracle),
        oracle_sha256=task._hash(oracle),
        prompt=request.prompt.content,
        prompt_sha256=hashlib.sha256(request.prompt.content.encode()).hexdigest(),
        hashes={path: task._hash(root / path) for path in (task.SOURCE, task.TESTS)},
        head="synthetic-baseline",
        model={
            "service_status": {"state": "READY"},
            "profile_fingerprint": "profile",
        },
        request_settings={
            "maximum_output_tokens": 4_096,
            "thinking_enabled": False,
            "tools": [],
        },
        limits={"requests": 1, "tools": 0, "retries": 0, "timeout_seconds": 300},
    )
    task._save(folder / "freeze.json", frozen, overwrite=True)
    original_command = task._command

    async def command(directory: Path, *args: str) -> dict[str, Any]:
        if args == ("git", "rev-parse", "HEAD"):
            return {"failed": False, "stdout": "synthetic-baseline\n"}
        return await original_command(directory, *args)

    monkeypatch.setattr(task, "_command", command)
    model = _Interaction([ModelResponse("not a diff", _Interaction.source)])
    result = asyncio.run(
        task.run_upfront_context_task(
            root,
            folder,
            model,
            service_status={"state": "READY", "observed_fingerprint": "profile"},
        )
    )
    assert len(model.requests) == 1
    assert model.requests[0].tools == ()
    assert model.requests[0].settings.maximum_output_tokens == 4_096
    assert result["model_invocation"] == "RESPONSE_RECEIVED"
    assert result["tool_calls_returned"] == 0
    assert not result["accepted"]
    assert result["automatic_retries"] == 0


@pytest.mark.parametrize(
    "arguments",
    [
        '{"path":"../outside.py"}',
        '{"path":"C:/outside.py"}',
        '{"path":"/outside.py"}',
        '{"path":"experiments/source_grounding/README.md"}',
        '{"path":null}',
        '{"path":[]}',
        '{"path":"x","extra":true}',
        '{"path":"x","path":"y"}',
        "[]",
        "not json",
    ],
)
def test_native_arguments_fail_closed(tmp_path: Path, arguments: str) -> None:
    """Schema disclosure is not authority: the materializer enforces the scope."""
    with pytest.raises((ValueError, TypeError)):
        task._ReadInvocation(resolve_path(tmp_path)).materialize(arguments)


def test_native_read_rejects_resolved_escape(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An allowed lexical name cannot redirect outside the root."""
    monkeypatch.setattr(
        task, "_materialize_relative_path", lambda *_: resolve_path(tmp_path.parent)
    )
    with pytest.raises(ValueError, match="escapes"):
        task._ReadInvocation(resolve_path(tmp_path)).materialize(
            json.dumps({"path": task.SOURCE})
        )


def test_real_git_patch_engine_changes_only_allowed_file(tmp_path: Path) -> None:
    """A harmless synthetic patch uses actual managed Git, without a new Git repo."""
    root = _workspace(tmp_path)
    folder = root / "evidence"
    folder.mkdir()
    asyncio.run(task.apply_markdown_patch(root, folder, _patch()))
    assert (root / task.SOURCE).read_text() == "new\n"
    assert (root / task.TESTS).read_text() == "# existing tests\n"


@pytest.mark.parametrize(
    "patch",
    [
        "textual tool call",
        _patch().replace(task.SOURCE, "../outside.py"),
        _patch() + "--- a/other.py\n+++ b/other.py\n@@ -1 +1 @@\n-x\n+y\n",
        _patch() + "diff --git a/other b/other\n",
        "x" * 16_385,
    ],
)
def test_patch_scope_rejection_does_not_write(tmp_path: Path, patch: str) -> None:
    """Malformed/multifile/path-escape proposals never reach application."""
    root = _workspace(tmp_path)
    with pytest.raises(PatchProposalError):
        asyncio.run(task.apply_markdown_patch(root, tmp_path, patch))
    assert (root / task.SOURCE).read_text() == "old\n"


def test_nonapplicable_hunk_is_preserved_and_not_applied(tmp_path: Path) -> None:
    """A rejected Git check leaves source bytes intact and retains the proposal."""
    root = _workspace(tmp_path)
    with pytest.raises(PatchProposalError):
        asyncio.run(
            task.apply_markdown_patch(
                root, tmp_path, _patch().replace("-old", "-absent")
            )
        )
    assert (root / task.SOURCE).read_text() == "old\n"
    assert (tmp_path / "proposal.patch").is_file()


class _Interaction:
    source = InteractionSource("synthetic")

    def __init__(self, responses: list[ModelResponse]) -> None:
        self.responses = iter(responses)
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        self.requests.append(request)
        return next(self.responses)


def _native_read() -> ModelResponse:
    return ModelResponse(
        "",
        InteractionSource("synthetic"),
        tool_calls=(
            ModelToolCall("read_repository_file", json.dumps({"path": task.TESTS})),
        ),
        termination=ModelTermination.TOOL_CALL,
    )


def _frozen(root: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Bind synthetic fixture Git identity, retaining actual Git patch execution."""
    original = task._command

    async def command(directory: Path, *args: str) -> dict[str, Any]:
        if args == ("git", "rev-parse", "HEAD"):
            return {"failed": False, "stdout": "synthetic-baseline\n"}
        if args == ("git", "branch", "--show-current"):
            return {"failed": False, "stdout": "synthetic-feature\n"}
        return await original(directory, *args)

    monkeypatch.setattr(task, "_command", command)
    monkeypatch.setattr(
        task, "ACCEPTANCE", "raise AssertionError('synthetic oracle')\n"
    )
    folder = root / "evidence"
    asyncio.run(task.freeze_markdown_task(root, folder))
    return folder


def test_worker_native_read_then_invalid_proposal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Native calls execute, but a textual pseudo-action cannot become a patch."""
    root = _workspace(tmp_path)
    folder = _frozen(root, monkeypatch)
    model = _Interaction(
        [
            _native_read(),
            ModelResponse("<tool_call>read x</tool_call>", _Interaction.source),
        ]
    )
    result = asyncio.run(task.run_markdown_task(root, folder, model))
    assert result["failure_class"] == "PATCH_VALIDATION"
    assert len(result["actions"]) == 1
    assert result["actions"][0]["accepted"]
    assert task.TESTS in model.requests[1].prompt.content
    assert not result["patch_applied"]
    assert not result["accepted"]
    assert (folder / "result.json").is_file()
    with pytest.raises(FileExistsError):
        asyncio.run(task.run_markdown_task(root, folder, model))


def test_text_only_tool_syntax_is_not_executed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Historical compatibility failure is observable, without an inferred read."""
    root = _workspace(tmp_path)
    folder = _frozen(root, monkeypatch)
    model = _Interaction(
        [ModelResponse('{"action":"read_repository_file"}', _Interaction.source)]
    )
    result = asyncio.run(task.run_markdown_task(root, folder, model))
    assert result["failure_class"] == "TOOL_PROTOCOL"
    assert result["actions"] == []
    assert result["model_turns_attempted"] == 1


def test_failed_acceptance_restores_only_model_edit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An applied synthetic patch is not accepted by the real independent oracle."""
    root = _workspace(tmp_path)
    folder = _frozen(root, monkeypatch)
    model = _Interaction([_native_read(), ModelResponse(_patch(), _Interaction.source)])
    result = asyncio.run(task.run_markdown_task(root, folder, model))
    assert result["patch_applied"]
    assert not result["accepted"]
    assert result["failure_class"] == "TEST_FAILURE"
    assert result["unaccepted_edit_restored"]
    assert (folder / "unaccepted-source.py").read_text() == "new\n"
    assert (root / task.SOURCE).read_text() == "old\n"


def test_changed_inputs_stop_before_model(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Prior preparation cannot authorize a changed task input."""
    root = _workspace(tmp_path)
    folder = _frozen(root, monkeypatch)
    (root / task.TESTS).write_text("changed", encoding="utf-8")
    model = _Interaction([])
    with pytest.raises(ValueError, match="input changed"):
        asyncio.run(task.run_markdown_task(root, folder, model))
    assert not model.requests


def test_action_cap_stops_before_ninth_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Repeated native requests consume the finite host action budget."""
    root = _workspace(tmp_path)
    folder = _frozen(root, monkeypatch)
    model = _Interaction([_native_read() for _ in range(9)])
    result = asyncio.run(task.run_markdown_task(root, folder, model))
    assert len(result["actions"]) == 8
    assert result["model_turns_attempted"] == 9
    assert not result["accepted"]
    assert "budget exhausted" in result["error"]


def test_timeout_preserves_unknown_provider_completion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Host cancellation cannot be reported as proof that inference did not run."""
    root = _workspace(tmp_path)
    folder = _frozen(root, monkeypatch)
    original_timeout = asyncio.timeout
    monkeypatch.setattr(asyncio, "timeout", lambda _: original_timeout(0.001))

    class Slow(_Interaction):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            await asyncio.sleep(1)
            return ModelResponse("unused", self.source)

    result = asyncio.run(task.run_markdown_task(root, folder, Slow([])))
    assert result["failure_class"] == "TIMEOUT"
    assert result["turns"] == []
    assert result["model_turns_attempted"] == 1
    assert result["automatic_retries"] == 0


def test_undisclosed_native_tool_is_not_executed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A native transport envelope does not confer command authority."""
    root = _workspace(tmp_path)
    folder = _frozen(root, monkeypatch)
    model = _Interaction(
        [
            ModelResponse(
                "", _Interaction.source, tool_calls=(ModelToolCall("shell", "{}"),)
            )
        ]
    )
    result = asyncio.run(task.run_markdown_task(root, folder, model))
    assert result["failure_class"] == "TOOL_PROTOCOL"
    assert len(result["actions"]) == 1
    assert not result["actions"][0]["accepted"]


def test_synthetic_success_retains_native_read_and_patch_evidence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Scripted validation proves host sequencing, never real task competence."""
    root = _workspace(tmp_path)
    folder = _frozen(root, monkeypatch)
    original = task._command

    async def validation(directory: Path, *args: str) -> dict[str, Any]:
        if "acceptance.py" in args[-1] or "pytest" in args:
            return {"failed": False, "exit_code": 0, "stdout": "synthetic PASS"}
        return await original(directory, *args)

    monkeypatch.setattr(task, "_command", validation)
    model = _Interaction([_native_read(), ModelResponse(_patch(), _Interaction.source)])
    result = asyncio.run(task.run_markdown_task(root, folder, model))
    assert result["accepted"]
    assert result["patch_applied"]
    assert (root / task.SOURCE).read_text() == "new\n"
    assert model.requests[0].tools[0].name == "read_repository_file"

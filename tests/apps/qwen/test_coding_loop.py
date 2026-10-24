# Copyright (c) 2026
# ruff: noqa: SLF001, PLR2004, COM812 -- bounded scripted consumer checks
"""Real retrieval/application/oracle checks with scripted models, never inference."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import TYPE_CHECKING, cast

import pytest

from apps.qwen import coding_loop as worker
from apps.qwen.development_task import SOURCE, _hash
from apps.qwen.tasks import MARKDOWN
from devtools.context import Repository
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
)
from scripts.qwen.patch_proposal_worker_acceptance import _confirm_local_execution

ROOT = Path(__file__).resolve().parents[3]

if TYPE_CHECKING:
    from collections.abc import Callable

    from apps.qwen.tasks import CodingTask
    from devtools.context.retrieval.source import SourceSearchMode


@pytest.fixture
def baseline_root(captured_inputs: Callable[[CodingTask], Path]) -> Path:
    """Use only captured task files, not the active maintained checkout."""
    return captured_inputs(MARKDOWN)


def proposal(old: str, new: str, *, path: str = SOURCE) -> ModelResponse:
    """Represent one native untrusted replacement, not a live model result."""
    return ModelResponse(
        "A bounded proposal for host validation.",
        InteractionSource("scripted"),
        termination=ModelTermination.TOOL_CALL,
        tool_calls=(
            ModelToolCall(
                "propose_edit",
                json.dumps(
                    {
                        "path": path,
                        "old_text": old,
                        "new_text": new,
                    }
                ),
                provider_call_id="call-1",
            ),
        ),
    )


# Scripted proposals exercise the unchanged real oracle. They are not Qwen
# outputs, are never disclosed as a solution, and establish only host behavior.
OLD = "if fence[0] == active_fence[0] and len(fence) >= len(active_fence):"
GOOD = (
    "if (fence[0] == active_fence[0] and len(fence) >= len(active_fence) "
    "and not line[fence_match.end():].strip()):"
)


class Scripted:
    """Record exact requests and deliver prescribed native response facts."""

    source = InteractionSource("scripted")

    def __init__(self, responses: list[ModelResponse | Exception]) -> None:
        """Freeze response order."""
        self.responses = responses
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Return one scripted response; never a provider invocation."""
        self.requests.append(request)
        result = self.responses[len(self.requests) - 1]
        if isinstance(result, Exception):
            raise result
        return result


@pytest.mark.parametrize("mode", ["file", "symbol", "window", "mixed"])
def test_context_selection_materializes_exact_source(
    mode: str,
    tmp_path: Path,
    baseline_root: Path,
) -> None:
    """All views use the admitted corpus with bound lineage and explicit expansion."""
    folder = tmp_path / "context"
    folder.mkdir()
    isolated = worker._prepare_workspace(baseline_root, folder)
    context, resources = worker.acquire_context(
        isolated,
        Repository.new(),
        mode=cast("SourceSearchMode", mode),
    )
    assert len(resources) == 2
    assert resources[0]["mode"] == mode
    assert resources[0]["materialized_kind"] == "file"
    if mode == "symbol":
        assert resources[0]["selected_kind"] == "symbol"
    assert "_FENCE_PATTERN" in context
    assert "Snapshot identity:" in context
    assert all(item["bytes"] > 0 and item["content_identity"] for item in resources)


def test_real_oracle_accepts_scripted_edit_and_cleans_workspace(
    tmp_path: Path,
    baseline_root: Path,
) -> None:
    """A passing real validation is required; the caller's source stays untouched."""
    model = Scripted([proposal(OLD, GOOD)])
    original_hash = _hash(baseline_root / SOURCE)
    result = asyncio.run(worker.run_coding_task(baseline_root, tmp_path / "run", model))
    assert result["accepted"], result
    assert result["baseline_validation"]["oracle"]["failed"]
    assert result["turns"][0]["validation"]["oracle"]["exit_code"] == 0
    assert result["turns"][0]["validation"]["tests"]["exit_code"] == 0
    assert result["workspace_removed"]
    assert result["original_unchanged"]
    assert _hash(baseline_root / SOURCE) == original_hash
    assert len(model.requests) == 1
    assert model.requests[0].conversation is None
    assert [tool.name for tool in model.requests[0].tools] == ["propose_edit"]
    assert model.requests[0].settings.maximum_output_tokens == 4096


def test_cancelled_model_retains_unknown_completion_and_restores_source(
    tmp_path: Path, baseline_root: Path
) -> None:
    """Cancellation restores owned source but is never proof of no model effect."""

    class Interrupted(Scripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            raise asyncio.CancelledError

    original = _hash(baseline_root / SOURCE)
    folder = tmp_path / "cancelled"
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(worker.run_coding_task(baseline_root, folder, Interrupted([])))
    receipt = json.loads((folder / "result.json").read_text())
    assert receipt["disposition"] == "CANCELLED_COMPLETION_UNKNOWN_NO_RETRY"
    assert receipt["model_calls_attempted"] == 1
    assert receipt["source_restored"]
    assert _hash(baseline_root / SOURCE) == original


def test_failure_feedback_current_source_and_second_repair(
    tmp_path: Path,
    baseline_root: Path,
) -> None:
    """A failed edit remains only in isolation and is the next proposal's baseline."""
    wrong = OLD.replace("len(fence) >=", "len(fence) >")
    model = Scripted([proposal(OLD, wrong), proposal(wrong, GOOD)])
    result = asyncio.run(worker.run_coding_task(baseline_root, tmp_path / "run", model))
    assert result["accepted"], result
    assert len(model.requests) == 2
    assert result["turns"][0]["disposition"] == "TESTS_FAILED"
    prompt = model.requests[1].prompt.content
    assert "EDIT_RETAINED_IN_ISOLATED_WORKSPACE" in prompt
    assert "call-1" in prompt
    assert "AssertionError" in prompt
    assert wrong in prompt
    assert "A bounded proposal for host validation." in prompt
    assert prompt.count("Repository Context disclosure") == 1
    assert result["turns"][1]["source_before"] == result["turns"][0]["source_after"]


@pytest.mark.parametrize(
    "response",
    [
        proposal(OLD, GOOD, path="../outside.py"),
        ModelResponse("no proposal", Scripted.source),
        ModelResponse("", Scripted.source, tool_calls=(ModelToolCall("shell", "{}"),)),
        RuntimeError("provider unavailable"),
        TimeoutError("unknown completion"),
        ModelResponse(
            "truncated", Scripted.source, termination=ModelTermination.OUTPUT_LIMIT
        ),
    ],
)
def test_failures_do_not_redispatch_or_escape(
    tmp_path: Path,
    response: ModelResponse | Exception,
    baseline_root: Path,
) -> None:
    """Invalid/native/provider outcomes stop rather than trying another call."""
    model = Scripted([response])
    result = asyncio.run(worker.run_coding_task(baseline_root, tmp_path / "run", model))
    assert not result["accepted"]
    assert len(model.requests) == 1
    assert result["workspace_removed"]
    assert result["original_unchanged"]
    assert not (tmp_path / "outside.py").exists()


def test_exhaustion_and_directory_reuse_refused(
    tmp_path: Path,
    baseline_root: Path,
) -> None:
    """Valid but behaviorally wrong edits stop at the configured call bound."""
    wrong = OLD.replace("len(fence) >=", "len(fence) >")
    model = Scripted([proposal(OLD, wrong)])
    folder = tmp_path / "run"
    result = asyncio.run(
        worker.run_coding_task(baseline_root, folder, model, maximum_calls=1)
    )
    assert result["disposition"] == "REPAIR_BUDGET_EXHAUSTED"
    assert result["workspace_removed"]
    assert result["original_unchanged"]
    with pytest.raises(FileExistsError):
        asyncio.run(worker.run_coding_task(baseline_root, folder, model))
    assert len(model.requests) == 1


def test_call_bound_refused_before_preparation(tmp_path: Path) -> None:
    """A caller cannot enlarge the admitted repair bound."""
    with pytest.raises(ValueError, match="authenticated task limit"):
        asyncio.run(
            worker.run_coding_task(
                ROOT, tmp_path / "run", Scripted([]), maximum_calls=4
            )
        )


def test_confirmation_describes_loop_and_defaults_no(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The genuine console prompt accurately describes all three possible calls."""
    import argparse  # noqa: PLC0415

    monkeypatch.setattr("sys.stdin.isatty", lambda: True)
    prompts = []

    def decline(prompt: str) -> str:
        prompts.append(prompt)
        return ""

    monkeypatch.setattr("builtins.input", decline)
    with pytest.raises(SystemExit, match="declined"):
        _confirm_local_execution(
            argparse.Namespace(
                freeze_only=False,
                authorize_local_execution=False,
                coding_loop=True,
                structured_edit=True,
                model="qwen38-local",
                report_path="run",
            )
        )
    assert "at most 3" in prompts[0]
    assert "[y/N]" in prompts[0]


def test_noninteractive_worker_does_not_advertise_a_bypass(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Offer only terminal consent for the bounded coding worker."""
    import argparse  # noqa: PLC0415

    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    with pytest.raises(SystemExit, match="real terminal") as refusal:
        _confirm_local_execution(
            argparse.Namespace(
                freeze_only=False,
                authorize_local_execution=False,
                coding_loop=True,
            )
        )
    assert "--authorize-local-execution" not in str(refusal.value)


def test_feedback_preserves_primary_failure_and_marks_truncation() -> None:
    """Full logs remain untouched while primary facts survive secondary noise."""
    facts = {
        "nodeid": "test_primary",
        "phase": "call",
        "exception": "TypeError",
        "message": "invalid split keyword",
        "message_truncated": False,
    }
    stderr = (
        "QWEN_TEST_FAILURE " + json.dumps(facts) + "\n" + "_pytest/formatter\n" * 2000
    )
    validation = {
        name: {"exit_code": 1, "stdout": "5 failed, 3 passed", "stderr": stderr}
        for name in ("oracle", "tests")
    }
    feedback = worker._validation_feedback(validation)
    assert feedback["tests"]["primary_failures"] == [facts]
    assert feedback["tests"]["reporting_failure"]
    assert feedback["tests"]["stderr_truncated"]
    assert "[TRUNCATED]" in feedback["tests"]["stderr"]
    assert validation["tests"]["stderr"] == stderr
    assert len(json.dumps(feedback)) < 6000


def test_primary_exception_captured_before_pytest_reporting_failure(
    tmp_path: Path,
    baseline_root: Path,
) -> None:
    """An ast.parse prohibition must not hide the actual code error."""
    folder = tmp_path / "diagnostics"
    folder.mkdir()
    workspace = worker._prepare_workspace(baseline_root, folder)
    test = workspace / "tests/resources/filesystem/models/markdown/test_file.py"
    test.write_text(
        "import ast\n"
        "def test_primary(monkeypatch):\n"
        "    def forbidden(*args, **kwargs):\n"
        "        raise AssertionError('secondary formatter failure')\n"
        "    monkeypatch.setattr(ast, 'parse', forbidden)\n"
        "    raise TypeError('primary code failure')\n"
    )
    result = asyncio.run(worker.validate_workspace(workspace, folder))
    assert result["tests"]["failed"]
    feedback = worker._validation_feedback(result)
    primary = feedback["tests"]["primary_failures"][0]
    assert primary["nodeid"].endswith("::test_primary")
    assert primary["exception"] == "TypeError"
    assert primary["message"] == "primary code failure"
    assert "secondary formatter failure" in result["tests"]["stderr"]

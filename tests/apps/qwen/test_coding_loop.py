# Copyright (c) 2026
# ruff: noqa: SLF001, PLR2004, COM812 -- bounded scripted consumer checks
"""Real retrieval/application/oracle checks with scripted models, never inference."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import TYPE_CHECKING, cast

import pytest

from apps.qwen import coding_loop as worker
from apps.qwen.development_task import SOURCE, _hash, _save, apply_source_patches
from apps.qwen.tasks import MARKDOWN, CodingTask
from devtools.context import Repository
from devtools.core.paths import resolve_path
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
    ModelUsage,
)
from devtools.resources.commands import Command, CommandExecutor
from devtools.resources.filesystem import write
from scripts.qwen.patch_proposal_worker_acceptance import _confirm_local_execution

ROOT = Path(__file__).resolve().parents[3]

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

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
    # The diagnostic test is a newly host-authored input, not candidate drift.
    task = replace(
        MARKDOWN,
        baseline_hashes=tuple(
            (p, _hash(workspace / p)) for p, _ in MARKDOWN.baseline_hashes
        ),
    )
    result = asyncio.run(worker.validate_workspace(workspace, folder, task=task))
    assert result["tests"]["failed"]
    feedback = worker._validation_feedback(result)
    primary = feedback["tests"]["primary_failures"][0]
    assert primary["nodeid"].endswith("::test_primary")
    assert primary["exception"] == "TypeError"
    assert primary["message"] == "primary code failure"
    assert "secondary formatter failure" in result["tests"]["stderr"]


_TINY_SOURCE = "src/devtools/sample.py"
_TINY_TEST = "tests/test_sample.py"
_TINY_OLD = "def value():\n    return 0\n"
_TINY_GOOD = "def value():\n    return 1\n"
_TINY_TEST_TEXT = (
    "from devtools.sample import value\n"
    "def test_integer():\n    assert isinstance(value(), int)\n"
)


async def _tiny_task(root: Path, *, native: bool = False) -> CodingTask:
    """Create a tiny actual Git baseline, without copying the Devtools tree."""
    root.mkdir()  # noqa: ASYNC240 -- tiny synchronous fixture setup, managed Git below
    for path, text in {
        _TINY_SOURCE: _TINY_OLD,
        _TINY_TEST: _TINY_TEST_TEXT,
        "src/devtools/__init__.py": "",
        "src/devtools/read_input.py": "# Frozen task read input.\n",
        ".gitignore": ".local/\n",
    }.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="")
    head = ""
    for args in (
        ("init", "--quiet"),
        ("add", "--", "."),
        (
            "-c",
            "user.name=Independent Test",
            "-c",
            "user.email=test@localhost",
            "commit",
            "--quiet",
            "-m",
            "Tiny authored worker baseline",
        ),
        ("rev-parse", "HEAD"),
    ):
        result = await CommandExecutor().execute(
            Command("git").args(*args).cwd(resolve_path(root)),
        )
        assert not result.failed, result.stderr
        head = result.stdout.decode().strip()
    return CodingTask(
        "tiny-worker",
        "Return one; preserve frozen tests and read inputs.",
        _TINY_SOURCE,
        (_TINY_TEST,),
        head,
        tuple(
            (p, _hash(root / p))
            for p in (_TINY_SOURCE, _TINY_TEST, "src/devtools/read_input.py")
        ),
        tuple(
            (p, "Frozen" if p.endswith("read_input.py") else "value", "file", "none")
            for p in (_TINY_SOURCE, _TINY_TEST, "src/devtools/read_input.py")
        ),
        'assert module.value() == 1, "must return one"',
        read_paths=("src/devtools/read_input.py",),
        context_mode="on-demand" if native else "prepared",
        path_edits=native,
    )


class _TinyScripted:
    """Literal source proposals and real native read feedback, without inference."""

    source = InteractionSource("tiny-selected")

    def __init__(
        self,
        task: CodingTask,
        changes: tuple[tuple[str, str], ...],
        *,
        foreign: bool = False,
    ) -> None:
        self.task, self.changes, self.foreign = task, changes, foreign
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Read before native proposals; preserve exact call identities."""
        self.requests.append(request)
        index = len(self.requests) - 1
        native = self.task.context_mode == "on-demand"
        if native and index == 0:
            name, values = "inspect_source", {"path": _TINY_SOURCE, "start": 0}
        else:
            old, new = self.changes[index - int(native)]
            name = "replace_source" if native else "propose_edit"
            values = {"path": _TINY_SOURCE, "old_text": old, "new_text": new}
        return ModelResponse(
            "Literal independent proposal.",
            InteractionSource("tiny-foreign") if self.foreign else self.source,
            termination=ModelTermination.TOOL_CALL,
            usage=ModelUsage(input_tokens=11, output_tokens=7),
            tool_calls=(ModelToolCall(name, json.dumps(values), f"tiny-{index}"),),
        )


@pytest.mark.parametrize("native", [False, True])
def test_worker_refuses_candidate_that_changes_frozen_test(
    tmp_path: Path,
    *,
    native: bool,
) -> None:
    """Real validation-time test writes invalidate acceptance in both modes."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root, native=native))
    changed = "def test_replaced():\n    assert True\n"
    candidate = (
        "from pathlib import Path\n"
        f"Path({str(root / _TINY_TEST)!r}).write_text({changed!r})\n" + _TINY_GOOD
    )
    model = _TinyScripted(task, ((_TINY_OLD, candidate),))
    folder = root / ".local/run"
    result = asyncio.run(
        worker.run_coding_task(
            root,
            folder,
            model,
            task=task,
            coordinated_edits=native,
            observed_edits=native,
        )
    )
    assert not result["accepted"], result
    assert result["disposition"] == "VALIDATION_FAILED"
    assert result["source_restored"]
    assert not result["original_unchanged"]
    assert (root / _TINY_SOURCE).read_text() == _TINY_OLD
    assert (root / _TINY_TEST).read_text() == changed
    assert (folder / "final-source.py").read_text() == candidate
    assert result["turns"][-1]["validation"]["tests"]["exit_code"] == 0
    assert result["turns"][-1]["validation"]["oracle"]["exit_code"] is None


@pytest.mark.parametrize("native", [False, True])
@pytest.mark.parametrize("cap", [1, 2])
def test_worker_enforces_proposal_cap_across_modes(
    tmp_path: Path,
    *,
    native: bool,
    cap: int,
) -> None:
    """One failed proposal stops at one; a permitted second can legitimately pass."""
    root = resolve_path(tmp_path / "task").value
    task = replace(asyncio.run(_tiny_task(root, native=native)), maximum_proposals=cap)
    wrong = "def value():\n    return 2\n"
    model = _TinyScripted(task, ((_TINY_OLD, wrong), (wrong, _TINY_GOOD)))
    result = asyncio.run(
        worker.run_coding_task(
            root,
            root / ".local/run",
            model,
            task=task,
            coordinated_edits=native,
            observed_edits=native,
        )
    )
    assert result["accepted"] is (cap == 2), result
    assert result["proposals_attempted"] == cap
    assert result["proposals_admitted"] == cap
    assert result["proposal_refusals"] == 0
    assert result["model_calls_attempted"] == cap + int(native)
    assert result["limits"]["proposals"] == cap
    assert result["source_restored"]
    assert result["original_unchanged"]
    if cap == 1:
        assert result["disposition"] == "REPAIR_BUDGET_EXHAUSTED"
    else:
        assert "tiny-" in str(model.requests[-1].prompt)


@pytest.mark.parametrize("native", [False, True])
def test_worker_absolute_call_cap_remains_independent(
    tmp_path: Path,
    *,
    native: bool,
) -> None:
    """A larger proposal allowance never permits another model invocation."""
    root = resolve_path(tmp_path / "task").value
    task = replace(
        asyncio.run(_tiny_task(root, native=native)), maximum_calls=1 + int(native)
    )
    wrong = "def value():\n    return 2\n"
    model = _TinyScripted(task, ((_TINY_OLD, wrong), (wrong, _TINY_GOOD)))
    result = asyncio.run(
        worker.run_coding_task(
            root,
            root / ".local/run",
            model,
            task=task,
            coordinated_edits=native,
            observed_edits=native,
        )
    )
    assert not result["accepted"]
    assert result["model_calls_attempted"] == task.maximum_calls
    assert result["proposals_admitted"] == 1
    assert result["source_restored"]


@pytest.mark.parametrize("native", [False, True])
def test_refused_proposal_is_counted_without_extra_mutation(
    tmp_path: Path,
    *,
    native: bool,
) -> None:
    """A refused first edit consumes the proposal cap without becoming admitted."""
    root = resolve_path(tmp_path / "task").value
    task = replace(asyncio.run(_tiny_task(root, native=native)), maximum_proposals=1)
    model = _TinyScripted(
        task, (("missing literal", _TINY_GOOD), (_TINY_OLD, _TINY_GOOD))
    )
    result = asyncio.run(
        worker.run_coding_task(
            root,
            root / ".local/run",
            model,
            task=task,
            coordinated_edits=native,
            observed_edits=native,
        )
    )
    assert not result["accepted"]
    assert result["proposals_attempted"] == 1
    assert result["proposal_refusals"] == 1
    assert result["proposals_admitted"] == 0
    assert result["model_calls_attempted"] == 1 + int(native)
    assert (root / _TINY_SOURCE).read_text() == _TINY_OLD


@pytest.mark.parametrize("native", [False, True])
def test_zero_proposal_cap_is_not_an_admitted_task(
    tmp_path: Path, *, native: bool
) -> None:
    """Existing task construction refuses zero; no model or Tool can enter."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root, native=native))
    with pytest.raises(ValueError, match="bounded native edit proposals"):
        replace(task, maximum_proposals=0)


@pytest.mark.parametrize("target", ["test", "read", "runner", "configuration"])
def test_worker_refuses_drift_between_fixed_checks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    target: str,
) -> None:
    """Host checking never rebinds its plan to a candidate-mutated input."""
    from apps.qwen import commands  # noqa: PLC0415 -- exercise actual shared selector

    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root))
    folder = root / ".local/run"
    model = _TinyScripted(task, ((_TINY_OLD, _TINY_GOOD),))
    original = commands.run_check
    calls: list[str] = []
    changed = {
        "test": root / _TINY_TEST,
        "read": root / "src/devtools/read_input.py",
        "runner": folder / "tests-runner.py",
        "configuration": root / "pytest.ini",
    }[target]

    async def drift(
        check_root: Path,
        check_folder: Path,
        check_task: CodingTask,
        name: str,
    ) -> dict[str, Any]:
        calls.append(name)
        result = await original(check_root, check_folder, check_task, name)
        if len(calls) == 3:  # baseline tests/oracle, then candidate tests
            changed.write_text("# unexpected validation drift\n", encoding="utf-8")
        return result

    monkeypatch.setattr(commands, "run_check", drift)
    result = asyncio.run(worker.run_coding_task(root, folder, model, task=task))
    assert not result["accepted"], result
    assert result["disposition"] == "VALIDATION_FAILED"
    assert calls == ["tests", "oracle", "tests"]
    assert changed.read_text() == "# unexpected validation drift\n"
    assert result["source_restored"]


@pytest.mark.parametrize("target", ["test", "runner", "configuration"])
def test_worker_reauthenticates_before_final_acceptance(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    target: str,
) -> None:
    """Later immutable drift cannot leave an accepted=True terminal receipt."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root))
    original = worker._turns
    folder = root / ".local/run"
    changed = {
        "test": root / _TINY_TEST,
        "runner": folder / "tests-runner.py",
        "configuration": root / "pytest.ini",
    }[target]

    async def drift(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401 -- preserve the complete worker signature in fault injection
        await original(*args, **kwargs)
        assert args[3]["accepted"]
        changed.write_text("# after validation\n", encoding="utf-8")

    monkeypatch.setattr(worker, "_turns", drift)
    result = asyncio.run(
        worker.run_coding_task(
            root,
            root / ".local/run",
            _TinyScripted(task, ((_TINY_OLD, _TINY_GOOD),)),
            task=task,
        )
    )
    assert not result["accepted"]
    assert result["original_unchanged"] is (target != "test")
    assert result["disposition"] == "INPUT_INTEGRITY_FAILED"
    assert result["source_restored"]


@pytest.mark.parametrize("native", [False, True])
@pytest.mark.parametrize("foreign", [False, True])
def test_response_source_is_checked_before_tools(
    tmp_path: Path,
    *,
    native: bool,
    foreign: bool,
) -> None:
    """Selected-source responses work; foreign facts remain archived, never acted on."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root, native=native))
    model = _TinyScripted(task, ((_TINY_OLD, _TINY_GOOD),), foreign=foreign)
    folder = root / ".local/run"
    result = asyncio.run(
        worker.run_coding_task(
            root,
            folder,
            model,
            task=task,
            coordinated_edits=native,
            observed_edits=native,
        )
    )
    assert result["accepted"] is (not foreign), result
    assert result["source_restored"]
    assert result["original_unchanged"]
    response = json.loads((folder / "turn-01/response.json").read_text())
    assert response["source"] == {
        "value": "tiny-foreign" if foreign else "tiny-selected"
    }
    assert response["tool_calls"][0]["provider_call_id"] == "tiny-0"
    assert response["usage"]["output_tokens"] == 7
    if foreign:
        assert result["disposition"] == "RESPONSE_VALIDATION_FAILED"
        assert result["model_calls_attempted"] == 1
        assert result["context_actions_attempted"] == 0
        assert result["proposals_attempted"] == 0
        assert result["proposals_admitted"] == 0
        assert result["turns"][0]["selected_source"] == "tiny-selected"
        assert result["turns"][0]["response_source"] == "tiny-foreign"
        assert result["turns"][0]["usage"]["input_tokens"] == 11
        assert not (folder / "turn-01/tools.json").exists()


def test_runtime_already_refuses_the_same_foreign_source(tmp_path: Path) -> None:
    """The worker's correspondence check matches the existing narrow Runtime."""
    from devtools.agents.conversation import (  # noqa: PLC0415
        Conversation,
        ConversationMessage,
        ConversationMessageRole,
    )
    from devtools.execution import Runtime  # noqa: PLC0415

    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root))
    model = _TinyScripted(task, ((_TINY_OLD, _TINY_GOOD),), foreign=True)
    with pytest.raises(ValueError, match="response source does not match"):
        asyncio.run(
            Runtime().send(
                conversation=Conversation.new(),
                interaction=model,
                message=ConversationMessage.new(
                    "Inspect the tiny source",
                    role=ConversationMessageRole.USER,
                    source=InteractionSource("tiny-caller"),
                ),
            )
        )
    assert len(model.requests) == 1
    assert (root / _TINY_SOURCE).read_text() == _TINY_OLD


def test_native_batch_components_consume_one_proposal(tmp_path: Path) -> None:
    """Two observed regions share the original transaction-level allowance."""
    root = resolve_path(tmp_path / "task").value
    task = replace(asyncio.run(_tiny_task(root, native=True)), maximum_proposals=1)

    class Batch(_TinyScripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            response = await super().send(request)
            if len(self.requests) == 1:
                return response
            return replace(
                response,
                tool_calls=tuple(
                    ModelToolCall(
                        "replace_source",
                        json.dumps(
                            {
                                "path": _TINY_SOURCE,
                                "old_text": old,
                                "new_text": new,
                            }
                        ),
                        f"component-{index}",
                    )
                    for index, (old, new) in enumerate(
                        (
                            ("def value():", "def value() -> int:"),
                            ("return 0", "return 1"),
                        )
                    )
                ),
            )

    folder = root / ".local/run"
    result = asyncio.run(
        worker.run_coding_task(
            root,
            folder,
            Batch(task, ((_TINY_OLD, _TINY_GOOD),)),
            task=task,
            coordinated_edits=True,
            observed_edits=True,
        )
    )
    assert result["accepted"], result
    assert result["proposals_attempted"] == 1
    assert result["proposals_admitted"] == 1
    assert len(result["turns"][-1]["edits"]) == 2
    assert (
        folder / "final-source.py"
    ).read_text() == "def value() -> int:\n    return 1\n"
    assert (root / _TINY_SOURCE).read_text() == _TINY_OLD


_TINY_TYPED_GOOD = "def value() -> int:\n    return 1\n"


class _SharedCompletion(_TinyScripted):
    """Acquire, implement, and request real shared checks; never inference."""

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Keep exact native calls and leave unavailable final usage unknown."""
        if len(self.requests) != 2:
            return await super().send(request)
        self.requests.append(request)
        return ModelResponse(
            "Check the installed candidate.",
            self.source,
            termination=ModelTermination.TOOL_CALL,
            tool_calls=(ModelToolCall("check_changes", "{}", "completion-check"),),
        )


def _terminal_cli_exit(
    root: Path,
    task: CodingTask,
    result: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> int:
    """Feed a genuine worker result to the maintained CLI return boundary."""
    from scripts.qwen import coding_worker as cli  # noqa: PLC0415

    definition = root / ".local/task.json"
    definition.write_text(json.dumps(asdict(task)))

    async def returned(*_args: Any, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401 -- actual returned worker result at the CLI consumer
        assert kwargs["task"].definition_sha256 == task.definition_sha256
        return result

    monkeypatch.setattr(cli, "run_local_task", returned)
    monkeypatch.setattr(
        "sys.argv",
        [
            "worker",
            "--task-definition",
            str(definition),
            "--report-directory",
            str(root / ".local/cli"),
            "--observed-edits",
            "--check-changes-before-completion",
        ],
    )
    return asyncio.run(cli.main())


def _refuse_terminal_closeout(root: Path, task: CodingTask, folder: Path) -> None:
    """Refuse local candidate admission for an actual nonaccepted worker result."""
    from scripts.backlog.coordinator import git  # noqa: PLC0415
    from scripts.backlog.work import WorkCycle  # noqa: PLC0415

    asyncio.run(git(root, "config", "devtools.backlogCoordinator", str(root)))
    backlog = root / "docs/backlog"
    backlog.mkdir(parents=True)
    (backlog / "overview.md").write_text("# Authored fixture backlog\n")
    with pytest.raises(PermissionError, match="Accepted exact task/oracle"):
        asyncio.run(
            WorkCycle(root).integration.closeout_local(
                task,
                folder,
                branch="feat/terminal",
                expected_head=task.baseline_revision,
            )
        )
    assert (root / _TINY_SOURCE).read_text() == _TINY_OLD
    assert not (root / ".local/backlog/checkout-owner").exists()


@pytest.mark.parametrize("failure", [None, OSError, TimeoutError])
def test_terminal_failure_revokes_worker_success_but_preserves_candidate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: type[OSError] | None,
) -> None:
    """Real validation/currentness survive a later fatal stage-record failure."""
    from scripts.backlog.coordinator import git  # noqa: PLC0415

    root = resolve_path(tmp_path / "task").value
    task = replace(
        asyncio.run(_tiny_task(root, native=True)),
        maximum_calls=3,
        maximum_proposals=1,
        command_tools=True,
        quality_checks=True,
    )
    asyncio.run(git(root, "branch", "-m", "feat/terminal"))
    model = _SharedCompletion(task, ((_TINY_OLD, _TINY_TYPED_GOOD),))
    folder = root / ".local/run"
    original_turns, original_save = worker._turns, _save
    observed: dict[str, Any] = {}

    async def capture(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401 -- inspect the actual public consumer's report, never seed acceptance
        observed["report"] = args[3]
        await original_turns(*args, **kwargs)

    def save(path: Path, value: Any, *, overwrite: bool = False) -> None:  # noqa: ANN401 -- fault only the existing stage-write boundary
        if (
            path == folder / "turn-03/stage.json"
            and value.get("disposition") == "CONTEXT_RETURNED"
        ):
            report = observed["report"]
            assert report["accepted"]
            assert report["change_check"]["ready_for_review"]
            assert report["change_check_freshness"]["current"]
            observed["accepted_before_write"] = True
            if failure is not None:
                message = "completion record unavailable"
                raise failure(message)
        original_save(path, value, overwrite=overwrite)

    monkeypatch.setattr(worker, "_turns", capture)
    monkeypatch.setattr(worker, "_save", save)
    result = asyncio.run(
        worker.run_coding_task(
            root,
            folder,
            model,
            task=task,
            coordinated_edits=True,
            observed_edits=True,
            check_changes_before_completion=True,
        )
    )
    assert observed["accepted_before_write"]
    assert len(model.requests) == result["model_calls_attempted"] == 3
    assert {
        name: result[name]
        for name in (
            "proposals_attempted",
            "proposals_admitted",
            "context_actions_attempted",
            "proposal_refusals",
            "repair_cycles",
        )
    } == {
        "proposals_attempted": 1,
        "proposals_admitted": 1,
        "context_actions_attempted": 2,
        "proposal_refusals": 0,
        "repair_cycles": 0,
    }
    assert result["turns"][1]["validation"]["accepted"]
    assert all(r["status"] == "PASS" for r in result["change_check"]["checks"].values())
    assert result["change_check_freshness"]["current"]
    assert result["source_restored"]
    assert result["original_unchanged"]
    assert (root / _TINY_SOURCE).read_text() == _TINY_OLD
    assert (folder / "final-source.py").read_text() == _TINY_TYPED_GOOD
    assert (folder / "turn-02/proposal.patch").is_file()
    assert result["turns"][0]["usage"]["input_tokens"] == 11
    assert all(value is None for value in result["usage_totals"].values())
    assert json.loads((folder / "result.json").read_text()) == json.loads(
        json.dumps(result)
    )

    expected = 0 if failure is None else 1
    assert _terminal_cli_exit(root, task, result, monkeypatch) == expected, {
        "accepted": result["accepted"],
        "disposition": result["disposition"],
    }
    assert result["accepted"] is (failure is None)
    if failure is None:
        assert result["disposition"] == "ACCEPTED"
        return
    assert result["disposition"] == (
        "HOST_TIMEOUT" if failure is TimeoutError else "CONTEXT_TOOL_EXECUTION_FAILED"
    )
    if failure is OSError:
        assert result["error"] == "OSError: completion record unavailable"
    _refuse_terminal_closeout(root, task, folder)


@pytest.mark.parametrize("point", ["stage", "apply", "result", "restore"])
def test_terminal_effects_are_preserved_without_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, point: str
) -> None:
    """Acknowledge actual effects and retain candidates across terminal faults."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root))
    model = _TinyScripted(task, ((_TINY_OLD, _TINY_TYPED_GOOD),))
    folder = root / ".local/run"
    original_apply = apply_source_patches
    original_save, original_write = _save, write
    failure = OSError("controlled terminal boundary")
    applied: list[str] = []
    faulted = False

    async def apply(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401 -- schedule after the real one-shot Git application
        await original_apply(*args, **kwargs)
        applied.append((root / _TINY_SOURCE).read_text())
        if point == "apply":
            raise failure

    def save(path: Path, value: Any, *, overwrite: bool = False) -> None:  # noqa: ANN401 -- existing write interface
        nonlocal faulted
        if (
            point == "stage"
            and not faulted
            and path == folder / "turn-01/stage.json"
            and value.get("phase") == "VALIDATION"
        ) or (point == "result" and path == folder / "result.json"):
            faulted = True
            raise failure
        original_save(path, value, overwrite=overwrite)

    def write_restoration(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401 -- preserve Resource overloads while failing only restoration
        file = args[0]
        if (
            point == "restore"
            and file.path.value == root / _TINY_SOURCE
            and file.content == _TINY_OLD
            and (folder / "final-source.py").exists()
        ):
            raise failure
        return original_write(*args, **kwargs)

    monkeypatch.setattr(worker, "apply_source_patches", apply)
    monkeypatch.setattr(worker, "_save", save)
    monkeypatch.setattr(worker, "write", write_restoration)
    operation = worker.run_coding_task(root, folder, model, task=task)
    if point in {"result", "restore"}:
        with pytest.raises(OSError, match="controlled terminal boundary") as raised:
            asyncio.run(operation)
        assert raised.value is failure
        assert not (folder / "result.json").exists()
    else:
        result = asyncio.run(operation)
        assert not result["accepted"]
        assert (
            result["disposition"]
            == {
                "stage": "VALIDATION_FAILED",
                "apply": "PATCH_APPLICATION_FAILED",
            }[point]
        )
        assert result["proposals_admitted"] == 1
        assert result["error"] == "OSError: controlled terminal boundary"
    expected_source = _TINY_TYPED_GOOD if point == "restore" else _TINY_OLD
    assert (root / _TINY_SOURCE).read_text() == expected_source
    assert (folder / "final-source.py").read_text() == _TINY_TYPED_GOOD
    assert applied == [_TINY_TYPED_GOOD]
    assert len(model.requests) == 1


def test_terminal_unknown_bytes_require_reconciliation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Passing checks never permit overwriting later unknown source bytes."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root))
    model = _TinyScripted(task, ((_TINY_OLD, _TINY_TYPED_GOOD),))
    folder = root / ".local/run"
    original = worker._turns

    async def changed(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401 -- controlled source change after genuine successful validation
        await original(*args, **kwargs)
        assert args[3]["accepted"]
        (root / _TINY_SOURCE).write_text("UNKNOWN SOURCE\n")

    monkeypatch.setattr(worker, "_turns", changed)
    result = asyncio.run(worker.run_coding_task(root, folder, model, task=task))
    assert not result["accepted"]
    assert result["disposition"] == "CLEANUP_RECONCILIATION_REQUIRED"
    assert result["turns"][0]["validation"]["accepted"]
    assert not result["source_restored"]
    assert (root / _TINY_SOURCE).read_text() == "UNKNOWN SOURCE\n"
    assert (folder / "final-source.py").read_text() == "UNKNOWN SOURCE\n"
    assert len(model.requests) == 1


@pytest.mark.parametrize("point", ["admission", "validation", "provider"])
def test_terminal_cancellation_and_unknown_entry_never_redispatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, point: str
) -> None:
    """Keep pre-entry, known edits and uncertain provider work distinct."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root))
    folder = root / ".local/run"
    original_authenticate = worker._authenticate_inputs
    original_validate = worker.validate_workspace
    validations: list[str] = []

    async def authenticate(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        if point == "admission":
            raise asyncio.CancelledError
        await original_authenticate(*args, **kwargs)

    async def validate(*args: Any, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        validations.append("entered")
        if point == "validation" and len(validations) == 2:
            raise asyncio.CancelledError
        return await original_validate(*args, **kwargs)

    class Interrupted(_TinyScripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            if point == "provider":
                self.requests.append(request)
                (folder / "possible-provider-effect.txt").write_text("entered\n")
                message = "unknown external completion"
                raise TimeoutError(message)
            return await super().send(request)

    model = Interrupted(task, ((_TINY_OLD, _TINY_TYPED_GOOD),))
    monkeypatch.setattr(worker, "_authenticate_inputs", authenticate)
    monkeypatch.setattr(worker, "validate_workspace", validate)
    operation = worker.run_coding_task(root, folder, model, task=task)
    if point == "provider":
        result = asyncio.run(operation)
        assert result["disposition"] == "TIMEOUT_COMPLETION_UNKNOWN_NO_RETRY"
        assert (folder / "possible-provider-effect.txt").read_text() == "entered\n"
        assert all(value is None for value in result["usage_totals"].values())
    else:
        with pytest.raises(asyncio.CancelledError):
            asyncio.run(operation)
        result = json.loads((folder / "result.json").read_text())
        assert result["disposition"] == "HOST_CANCELLED"
    assert not result["accepted"]
    assert result["source_restored"]
    assert (
        result["model_calls_attempted"]
        == len(model.requests)
        == int(point != "admission")
    )
    assert result["proposals_admitted"] == int(point == "validation")
    assert (root / _TINY_SOURCE).read_text() == _TINY_OLD

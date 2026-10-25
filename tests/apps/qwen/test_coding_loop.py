# Copyright (c) 2026
# ruff: noqa: SLF001, PLR2004, COM812 -- bounded scripted consumer checks
"""Real retrieval/application/oracle checks with scripted models, never inference."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, cast

import pytest

from apps.qwen import coding_loop as worker
from apps.qwen.development_task import SOURCE, _hash
from apps.qwen.tasks import MARKDOWN, CodingTask
from devtools.context import Repository
from devtools.core.paths import resolve_path
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
)
from devtools.resources.commands import Command, CommandExecutor
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


def test_worker_reauthenticates_before_final_acceptance(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Later immutable drift cannot leave an accepted=True terminal receipt."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root))
    original = worker._turns

    async def drift(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401 -- preserve the complete worker signature in fault injection
        await original(*args, **kwargs)
        (root / _TINY_TEST).write_text("# after validation\n", encoding="utf-8")

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
    assert not result["original_unchanged"]
    assert result["disposition"] == "INPUT_INTEGRITY_FAILED"
    assert result["source_restored"]

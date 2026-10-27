# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004 -- independently authored contract regressions
"""Codex regressions for fixed validation composition, without model inference."""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from apps.qwen import commands
from apps.qwen.development_task import _save
from devtools.agents import model_tools
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.models.interaction import ModelToolCall
from devtools.resources.commands import (
    Command,
    CommandError,
    CommandExecutor,
    CommandNotFoundError,
    CommandTimeoutError,
)
from devtools.tools import ToolRunner

ROOT = Path(__file__).resolve().parents[3]
ORACLE_SHA256 = "2f23ecf07e9b425e37d7f5f80e7984e7db50e9283dc3606fedfefcb66e579a56"


def _contract() -> tuple[str, dict[str, Any]]:
    source = json.loads(
        (ROOT / "apps/qwen/evaluation/check-bundle-18/task.json").read_text(
            encoding="utf-8"
        )
    )["oracle"]
    assert hashlib.sha256(source.encode()).hexdigest() == ORACLE_SHA256
    namespace: dict[str, Any] = {"__name__": "independent_contract_fixture"}
    exec(compile(source, "unchanged-bundle18-contract", "exec"), namespace)  # noqa: S102 -- immutable trusted host acceptance, never model code
    return source, namespace


@pytest.fixture
def bundle(tmp_path: Path) -> commands.CodingCommands:
    """Reuse authored, qualified tiny files; never copy a Devtools source tree."""
    _, namespace = _contract()
    root = tmp_path.resolve()
    task, folder = asyncio.run(namespace["fixture"](root))
    return commands.CodingCommands(root, folder, task)


def _invoke(tool: commands.CodingCommands) -> dict[str, Any]:
    return asyncio.run(ToolRunner().execute(tool, ("run_check", {"check": "all"})))


def test_command_dispatch_enters_shared_composition_and_archives_real_result(
    bundle: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Host-fixed real check enters shared composition and retains its receipt."""
    original = model_tools.execute_model_tool_call
    entries: list[str] = []

    async def shared(selected: ModelToolCall, **kwargs: Any) -> Any:  # noqa: ANN401 -- transparent instrumentation of a generic operation
        assert kwargs["tool"] is bundle
        assert kwargs["invocation"].descriptor.name == "run_check"
        assert kwargs["tool"].name != selected.name
        entries.append(selected.provider_call_id or "missing")
        return await original(selected, **kwargs)

    monkeypatch.setattr(model_tools, "execute_model_tool_call", shared)
    result = asyncio.run(
        bundle.dispatch(ModelToolCall("run_check", '{"check":"tests"}', "check-native"))
    )
    assert entries == ["check-native"]
    assert result["status"] == "PASS"
    record = json.loads((bundle.folder / result["evidence"]).read_text())
    assert record["status"] == "COMPLETED"
    assert record["result"]["exit_code"] == 0


def test_command_shared_failure_never_enters_command_or_reserves_result(
    bundle: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Actual dispatcher cannot bypass a shared-boundary failure or retry it."""
    error = OSError("composition unavailable")
    entries: list[str] = []

    async def refused(_call: ModelToolCall, **_kwargs: Any) -> Any:  # noqa: ANN401 -- generic boundary fault
        entries.append("shared")
        raise error

    async def forbidden(_arguments: object) -> Any:  # noqa: ANN401 -- unreachable Tool fault target
        pytest.fail("Command Tool bypassed shared composition")

    before = set(bundle.folder.iterdir())
    monkeypatch.setattr(model_tools, "execute_model_tool_call", refused)
    monkeypatch.setattr(bundle, "execute", forbidden)
    with pytest.raises(OSError, match="composition unavailable") as raised:
        asyncio.run(
            bundle.dispatch(
                ModelToolCall("run_check", '{"check":"tests"}', "check-native")
            )
        )
    assert raised.value is error
    assert entries == ["shared"]
    assert set(bundle.folder.iterdir()) == before


def _success(*argv: str) -> dict[str, Any]:
    return {
        "argv": argv,
        "exit_code": 0,
        "stdout": "ok",
        "stderr": "",
        "failed": False,
        "elapsed_seconds": 0.01,
    }


def test_unchanged_contract_through_native_toolrunner_in_fresh_interpreter() -> None:
    """Exercise real checks, independent failures, drift and archival in new imports."""
    source, _ = _contract()
    code = f"import sys\nsys.path.insert(0, {str(ROOT)!r})\n" + source
    result = asyncio.run(
        CommandExecutor().execute(
            Command(sys.executable)
            .args("-I", "-B", "-c", code)
            .cwd(resolve_path(ROOT))
            .with_timeout(Duration.minutes(5))
        )
    )
    assert not result.failed, (result.stdout.decode(), result.stderr.decode())
    assert b"PASS: real5-check/native+ToolRunner bundle" in result.stdout


@pytest.mark.parametrize(
    "error",
    [CommandError, CommandNotFoundError, CommandTimeoutError, OSError, ValueError],
)
def test_unavailable_checks_block_independently(
    bundle: commands.CodingCommands,
    monkeypatch: pytest.MonkeyPatch,
    error: type[Exception],
) -> None:
    calls = []

    async def execute(_root: Path, *argv: str) -> dict[str, Any]:
        calls.append(argv)
        if "ruff" in argv and "format" not in argv:
            message = "Independent unavailable check"
            raise error(message)
        return _success(*argv)

    monkeypatch.setattr(commands, "_timed_command", execute)
    result = _invoke(bundle)
    assert result["status"] == "BLOCKED"
    assert result["checks"]["ruff"]["status"] == "BLOCKED"
    assert result["checks"]["typing"]["status"] == "PASS"
    assert len(calls) == 5


@pytest.mark.parametrize("mode", ["missing-executable", "timeout"])
def test_actual_managed_unavailability_and_timeout(
    bundle: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch, mode: str
) -> None:
    async def execute(root: Path, *argv: str) -> dict[str, Any]:
        if any(a.endswith("tests-runner.py") for a in argv):
            command = (
                Command("devtools-qualified-nonexistent-executable")
                if mode == "missing-executable"
                else Command(sys.executable).args("-c", "import time; time.sleep(2)")
            )
            await CommandExecutor().execute(
                command.cwd(resolve_path(root)).with_timeout(Duration.seconds(0.1))
            )
            pytest.fail("Expected real managed execution error")
        return _success(*argv)

    monkeypatch.setattr(commands, "_timed_command", execute)
    result = _invoke(bundle)
    assert result["status"] == "BLOCKED"
    assert result["checks"]["tests"]["status"] == "BLOCKED"
    assert result["checks"]["oracle"]["status"] == "PASS"


@pytest.mark.parametrize(
    "drift", ["task", "runner", "read", "config", "tests", "source-missing", "scope"]
)
def test_before_validation_drift_cannot_start_commands(
    bundle: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch, drift: str
) -> None:
    if drift == "task":
        bundle.task = replace(bundle.task, objective="Changed plan")
    elif drift == "runner":
        (bundle.folder / "oracle-runner.py").write_text(
            "raise RuntimeError('changed')\n"
        )
    elif drift == "scope":
        object.__setattr__(bundle.task, "source", "../outside.py")
    else:
        path = {
            "read": bundle.task.read_paths[0],
            "tests": bundle.task.tests[0],
            "config": "pyproject.toml",
            "source-missing": bundle.task.source,
        }[drift]
        if drift == "source-missing":
            (bundle.root / path).unlink()
        else:
            with (bundle.root / path).open("a") as target:
                target.write("\n# changed input\n")

    async def never(_root: Path, *_argv: str) -> dict[str, Any]:
        pytest.fail("Invalid input must refuse before executing a check")

    monkeypatch.setattr(commands, "_timed_command", never)
    result = _invoke(bundle)
    assert result["status"] == "BLOCKED"
    assert all(row["status"] != "PASS" for row in result["checks"].values())


def test_preexisting_read_drift_is_not_rebound_by_fresh_tool(
    bundle: commands.CodingCommands,
) -> None:
    target = bundle.root / bundle.task.read_paths[0]
    target.write_text("VALUE = 100\n")
    fresh = commands.CodingCommands(bundle.root, bundle.folder, bundle.task)
    assert _invoke(fresh)["status"] == "BLOCKED"


def test_observed_drift_stays_invalid_after_bytes_restored(
    bundle: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = bundle.root / bundle.task.source
    original = path.read_bytes()
    save = _save

    async def mutate(_root: Path, *argv: str) -> dict[str, Any]:
        path.write_bytes(original + b"\n# observed drift\n")
        return _success(*argv)

    def restore_after_journal(
        target: Path, value: object, *, overwrite: bool = False
    ) -> None:
        save(target, value, overwrite=overwrite)
        assert isinstance(value, dict)
        if not value["result"]["source_unchanged"]:
            path.write_bytes(original)

    monkeypatch.setattr(commands, "_timed_command", mutate)
    monkeypatch.setattr(commands, "_save", restore_after_journal)
    result = _invoke(bundle)
    assert path.read_bytes() == original
    assert result["source_sha256"] == result["source_after_sha256"]
    assert result["source_unchanged"] is False
    assert result["status"] == "BLOCKED"


def test_unexpected_failure_preserves_incomplete_journal(
    bundle: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def fail(_root: Path, *_argv: str) -> dict[str, Any]:
        message = "Unexpected host failure"
        raise RuntimeError(message)

    monkeypatch.setattr(commands, "_timed_command", fail)
    with pytest.raises(RuntimeError, match="Unexpected host"):
        _invoke(bundle)
    receipt = json.loads(next(bundle.folder.glob("coding-command-*.json")).read_text())
    assert receipt["result"]["status"] == "BLOCKED"
    assert all(
        row["status"] == "NOT_RUN" for row in receipt["result"]["checks"].values()
    )


def test_capture_limits_block_instead_of_claiming_complete_evidence(
    bundle: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def truncated(_root: Path, *argv: str) -> dict[str, Any]:
        return {**_success(*argv), "stdout_truncated": True}

    monkeypatch.setattr(commands, "_timed_command", truncated)
    assert _invoke(bundle)["status"] == "BLOCKED"


def test_cancellation_survives_journal_io_failure(
    bundle: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    cancelled = asyncio.CancelledError("Independent cancellation")

    async def stop(_root: Path, *_argv: str) -> dict[str, Any]:
        raise cancelled

    def journal(target: Path, value: object, *, overwrite: bool = False) -> None:
        assert isinstance(value, dict)
        if value["result"]["checks"]["tests"]["status"] == "INTERRUPTED":
            message = "Independent storage failure"
            raise OSError(message)
        _save(target, value, overwrite=overwrite)

    monkeypatch.setattr(commands, "_timed_command", stop)
    monkeypatch.setattr(commands, "_save", journal)
    with pytest.raises(asyncio.CancelledError) as raised:
        _invoke(bundle)
    assert raised.value is cancelled
    assert any(
        "Incomplete cancellation evidence" in note for note in cancelled.__notes__
    )


def test_receipts_are_not_overwritten_by_new_tool_instance(
    bundle: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def execute(_root: Path, *argv: str) -> dict[str, Any]:
        return _success(*argv)

    monkeypatch.setattr(commands, "_timed_command", execute)
    first = _invoke(bundle)
    saved = (bundle.folder / first["evidence"]).read_bytes()
    second = _invoke(commands.CodingCommands(bundle.root, bundle.folder, bundle.task))
    assert second["evidence"] != first["evidence"]
    assert (bundle.folder / first["evidence"]).read_bytes() == saved


def test_single_real_checks_preserve_preexisting_and_successive_receipts(
    bundle: commands.CodingCommands,
) -> None:
    """Actual managed tests get distinct evidence through fresh ToolRunner callers."""
    original = bundle.folder / "coding-command-01.json"
    original.write_bytes(b'{"original": "immutable"}\n')
    saved = original.read_bytes()
    paths = []
    for _ in range(2):
        tool = commands.CodingCommands(bundle.root, bundle.folder, bundle.task)
        result = asyncio.run(
            ToolRunner().execute(tool, ("run_check", {"check": "tests"}))
        )
        assert result["status"] == "PASS"
        paths.append(result["evidence"])
        receipt = json.loads((bundle.folder / result["evidence"]).read_text())
        assert receipt["status"] == "COMPLETED"
        assert receipt["result"]["exit_code"] == 0
        assert receipt["source_sha256"] == result["source_sha256"]
    assert paths == ["coding-command-02.json", "coding-command-03.json"]
    assert original.read_bytes() == saved


def test_competing_adapters_reserve_before_command_entry(
    bundle: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Deterministic overlapping calls cannot select the same durable journal."""

    async def run() -> None:
        entered = 0
        both = asyncio.Event()

        async def check(*_args: object) -> dict[str, Any]:
            nonlocal entered
            entered += 1
            if entered == 2:
                both.set()
            await asyncio.wait_for(both.wait(), 5)
            journals = list(bundle.folder.glob("coding-command-*.json"))
            assert len(journals) == 2
            return _success("independent-side-effect")

        monkeypatch.setattr(commands, "run_check", check)
        first = commands.CodingCommands(bundle.root, bundle.folder, bundle.task)
        second = commands.CodingCommands(bundle.root, bundle.folder, bundle.task)
        results = await asyncio.gather(
            *(
                ToolRunner().execute(tool, ("run_check", {"check": "tests"}))
                for tool in (first, second)
            )
        )
        assert {r["evidence"] for r in results} == {
            "coding-command-01.json",
            "coding-command-02.json",
        }
        assert entered == 2
        assert all(
            json.loads((bundle.folder / r["evidence"]).read_text())["status"]
            == "COMPLETED"
            for r in results
        )

    asyncio.run(run())


@pytest.mark.parametrize("failure", ["reservation", "intent", "completed"])
def test_storage_failures_never_redispatch_or_overwrite(
    bundle: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch, failure: str
) -> None:
    """Fail before entry, or retain unknown effect evidence after failed persistence."""
    entered = []
    mkdir = Path.mkdir

    def reserve(
        path: Path, mode: int = 0o777, *, parents: bool = False, exist_ok: bool = False
    ) -> None:
        if path.suffix == ".reservation" and failure == "reservation":
            message = "independent reservation failure"
            raise PermissionError(message)
        mkdir(path, mode, parents=parents, exist_ok=exist_ok)

    def save(path: Path, value: object, *, overwrite: bool = False) -> None:
        if (failure == "intent" and not overwrite) or (
            failure == "completed" and overwrite
        ):
            message = "independent persistence failure"
            raise OSError(message)
        _save(path, value, overwrite=overwrite)

    async def check(*_args: object) -> dict[str, Any]:
        entered.append("actual deterministic executor entered")
        return _success("fixed-check")

    monkeypatch.setattr(Path, "mkdir", reserve)
    monkeypatch.setattr(commands, "_save", save)
    monkeypatch.setattr(commands, "run_check", check)
    with pytest.raises(OSError, match="independent"):
        asyncio.run(ToolRunner().execute(bundle, ("run_check", {"check": "tests"})))
    assert len(entered) == (1 if failure == "completed" else 0)
    if failure == "completed":
        receipt = json.loads((bundle.folder / "coding-command-01.json").read_text())
        assert receipt["status"] == "EXECUTION_INTENT"
        assert "result" not in receipt
    # Reserved names remain unavailable even without a completed result.
    assert (bundle.folder / "coding-command-01.reservation").is_dir() is (
        failure != "reservation"
    )


def test_single_source_drift_retains_completed_result_before_refusal(
    bundle: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def mutate(*_args: object) -> dict[str, Any]:
        (bundle.root / bundle.task.source).write_text("# unexpected executor bytes\n")
        return _success("fixed-check")

    monkeypatch.setattr(commands, "run_check", mutate)
    with pytest.raises(ValueError, match="mutated source"):
        asyncio.run(ToolRunner().execute(bundle, ("run_check", {"check": "tests"})))
    receipt = json.loads((bundle.folder / "coding-command-01.json").read_text())
    assert receipt["source_unchanged"] is False
    assert receipt["result"]["exit_code"] == 0


def test_optional_typing_and_quality_are_not_applicable_for_direct_host_check(
    bundle: commands.CodingCommands,
) -> None:
    task = replace(bundle.task, quality_checks=False, command_tools=False)
    result = asyncio.run(commands.run_check(bundle.root, bundle.folder, task, "all"))
    assert result["status"] == "PASS"
    assert all(
        result["checks"][c]["status"] == "NOT_APPLICABLE"
        for c in ("ruff", "format", "typing")
    )
    # Availability is still distinct from native Tool authorization.
    with pytest.raises(ValueError, match="task-authorized"):
        _invoke(commands.CodingCommands(bundle.root, bundle.folder, task))


@pytest.mark.parametrize("missing", ["tests", "oracle", "empty-runner"])
def test_invalid_required_plans_are_blocked(
    bundle: commands.CodingCommands, missing: str
) -> None:
    if missing == "empty-runner":
        (bundle.folder / "tests-runner.py").write_text("")
    else:
        object.__setattr__(bundle.task, missing, () if missing == "tests" else " ")
    result = _invoke(commands.CodingCommands(bundle.root, bundle.folder, bundle.task))
    assert result["status"] == "BLOCKED"
    assert (
        result["checks"]["oracle" if missing == "oracle" else "tests"]["status"]
        == "BLOCKED"
    )


@pytest.mark.parametrize("config", ["src/ruff.toml", "tests/conftest.py"])
@pytest.mark.parametrize("during", [False, True])
def test_check_local_configuration_is_bound_to_plan(
    bundle: commands.CodingCommands,
    monkeypatch: pytest.MonkeyPatch,
    config: str,
    during: bool,  # noqa: FBT001 -- pytest parameterized timing case
) -> None:
    path = bundle.root / config
    calls = []

    async def execute(_root: Path, *argv: str) -> dict[str, Any]:
        calls.append(argv)
        if during:
            path.write_text("# configuration changed during validation\n")
        else:
            pytest.fail("Changed configuration must block before checks")
        return _success(*argv)

    if not during:
        path.write_text("# configuration changed before validation\n")
    monkeypatch.setattr(commands, "_timed_command", execute)
    result = _invoke(bundle)
    assert result["status"] == "BLOCKED"
    assert not result["plan_unchanged"]
    assert len(calls) == (1 if during else 0)


@pytest.mark.parametrize("name", ["tests", "oracle"])
def test_substituted_nonempty_runner_cannot_be_admitted_by_new_tool(
    bundle: commands.CodingCommands, name: str
) -> None:
    (bundle.folder / (name + "-runner.py")).write_text("print('not an actual check')\n")
    result = _invoke(commands.CodingCommands(bundle.root, bundle.folder, bundle.task))
    assert result["status"] == "BLOCKED"
    assert result["checks"][name]["status"] == "BLOCKED"

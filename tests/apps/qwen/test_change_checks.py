# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004, PT018 -- independent Codex application regressions
"""Real Git/ToolRunner scoped freshness, without model or repository copies."""

from __future__ import annotations

import asyncio
import copy
import hashlib
import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen import change_checks, commands
from apps.qwen.development_task import _hash
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.models.interaction import ModelToolCall
from devtools.resources.commands import Command, CommandExecutor, CommandTimeoutError
from devtools.tools import ToolRunner
from scripts.backlog.coordinator import git

if TYPE_CHECKING:
    from apps.qwen.tasks import CodingTask

ROOT = Path(__file__).resolve().parents[3]
ORACLE = "e30b61a42763d4e3c4a7ba515b4f9d1532421248c040695d876a55cfa10a5d8d"


def _contract() -> tuple[str, dict[str, Any]]:
    source = json.loads(
        (ROOT / "apps/qwen/evaluation/change-check-16/task.json").read_text(
            encoding="utf-8"
        )
    )["oracle"]
    assert hashlib.sha256(source.encode()).hexdigest() == ORACLE
    namespace: dict[str, Any] = {"__name__": "unchanged_independent_contract"}
    exec(compile(source, "unchanged-engineering16", "exec"), namespace)  # noqa: S102 -- frozen trusted host oracle, never model code
    return source, namespace


@pytest.fixture
def candidate(tmp_path: Path) -> commands.CodingCommands:
    _, ns = _contract()
    root = tmp_path.resolve()
    task, folder = asyncio.run(ns["fixture"](root))
    (root / task.source).write_text(ns["GOOD"], encoding="utf-8")
    return commands.CodingCommands(root, folder, task)


def _invoke(tool: commands.CodingCommands) -> dict[str, Any]:
    return asyncio.run(
        tool.dispatch(ModelToolCall("check_changes", "{}", "native-check"))
    )


def _current(tool: commands.CodingCommands, report: dict[str, Any]) -> dict[str, Any]:
    return asyncio.run(ToolRunner().execute(tool, ("is_current", {"report": report})))


def _fast_checks(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    calls: list[str] = []

    async def check(
        _root: Path, _folder: Path, _task: CodingTask, name: str
    ) -> dict[str, Any]:
        assert name in commands.CHECKS, "The real bundle must own composition"
        calls.append(name)
        return {
            "failed": False,
            "exit_code": 0,
            "stdout": "ok",
            "stderr": "",
            "elapsed_seconds": 0.0,
        }

    monkeypatch.setattr(commands, "run_check", check)
    return calls


def test_original_oracle_and_real_checks_in_fresh_interpreter() -> None:
    source, _ = _contract()
    code = f"import sys\nsys.path.insert(0,{str(ROOT)!r})\n" + source
    result = asyncio.run(
        CommandExecutor().execute(
            Command(sys.executable)
            .args("-I", "-B", "-c", code)
            .cwd(resolve_path(ROOT))
            .with_timeout(Duration.minutes(5))
        )
    )
    assert not result.failed, (result.stdout.decode(), result.stderr.decode())
    assert b"PASS: native ToolRunner composition" in result.stdout


@pytest.mark.parametrize("mode", ["unstaged", "staged", "both", "new", "ignored-new"])
def test_actual_git_change_kinds_and_freshness(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch, mode: str
) -> None:
    calls = _fast_checks(monkeypatch)
    if mode in {"staged", "both"}:
        asyncio.run(git(candidate.root, "add", "--", candidate.task.source))
    if mode == "both":
        with (candidate.root / candidate.task.source).open("a") as stream:
            stream.write("\n# unstaged difference\n")
    if mode in {"new", "ignored-new"}:
        new = candidate.task.new_paths[0]
        if mode == "ignored-new":
            info = candidate.root / ".git/info/exclude"
            with info.open("a") as stream:
                stream.write("\n" + new + "\n")
        (candidate.root / new).write_text('"""Authorized new module."""\n')
    report = _invoke(candidate)
    assert report["ready_for_review"] and calls == list(commands.CHECKS)
    assert candidate.task.source in report["changed"]
    row = report["changed"][candidate.task.source]
    assert row["index_status"] == ("M" if mode in {"staged", "both"} else " ")
    assert row["worktree_status"] == (" " if mode == "staged" else "M")
    if mode in {"new", "ignored-new"}:
        assert report["changed"][candidate.task.new_paths[0]]["present"]
    assert _current(candidate, report)["current"]
    assert candidate.is_current(report)
    # Fresh instances reauthenticate durable evidence, not an in-memory cache.
    fresh = commands.CodingCommands(candidate.root, candidate.folder, candidate.task)
    assert fresh.is_current(report)
    assert calls == list(commands.CHECKS), "Freshness must not rerun checks"


@pytest.mark.parametrize(
    "mutation",
    [
        "source",
        "new-presence",
        "index",
        "head",
        "runner",
        "task",
        "read",
        "test",
        "config",
        "bundle-log",
    ],
)
def test_saved_success_becomes_stale(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch, mutation: str
) -> None:
    calls = _fast_checks(monkeypatch)
    report = _invoke(candidate)
    if mutation == "source":
        with (candidate.root / candidate.task.source).open("a") as stream:
            stream.write("\n# changed\n")
    elif mutation == "new-presence":
        (candidate.root / candidate.task.new_paths[0]).write_text("VALUE = 1\n")
    elif mutation == "index":
        asyncio.run(git(candidate.root, "add", "--", candidate.task.source))
    elif mutation == "head":
        asyncio.run(
            git(
                candidate.root,
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@invalid",
                "commit",
                "--allow-empty",
                "-qm",
                "New HEAD",
            )
        )
    elif mutation == "task":
        candidate.task = replace(candidate.task, objective="Changed host objective")
    else:
        path = {
            "runner": candidate.folder / "tests-runner.py",
            "read": candidate.root / candidate.task.read_paths[0],
            "test": candidate.root / candidate.task.tests[0],
            "config": candidate.root / "pyproject.toml",
            "bundle-log": candidate.folder / report["bundle_evidence"],
        }[mutation]
        with path.open("a") as stream:
            stream.write("\n# mutated after checking\n")
    current = _current(candidate, report)
    assert not current["current"] and not current["ready_for_review"]
    assert len(calls) == 5


def test_index_only_drift_then_new_current_report(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    _fast_checks(monkeypatch)
    old = _invoke(candidate)
    identity = _hash(candidate.root / candidate.task.source)
    asyncio.run(git(candidate.root, "add", "--", candidate.task.source))
    assert _hash(candidate.root / candidate.task.source) == identity
    assert not candidate.is_current(old)
    new = _invoke(candidate)
    assert new["candidate_sha256"] != old["candidate_sha256"]
    assert candidate.is_current(new) and new["ready_for_review"]


@pytest.mark.parametrize(
    "kind", ["tracked-test", "read", "new-outside", "missing-source", "unsafe"]
)
def test_scope_and_absence_fail_closed(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch, kind: str
) -> None:
    calls = _fast_checks(monkeypatch)
    if kind == "unsafe":
        object.__setattr__(candidate.task, "source", "../outside.py")
    elif kind == "missing-source":
        (candidate.root / candidate.task.source).unlink()
    else:
        path = {
            "tracked-test": candidate.task.tests[0],
            "read": candidate.task.read_paths[0],
            "new-outside": "src/devtools/unauthorized.py",
        }[kind]
        with (candidate.root / path).open("a") as stream:
            stream.write("\n# unauthorized effect\n")
    report = _invoke(candidate)
    assert report["status"] == "BLOCKED" and not report["ready_for_review"]
    assert not calls


def test_unrelated_forensics_excluded_and_no_changes_runs_nothing(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = _fast_checks(monkeypatch)
    asyncio.run(git(candidate.root, "restore", "--", candidate.task.source))
    forensic = candidate.root / "forensic.txt"
    forensic.write_text("preserved")
    report = _invoke(candidate)
    assert report["status"] == "NO_CHANGES" and not report["ready_for_review"]
    assert not calls and candidate.is_current(report)
    forensic.write_text("new unrelated evidence")
    assert candidate.is_current(report), (
        "Do not claim unrelated artifacts were validated"
    )


@pytest.mark.parametrize(
    "field", ["ready_for_review", "checks", "receipt_sha256", "evidence"]
)
def test_tampered_payload_never_trusted(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch, field: str
) -> None:
    _fast_checks(monkeypatch)
    report = _invoke(candidate)
    bad = copy.deepcopy(report)
    bad[field] = {
        "ready_for_review": False,
        "checks": {},
        "receipt_sha256": "0" * 64,
        "evidence": "../outside.json",
    }[field]
    assert not _current(candidate, bad)["current"]
    assert candidate.is_current(report)


def test_failure_is_current_but_not_review_eligible(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def check(_a: Path, _b: Path, _task: CodingTask, name: str) -> dict[str, Any]:
        return {
            "failed": name == "tests",
            "exit_code": int(name == "tests"),
            "stdout": "actual validation failure" if name == "tests" else "ok",
            "stderr": "",
        }

    monkeypatch.setattr(commands, "run_check", check)
    report = _invoke(candidate)
    assert report["status"] == "FAIL" and report["checks"]["oracle"]["status"] == "PASS"
    current = _current(candidate, report)
    assert current["current"] and not current["ready_for_review"]


@pytest.mark.parametrize("drift", ["index", "source", "runner", "config"])
def test_drift_during_check_invalidates_bundle(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch, drift: str
) -> None:
    async def check(
        root: Path, folder: Path, task: CodingTask, name: str
    ) -> dict[str, Any]:
        if name == "tests":
            if drift == "index":
                await git(root, "add", "--", task.source)
            else:
                path = {
                    "source": root / task.source,
                    "runner": folder / "tests-runner.py",
                    "config": root / "pyproject.toml",
                }[drift]
                with path.open("a") as stream:
                    stream.write("\n# during validation\n")
        return {"failed": False, "exit_code": 0, "stdout": "ok", "stderr": ""}

    monkeypatch.setattr(commands, "run_check", check)
    report = _invoke(candidate)
    assert report["status"] == "BLOCKED" and not report["ready_for_review"]
    assert not candidate.is_current(report)


@pytest.mark.parametrize(
    "mode", ["missing-runner", "missing-oracle", "optional-quality", "timeout"]
)
def test_incomplete_plan_and_execution_cannot_pass(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch, mode: str
) -> None:
    _fast_checks(monkeypatch)
    if mode == "missing-runner":
        (candidate.folder / "tests-runner.py").unlink()
    elif mode == "missing-oracle":
        candidate.task = replace(candidate.task, oracle=" ")
    elif mode == "optional-quality":
        candidate.task = replace(candidate.task, quality_checks=False)
    else:

        async def check(*_args: object) -> dict[str, Any]:
            message = "Qualified timeout"
            raise CommandTimeoutError(message)

        monkeypatch.setattr(commands, "run_check", check)
    report = _invoke(candidate)
    assert report["status"] == "BLOCKED" and not report["ready_for_review"]


def test_cancellation_preserves_both_journals(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def cancel(
        _root: Path, _folder: Path, _task: CodingTask, name: str
    ) -> dict[str, Any]:
        if name == "oracle":
            message = "Host interruption"
            raise asyncio.CancelledError(message)
        return {"failed": False, "exit_code": 0, "stdout": "ok", "stderr": ""}

    monkeypatch.setattr(commands, "run_check", cancel)
    with pytest.raises(asyncio.CancelledError):
        _invoke(candidate)
    journals = list(candidate.folder.glob("change-check-*.json"))
    report = json.loads(journals[0].read_text())["result"]
    assert report["status"] == "INTERRUPTED" and not report["ready_for_review"]
    assert report["checks"]["tests"]["status"] == "PASS"
    assert report["checks"]["oracle"]["status"] == "INTERRUPTED"
    assert report["checks"]["typing"]["bundle_status"] == "NOT_RUN"
    assert any(
        "INTERRUPTED" in p.read_text()
        for p in candidate.folder.glob("coding-command-*.json")
    )


def test_native_argument_admission(candidate: commands.CodingCommands) -> None:
    invalid: list[tuple[str, dict[str, Any]]] = [
        ("check_changes", {"paths": ["../outside"]}),
        ("is_current", {"report": True}),
        ("is_current", {}),
    ]
    for arguments in invalid:
        with pytest.raises(ValueError, match="Unsupported"):
            asyncio.run(ToolRunner().execute(candidate, arguments))


def test_actual_unmerged_index_blocks_readiness(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = _fast_checks(monkeypatch)

    async def conflict() -> None:
        path = candidate.task.source
        blob = await git(candidate.root, "rev-parse", "HEAD:" + path)
        await git(candidate.root, "update-index", "--force-remove", "--", path)
        index = f"100644 {blob} 1\t{path}\n100644 {blob} 2\t{path}\n"
        result = await CommandExecutor().execute(
            Command("git")
            .args("update-index", "--index-info")
            .with_stdin(index.encode())
            .cwd(resolve_path(candidate.root))
            .with_timeout(Duration.seconds(10))
        )
        assert not result.failed

    asyncio.run(conflict())
    report = _invoke(candidate)
    assert report["status"] == "BLOCKED" and not calls
    assert any("Unmerged" in line for line in report["diagnostics"])


def test_mutation_while_reading_git_cannot_validate_old_source(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    _fast_checks(monkeypatch)
    report = _invoke(candidate)
    original = change_checks.git_state

    async def drift(
        tool: commands.CodingCommands, plan: dict[str, Any]
    ) -> dict[str, Any]:
        state = await original(tool, plan)
        with (tool.root / tool.task.source).open("a") as stream:
            stream.write("\n# changed during state observation\n")
        return state

    monkeypatch.setattr(change_checks, "git_state", drift)
    current = _current(candidate, report)
    assert not current["current"]
    assert any("while observing" in line for line in current["diagnostics"])


def test_journal_tampering_and_missing_full_evidence_are_refused(
    candidate: commands.CodingCommands, monkeypatch: pytest.MonkeyPatch
) -> None:
    _fast_checks(monkeypatch)
    report = _invoke(candidate)
    path = candidate.folder / report["evidence"]
    original = path.read_bytes()
    path.write_text("{}")
    assert not candidate.is_current(report)
    path.write_bytes(original)
    (candidate.folder / report["bundle_evidence"]).unlink()
    assert not candidate.is_current(report)

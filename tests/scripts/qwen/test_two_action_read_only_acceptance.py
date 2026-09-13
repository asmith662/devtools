# Copyright (c) 2026
# ruff: noqa: E501, INP001
"""Tests for bounded reporting in the two-action Qwen acceptance script."""

from __future__ import annotations

import asyncio
import importlib.util
import json
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from devtools.context import Message, MessageRole, MessageSource
from devtools.filesystem import FilesystemNotFoundError
from devtools.interactions import ConversationRef, InteractionTurn

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import ModuleType


_SCRIPT_PATH = Path("scripts/qwen/two_action_read_only_acceptance.py").resolve()


@pytest.fixture
def acceptance() -> Iterator[ModuleType]:
    """Load the tracked script without treating the scripts directory as a package."""
    specification = importlib.util.spec_from_file_location(
        "test_two_action_read_only_acceptance",
        _SCRIPT_PATH,
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    try:
        specification.loader.exec_module(module)
        yield module
    finally:
        sys.modules.pop(specification.name, None)


@dataclass(slots=True)
class _ScriptedInteraction:
    """Return exact planned assistant results through the Interaction contract."""

    responses: list[str]
    calls: list[Message] = field(default_factory=list)
    source: MessageSource = field(default_factory=lambda: MessageSource("qwen"))

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> InteractionTurn:
        """Retain one caller message and produce the next assistant Message."""
        assert conversation is None
        self.calls.append(message)
        return InteractionTurn(
            Message.new(
                self.responses.pop(0),
                role=MessageRole.ASSISTANT,
                source=self.source,
            ),
        )


def test_malformed_first_proposal_retains_raw_assistant_without_execution(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """A modeled first-turn parse failure remains a model-conformance report."""
    fixture = acceptance.create_fixture(tmp_path)
    try:
        report = asyncio.run(
            acceptance.run_acceptance(
                task=acceptance.initial_task(),
                repository_root=fixture.root,
                interaction=_ScriptedInteraction(["{not json"]),
            ),
        )
    finally:
        shutil.rmtree(fixture.root)

    assert report.failure_category == "MODEL CONFORMANCE"
    assert report.latest_assistant is not None
    assert report.latest_assistant.content == "{not json"
    assert report.execution_actions == ()
    assert report.cycles == ()


def test_successful_report_serializes_selected_actions_and_durable_artifact(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """A synthetic production-path success retains selection, projections, and answer."""
    fixture = acceptance.create_fixture(tmp_path)
    target_path = f"facts/{fixture.target_filename}"
    try:
        report = asyncio.run(
            acceptance.run_acceptance(
                task=acceptance.initial_task(),
                repository_root=fixture.root,
                interaction=_ScriptedInteraction(
                    [
                        '{"action":"list_repository_directory","path":"facts"}',
                        f'{{"action":"read_repository_file","path":"{target_path}"}}',
                        fixture.nonce,
                    ],
                ),
            ),
        )
        outcome = acceptance.QwenTwoActionReadOnlyOutcome(
            report=report,
            target_filename=fixture.target_filename,
            nonce=fixture.nonce,
            persistent_service_status="state: READY",
            persistent_service_error_type=None,
            persistent_service_error_message=None,
            fixture_cleanup_succeeded=True,
        )
        report_path = tmp_path / "outcome.json"
        acceptance._write_report(report_path, acceptance._report_payload(outcome))  # noqa: SLF001
    finally:
        shutil.rmtree(fixture.root)

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["schema"] == "qwen-two-action-read-only-acceptance/1"
    assert payload["verdict"] == "PASS"
    assert payload["tool_executions"]["actions"] == [
        "list_repository_directory",
        "read_repository_file",
    ]
    assert payload["cycles"][0]["listing"]["truncated"] is False
    assert payload["final_answer"] == fixture.nonce
    assert not list(tmp_path.glob("*.tmp"))


def test_later_malformed_proposal_retains_first_execution_and_raw_response(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """The final durable artifact retains all bounded later-failure evidence."""
    fixture = acceptance.create_fixture(tmp_path)
    report_path = tmp_path / "partial-failure.json"
    try:
        report = asyncio.run(
            acceptance.run_acceptance(
                task=acceptance.initial_task(),
                repository_root=fixture.root,
                interaction=_ScriptedInteraction(
                    [
                        '{"action":"list_repository_directory","path":"facts"}',
                        "{not json",
                    ],
                ),
            ),
        )
        outcome = acceptance.QwenTwoActionReadOnlyOutcome(
            report=report,
            target_filename=fixture.target_filename,
            nonce=fixture.nonce,
            persistent_service_status="state: READY",
            persistent_service_error_type=None,
            persistent_service_error_message=None,
            fixture_cleanup_succeeded=True,
        )
        acceptance._write_report(  # noqa: SLF001
            report_path,
            acceptance._report_payload(outcome),  # noqa: SLF001
        )
    finally:
        shutil.rmtree(fixture.root)

    assert report_path.exists()
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["schema"] == "qwen-two-action-read-only-acceptance/1"
    assert payload["verdict"] == "FAIL — MODEL CONFORMANCE"
    assert len(payload["cycles"]) == 1
    cycle = payload["cycles"][0]
    assert cycle["action"] == "list_repository_directory"
    assert cycle["relative_path"] == "facts"
    assert f"{fixture.target_filename} [file]" in cycle["result_projection"]
    assert cycle["listing"]["truncated"] is False
    assert cycle["listing"]["entries"] == [
        {"name": cycle["listing"]["entries"][0]["name"], "kind": "file"},
        {"name": fixture.target_filename, "kind": "file"},
    ]
    assert cycle["listing"]["entries"][0]["name"].startswith("decoy-")
    assert payload["latest_assistant"]["content"] == "{not json"
    assert [message["role"] for message in payload["history"]] == [
        "user",
        "assistant",
        "system",
        "assistant",
    ]
    assert [message["source"] for message in payload["history"]] == [
        "qwen-two-action-read-only-acceptance",
        "qwen",
        "runtime",
        "qwen",
    ]
    assert payload["tool_executions"] == {
        "actions": ["list_repository_directory"],
        "resolved_paths": [str((fixture.root / "facts").resolve())],
    }
    assert payload["failure"] == {
        "category": "MODEL CONFORMANCE",
        "error_type": "ReadOnlyProposalError",
        "error_message": "Read-only proposal must be exactly one JSON object.",
    }
    assert not list(tmp_path.glob("*.tmp"))


def test_stdout_remains_a_human_readable_secondary_sink(
    acceptance: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Durable reporting supplements rather than replaces existing stdout evidence."""
    fixture = acceptance.create_fixture(tmp_path)
    report = acceptance.QwenTwoActionReadOnlyReport(
        task=acceptance.initial_task(),
        history=(),
        execution_actions=(),
        execution_paths=(),
        cycles=(),
        result=None,
        failure_category="MODEL CONFORMANCE",
        error_type="ReadOnlyProposalError",
        error_message="malformed proposal",
        latest_assistant=None,
    )
    outcome = acceptance.QwenTwoActionReadOnlyOutcome(
        report=report,
        target_filename=fixture.target_filename,
        nonce=fixture.nonce,
        persistent_service_status="state: READY",
        persistent_service_error_type=None,
        persistent_service_error_message=None,
        fixture_cleanup_succeeded=True,
    )
    try:
        acceptance._print_outcome(outcome)  # noqa: SLF001
    finally:
        shutil.rmtree(fixture.root)

    output = capsys.readouterr().out
    assert "acceptance verdict: FAIL — MODEL CONFORMANCE" in output
    assert "tool actions: none" in output


def test_second_tool_failure_serializes_only_the_completed_list_cycle(
    acceptance: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A failed second read does not erase or publish beyond the first cycle."""
    fixture = acceptance.create_fixture(tmp_path)
    target_path = f"facts/{fixture.target_filename}"

    async def failed_read(_tool: object, _path: object) -> object:
        msg = "fixture read failure"
        raise FilesystemNotFoundError(msg)

    monkeypatch.setattr(acceptance.ReadRepositoryFileTool, "execute", failed_read)
    try:
        report = asyncio.run(
            acceptance.run_acceptance(
                task=acceptance.initial_task(),
                repository_root=fixture.root,
                interaction=_ScriptedInteraction(
                    [
                        '{"action":"list_repository_directory","path":"facts"}',
                        f'{{"action":"read_repository_file","path":"{target_path}"}}',
                    ],
                ),
            ),
        )
    finally:
        shutil.rmtree(fixture.root)

    assert report.failure_category == "FRAMEWORK BOUNDARY"
    assert report.execution_actions == (
        "list_repository_directory",
        "read_repository_file",
    )
    assert len(report.cycles) == 1
    assert report.cycles[0].relative_path == "facts"


def test_main_reports_write_failure_as_nonzero(
    acceptance: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A requested authoritative report cannot fail silently after a successful run."""
    fixture = acceptance.create_fixture(tmp_path)
    report = acceptance.QwenTwoActionReadOnlyReport(
        task=acceptance.initial_task(),
        history=(),
        execution_actions=(),
        execution_paths=(),
        cycles=(),
        result=None,
        failure_category="MODEL CONFORMANCE",
        error_type="x",
        error_message="y",
        latest_assistant=None,
    )
    outcome = acceptance.QwenTwoActionReadOnlyOutcome(
        report=report,
        target_filename=fixture.target_filename,
        nonce=fixture.nonce,
        persistent_service_status="state: READY",
        persistent_service_error_type=None,
        persistent_service_error_message=None,
        fixture_cleanup_succeeded=True,
    )

    async def successful_run(_arguments: object) -> object:
        return outcome

    monkeypatch.setattr(acceptance, "run", successful_run)
    parent_file = tmp_path / "not-a-directory"
    parent_file.write_text("inert", encoding="utf-8")
    try:
        with pytest.raises(SystemExit) as exit_error:
            acceptance.main(["--report-path", str(parent_file / "outcome.json")])
    finally:
        shutil.rmtree(fixture.root)

    assert exit_error.value.code == 1
    assert "could not write durable acceptance report" in capsys.readouterr().err

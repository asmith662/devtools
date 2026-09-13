# Copyright (c) 2026
# ruff: noqa: E501, INP001
"""Tests for bounded failure capture in the live two-read Qwen acceptance."""

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

from devtools.agents.conversation import (
    ConversationMessage,
    ConversationMessageRole,
    InteractionSource,
)
from devtools.models.interaction import ConversationRef, ModelResponse
from devtools.models.interaction.providers.llama_cpp_errors import (
    LlamaCppTransportError,
)

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import ModuleType


_SCRIPT_DIRECTORY = Path("scripts/qwen").resolve()
_SCRIPT_PATH = _SCRIPT_DIRECTORY / "two_read_acceptance.py"
_REQUIRED_READS = 2


@pytest.fixture
def acceptance() -> Iterator[ModuleType]:
    """Load the tracked acceptance script without making scripts a package."""
    specification = importlib.util.spec_from_file_location(
        "test_two_read_acceptance",
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
    """Return planned assistant text or a provider failure through ModelInteraction semantics."""

    responses: list[str]
    fail_on_call: int | None = None
    failure: Exception | None = None
    calls: list[ConversationMessage] = field(default_factory=list)
    source: InteractionSource = field(default_factory=lambda: InteractionSource("qwen"))

    async def send(
        self,
        message: ConversationMessage,
        *,
        conversation: ConversationRef | None = None,
    ) -> ModelResponse:
        """Retain each input and return the next exact assistant result."""
        assert conversation is None
        self.calls.append(message)
        if self.fail_on_call == len(self.calls):
            assert self.failure is not None
            raise self.failure
        return ModelResponse(content=self.responses.pop(0), source=self.source)


@dataclass(frozen=True, slots=True)
class _Fixture:
    """Provide static test typing for a dynamically loaded script fixture."""

    root: Path
    first_nonce: str
    second_nonce: str


def _fixture(acceptance: ModuleType, tmp_path: Path) -> _Fixture:
    created = acceptance.create_fixture(tmp_path)
    return _Fixture(created.root, created.first_nonce, created.second_nonce)


def _outcome(
    acceptance: ModuleType,
    report: object,
    fixture: _Fixture,
) -> object:
    """Build a script-local completed outcome without contacting a provider."""
    return acceptance.QwenTwoReadAcceptanceOutcome(
        report=report,
        first_nonce=fixture.first_nonce,
        second_nonce=fixture.second_nonce,
        persistent_service_status="state: READY",
        persistent_service_error_type=None,
        persistent_service_error_message=None,
        fixture_cleanup_succeeded=True,
    )


def _successful_report(acceptance: ModuleType, fixture: _Fixture) -> object:
    """Complete the bounded experiment through deterministic scripted responses."""
    interaction = _ScriptedInteraction(
        [
            '{"action":"read_repository_file","path":"facts/first.txt"}',
            '{"action":"read_repository_file","path":"facts/second.txt"}',
            f"{fixture.first_nonce}:{fixture.second_nonce}",
        ],
    )
    return asyncio.run(
        acceptance.run_acceptance(
            task=acceptance.initial_task(),
            repository_root=fixture.root,
            interaction=interaction,
        ),
    )


def test_first_malformed_proposal_retains_exact_assistant_and_session(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """First-turn parser failure retains the original Qwen content and zero reads."""
    fixture = _fixture(acceptance, tmp_path)
    agent = _ScriptedInteraction(["{not json"])
    try:
        report = asyncio.run(
            acceptance.run_acceptance(
                task=acceptance.initial_task(),
                repository_root=fixture.root,
                interaction=agent,
            ),
        )
    finally:
        shutil.rmtree(fixture.root)

    assert report.result is None
    assert (
        report.failure_category
        is acceptance.QwenTwoReadFailureCategory.MODEL_CONFORMANCE
    )
    assert report.error_type == "ReadProposalError"
    assert report.latest_assistant is not None
    assert report.latest_assistant.content == "{not json"
    assert report.tool_execution_count == 0
    assert report.tool_execution_paths == ()
    assert [(message.role, message.source) for message in report.history] == [
        (ConversationMessageRole.USER, InteractionSource("qwen-two-read-acceptance")),
        (ConversationMessageRole.ASSISTANT, InteractionSource("qwen")),
    ]


def test_later_malformed_proposal_retains_history_and_completed_read(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """A failed second proposal retains its text, prior SYSTEM result, and one read."""
    fixture = _fixture(acceptance, tmp_path)
    agent = _ScriptedInteraction(
        [
            '{"action":"read_repository_file","path":"facts/first.txt"}',
            '{"action":"unknown","path":"facts/second.txt"}',
        ],
    )
    try:
        report = asyncio.run(
            acceptance.run_acceptance(
                task=acceptance.initial_task(),
                repository_root=fixture.root,
                interaction=agent,
            ),
        )
    finally:
        shutil.rmtree(fixture.root)

    assert report.result is None
    assert (
        report.failure_category
        is acceptance.QwenTwoReadFailureCategory.MODEL_CONFORMANCE
    )
    assert report.latest_assistant is not None
    assert report.latest_assistant.content.startswith('{"action":"unknown"')
    assert report.tool_execution_count == 1
    assert len(report.tool_execution_paths) == 1
    assert [message.role for message in report.history] == [
        ConversationMessageRole.USER,
        ConversationMessageRole.ASSISTANT,
        ConversationMessageRole.SYSTEM,
        ConversationMessageRole.ASSISTANT,
    ]


def test_provider_failure_does_not_invent_assistant_content(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """A provider failure before a result leaves no fabricated assistant ConversationMessage."""
    fixture = _fixture(acceptance, tmp_path)
    agent = _ScriptedInteraction([], fail_on_call=1, failure=LlamaCppTransportError())
    try:
        report = asyncio.run(
            acceptance.run_acceptance(
                task=acceptance.initial_task(),
                repository_root=fixture.root,
                interaction=agent,
            ),
        )
    finally:
        shutil.rmtree(fixture.root)

    assert report.result is None
    assert report.failure_category is acceptance.QwenTwoReadFailureCategory.PROVIDER
    assert report.latest_assistant is None
    assert report.tool_execution_count == 0
    assert report.tool_execution_paths == ()
    assert [message.role for message in report.history] == [
        ConversationMessageRole.USER,
    ]


def test_temporary_fixture_is_removed_after_manual_cleanup(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """The isolated inert fixture can be removed without touching its parent."""
    fixture = _fixture(acceptance, tmp_path)
    assert (fixture.root / "facts" / "first.txt").read_text(
        encoding="utf-8",
    ) == fixture.first_nonce
    shutil.rmtree(fixture.root)
    assert not fixture.root.exists()
    assert tmp_path.exists()


def test_persistent_status_command_is_observational_and_repository_owned(
    acceptance: ModuleType,
) -> None:
    """The acceptance runner invokes only the tracked service status command."""
    command = acceptance._persistent_status_command()  # noqa: SLF001
    assert command.executable == acceptance.sys.executable
    assert command.arguments == (str(acceptance._SERVICE_SCRIPT), "status")  # noqa: SLF001


def test_successful_report_is_durable_parseable_and_survives_fixture_cleanup(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """A caller-selected report remains after the temporary fixture is removed."""
    fixture = _fixture(acceptance, tmp_path)
    report = _successful_report(acceptance, fixture)
    outcome = _outcome(acceptance, report, fixture)
    report_path = tmp_path / "acceptance" / "outcome.json"
    try:
        acceptance._write_report(report_path, acceptance._report_payload(outcome))  # noqa: SLF001
    finally:
        shutil.rmtree(fixture.root)

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["schema"] == "qwen-two-read-acceptance/1"
    assert payload["verdict"] == "PASS"
    assert payload["fixture"]["first_nonce"] == fixture.first_nonce
    assert payload["fixture"]["second_nonce"] == fixture.second_nonce
    assert payload["fixture"]["cleanup"] == "completed"
    assert payload["tool_executions"]["count"] == _REQUIRED_READS
    assert payload["final_answer"] == f"{fixture.first_nonce}:{fixture.second_nonce}"
    assert len(payload["cycles"]) == _REQUIRED_READS
    assert not list(report_path.parent.glob("*.tmp"))


def test_failure_report_preserves_exact_assistant_and_zero_executions(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """A modeled malformed-proposal failure serializes its original diagnostics."""
    fixture = _fixture(acceptance, tmp_path)
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

    payload = acceptance._report_payload(_outcome(acceptance, report, fixture))  # noqa: SLF001
    assert payload["verdict"] == "FAIL — MODEL CONFORMANCE"
    assert payload["latest_assistant"]["content"] == "{not json"
    assert payload["failure"]["error_type"] == "ReadProposalError"
    assert payload["tool_executions"] == {"count": 0, "resolved_paths": []}


def test_later_failure_report_preserves_first_execution_and_latest_response(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """Failure after one read retains the actual completed execution and raw response."""
    fixture = _fixture(acceptance, tmp_path)
    try:
        report = asyncio.run(
            acceptance.run_acceptance(
                task=acceptance.initial_task(),
                repository_root=fixture.root,
                interaction=_ScriptedInteraction(
                    [
                        '{"action":"read_repository_file","path":"facts/first.txt"}',
                        '{"action":"unknown","path":"facts/second.txt"}',
                    ],
                ),
            ),
        )
    finally:
        shutil.rmtree(fixture.root)

    payload = acceptance._report_payload(_outcome(acceptance, report, fixture))  # noqa: SLF001
    assert payload["tool_executions"]["count"] == 1
    assert payload["tool_executions"]["resolved_paths"] == [
        str(fixture.root / "facts" / "first.txt"),
    ]
    assert payload["latest_assistant"]["content"].startswith('{"action":"unknown"')
    assert [message["role"] for message in payload["history"]] == [
        "user",
        "assistant",
        "system",
        "assistant",
    ]


def test_report_write_failure_is_not_silent(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """A report destination beneath an ordinary file fails rather than faking success."""
    parent_file = tmp_path / "not-a-directory"
    parent_file.write_text("inert", encoding="utf-8")
    with pytest.raises(FileExistsError):
        acceptance._write_report(parent_file / "outcome.json", {})  # noqa: SLF001


def test_main_exits_nonzero_when_requested_report_cannot_be_written(
    acceptance: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A successful acceptance cannot become an operational pass without its record."""
    fixture = _fixture(acceptance, tmp_path)
    outcome = _outcome(acceptance, _successful_report(acceptance, fixture), fixture)

    async def successful_run(arguments: object) -> object:
        assert arguments is not None
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


def test_stdout_report_remains_available(
    acceptance: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The durable sink supplements rather than replaces human-readable stdout."""
    fixture = _fixture(acceptance, tmp_path)
    try:
        outcome = _outcome(acceptance, _successful_report(acceptance, fixture), fixture)
        acceptance._print_outcome(outcome)  # noqa: SLF001
    finally:
        shutil.rmtree(fixture.root)

    captured = capsys.readouterr()
    assert "tool executions: 2" in captured.out
    assert "acceptance verdict: PASS" in captured.out
    assert fixture.first_nonce in captured.out
    assert captured.err == ""


def test_main_writes_requested_report_and_uses_success_exit(
    acceptance: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The CLI boundary writes its authoritative artifact before exiting successfully."""
    fixture = _fixture(acceptance, tmp_path)
    outcome = _outcome(acceptance, _successful_report(acceptance, fixture), fixture)

    async def successful_run(arguments: object) -> object:
        assert arguments is not None
        return outcome

    monkeypatch.setattr(acceptance, "run", successful_run)
    report_path = tmp_path / "cli-report.json"
    try:
        with pytest.raises(SystemExit) as exit_error:
            acceptance.main(["--report-path", str(report_path)])
    finally:
        shutil.rmtree(fixture.root)

    assert exit_error.value.code == 0
    assert json.loads(report_path.read_text(encoding="utf-8"))["verdict"] == "PASS"


def test_main_writes_runner_failure_when_initialization_fails(
    acceptance: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Failures after argument parsing retain a bounded artifact when requested."""

    async def failed_run(arguments: object) -> object:
        assert arguments is not None
        msg = "inert initialization failure"
        raise RuntimeError(msg)

    monkeypatch.setattr(acceptance, "run", failed_run)
    report_path = tmp_path / "runner-failure.json"
    with pytest.raises(SystemExit) as exit_error:
        acceptance.main(["--report-path", str(report_path)])

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert exit_error.value.code == 1
    assert payload["verdict"] == "FAIL — RUNNER"
    assert payload["runner_failure"] == {
        "error_type": "RuntimeError",
        "error_message": "inert initialization failure",
    }

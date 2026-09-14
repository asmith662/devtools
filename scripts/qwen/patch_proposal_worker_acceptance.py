# Copyright (c) 2026
# ruff: noqa: E402, E501, INP001, T201
"""Run one bounded live Qwen B-0009 patch-proposal acceptance."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import uuid4

_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))

from devtools.agents.conversation import (
    Conversation,
    ConversationMessage,
    InteractionSource,
)
from devtools.core.time import Duration, Stopwatch
from devtools.execution import Runtime
from devtools.models.interaction.providers import (
    LlamaCppInteraction,
    LlamaCppInteractionError,
)
from devtools.resources.commands import Command, CommandExecutor
from devtools.tools.filesystem import (
    ListRepositoryDirectoryTool,
    ReadRepositoryFileTool,
)
from experiments.qwen.patch_proposal_worker import (
    _BASELINE_FIXTURE,
    _SELECTION_STRESS_FIXTURE,
    PatchProposalError,
    QwenGroundingCorrection,
    QwenPatchProposalWorker,
    QwenPatchProposalWorkerResult,
    QwenSelectionMeasurements,
    UngroundedFinalResponseError,
    _PatchProposalFixture,
    coding_worker_task,
    create_patch_proposal_fixture,
    create_selection_stress_fixture,
    selection_stress_measurements,
    selection_stress_task,
)
from experiments.qwen.two_action_read_only_experiment import (
    QwenListDirectoryCycle,
    QwenReadOnlyCycle,
    QwenReadRepositoryFileCycle,
    ReadOnlyProposalError,
)
from scripts.qwen.llama_cpp_profile import QWEN38_27B_UD_IQ4_XS

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from devtools.core.paths import ResolvedPath
    from devtools.models.interaction import (
        ModelInteraction,
        ModelResponse,
        ModelTermination,
        ModelUsage,
    )


_DEFAULT_ENDPOINT = "http://127.0.0.1:8080"
_DEFAULT_MODEL = "qwen38-local"
_REPORT_SCHEMA = "qwen-b0009-live-acceptance/3"
_SERVICE_SCRIPT = Path(__file__).with_name("llama_cpp_service.py")
_CALLER_SOURCE = InteractionSource("qwen-b0009-live-acceptance")
_MAXIMUM_ACTIONS = 5
_SELECTION_STRESS_MAXIMUM_ACTIONS = 7
_MODEL_CONTEXT_CAPACITY_TOKENS = QWEN38_27B_UD_IQ4_XS.context_size
_FIXTURE_CHOICES = ("baseline", "selection-stress")


@dataclass(frozen=True, slots=True)
class B0009LiveReport:
    """Retain bounded facts from one real-provider attempt."""

    task: ConversationMessage
    history: tuple[ConversationMessage, ...]
    cycles: tuple[QwenReadOnlyCycle, ...]
    execution_actions: tuple[str, ...]
    execution_paths: tuple[str, ...]
    grounding_corrections: tuple[QwenGroundingCorrection, ...]
    model_terminations: tuple[ModelTermination | None, ...]
    model_usages: tuple[ModelUsage | None, ...]
    fixture: _PatchProposalFixture
    fixture_id: str
    maximum_actions: int
    maximum_output_tokens: int | None
    selection_measurements: QwenSelectionMeasurements | None
    result: QwenPatchProposalWorkerResult | None
    failure_category: str | None
    error_type: str | None
    error_message: str | None
    patch_evaluation: dict[str, bool | str | None]


@dataclass(frozen=True, slots=True)
class B0009LiveOutcome:
    """Retain the completed artifact facts after fixture cleanup."""

    report: B0009LiveReport
    persistent_service_status: str | None
    persistent_service_error_type: str | None
    persistent_service_error_message: str | None
    fixture_cleanup_succeeded: bool
    duration: Duration = field(default_factory=lambda: Duration.seconds(0))


def parse_arguments(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse one fixed service endpoint and caller-selected durable artifact path."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", default=_DEFAULT_ENDPOINT)
    parser.add_argument("--model", default=_DEFAULT_MODEL)
    parser.add_argument("--fixture", choices=_FIXTURE_CHOICES, default="baseline")
    parser.add_argument("--maximum-output-tokens", type=int)
    parser.add_argument("--report-path", required=True, type=Path)
    return parser.parse_args(arguments)


async def run_acceptance(  # noqa: PLR0913 - preserves explicit fixture-local collaborators.
    *,
    task: ConversationMessage,
    repository_root: ResolvedPath,
    interaction: ModelInteraction,
    fixture: _PatchProposalFixture = _BASELINE_FIXTURE,
    fixture_id: str | None = None,
    maximum_actions: int = _MAXIMUM_ACTIONS,
    maximum_output_tokens: int | None = None,
) -> B0009LiveReport:
    """Run the committed experiment once while retaining script-local diagnostics."""
    conversation = Conversation.new()
    cycles: list[QwenReadOnlyCycle] = []
    actions: list[str] = []
    paths: list[str] = []
    grounding_corrections: list[QwenGroundingCorrection] = []
    model_terminations: list[ModelTermination | None] = []
    model_usages: list[ModelUsage | None] = []
    report_fixture_id = fixture_id or _fixture_id(fixture)
    original_list = ListRepositoryDirectoryTool.execute
    original_read = ReadRepositoryFileTool.execute

    async def counted_list(tool: ListRepositoryDirectoryTool, path: ResolvedPath) -> object:
        actions.append("list_repository_directory")
        paths.append(_relative_path(path, repository_root))
        return await original_list(tool, path)

    async def counted_read(tool: ReadRepositoryFileTool, path: ResolvedPath) -> object:
        actions.append("read_repository_file")
        paths.append(_relative_path(path, repository_root))
        return await original_read(tool, path)

    def recorded_model_response(response: ModelResponse) -> None:
        model_terminations.append(response.termination)
        model_usages.append(response.usage)

    ListRepositoryDirectoryTool.execute = counted_list
    ReadRepositoryFileTool.execute = counted_read
    try:
        result = await QwenPatchProposalWorker(
            runtime=Runtime(),
            conversation=conversation,
            interaction=interaction,
            repository_root=repository_root,
            fixture=fixture,
            maximum_actions=maximum_actions,
            maximum_output_tokens=maximum_output_tokens,
            on_cycle_completed=cycles.append,
            on_model_response=recorded_model_response,
            on_grounding_correction=grounding_corrections.append,
        ).run(task)
    except asyncio.CancelledError:
        raise
    except Exception as error:  # noqa: BLE001 - artifact must retain live failure facts.
        return B0009LiveReport(
            task,
            tuple(conversation.history),
            tuple(cycles),
            tuple(actions),
            tuple(paths),
            tuple(grounding_corrections),
            tuple(model_terminations),
            tuple(model_usages),
            fixture,
            report_fixture_id,
            maximum_actions,
            maximum_output_tokens,
            _selection_measurements(fixture, tuple(cycles)),
            None,
            _failure_category(error),
            type(error).__name__,
            str(error),
            _patch_evaluation(error),
        )
    finally:
        ListRepositoryDirectoryTool.execute = original_list
        ReadRepositoryFileTool.execute = original_read
    return B0009LiveReport(
        task,
        tuple(conversation.history),
        tuple(cycles),
        tuple(actions),
        tuple(paths),
        tuple(grounding_corrections),
        tuple(model_terminations),
        tuple(model_usages),
        fixture,
        report_fixture_id,
        maximum_actions,
        maximum_output_tokens,
        _selection_measurements(fixture, tuple(cycles)),
        result,
        None,
        None,
        None,
        {
            "parse_valid": True,
            "permitted_target": True,
            "applied": True,
            "behavior_valid": True,
            "terminal_newline_canonicalized": result.terminal_newline_canonicalized,
            "reason": "accepted",
        },
    )


def _relative_path(path: ResolvedPath, root: ResolvedPath) -> str:
    """Retain only repository-relative execution facts in the durable report."""
    return path.value.relative_to(root.value).as_posix() or "."


def _failure_category(error: Exception) -> str:
    """Classify only this acceptance's bounded failure vocabulary."""
    if isinstance(error, LlamaCppInteractionError):
        return "PROVIDER"
    if isinstance(error, UngroundedFinalResponseError):
        return "UNGROUNDED_FINAL_RESPONSE"
    if isinstance(error, ReadOnlyProposalError):
        return "MODEL_CONFORMANCE"
    if isinstance(error, PatchProposalError):
        return _patch_failure_category(error)
    return "FRAMEWORK_BOUNDARY"


def _patch_failure_category(error: PatchProposalError) -> str:
    """Classify the fixture evaluator's distinct final-patch failure stages."""
    if "cannot apply" in str(error):
        return "PATCH_APPLICATION"
    if "does not satisfy" in str(error) or "unrelated" in str(error):
        return "BEHAVIORAL_VALIDATION"
    return "PATCH_CONFORMANCE"


def _patch_evaluation(error: Exception) -> dict[str, bool | str | None]:
    """Represent only the completed or failed host-side patch boundary."""
    if not isinstance(error, PatchProposalError):
        return {
            "parse_valid": None,
            "permitted_target": None,
            "applied": None,
            "behavior_valid": None,
            "terminal_newline_canonicalized": None,
            "reason": "not reached",
        }
    category = _failure_category(error)
    return {
        "parse_valid": category != "PATCH_CONFORMANCE",
        "permitted_target": category != "PATCH_CONFORMANCE",
        "applied": category not in {"PATCH_CONFORMANCE", "PATCH_APPLICATION"},
        "behavior_valid": False if category == "BEHAVIORAL_VALIDATION" else None,
        "terminal_newline_canonicalized": None,
        "reason": str(error),
    }


async def _persistent_status() -> str:
    """Observe the independently owned persistent service after the one attempt."""
    result = await CommandExecutor().execute(
        Command(sys.executable, (str(_SERVICE_SCRIPT), "status")),
    )
    output = (result.stdout or result.stderr).decode(errors="replace").strip()
    return output or "persistent service status produced no output"


async def run(arguments: argparse.Namespace) -> B0009LiveOutcome:
    """Run exactly one fixture-local attempt without owning service lifecycle."""
    fixture, fixture_factory, task_factory, maximum_actions = _fixture_configuration(
        arguments.fixture,
    )
    stopwatch = Stopwatch()
    with tempfile.TemporaryDirectory(prefix="devtools-qwen-b0009-") as directory:
        root = fixture_factory(Path(directory))
        status: str | None = None
        status_error: Exception | None = None
        cleanup_succeeded = False
        try:
            report = await run_acceptance(
                task=_live_task(task_factory),
                repository_root=root,
                interaction=LlamaCppInteraction(
                    endpoint=arguments.endpoint,
                    model=arguments.model,
                    source=InteractionSource("qwen"),
                ),
                fixture=fixture,
                fixture_id=arguments.fixture,
                maximum_actions=maximum_actions,
                maximum_output_tokens=arguments.maximum_output_tokens,
            )
            try:
                status = await _persistent_status()
            except Exception as error:  # noqa: BLE001 - observation cannot erase attempt facts.
                status_error = error
        finally:
            try:
                shutil.rmtree(root.value)
            except FileNotFoundError:
                pass
            else:
                cleanup_succeeded = True
        return B0009LiveOutcome(
            report,
            status,
            type(status_error).__name__ if status_error else None,
            str(status_error) if status_error else None,
            cleanup_succeeded,
            stopwatch.stop(),
        )


def _fixture_configuration(
    fixture_id: str,
) -> tuple[
    _PatchProposalFixture,
    Callable[[Path], ResolvedPath],
    Callable[[], ConversationMessage],
    int,
]:
    """Select one of the two committed experiment fixtures without a registry."""
    if fixture_id == "selection-stress":
        return (
            _SELECTION_STRESS_FIXTURE,
            create_selection_stress_fixture,
            selection_stress_task,
            _SELECTION_STRESS_MAXIMUM_ACTIONS,
        )
    return (
        _BASELINE_FIXTURE,
        create_patch_proposal_fixture,
        coding_worker_task,
        _MAXIMUM_ACTIONS,
    )


def _fixture_id(fixture: _PatchProposalFixture) -> str:
    """Name the only non-default fixture while preserving baseline compatibility."""
    return "selection-stress" if fixture is _SELECTION_STRESS_FIXTURE else "baseline"


def _live_task(
    task_factory: Callable[[], ConversationMessage] = coding_worker_task,
) -> ConversationMessage:
    """Create the committed task with an acceptance-specific caller provenance."""
    task = task_factory()
    return ConversationMessage.new(
        task.content,
        role=task.role,
        source=_CALLER_SOURCE,
    )


def _message_payload(message: ConversationMessage) -> dict[str, str]:
    """Serialize retained conversation facts without absolute repository paths."""
    return {"role": message.role.value, "source": message.source.value, "content": message.content}


def _cycle_payload(cycle: QwenReadOnlyCycle) -> dict[str, object]:
    """Serialize one accepted list/read cycle with its bounded projection."""
    payload: dict[str, object] = {
        "proposal": _message_payload(cycle.proposal),
        "relative_path": cycle.relative_path,
        "result_projection": cycle.result_projection,
        "follow_up": _message_payload(cycle.follow_up),
    }
    if isinstance(cycle, QwenListDirectoryCycle):
        payload["action"] = "list_repository_directory"
        payload["tool_type"] = "ListRepositoryDirectoryTool"
        payload["listing"] = {
            "entries": [
                {"name": entry.name, "kind": entry.kind.value}
                for entry in cycle.listing.entries
            ],
            "truncated": cycle.listing.truncated,
        }
    else:
        payload["action"] = "read_repository_file"
        payload["tool_type"] = "ReadRepositoryFileTool"
    return payload


def _usage_payload(usage: ModelUsage | None) -> dict[str, float | int | None] | None:
    """Serialize one optional provider-reported ModelUsage without estimation."""
    if usage is None:
        return None
    input_tokens = usage.input_tokens
    return {
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "total_tokens": usage.total_tokens,
        "input_context_utilization": (
            input_tokens / _MODEL_CONTEXT_CAPACITY_TOKENS
            if input_tokens is not None
            else None
        ),
    }


def _termination_payload(termination: ModelTermination | None) -> str | None:
    """Serialize one optional provider-neutral ModelTermination."""
    return termination.value if termination is not None else None


def _selection_measurements(
    fixture: _PatchProposalFixture,
    cycles: tuple[QwenReadOnlyCycle, ...],
) -> QwenSelectionMeasurements | None:
    """Retain relevance facts only for the fixed selection-stress fixture."""
    if fixture is _SELECTION_STRESS_FIXTURE:
        return selection_stress_measurements(cycles)
    return None


def _selection_payload(
    measurements: QwenSelectionMeasurements | None,
) -> dict[str, float | list[str] | None] | None:
    """Serialize fixed-fixture relevance facts without creating generic metrics."""
    if measurements is None:
        return None
    return {
        "required_files_read": list(measurements.required_files_read),
        "plausible_unnecessary_files_read": list(
            measurements.plausible_unnecessary_files_read,
        ),
        "clearly_irrelevant_files_read": list(
            measurements.clearly_irrelevant_files_read,
        ),
        "required_read_coverage": measurements.required_read_coverage,
        "acquisition_precision": measurements.acquisition_precision,
    }


def _cumulative_usage_payload(
    usages: tuple[ModelUsage | None, ...],
) -> dict[str, int | None]:
    """Sum a token field only when every model turn reported that field."""
    return {
        "input_tokens": _complete_usage_total(usages, "input_tokens"),
        "input_tokens_reported_turns": _reported_usage_turns(usages, "input_tokens"),
        "output_tokens": _complete_usage_total(usages, "output_tokens"),
        "output_tokens_reported_turns": _reported_usage_turns(usages, "output_tokens"),
        "total_tokens": _complete_usage_total(usages, "total_tokens"),
        "total_tokens_reported_turns": _reported_usage_turns(usages, "total_tokens"),
    }


def _complete_usage_total(
    usages: tuple[ModelUsage | None, ...],
    field: str,
) -> int | None:
    """Return an exact total only when no turn left the requested count unknown."""
    values = [
        value
        for usage in usages
        if usage is not None and (value := getattr(usage, field)) is not None
    ]
    return sum(values) if usages and len(values) == len(usages) else None


def _reported_usage_turns(usages: tuple[ModelUsage | None, ...], field: str) -> int:
    """Count turns that supplied one specific provider-reported token field."""
    return sum(
        usage is not None and getattr(usage, field) is not None for usage in usages
    )


def _verdict(outcome: B0009LiveOutcome) -> str:
    """Evaluate this one worker run without demanding a scripted navigation order."""
    report = outcome.report
    if report.failure_category is not None:
        return f"FAIL — {report.failure_category}"
    if report.result is None or outcome.persistent_service_error_type is not None:
        return "FAIL — RUNNER"
    read_paths = {
        cycle.relative_path
        for cycle in report.cycles
        if isinstance(cycle, QwenReadRepositoryFileCycle)
    }
    if not outcome.report.fixture.required_evidence_paths.issubset(read_paths):
        return "FAIL — RELEVANCE_SELECTION"
    return "PASS"


def _report_payload(outcome: B0009LiveOutcome) -> dict[str, object]:
    """Construct the authoritative local acceptance artifact."""
    report = outcome.report
    task_content = report.task.content
    return {
        "schema": _REPORT_SCHEMA,
        "verdict": _verdict(outcome),
        "fixture": {
            "id": report.fixture_id,
            "maximum_output_tokens": report.maximum_output_tokens,
            "logical_structure": [path for path, _ in report.fixture.files],
            "cleanup": "completed" if outcome.fixture_cleanup_succeeded else "failed",
        },
        "initial_task": _message_payload(report.task),
        "initial_task_secrecy": {
            "contains_target_path": report.fixture.target_path in task_content,
            "contains_test_path": report.fixture.test_path in task_content,
            "contains_target_filename": Path(report.fixture.target_path).name
            in task_content,
            "contains_test_filename": Path(report.fixture.test_path).name
            in task_content,
        },
        "model_responses": [
            _message_payload(message)
            for message in report.history
            if message.source == InteractionSource("qwen")
        ],
        "history": [_message_payload(message) for message in report.history],
        "accepted_tool_cycles": [_cycle_payload(cycle) for cycle in report.cycles],
        "grounding": {
            "required_read_paths": sorted(report.fixture.required_evidence_paths),
            "acquired_read_paths": [
                cycle.relative_path
                for cycle in report.cycles
                if isinstance(cycle, QwenReadRepositoryFileCycle)
            ],
            "corrections": [
                {
                    "premature_response": _message_payload(correction.premature_response),
                    "follow_up": _message_payload(correction.follow_up),
                    "acquired_paths": list(correction.acquired_paths),
                }
                for correction in report.grounding_corrections
            ],
        },
        "tool_executions": {
            "count": len(report.execution_actions),
            "actions": list(report.execution_actions),
            "relative_paths": list(report.execution_paths),
        },
        "measurements": {
            "model_turn_count": len(report.model_terminations),
            "model_termination_by_turn": [
                _termination_payload(termination)
                for termination in report.model_terminations
            ],
            "model_usage_by_turn": [
                _usage_payload(usage) for usage in report.model_usages
            ],
            "cumulative_reported_model_usage": _cumulative_usage_payload(
                report.model_usages,
            ),
            "model_context_capacity_tokens": _MODEL_CONTEXT_CAPACITY_TOKENS,
            "tool_action_budget": report.maximum_actions,
            "tool_action_budget_used": len(report.execution_actions),
            "directory_listing_count": sum(
                isinstance(cycle, QwenListDirectoryCycle) for cycle in report.cycles
            ),
            "file_read_count": sum(
                isinstance(cycle, QwenReadRepositoryFileCycle)
                for cycle in report.cycles
            ),
            "unique_path_count": len(set(report.execution_paths)),
            "repeated_path_count": len(report.execution_paths)
            - len(set(report.execution_paths)),
            "repository_projection_characters": sum(
                len(cycle.result_projection) for cycle in report.cycles
            ),
            "run_duration_seconds": outcome.duration.total_seconds,
            "selection": _selection_payload(report.selection_measurements),
        },
        "final_model_response": (
            report.result.final_patch
            if report.result is not None
            else _latest_assistant_content(report.history)
        ),
        "canonical_accepted_patch": (
            report.result.canonical_patch if report.result is not None else None
        ),
        "patch_evaluation": report.patch_evaluation,
        "failure": {
            "category": report.failure_category,
            "error_type": report.error_type,
            "error_message": report.error_message,
        },
        "persistent_service": {
            "status": outcome.persistent_service_status,
            "error_type": outcome.persistent_service_error_type,
            "error_message": outcome.persistent_service_error_message,
        },
    }


def _latest_assistant_content(history: tuple[ConversationMessage, ...]) -> str | None:
    """Return the exact last Qwen response retained before terminal failure."""
    return next(
        (
            message.content
            for message in reversed(history)
            if message.source == InteractionSource("qwen")
        ),
        None,
    )


def _write_report(path: Path, payload: dict[str, object]) -> None:
    """Atomically write one caller-selected local JSON artifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.{uuid4()}.tmp")
    try:
        with temporary_path.open("w", encoding="utf-8", newline="\n") as output:
            json.dump(payload, output, indent=2, sort_keys=True)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        temporary_path.replace(path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def _print_outcome(outcome: B0009LiveOutcome) -> None:
    """Print a concise secondary summary beside the durable JSON artifact."""
    print(f"acceptance verdict: {_verdict(outcome)}")
    print(f"tool actions: {', '.join(outcome.report.execution_actions) or 'none'}")
    print(f"tool paths: {', '.join(outcome.report.execution_paths) or 'none'}")
    print(f"persistent service status: {outcome.persistent_service_status or outcome.persistent_service_error_message}")


def main(arguments: Sequence[str] | None = None) -> None:
    """Run one live attempt and require durable reporting regardless of its verdict."""
    parsed = parse_arguments(arguments)
    try:
        outcome = asyncio.run(run(parsed))
    except Exception as error:
        payload = {
            "schema": _REPORT_SCHEMA,
            "verdict": "FAIL — RUNNER",
            "runner_failure": {"error_type": type(error).__name__, "error_message": str(error)},
        }
        _write_report(parsed.report_path, payload)
        raise SystemExit(1) from error
    _write_report(parsed.report_path, _report_payload(outcome))
    _print_outcome(outcome)
    raise SystemExit(0 if _verdict(outcome) == "PASS" else 1)


if __name__ == "__main__":
    main()

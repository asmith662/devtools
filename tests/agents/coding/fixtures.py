# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, PLR0915, PLR0912, C901 -- literal independent fault schedules
"""Authored non-application host configuration; contains no coding/repair loop."""

from __future__ import annotations

import asyncio
import difflib
import json
import sys
from typing import TYPE_CHECKING, Any

from devtools.agents.coding import CodingLimits, run_coding_agent
from devtools.agents.coding.repository import (
    CodingObjective,
    EditLimits,
    RepositoryCodingHost,
    write_source_changes,
)
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.corpus import define_repository_text_corpus
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
)
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.filesystem import TextFile, write
from devtools.tools.source import SourceScope

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from devtools.agents.coding.repository import SourceChange

SOURCE = "# π\ndef answer():\n    return 6\n"
GOOD = "# π\ndef answer():\n    return 7\n"
WRONG = "# π\ndef answer():\n    return 8\n"
UNKNOWN = "UNKNOWN EXTERNAL SOURCE\n"
CHECK = (
    'import runpy,sys; assert runpy.run_path("module.py")["answer"]() '
    '== 7; sys.stdout.buffer.write(b"checked:7\\n")'
)
SCENARIOS = (
    "success",
    "repair",
    "missing-context",
    "unadmitted-edit",
    "stale",
    "invalid-edit",
    "failed-check",
    "proposal-limit",
    "call-limit",
    "action-limit",
    "cancel-provider",
    "foreign-model",
    "lost-file-ack",
    "lost-git-ack",
    "completion-failed",
    "unknown-installed",
    "unknown-after-check",
    "restore-failed",
    "feedback-failed",
    "primary-and-completion",
    "partial-context",
    "required-context",
    "output-limit",
    "missing-id",
    "duplicate-ids",
    "batch-overflow",
    "partial-batch",
    "completion-check",
    "duplicate-arguments",
    "overlap",
    "two-edits",
    "completion-overrun",
    "completion-raised",
    "completion-cancelled",
    "cancel-check",
    "lost-check-ack",
)


class Model:
    """Literal native responses; no model inference or second agent algorithm."""

    source = InteractionSource("independent-bounded-coding")

    def __init__(self, root: Path, scenario: str) -> None:
        """Retain an explicit literal schedule and actual invocation inputs."""
        self.root, self.scenario = root, scenario
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Return predeclared native requests, including controlled unknown entry."""
        self.requests.append(request)
        number = len(self.requests)
        if number == 2 and self.scenario != "missing-context":
            last = request.prompt.messages[-1]
            assert last.role == "tool"
            assert last.tool_call_id == "read-1"
            disclosed = json.loads(last.content)
            assert disclosed["text"] == (
                "# \u03c0\ndef" if self.scenario == "partial-context" else SOURCE
            )
            assert disclosed["span"] == [
                0,
                7 if self.scenario == "partial-context" else len(SOURCE),
            ]
            assert disclosed["snapshot"]
            assert disclosed["version"]
        if number == 3 and self.scenario == "repair":
            last = request.prompt.messages[-1]
            assert last.tool_call_id == "edit-2"
            evidence = json.loads(last.content)
            assert evidence["passed"] is False
            assert evidence["checks"][0]["exit_code"] == 1
            assert evidence["sources"][0]["text"] == WRONG
            assert (
                evidence["sources"][0]["version"]
                != json.loads(request.prompt.messages[2].content)["version"]
            )
        if self.scenario == "cancel-provider":
            message = "provider outcome unknown"
            raise asyncio.CancelledError(message)
        if number == 1 and self.scenario != "missing-context":
            calls: tuple[ModelToolCall, ...] = (
                ModelToolCall(
                    "read_source",
                    json.dumps({"path": "module.py", "start": 0, "end": len(SOURCE)}),
                    None if self.scenario == "missing-id" else "read-1",
                ),
            )
            if self.scenario == "duplicate-ids":
                calls += calls
            elif self.scenario in {"batch-overflow", "partial-batch"}:
                calls += (
                    ModelToolCall(
                        "read_source",
                        json.dumps(
                            {
                                "path": "foreign.py"
                                if self.scenario == "partial-batch"
                                else "module.py",
                                "start": 0,
                                "end": 2,
                            },
                        ),
                        "read-2",
                    ),
                )
        elif number == 3 and self.scenario == "completion-check":
            calls = (ModelToolCall("validate_candidate", "{}", "check-3"),)
        else:
            if self.scenario == "stale":
                write(TextFile(resolve_path(self.root / "module.py"), UNKNOWN))
            old = "return 8" if number == 3 else "return 6"
            new = (
                "return 8"
                if number == 2 and self.scenario in {"repair", "proposal-limit"}
                else "return 7"
            )
            if self.scenario == "invalid-edit":
                old = "missing anchor"
            args = json.dumps(
                {
                    "path": "foreign.py"
                    if self.scenario == "unadmitted-edit"
                    else "module.py",
                    "old_text": old,
                    "new_text": new,
                },
            )
            if self.scenario == "duplicate-arguments":
                args = (
                    '{"path":"module.py","path":"foreign.py",'
                    '"old_text":"return 6","new_text":"return 7"}'
                )
            calls = (
                ModelToolCall(
                    "replace_source",
                    args,
                    "repair-3" if number == 3 else "edit-2",
                ),
            )
            if self.scenario == "overlap":
                calls += (ModelToolCall("replace_source", args, "edit-overlap"),)
            elif self.scenario == "two-edits":
                calls += (
                    ModelToolCall(
                        "replace_source",
                        json.dumps(
                            {
                                "path": "module.py",
                                "old_text": "# π",
                                "new_text": "# changed",
                            },
                        ),
                        "edit-comment",
                    ),
                )
        return ModelResponse(
            "literal requested coding step",
            InteractionSource("foreign")
            if self.scenario == "foreign-model"
            else self.source,
            tool_calls=calls,
            termination=ModelTermination.OUTPUT_LIMIT
            if self.scenario == "output-limit"
            else None,
        )


async def scenario(root: Path, name: str) -> dict[str, Any]:
    root = resolve_path(root).value
    path = resolve_path(root / "module.py")
    write(TextFile(path, SOURCE), overwrite=False)
    commands = CommandExecutor()
    for args in [
        ("init", "-q", "-b", "main"),
        ("config", "core.autocrlf", "false"),
        ("add", "--", "module.py"),
        (
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "Authored bounded task",
        ),
    ]:
        actual = await commands.execute(
            Command("git")
            .args(*args)
            .cwd(resolve_path(root))
            .with_timeout(Duration.seconds(20)),
        )
        assert actual.exit_code == 0
    address = RepositoryResourceAddress("module.py")
    repository = Repository.new()
    scope = SourceScope.observe(
        root=resolve_path(root),
        repository=repository,
        addresses=(address,),
        maximum_resource_bytes=8192,
    )
    discovery = discover_repository_resource_addresses(
        repository=repository,
        root=scope.root,
        maximum_resource_count=4,
        maximum_traversal_entry_count=128,
        requested_addresses=(address,),
    )
    corpus = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(address,),
    )
    from devtools.tools.checks import FixedCheck, FixedCheckPlan  # noqa: PLC0415

    code = "raise SystemExit(7)" if name == "failed-check" else CHECK
    fixed = (
        Command(sys.executable)
        .args("-I", "-B", "-c", code)
        .cwd(scope.root)
        .with_timeout(Duration.seconds(10))
    )
    checks = FixedCheckPlan(
        scope.root,
        (FixedCheck("behavior", fixed),),
        scope,
        CommandOutputPolicy(max_stdout_bytes=4096, max_stderr_bytes=4096),
    )
    objective = CodingObjective(
        "Make answer return integer 7, preserving other source.",
        scope,
        (address,),
        checks,
        EditLimits(1024, 8192, 4096, 4),
        8 if name == "partial-context" else 2048,
        32768,
    )
    entries: list[str] = []
    admitted: list[str | None] = []
    archived: dict[str, str | None] = {}
    failure = OSError("effect acknowledgment lost")
    completion_failure = ValueError("archive acknowledgment lost")

    async def authorize(call: ModelToolCall, _arguments: object) -> None:
        admitted.append(call.provider_call_id)

    async def apply(changes: tuple[SourceChange, ...]) -> None:
        entries.append("apply")
        if name == "lost-git-ack":
            patch = "".join(
                difflib.unified_diff(
                    SOURCE.splitlines(keepends=True),
                    GOOD.splitlines(keepends=True),
                    fromfile="a/module.py",
                    tofile="b/module.py",
                ),
            )
            applied = await commands.execute(
                Command("git")
                .args("apply", "-")
                .with_stdin(patch.encode())
                .cwd(scope.root)
                .with_timeout(Duration.seconds(10)),
            )
            assert applied.exit_code == 0
            raise failure
        write_source_changes(scope.root, changes)
        if name == "unknown-installed":
            write(TextFile(path, UNKNOWN))
        if name in {"lost-file-ack", "primary-and-completion"}:
            raise failure

    def archive(current: Mapping[RepositoryResourceAddress, str | None]) -> None:
        archived.update({str(k): v for k, v in current.items()})
        out = root / ".candidate"
        out.mkdir()
        write(
            TextFile(resolve_path(out / "module.py"), current[address] or ""),
            overwrite=False,
        )
        if name in {"completion-failed", "primary-and-completion"}:
            raise completion_failure

    def restore(selected: RepositoryResourceAddress, text: str | None) -> None:
        assert selected == address
        if name == "restore-failed":
            raise completion_failure
        assert text is not None
        write(TextFile(path, text))

    def readiness(_snapshot: object, _evidence: object) -> None:
        if name == "required-context":
            message = "Required host obligation remains unresolved"
            raise ValueError(message)

    host = RepositoryCodingHost(
        objective,
        corpus=corpus,
        authorize=authorize,
        apply_changes=apply,
        archive=archive,
        restore=restore,
        readiness=readiness,
    )
    feedback = host.feedback

    async def report(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401 -- controlled post-validation reporting fault
        await feedback(*args, **kwargs)
        if name == "unknown-after-check":
            write(TextFile(path, UNKNOWN))
        if name == "feedback-failed":
            raise completion_failure

    host.feedback = report  # type: ignore[method-assign]
    finish = host.finish

    async def terminal(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401 -- a lost terminal acknowledgment after real restoration
        await finish(*args, **kwargs)
        if name == "completion-cancelled":
            message = "terminal acknowledgment interrupted"
            raise asyncio.CancelledError(message)
        raise completion_failure

    if name in {"completion-raised", "completion-cancelled"}:
        host.finish = terminal  # type: ignore[method-assign]
    check = host.check

    async def interrupted_check(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401 -- real completed check with interrupted acknowledgment
        await check(*args, **kwargs)
        if name == "cancel-check":
            message = "validation acknowledgment interrupted"
            raise asyncio.CancelledError(message)
        raise failure

    if name in {"cancel-check", "lost-check-ack"}:
        host.check = interrupted_check  # type: ignore[method-assign]
    model = Model(root, name)
    one_proposal = name not in {"repair", "completion-check"}
    limits = CodingLimits(
        1 if name in {"call-limit", "action-limit", "batch-overflow"} else 4,
        1 if one_proposal else 2,
        0 if name == "action-limit" else 1 if name == "batch-overflow" else 4,
        Duration.seconds(5),
        Duration.seconds(30),
        name in {"completion-check", "completion-overrun"},
    )
    result = await run_coding_agent(model, limits=limits, host=host)
    return {
        "scenario": name,
        "accepted": result.accepted,
        "disposition": result.disposition,
        "candidate_validated": result.candidate_validated,
        "completed": result.completed,
        "error": type(result.error).__name__ if result.error else None,
        "original_effect_error": result.error is failure,
        "completion_error": type(result.completion_error).__name__
        if result.completion_error
        else None,
        "failure_phase": result.failure_phase,
        "restored": result.custody.restored,
        "reconciliation": result.custody.reconciliation_required,
        "model_calls": result.progress.model_calls,
        "proposals": result.progress.proposals,
        "actions": result.progress.actions,
        "effects": [
            {
                "kind": e.kind,
                "ids": e.native_call_ids,
                "ack": e.acknowledged,
                "check": e.check_name,
            }
            for e in result.progress.effects
        ],
        "usage": [None if u is None else "observed" for u in result.progress.usage],
        "source": path.value.read_text(encoding="utf-8"),
        "archive": archived,
        "apply_entries": entries,
        "admitted": admitted,
        "checks": [
            [
                {
                    "exit": r.command_result.exit_code,
                    "stdout": r.command_result.stdout.decode(),
                    "passed": r.passed,
                    "argv": r.command_result.command.argv,
                }
                for r in batch
            ]
            for batch in host.check_results
        ],
        "feedback_ids": [m.tool_call_id for m in host.messages if m.role == "tool"],
        "request_count": len(model.requests),
        "framework": run_coding_agent.__code__.co_filename,
    }

# Copyright (c) 2026
"""One deterministic inspect/scope/select/check/reinspect developer procedure."""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from devtools.observability.commands.inspection import completed_observation
from devtools.observability.commands.models import (
    CommandObservation,
    CommandOrigin,
    CommandPattern,
)
from devtools.tools import ToolRunner
from devtools.tools.checks import FixedCheckPlan, FixedCheckResult, FixedCheckTool
from devtools.tools.errors import ToolInputError
from devtools.tools.repository.git import GitInspection, GitInspectionTool

if TYPE_CHECKING:
    from devtools.context import RepositoryResourceAddress

_CHECK_PATTERN = CommandPattern(
    "check",
    "fixed",
    ("opaque",),
    (),
    "tools.checks.FixedCheckTool",
)


@dataclass(frozen=True, slots=True)
class CheckSelection:
    """Run one fixed check always, or when an explicit path set intersects changes."""

    name: str
    changed_paths: frozenset[RepositoryResourceAddress] = frozenset()
    pattern: CommandPattern = _CHECK_PATTERN


@dataclass(frozen=True, slots=True)
class ChangeValidationPlan:
    """Host-authored scope, fixed checks and a finite deterministic selection rule."""

    checks: FixedCheckPlan
    expected_revision: str
    allowed_changes: frozenset[RepositoryResourceAddress]
    selection: tuple[CheckSelection, ...]
    environment_names: frozenset[str] = frozenset()
    stop_on_failure: bool = True

    def __post_init__(self) -> None:
        """Refuse mutable/unknown selections and unadmitted environment overrides."""
        if (
            not re.fullmatch("(?:[0-9a-f]{40}|[0-9a-f]{64})", self.expected_revision)
            or not isinstance(self.allowed_changes, frozenset)
            or not isinstance(self.selection, tuple)
            or not self.selection
            or len({s.name for s in self.selection}) != len(self.selection)
            or not isinstance(self.environment_names, frozenset)
            or any(not isinstance(s.changed_paths, frozenset) for s in self.selection)
        ):
            msg = "Change validation requires an immutable bounded host plan."
            raise ValueError(msg)
        for selection in self.selection:
            self.checks.select(selection.name)
        if any(
            set(c.command.environment or ()) - self.environment_names
            for c in self.checks.checks
        ):
            msg = "Fixed command environment override is outside the host allowlist."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class CheckExecution:
    """Known bounded result or unavailable acknowledgment, with original failure."""

    name: str
    status: Literal["passed", "failed", "unknown", "cancelled"]
    result: FixedCheckResult | None = None
    error: BaseException | None = None


@dataclass(frozen=True, slots=True)
class ChangeValidationReport:
    """Consolidated evidence, never acceptance/review/publication authority.

    Full bounded CommandResults stay available to the selected caller. Analytics
    observations omit their argv, output, environment and exception payloads.
    """

    status: Literal["passed", "failed", "skipped", "refused", "incomplete", "cancelled"]
    before: GitInspection | None
    after: GitInspection | None
    checks: tuple[CheckExecution, ...]
    observations: tuple[CommandObservation, ...]
    reason: str | None = None
    error: BaseException | None = None


class InspectAndValidateTool:
    """Execute one host-fixed procedure through existing Git/Tool/Command owners."""

    name = "inspect_and_validate_change"
    description = (
        "Inspect scope, execute selected fixed checks and report known evidence."
    )

    def __init__(self, plan: ChangeValidationPlan, *, origin: CommandOrigin) -> None:
        """Bind explicit host policy; model input cannot supply commands or scope."""
        self.plan, self.origin = plan, origin
        self.inspection = GitInspectionTool(plan.checks.root, origin=origin)
        self.check_tool = FixedCheckTool(plan.checks)
        self.last_report: ChangeValidationReport | None = None
        self._entered = False

    def validate(self, arguments: None) -> None:
        """Accept only the already selected host procedure."""
        if arguments is not None or self._entered:
            msg = (
                "Change validation takes no model-selected scope and requires "
                "one fresh host origin/Tool instance per invocation."
            )
            raise ToolInputError(msg)

    async def execute(self, arguments: None) -> ChangeValidationReport:  # noqa: C901, PLR0912 -- one explicit bounded procedure, no workflow engine
        """Run once, preserve partial results, and propagate caller cancellation."""
        del arguments
        self._entered = True
        before = after = None
        checks: list[CheckExecution] = []
        observations: list[CommandObservation] = []
        status: Literal[
            "passed",
            "failed",
            "skipped",
            "refused",
            "incomplete",
            "cancelled",
        ] = "incomplete"
        reason: str | None = None
        failure: BaseException | None = None
        try:
            before = await ToolRunner().execute(self.inspection, None)
            paths = {
                p
                for c in before.changes
                for p in (c.path, c.original_path)
                if p is not None
            }
            if (
                not before.stable
                or before.revision != self.plan.expected_revision
                or paths - {p.value for p in self.plan.allowed_changes}
                or any(c.unmerged for c in before.changes)
            ):
                status, reason = "refused", "repository_scope_or_revision"
            else:
                status = "passed"
                for index, selection in enumerate(self.plan.selection):
                    if selection.changed_paths and not paths.intersection(
                        p.value for p in selection.changed_paths
                    ):
                        continue
                    origin = CommandOrigin(
                        self.origin.agent,
                        self.origin.task,
                        self.origin.run,
                        self.origin.call + "/check-" + str(index),
                    )
                    pattern = selection.pattern
                    try:
                        result = await ToolRunner().execute(
                            self.check_tool,
                            selection.name,
                        )
                    except (Exception, asyncio.CancelledError) as error:
                        observations.append(
                            CommandObservation(
                                origin,
                                pattern,
                                "framework-result",
                                outcome="cancelled"
                                if isinstance(error, asyncio.CancelledError)
                                else "unknown",
                            ),
                        )
                        checks.append(
                            CheckExecution(
                                selection.name,
                                "cancelled"
                                if isinstance(error, asyncio.CancelledError)
                                else "unknown",
                                error=error,
                            ),
                        )
                        raise
                    checks.append(
                        CheckExecution(
                            selection.name,
                            "passed" if result.passed else "failed",
                            result,
                        ),
                    )
                    observations.append(
                        completed_observation(
                            result.command_result,
                            origin=origin,
                            pattern=pattern,
                        ),
                    )
                    if not result.passed:
                        status = "failed"
                        if self.plan.stop_on_failure:
                            break
                after = await ToolRunner().execute(self.inspection, None)
                if not checks:
                    status = "skipped"
                if self.plan.checks.source_scope is not None:
                    self.plan.checks.source_scope.check_current()
                if not after.stable or before != after:
                    status, reason = "incomplete", "repository_changed_during_checks"
        except (Exception, asyncio.CancelledError) as error:
            failure = error
            status = (
                "cancelled"
                if isinstance(error, asyncio.CancelledError)
                else "incomplete"
            )
            reason = "command_or_inspection_incomplete"
            if isinstance(error, asyncio.CancelledError):
                raise
        finally:
            self.last_report = ChangeValidationReport(
                status,
                before,
                after,
                tuple(checks),
                (*self.inspection.observations, *observations),
                reason,
                failure,
            )
        return self.last_report

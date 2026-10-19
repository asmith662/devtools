# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, SLF001 -- concrete backlog/Qwen composition
"""One coordinator-owned B-item assignment through the existing Qwen coding loop.

Receipt hashes bind scope and evidence, not human authority. Trusted hosts must
authorize exact implementation grants and recheck them at dispatch. Integration
phases separately consume standing integration authority; coding grants never
confer commit, promotion or canonical backlog-close authority.
"""

from __future__ import annotations

import difflib
import hashlib
import re
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from apps.qwen.coding_loop import run_coding_task
from apps.qwen.development_task import _hash
from apps.qwen.patch_proposal_worker import _read_text
from apps.qwen.tasks import CodingTask
from devtools.core.paths import resolve_path
from devtools.core.time import Stopwatch, Timestamp
from devtools.resources.filesystem import TextFile, write
from scripts.backlog.checkout import Checkout, idle
from scripts.backlog.coordinator import git, locate
from scripts.backlog.intake import Intake, _digest, load_json

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from pathlib import Path

    from devtools.models.interaction import ModelInteraction
    from scripts.backlog.integration import Integration

SCOPE = "bounded-local-qwen-implementation; review candidate only; no integration"


def _digest_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def same_backlog(
    left: dict[str, Any], right: dict[str, Any], *, relocated: bool = False
) -> bool:
    """Authenticate scope across Git newline materialization, never new decisions."""
    represented = {"text", "item_sha256"} | ({"path"} if relocated else set())
    return (
        {k: v for k, v in left.items() if k not in represented}
        == {k: v for k, v in right.items() if k not in represented}
        and left["text"].replace("\r\n", "\n") == right["text"].replace("\r\n", "\n")
        and left["item_sha256"] == _digest(left["text"])
        and right["item_sha256"] == _digest(right["text"])
    )


def task_from_dict(value: dict[str, Any]) -> CodingTask:
    """Decode exactly the existing host task definition, never an execution DSL."""
    return CodingTask(
        **{
            **value,
            "tests": tuple(value["tests"]),
            "baseline_hashes": tuple(tuple(v) for v in value["baseline_hashes"]),
            "context": tuple(tuple(v) for v in value["context"]),
            "read_paths": tuple(value.get("read_paths", ())),
            "additional_edit_paths": tuple(value.get("additional_edit_paths", ())),
            "api_targets": tuple(value.get("api_targets", ())),
        }
    )


def _load(path: Path, schema: str) -> dict[str, Any]:
    value = load_json(path)
    digest = value.pop("sha256")
    if value["schema"] != schema or _digest(value) != digest:
        raise ValueError("Work receipt identity/schema mismatch")
    return {**value, "sha256": digest}


class WorkCycle:
    """Prepare/authorize/dispatch one bounded assignment per canonical work item."""

    def __init__(self, coordinator: Path) -> None:
        """Select the host coordinator; every mutation rechecks Git designation."""
        self.root = resolve_path(coordinator).value
        self.intake = Intake(self.root, coordinator=self.root)
        self._checkout: Checkout | None = None

    @property
    def integration(self) -> Integration:
        """Expose the maintained integration phases of this same work lifecycle."""
        from scripts.backlog.integration import Integration  # noqa: PLC0415

        return Integration(self)

    async def _coordinator(self) -> None:
        if await locate(self.root) != self.root:
            raise PermissionError(
                "Work administration must run in the designated coordinator"
            )

    def _folder(self, item: str) -> Path:
        if not re.fullmatch(r"B-\d{4}", item):
            raise PermissionError("An approved canonical B-number is required")
        return self.intake._path(".local/backlog/work/" + item)

    def _save(self, path: Path, value: dict[str, Any]) -> dict[str, Any]:
        sealed = {**value, "sha256": _digest(value)}
        self.intake._save(path, sealed)
        return sealed

    async def _target(self, target: Path, branch: str, task: CodingTask) -> None:
        if target != self.root:
            raise PermissionError(
                "Implementation target must be the canonical coordinator"
            )
        if branch in {"main", "master"} or not branch.startswith("feat/"):
            raise PermissionError("A named ordinary feature branch is required")
        if (
            await git(
                target, "for-each-ref", "--format=%(objectname)", "refs/heads/" + branch
            )
            != task.baseline_revision
        ):
            raise PermissionError("Target/base revision changed")
        await idle(target)
        if (
            self.root / ".local/backlog/checkout-owner"
        ).exists() and self._checkout is None:
            raise PermissionError("Checkout owned; explicit recovery required")
        for relative, digest in task.baseline_hashes:
            await self._baseline(task, relative, digest)

    async def _baseline(self, task: CodingTask, relative: str, digest: str) -> str:
        from scripts.backlog.integration.git import blob  # noqa: PLC0415

        text = (await blob(self.root, task.baseline_revision, relative)).replace(
            "\r\n", "\n"
        )
        for candidate in (text, text.replace("\n", "\r\n")):
            if _digest_text(candidate) == digest:
                return candidate
        raise PermissionError("Task source/test identity differs from target")

    async def prepare(
        self, item: str, *, target: Path, branch: str, task: CodingTask
    ) -> dict[str, Any]:
        """Freeze reviewed work and exact task/target; this creates no authority."""
        await self._coordinator()
        target = resolve_path(target).value
        binding = self.intake.approved_item(item)
        if task.additional_edit_paths:
            raise PermissionError(
                "Governed assignment-v1 remains one-file; "
                "use exact authorized local scope"
            )
        if task.source not in binding["proposal"]["payload"]["resources"]:
            raise PermissionError(
                "Edit target is outside the reviewed proposal resources"
            )
        await self._target(target, branch, task)
        folder = self._folder(item)
        with self.intake._writer():
            # One slot per B-number, including failed/uncertain dispatches. No
            # new run identity is invented and no previous attempt is retried.
            folder.parent.mkdir(parents=True, exist_ok=True)
            folder.mkdir()
            return self._save(
                folder / "assignment.json",
                {
                    "schema": "backlog-qwen-assignment-v1",
                    "item": item,
                    "prepared_at": str(Timestamp.now()),
                    "coordinator": str(self.root),
                    "backlog": binding,
                    "target": str(target),
                    "branch": branch,
                    "base_head": task.baseline_revision,
                    "task": asdict(task),
                    "baseline_source": await self._baseline(
                        task, task.source, dict(task.baseline_hashes)[task.source]
                    ),
                    "task_sha256": task.definition_sha256,
                    "allowed_files": [task.source],
                    "actions": {
                        "tool": "propose_edit",
                        "per_call": 1,
                        "total": min(task.maximum_calls, 3),
                        **(
                            {
                                "read_only_context_tools": 8,
                                "model_calls_total": task.maximum_calls,
                            }
                            if task.context_mode == "on-demand"
                            else {}
                        ),
                    },
                    "scope": SCOPE,
                    "execution_authorized": False,
                },
            )

    async def _validate(self, assignment: dict[str, Any]) -> CodingTask:
        await self._coordinator()
        if assignment["coordinator"] != str(self.root) or assignment["scope"] != SCOPE:
            raise PermissionError("Assignment coordinator/scope changed")
        if self._checkout is None:
            binding = self.intake.approved_item(assignment["item"])
        else:
            # The administrative backlog was authenticated before switching.
            # An older implementation base need not contain its later approval.
            owner = self._checkout.record
            if (
                await git(self.root, "rev-parse", owner["return_branch"])
                != owner["return_head"]
            ):
                raise PermissionError("Administrative backlog revision changed")
            binding = assignment["backlog"]
        if not same_backlog(binding, assignment["backlog"]):
            raise PermissionError(
                "Backlog status/content/review changed after preparation"
            )
        task = task_from_dict(assignment["task"])
        if (
            task.definition_sha256 != assignment["task_sha256"]
            or task.baseline_revision != assignment["base_head"]
            or assignment["allowed_files"] != [task.source]
            or task.source not in binding["proposal"]["payload"]["resources"]
        ):
            raise PermissionError("Frozen task definition changed")
        await self._target(
            resolve_path(assignment["target"]).value, assignment["branch"], task
        )
        return task

    async def authorize(
        self,
        item: str,
        *,
        principal: str,
        reference: str,
        expires_at: Timestamp,
        authorize: Callable[[dict[str, Any]], bool] | None = None,
    ) -> dict[str, Any]:
        """Record separately authenticated implementation authority, default deny."""
        folder = self._folder(item)
        assignment = _load(folder / "assignment.json", "backlog-qwen-assignment-v1")
        await self._validate(assignment)
        now = Timestamp.now()
        if (
            not principal.strip()
            or not reference.strip()
            or expires_at.value <= now.value
        ):
            raise PermissionError(
                "Explicit principal, provenance and future expiry required"
            )
        grant = {
            "schema": "backlog-qwen-authorization-v1",
            "item": item,
            "assignment_sha256": assignment["sha256"],
            "scope": SCOPE,
            "principal": principal,
            "decision_reference": reference,
            "issued_at": str(now),
            "expires_at": str(expires_at),
        }
        if authorize is None or not authorize(
            {"assignment": assignment, "grant": grant}
        ):
            raise PermissionError("Separate host implementation authorization required")
        await self._validate(assignment)
        if Timestamp.now().value >= expires_at.value:
            raise PermissionError("Implementation authority expired before publication")
        with self.intake._writer():
            return self._save(folder / "authorization.json", grant)

    async def execute(
        self,
        item: str,
        *,
        interaction_factory: Callable[
            [], Awaitable[tuple[ModelInteraction, dict[str, Any]]]
        ],
        authorize: Callable[[dict[str, Any]], bool] | None = None,
    ) -> dict[str, Any]:
        """Own the canonical source while the existing bounded worker executes."""
        folder = self._folder(item)
        assignment = _load(folder / "assignment.json", "backlog-qwen-assignment-v1")
        await self._validate(assignment)
        if (folder / "dispatch.json").exists():
            raise PermissionError("Prior dispatch exists; reconcile, never redispatch")
        async with Checkout(
            self,
            "coding:" + assignment["sha256"],
            assignment["branch"],
            assignment["base_head"],
            files=[
                {
                    "path": assignment["task"]["source"],
                    "text": assignment["baseline_source"],
                }
            ],
        ) as checkout:
            self._checkout = checkout
            try:
                return await self._execute(
                    item, interaction_factory=interaction_factory, authorize=authorize
                )
            finally:
                self._checkout = None

    async def _execute(  # noqa: C901 -- manual/delegated admission to one executor
        self,
        item: str,
        *,
        interaction_factory: Callable[
            [], Awaitable[tuple[ModelInteraction, dict[str, Any]]]
        ],
        authorize: Callable[[dict[str, Any]], bool] | None = None,
    ) -> dict[str, Any]:
        """Revalidate, claim once, and compose run_coding_task without another loop."""
        stopwatch = Stopwatch()
        folder = self._folder(item)
        assignment = _load(folder / "assignment.json", "backlog-qwen-assignment-v1")
        task = await self._validate(assignment)
        if not (folder / "authorization.json").exists():
            raise PermissionError("Missing separate implementation authorization")
        grant = _load(folder / "authorization.json", "backlog-qwen-authorization-v1")
        now = Timestamp.now()
        if (
            grant["item"] != item
            or grant["assignment_sha256"] != assignment["sha256"]
            or grant["scope"] != SCOPE
            or not Timestamp.from_isoformat(grant["issued_at"]).value
            <= now.value
            < Timestamp.from_isoformat(grant["expires_at"]).value
        ):
            raise PermissionError(
                "Missing, stale or mismatched implementation authority"
            )
        delegated = "delegation" in grant
        if delegated:
            from scripts.backlog.delegation import Delegations  # noqa: PLC0415

            Delegations(self).authority(grant, assignment, task)
        elif authorize is None or not authorize(
            {"assignment": assignment, "grant": grant}
        ):
            raise PermissionError(
                "Current host authority required before Qwen dispatch"
            )
        # Terminal consent may take time. Recheck freshness and source after it,
        # rather than admitting against the pre-prompt state.
        task = await self._validate(assignment)
        now = Timestamp.now()
        if now.value >= Timestamp.from_isoformat(grant["expires_at"]).value:
            raise PermissionError("Implementation authority expired before admission")
        with self.intake._writer():
            if delegated:
                Delegations(self).authority(grant, assignment, task)
            if (folder / "dispatch.json").exists() or (folder / "worker").exists():
                raise PermissionError(
                    "Prior dispatch exists; reconcile, never blindly redispatch"
                )
            self._save(
                folder / "dispatch.json",
                {
                    "schema": "backlog-qwen-dispatch-v1",
                    "item": item,
                    "authorization_sha256": grant["sha256"],
                    "at": str(now),
                    "disposition": "DISPATCH_CLAIMED; NOT_PROOF_OF_MODEL_ENTRY",
                },
            )
        target = resolve_path(assignment["target"]).value
        worker: dict[str, Any] | None = None
        error = None
        try:
            interaction, provenance = await interaction_factory()
            if delegated:
                authority = Delegations(self)
                authority.model(grant, provenance)
                interaction = authority.guard(grant, task, interaction)
            worker = await run_coding_task(
                target,
                folder / "worker",
                interaction,
                task=task,
                provenance={
                    **provenance,
                    "backlog_item": item,
                    "assignment_sha256": assignment["sha256"],
                    "authorization_sha256": grant["sha256"],
                },
                admit_edit=self._checkout.expect if self._checkout else None,
            )
            if (
                delegated
                and (authority.folder(grant["delegation"]) / "blocked.json").exists()
            ):
                error = "Delegated provider exceeded requested output allowance"
        except Exception as failure:  # noqa: BLE001 -- retain ambiguity; never redispatch
            error = f"{type(failure).__name__}: {failure}"
        result = await self._closeout(assignment, grant, worker, error)
        result["execution_elapsed_seconds"] = stopwatch.stop().total_seconds
        with self.intake._writer():
            return self._save(folder / "result.json", result)

    async def _closeout(
        self,
        assignment: dict[str, Any],
        grant: dict[str, Any],
        worker: dict[str, Any] | None,
        error: str | None,
    ) -> dict[str, Any]:
        item = assignment["item"]
        task = task_from_dict(assignment["task"])
        folder = self._folder(item)
        target = resolve_path(assignment["target"]).value
        original = assignment["baseline_source"]
        final = folder / "worker/final-source.py"
        changed: list[str] = []
        final_hash = None
        diff_path = None
        if final.exists():
            text = _read_text(resolve_path(final)).content
            final_hash = _hash(final)
            if text != original:
                changed = [task.source]
                diff_path = str(folder / "candidate.patch")
                diff = "".join(
                    difflib.unified_diff(
                        original.splitlines(keepends=True),
                        text.splitlines(keepends=True),
                        fromfile="a/" + task.source,
                        tofile="b/" + task.source,
                    )
                )
                write(TextFile(resolve_path(diff_path), diff), overwrite=False)
        unchanged = await git(target, "rev-parse", "HEAD") == assignment[
            "base_head"
        ] and not await git(target, "status", "--porcelain", "--untracked-files=no")
        last = worker["turns"][-1] if worker and worker["turns"] else {}
        validation = last.get("validation", {})
        accepted = bool(
            worker
            and not error
            and worker["accepted"]
            and unchanged
            and worker["workspace_removed"]
            and worker["original_unchanged"]
            and worker["task_definition_sha256"] == assignment["task_sha256"]
            and last.get("source_after") == final_hash
            and validation.get("accepted")
            and changed
        )
        return {
            "schema": "backlog-qwen-result-v1",
            "objective": task.objective,
            "item": item,
            "assignment_sha256": assignment["sha256"],
            "authorization_sha256": grant["sha256"],
            "decision_reference": grant["decision_reference"],
            "base_head": assignment["base_head"],
            "branch": assignment["branch"],
            "target": str(target),
            "allowed_files": assignment["allowed_files"],
            "candidate_changed_files": changed,
            "target_unchanged": unchanged,
            "baseline_sha256": dict(task.baseline_hashes)[task.source],
            "candidate_sha256": final_hash,
            "diff": diff_path,
            "worker_result": str(folder / "worker/result.json"),
            "validation": validation,
            "usage": worker["usage_totals"] if worker else None,
            "worker_elapsed_seconds": worker["elapsed_seconds"] if worker else None,
            "validation_seconds": worker["validation_seconds"] if worker else None,
            "repair_cycles": worker["repair_cycles"] if worker else None,
            "model_calls": worker["model_calls_attempted"] if worker else None,
            "worker_disposition": worker["disposition"]
            if worker
            else "UNKNOWN_NOT_RETRIED",
            "error": error or (worker.get("error") if worker else None),
            "disposition": "REVIEW_CANDIDATE" if accepted else "ESCALATION_REQUIRED",
            "reviewer_recommendation": "ADVISORY: review for integration"
            if accepted
            else "ADVISORY: escalate; preserve failure",
            "integration_authorized": False,
            "canonical_item_closed": False,
            "finished_at": str(Timestamp.now()),
        }

    def status(self, item: str) -> dict[str, Any]:
        """Read evidence; missing completion never establishes zero model calls."""
        folder = self._folder(item)
        _load(folder / "assignment.json", "backlog-qwen-assignment-v1")
        if (folder / "result.json").exists():
            result = _load(folder / "result.json", "backlog-qwen-result-v1")
            plans = folder / "integration"
            if plans.exists():
                result = {
                    **result,
                    "integration": [
                        self.integration.status(item, p.name)
                        for p in sorted(plans.iterdir())
                        if p.is_dir()
                    ],
                }
            return result
        return {
            "item": item,
            "disposition": "RECONCILIATION_REQUIRED"
            if (folder / "dispatch.json").exists()
            else "AWAITING_IMPLEMENTATION_AUTHORITY_OR_DISPATCH",
            "model_usage": "UNKNOWN",
        }

    async def discover(self, item: str, payload: dict[str, Any]) -> str:
        """Forward a caller observation to intake without changing the assignment."""
        await self._coordinator()
        assignment = _load(
            self._folder(item) / "assignment.json", "backlog-qwen-assignment-v1"
        )
        if payload["parent"] not in {None, item}:
            raise ValueError("Discovery parent differs from assigned work")
        return self.intake.capture(
            {
                **payload,
                "parent": item,
                "evidence": [
                    *payload["evidence"],
                    f"work:{item}#assignment-sha256={assignment['sha256']}",
                ],
            }
        )

# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, SLF001, PLR2004 -- concrete WorkCycle integration
"""Candidate to verified destination and canonical backlog progress.

Each immutable intent precedes its effect. Re-entry inspects exact Git objects
and refs, never creates a replacement commit or overwrites divergent work.
"""

from __future__ import annotations

import difflib
import getpass
import hashlib
import re
from typing import TYPE_CHECKING, Any, cast

from devtools.context import RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.resources.filesystem import TextFile, write
from scripts.backlog.checkout import Checkout
from scripts.backlog.checkout import untracked as untracked_files
from scripts.backlog.coordinator import common_directory, git
from scripts.backlog.intake import _digest, _read
from scripts.backlog.integration.authority import IntegrationAuthority
from scripts.backlog.integration.git import blob, clean, publish, remote_head
from scripts.backlog.integration.validation import validate_tree
from scripts.backlog.work import _load, same_backlog, task_from_dict

if TYPE_CHECKING:
    from pathlib import Path

    from apps.qwen.tasks import CodingTask
    from scripts.backlog.work import WorkCycle


def digest_text(value: str) -> str:
    """Identify exact encoded source, not a semantic RI identity."""
    return hashlib.sha256(value.encode()).hexdigest()


def independent_files(
    files: list[dict[str, Any]],
    additions: list[dict[str, str]],
    source: str,
    *,
    allow_source: bool = True,
) -> list[dict[str, Any]]:
    """Admit bounded independently attributed additions for both integration entries."""
    if not isinstance(additions, list) or len(additions) > 19:
        raise ValueError("Bounded independent test/correction additions required")
    if len({f["path"] for f in additions}) != len(additions):
        raise ValueError("Duplicate addition paths")
    for addition in additions:
        if (
            set(addition) != {"path", "text", "author", "reference"}
            or not addition["author"].strip()
            or addition["author"] == "Qwen"
            or not addition["reference"].strip()
            or not isinstance(addition["text"], str)
        ):
            raise ValueError("Independently authored additions require provenance")
        path = addition["path"]
        RepositoryResourceAddress(path)
        if not path.endswith(".py") or not (
            path.startswith("tests/") or (allow_source and path == source)
        ):
            raise PermissionError("Addition outside source/test boundary")
        files = [v for v in files if v["path"] != path]
        files.append({**addition, "sha256": digest_text(addition["text"])})
    return files


class Integration:
    """Implement the integration phases of the existing WorkCycle only."""

    def __init__(self, cycle: WorkCycle) -> None:
        """Reuse the coordinator and its state/atomic writer."""
        self.cycle = cycle
        self.authority = IntegrationAuthority(cycle)

    async def closeout_local(
        self,
        task: CodingTask,
        evidence: Path,
        **options: Any,  # noqa: ANN401 -- explicit local operator options forwarded unchanged
    ) -> dict[str, Any]:
        """Trusted local candidate entry; protected/backlog operations stay separate."""
        from scripts.backlog.integration.local import (  # noqa: PLC0415 -- avoid WorkCycle module cycle
            closeout_local,
        )

        return await closeout_local(self, task, evidence, **options)

    def folder(self, item: str, identity: str) -> Path:
        """Resolve an immutable plan within the existing work-item state."""
        if not re.fullmatch(r"[a-f0-9]{64}", identity):
            raise ValueError("Invalid integration plan identity")
        return self.cycle._folder(item) / "integration" / identity

    def record(self, item: str, identity: str, name: str) -> dict[str, Any]:
        """Read one closed phase receipt, validating its content hash."""
        return _load(
            self.folder(item, identity) / (name + ".json"),
            "backlog-integration-" + name + "-v1",
        )

    def save(
        self, item: str, identity: str, name: str, value: dict[str, Any]
    ) -> dict[str, Any]:
        """Append an immutable phase record; existing records are never replaced."""
        path = self.folder(item, identity) / (name + ".json")
        if path.exists():
            existing = self.record(item, identity, name)
            if any(existing.get(key) != v for key, v in value.items()):
                raise PermissionError("Recorded transition differs; reconcile first")
            return existing
        return self.cycle._save(
            path,
            {
                "schema": "backlog-integration-" + name + "-v1",
                "at": str(Timestamp.now()),
                **value,
            },
        )

    def candidate(self, item: str, review: str) -> dict[str, Any]:
        """Authenticate exact candidate/diff and the Codex result review."""
        folder = self.cycle._folder(item)
        assignment = _load(folder / "assignment.json", "backlog-qwen-assignment-v1")
        result = _load(folder / "result.json", "backlog-qwen-result-v1")
        if not re.fullmatch(r"[a-f0-9]{64}", review):
            raise ValueError("Invalid accepted review identity")
        decision = _load(
            folder / ("supervision-" + review + ".json"), "backlog-qwen-supervision-v1"
        )
        source = _read(folder / "worker/final-source.py")
        patch = _read(folder / "candidate.patch")
        expected = "".join(
            difflib.unified_diff(
                assignment["baseline_source"].splitlines(keepends=True),
                source.splitlines(keepends=True),
                fromfile="a/" + assignment["task"]["source"],
                tofile="b/" + assignment["task"]["source"],
            )
        )
        task = task_from_dict(assignment["task"])
        authorization = _load(
            folder / "authorization.json", "backlog-qwen-authorization-v1"
        )
        if (
            result["assignment_sha256"] != assignment["sha256"]
            or authorization["assignment_sha256"] != assignment["sha256"]
            or list(assignment["allowed_files"]) != [task.source]
            or digest_text(assignment["baseline_source"])
            != dict(task.baseline_hashes)[task.source]
            or result["authorization_sha256"] != authorization["sha256"]
            or result["disposition"] != "REVIEW_CANDIDATE"
            or result["candidate_changed_files"] != [task.source]
            or result["candidate_sha256"] != digest_text(source)
            or not result["validation"]["accepted"]
            or task.definition_sha256 != assignment["task_sha256"]
            or decision["sha256"] != review
            or decision["result_sha256"] != result["sha256"]
            or decision["assignment_sha256"] != assignment["sha256"]
            or decision["reviewer"] != "Codex"
            or decision["disposition"] != "ACCEPT_RECOMMENDED"
            or patch != expected
        ):
            raise PermissionError(
                "Candidate, diff or accepted supervision does not authenticate"
            )
        return {
            "assignment": assignment,
            "result": result,
            "review": decision,
            "source": source,
            "patch_sha256": digest_text(patch),
        }

    async def plan(  # noqa: C901, PLR0912 -- closed plan admission checks
        self, item: str, review: str, spec: dict[str, Any]
    ) -> dict[str, Any]:
        """Freeze a read-only destination-based plan; no grant is inferred."""
        await self.cycle._coordinator()
        candidate = self.candidate(item, review)
        assignment = candidate["assignment"]
        task = task_from_dict(assignment["task"])
        backlog = self.cycle.intake.approved_item(item)
        if not same_backlog(backlog, assignment["backlog"], relocated=True):
            raise PermissionError("Backlog changed; review the new scope explicitly")
        if set(spec) != {
            "remote",
            "destination",
            "feature",
            "checkout",
            "additions",
            "parent_complete",
            "remaining",
            "rationale",
            "validation_seconds",
        }:
            raise ValueError("Unsupported integration plan fields")
        for branch in (spec["destination"], spec["feature"]):
            await git(self.cycle.root, "check-ref-format", "refs/heads/" + branch)
        if spec["destination"] == await git(
            self.cycle.root, "branch", "--show-current"
        ):
            raise PermissionError(
                "Destination must differ from the authoritative coordinator branch"
            )
        if spec["feature"] in {spec["destination"], "main", "master"} or not spec[
            "feature"
        ].startswith("feat/"):
            raise PermissionError("An isolated feature branch is required")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", spec["remote"]):
            raise ValueError("Invalid existing remote")
        if (
            type(spec["parent_complete"]) is not bool
            or not isinstance(spec["remaining"], list)
            or any(not isinstance(v, str) or not v.strip() for v in spec["remaining"])
            or not spec["rationale"].strip()
            or (spec["parent_complete"] and spec["remaining"])
            or (not spec["parent_complete"] and not spec["remaining"])
        ):
            raise ValueError(
                "Explicit parent completion decision and remaining obligations required"
            )
        if (
            type(spec["validation_seconds"]) is not int
            or not 1 <= spec["validation_seconds"] <= 1800
        ):
            raise ValueError("Bounded validation time required")
        destination = await remote_head(
            self.cycle.root, spec["remote"], spec["destination"]
        )
        if not destination:
            raise ValueError("Intended destination must already exist")
        local_destination = await git(
            self.cycle.root,
            "for-each-ref",
            "--format=%(objectname)",
            "refs/heads/" + spec["destination"],
        )
        if local_destination and local_destination != destination:
            raise PermissionError("Local destination differs from the pinned remote")
        await git(self.cycle.root, "cat-file", "-e", destination + "^{commit}")
        original = await blob(self.cycle.root, destination, task.source)
        normalized = original.replace("\r\n", "\n")
        if assignment["baseline_source"] not in (
            normalized,
            normalized.replace("\n", "\r\n"),
        ):
            raise PermissionError(
                "Destination source diverged; no implicit rebase or replacement"
            )
        files = [
            {
                "path": task.source,
                "text": candidate["source"],
                "sha256": digest_text(candidate["source"]),
                "author": "Qwen",
                "reference": candidate["result"]["sha256"],
            }
        ]
        files = independent_files(files, spec["additions"], task.source)
        checkout = resolve_path(spec["checkout"]).value
        if checkout != self.cycle.root:
            raise PermissionError("Plan must use the canonical checkout")
        base = await git(
            self.cycle.root, "merge-base", destination, assignment["base_head"]
        )
        unrelated = (
            await git(
                self.cycle.root,
                "rev-list",
                destination + ".." + assignment["base_head"],
            )
        ).splitlines()
        plan = {
            "schema": "backlog-integration-plan-v1",
            "item": item,
            "candidate_result": candidate["result"]["sha256"],
            "accepted_review": review,
            "candidate_sha256": candidate["result"]["candidate_sha256"],
            "patch_sha256": candidate["patch_sha256"],
            "destination_source_sha256": digest_text(original),
            "target_diff": "".join(
                difflib.unified_diff(
                    normalized.splitlines(keepends=True),
                    next(f["text"] for f in files if f["path"] == task.source)
                    .replace("\r\n", "\n")
                    .splitlines(keepends=True),
                    fromfile="a/" + task.source,
                    tofile="b/" + task.source,
                )
            ),
            "source": task.source,
            "tests": list(task.tests),
            "oracle_sha256": task.oracle_sha256,
            "remote": spec["remote"],
            "remote_url": await git(
                self.cycle.root, "remote", "get-url", spec["remote"]
            ),
            "destination": spec["destination"],
            "destination_base": destination,
            "destination_local_base": local_destination,
            "feature": spec["feature"],
            "checkout": str(checkout),
            "operating_model": "single-checkout-v1",
            "merge_base": base,
            "excluded_source_commits": unrelated,
            "strategy": "destination-based-reviewed-fast-forward",
            "files": files,
            "parent_complete": spec["parent_complete"],
            "remaining": spec["remaining"],
            "rationale": spec["rationale"],
            "validation_seconds": spec["validation_seconds"],
            "backlog": backlog,
            "original_backlog_location": assignment["backlog"]["path"],
        }
        identity = _digest(plan)
        with self.cycle.intake._writer():
            folder = self.folder(item, identity)
            folder.mkdir(parents=True, exist_ok=True)
            if (folder / "plan.json").exists():
                return self.record(item, identity, "plan")
            return self.cycle._save(folder / "plan.json", plan)

    async def _context(
        self, item: str, identity: str, grant: str, action: str
    ) -> dict[str, Any]:
        plan = self.record(item, identity, "plan")
        if plan["sha256"] != identity or plan["item"] != item:
            raise ValueError("Plan identity differs")
        candidate = self.candidate(item, plan["accepted_review"])
        if (
            candidate["result"]["sha256"] != plan["candidate_result"]
            or candidate["patch_sha256"] != plan["patch_sha256"]
        ):
            raise PermissionError("Accepted implementation changed after planning")
        await self.authority.admit(grant, plan, action)
        installed = self.folder(item, identity) / "install.json"
        if (
            installed.exists()
            and self.record(item, identity, "install")["grant"] != grant
        ):
            raise PermissionError("Different grant cannot inherit this integration")
        return plan

    async def _operate(
        self, item: str, identity: str, grant: str, phase: str, **decision: str
    ) -> dict[str, Any]:
        """Materialize a phase temporarily; Git objects and receipts retain state.

        Returning to the administrative branch keeps the CLI available even when
        the destination predates the governed-development implementation.
        """
        action = {"review": "publish", "close_review": "closeout"}.get(phase, phase)
        plan = await self._context(item, identity, grant, action)
        authority = await self.authority.admit(grant, plan, action)
        if (
            await git(self.cycle.root, "branch", "--show-current")
            != authority["coordinator_branch"]
        ):
            raise PermissionError(
                "Administrative branch differs from integration grant"
            )
        if plan.get("operating_model") != "single-checkout-v1" or plan.get(
            "checkout"
        ) != str(self.cycle.root):
            raise PermissionError(
                "Historical checkout-bound plan requires a new plan and grant"
            )
        administrative = phase in {"promote", "close_review", "closeout"}
        branch = (
            await git(self.cycle.root, "branch", "--show-current")
            if administrative
            else plan["feature"]
        )
        revision = (
            await git(self.cycle.root, "rev-parse", "HEAD")
            if administrative
            else await git(
                self.cycle.root,
                "for-each-ref",
                "--format=%(objectname)",
                "refs/heads/" + branch,
            )
        )
        if not revision:
            if (
                phase != "install"
                or (self.folder(item, identity) / "install-intent.json").exists()
            ):
                raise PermissionError(
                    "Integration branch missing; reconcile without recreating an effect"
                )
            revision = plan["destination_base"]
        publication_path = self.folder(item, identity) / "publication.json"
        if (
            not administrative
            and publication_path.exists()
            and revision != self.record(item, identity, "publication")["commit"]
        ):
            raise PermissionError(
                "Published branch identity changed; reconcile without another commit"
            )
        if (
            not administrative
            and revision != plan["destination_base"]
            and (
                not (self.folder(item, identity) / "publication-intent.json").exists()
                or await git(self.cycle.root, "show", "-s", "--format=%P", revision)
                != plan["destination_base"]
                or "Integration-Plan: " + identity
                not in await git(self.cycle.root, "show", "-s", "--format=%B", revision)
            )
        ):
            raise PermissionError("Unrelated integration feature history")
        async with Checkout(
            self.cycle,
            "integration:" + identity + ":" + phase,
            branch,
            revision,
            files=[] if administrative else plan["files"],
            create=not administrative,
            commit_allowed=phase in {"publish", "closeout"},
        ) as checkout:
            self._checkout = checkout
            if not administrative and phase not in {"install", "verify"}:
                self.record(item, identity, "install")
                for file in plan["files"]:
                    path = self._path(self.cycle.root, file["path"])
                    path.parent.mkdir(parents=True, exist_ok=True)
                    write(TextFile(resolve_path(path), file["text"]))
                if phase in {"review", "publish"}:
                    await git(
                        self.cycle.root,
                        "add",
                        "--",
                        *(f["path"] for f in plan["files"]),
                    )
            return cast(
                "dict[str, Any]",
                await getattr(self, "_" + phase)(item, identity, grant, **decision),
            )

    async def install(self, item: str, identity: str, grant: str) -> dict[str, Any]:
        """Admit and stage installation using the single canonical checkout."""
        return await self._operate(item, identity, grant, "install")

    async def validate(self, item: str, identity: str, grant: str) -> dict[str, Any]:
        """Validate the exact temporarily materialized integration tree."""
        return await self._operate(item, identity, grant, "validate")

    async def review(  # noqa: PLR0913 -- explicit supervisory provenance
        self,
        item: str,
        identity: str,
        grant: str,
        *,
        decision: str,
        reference: str,
        rationale: str,
    ) -> dict[str, Any]:
        """Record supervisory review of the exact validated tree."""
        return await self._operate(
            item,
            identity,
            grant,
            "review",
            decision=decision,
            reference=reference,
            rationale=rationale,
        )

    async def publish(self, item: str, identity: str, grant: str) -> dict[str, Any]:
        """Commit and publish the destination-based bounded feature."""
        return await self._operate(item, identity, grant, "publish")

    async def promote(self, item: str, identity: str, grant: str) -> dict[str, Any]:
        """Advance only the independently authorized destination ref."""
        return await self._operate(item, identity, grant, "promote")

    async def verify(self, item: str, identity: str, grant: str) -> dict[str, Any]:
        """Check the actual destination commit in this checkout and return."""
        return await self._operate(item, identity, grant, "verify")

    async def close_review(  # noqa: PLR0913 -- explicit completion provenance
        self,
        item: str,
        identity: str,
        grant: str,
        *,
        decision: str,
        reference: str,
        rationale: str,
    ) -> dict[str, Any]:
        """Review parent versus slice completion after destination verification."""
        return await self._operate(
            item,
            identity,
            grant,
            "close_review",
            decision=decision,
            reference=reference,
            rationale=rationale,
        )

    async def closeout(self, item: str, identity: str, grant: str) -> dict[str, Any]:
        """Publish authoritative progress under the same source ownership."""
        return await self._operate(item, identity, grant, "closeout")

    def _intent(self, item: str, identity: str, phase: str, grant: str) -> None:
        path = self.folder(item, identity) / (phase + "-intent.json")
        if path.exists():
            intent = self.record(item, identity, phase + "-intent")
            if intent["grant"] != grant:
                raise PermissionError("Interrupted operation belongs to another grant")
        else:
            self.save(
                item,
                identity,
                phase + "-intent",
                {
                    "grant": grant,
                    "plan": identity,
                    "disposition": "EFFECT_PENDING_RECONCILIATION",
                },
            )

    async def _files(
        self, plan: dict[str, Any], checkout: Path, *, git_checkout: bool = False
    ) -> dict[str, str]:
        if await common_directory(checkout) != await common_directory(self.cycle.root):
            raise PermissionError("Integration checkout belongs to another repository")
        branch = await git(checkout, "branch", "--show-current")
        expected = plan["feature"]
        if branch != expected:
            raise PermissionError("Integration checkout branch differs from the plan")
        observed = {}
        for f in plan["files"]:
            content = _read(self._path(checkout, f["path"]))
            observed[f["path"]] = digest_text(content)
            if observed[f["path"]] != f["sha256"] and (
                not git_checkout
                or content.replace("\r\n", "\n") != f["text"].replace("\r\n", "\n")
            ):
                raise PermissionError("Unreviewed change to integration source/tests")
        changed = set(
            (
                await git(checkout, "diff", "--name-only", plan["destination_base"])
            ).splitlines()
        )
        untracked = set(
            (
                await git(checkout, "ls-files", "--others", "--exclude-standard")
            ).splitlines()
        )
        preserved = set(self._checkout.record["untracked"])
        if not (changed | (untracked - preserved)) <= {
            f["path"] for f in plan["files"]
        }:
            raise PermissionError("Unapproved files in integration checkout")
        return observed

    @staticmethod
    def _path(checkout: Path, relative: str) -> Path:
        """Apply the repository's resolved-path containment at the write boundary."""
        path = resolve_path(relative, base_directory=checkout).value
        if not path.is_relative_to(checkout):
            raise PermissionError("Integration path escapes the isolated checkout")
        return path

    async def _reserve(self, grant: str, plan: dict[str, Any]) -> None:
        """Reserve once under the caller's coordinator lease; authenticate resume."""
        policy = (await self.authority.admit(grant, plan, "install"))["policy"]
        reservations = self.authority.folder(grant) / "reservations"
        reservations.mkdir(exist_ok=True)
        reservation = reservations / (plan["sha256"] + ".json")
        for path in reservations.iterdir():
            reserved = _load(path, "backlog-integration-reservation-v1")
            if reserved["plan"] != path.stem or reserved["grant"] != grant:
                raise PermissionError("Reservation identity requires reconciliation")
        if reservation.exists():
            reserved = _load(reservation, "backlog-integration-reservation-v1")
            if reserved["validation_seconds"] != 2 * plan["validation_seconds"]:
                raise PermissionError("Reservation allowance differs from plan")
            return
        if len(list(reservations.iterdir())) >= policy["max_integrations"]:
            raise PermissionError("Integration allowance exhausted")
        self.cycle._save(
            reservation,
            {
                "schema": "backlog-integration-reservation-v1",
                "plan": plan["sha256"],
                "grant": grant,
                "at": str(Timestamp.now()),
                "validation_seconds": 2 * plan["validation_seconds"],
            },
        )

    async def _install(self, item: str, identity: str, grant: str) -> dict[str, Any]:
        """Install only authenticated bytes in a destination-based worktree."""
        plan = await self._context(item, identity, grant, "install")
        folder = self.folder(item, identity)
        checkout = resolve_path(plan["checkout"]).value
        with self.cycle.intake._writer():
            await self._reserve(grant, plan)
            self._intent(item, identity, "install", grant)
            if (folder / "install.json").exists():
                await self._files(plan, checkout)
                return self.record(item, identity, "install")
            if (
                await git(checkout, "branch", "--show-current") != plan["feature"]
                or await git(checkout, "rev-parse", "HEAD") != plan["destination_base"]
            ):
                raise PermissionError("Integration branch/base differs")
            # Existing partial installation is never overwritten unless bytes
            # are already the planned bytes or the authenticated Git baseline.
            for f in plan["files"]:
                path = self._path(checkout, f["path"])
                if path.exists():
                    current = _read(path)
                    if digest_text(current) != f["sha256"]:
                        original = await blob(
                            self.cycle.root, plan["destination_base"], f["path"]
                        )
                        if current.replace("\r\n", "\n") != original.replace(
                            "\r\n", "\n"
                        ):
                            raise PermissionError(
                                "Conflicting partial installation; reconcile first"
                            )
                path.parent.mkdir(parents=True, exist_ok=True)
                write(TextFile(resolve_path(path), f["text"]))
            await self._files(plan, checkout)
            return self.save(
                item,
                identity,
                "install",
                {
                    "disposition": "INSTALLED",
                    "grant": grant,
                    "base": plan["destination_base"],
                },
            )

    async def _validate(self, item: str, identity: str, grant: str) -> dict[str, Any]:
        """Validate exact source; retain failure without silently repairing it."""
        plan = await self._context(item, identity, grant, "validate")
        self.record(item, identity, "install")
        folder = self.folder(item, identity)
        checkout = resolve_path(plan["checkout"]).value
        await self._files(plan, checkout)
        if (folder / "validation.json").exists():
            return self.record(item, identity, "validation")
        if await git(checkout, "rev-parse", "HEAD") != plan["destination_base"]:
            raise PermissionError("Unrelated integration history requires replanning")
        with self.cycle.intake._writer():
            if (folder / "validation-intent.json").exists():
                raise PermissionError(
                    "Interrupted validation requires a new reviewed plan; "
                    "allowance retained"
                )
            self._intent(item, identity, "validation", grant)
        task = task_from_dict(
            self.candidate(item, plan["accepted_review"])["assignment"]["task"]
        )
        result = await validate_tree(
            checkout, folder / "pre-checks", plan, task.oracle, post=False
        )
        await self._files(plan, checkout)
        await git(checkout, "add", "--", *(f["path"] for f in plan["files"]))
        tree_id = await git(checkout, "write-tree")
        with self.cycle.intake._writer():
            return self.save(
                item,
                identity,
                "validation",
                {
                    "disposition": "VALIDATED"
                    if result["passed"]
                    else "REWORK_REQUIRED",
                    "tree": tree_id,
                    "evidence": result,
                },
            )

    async def _review(  # noqa: PLR0913 -- explicit decision provenance
        self,
        item: str,
        identity: str,
        grant: str,
        *,
        decision: str,
        reference: str,
        rationale: str,
    ) -> dict[str, Any]:
        """Codex reviews the exact tree, additions, ancestry and destination."""
        plan = await self._context(item, identity, grant, "publish")
        validation = self.record(item, identity, "validation")
        if (
            decision not in {"APPROVE_INTEGRATION", "REJECT", "REWORK_REQUIRED"}
            or not reference.strip()
            or not rationale.strip()
        ):
            raise PermissionError("Explicit Codex integration decision required")
        if (
            decision == "APPROVE_INTEGRATION"
            and validation["disposition"] != "VALIDATED"
        ):
            raise PermissionError("Failed validation cannot be approved")
        await self._files(plan, resolve_path(plan["checkout"]).value)
        if await git(self.cycle.root, "write-tree") != validation["tree"]:
            raise PermissionError(
                "Materialized tree differs from validated integration"
            )
        with self.cycle.intake._writer():
            return self.save(
                item,
                identity,
                "review",
                {
                    "disposition": decision,
                    "reviewer": "Codex",
                    "principal": getpass.getuser(),
                    "reference": reference,
                    "rationale": rationale,
                    "tree": validation["tree"],
                    "plan": identity,
                    "grant": grant,
                    "validation": validation["sha256"],
                },
            )

    async def _publish(self, item: str, identity: str, grant: str) -> dict[str, Any]:
        """Create one reviewed commit; verify or reconcile feature publication."""
        plan = await self._context(item, identity, grant, "publish")
        review = self.record(item, identity, "review")
        validation = self.record(item, identity, "validation")
        if (
            review["disposition"] != "APPROVE_INTEGRATION"
            or review["grant"] != grant
            or review["tree"] != validation["tree"]
        ):
            raise PermissionError("Exact validated-tree integration approval required")
        checkout = resolve_path(plan["checkout"]).value
        with self.cycle.intake._writer():
            self._intent(item, identity, "publication", grant)
            await self.authority.admit(grant, plan, "publish")
            await self._files(plan, checkout)
            head = await git(checkout, "rev-parse", "HEAD")
            if head == plan["destination_base"]:
                if await git(checkout, "write-tree") != review["tree"] or await git(
                    checkout, "diff", "--name-only"
                ):
                    raise PermissionError("Integration changed after review")
                await git(
                    checkout,
                    "commit",
                    "-m",
                    "Integrate " + item + " reviewed development slice",
                    "-m",
                    "Integration-Plan: "
                    + identity
                    + "\nImplementation-Candidate: "
                    + plan["candidate_sha256"]
                    + "\nImplementation-by: Qwen (immutable candidate)"
                    + "\nApplied-by: "
                    + getpass.getuser()
                    + "\nSupervised-by: Codex\nIndependent additions: "
                    + ", ".join(
                        f["author"] + ":" + f["reference"]
                        for f in plan["files"]
                        if f["author"] != "Qwen"
                    ),
                )
                head = await git(checkout, "rev-parse", "HEAD")
            if (
                await git(checkout, "show", "-s", "--format=%P", head)
                != plan["destination_base"]
                or await git(checkout, "rev-parse", head + "^{tree}") != review["tree"]
                or "Integration-Plan: " + identity
                not in await git(checkout, "show", "-s", "--format=%B", head)
            ):
                raise PermissionError("Unrelated history cannot be promoted")
            await clean(checkout)
            await self.authority.admit(grant, plan, "publish")
            await publish(self.cycle.root, plan["remote"], plan["feature"], head, "")
            path = self.folder(item, identity) / "publication.json"
            if path.exists():
                return self.record(item, identity, "publication")
            return self.save(
                item,
                identity,
                "publication",
                {
                    "disposition": "FEATURE_PUBLISHED",
                    "commit": head,
                    "tree": review["tree"],
                    "parent": plan["destination_base"],
                    "revert_parent": plan["destination_base"],
                    "revert_command": "git revert " + head,
                    "review": review["sha256"],
                },
            )

    async def _promote(self, item: str, identity: str, grant: str) -> dict[str, Any]:
        """Promote only the destination-based reviewed commit via exact-ref lease."""
        plan = await self._context(item, identity, grant, "promote")
        publication = self.record(item, identity, "publication")
        with self.cycle.intake._writer():
            self._intent(item, identity, "promotion", grant)
            await self.authority.admit(grant, plan, "promote")
            if (
                await remote_head(self.cycle.root, plan["remote"], plan["feature"])
                != publication["commit"]
            ):
                raise PermissionError("Published feature ref changed")
            await publish(
                self.cycle.root,
                plan["remote"],
                plan["destination"],
                publication["commit"],
                plan["destination_base"],
            )
            local = await git(
                self.cycle.root,
                "for-each-ref",
                "--format=%(objectname)",
                "refs/heads/" + plan["destination"],
            )
            if local != publication["commit"]:
                if local != plan["destination_local_base"]:
                    raise PermissionError(
                        "Local destination moved; reconcile promotion"
                    )
                await self.authority.admit(grant, plan, "promote")
                await git(
                    self.cycle.root,
                    "update-ref",
                    "refs/heads/" + plan["destination"],
                    publication["commit"],
                    local or "0" * len(publication["commit"]),
                )
            if (self.folder(item, identity) / "promotion.json").exists():
                return self.record(item, identity, "promotion")
            return self.save(
                item,
                identity,
                "promotion",
                {
                    "disposition": "TARGET_PROMOTED",
                    "destination_commit": publication["commit"],
                    "prior_commit": plan["destination_base"],
                    "remote": plan["remote"],
                    "destination": plan["destination"],
                },
            )

    async def _verify(self, item: str, identity: str, grant: str) -> dict[str, Any]:
        """Authenticate the destination and run post-integration acceptance."""
        plan = await self._context(item, identity, grant, "verify")
        promoted = self.record(item, identity, "promotion")
        folder = self.folder(item, identity)
        checkout = resolve_path(plan["checkout"]).value
        if (
            await remote_head(self.cycle.root, plan["remote"], plan["destination"])
            != promoted["destination_commit"]
            or await git(
                self.cycle.root, "rev-parse", "refs/heads/" + plan["destination"]
            )
            != promoted["destination_commit"]
        ):
            raise PermissionError(
                "Destination moved; post-integration reconciliation required"
            )
        if (folder / "verification.json").exists():
            return self.record(item, identity, "verification")
        with self.cycle.intake._writer():
            if (folder / "verification-intent.json").exists():
                raise PermissionError(
                    "Interrupted post-validation requires reconciliation"
                )
            self._intent(item, identity, "verification", grant)
        pre = self.record(item, identity, "validation")
        if await git(checkout, "rev-parse", "HEAD^{tree}") != pre["tree"]:
            raise PermissionError("Destination differs from protected-validated tree")
        if await git(checkout, "rev-parse", "HEAD") != promoted["destination_commit"]:
            raise PermissionError(
                "Verification checkout differs from the exact destination commit"
            )
        materialized = await self._files(plan, checkout, git_checkout=True)
        task = task_from_dict(
            self.candidate(item, plan["accepted_review"])["assignment"]["task"]
        )
        result = await validate_tree(
            checkout, folder / "post-checks", plan, task.oracle, post=True
        )
        if await self._files(plan, checkout, git_checkout=True) != materialized:
            raise PermissionError("Post-validation changed source materialization")
        await clean(checkout)
        with self.cycle.intake._writer():
            return self.save(
                item,
                identity,
                "verification",
                {
                    "disposition": "DESTINATION_VERIFIED"
                    if result["passed"]
                    else "POST_INTEGRATION_FAILED",
                    "commit": promoted["destination_commit"],
                    "tree": pre["tree"],
                    "protected_validation_reused_for_identical_tree": pre["sha256"],
                    "materialized_sha256": materialized,
                    "planned_sha256": {f["path"]: f["sha256"] for f in plan["files"]},
                    "checkout_equivalence": "Git LF/CRLF; tree authenticated first",
                    "evidence": result,
                },
            )

    def status(self, item: str, identity: str) -> dict[str, Any]:
        """Project immutable phase evidence; pending intent never proves success."""
        plan = self.record(item, identity, "plan")
        folder = self.folder(item, identity)
        phases = (
            "install",
            "validation",
            "review",
            "publication",
            "promotion",
            "verification",
            "completion-review",
            "completion",
        )
        events = [
            self.record(item, identity, name)
            for name in phases
            if (folder / (name + ".json")).exists()
        ]
        pending = [
            name
            for name in (
                "install",
                "validation",
                "publication",
                "promotion",
                "verification",
                "completion",
            )
            if (folder / (name + "-intent.json")).exists()
            and not (folder / (name + ".json")).exists()
        ]
        refusals = [
            _load(path, "backlog-integration-refusal-v1")
            for path in sorted((folder / "refusals").glob("*.json"))
        ]
        refusals.sort(key=lambda r: r["at"])
        blocked = bool(
            refusals and (not events or refusals[-1]["at"] > events[-1]["at"])
        )
        return {
            "plan": identity,
            "operating_model": plan.get(
                "operating_model", "historical-secondary-checkout"
            ),
            "checkout": plan.get("checkout"),
            "temporary_source_restored_between_commands": plan.get("operating_model")
            == "single-checkout-v1",
            "checkout_reconciliation_required": (
                self.cycle.root / ".local/backlog/checkout-owner"
            ).exists(),
            "item": item,
            "destination": plan["destination"],
            "strategy": plan["strategy"],
            "disposition": "RECONCILIATION_REQUIRED"
            if pending
            else "BLOCKED"
            if blocked
            else events[-1]["disposition"]
            if events
            else "INTEGRATION_PLAN",
            "pending": pending,
            "history": events,
            "refusals": refusals,
            "remaining": plan["remaining"],
            "parent_complete": bool(events and events[-1].get("parent_closed")),
        }

    def refusal(self, item: str, identity: str, action: str, error: Exception) -> None:
        """Preserve a CLI refusal without treating an uncertain effect as failed."""
        self.record(item, identity, "plan")
        value = {
            "schema": "backlog-integration-refusal-v1",
            "at": str(Timestamp.now()),
            "action": action,
            "error_type": type(error).__name__,
            "error": str(error)[:4096],
            "plan": identity,
            "pending": self.status(item, identity)["pending"],
        }
        with self.cycle.intake._writer():
            folder = self.folder(item, identity) / "refusals"
            folder.mkdir(exist_ok=True)
            self.cycle._save(folder / (_digest(value) + ".json"), value)

    async def _close_review(  # noqa: PLR0913 -- explicit completion provenance
        self,
        item: str,
        identity: str,
        grant: str,
        *,
        decision: str,
        reference: str,
        rationale: str,
    ) -> dict[str, Any]:
        """Make the parent-vs-slice completion decision explicit after verification."""
        plan = await self._context(item, identity, grant, "closeout")
        verified = self.record(item, identity, "verification")
        expected = "COMPLETE_PARENT" if plan["parent_complete"] else "SLICE_ONLY"
        if (
            verified["disposition"] != "DESTINATION_VERIFIED"
            or decision != expected
            or not reference.strip()
            or not rationale.strip()
        ):
            raise PermissionError(
                "Verified destination and explicit completion decision required"
            )
        with self.cycle.intake._writer():
            return self.save(
                item,
                identity,
                "completion-review",
                {
                    "disposition": "COMPLETION_REVIEWED",
                    "reviewer": "Codex",
                    "principal": getpass.getuser(),
                    "grant": grant,
                    "verification": verified["sha256"],
                    "decision": decision,
                    "reference": reference,
                    "rationale": rationale,
                },
            )

    async def _closeout(self, item: str, identity: str, grant: str) -> dict[str, Any]:  # noqa: C901, PLR0912, PLR0915 -- one recoverable Git/backlog transaction
        """Publish authoritative backlog progress, keeping incomplete parents open."""
        plan = await self._context(item, identity, grant, "closeout")
        verified = self.record(item, identity, "verification")
        decision = self.record(item, identity, "completion-review")
        authority = await self.authority.admit(grant, plan, "closeout")
        if (
            verified["disposition"] != "DESTINATION_VERIFIED"
            or decision["verification"] != verified["sha256"]
            or decision["grant"] != grant
        ):
            raise PermissionError("Exact post-integration completion review required")
        if (
            await remote_head(self.cycle.root, plan["remote"], plan["destination"])
            != verified["commit"]
        ):
            raise PermissionError("Destination changed before authoritative closeout")
        branch = await git(self.cycle.root, "branch", "--show-current")
        if branch != authority["coordinator_branch"]:
            raise PermissionError("Coordinator publication branch differs from grant")
        if branch in {"main", "master"}:
            allowed = (
                await git(
                    self.cycle.root,
                    "config",
                    "--get-all",
                    "devtools.integrationProtectedTarget",
                    missing_ok=True,
                )
            ).splitlines()
            if (
                not authority["policy"]["protected"]
                or plan["remote"] + ":" + branch not in allowed
            ):
                raise PermissionError("Protected backlog publication is not permitted")
        folder = self.folder(item, identity)
        if (folder / "completion.json").exists():
            result = self.record(item, identity, "completion")
            if (
                await remote_head(self.cycle.root, plan["remote"], branch)
                != result["backlog_commit"]
            ):
                raise PermissionError("Backlog publication moved; reconcile history")
            return result
        with self.cycle.intake._writer():
            intent_path = folder / "completion-intent.json"
            if not intent_path.exists():
                await clean(self.cycle.root)
                base = await git(self.cycle.root, "rev-parse", "HEAD")
                if await remote_head(self.cycle.root, plan["remote"], branch) != base:
                    raise PermissionError("Coordinator remote must be synchronized")
                current = self.cycle.intake.approved_item(item)
                if not same_backlog(current, plan["backlog"]):
                    raise PermissionError("Backlog changed before closeout")
                path = resolve_path(current["path"]).value
                overview = self.cycle.root / "docs/backlog/overview.md"
                old = _read(path)
                old_index = _read(overview)
                new = (
                    old.replace("- status: BACKLOG", "- status: CLOSED", 1)
                    if plan["parent_complete"]
                    else old
                )
                new += (
                    "\n## Verified development integration "
                    + identity
                    + "\n\n"
                    + "- Target: "
                    + plan["remote"]
                    + "/"
                    + plan["destination"]
                    + " @ "
                    + verified["commit"]
                    + "\n"
                    + "- Candidate: "
                    + plan["candidate_sha256"]
                    + "\n"
                    + "- Accepted worker review: "
                    + plan["accepted_review"]
                    + "\n"
                    + "- Integration authority: "
                    + grant
                    + "\n"
                    + "- Protected/post validation: "
                    + verified["sha256"]
                    + "\n"
                    + "- Codex completion review: "
                    + decision["sha256"]
                    + "\n"
                    + "- Decision: "
                    + decision["decision"]
                    + "; "
                    + decision["rationale"]
                    + "\n"
                    + "- Remaining obligations: "
                    + (
                        "; ".join(plan["remaining"])
                        or "none; explicitly reviewed complete"
                    )
                    + "\n"
                )
                lines = old_index.splitlines(keepends=True)
                if plan["parent_complete"]:
                    lines = [
                        line.replace("| BACKLOG |", "| CLOSED |", 1)
                        if line.startswith("| [" + item + "]")
                        else line
                        for line in lines
                    ]
                intent = self.save(
                    item,
                    identity,
                    "completion-intent",
                    {
                        "grant": grant,
                        "plan": identity,
                        "base": base,
                        "branch": branch,
                        "files": [
                            {
                                "path": path.relative_to(self.cycle.root).as_posix(),
                                "before": old,
                                "after": new,
                            },
                            {
                                "path": "docs/backlog/overview.md",
                                "before": old_index,
                                "after": "".join(lines),
                            },
                        ],
                    },
                )
            else:
                intent = self.record(item, identity, "completion-intent")
                if intent["grant"] != grant:
                    raise PermissionError("Closeout belongs to another authority")
            paths = [v["path"] for v in intent["files"]]
            changed = set(
                (
                    await git(self.cycle.root, "diff", "--name-only", intent["base"])
                ).splitlines()
            )
            if (
                not changed <= set(paths)
                or await untracked_files(self.cycle.root)
                != self._checkout.record["untracked"]
            ):
                raise PermissionError(
                    "Unrelated coordinator work prevents closeout publication"
                )
            for f in intent["files"]:
                path = resolve_path(f["path"], base_directory=self.cycle.root).value
                if _read(path) not in (f["before"], f["after"]):
                    raise PermissionError(
                        "Conflicting backlog closeout requires reconciliation"
                    )
                self._checkout.record["files"].append(
                    {"path": f["path"], "expected": []}
                )
                self._checkout.expect(f["path"], f["after"])
                write(TextFile(resolve_path(path), f["after"]))
            head = await git(self.cycle.root, "rev-parse", "HEAD")
            if head == intent["base"]:
                await self.authority.admit(grant, plan, "closeout")
                await git(self.cycle.root, "add", "--", *paths)
                await git(
                    self.cycle.root,
                    "commit",
                    "-m",
                    "Record " + item + " verified integration progress",
                    "-m",
                    "Integration-Closeout: " + identity,
                )
                head = await git(self.cycle.root, "rev-parse", "HEAD")
            if await git(self.cycle.root, "show", "-s", "--format=%P", head) != intent[
                "base"
            ] or "Integration-Closeout: " + identity not in await git(
                self.cycle.root, "show", "-s", "--format=%B", head
            ):
                raise PermissionError(
                    "Ambiguous closeout commit; reconcile without duplication"
                )
            if not set(
                (
                    await git(
                        self.cycle.root,
                        "diff-tree",
                        "--no-commit-id",
                        "--name-only",
                        "-r",
                        head,
                    )
                ).splitlines()
            ) <= set(paths):
                raise PermissionError("Unrelated changes in closeout commit")
            await clean(self.cycle.root)
            await self.authority.admit(grant, plan, "closeout")
            await publish(self.cycle.root, plan["remote"], branch, head, intent["base"])
            return self.save(
                item,
                identity,
                "completion",
                {
                    "disposition": "VERIFIED_COMPLETION",
                    "target_commit": verified["commit"],
                    "backlog_commit": head,
                    "parent_closed": plan["parent_complete"],
                    "remaining": plan["remaining"],
                    "completion_review": decision["sha256"],
                    "revert_commit": "git revert " + verified["commit"],
                    "revert_requires_separate_authority": True,
                },
            )

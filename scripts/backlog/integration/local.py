# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, SLF001, PLR0913 -- trusted local integration boundary
"""Local candidate entry into the existing WorkCycle integration owner.

Trusted supervisor invocation may publish only an explicitly named ordinary
feature. Backlog closeout and destination promotion remain governed operations.
"""

from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING, Any

from apps.qwen.coding_loop import _prepare_workspace, validate_workspace
from apps.qwen.patch_proposal_worker import _read_text
from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.resources.filesystem import TextFile, write
from scripts.backlog.checkout import Checkout
from scripts.backlog.checkout import _paths as file_names
from scripts.backlog.coordinator import git
from scripts.backlog.integration.git import publish, remote_head
from scripts.backlog.integration.lifecycle import independent_files
from scripts.backlog.integration.validation import validate_tree

if TYPE_CHECKING:
    from pathlib import Path

    from apps.qwen.tasks import CodingTask
    from scripts.backlog.integration import Integration

MAX_SOURCE_BYTES = 32768
MAX_FILES = 8
MAX_INSTALL_BYTES = 131072


def _fresh_protected(report: dict[str, Any]) -> bool:
    """Accept only the current direct validator's fresh protected result."""
    return (
        report.get("passed") is True
        and report.get("profile") == "pre-publication-protected"
        and report.get("reuse_policy") == "fresh-only-v1"
    )


async def closeout_local(  # noqa: C901, PLR0912, PLR0915 -- one recoverable installation/review/publication phase
    integration: Integration,
    task: CodingTask,
    evidence: Path,
    *,
    branch: str,
    expected_head: str,
    review: dict[str, Any] | None = None,
    commit: bool = False,
    push: bool = False,
    additions: list[dict[str, str]] | None = None,
    protected_validation: bool = False,
    expected_remote: str | None = None,
    implementation_author: str = "Qwen",
) -> dict[str, Any]:
    """Authenticate, install, validate, review and optionally publish one candidate.

    No model-facing Tool can call this operation. `commit`/`push` are explicit
    trusted operator effects. A review recommends, but never grants, publication.
    Interrupted commit/push is reconciled by exact commit/ref, not repeated.
    """
    root, cycle = integration.cycle.root, integration.cycle
    if implementation_author not in {"Qwen", "Codex"}:
        raise ValueError("Local implementation author must be Qwen or Codex")
    if any(type(value) is not bool for value in (commit, push, protected_validation)):
        raise TypeError("Closeout effects require explicit boolean flags")
    evidence = resolve_path(evidence).value
    if not evidence.is_relative_to(root / ".local") or not branch.startswith("feat/"):
        raise PermissionError(
            "Local closeout requires local evidence and ordinary feature"
        )
    if push and not commit:
        raise PermissionError("Push requires explicit feature commit authority")
    result_path = evidence / "result.json"
    result_text = _read_text(resolve_path(result_path)).content
    result_sha = hashlib.sha256(result_text.encode()).hexdigest()
    result = json.loads(result_text)
    if (
        not result.get("accepted")
        or result.get("task_definition_sha256") != task.definition_sha256
        or result.get("oracle_sha256") != task.oracle_sha256
        or result.get("implementation_by", "Qwen") != implementation_author
    ):
        raise PermissionError("Accepted exact task/oracle candidate required")
    candidates = result.get("candidates", [])
    if {c["path"] for c in candidates} != set(task.sources) or len(candidates) != len(
        task.sources
    ):
        raise PermissionError("Candidate source scope differs")
    sources = {}
    baseline: dict[str, str | None] = {}
    for candidate in candidates:
        path = candidate["path"]
        raw = evidence / candidate["evidence"]
        file = resolve_path(candidate["evidence"], base_directory=evidence).value
        if file != raw or not file.is_relative_to(evidence):
            raise PermissionError("Candidate path alias is not admitted")
        text = _read_text(resolve_path(file)).content
        if (
            not file.is_relative_to(evidence)
            or file.is_symlink()
            or hashlib.sha256(text.encode()).hexdigest() != candidate["sha256"]
            or len(text.encode()) > MAX_SOURCE_BYTES
        ):
            raise PermissionError("Candidate bytes or evidence path changed")
        sources[path] = text
        baseline[path] = (
            None
            if path in task.new_paths
            else await cycle._baseline(task, path, dict(task.baseline_hashes)[path])
        )
    files = independent_files(
        [
            {
                "path": p,
                "text": t,
                "author": implementation_author,
                "reference": result_sha,
                "sha256": hashlib.sha256(t.encode()).hexdigest(),
            }
            for p, t in sources.items()
        ],
        additions or [],
        task.source,
        allow_source=False,
    )
    if (
        len(files) > MAX_FILES
        or sum(len(f["text"].encode()) for f in files) > MAX_INSTALL_BYTES
    ):
        raise ValueError("Local closeout source/test scope exceeds bounded size")
    for addition in additions or []:
        path = addition["path"]
        raw = root / path
        if resolve_path(raw).value != raw or not raw.parent.is_dir():
            raise PermissionError("Test addition aliases or has no maintained parent")
        baseline[path] = _read_text(resolve_path(raw)).content if raw.exists() else None
    installed = {f["path"]: f["text"] for f in files}
    receipt = evidence / "closeout.json"
    previous: dict[str, Any] = {}
    if receipt.exists():
        previous = json.loads(receipt.read_text())
        if (
            previous.get("result_sha256") != result_sha
            or previous.get("branch") != branch
            or previous.get("implementation_by", "Qwen") != implementation_author
        ):
            raise PermissionError("Existing closeout binding changed")
        if previous.get("disposition") == "COMMIT_INTENT" and not previous.get(
            "commit"
        ):
            observed = await git(root, "rev-parse", branch)
            if observed != expected_head:
                if (
                    await git(root, "show", "-s", "--format=%P", observed)
                    != expected_head
                    or await git(root, "rev-parse", observed + "^{tree}")
                    != previous["tree"]
                    or "Local-Closeout: " + previous["review_subject"]
                    not in await git(root, "show", "-s", "--format=%B", observed)
                ):
                    raise PermissionError(
                        "Ambiguous commit intent requires reconciliation"
                    )
                previous["commit"] = observed
                previous["disposition"] = "FEATURE_COMMITTED"
                write(TextFile(resolve_path(receipt), json.dumps(previous, indent=2)))
        if previous.get("commit"):
            head = previous["commit"]
            if (
                await git(root, "rev-parse", branch) != head
                or await git(root, "show", "-s", "--format=%P", head) != expected_head
            ):
                raise PermissionError("Recorded feature commit diverged")
            changed = await file_names(
                root, "diff-tree", "--no-commit-id", "--name-only", "-r", head
            )
            if not changed <= set(installed) or not changed:
                raise PermissionError("Recorded commit contains unapproved changes")
            for path, text in installed.items():
                if await git(
                    root, "show", head + ":" + path, trim=False
                ) != text.replace("\r\n", "\n"):
                    raise PermissionError("Recorded committed source changed")
            if push:
                observed_remote = await remote_head(root, "origin", branch)
                if observed_remote != head:
                    if observed_remote != previous["remote_before"]:
                        raise PermissionError("Remote advanced; reconcile publication")
                    if (
                        await git(root, "branch", "--show-current") != branch
                        or await git(root, "rev-parse", "HEAD") != head
                    ):
                        raise PermissionError("Exact committed checkout required")
                    async with Checkout(
                        cycle, "local-publish:" + result_sha, branch, head, files=[]
                    ):
                        report = await validate_tree(
                            root,
                            evidence
                            / (
                                "committed-validation-"
                                + str(Timestamp.now()).replace(":", "-")
                            ),
                            {
                                "source": task.source,
                                "tests": list(task.tests),
                                "files": files,
                                "validation_seconds": 1800,
                            },
                            task.oracle,
                            post=False,
                        )
                        if not _fresh_protected(report):
                            raise PermissionError(
                                "Fresh committed protected validation required"
                            )
                        previous["committed_protected_validation"] = report
                        write(
                            TextFile(
                                resolve_path(receipt), json.dumps(previous, indent=2)
                            )
                        )
                        await publish(
                            root, "origin", branch, head, previous["remote_before"]
                        )
                # An already accepted exact ref is observation, not reuse of a
                # passing check as proof of current environment/input freshness.
                previous["disposition"] = "FEATURE_PUBLISHED"
            previous["publication_eligible"] = False
            previous["validation_claim"] = (
                "historical result; not current reusable proof"
            )
            write(TextFile(resolve_path(receipt), json.dumps(previous, indent=2)))
            return previous
    if (
        await git(root, "rev-parse", "HEAD") != expected_head
        or await git(root, "branch", "--show-current") != branch
    ):
        raise PermissionError("Exact active feature HEAD required")
    for path, baseline_text in baseline.items():
        current = (
            (root / path).read_bytes().decode() if (root / path).exists() else None
        )
        if (current or "").replace("\r\n", "\n") != (baseline_text or "").replace(
            "\r\n", "\n"
        ) or (current is None) != (baseline_text is None):
            raise PermissionError("Maintained source drift requires rebase/review")
        baseline[path] = current
    record: dict[str, Any] = {
        "at": str(Timestamp.now()),
        "result_sha256": result_sha,
        "branch": branch,
        "base": expected_head,
        "candidate_sha256": {
            p: hashlib.sha256(t.encode()).hexdigest() for p, t in sources.items()
        },
        "publication_authority": "explicit trusted local feature invocation"
        if commit
        else "NONE",
        "protected_promotion": "PROHIBITED",
        "implementation_by": implementation_author,
        "supervision_by": "Codex",
        "commit": None,
        "files": [{k: v for k, v in f.items() if k != "text"} for f in files],
        "host_mechanical_changes": [
            s.get("mechanical_format")
            for s in result.get("turns", [])
            if s.get("mechanical_format")
        ],
        "validation_inputs": {
            p: hashlib.sha256(
                (
                    installed.get(p) or _read_text(resolve_path(root / p)).content
                ).encode()
            ).hexdigest()
            for p in task.tests
        },
    }
    async with Checkout(
        cycle,
        "local-closeout:" + result_sha,
        branch,
        expected_head,
        files=[{"path": p, "text": t or ""} for p, t in baseline.items()],
        commit_allowed=commit,
    ) as owner:
        for path, text in installed.items():
            owner.expect(path, text)
            write(TextFile(resolve_path(root / path), text))
        checks = evidence / (
            "closeout-validation-" + str(Timestamp.now()).replace(":", "-")
        )
        checks.mkdir()
        _prepare_workspace(root, checks, task)
        validation = await validate_workspace(root, checks, task=task)
        record["validation"] = validation
        if validation["accepted"] and (protected_validation or commit):
            plan = {
                "source": task.source,
                "tests": list(task.tests),
                "files": files,
                "validation_seconds": 1800,
            }
            record["protected_validation"] = await validate_tree(
                root, checks / "protected", plan, task.oracle, post=False
            )
            validation["accepted"] = validation["accepted"] and _fresh_protected(
                record["protected_validation"]
            )
        record["disposition"] = (
            "SUPERVISORY_REVIEW"
            if validation["accepted"]
            else "INTEGRATION_VALIDATION_FAILED"
        )
        record["review_subject"] = hashlib.sha256(
            json.dumps(
                {
                    "result": result_sha,
                    "base": expected_head,
                    "files": record["files"],
                },
                sort_keys=True,
            ).encode()
        ).hexdigest()
        record["publication_eligible"] = validation["accepted"] and _fresh_protected(
            record.get("protected_validation", {})
        )
        record["validation_claim"] = (
            "fresh invocation only; saved results cannot authorize reuse"
        )
        write(TextFile(resolve_path(receipt), json.dumps(record, indent=2)))
        if not validation["accepted"] or not commit:
            return record
        if (
            not review
            or review.get("subject") != record["review_subject"]
            or review.get("reviewer") != "Codex"
            or review.get("disposition") != "ACCEPT_RECOMMENDED"
            or not str(review.get("rationale", "")).strip()
        ):
            raise PermissionError(
                "Exact final-source Codex review required before commit"
            )
        if not record["publication_eligible"]:
            raise PermissionError(
                "Protected development validation of this exact candidate is required"
            )
        record["review"] = review
        record["remote_before"] = (
            await remote_head(root, "origin", branch) if push else ""
        )
        if push:
            if record["remote_before"] != (expected_remote or expected_head):
                raise PermissionError(
                    "Remote feature advanced or explicit expected remote is missing"
                )
            if (
                record["remote_before"]
                and await git(
                    root, "merge-base", record["remote_before"], expected_head
                )
                != record["remote_before"]
            ):
                raise PermissionError(
                    "Feature publication would import divergent ancestry"
                )
        await git(root, "add", "--", *installed)
        record["tree"] = await git(root, "write-tree")
        record["disposition"] = "COMMIT_INTENT"
        write(TextFile(resolve_path(receipt), json.dumps(record, indent=2)))
        await git(
            root,
            "commit",
            "-m",
            "Integrate reviewed " + implementation_author + " task: " + task.name,
            "-m",
            implementation_author
            + "-Result: "
            + result_sha
            + "\nReviewed-by: Codex\nImplementation-by: "
            + implementation_author
            + "\nLocal-Closeout: "
            + record["review_subject"],
        )
        record["commit"] = await git(root, "rev-parse", "HEAD")
        record["disposition"] = "FEATURE_COMMITTED"
        record["revert_parent"] = expected_head
        record["revert_command"] = "git revert " + record["commit"]
        write(TextFile(resolve_path(receipt), json.dumps(record, indent=2)))
        if push:
            await publish(
                root, "origin", branch, record["commit"], record["remote_before"]
            )
            record["disposition"] = "FEATURE_PUBLISHED"
            write(TextFile(resolve_path(receipt), json.dumps(record, indent=2)))
    return record

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
from apps.qwen.development_task import _hash
from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.resources.filesystem import TextFile, write
from scripts.backlog.checkout import Checkout
from scripts.backlog.coordinator import git
from scripts.backlog.integration.git import publish, remote_head

if TYPE_CHECKING:
    from pathlib import Path

    from apps.qwen.tasks import CodingTask
    from scripts.backlog.integration import Integration


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
) -> dict[str, Any]:
    """Authenticate, install, validate, review and optionally publish one candidate.

    No model-facing Tool can call this operation. `commit`/`push` are explicit
    trusted operator effects. A review recommends, but never grants, publication.
    Interrupted commit/push is reconciled by exact commit/ref, not repeated.
    """
    root, cycle = integration.cycle.root, integration.cycle
    evidence = resolve_path(evidence).value
    if not evidence.is_relative_to(root / ".local") or not branch.startswith("feat/"):
        raise PermissionError(
            "Local closeout requires local evidence and ordinary feature"
        )
    if push and not commit:
        raise PermissionError("Push requires explicit feature commit authority")
    result_path = evidence / "result.json"
    result_sha = _hash(result_path)
    result = json.loads(result_path.read_text(encoding="utf-8"))
    if (
        not result.get("accepted")
        or result.get("task_definition_sha256") != task.definition_sha256
        or result.get("oracle_sha256") != task.oracle_sha256
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
        file = resolve_path(candidate["evidence"], base_directory=evidence).value
        if (
            not file.is_relative_to(evidence)
            or file.is_symlink()
            or _hash(file) != candidate["sha256"]
        ):
            raise PermissionError("Candidate bytes or evidence path changed")
        sources[path] = file.read_bytes().decode("utf-8")
        baseline[path] = (
            None
            if path in task.new_paths
            else await cycle._baseline(task, path, dict(task.baseline_hashes)[path])
        )
    receipt = evidence / "closeout.json"
    if receipt.exists():
        previous: dict[str, Any] = json.loads(receipt.read_text())
        if (
            previous.get("result_sha256") != result_sha
            or previous.get("branch") != branch
        ):
            raise PermissionError("Existing closeout binding changed")
        if previous.get("commit"):
            head = previous["commit"]
            if (
                await git(root, "rev-parse", branch) != head
                or await git(root, "show", "-s", "--format=%P", head) != expected_head
            ):
                raise PermissionError("Recorded feature commit diverged")
            for path, text in sources.items():
                if await git(
                    root, "show", head + ":" + path, trim=False
                ) != text.replace("\r\n", "\n"):
                    raise PermissionError("Recorded committed source changed")
            if push:
                await publish(root, "origin", branch, head, previous["remote_before"])
                previous["disposition"] = "FEATURE_PUBLISHED"
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
        "implementation_by": "Qwen",
        "supervision_by": "Codex",
        "commit": None,
    }
    async with Checkout(
        cycle,
        "local-closeout:" + result_sha,
        branch,
        expected_head,
        files=[{"path": p, "text": t or ""} for p, t in baseline.items()],
        commit_allowed=commit,
    ) as owner:
        for path, text in sources.items():
            owner.expect(path, text)
            write(TextFile(resolve_path(root / path), text))
        checks = evidence / (
            "closeout-validation-" + str(Timestamp.now()).replace(":", "-")
        )
        checks.mkdir()
        _prepare_workspace(root, checks, task)
        validation = await validate_workspace(root, checks, task=task)
        record["validation"] = validation
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
                    "files": record["candidate_sha256"],
                },
                sort_keys=True,
            ).encode()
        ).hexdigest()
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
        record["review"] = review
        record["remote_before"] = (
            await remote_head(root, "origin", branch) if push else ""
        )
        if push and record["remote_before"] != expected_head:
            raise PermissionError(
                "Publish framework checkpoint first; remote feature advanced or stale"
            )
        await git(root, "add", "--", *task.sources)
        record["tree"] = await git(root, "write-tree")
        record["disposition"] = "COMMIT_INTENT"
        write(TextFile(resolve_path(receipt), json.dumps(record, indent=2)))
        await git(
            root,
            "commit",
            "-m",
            "Integrate reviewed Qwen task: " + task.name,
            "-m",
            "Qwen-Result: "
            + result_sha
            + "\nReviewed-by: Codex\nImplementation-by: Qwen\nLocal-Closeout: "
            + record["review_subject"],
        )
        record["commit"] = await git(root, "rev-parse", "HEAD")
        record["disposition"] = "FEATURE_COMMITTED"
        write(TextFile(resolve_path(receipt), json.dumps(record, indent=2)))
        if push:
            await publish(root, "origin", branch, record["commit"], expected_head)
            record["disposition"] = "FEATURE_PUBLISHED"
            write(TextFile(resolve_path(receipt), json.dumps(record, indent=2)))
    return record

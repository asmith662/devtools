# Copyright (c) 2026
# ruff: noqa: COM812 -- tiny authored Git fixture
"""Exact local candidates enter the same integration owner; no model dispatch."""

from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from scripts.backlog.coordinator import git
from tests.scripts.backlog.test_work import GOOD, OLD
from tests.scripts.backlog.test_work import fixture as fixture  # noqa: PLC0414


def evidence(f: dict[str, Any]) -> Path:
    """Create explicitly synthetic local result, independent of production evidence."""
    task = f["task"]
    folder = Path(f["root"]) / ".local/local-result"
    folder.mkdir()
    text = (f["root"] / task.source).read_bytes().decode().replace(OLD, GOOD)
    (folder / "final-source.py").write_bytes(text.encode())
    (folder / "result.json").write_text(
        json.dumps(
            {
                "accepted": True,
                "task_definition_sha256": task.definition_sha256,
                "oracle_sha256": task.oracle_sha256,
                "candidates": [
                    {
                        "path": task.source,
                        "evidence": "final-source.py",
                        "sha256": hashlib.sha256(text.encode()).hexdigest(),
                    }
                ],
            }
        )
    )
    return folder


def test_local_candidate_validation_review_commit_push_and_idempotence(
    fixture: dict[str, Any],
) -> None:
    """Use actual scoped validation, feature commit and a bare fixture remote."""

    async def run() -> None:
        f = fixture
        root = f["root"]
        task = f["task"]
        candidate = evidence(f)
        await git(root, "switch", "feat/fixture")
        head = await git(root, "rev-parse", "HEAD")
        remote = root.parent / "local-origin.git"
        await git(root, "init", "--bare", str(remote))
        await git(root, "remote", "add", "origin", str(remote))
        await git(root, "push", "origin", "HEAD:refs/heads/feat/fixture")
        record = await f["cycle"].integration.closeout_local(
            task, candidate, branch="feat/fixture", expected_head=head
        )
        assert record["disposition"] == "SUPERVISORY_REVIEW"
        assert await git(root, "diff") == ""
        with pytest.raises(PermissionError, match="Codex review"):
            await f["cycle"].integration.closeout_local(
                task, candidate, branch="feat/fixture", expected_head=head, commit=True
            )
        review = {
            "subject": record["review_subject"],
            "reviewer": "Codex",
            "disposition": "ACCEPT_RECOMMENDED",
            "rationale": "Synthetic exact-source independent review",
        }
        record = await f["cycle"].integration.closeout_local(
            task,
            candidate,
            branch="feat/fixture",
            expected_head=head,
            review=review,
            commit=True,
            push=True,
        )
        assert record["disposition"] == "FEATURE_PUBLISHED"
        again = await f["cycle"].integration.closeout_local(
            task,
            candidate,
            branch="feat/fixture",
            expected_head=head,
            review=review,
            commit=True,
            push=True,
        )
        assert again["commit"] == record["commit"]
        assert await git(root, "status", "--porcelain", "--untracked-files=no") == ""

    asyncio.run(run())


@pytest.mark.parametrize("failure", ["scope", "bytes", "unaccepted", "protected"])
def test_local_closeout_refuses_before_mutation(
    fixture: dict[str, Any], failure: str
) -> None:
    """Candidate tampering or model recommendation never grants broader effects."""

    async def run() -> None:
        f = fixture
        folder = evidence(f)
        path = folder / "result.json"
        result = json.loads(path.read_text())
        if failure == "scope":
            result["candidates"][0]["path"] = "src/devtools/private.py"
        if failure == "bytes":
            (folder / "final-source.py").write_text("changed")
        if failure == "unaccepted":
            result["accepted"] = False
        path.write_text(json.dumps(result))
        with pytest.raises(PermissionError):
            await f["cycle"].integration.closeout_local(
                f["task"],
                folder,
                branch="main" if failure == "protected" else "feat/fixture",
                expected_head=f["task"].baseline_revision,
            )
        assert await git(f["root"], "diff") == ""

    asyncio.run(run())

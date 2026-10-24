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
from scripts.backlog.integration import local as local_integration
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


@pytest.mark.parametrize("author", ["Qwen", "Codex"])
def test_local_candidate_validation_review_commit_push_and_idempotence(
    fixture: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    author: str,
) -> None:
    """Use actual scoped validation, feature commit and a bare fixture remote."""

    async def protected_fixture(*_args: object, **_kwargs: object) -> dict[str, Any]:
        return {"passed": True, "profile": "SCRIPTED-FIXTURE-ONLY"}

    monkeypatch.setattr(local_integration, "validate_tree", protected_fixture)

    async def run() -> None:
        f = fixture
        root = f["root"]
        task = f["task"]
        candidate = evidence(f)
        if author == "Codex":
            receipt = candidate / "result.json"
            value = json.loads(receipt.read_text())
            value["implementation_by"] = author
            receipt.write_text(json.dumps(value))
        await git(root, "switch", "feat/fixture")
        head = await git(root, "rev-parse", "HEAD")
        remote = root.parent / "local-origin.git"
        await git(root, "init", "--bare", str(remote))
        await git(root, "remote", "add", "origin", str(remote))
        await git(root, "push", "origin", "HEAD:refs/heads/feat/fixture")
        addition = {
            "path": "tests/test_independent.py",
            "text": "def test_independent():\n    assert True\n",
            "author": "Codex",
            "reference": "independent synthetic regression",
        }
        # This host-authored test is absent before and after temporary validation.
        assert not (root / addition["path"]).exists()
        record = await f["cycle"].integration.closeout_local(
            task,
            candidate,
            branch="feat/fixture",
            expected_head=head,
            protected_validation=True,
            additions=[addition],
            implementation_author=author,
        )
        assert record["disposition"] == "SUPERVISORY_REVIEW"
        assert record["implementation_by"] == author
        assert record["files"][0]["author"] == author
        assert await git(root, "diff") == ""
        assert not (root / addition["path"]).exists()
        with pytest.raises(PermissionError, match="Codex review"):
            await f["cycle"].integration.closeout_local(
                task,
                candidate,
                branch="feat/fixture",
                expected_head=head,
                commit=True,
                additions=[addition],
                implementation_author=author,
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
            additions=[addition],
            expected_remote=head,
            implementation_author=author,
        )
        assert record["disposition"] == "FEATURE_PUBLISHED"
        message = await git(root, "log", "-1", "--format=%B")
        assert f"Integrate reviewed {author} task:" in message
        assert f"Implementation-by: {author}\n" in message
        assert f"{author}-Result: " in message
        # Model a lost response after the local commit; reconcile, never recommit.
        interrupted = dict(record, commit=None, disposition="COMMIT_INTENT")
        (candidate / "closeout.json").write_text(json.dumps(interrupted))
        again = await f["cycle"].integration.closeout_local(
            task,
            candidate,
            branch="feat/fixture",
            expected_head=head,
            review=review,
            commit=True,
            push=True,
            additions=[addition],
            implementation_author=author,
        )
        assert again["commit"] == record["commit"]
        assert (root / addition["path"]).is_file()
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


@pytest.mark.parametrize("author", ["unknown", "Codex"])
def test_local_closeout_requires_explicit_matching_implementation_attribution(
    fixture: dict[str, Any], author: str
) -> None:
    """The trusted caller cannot silently relabel a Qwen receipt as Codex work."""

    async def run() -> None:
        folder = evidence(fixture)
        with pytest.raises((ValueError, PermissionError)):
            await fixture["cycle"].integration.closeout_local(
                fixture["task"],
                folder,
                branch="feat/fixture",
                expected_head=fixture["task"].baseline_revision,
                implementation_author=author,
            )
        assert await git(fixture["root"], "diff") == ""

    asyncio.run(run())

# Copyright (c) 2026
# ruff: noqa: COM812 -- tiny authored Git fixture
"""Exact local candidates enter the same integration owner; no model dispatch."""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pytest

from devtools.core.paths import resolve_path
from devtools.resources.commands import Command, CommandExecutor
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
@pytest.mark.parametrize(
    "test_path", ["tests/test_independent.py", "tests/test_π & independent.py"]
)
def test_local_candidate_validation_review_commit_push_and_idempotence(
    fixture: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    author: str,
    test_path: str,
) -> None:
    """Use actual scoped validation, feature commit and a bare fixture remote."""

    async def protected_fixture(*_args: object, **_kwargs: object) -> dict[str, Any]:
        return {
            "passed": True,
            "profile": "pre-publication-protected",
            "reuse_policy": "fresh-only-v1",
            "fixture_only": "scripted dispatch, not a real protected gate",
        }

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
            "path": test_path,
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


def test_ignored_ruff_drift_requires_fresh_check_before_local_commit(
    fixture: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """One real Ruff command substitutes only in this fixture, not production proof."""
    calls = []

    async def run() -> None:
        root, task = fixture["root"], fixture["task"]
        candidate = evidence(fixture)
        await git(root, "switch", "feat/fixture")
        head = await git(root, "rev-parse", "HEAD")
        # Git's own ignored configuration discovery remains active for real Ruff.
        with (root / ".git/info/exclude").open("a") as stream:
            stream.write("\n.ruff.toml\n")
        config = root / ".ruff.toml"
        config.write_bytes(b'lint.ignore = ["ALL"]\n')

        async def protected_fixture(
            *_args: object, **_kwargs: object
        ) -> dict[str, Any]:
            result = await CommandExecutor().execute(
                Command(sys.executable)
                .args("-m", "ruff", "check", task.source)
                .cwd(resolve_path(root))
            )
            calls.append(result.exit_code)
            return {
                "passed": not result.failed,
                "profile": "pre-publication-protected",
                "reuse_policy": "fresh-only-v1",
                "fixture_only": "single real Ruff check; NOT the protected gate",
            }

        monkeypatch.setattr(local_integration, "validate_tree", protected_fixture)
        integration = fixture["cycle"].integration
        first = await integration.closeout_local(
            task,
            candidate,
            branch="feat/fixture",
            expected_head=head,
            protected_validation=True,
        )
        assert first["publication_eligible"]
        # No saved result, even unchanged, attests today's unsupported environment.
        preview = await integration.closeout_local(
            task, candidate, branch="feat/fixture", expected_head=head
        )
        assert preview["publication_eligible"] is False
        assert calls == [0]
        config.write_bytes(b'required-version = "==0.0.0"\n')
        review = {
            "subject": first["review_subject"],
            "reviewer": "Codex",
            "disposition": "ACCEPT_RECOMMENDED",
            "rationale": "Explicit synthetic review fixture only",
        }
        refused = await integration.closeout_local(
            task,
            candidate,
            branch="feat/fixture",
            expected_head=head,
            commit=True,
            review=review,
        )
        assert calls == [0, 2]
        assert refused["publication_eligible"] is False
        assert refused["commit"] is None
        assert await git(root, "rev-parse", "HEAD") == head
        assert config.read_bytes() == b'required-version = "==0.0.0"\n'
        assert await git(root, "diff") == ""

    asyncio.run(run())


@pytest.mark.parametrize(
    ("profile", "policy"),
    [(None, None), ("unknown", "fresh-only-v1"), ("pre-publication-protected", None)],
)
def test_unsupported_protected_profile_cannot_authorize_commit(
    fixture: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    profile: str | None,
    policy: str | None,
) -> None:
    """Legacy or unrecognized receipts do not acquire publication authority."""

    async def unsupported(*_args: object, **_kwargs: object) -> dict[str, Any]:
        return {"passed": True, "profile": profile, "reuse_policy": policy}

    monkeypatch.setattr(local_integration, "validate_tree", unsupported)

    async def run() -> None:
        folder = evidence(fixture)
        await git(fixture["root"], "switch", "feat/fixture")
        head = await git(fixture["root"], "rev-parse", "HEAD")
        result = await fixture["cycle"].integration.closeout_local(
            fixture["task"],
            folder,
            branch="feat/fixture",
            expected_head=head,
            commit=True,
        )
        assert result["publication_eligible"] is False
        assert result["commit"] is None
        assert await git(fixture["root"], "rev-parse", "HEAD") == head

    asyncio.run(run())


def test_unpublished_committed_replay_runs_fresh_gate_on_exact_head(
    fixture: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Delayed publication checks committed inputs; accepted refs need observation."""
    calls: list[str] = []
    allowed = True

    async def run() -> None:
        nonlocal allowed
        root, task = fixture["root"], fixture["task"]
        folder = evidence(fixture)
        await git(root, "switch", "feat/fixture")
        base = await git(root, "rev-parse", "HEAD")

        async def protected_fixture(
            *_args: object, **_kwargs: object
        ) -> dict[str, Any]:
            calls.append(await git(root, "rev-parse", "HEAD"))
            return {
                "passed": allowed,
                "profile": "pre-publication-protected",
                "reuse_policy": "fresh-only-v1",
                "fixture_only": "dispatch and HEAD assertion, not a real gate",
            }

        monkeypatch.setattr(local_integration, "validate_tree", protected_fixture)
        integration = fixture["cycle"].integration
        first = await integration.closeout_local(
            task,
            folder,
            branch="feat/fixture",
            expected_head=base,
            protected_validation=True,
        )
        review = {
            "subject": first["review_subject"],
            "reviewer": "Codex",
            "disposition": "ACCEPT_RECOMMENDED",
            "rationale": "Independent synthetic review fixture",
        }
        record = await integration.closeout_local(
            task,
            folder,
            branch="feat/fixture",
            expected_head=base,
            commit=True,
            review=review,
        )
        head = record["commit"]
        assert head != base
        assert calls == [base, base]
        remote = root.parent / "delayed-origin.git"
        await git(root, "init", "--bare", str(remote))
        await git(root, "remote", "add", "origin", str(remote))
        allowed = False
        with pytest.raises(PermissionError, match="Fresh committed"):
            await integration.closeout_local(
                task,
                folder,
                branch="feat/fixture",
                expected_head=base,
                commit=True,
                push=True,
            )
        assert calls == [base, base, head]
        assert await git(root, "ls-remote", "origin", "refs/heads/feat/fixture") == ""
        allowed = True
        published = await integration.closeout_local(
            task,
            folder,
            branch="feat/fixture",
            expected_head=base,
            commit=True,
            push=True,
        )
        assert published["disposition"] == "FEATURE_PUBLISHED"
        assert calls == [base, base, head, head]
        again = await integration.closeout_local(
            task,
            folder,
            branch="feat/fixture",
            expected_head=base,
            commit=True,
            push=True,
        )
        assert calls == [base, base, head, head]
        assert again["commit"] == head
        assert again["publication_eligible"] is False
        assert "historical" in again["validation_claim"]
        assert await git(root, "rev-parse", "HEAD") == head

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

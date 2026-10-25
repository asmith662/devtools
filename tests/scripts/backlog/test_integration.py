# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, SLF001, ASYNC240 -- isolated Git/authority fixtures
"""Real local Git lifecycle; synthetic accepted work, never live model calls."""

from __future__ import annotations

import argparse
import asyncio
import difflib
import getpass
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import pytest

from devtools.core.time import Duration, Timestamp
from devtools.resources.filesystem import write
from devtools.resources.filesystem.errors import FilesystemError
from scripts.backlog.checkout import Checkout
from scripts.backlog.coordinator import git
from scripts.backlog.integration import cli as integration_cli
from scripts.backlog.integration import lifecycle
from scripts.backlog.integration.authority import ACTIONS
from scripts.backlog.integration.git import publish, remote_head
from tests.scripts.backlog import test_work as helpers
from tests.scripts.backlog.test_work import fixture as fixture  # noqa: PLC0414


def test_exact_planned_path_population_with_unicode_and_special_names(
    fixture: dict[str, Any],
) -> None:
    """Real staged and untracked paths authenticate; unplanned names still refuse."""

    async def run() -> None:
        f = fixture
        root, cycle = f["root"], f["cycle"]
        names = ["tests/test_π.py", "tests/test spaced & (π).py"]
        if os.name != "nt":
            names.extend(['tests/test_"quoted".py', "tests/test_new\nline.py"])
        text = "def test_literal():\n    assert True\n"
        files = [
            {
                "path": name,
                "text": text,
                "sha256": hashlib.sha256(text.encode()).hexdigest(),
            }
            for name in names
        ]
        plan = {
            "feature": "feat/fixture",
            "destination_base": f["task"].baseline_revision,
            "files": files,
        }
        integration = cycle.integration
        async with Checkout(
            cycle,
            "exact-planned-paths",
            "feat/fixture",
            f["task"].baseline_revision,
            files=files,
        ) as owner:
            integration._checkout = owner
            for entry in files:
                owner.expect(entry["path"], text)
                (root / entry["path"]).write_bytes(text.encode())
            # First inspect real untracked filenames, then the staged diff.
            expected = {
                name: hashlib.sha256(text.encode()).hexdigest() for name in names
            }
            assert await integration._files(plan, root) == expected
            await git(root, "add", "--", *names)
            assert await integration._files(plan, root) == expected
            plain = await git(root, "diff", "--name-only", f["task"].baseline_revision)
            assert '"tests/test_' in plain  # default Git quoting is genuinely active
            extra = root / "tests/unplanned_π.py"
            extra.write_bytes(b"# unplanned\n")
            with pytest.raises(PermissionError, match="Unapproved files"):
                await integration._files(plan, root)
            extra.unlink()
            (root / names[0]).write_bytes(b"# wrong planned bytes\n")
            with pytest.raises(PermissionError, match="Unreviewed change"):
                await integration._files(plan, root)
            (root / names[0]).write_bytes(text.encode())

    asyncio.run(run())


async def setup(f: dict[str, Any]) -> dict[str, Any]:
    """Build explicitly synthetic accepted evidence and an owned bare origin."""
    a = await helpers.prepare(f)
    c = f["cycle"]
    work = c._folder(f["item"])
    (work / "worker").mkdir()
    source = a["baseline_source"].replace(helpers.OLD, helpers.GOOD)
    (work / "worker/final-source.py").write_bytes(source.encode())
    (work / "candidate.patch").write_bytes(
        "".join(
            difflib.unified_diff(
                a["baseline_source"].splitlines(keepends=True),
                source.splitlines(keepends=True),
                fromfile="a/" + f["task"].source,
                tofile="b/" + f["task"].source,
            )
        ).encode()
    )
    auth = c._save(
        work / "authorization.json",
        {
            "schema": "backlog-qwen-authorization-v1",
            "assignment_sha256": a["sha256"],
            "principal": getpass.getuser(),
        },
    )
    result = c._save(
        work / "result.json",
        {
            "schema": "backlog-qwen-result-v1",
            "item": f["item"],
            "assignment_sha256": a["sha256"],
            "authorization_sha256": auth["sha256"],
            "disposition": "REVIEW_CANDIDATE",
            "candidate_changed_files": [f["task"].source],
            "candidate_sha256": lifecycle.digest_text(source),
            "validation": {"accepted": True},
        },
    )
    review = c._save(
        work / ("supervision-" + "a" * 64 + ".json"),
        {
            "schema": "backlog-qwen-supervision-v1",
            "reviewer": "Codex",
            "result_sha256": result["sha256"],
            "assignment_sha256": a["sha256"],
            "disposition": "ACCEPT_RECOMMENDED",
        },
    )
    (work / ("supervision-" + "a" * 64 + ".json")).rename(
        work / ("supervision-" + review["sha256"] + ".json")
    )
    remote = f["root"].parent / "origin.git"
    await git(f["root"], "init", "--bare", str(remote))
    await git(f["root"], "remote", "add", "origin", str(remote))
    base = a["base_head"]
    await git(
        f["root"],
        "push",
        "origin",
        base + ":refs/heads/delivery",
        base + ":refs/heads/coordinator",
        base + ":refs/heads/main",
    )
    spec = {
        "remote": "origin",
        "destination": "delivery",
        "feature": "feat/integration-fixture",
        "checkout": str(f["root"]),
        "additions": [],
        "parent_complete": False,
        "remaining": ["A separate parent obligation remains"],
        "rationale": "Synthetic slice only",
        "validation_seconds": 120,
    }
    plan = await c.integration.plan(f["item"], review["sha256"], spec)
    policy = {
        "sources": [f["task"].source],
        "tests": list(f["task"].tests),
        "oracles": [f["task"].oracle_sha256],
        "remote": "origin",
        "destinations": ["delivery", "main"],
        "checkout": str(f["root"]),
        "actions": list(ACTIONS),
        "protected": False,
        "corrections": False,
        "parent_close": False,
        "max_integrations": 2,
        "max_files": 3,
        "max_bytes": 65536,
        "validation_seconds": 120,
    }
    grant = await c.integration.authority.issue(
        policy,
        reference="fixture://human-integration-policy",
        expires=Timestamp.now() + Duration.minutes(10),
        authorize=lambda _: True,
    )
    return {
        **f,
        "integration": c.integration,
        "plan": plan,
        "spec": spec,
        "policy": policy,
        "grant": grant,
        "review": review,
    }


@pytest.fixture
def prepared(
    fixture: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> dict[str, Any]:
    """Use Git/authority production paths; substitute costly validation only."""
    f = asyncio.run(setup(fixture))

    async def checks(
        checkout: Path, evidence: Path, plan: dict[str, Any], oracle: str, *, post: bool
    ) -> dict[str, Any]:
        # The production fixed gate is tested separately. Never present this
        # stand-in as actual protected validation or Qwen competence.
        evidence.mkdir()
        actual = (checkout / plan["source"]).read_bytes().decode()
        expected = plan["files"][0]["text"]
        assert (
            actual.replace("\r\n", "\n") == expected.replace("\r\n", "\n")
            if post
            else actual == expected
        )
        assert oracle == f["task"].oracle
        return {"passed": True, "fixture_only": True, "post": post}

    monkeypatch.setattr(lifecycle, "validate_tree", checks)
    return f


async def through_publish(f: dict[str, Any]) -> dict[str, Any]:
    """Advance actual integration stages, including native Git commit/push."""
    i = f["integration"]
    item = f["item"]
    p = f["plan"]["sha256"]
    g = f["grant"]["sha256"]
    await i.install(item, p, g)
    await i.validate(item, p, g)
    await i.review(
        item,
        p,
        g,
        decision="APPROVE_INTEGRATION",
        reference="fixture://tree-review",
        rationale="Exact tree, scope and target reviewed",
    )
    result: dict[str, Any] = await i.publish(item, p, g)
    return result


def test_full_git_cycle_and_partial_parent_closeout(prepared: dict[str, Any]) -> None:
    """Source installation through remote promotion and authoritative progress."""

    async def run() -> None:
        f = prepared
        i = f["integration"]
        p = f["plan"]["sha256"]
        g = f["grant"]["sha256"]
        item = f["item"]
        publication = await through_publish(f)
        assert await i.publish(item, p, g) == publication
        other = await i.authority.issue(
            f["policy"],
            reference="fixture://different-grant",
            expires=Timestamp.now() + Duration.minutes(10),
            authorize=lambda _: True,
        )
        with pytest.raises(PermissionError, match="Different grant"):
            await i.promote(item, p, other["sha256"])
        promoted = await i.promote(item, p, g)
        assert await i.promote(item, p, g) == promoted
        verification = await i.verify(item, p, g)
        assert verification["disposition"] == "DESTINATION_VERIFIED"
        await i.close_review(
            item,
            p,
            g,
            decision="SLICE_ONLY",
            reference="fixture://close-review",
            rationale="Other obligation remains",
        )
        completion = await i.closeout(item, p, g)
        assert completion["disposition"] == "VERIFIED_COMPLETION"
        assert not completion["parent_closed"]
        assert await i.closeout(item, p, g) == completion
        binding = f["intake"].approved_item(item)
        assert binding["status"] == "BACKLOG"
        assert promoted["destination_commit"] in binding["text"]
        assert i.status(item, p)["disposition"] == "VERIFIED_COMPLETION"
        assert (
            f["cycle"].status(item)["integration"][0]["disposition"]
            == "VERIFIED_COMPLETION"
        )
        assert (
            await git(
                Path(f["spec"]["checkout"]),
                "show",
                "-s",
                "--format=%P",
                publication["commit"],
            )
            == f["task"].baseline_revision
        )
        assert await git(f["target"], "status", "--porcelain") == ""

    asyncio.run(run())


@pytest.mark.parametrize("published", [False, True])
def test_missing_integration_branch_requires_reconciliation(
    prepared: dict[str, Any], *, published: bool
) -> None:
    """A deleted branch never silently creates another integration commit."""

    async def run() -> None:
        f = prepared
        i, p, g, item = (
            f["integration"],
            f["plan"]["sha256"],
            f["grant"]["sha256"],
            f["item"],
        )
        if published:
            result = await through_publish(f)
        else:
            await i.install(item, p, g)
        await git(f["root"], "branch", "-D", f["spec"]["feature"])
        operation = i.publish if published else i.install
        with pytest.raises(PermissionError, match="branch missing"):
            await operation(item, p, g)
        assert not await git(
            f["root"],
            "for-each-ref",
            "--format=%(objectname)",
            "refs/heads/" + f["spec"]["feature"],
        )
        if published:
            assert (
                await remote_head(f["root"], "origin", f["spec"]["feature"])
                == result["commit"]
            )

    asyncio.run(run())


@pytest.mark.parametrize("failure", ["missing", "expired", "revoked", "scope"])
def test_integration_authority_refusals(
    prepared: dict[str, Any], monkeypatch: pytest.MonkeyPatch, failure: str
) -> None:
    """Coding/approval recommendations never act as integration authority."""

    async def run() -> None:
        f = prepared
        i = f["integration"]
        g = f["grant"]["sha256"]
        if failure == "missing":
            g = "0" * 64
        elif failure == "expired":
            future = Timestamp.now() + Duration.minutes(1440)
            monkeypatch.setattr(Timestamp, "now", classmethod(lambda _cls: future))
        elif failure == "revoked":
            await i.authority.revoke(
                g, reference="fixture://revoke", authorize=lambda _: True
            )
        else:
            f["grant"]["policy"]["sources"] = ["src/devtools/other.py"]
            # A tampered sealed grant is refused rather than expanded.
            path = i.authority.folder(g) / "grant.json"
            path.write_text(json.dumps(f["grant"]))
        with pytest.raises((PermissionError, ValueError, OSError, FilesystemError)):
            await i.install(f["item"], f["plan"]["sha256"], g)
        assert not (f["root"] / ".local/backlog/checkout-owner").exists()

    asyncio.run(run())


def test_tampered_candidate_and_rejected_review_refuse(
    prepared: dict[str, Any],
) -> None:
    """Accepted review cannot authorize changed bytes or a rejected result."""

    async def run() -> None:
        f = prepared
        folder = f["cycle"]._folder(f["item"])
        path = folder / "worker/final-source.py"
        path.write_bytes(path.read_bytes() + b"# unreviewed\n")
        with pytest.raises(PermissionError, match="authenticate"):
            await f["integration"].install(
                f["item"], f["plan"]["sha256"], f["grant"]["sha256"]
            )

    asyncio.run(run())


def test_unapproved_changes_and_validation_failure_block_publication(
    prepared: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Neither new files nor a failed test can inherit acceptance."""

    async def run() -> None:
        f = prepared
        i = f["integration"]
        p = f["plan"]["sha256"]
        g = f["grant"]["sha256"]
        await i.install(f["item"], p, g)
        extra = f["root"] / ".gitignore"
        original = extra.read_bytes()
        extra.write_bytes(original + b"# unrelated edit\n")
        with pytest.raises(PermissionError, match="not clean"):
            await i.validate(f["item"], p, g)
        assert extra.read_bytes() == original + b"# unrelated edit\n"
        extra.write_bytes(original)

        async def fail(*_args: object, **_kwargs: object) -> dict[str, Any]:
            return {"passed": False, "fixture_only": True}

        monkeypatch.setattr(lifecycle, "validate_tree", fail)
        result = await i.validate(f["item"], p, g)
        assert result["disposition"] == "REWORK_REQUIRED"
        with pytest.raises(PermissionError, match="Failed validation"):
            await i.review(
                f["item"],
                p,
                g,
                decision="APPROVE_INTEGRATION",
                reference="fixture",
                rationale="Cannot approve failed work",
            )
        assert not await remote_head(f["root"], "origin", f["spec"]["feature"])

    asyncio.run(run())


def test_remote_divergence_and_protected_refusal(prepared: dict[str, Any]) -> None:
    """Target CAS and protected policy prevent overwriting unrelated history."""

    async def run() -> None:
        f = prepared
        i = f["integration"]
        p = f["plan"]["sha256"]
        g = f["grant"]["sha256"]
        publication = await through_publish(f)
        await git(
            f["root"], "commit", "--allow-empty", "-m", "Unrelated destination advance"
        )
        advanced = await git(f["root"], "rev-parse", "HEAD")
        await git(f["root"], "push", "origin", advanced + ":refs/heads/delivery")
        with pytest.raises(PermissionError, match="advanced"):
            await i.promote(f["item"], p, g)
        with pytest.raises(PermissionError, match="grant AND repository"):
            await i.authority.admit(g, {**f["plan"], "destination": "main"}, "promote")
        assert await remote_head(f["root"], "origin", "delivery") == advanced
        assert publication["commit"] != advanced

    asyncio.run(run())


@pytest.mark.parametrize("after_push", [False, True])
def test_commit_interruption_reconciles_without_duplicate(
    prepared: dict[str, Any], monkeypatch: pytest.MonkeyPatch, *, after_push: bool
) -> None:
    """A commit followed by lost publication observation reuses the exact commit."""

    async def run() -> None:
        f = prepared
        i = f["integration"]
        p = f["plan"]["sha256"]
        g = f["grant"]["sha256"]
        original = publish

        async def unavailable(
            root: Path, remote: str, branch: str, commit: str, expected: str
        ) -> None:
            if after_push:
                await original(root, remote, branch, commit, expected)
            raise OSError("fixture connection lost after commit")

        monkeypatch.setattr(lifecycle, "publish", unavailable)
        with pytest.raises(OSError, match="connection"):
            await through_publish(f)
        commit = await git(f["root"], "rev-parse", f["spec"]["feature"])
        assert i.status(f["item"], p)["disposition"] == "RECONCILIATION_REQUIRED"
        monkeypatch.setattr(lifecycle, "publish", original)
        result = await i.publish(f["item"], p, g)
        assert result["commit"] == commit
        assert (
            await git(
                Path(f["spec"]["checkout"]),
                "rev-list",
                "--count",
                f["task"].baseline_revision + ".." + f["spec"]["feature"],
            )
            == "1"
        )

    asyncio.run(run())


def test_protected_promotion_requires_both_policies(prepared: dict[str, Any]) -> None:
    """A grant alone never changes the repository's protected publication policy."""

    async def run() -> None:
        f = prepared
        i = f["integration"]
        spec = {**f["spec"], "destination": "main"}
        plan = await i.plan(f["item"], f["review"]["sha256"], spec)
        grant = await i.authority.issue(
            {**f["policy"], "protected": True},
            reference="fixture://protected-grant",
            expires=Timestamp.now() + Duration.minutes(10),
            authorize=lambda _: True,
        )
        f = {**f, "plan": plan, "grant": grant}
        await through_publish(f)
        with pytest.raises(PermissionError, match="grant AND repository"):
            await i.promote(f["item"], plan["sha256"], grant["sha256"])
        await git(
            f["root"],
            "config",
            "--add",
            "devtools.integrationProtectedTarget",
            "origin:main",
        )
        result = await i.promote(f["item"], plan["sha256"], grant["sha256"])
        assert (
            await remote_head(f["root"], "origin", "main")
            == result["destination_commit"]
        )

    asyncio.run(run())


def test_parent_close_requires_explicit_scope_and_decision(
    prepared: dict[str, Any],
) -> None:
    """Only a complete plan, parent-close grant and explicit review can close work."""

    async def run() -> None:
        f = prepared
        i = f["integration"]
        spec = {**f["spec"], "parent_complete": True, "remaining": []}
        plan = await i.plan(f["item"], f["review"]["sha256"], spec)
        with pytest.raises(PermissionError, match="Parent backlog"):
            await i.authority.admit(f["grant"]["sha256"], plan, "install")
        grant = await i.authority.issue(
            {**f["policy"], "parent_close": True},
            reference="fixture://complete-parent",
            expires=Timestamp.now() + Duration.minutes(10),
            authorize=lambda _: True,
        )
        f = {**f, "plan": plan, "grant": grant}
        p, g, item = plan["sha256"], grant["sha256"], f["item"]
        await through_publish(f)
        await i.promote(item, p, g)
        await i.verify(item, p, g)
        with pytest.raises(PermissionError, match="completion decision"):
            await i.close_review(
                item,
                p,
                g,
                decision="SLICE_ONLY",
                reference="fixture",
                rationale="Wrong decision",
            )
        await i.close_review(
            item,
            p,
            g,
            decision="COMPLETE_PARENT",
            reference="fixture://complete",
            rationale="All fixture obligations validated",
        )
        result = await i.closeout(item, p, g)
        assert result["parent_closed"]
        assert "- status: CLOSED" in Path(plan["backlog"]["path"]).read_text()
        assert "| CLOSED |" in (f["root"] / "docs/backlog/overview.md").read_text()

    asyncio.run(run())


def test_post_validation_failure_prevents_closeout(
    prepared: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Remote publication success is not verified scientific or engineering success."""

    async def run() -> None:
        f = prepared
        i, p, g, item = (
            f["integration"],
            f["plan"]["sha256"],
            f["grant"]["sha256"],
            f["item"],
        )
        await through_publish(f)
        await i.promote(item, p, g)

        async def failed(*_args: object, **_kwargs: object) -> dict[str, Any]:
            return {"passed": False, "fixture_only": True}

        monkeypatch.setattr(lifecycle, "validate_tree", failed)
        result = await i.verify(item, p, g)
        assert result["disposition"] == "POST_INTEGRATION_FAILED"
        with pytest.raises(PermissionError, match="Verified destination"):
            await i.close_review(
                item,
                p,
                g,
                decision="SLICE_ONLY",
                reference="fixture",
                rationale="Cannot close",
            )
        assert f["intake"].approved_item(item)["text"] == f["plan"]["backlog"]["text"]

    asyncio.run(run())


def test_missing_and_rejected_review(prepared: dict[str, Any]) -> None:
    """Neither absence nor an explicit rejection can become publication authority."""

    async def run() -> None:
        f = prepared
        i, p, g, item = (
            f["integration"],
            f["plan"]["sha256"],
            f["grant"]["sha256"],
            f["item"],
        )
        await i.install(item, p, g)
        await i.validate(item, p, g)
        with pytest.raises(FilesystemError):
            await i.publish(item, p, g)
        await i.review(
            item,
            p,
            g,
            decision="REJECT",
            reference="fixture://rejected",
            rationale="Review rejects this tree",
        )
        with pytest.raises(PermissionError, match="approval required"):
            await i.publish(item, p, g)
        assert not await remote_head(f["root"], "origin", f["spec"]["feature"])

    asyncio.run(run())


def test_plan_detects_diverged_source_and_excludes_history(
    prepared: dict[str, Any],
) -> None:
    """Select source without importing unrelated source-branch ancestry."""

    async def run() -> None:
        f = prepared
        root = f["root"]
        await git(root, "commit", "--allow-empty", "-m", "Unrelated destination change")
        head = await git(root, "rev-parse", "HEAD")
        await git(root, "push", "origin", head + ":refs/heads/delivery")
        new = await f["integration"].plan(f["item"], f["review"]["sha256"], f["spec"])
        assert new["destination_base"] == head
        assert new["merge_base"] == f["task"].baseline_revision
        path = root / f["task"].source
        path.write_bytes(path.read_bytes() + b"# destination diverged\n")
        await git(root, "add", "--", f["task"].source)
        await git(root, "commit", "-m", "Independent source modification")
        await git(root, "push", "origin", "HEAD:refs/heads/delivery")
        with pytest.raises(PermissionError, match="source diverged"):
            await f["integration"].plan(f["item"], f["review"]["sha256"], f["spec"])
        tree = await git(root, "rev-parse", f["task"].baseline_revision + "^{tree}")
        orphan = await git(root, "commit-tree", tree, "-m", "Unrelated root")
        await git(root, "push", "origin", orphan + ":refs/heads/unrelated")
        with pytest.raises(ValueError, match="merge-base"):
            await f["integration"].plan(
                f["item"],
                f["review"]["sha256"],
                {**f["spec"], "destination": "unrelated"},
            )

    asyncio.run(run())


@pytest.mark.parametrize(
    ("answer", "expected"), [("", False), ("n", False), ("y", True)]
)
def test_integration_consent_is_real_default_no(
    monkeypatch: pytest.MonkeyPatch, answer: str, *, expected: bool
) -> None:
    """Only an actual interactive local principal can issue policy consent."""
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _: answer)
    assert integration_cli.confirm({"principal": getpass.getuser()}) is expected
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    with pytest.raises(PermissionError, match="interactive"):
        integration_cli.confirm({"principal": getpass.getuser()})


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("destinations", ["other"]),
        ("sources", ["src/devtools/other.py"]),
        ("tests", ["tests/other.py"]),
        ("oracles", ["0" * 64]),
        ("max_bytes", 1),
    ],
)
def test_each_integration_scope_is_enforced(
    prepared: dict[str, Any], field: str, value: object
) -> None:
    """An applicable grant must cover every path, target and oracle."""

    async def run() -> None:
        f = prepared
        i = f["integration"]
        grant = await i.authority.issue(
            {**f["policy"], field: value},
            reference="fixture://restricted-policy",
            expires=Timestamp.now() + Duration.minutes(10),
            authorize=lambda _: True,
        )
        with pytest.raises(PermissionError):
            await i.install(f["item"], f["plan"]["sha256"], grant["sha256"])
        assert not (f["root"] / ".local/backlog/checkout-owner").exists()

    asyncio.run(run())


def test_reservation_exhaustion_and_partial_install_recovery(
    prepared: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Interrupted installation retains its reservation and resumes exact bytes."""

    async def run() -> None:
        f = prepared
        i, item = f["integration"], f["item"]
        grant = await i.authority.issue(
            {**f["policy"], "max_integrations": 1},
            reference="fixture://one-integration",
            expires=Timestamp.now() + Duration.minutes(10),
            authorize=lambda _: True,
        )
        original = write

        def unavailable(*_args: object, **_kwargs: object) -> None:
            raise OSError("fixture installation interrupted")

        monkeypatch.setattr(lifecycle, "write", unavailable)
        with pytest.raises(OSError, match="interrupted"):
            await i.install(item, f["plan"]["sha256"], grant["sha256"])
        monkeypatch.setattr(lifecycle, "write", original)
        result = await i.install(item, f["plan"]["sha256"], grant["sha256"])
        assert result["disposition"] == "INSTALLED"
        spec = {
            **f["spec"],
            "feature": "feat/another",
            "checkout": str(f["root"]),
        }
        second = await i.plan(item, f["review"]["sha256"], spec)
        with pytest.raises(PermissionError, match="exhausted"):
            await i.install(item, second["sha256"], grant["sha256"])
        assert not (f["root"] / ".local/backlog/checkout-owner").exists()

    asyncio.run(run())


def test_independent_additions_require_scope_and_tree_review(
    prepared: dict[str, Any],
) -> None:
    """Independent tests retain attribution and need an expanded explicit grant."""

    async def run() -> None:
        f = prepared
        addition = {
            "path": "tests/independent.py",
            "text": "def test_independent() -> None:\n    assert True\n",
            "author": "Codex",
            "reference": "fixture://independent-test",
        }
        plan = await f["integration"].plan(
            f["item"], f["review"]["sha256"], {**f["spec"], "additions": [addition]}
        )
        with pytest.raises(PermissionError, match="Unapproved"):
            await f["integration"].install(
                f["item"], plan["sha256"], f["grant"]["sha256"]
            )
        grant = await f["integration"].authority.issue(
            {**f["policy"], "tests": [*f["policy"]["tests"], addition["path"]]},
            reference="fixture://tests-in-scope",
            expires=Timestamp.now() + Duration.minutes(10),
            authorize=lambda _: True,
        )
        await git(f["root"], "config", "core.autocrlf", "true")
        result = await through_publish({**f, "plan": plan, "grant": grant})
        body = await git(f["root"], "show", "-s", "--format=%B", result["commit"])
        assert "Codex:fixture://independent-test" in body
        assert plan["files"][0]["author"] == "Qwen"
        i, p, g, item = f["integration"], plan["sha256"], grant["sha256"], f["item"]
        await i.promote(item, p, g)
        verified = await i.verify(item, p, g)
        assert verified["disposition"] == "DESTINATION_VERIFIED"
        assert (
            verified["materialized_sha256"][addition["path"]]
            != verified["planned_sha256"][addition["path"]]
        )

    asyncio.run(run())


def test_branch_switch_and_unrelated_commit_refuse(prepared: dict[str, Any]) -> None:
    """An allowed file tree cannot launder an unrelated commit or branch."""

    async def run() -> None:
        f = prepared
        i, p, g, item = (
            f["integration"],
            f["plan"]["sha256"],
            f["grant"]["sha256"],
            f["item"],
        )
        await i.install(item, p, g)
        checkout = Path(f["spec"]["checkout"])
        await git(checkout, "switch", "-c", "feat/rogue")
        with pytest.raises(PermissionError, match="branch differs"):
            await i.validate(item, p, g)
        await git(checkout, "switch", "coordinator")
        await i.validate(item, p, g)
        decision = await i.review(
            item,
            p,
            g,
            decision="APPROVE_INTEGRATION",
            reference="fixture://review",
            rationale="Exact reviewed tree",
        )
        assert (
            await i.review(
                item,
                p,
                g,
                decision="APPROVE_INTEGRATION",
                reference="fixture://review",
                rationale="Exact reviewed tree",
            )
            == decision
        )
        await git(checkout, "switch", f["spec"]["feature"])
        await git(
            checkout,
            "commit",
            "--allow-empty",
            "-m",
            "Unrelated commit without integration provenance",
        )
        await git(checkout, "switch", "coordinator")
        with pytest.raises(
            PermissionError, match="Unrelated integration feature history"
        ):
            await i.publish(item, p, g)
        assert not await remote_head(f["root"], "origin", f["spec"]["feature"])

    asyncio.run(run())


def test_rejected_candidate_review_refuses_planning(prepared: dict[str, Any]) -> None:
    """Publication cannot even be planned from an explicitly rejected candidate."""

    async def run() -> None:
        f = prepared
        work = f["cycle"]._folder(f["item"])
        value = {k: v for k, v in f["review"].items() if k != "sha256"}
        value["disposition"] = "REJECT"
        record = f["cycle"]._save(work / "synthetic-rejection.json", value)
        (work / "synthetic-rejection.json").rename(
            work / ("supervision-" + record["sha256"] + ".json")
        )
        with pytest.raises(PermissionError, match="authenticate"):
            await f["integration"].plan(f["item"], record["sha256"], f["spec"])

    asyncio.run(run())


def test_windows_backlog_materialization_preserves_review_binding(
    prepared: dict[str, Any],
) -> None:
    """Git newline conversion does not change the original approved work scope."""

    async def run() -> None:
        f = prepared
        binding = f["intake"].approved_item(f["item"])
        path = Path(binding["path"])
        path.write_bytes(
            binding["text"].replace("\r\n", "\n").replace("\n", "\r\n").encode()
        )
        current = f["intake"].approved_item(f["item"])
        assert current["review"] == binding["review"]
        plan = await f["integration"].plan(
            f["item"],
            f["review"]["sha256"],
            {**f["spec"], "rationale": "Rebind only current canonical materialization"},
        )
        assert plan["backlog"] == current
        assert plan["candidate_sha256"] == f["plan"]["candidate_sha256"]
        path.write_bytes(path.read_bytes() + b"\nChanged objective\n")
        with pytest.raises(PermissionError, match="Backlog changed"):
            await f["integration"].plan(f["item"], f["review"]["sha256"], f["spec"])

    asyncio.run(run())


def test_cli_refusal_is_durable_and_nonexecuting(prepared: dict[str, Any]) -> None:
    """A missing integration grant produces inspectable BLOCKED evidence only."""
    f = prepared
    args = argparse.Namespace(
        command="integration-install",
        item=f["item"],
        plan=f["plan"]["sha256"],
        grant="0" * 64,
    )
    with pytest.raises(ValueError, match="does not exist"):
        asyncio.run(integration_cli.run(args, f["root"]))
    state = f["integration"].status(f["item"], f["plan"]["sha256"])
    assert state["disposition"] == "BLOCKED"
    assert state["refusals"][0]["action"] == "integration-install"
    assert not (f["root"] / ".local/backlog/checkout-owner").exists()


def test_corrupt_reservation_refuses_resume(prepared: dict[str, Any]) -> None:
    """Retained reservations are authenticated rather than silently reused."""

    async def run() -> None:
        f = prepared
        i, p, g, item = (
            f["integration"],
            f["plan"]["sha256"],
            f["grant"]["sha256"],
            f["item"],
        )
        await i.install(item, p, g)
        path = i.authority.folder(g) / "reservations" / (p + ".json")
        value = json.loads(path.read_text())
        value["validation_seconds"] += 1
        path.write_text(json.dumps(value))
        with pytest.raises(ValueError, match="identity/schema"):
            await i.install(item, p, g)
        assert (
            Path(f["spec"]["checkout"]) / f["task"].source
        ).read_bytes().decode().replace("\r\n", "\n") == f[
            "cycle"
        ].integration.candidate(f["item"], f["review"]["sha256"])["assignment"][
            "baseline_source"
        ].replace("\r\n", "\n")

    asyncio.run(run())

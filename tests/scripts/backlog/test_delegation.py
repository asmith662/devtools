# Copyright (c) 2026
# ruff: noqa: COM812, SLF001, PLR2004 -- isolated synthetic host authority
"""Standing authority through the existing worker; no live model or real grant."""

from __future__ import annotations

import asyncio
import getpass
import json
import sys
from dataclasses import asdict, replace
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen.development_task import _structured_edit_definition
from devtools.core.time import Duration, Timestamp
from devtools.models.interaction import (
    ModelRequest,
    ModelResponse,
    ModelSettings,
    ModelToolCall,
    Prompt,
)
from devtools.resources.filesystem.errors import FilesystemError
from scripts.backlog import __main__ as cli
from scripts.backlog.coordinator import git
from scripts.backlog.delegation import Delegations, validate_policy
from scripts.qwen.llama_cpp_profile import QWEN38_27B_UD_IQ4_XS
from tests.scripts.backlog import test_work as helpers
from tests.scripts.backlog.test_work import fixture as fixture  # noqa: PLC0414

if TYPE_CHECKING:
    from pathlib import Path


def policy(f: dict[str, Any]) -> dict[str, Any]:
    """Define synthetic policy for one fixture task, never real authority."""
    task = f["task"]
    return {
        "categories": ["bug"],
        "sources": [task.source],
        "tests": list(task.tests),
        "oracles": [task.oracle_sha256],
        "per_task": {"calls": 3, "output_tokens": 4096, "seconds": 900, "edits": 3},
        "total": {"tasks": 1, "calls": 3, "output_tokens": 12288, "seconds": 900},
    }


async def setup(
    f: dict[str, Any],
) -> tuple[Delegations, dict[str, Any], dict[str, Any]]:
    """Prepare and explicitly consent only inside a disposable repository."""
    assignment = await helpers.prepare(f)
    owner = Delegations(f["cycle"])
    grant = await owner.issue(
        policy(f),
        principal=getpass.getuser(),
        reference="fixture://human-standing-decision",
        expires_at=Timestamp.now() + Duration.minutes(5),
        authorize=lambda _: True,
    )
    return owner, grant, assignment


async def review(
    owner: Delegations, f: dict[str, Any], grant: dict[str, Any]
) -> dict[str, Any]:
    """Attribute a synthetic supervisor decision through the trusted host API."""
    return await owner.review(
        f["item"],
        grant["sha256"],
        reference="fixture://codex-review",
        rationale="Synthetic one-file maintenance; acceptance checked",
        disposition="APPROVE_ROUTINE",
    )


def provenance() -> dict[str, Any]:
    """Represent a pinned local profile; the fixture interaction remains scripted."""
    return {
        "model": "qwen38-local",
        "endpoint": "http://127.0.0.1:8080",
        "profile": asdict(QWEN38_27B_UD_IQ4_XS),
        "service": {
            "state": "READY",
            "expected_fingerprint": "fixture",
            "observed_fingerprint": "fixture",
        },
    }


def test_delegated_scripted_repair_and_review_without_terminal(
    fixture: dict[str, Any],
) -> None:
    """Exact authority uses real isolated edits/tests and never a second executor."""

    async def run() -> None:
        owner, grant, _ = await setup(fixture)
        decision = await review(owner, fixture, grant)
        authority = await owner.authorize(
            fixture["item"], grant["sha256"], decision["sha256"]
        )
        model = helpers.Scripted(
            [(helpers.OLD, helpers.WRONG), (helpers.WRONG, helpers.GOOD)]
        )

        async def factory() -> tuple[Any, dict[str, Any]]:
            return model, provenance()

        result = await fixture["cycle"].execute(
            fixture["item"], interaction_factory=factory
        )
        assert result["disposition"] == "REVIEW_CANDIDATE"
        assert result["model_calls"] == 2
        assert result["repair_cycles"] == 1
        assert not result["integration_authorized"]
        assert result["objective"]
        post = await owner.review(
            fixture["item"],
            grant["sha256"],
            reference="fixture://review-result",
            rationale="Independent checks passed; integration remains separate",
            disposition="ACCEPT_RECOMMENDED",
            result_sha256=result["sha256"],
        )
        assert post["reviewer"] == "Codex"
        assert not post["integration_authorized"]
        with pytest.raises(PermissionError, match="Prior dispatch"):
            await fixture["cycle"].execute(fixture["item"], interaction_factory=factory)
        assert len(model.requests) == 2
        assert authority["delegation"] == grant["sha256"]

    asyncio.run(run())


def test_delegated_native_context_worker_preserves_assignment_scope(
    fixture: dict[str, Any],
) -> None:
    """New task digest admits exact read-only native Tools through the same guard."""

    async def run() -> None:
        fixture["task"] = replace(fixture["task"], context_mode="on-demand")
        owner, grant, assignment = await setup(fixture)
        decision = await review(owner, fixture, grant)
        await owner.authorize(fixture["item"], grant["sha256"], decision["sha256"])

        class Investigate(helpers.Scripted):
            async def send(self, request: ModelRequest) -> ModelResponse:
                if not self.requests:
                    self.requests.append(request)
                    return ModelResponse(
                        "Inspect source",
                        self.source,
                        tool_calls=(
                            ModelToolCall(
                                "search_source",
                                '{"query":"closes","mode":"symbol"}',
                                "search",
                            ),
                        ),
                    )
                self.requests.append(request)
                # Use the existing scripted proposal as the second native call.
                return await helpers.Scripted([(helpers.OLD, helpers.GOOD)]).send(
                    request
                )

        model = Investigate([])

        async def factory() -> tuple[Any, dict[str, Any]]:
            return model, provenance()

        result = await fixture["cycle"].execute(
            fixture["item"], interaction_factory=factory
        )
        assert result["disposition"] == "REVIEW_CANDIDATE", result
        assert result["model_calls"] == 2
        assert assignment["task_sha256"] == fixture["task"].definition_sha256
        assert model.requests[1].prompt.messages[-1].role == "tool"
        assert not result["integration_authorized"]
        # Broader read paths never inherit an eligible source-only grant.
        other = replace(
            fixture["task"],
            read_paths=("src/devtools/private.py",),
            baseline_hashes=(
                *fixture["task"].baseline_hashes,
                ("src/devtools/private.py", "0" * 64),
            ),
            context=(
                *fixture["task"].context,
                ("src/devtools/private.py", "private", "file", "file"),
            ),
        )
        with pytest.raises(PermissionError, match="outside delegation"):
            owner.eligible(grant["policy"], assignment, other)

    asyncio.run(run())


@pytest.mark.parametrize("change", ["source", "tests", "oracle", "category", "limit"])
def test_scope_refusals(fixture: dict[str, Any], change: str) -> None:
    """Policy presence cannot admit a different path, category or validation code."""

    async def run() -> None:
        owner, grant, assignment = await setup(fixture)
        task = fixture["task"]
        if change == "source":
            task = replace(
                task,
                source="src/devtools/other.py",
                baseline_hashes=(
                    ("src/devtools/other.py", "a" * 64),
                    *task.baseline_hashes[1:],
                ),
                context=(
                    ("src/devtools/other.py", "other", "file", "file"),
                    *task.context[1:],
                ),
            )
        elif change == "tests":
            p = policy(fixture)
            p["tests"] = ["tests/other.py"]
            with pytest.raises(PermissionError):
                owner.eligible(p, assignment, task)
            return
        elif change == "oracle":
            task = replace(task, oracle="raise SystemExit(0)")
        elif change == "category":
            assignment["backlog"]["proposal"]["payload"]["kind"] = "investigation"
        else:
            p = policy(fixture)
            p["per_task"]["calls"] = 1
            with pytest.raises(PermissionError):
                owner.eligible(p, assignment, task)
            return
        with pytest.raises(PermissionError):
            owner.check(grant["sha256"], assignment, task)

    asyncio.run(run())


def test_missing_supervision_refusal_and_no_reservation(
    fixture: dict[str, Any],
) -> None:
    """Neither preparation nor a standing grant substitutes for supervisory review."""

    async def run() -> None:
        owner, grant, _ = await setup(fixture)
        with pytest.raises((FilesystemError, OSError)):
            await owner.authorize(fixture["item"], grant["sha256"], "a" * 64)
        assert not list((owner.folder(grant["sha256"]) / "reservations").iterdir())
        decision = await owner.review(
            fixture["item"],
            grant["sha256"],
            reference="fixture://reject",
            rationale="Not suitable",
            disposition="REJECT",
        )
        with pytest.raises(PermissionError, match="Existing supervisory decision"):
            await review(owner, fixture, grant)
        with pytest.raises(PermissionError):
            await owner.authorize(fixture["item"], grant["sha256"], decision["sha256"])

    asyncio.run(run())


def test_output_overrun_blocks_grant_and_preserves_response(
    fixture: dict[str, Any],
) -> None:
    """Observed provider overrun cannot silently admit further delegated calls."""

    async def run() -> None:
        owner, grant, _ = await setup(fixture)

        class Overrun(helpers.Scripted):
            async def send(self, request: ModelRequest) -> ModelResponse:
                response = await super().send(request)
                assert response.usage is not None
                return replace(
                    response, usage=replace(response.usage, output_tokens=4097)
                )

        model = Overrun([(helpers.OLD, helpers.GOOD)])
        guarded = owner.guard({"delegation": grant["sha256"]}, fixture["task"], model)
        request = ModelRequest(
            Prompt("fixture", role="user"),
            ModelSettings(4096, thinking_enabled=False),
            tools=(_structured_edit_definition(),),
        )
        response = await guarded.send(request)
        assert response.usage is not None
        assert response.usage.output_tokens == 4097
        assert response.tool_calls
        with pytest.raises(PermissionError):
            await guarded.send(request)
        assert len(model.requests) == 1
        assert (owner.folder(grant["sha256"]) / "blocked.json").exists()

    asyncio.run(run())


@pytest.mark.parametrize("state", ["expired", "revoked", "other-host"])
def test_inactive_grant_refused(
    fixture: dict[str, Any], monkeypatch: pytest.MonkeyPatch, state: str
) -> None:
    """Current host, expiration and revocation apply again after reservation."""

    async def run() -> None:
        owner, grant, assignment = await setup(fixture)
        decision = await review(owner, fixture, grant)
        await owner.authorize(fixture["item"], grant["sha256"], decision["sha256"])
        if state == "revoked":
            await owner.revoke(
                grant["sha256"],
                principal=getpass.getuser(),
                reference="fixture://revoke",
                authorize=lambda _: True,
            )
        elif state == "expired":
            future = Timestamp.now() + Duration.minutes(10)
            monkeypatch.setattr(Timestamp, "now", classmethod(lambda _cls: future))
        else:
            monkeypatch.setattr(getpass, "getuser", lambda: "unrelated-host")
        with pytest.raises(PermissionError):
            owner.check(grant["sha256"], assignment, fixture["task"])
        with pytest.raises(PermissionError):
            await fixture["cycle"].execute(
                fixture["item"],
                interaction_factory=helpers.factory(helpers.Scripted([])),
            )

    asyncio.run(run())


def test_competing_admission_and_writer_lease(fixture: dict[str, Any]) -> None:
    """Two distinct tasks cannot both reserve the one available task allowance."""

    async def run() -> None:
        owner, grant, _ = await setup(fixture)
        first = await review(owner, fixture, grant)
        payload = helpers.discovery()
        payload["title"] = "Second synthetic task"
        intake = fixture["intake"]
        proposal = intake.capture(payload)
        intake.review(
            proposal,
            decision="APPROVED",
            reviewer="fixture-host",
            reference="fixture://review-two",
            rationale="Synthetic",
            duplicate_disposition="Separate fixture",
            domain="resources",
            authorize=lambda _: True,
        )
        second = intake.promote(proposal, authorize=lambda _: True)
        await git(fixture["root"], "add", "docs/backlog")
        await git(fixture["root"], "commit", "-m", "Second approved fixture item")
        second_base = await git(fixture["root"], "rev-parse", "HEAD")
        await git(fixture["root"], "branch", "feat/second", second_base)
        await fixture["cycle"].prepare(
            second,
            target=fixture["target"],
            branch="feat/second",
            task=replace(fixture["task"], baseline_revision=second_base),
        )
        review_two = await owner.review(
            second,
            grant["sha256"],
            reference="fixture://two",
            rationale="Synthetic",
            disposition="APPROVE_ROUTINE",
        )
        with intake._writer(), pytest.raises(FileExistsError):
            await owner.authorize(fixture["item"], grant["sha256"], first["sha256"])
        results = await asyncio.gather(
            owner.authorize(fixture["item"], grant["sha256"], first["sha256"]),
            owner.authorize(second, grant["sha256"], review_two["sha256"]),
            return_exceptions=True,
        )
        assert sum(isinstance(r, dict) for r in results) == 1
        assert sum(isinstance(r, PermissionError) for r in results) == 1
        records = list((owner.folder(grant["sha256"]) / "reservations").iterdir())
        assert len(records) == 1
        assert json.loads(records[0].read_text())["allowance"]["calls"] == 3

    asyncio.run(run())


def test_untrusted_policy_cannot_issue_and_paths_are_confined(
    fixture: dict[str, Any],
) -> None:
    """Supplying a policy/model message grants nothing without trusted consent."""

    async def run() -> None:
        owner = Delegations(fixture["cycle"])
        with pytest.raises(PermissionError, match="consent"):
            await owner.issue(
                policy(fixture),
                principal=getpass.getuser(),
                reference="untrusted proposal",
                expires_at=Timestamp.now() + Duration.minutes(1),
            )
        for identity in ("../escape", "A" * 64, "x"):
            with pytest.raises(ValueError, match="identity"):
                owner.folder(identity)
        p = policy(fixture)
        p["sources"] = ["src/devtools/governance/usage.py"]
        with pytest.raises(PermissionError):
            validate_policy(p)
        p = policy(fixture)
        p["total"]["tasks"] = True
        with pytest.raises(ValueError, match="allowance"):
            validate_policy(p)
        p = policy(fixture)
        p["authorize"] = True
        with pytest.raises(ValueError, match="fields"):
            validate_policy(p)

    asyncio.run(run())


def test_profile_refusal_retains_claim_no_invocation(fixture: dict[str, Any]) -> None:
    """A changed provider cannot consume the reserved grant or trigger a retry."""

    async def run() -> None:
        owner, grant, _ = await setup(fixture)
        decision = await review(owner, fixture, grant)
        await owner.authorize(fixture["item"], grant["sha256"], decision["sha256"])
        model = helpers.Scripted([])
        result = await fixture["cycle"].execute(
            fixture["item"], interaction_factory=helpers.factory(model)
        )
        assert result["disposition"] == "ESCALATION_REQUIRED"
        assert "Model/environment" in result["error"]
        assert not model.requests
        with pytest.raises(PermissionError):
            await fixture["cycle"].execute(
                fixture["item"], interaction_factory=helpers.factory(model)
            )

    asyncio.run(run())


@pytest.mark.parametrize(
    ("answer", "expected"), [("y", True), ("", False), ("n", False)]
)
def test_real_terminal_defaults_no(
    monkeypatch: pytest.MonkeyPatch, answer: str, *, expected: bool
) -> None:
    """New standing prompt is genuine; existing per-task prompt remains separate."""
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _: answer)
    request = {"grant": {"principal": getpass.getuser()}}
    assert cli.confirm_delegation(request) is expected
    assert cli.confirm_work(request) is expected


def test_noninteractive_standing_issue_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    """No command-line policy acts as an implicit --yes."""
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
    with pytest.raises(PermissionError, match="interactive"):
        cli.confirm_delegation({"grant": {"principal": getpass.getuser()}})


@pytest.mark.parametrize("dimension", ["calls", "output_tokens", "seconds"])
def test_each_resource_allowance_is_enforced(
    fixture: dict[str, Any], dimension: str
) -> None:
    """Refuse admission if any cumulative resource is insufficient."""

    async def run() -> None:
        await helpers.prepare(fixture)
        owner = Delegations(fixture["cycle"])
        p = policy(fixture)
        p["total"][dimension] -= 1
        grant = await owner.issue(
            p,
            principal=getpass.getuser(),
            reference="fixture://limited",
            expires_at=Timestamp.now() + Duration.minutes(5),
            authorize=lambda _: True,
        )
        decision = await review(owner, fixture, grant)
        with pytest.raises(PermissionError, match="exhausted"):
            await owner.authorize(fixture["item"], grant["sha256"], decision["sha256"])
        assert not (
            fixture["cycle"]._folder(fixture["item"]) / "authorization.json"
        ).exists()

    asyncio.run(run())


def test_partial_authorization_does_not_refund_allowance(
    fixture: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A crash between reservation and authority leaves conservative accounting."""

    async def run() -> None:
        owner, grant, _ = await setup(fixture)
        decision = await review(owner, fixture, grant)
        save = fixture["cycle"]._save

        def interrupted(path: Path, value: dict[str, Any]) -> dict[str, Any]:
            if path.name == "authorization.json":
                message = "fixture interruption after reservation"
                raise OSError(message)
            saved: dict[str, Any] = save(path, value)
            return saved

        monkeypatch.setattr(fixture["cycle"], "_save", interrupted)
        with pytest.raises(OSError, match="interruption"):
            await owner.authorize(fixture["item"], grant["sha256"], decision["sha256"])
        monkeypatch.setattr(fixture["cycle"], "_save", save)
        with pytest.raises(PermissionError, match="exhausted"):
            await owner.authorize(fixture["item"], grant["sha256"], decision["sha256"])

    asyncio.run(run())


def test_per_call_guard_revocation_limits_and_profile(fixture: dict[str, Any]) -> None:
    """Recheck authority/settings on each call and reject alternate providers."""

    async def run() -> None:
        owner, grant, _ = await setup(fixture)
        for field in ("model", "endpoint", "profile", "service"):
            changed = provenance()
            changed[field] = {} if field in {"profile", "service"} else "unapproved"
            with pytest.raises(PermissionError, match="Model/environment"):
                owner.model({"delegation": grant["sha256"]}, changed)
        model = helpers.Scripted([(helpers.OLD, helpers.GOOD)] * 3)
        guarded = owner.guard({"delegation": grant["sha256"]}, fixture["task"], model)
        invalid = ModelRequest(
            Prompt("fixture", role="user"), ModelSettings(4097, thinking_enabled=False)
        )
        with pytest.raises(PermissionError, match="limits"):
            await guarded.send(invalid)
        assert not model.requests
        request = ModelRequest(
            Prompt("fixture", role="user"),
            ModelSettings(4096, thinking_enabled=False),
            tools=(_structured_edit_definition(),),
        )
        await guarded.send(request)
        await guarded.send(request)
        await guarded.send(request)
        with pytest.raises(PermissionError, match="limits"):
            await guarded.send(request)
        await owner.revoke(
            grant["sha256"],
            principal=getpass.getuser(),
            reference="fixture://stop-next-turn",
            authorize=lambda _: True,
        )
        with pytest.raises(PermissionError, match="revoked"):
            await guarded.send(request)
        assert len(model.requests) == 3

    asyncio.run(run())

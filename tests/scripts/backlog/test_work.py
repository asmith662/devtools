# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004, SLF001 -- synthetic host/Git integration
"""Real backlog-to-worker path in temporary Git worktrees, never live inference."""

from __future__ import annotations

import asyncio
import json
import shutil
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import pytest

from devtools.core.time import Duration, Timestamp
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
)
from devtools.models.interaction.usage import ModelUsage
from experiments.qwen.development_task import _command, _hash
from experiments.qwen.tasks import MARKDOWN
from scripts.backlog import __main__ as cli
from scripts.backlog.coordinator import designate, git, locate
from scripts.backlog.intake import Intake
from scripts.backlog.work import WorkCycle

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from devtools.models.interaction import ModelInteraction

ROOT = Path(__file__).resolve().parents[3]
OLD = "if fence[0] == active_fence[0] and len(fence) >= len(active_fence):"
GOOD = (
    "if (fence[0] == active_fence[0] and len(fence) >= len(active_fence) "
    "and not line[fence_match.end():].strip()):"
)
WRONG = OLD.replace("len(fence) >=", "len(fence) >")


class Scripted:
    """Deliver scripted native proposals, never provider calls or task competence."""

    source = InteractionSource("scripted-work-cycle")

    def __init__(self, edits: list[tuple[str, str]]) -> None:
        """Freeze an explicit ordered response inventory."""
        self.edits = edits
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Exercise production proposal/application/validation with fixture data."""
        self.requests.append(request)
        old, new = self.edits[len(self.requests) - 1]
        return ModelResponse(
            "scripted proposal",
            self.source,
            usage=ModelUsage(input_tokens=100, output_tokens=20),
            termination=ModelTermination.TOOL_CALL,
            tool_calls=(
                ModelToolCall(
                    "propose_edit",
                    json.dumps(
                        {
                            "path": MARKDOWN.source,
                            "old_text": old,
                            "new_text": new,
                        }
                    ),
                    provider_call_id="fixture-call",
                ),
            ),
        )


def discovery() -> dict[str, Any]:
    """Define only synthetic discovery data; no authority fields are permitted."""
    return {
        "kind": "bug",
        "title": "Fixture Markdown correction",
        "summary": "Synthetic authorized backlog-to-worker integration.",
        "discovery": {"kind": "tool", "reference": "fixture://baseline"},
        "parent": None,
        "resources": [MARKDOWN.source],
        "evidence": ["fixture://oracle"],
        "benefit": "Exercise host wiring, not Qwen competence.",
        "uncertainty": "Synthetic result only.",
        "dependencies": [],
    }


@pytest.fixture
def fixture(tmp_path: Path) -> dict[str, Any]:
    """Build one harmless temporary repository and an ordinary linked worktree."""

    async def construct() -> dict[str, Any]:
        coordinator = tmp_path / "coordinator"
        coordinator.mkdir()
        await git(coordinator, "init", "-b", "coordinator")
        await git(coordinator, "config", "user.name", "Synthetic Fixture")
        await git(coordinator, "config", "user.email", "fixture@example.invalid")
        shutil.copytree(
            ROOT / "src",
            coordinator / "src",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        for relative in (MARKDOWN.source, *MARKDOWN.tests):
            raw = await _command(
                ROOT, "git", "show", MARKDOWN.baseline_revision + ":" + relative
            )
            assert not raw["failed"]
            path = coordinator / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(raw["stdout"], encoding="utf-8", newline="")
        (coordinator / ".gitignore").write_text(
            ".local/\n__pycache__/\n.pytest_cache/\n"
        )
        backlog = coordinator / "docs/backlog"
        (backlog / "items").mkdir(parents=True)
        (backlog / "epics").mkdir()
        (backlog / "items/B-0009-existing.md").write_text(
            "# B-0009 — Existing\n", encoding="utf-8"
        )
        (backlog / "overview.md").write_text(
            "| ID | Title | Status | Domain |\n| --- | --- | --- | --- |\n"
            "| [B-0009](items/B-0009-existing.md) | Existing | BACKLOG | tools |\n"
        )
        await designate(coordinator, authorize=lambda _: True)
        intake = Intake(coordinator, coordinator=coordinator)
        proposal = intake.capture(discovery())
        intake.review(
            proposal,
            decision="APPROVED",
            reviewer="synthetic-host",
            reference="fixture://backlog-approval",
            rationale="Fixture inclusion only",
            duplicate_disposition="Distinct fixture",
            domain="resources",
            authorize=lambda _: True,
        )
        item = intake.promote(proposal, authorize=lambda _: True)
        await git(coordinator, "add", ".")
        await git(
            coordinator,
            "commit",
            "-m",
            "Synthetic approved backlog and source baseline",
        )
        base = await git(coordinator, "rev-parse", "HEAD")
        target = tmp_path / "feature"
        await git(
            coordinator, "worktree", "add", "-b", "feat/fixture", str(target), base
        )
        task = replace(
            MARKDOWN,
            baseline_revision=base,
            baseline_hashes=tuple(
                (p, _hash(target / p)) for p in (MARKDOWN.source, *MARKDOWN.tests)
            ),
        )
        return {
            "root": coordinator,
            "target": target,
            "item": item,
            "proposal": proposal,
            "task": task,
            "cycle": WorkCycle(coordinator),
            "intake": intake,
        }

    return asyncio.run(construct())


async def prepare(fixture: dict[str, Any]) -> dict[str, Any]:
    """Freeze fixture scope without granting execution authority."""
    cycle = cast("WorkCycle", fixture["cycle"])
    return await cycle.prepare(
        fixture["item"],
        target=fixture["target"],
        branch="feat/fixture",
        task=fixture["task"],
    )


async def grant(fixture: dict[str, Any]) -> dict[str, Any]:
    """Use an explicitly synthetic host grant for this fixture only."""
    cycle = cast("WorkCycle", fixture["cycle"])
    return await cycle.authorize(
        fixture["item"],
        principal="synthetic-host",
        reference="fixture://separate-implementation-grant",
        expires_at=Timestamp.now() + Duration.minutes(5),
        authorize=lambda _: True,
    )


def factory(
    model: Scripted,
) -> Callable[[], Awaitable[tuple[ModelInteraction, dict[str, Any]]]]:
    """Construct a scripted interaction after admission, never before it."""

    async def create() -> tuple[ModelInteraction, dict[str, Any]]:
        return model, {"model": "scripted; no inference"}

    return create


def test_real_scripted_cycle_repair_discovery_and_review_candidate(
    fixture: dict[str, Any],
    record_testsuite_property: Callable[[str, object], None],
) -> None:
    """Approved work plus a separate grant uses real search/edit/tests/repair."""

    async def run() -> dict[str, Any]:
        assignment = await prepare(fixture)
        assert not assignment["execution_authorized"]
        before = (
            fixture["cycle"]._folder(fixture["item"]) / "assignment.json"
        ).read_bytes()
        opportunity = discovery()
        opportunity["title"] = "A secondary fixture opportunity"
        proposal = await fixture["cycle"].discover(fixture["item"], opportunity)
        queued = fixture["intake"].get(proposal)
        assert queued["state"] == "PENDING_REVIEW"
        assert queued["proposal"]["payload"]["parent"] == fixture["item"]
        assert (
            fixture["cycle"]._folder(fixture["item"]) / "assignment.json"
        ).read_bytes() == before
        authorization = await grant(fixture)
        model = Scripted([(OLD, WRONG), (WRONG, GOOD)])
        result = await fixture["cycle"].execute(
            fixture["item"],
            interaction_factory=factory(model),
            authorize=lambda _: True,
        )
        assert len(model.requests) == 2
        assert "HOST FEEDBACK" in model.requests[1].prompt.content
        assert result["authorization_sha256"] == authorization["sha256"]
        assert result["base_head"] == fixture["task"].baseline_revision
        assert result["branch"] == "feat/fixture"
        assert result["disposition"] == "REVIEW_CANDIDATE", result
        assert result["candidate_changed_files"] == [MARKDOWN.source]
        assert result["target_unchanged"]
        assert not result["integration_authorized"]
        assert not result["canonical_item_closed"]
        assert result["usage"]["input_tokens"] == 200
        assert result["repair_cycles"] == 1
        assert result["validation"]["oracle"]["exit_code"] == 0
        assert result["validation"]["tests"]["exit_code"] == 0
        assert Path(result["diff"]).is_file()  # noqa: ASYNC240 -- local artifact
        assert fixture["cycle"].status(fixture["item"])["sha256"] == result["sha256"]
        return cast("dict[str, Any]", result)

    result = asyncio.run(run())
    assert result["model_calls"] == 2
    record_testsuite_property("scripted_work_cycle_result", json.dumps(result))
    assert asyncio.run(git(fixture["target"], "status", "--porcelain")) == ""


def test_failed_work_remains_bounded_escalation(fixture: dict[str, Any]) -> None:
    """Keep exhausted worker attempts failed and bounded."""

    async def run() -> None:
        fixture["task"] = replace(fixture["task"], maximum_calls=1)
        await prepare(fixture)
        await grant(fixture)
        model = Scripted([(OLD, WRONG)])
        result = await fixture["cycle"].execute(
            fixture["item"],
            interaction_factory=factory(model),
            authorize=lambda _: True,
        )
        assert result["disposition"] == "ESCALATION_REQUIRED"
        assert result["worker_disposition"] == "REPAIR_BUDGET_EXHAUSTED"
        assert result["model_calls"] == 1
        assert len(model.requests) == 1
        assert not result["integration_authorized"]

    asyncio.run(run())


@pytest.mark.parametrize("kind", ["pending", "advisory"])
def test_unapproved_work_refused(fixture: dict[str, Any], kind: str) -> None:
    """Neither proposal identity nor an existing unapproved B-number is executable."""
    identity = fixture["intake"].capture(discovery())
    if kind == "advisory":
        fixture["intake"].review(
            identity,
            decision="ADVISORY",
            reviewer="Codex advice",
            reference="fixture://advice",
            rationale="No grant",
            duplicate_disposition="related",
        )
        identity = "B-0009"
    with pytest.raises(PermissionError, match=r"approved|B-number"):
        asyncio.run(
            fixture["cycle"].prepare(
                identity,
                target=fixture["target"],
                branch="feat/fixture",
                task=fixture["task"],
            )
        )


@pytest.mark.parametrize(
    "kind",
    [
        "missing",
        "denied",
        "expired",
        "changed-backlog",
        "changed-target",
        "wrong-branch",
    ],
)
def test_fresh_admission_refuses_without_factory_or_model(
    fixture: dict[str, Any], kind: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Fresh state, exact branch/source and current authority precede service access."""

    async def run() -> None:
        await prepare(fixture)
        if kind != "missing":
            await grant(fixture)
        if kind == "expired":
            future = Timestamp.now() + Duration.minutes(10)
            monkeypatch.setattr(Timestamp, "now", lambda: future)
        elif kind == "changed-backlog":
            binding = fixture["intake"].approved_item(fixture["item"])
            p = Path(binding["path"])
            p.write_text(p.read_text() + "\nChanged objective\n")  # noqa: ASYNC240 -- fixture
        elif kind == "changed-target":
            (fixture["target"] / MARKDOWN.source).write_text("changed")
        elif kind == "wrong-branch":
            await git(fixture["target"], "branch", "-m", "feat/other")

        async def forbidden() -> tuple[ModelInteraction, dict[str, Any]]:
            pytest.fail("Refused work must not reach the model factory")

        with pytest.raises(PermissionError):
            await fixture["cycle"].execute(
                fixture["item"],
                interaction_factory=forbidden,
                authorize=(lambda _: False) if kind == "denied" else (lambda _: True),
            )
        assert not (
            fixture["cycle"]._folder(fixture["item"]) / "dispatch.json"
        ).exists()

    asyncio.run(run())


def test_separate_authorization_required_even_after_approval(
    fixture: dict[str, Any],
) -> None:
    """An approved prepared item creates no execution permission by itself."""

    async def run() -> None:
        await prepare(fixture)
        with pytest.raises(PermissionError, match="Separate host"):
            await fixture["cycle"].authorize(
                fixture["item"],
                principal="model claims human",
                reference="untrusted",
                expires_at=Timestamp.now() + Duration.minutes(5),
            )

    asyncio.run(run())


def test_duplicate_preparation_and_ambiguous_dispatch_never_relaunch(
    fixture: dict[str, Any],
) -> None:
    """A crash after the durable claim requires reconciliation, not redispatch."""

    async def run() -> None:
        await prepare(fixture)
        with pytest.raises(FileExistsError):
            await prepare(fixture)
        await grant(fixture)

        async def interrupted() -> tuple[ModelInteraction, dict[str, Any]]:
            raise asyncio.CancelledError

        with pytest.raises(asyncio.CancelledError):
            await fixture["cycle"].execute(
                fixture["item"],
                interaction_factory=interrupted,
                authorize=lambda _: True,
            )
        assert (
            fixture["cycle"].status(fixture["item"])["disposition"]
            == "RECONCILIATION_REQUIRED"
        )
        with pytest.raises(PermissionError, match="Prior dispatch"):
            await fixture["cycle"].execute(
                fixture["item"],
                interaction_factory=interrupted,
                authorize=lambda _: True,
            )

    asyncio.run(run())


def test_only_designated_coordinator_can_mutate(fixture: dict[str, Any]) -> None:
    """A linked execution worktree cannot publish independent canonical state."""
    assert asyncio.run(locate(fixture["target"])) == fixture["root"]
    with pytest.raises(PermissionError, match="designated coordinator"):
        Intake(fixture["target"], coordinator=fixture["root"]).capture(discovery())
    with pytest.raises(PermissionError, match="designated coordinator"):
        Intake(fixture["root"]).capture(discovery())
    with pytest.raises(PermissionError, match="different coordinator"):
        asyncio.run(designate(fixture["target"], authorize=lambda _: True))


def test_terminal_work_authority_defaults_no(monkeypatch: pytest.MonkeyPatch) -> None:
    """Implementation consent is separate from the backlog-only prompt."""
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    monkeypatch.setattr("getpass.getuser", lambda: "fixture-host")
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert not cli.confirm_work({"grant": {"principal": "fixture-host"}})
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    with pytest.raises(PermissionError, match="interactive terminal"):
        cli.confirm_work({"grant": {"principal": "fixture-host"}})


def test_expiry_during_terminal_consent_is_rechecked(
    fixture: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Waiting at the host prompt cannot turn stale authority into admission."""

    async def run() -> None:
        await prepare(fixture)
        await grant(fixture)
        future = Timestamp.now() + Duration.minutes(10)

        def delayed_consent(_request: dict[str, Any]) -> bool:
            monkeypatch.setattr(Timestamp, "now", lambda: future)
            return True

        async def forbidden() -> tuple[ModelInteraction, dict[str, Any]]:
            pytest.fail("Expired consent reached factory")

        with pytest.raises(PermissionError, match="expired before admission"):
            await fixture["cycle"].execute(
                fixture["item"],
                interaction_factory=forbidden,
                authorize=delayed_consent,
            )

    asyncio.run(run())


def test_factory_failure_is_reviewable_escalation_not_retry(
    fixture: dict[str, Any],
) -> None:
    """Environment/provider setup failure leaves a durable conservative result."""

    async def run() -> None:
        await prepare(fixture)
        await grant(fixture)

        async def unavailable() -> tuple[ModelInteraction, dict[str, Any]]:
            message = "fixture provider unavailable"
            raise RuntimeError(message)

        result = await fixture["cycle"].execute(
            fixture["item"], interaction_factory=unavailable, authorize=lambda _: True
        )
        assert result["disposition"] == "ESCALATION_REQUIRED"
        assert result["model_calls"] is None
        assert "unavailable" in result["error"]
        with pytest.raises(PermissionError, match="Prior dispatch"):
            await fixture["cycle"].execute(
                fixture["item"],
                interaction_factory=unavailable,
                authorize=lambda _: True,
            )

    asyncio.run(run())


def test_implementation_scope_must_match_reviewed_resources(
    fixture: dict[str, Any],
) -> None:
    """An unrelated implementation file cannot inherit an approved work identity."""
    payload = discovery()
    payload["resources"] = ["src/unrelated.py"]
    intake = fixture["intake"]
    proposal = intake.capture(payload)
    intake.review(
        proposal,
        decision="APPROVED",
        reviewer="fixture-host",
        reference="fixture://review",
        rationale="Unrelated scope",
        duplicate_disposition="Explicitly distinct",
        domain="resources",
        authorize=lambda _: True,
    )
    item = intake.promote(proposal, authorize=lambda _: True)
    with pytest.raises(PermissionError, match="outside the reviewed"):
        asyncio.run(
            fixture["cycle"].prepare(
                item,
                target=fixture["target"],
                branch="feat/fixture",
                task=fixture["task"],
            )
        )


def test_missing_designation_cannot_fall_back_to_local_writes(
    fixture: dict[str, Any],
) -> None:
    """Shared coordinator configuration is required rather than silently guessed."""
    asyncio.run(
        git(
            fixture["root"],
            "config",
            "--local",
            "--unset",
            "devtools.backlogCoordinator",
        )
    )
    with pytest.raises(ValueError, match="Git inspection failed"):
        asyncio.run(prepare(fixture))

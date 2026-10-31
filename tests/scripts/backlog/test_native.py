# Copyright (c) 2026
# ruff: noqa: PLR2004, COM812, SLF001, E501, C901, PLR0912, PLR0915 -- finite authored lifecycle controls
"""Actual neutral source/check/repair/custody/review/plan without live models."""

from __future__ import annotations

import asyncio
import copy
import json
from typing import TYPE_CHECKING, Any

import pytest

from devtools.core.time import Duration, Timestamp
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelToolCall,
)
from scripts.backlog.coordinator import designate, git
from scripts.backlog.intake import _digest
from scripts.backlog.work import WorkCycle

if TYPE_CHECKING:
    from pathlib import Path

SOURCE = "src/devtools/sample.py"
BASE = "def value():\n    return 1\n"
PUBLIC = "tests/test_sample.py"


def task(source: str = "neutral-script-a") -> dict[str, Any]:
    """Define a supervisor-owned finite packet with private acceptance provenance."""
    return {
        "objective": "Repair value() to return 3. Inspect current source before editing.",
        "source": SOURCE,
        "read_paths": [],
        "tests": [PUBLIC],
        "oracle": "assert module.value() == 3\n",
        "obligations": [
            {
                "name": "owner",
                "predicate": "Inspect the current implementation",
                "path": SOURCE,
                "criterion": "current-whole-resource-v1",
            }
        ],
        "preflight": {
            "reference": "fixture://independent-expectations",
            "controls_reference": "fixture://baseline-failure-and-positive-controls",
            "comparisons": [
                {
                    "name": c,
                    "obligation": "owner",
                    "category": c,
                    "expected": 3,
                    "independently_derived": 3,
                    "derivation": "Independently authored constant-value contract",
                }
                for c in ("normal", "boundary", "empty")
            ],
        },
        "worker": {
            "actor": "neutral-coder",
            "source": source,
            "profile": "scripted-v1",
        },
        "settings": {"maximum_output_tokens": 512, "thinking_enabled": False},
        "budgets": {
            "model_calls": 4,
            "proposals": 3,
            "acquisitions": 6,
            "call_seconds": 10,
            "wall_seconds": 60,
            "prompt_bytes": 32768,
            "source_bytes": 32768,
            "capture_bytes": 524288,
        },
        "capture": "bounded-full-v1",
    }


@pytest.fixture
def repository(tmp_path: Path) -> tuple[WorkCycle, str]:
    """Create a small repository with reviewed backlog and isolated local origin."""

    async def build() -> tuple[WorkCycle, str]:
        root = tmp_path / "repository"
        root.mkdir()
        await git(root, "init", "-b", "admin")
        await git(root, "config", "user.name", "Native Fixture")
        await git(root, "config", "user.email", "fixture@invalid")
        for name, text in {
            SOURCE: BASE,
            "src/devtools/__init__.py": "",
            PUBLIC: "import runpy\nfrom pathlib import Path\ndef test_value():\n    assert runpy.run_path(str(Path(__file__).parents[1] / 'src/devtools/sample.py'))['value']() == 3\n",
            ".gitignore": ".local/\n__pycache__/\n.pytest_cache/\n",
            "uv.lock": "# bounded lock input\n" * 14000,
            "docs/backlog/overview.md": "| ID | Title | Status | Domain |\n| --- | --- | --- | --- |\n| [B-0009](items/B-0009-existing.md) | Existing | BACKLOG | agents |\n",
        }.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        await designate(root, authorize=lambda _: True)
        (root / "docs/backlog/items").mkdir()
        (root / "docs/backlog/items/B-0009-existing.md").write_text(
            "# B-0009 Existing\n- status: BACKLOG\n", encoding="utf-8"
        )
        cycle = WorkCycle(root)
        identity = cycle.intake.capture(
            {
                "kind": "bug",
                "title": "Native value repair",
                "summary": "Authored one-file repair",
                "discovery": {"kind": "tool", "reference": "fixture://source"},
                "parent": None,
                "resources": [SOURCE],
                "evidence": ["fixture://contract"],
                "benefit": "Exercise neutral handoff",
                "uncertainty": "Scripted mechanics only",
                "dependencies": [],
            }
        )
        cycle.intake.review(
            identity,
            decision="APPROVED",
            reviewer="host-supervisor",
            reference="fixture://review",
            rationale="Bounded implementation obligation",
            duplicate_disposition="Distinct authored task",
            domain="agents",
            authorize=lambda _: True,
        )
        item = cycle.intake.promote(identity, authorize=lambda _: True)
        await git(root, "add", ".")
        await git(root, "commit", "-m", "Authored reviewed baseline")
        await git(root, "branch", "feat/native-work")
        await git(root, "branch", "release")
        origin = tmp_path / "origin.git"
        await git(root, "init", "--bare", str(origin))
        await git(root, "remote", "add", "origin", str(origin))
        await git(root, "push", "origin", "release")
        return cycle, item

    return asyncio.run(build())


def read_call() -> ModelToolCall:
    """Select the source through the native Tool, not a hidden test-side read."""
    return ModelToolCall(
        "read_source",
        json.dumps({"path": SOURCE, "start": 0}),
        "read-1",
    )


def edit(old: int, new: int, identity: str) -> ModelToolCall:
    """Create one grounded native replacement proposal."""
    return ModelToolCall(
        "replace_source",
        json.dumps(
            {"path": SOURCE, "old_text": f"return {old}", "new_text": f"return {new}"}
        ),
        identity,
    )


class Scripted:
    """Supply neutral responses; lifecycle effects remain in production owners."""

    def __init__(self, source: str, calls: list[ModelToolCall] | None = None) -> None:
        """Freeze independently authored response choices and retain actual requests."""
        self.source = InteractionSource(source)
        self.calls = (
            calls
            if calls is not None
            else [read_call(), edit(1, 2, "edit-2"), edit(2, 3, "repair-3")]
        )
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Exercise actual source read, failure feedback and independently selected repair."""
        index = len(self.requests)
        self.requests.append(request)
        if index >= len(self.calls):
            return ModelResponse("Cannot proceed within this schedule", self.source)
        return ModelResponse(
            "native scripted operation", self.source, tool_calls=(self.calls[index],)
        )


async def prepared(
    cycle: WorkCycle, item: str, packet: dict[str, Any]
) -> dict[str, Any]:
    """Prepare then issue a separate exact native execution decision."""
    assignment = await cycle.native.prepare(
        item, branch="feat/native-work", task=packet, supervisor="trusted-supervisor"
    )
    assert assignment["execution_authorized"] is False
    await cycle.native.authorize(
        item,
        reference="fixture://native-approval",
        expires=Timestamp.now() + Duration.minutes(5),
        authorize=lambda _: True,
    )
    return assignment


@pytest.mark.parametrize("source", ["neutral-script-a", "independent-script-b"])
def test_reviewed_native_task_to_authenticated_installable_plan(
    repository: tuple[WorkCycle, str], source: str
) -> None:
    """Run real failed/public checks, repair, withheld acceptance and governed handoff."""

    async def run() -> None:
        cycle, item = repository
        await prepared(cycle, item, task(source))
        model = Scripted(source)
        result = await cycle.native.execute(
            item, interaction=model, profile="scripted-v1", authorize=lambda _: True
        )
        assert result["disposition"] == "REVIEW_CANDIDATE", result
        facts = result["facts"]
        assert [g[0]["exit_code"] for g in facts["checks"]] == [1, 0]
        assert facts["acceptance"]["passed"]
        assert facts["restored"]
        assert facts["initial_context"]["unresolved"] == ["owner"]
        assert facts["readiness"][0]["ready"]
        assert facts["model_calls"] == 3
        assert facts["proposals"] == 2
        assert "assert 2 == 3" in facts["checks"][0][0]["stdout"]
        assert all("assert module.value()" not in str(r.prompt) for r in model.requests)
        assert (cycle.root / SOURCE).read_text() == BASE
        assert not (cycle.root / ".local/backlog/checkout-owner").exists()
        with pytest.raises(PermissionError, match="Independent"):
            await cycle.native.review(
                item,
                reviewer="neutral-coder",
                reference="fixture://self",
                rationale="self",
                accept=True,
                authorize=lambda _: True,
            )
        review = await cycle.native.review(
            item,
            reviewer="independent-reviewer",
            reference="fixture://independent-review",
            rationale="Inspected exact candidate and positive/negative check results",
            accept=True,
            authorize=lambda _: True,
        )
        review_path = cycle._folder(item) / ("review-" + review["sha256"] + ".json")
        original_review = review_path.read_bytes()
        review_path.write_text(json.dumps({**review, "reviewer": "tampered"}))
        with pytest.raises(ValueError, match="identity/schema"):
            cycle.integration.candidate(item, review["sha256"])
        review_path.write_bytes(original_review)
        candidate_path = cycle._folder(item) / "worker/final-source.py"
        original_candidate = candidate_path.read_bytes()
        candidate_path.write_text("def value():\n    return 999\n")
        with pytest.raises(PermissionError, match="bytes/diff"):
            cycle.integration.candidate(item, review["sha256"])
        candidate_path.write_bytes(original_candidate)
        plan = await cycle.integration.plan(
            item,
            review["sha256"],
            {
                "remote": "origin",
                "destination": "release",
                "feature": "feat/native-integration",
                "checkout": str(cycle.root),
                "additions": [],
                "parent_complete": False,
                "remaining": ["Broader autonomous lifecycle remains separate"],
                "rationale": "One independently reviewed repair",
                "validation_seconds": 60,
            },
        )
        assert plan["candidate_kind"] == "native-v1"
        assert plan["files"][0]["author"] == "neutral-coder"
        assert plan["candidate_result"] == result["sha256"]
        assert not (
            cycle.integration.folder(item, plan["sha256"]) / "install.json"
        ).exists()
        policy = {
            "sources": [SOURCE],
            "tests": [PUBLIC],
            "oracles": [plan["oracle_sha256"]],
            "remote": "origin",
            "destinations": ["release"],
            "checkout": str(cycle.root),
            "actions": ["install"],
            "protected": False,
            "corrections": False,
            "parent_close": False,
            "max_integrations": 1,
            "max_files": 1,
            "max_bytes": 32768,
            "validation_seconds": 60,
        }
        legacy = await cycle.integration.authority.issue(
            policy,
            reference="fixture://legacy-scope",
            expires=Timestamp.now() + Duration.minutes(5),
            authorize=lambda _: True,
        )
        with pytest.raises(PermissionError, match="candidate kind"):
            await cycle.integration.authority.admit(legacy["sha256"], plan, "install")
        grant = await cycle.integration.authority.issue(
            policy,
            native=True,
            reference="fixture://separate-native-install",
            expires=Timestamp.now() + Duration.minutes(5),
            authorize=lambda _: True,
        )
        installed = await cycle.integration.install(
            item, plan["sha256"], grant["sha256"]
        )
        assert installed["disposition"] == "INSTALLED"
        assert (cycle.root / SOURCE).read_text() == BASE
        assert await git(cycle.root, "branch", "--show-current") == "admin"
        assert cycle.intake.approved_item(item)["status"] == "BACKLOG"
        with pytest.raises(PermissionError, match="Prior native dispatch"):
            await cycle.native.execute(
                item, interaction=model, profile="scripted-v1", authorize=lambda _: True
            )

    asyncio.run(run())


@pytest.mark.parametrize(
    "fault",
    [
        "no-approval",
        "wrong-profile",
        "expired",
        "changed-source",
        "incomplete",
        "exhausted",
        "private-failure",
        "capture",
        "proposal-limit",
        "tool-limit",
        "prompt-limit",
        "configuration",
    ],
)
def test_native_refusal_and_bounded_failure(
    repository: tuple[WorkCycle, str], fault: str
) -> None:
    """Retain truthful blockers and never produce a plan from incomplete work."""

    async def run() -> None:
        cycle, item = repository
        packet = task()
        if fault == "incomplete":
            packet["obligations"].append(
                {
                    "name": "public-contract",
                    "predicate": "Read tests",
                    "path": PUBLIC,
                    "criterion": "current-whole-resource-v1",
                }
            )
            packet["preflight"]["comparisons"].extend(
                {
                    **copy.deepcopy(r),
                    "name": "public-" + r["name"],
                    "obligation": "public-contract",
                }
                for r in list(packet["preflight"]["comparisons"])
            )
        if fault == "exhausted":
            packet["budgets"]["model_calls"] = 1
        if fault == "proposal-limit":
            packet["budgets"]["proposals"] = 1
        if fault == "tool-limit":
            packet["budgets"]["acquisitions"] = 1
        if fault == "prompt-limit":
            packet["budgets"]["prompt_bytes"] = 1
        if fault == "private-failure":
            packet["oracle"] = "assert module.value() == 999\n"
        if fault == "capture":
            packet["budgets"]["capture_bytes"] = 1
        await prepared(cycle, item, packet)
        model = Scripted(
            "neutral-script-a",
            [read_call(), read_call()] if fault == "tool-limit" else None,
        )
        if fault == "expired":
            path = cycle._folder(item) / "authorization.json"
            value = json.loads(path.read_text())
            value.pop("sha256")
            value["expires_at"] = "2000-01-01T00:00:00+00:00"
            path.write_text(json.dumps({**value, "sha256": _digest(value)}))
        if fault == "changed-source":
            (cycle.root / SOURCE).write_text(BASE + "# external change\n")
        if fault == "configuration":
            (cycle.root / "conftest.py").write_text(
                "# newly introduced global fixture\n"
            )
        if fault in {
            "no-approval",
            "wrong-profile",
            "expired",
            "changed-source",
            "configuration",
        }:
            with pytest.raises(PermissionError):
                await cycle.native.execute(
                    item,
                    interaction=model,
                    profile="wrong" if fault == "wrong-profile" else "scripted-v1",
                    authorize=None if fault == "no-approval" else lambda _: True,
                )
            assert not model.requests
            assert not (cycle._folder(item) / "dispatch.json").exists()
        else:
            result = await cycle.native.execute(
                item, interaction=model, profile="scripted-v1", authorize=lambda _: True
            )
            assert result["disposition"] == "BLOCKED"
            facts = result["facts"]
            if fault == "incomplete":
                assert "public-contract" in facts["readiness"][-1]["unresolved"]
            if fault == "proposal-limit":
                assert facts["coding_disposition"] == "proposal_limit"
                assert facts["model_calls"] == 2
            if fault == "tool-limit":
                assert facts["acquisitions"] == 1
                assert len(facts["effects"]) == 1
            if fault == "prompt-limit":
                assert facts["model_calls"] == 0
            if fault == "capture":
                assert not model.requests
            if fault == "private-failure":
                assert facts["coding_accepted"]
                assert not facts["acceptance"]["passed"]
            with pytest.raises(PermissionError, match="mismatch"):
                await cycle.native.review(
                    item,
                    reviewer="independent",
                    reference="fixture://review",
                    rationale="No accepted candidate",
                    accept=True,
                    authorize=lambda _: True,
                )
            assert not (cycle.root / ".local/backlog/checkout-owner").exists()

    asyncio.run(run())


@pytest.mark.parametrize(
    "fault",
    ["timeout", "wrong-source", "capture-after-return", "unknown-source", "timed"],
)
def test_native_uncertain_entry_never_replays(
    repository: tuple[WorkCycle, str], monkeypatch: pytest.MonkeyPatch, fault: str
) -> None:
    """Keep dispatch facts and unknown source, refusing automatic replay or cleanup."""
    from scripts.backlog.native import execution  # noqa: PLC0415

    async def run() -> None:
        cycle, item = repository
        packet = task()
        if fault == "timed":
            packet["budgets"].update(call_seconds=1, wall_seconds=1)
        await prepared(cycle, item, packet)

        class Uncertain(Scripted):
            async def send(self, request: ModelRequest) -> ModelResponse:
                if fault == "timed":
                    self.requests.append(request)
                    await asyncio.sleep(2)
                if fault == "timeout":
                    self.requests.append(request)
                    msg = "provider entry uncertain"
                    raise TimeoutError(msg)
                response = await super().send(request)
                if fault == "wrong-source":
                    return ModelResponse(
                        response.content,
                        InteractionSource("foreign"),
                        tool_calls=response.tool_calls,
                    )
                return response

        model = Uncertain("neutral-script-a")
        if fault == "capture-after-return":
            original_capture = execution.Capture.add

            def fail_capture(self: Any, kind: str, value: Any) -> None:  # noqa: ANN401 -- explicit failure injection
                if kind == "model-returned":
                    msg = "response capture failed after model entry"
                    raise ValueError(msg)
                original_capture(self, kind, value)

            monkeypatch.setattr(execution.Capture, "add", fail_capture)
        if fault == "unknown-source":
            from devtools.agents.coding.repository import (  # noqa: PLC0415
                write_source_changes,
            )

            original_apply = write_source_changes

            def unknown(root: Any, changes: Any) -> None:  # noqa: ANN401 -- explicit external mutation
                original_apply(root, changes)
                (cycle.root / SOURCE).write_text("# unknown source preserved\n")
                msg = "application outcome uncertain"
                raise OSError(msg)

            monkeypatch.setattr(execution, "write_source_changes", unknown)
            with pytest.raises(PermissionError, match="Unreviewed source"):
                await cycle.native.execute(
                    item,
                    interaction=model,
                    profile="scripted-v1",
                    authorize=lambda _: True,
                )
            assert (cycle.root / ".local/backlog/checkout-owner").exists()
            assert (cycle.root / SOURCE).read_text() == "# unknown source preserved\n"
        else:
            result = await cycle.native.execute(
                item, interaction=model, profile="scripted-v1", authorize=lambda _: True
            )
            assert result["disposition"] == "BLOCKED"
            if fault == "timed":
                assert len(model.requests) <= 1
                assert result["facts"]["model_calls"] == 1
                assert result["facts"]["error"].startswith("TimeoutError")
                assert not result["facts"]["effects"]
            else:
                assert len(model.requests) == 1
            with pytest.raises(PermissionError, match="Prior native dispatch"):
                await cycle.native.execute(
                    item,
                    interaction=model,
                    profile="scripted-v1",
                    authorize=lambda _: True,
                )
        assert cycle.native.record(item, "result")["disposition"] == "BLOCKED"

    asyncio.run(run())


def test_checkout_release_failure_cannot_publish_a_reviewable_result(
    repository: tuple[WorkCycle, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Keep worker success separate from failure to release repository custody."""
    from scripts.backlog.checkout import Checkout  # noqa: PLC0415

    async def run() -> None:
        cycle, item = repository
        await prepared(cycle, item, task())
        original = Checkout._finish

        async def fail_release(owner: Checkout) -> None:
            (cycle.root / "unexpected.txt").write_text("unknown external file\n")
            await original(owner)

        monkeypatch.setattr(Checkout, "_finish", fail_release)
        with pytest.raises(PermissionError, match="Untracked evidence changed"):
            await cycle.native.execute(
                item,
                interaction=Scripted("neutral-script-a"),
                profile="scripted-v1",
                authorize=lambda _: True,
            )
        result = cycle.native.record(item, "result")
        assert result["facts"]["coding_accepted"]
        assert result["disposition"] == "BLOCKED"
        assert result["checkout_released"] is False
        assert (cycle.root / ".local/backlog/checkout-owner").exists()
        assert (cycle.root / "unexpected.txt").read_text() == "unknown external file\n"
        with pytest.raises(PermissionError, match="Checkout owned"):
            await cycle.native.review(
                item,
                reviewer="independent",
                reference="fixture://review",
                rationale="Custody not released",
                accept=True,
                authorize=lambda _: True,
            )

    asyncio.run(run())


def test_native_operator_preview_and_default_no_authorization(
    repository: tuple[WorkCycle, str], capsys: pytest.CaptureFixture[str]
) -> None:
    """Expose a maintained operator preview without manufacturing host approval."""
    from scripts.backlog import __main__ as cli  # noqa: PLC0415

    cycle, item = repository
    asyncio.run(
        cycle.native.prepare(
            item,
            branch="feat/native-work",
            task=task(),
            supervisor="operator-supervisor",
        )
    )
    assert cli.main(["--root", str(cycle.root), "native-preview", item]) == 0
    preview = json.loads(capsys.readouterr().out)
    assert preview["assignment"]["execution_authorized"] is False
    assert preview["assignment"]["tool_definitions"]
    assert (
        cli.main(
            [
                "--root",
                str(cycle.root),
                "native-authorize",
                item,
                "--reference",
                "fixture://unapproved",
                "--expires",
                str(Timestamp.now() + Duration.minutes(5)),
            ]
        )
        == 1
    )
    assert not (cycle._folder(item) / "authorization.json").exists()

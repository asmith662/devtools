# Copyright (c) 2026
# ruff: noqa: PLR2004, COM812, SLF001, E501, C901, PLR0912, PLR0915, PT018, EM101, TRY003 -- finite authored lifecycle controls
"""Actual neutral source/check/repair/custody/review/plan without live models."""

from __future__ import annotations

import asyncio
import copy
import json
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

import pytest

from devtools.core.time import Duration, Timestamp
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
    ModelUsage,
)
from devtools.resources.filesystem import FilesystemNotFoundError
from scripts.backlog.coordinator import designate, git
from scripts.backlog.intake import _digest
from scripts.backlog.native.review.proposal import parse
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
        if str(self.source) == "context-script":
            if index == 0:
                selected = ModelToolCall(
                    "find_source",
                    json.dumps({"path": SOURCE, "mode": "symbol", "query": "value"}),
                    "find-0",
                )
            elif index == 1:
                metadata = json.loads(
                    next(
                        m.content
                        for m in request.prompt.messages
                        if m.tool_call_id == "find-0"
                    )
                )
                assert metadata["source_acquired"] is False
                assert metadata["units"][0]["name"] == "value"
                selected = ModelToolCall(
                    "read_source_unit",
                    json.dumps(
                        {
                            "unit_id": metadata["units"][0]["file_id"],
                            "snapshot_id": metadata["snapshot_id"],
                        }
                    ),
                    "read-1",
                )
            else:
                selected = self.calls[index - 1]
            return ModelResponse(
                "model-selected navigation/repair", self.source, tool_calls=(selected,)
            )
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


@pytest.mark.parametrize(
    "source", ["neutral-script-a", "independent-script-b", "context-script"]
)
def test_reviewed_native_task_to_authenticated_installable_plan(
    repository: tuple[WorkCycle, str], source: str
) -> None:
    """Run real failed/public checks, repair, withheld acceptance and governed handoff."""

    async def run() -> None:
        cycle, item = repository
        packet = task(source)
        if source == "context-script":
            packet["context"] = {
                "schema": "native-context-v1",
                "context_tokens": 65536,
                "input_tokens": 62464,
                "reserved_output_tokens": 2048,
                "disclosure_bytes": 65536,
                "warning_bytes": 98304,
                "trigger_bytes": 114688,
                "target_bytes": 98304,
            }
            packet["budgets"]["prompt_bytes"] = 131072
        await prepared(cycle, item, packet)
        model = Scripted(source)

        async def measured(_request: ModelRequest) -> int:
            return 512  # Authored tokenizer control, never a live capacity claim.

        result = await cycle.native.execute(
            item,
            interaction=model,
            profile="scripted-v1",
            authorize=lambda _: True,
            measure_input=measured,
            provider_context_tokens=65536,
        )
        assert result["disposition"] == "REVIEW_CANDIDATE", result
        facts = result["facts"]
        assert [g[0]["exit_code"] for g in facts["checks"]] == [1, 0]
        assert facts["acceptance"]["passed"]
        assert facts["restored"]
        assert facts["initial_context"]["unresolved"] == ["owner"]
        assert facts["readiness"][0]["ready"]
        assert facts["model_calls"] == (4 if source == "context-script" else 3)
        if source == "context-script":
            assert {t.name for t in model.requests[0].tools} == {
                "read_source",
                "replace_source",
                "validate_candidate",
                "find_source",
                "read_source_unit",
            }
            observations = [
                json.loads((cycle._folder(item) / "worker" / row["file"]).read_bytes())
                for row in facts["observations"]
            ]
            pressure = [r for r in observations if r["kind"] == "context-pressure"]
            assert len(pressure) == 4 and all(
                r["measured_input_tokens"] == 512 for r in pressure
            )
            assert all(r["policy"] == "deterministic" for r in pressure)
        history = next(
            json.loads((cycle._folder(item) / "worker" / row["file"]).read_bytes())
            for row in facts["observations"]
            if json.loads((cycle._folder(item) / "worker" / row["file"]).read_bytes())[
                "kind"
            ]
            == "coding-feedback-history"
        )
        assert [m["tool_call_id"] for m in history["messages"]] == (
            ["find-0"] if source == "context-script" else []
        ) + [
            "read-1",
            "edit-2",
            "repair-3",
        ]
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
                item,
                interaction=model,
                profile="scripted-v1",
                authorize=lambda _: True,
                measure_input=measured,
                provider_context_tokens=65536,
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


def reviewer_policy(source: str = "neutral-review-a") -> dict[str, Any]:
    """Approve an independently provisioned session, not merely another label."""
    return {
        "actor": "independent-review-actor",
        "source": source,
        "profile": "review-script-v1",
        "independence": {
            "reference": "fixture://host-session-attestation",
            "session": "fresh-review-session",
            "implementation_participant": False,
            "privileged_reference_access": False,
        },
        "read_paths": [PUBLIC],
        "settings": {"maximum_output_tokens": 1024, "thinking_enabled": False},
        "budgets": {
            "model_calls": 3,
            "reads": 2,
            "call_seconds": 10,
            "wall_seconds": 60,
            "prompt_bytes": 65536,
            "response_bytes": 16384,
            "capture_bytes": 524288,
        },
    }


def conclusion(disposition: str = "accept") -> dict[str, Any]:
    """Describe a model-attributed conclusion, never host authorization."""
    return {
        "disposition": disposition,
        "summary": "Candidate returns 3; observed checks support this finite repair, not general correctness.",
        "evidence": [
            "task",
            "baseline",
            "candidate",
            "public-checks",
            "acceptance",
            "custody",
        ],
        "findings": [
            {
                "kind": "observed",
                "severity": "advisory",
                "message": "A public failure preceded the successful repair",
                "evidence": ["public-checks"],
            }
        ],
        "outstanding": [],
        "requests": [],
        "assessed_obligations": ["objective", "owner"],
    }


def review_response(
    request: ModelRequest, source: InteractionSource, value: dict[str, Any]
) -> ModelResponse:
    """Emit a proposal through the actual advertised transport, including legacy fixtures."""
    from scripts.backlog.native.review import delivery  # noqa: PLC0415

    final = next((t for t in request.tools if t.name == delivery.NAME), None)
    if final is None:
        return ModelResponse(json.dumps(value), source)
    properties = json.loads(final.input_schema_json)["properties"]
    return ModelResponse(
        "",
        source,
        termination=ModelTermination.TOOL_CALL,
        tool_calls=(
            ModelToolCall(
                delivery.NAME,
                json.dumps(
                    {
                        "subject_sha256": properties["subject_sha256"]["enum"][0],
                        "candidate_sha256": properties["candidate_sha256"]["enum"][0],
                        "conclusion": value,
                    }
                ),
                "final-proposal",
            ),
        ),
    )


class ReviewModel:
    """Select actual read Tools and a structured review through ModelInteraction."""

    def __init__(
        self,
        source: str = "neutral-review-a",
        *,
        response: dict[str, Any] | None = None,
        fault: str | None = None,
    ) -> None:
        """Keep response choices separate from trusted host decisions."""
        self.source = InteractionSource(source)
        self.response, self.fault = response or conclusion(), fault
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Inspect actual disclosure and select a read before concluding."""
        self.requests.append(request)
        assert request.conversation is None and request.provider_settings is None
        assert [t.name for t in request.tools] in (
            ["read_source"],
            ["read_source", "submit_review_proposal"],
        )
        assert json.loads(request.prompt.messages[1].content)["review_scope"][
            "read_paths"
        ] == [PUBLIC]
        content = json.dumps(asdict(request))
        assert "assert module.value()" not in content
        assert "independently_derived" not in content
        assert "withheld.py" not in content
        if self.fault == "timeout":
            await asyncio.sleep(5)
        if self.fault == "malformed":
            return ModelResponse("Approved!", self.source)
        if self.fault == "output":
            return ModelResponse(
                json.dumps(self.response),
                self.source,
                termination=ModelTermination.OUTPUT_LIMIT,
            )
        if self.fault == "usage":
            return ModelResponse(
                json.dumps(self.response),
                self.source,
                usage=ModelUsage(output_tokens=1025),
            )
        if self.fault == "source":
            return ModelResponse(
                json.dumps(self.response), InteractionSource("foreign-review")
            )
        if len(self.requests) == 1 or self.fault == "calls":
            name = "replace_source" if self.fault == "edit" else "read_source"
            path = SOURCE if self.fault == "unauthorized" else PUBLIC
            return ModelResponse(
                "Inspect the published test obligation",
                self.source,
                tool_calls=(
                    ModelToolCall(
                        name,
                        json.dumps({"path": path, "start": 0}),
                        f"review-read-{len(self.requests)}",
                    ),
                ),
            )
        assert any(m.role == "tool" for m in request.prompt.messages)
        return review_response(request, self.source, self.response)


async def native_candidate(cycle: WorkCycle, item: str) -> None:
    """Produce a real checked/restored candidate for refusal controls."""
    await prepared(cycle, item, task())
    result = await cycle.native.execute(
        item,
        interaction=Scripted(
            "neutral-script-a", [read_call(), edit(1, 3, "direct-repair")]
        ),
        profile="scripted-v1",
        authorize=lambda _: True,
    )
    assert result["disposition"] == "REVIEW_CANDIDATE"


async def approve_reviewer(cycle: WorkCycle, item: str, config: dict[str, Any]) -> None:
    """Separately authorize only the exact frozen review subject."""
    await cycle.native.reviewer.prepare(item, reviewer=config)
    await cycle.native.reviewer.authorize(
        item,
        reference="fixture://review-only-approval",
        expires=Timestamp.now() + Duration.minutes(5),
        authorize=lambda _: True,
    )


@pytest.mark.parametrize("source", ["neutral-review-a", "independent-review-b"])
def test_native_review_actor_to_existing_integration_plan(
    repository: tuple[WorkCycle, str], source: str
) -> None:
    """Consume real failure/repair evidence; only a later host decision forms review."""

    async def run() -> None:
        cycle, item = repository
        await prepared(cycle, item, task())
        result = await cycle.native.execute(
            item,
            interaction=Scripted("neutral-script-a"),
            profile="scripted-v1",
            authorize=lambda _: True,
        )
        assert result["disposition"] == "REVIEW_CANDIDATE"
        await approve_reviewer(cycle, item, reviewer_policy(source))
        model = ReviewModel(source)
        proposal = await cycle.native.reviewer.execute(
            item,
            interaction=model,
            profile="review-script-v1",
            authorize=lambda _: True,
        )
        assert proposal["status"] == "proposed", proposal
        assert proposal["host_approved"] is False and proposal["model_calls"] == 2
        assert proposal["references"]["read:1"]
        assert not list(cycle._folder(item).glob("review-*.json"))
        with pytest.raises(PermissionError, match="host review"):
            await cycle.native.reviewer.decide(
                item,
                proposal=proposal["sha256"],
                accept=True,
                reference="fixture://declined",
                rationale="Host declined",
                authorize=lambda _: False,
            )
        seen = []

        def approve(value: dict[str, Any]) -> bool:
            seen.append(value)
            return True

        review = await cycle.native.reviewer.decide(
            item,
            proposal=proposal["sha256"],
            accept=True,
            reference="fixture://host-reviewed-proposal",
            rationale="Host independently inspected exact candidate and attributed findings",
            authorize=approve,
        )
        assert seen[0]["review_proposal"] == proposal
        assert (
            review["proposal_sha256"] == proposal["sha256"]
            and review["installation_authorized"] is False
        )
        plan = await cycle.integration.plan(
            item,
            review["sha256"],
            {
                "remote": "origin",
                "destination": "release",
                "feature": "feat/reviewed-native",
                "checkout": str(cycle.root),
                "additions": [],
                "parent_complete": False,
                "remaining": ["Authorized implementation competence remains unproved"],
                "rationale": "Host-approved grounded review",
                "validation_seconds": 60,
            },
        )
        assert (
            plan["candidate_kind"] == "native-v1"
            and plan["candidate_result"] == result["sha256"]
        )
        path = cycle.native.reviewer.folder(item) / "proposal.json"
        original = path.read_bytes()
        path.write_text(json.dumps({**proposal, "actor": "forged"}), encoding="utf-8")
        with pytest.raises(ValueError, match="identity/schema"):
            cycle.integration.candidate(item, review["sha256"])
        path.write_bytes(original)
        assert (cycle.root / SOURCE).read_text() == BASE
        assert not (cycle.root / ".local/backlog/checkout-owner").exists()
        assert not (
            cycle.integration.folder(item, plan["sha256"]) / "install.json"
        ).exists()

    asyncio.run(run())


@pytest.mark.parametrize(
    "fault",
    [
        "malformed",
        "output",
        "usage",
        "source",
        "unauthorized",
        "edit",
        "calls",
        "prompt",
        "capture",
        "timeout",
        "persist",
    ],
)
def test_native_review_actor_blocked_without_replay(
    repository: tuple[WorkCycle, str], fault: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Unknown/malformed/unauthorized outcomes never become acceptance or replay."""

    async def run() -> None:
        cycle, item = repository
        await native_candidate(cycle, item)
        config = reviewer_policy()
        if fault == "prompt":
            config["budgets"]["prompt_bytes"] = 1
        if fault == "capture":
            config["budgets"]["capture_bytes"] = 1
        if fault == "calls":
            config["budgets"]["model_calls"] = 1
        if fault == "timeout":
            config["budgets"]["call_seconds"] = config["budgets"]["wall_seconds"] = 1
        await approve_reviewer(cycle, item, config)
        # Materialize the historical pre-completion-policy contract in this
        # authored fixture; new known-refusal recovery has separate regressions.
        path = cycle.native.reviewer.folder(item) / "subject.json"
        packet = json.loads(path.read_bytes())
        packet.pop("sha256")
        packet.pop("completion")
        packet.pop("delivery")
        packet["sha256"] = _digest(packet)
        path.write_text(json.dumps(packet), encoding="utf-8")
        grant_path = cycle.native.reviewer.folder(item) / "authorization.json"
        grant = json.loads(grant_path.read_bytes())
        grant.pop("sha256")
        grant["subject_sha256"] = packet["sha256"]
        grant["sha256"] = _digest(grant)
        grant_path.write_text(json.dumps(grant), encoding="utf-8")
        model = ReviewModel(fault=fault)
        actor = cycle.native.reviewer
        original = actor.save

        def save(item: str, name: str, value: dict[str, Any]) -> dict[str, Any]:
            if name == "proposal":
                raise OSError("authored persistence failure")
            return original(item, name, value)

        if fault == "persist":
            monkeypatch.setattr(actor, "save", save)
        if fault == "persist":
            with pytest.raises(OSError, match="persistence"):
                await actor.execute(
                    item,
                    interaction=model,
                    profile="review-script-v1",
                    authorize=lambda _: True,
                )
        else:
            proposal = await actor.execute(
                item,
                interaction=model,
                profile="review-script-v1",
                authorize=lambda _: True,
            )
            assert proposal["status"] == "blocked" and proposal["conclusion"] is None, (
                proposal
            )
            expected = {
                "malformed": "JSONDecodeError",
                "output": "source/output allowance",
                "usage": "source/output allowance",
                "source": "source/output allowance",
                "unauthorized": "outside the admitted corpus",
                "edit": "not an authorized read",
                "calls": "model-call budget exhausted",
                "prompt": "Context cannot fit",
                "capture": "capture budget exhausted",
                "timeout": "TimeoutError",
            }
            assert expected[fault] in proposal["error"]
            with pytest.raises(PermissionError):
                await actor.decide(
                    item,
                    proposal=proposal["sha256"],
                    accept=True,
                    reference="fixture://unsafe",
                    rationale="Must refuse",
                    authorize=lambda _: True,
                )
        calls = len(model.requests)
        with pytest.raises(FileExistsError):
            await actor.execute(
                item,
                interaction=model,
                profile="review-script-v1",
                authorize=lambda _: True,
            )
        assert len(model.requests) == calls
        assert not list(cycle._folder(item).glob("review-*.json"))
        assert not (cycle.root / ".local/backlog/checkout-owner").exists()

    asyncio.run(run())


@pytest.mark.parametrize("disposition", ["reject", "insufficient-evidence"])
def test_native_adverse_review_requires_supervisor(
    repository: tuple[WorkCycle, str], disposition: str
) -> None:
    """Keep adverse or insufficient proposals out of integration admission."""

    async def run() -> None:
        cycle, item = repository
        await native_candidate(cycle, item)
        await approve_reviewer(cycle, item, reviewer_policy())
        value = conclusion(disposition)
        value["outstanding"] = ["Broader callers have not been inspected"]
        value["requests"] = ["Supervisor should authorize caller inspection"]
        value["findings"] = [
            {
                "kind": "inference",
                "severity": "blocking",
                "message": "A wider behavior contract may exist",
                "evidence": ["task", "candidate"],
            }
        ]
        proposal = await cycle.native.reviewer.execute(
            item,
            interaction=ReviewModel(response=value),
            profile="review-script-v1",
            authorize=lambda _: True,
        )
        assert proposal["conclusion"]["disposition"] == disposition
        with pytest.raises(PermissionError, match="Adverse"):
            await cycle.native.reviewer.decide(
                item,
                proposal=proposal["sha256"],
                accept=True,
                reference="fixture://cannot-overrule",
                rationale="Refuse acceptance",
                authorize=lambda _: True,
            )
        review = await cycle.native.reviewer.decide(
            item,
            proposal=proposal["sha256"],
            accept=False,
            reference="fixture://return-to-supervisor",
            rationale="Record adverse review and stop",
            authorize=lambda _: True,
        )
        assert review["disposition"] == "REJECTED"
        with pytest.raises(PermissionError):
            cycle.integration.candidate(item, review["sha256"])

    asyncio.run(run())


@pytest.mark.parametrize(
    "fault",
    [
        "identity",
        "participant",
        "privileged",
        "read-scope",
        "expired",
        "drift",
        "candidate",
        "missing",
    ],
)
def test_native_review_authority_and_subject_boundaries(
    repository: tuple[WorkCycle, str], fault: str
) -> None:
    """Refuse conflicting provenance, expired authority and drift before entry."""

    async def run() -> None:
        cycle, item = repository
        await native_candidate(cycle, item)
        config = reviewer_policy()
        if fault == "identity":
            config["actor"] = "neutral-coder"
        if fault == "participant":
            config["independence"]["implementation_participant"] = True
        if fault == "privileged":
            config["independence"]["privileged_reference_access"] = True
        if fault == "read-scope":
            config["read_paths"] = ["secrets.py"]
        if fault in {"identity", "participant", "privileged", "read-scope"}:
            with pytest.raises(PermissionError):
                await cycle.native.reviewer.prepare(item, reviewer=config)
            return
        await approve_reviewer(cycle, item, config)
        if fault == "expired":
            path = cycle.native.reviewer.folder(item) / "authorization.json"
            grant = cycle.native.reviewer.record(item, "authorization")
            grant["expires_at"] = str(Timestamp.now() - Duration.seconds(1))
            grant.pop("sha256")
            path.write_text(
                json.dumps({**grant, "sha256": _digest(grant)}), encoding="utf-8"
            )
        if fault == "drift":
            (cycle.root / SOURCE).write_text(
                "def value():\n    return 4\n", encoding="utf-8"
            )
        if fault == "candidate":
            (cycle._folder(item) / "worker/final-source.py").write_text(
                "def value():\n    return 8\n", encoding="utf-8"
            )
        if fault == "missing":
            (cycle._folder(item) / "worker/final-source.py").unlink()
        model = ReviewModel()
        with pytest.raises(
            (PermissionError, FileNotFoundError, FilesystemNotFoundError)
        ):
            await cycle.native.reviewer.execute(
                item,
                interaction=model,
                profile="review-script-v1",
                authorize=lambda _: True,
            )
        assert not model.requests

    asyncio.run(run())


@pytest.mark.parametrize(
    "fault",
    [
        "no-summary",
        "unknown-reference",
        "outstanding",
        "incomplete",
        "blocking",
        "self-authority",
        "duplicate-field",
    ],
)
def test_native_review_closed_grounded_conclusion(fault: str) -> None:
    """Reject incomplete, ungrounded or self-authorizing conclusions."""
    value = conclusion()
    if fault == "no-summary":
        value["summary"] = ""
    if fault == "unknown-reference":
        value["evidence"] = ["invented-proof"]
    if fault == "outstanding":
        value["outstanding"] = ["Unresolved behavior"]
    if fault == "incomplete":
        value["assessed_obligations"] = ["owner"]
    if fault == "blocking":
        value["findings"][0]["severity"] = "blocking"
    if fault == "self-authority":
        value["host_approved"] = True
    text = json.dumps(value)
    if fault == "duplicate-field":
        text = text[:-1] + ', "disposition": "accept"}'
    with pytest.raises(ValueError, match=r"Review|review|Acceptance|Duplicate|Coding"):
        parse(
            text,
            dict.fromkeys(conclusion()["evidence"], "exact-input-id"),
            {"objective", "owner"},
        )


def test_native_review_refuses_incomplete_terminal_evidence(
    repository: tuple[WorkCycle, str],
) -> None:
    """Inject authenticated fixture faults; no bad terminal evidence reaches a model."""

    async def run() -> None:
        cycle, item = repository
        await native_candidate(cycle, item)
        folder = cycle._folder(item)
        originals = {
            name: (folder / (name + ".json")).read_bytes()
            for name in ("execution", "result")
        }

        def replace_record(name: str, record: dict[str, Any]) -> dict[str, Any]:
            record.pop("sha256", None)
            sealed = {**record, "sha256": _digest(record)}
            (folder / (name + ".json")).write_text(json.dumps(sealed), encoding="utf-8")
            return sealed

        for fault in (
            "not-run",
            "failed",
            "private",
            "effects",
            "custody",
            "release",
            "completed",
            "task",
        ):
            for name, data in originals.items():
                (folder / (name + ".json")).write_bytes(data)
            execution = cycle.native.record(item, "execution")
            result = cycle.native.record(item, "result")
            facts = result["facts"]
            if fault == "not-run":
                facts["checks"] = []
            if fault == "failed":
                facts["checks"][-1][0]["passed"] = False
            if fault == "private":
                facts["acceptance"]["passed"] = False
            if fault == "effects":
                facts["effects"][0]["acknowledged"] = False
            if fault == "custody":
                facts["restored"] = False
            if fault == "release":
                result["checkout_released"] = False
            if fault == "completed":
                facts["completed"] = False
            if fault == "task":
                result["item"] = "B-9999"
            execution["facts"] = facts
            result["execution_sha256"] = replace_record("execution", execution)[
                "sha256"
            ]
            replace_record("result", result)
            with pytest.raises(PermissionError):
                await cycle.native.reviewer.prepare(item, reviewer=reviewer_policy())
            assert not cycle.native.reviewer.folder(item).exists()
        for name, data in originals.items():
            (folder / (name + ".json")).write_bytes(data)
        await cycle.native.reviewer.prepare(item, reviewer=reviewer_policy())

    asyncio.run(run())


def test_native_review_host_expiry_and_proposal_binding(
    repository: tuple[WorkCycle, str],
) -> None:
    """Reject fabricated conclusions, stale subjects and expiry during host consent."""

    async def run() -> None:
        cycle, item = repository
        await native_candidate(cycle, item)
        actor = cycle.native.reviewer
        await actor.prepare(item, reviewer=reviewer_policy())
        with pytest.raises(PermissionError):
            await actor.authorize(
                item,
                reference="fixture://no",
                expires=Timestamp.now() + Duration.minutes(5),
                authorize=lambda _: False,
            )
        await actor.authorize(
            item,
            reference="fixture://yes",
            expires=Timestamp.now() + Duration.minutes(5),
            authorize=lambda _: True,
        )
        model = ReviewModel()
        with pytest.raises(PermissionError, match="source/profile"):
            await actor.execute(
                item,
                interaction=model,
                profile="wrong-profile",
                authorize=lambda _: True,
            )
        with pytest.raises(PermissionError, match="dispatch"):
            await actor.execute(
                item,
                interaction=model,
                profile="review-script-v1",
                authorize=lambda _: False,
            )
        assert not model.requests
        proposal = await actor.execute(
            item,
            interaction=model,
            profile="review-script-v1",
            authorize=lambda _: True,
        )
        assert proposal["status"] == "proposed"
        path = actor.folder(item) / "proposal.json"
        original = path.read_bytes()
        forged = copy.deepcopy(proposal)
        forged["conclusion"]["summary"] = (
            "A different review that the model never returned"
        )
        forged.pop("sha256")
        forged = {**forged, "sha256": _digest(forged)}
        path.write_text(json.dumps(forged), encoding="utf-8")
        with pytest.raises(PermissionError, match="actual final model"):
            await actor.decide(
                item,
                proposal=forged["sha256"],
                accept=True,
                reference="fixture://forged",
                rationale="Reject substituted conclusion",
                authorize=lambda _: True,
            )
        path.write_bytes(original)
        forged = copy.deepcopy(proposal)
        forged["subject_sha256"] = "0" * 64
        forged.pop("sha256")
        forged = {**forged, "sha256": _digest(forged)}
        path.write_text(json.dumps(forged), encoding="utf-8")
        with pytest.raises(PermissionError, match="subject mismatch"):
            await actor.decide(
                item,
                proposal=forged["sha256"],
                accept=True,
                reference="fixture://stale",
                rationale="Reject another subject",
                authorize=lambda _: True,
            )
        path.write_bytes(original)

        def expire(_value: dict[str, Any]) -> bool:
            grant = actor.record(item, "authorization")
            grant["expires_at"] = str(Timestamp.now() - Duration.seconds(1))
            grant.pop("sha256")
            (actor.folder(item) / "authorization.json").write_text(
                json.dumps({**grant, "sha256": _digest(grant)}), encoding="utf-8"
            )
            return True

        with pytest.raises(PermissionError, match="expired"):
            await actor.decide(
                item,
                proposal=proposal["sha256"],
                accept=True,
                reference="fixture://expired-during-consent",
                rationale="Must recheck authority after host consent",
                authorize=expire,
            )
        assert not list(cycle._folder(item).glob("review-*.json"))

    asyncio.run(run())

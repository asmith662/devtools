# Copyright (c) 2026
# ruff: noqa: PLR2004 -- concrete administrative boundary checks
"""Backlog intake tests use isolated files and synthetic trusted hosts, no models."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import pytest

from devtools.resources.filesystem import write as filesystem_write
from scripts.backlog import __main__ as cli
from scripts.backlog import intake as module
from scripts.backlog.intake import Intake

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from devtools.resources.filesystem import File


@pytest.fixture
def intake(tmp_path: Path) -> Intake:
    """Create a canonical backlog plus an unrelated active task marker."""
    backlog = tmp_path / "docs/backlog"
    (backlog / "items").mkdir(parents=True)
    (backlog / "epics").mkdir()
    (backlog / "overview.md").write_text(
        "# Canonical backlog\n\n| ID | Title | Status | Domain |\n"
        "| --- | --- | --- | --- |\n"
        "| [B-0009](items/B-0009-existing.md) | Existing | BACKLOG | tools |\n"
        "\nFooter retained.\n",
        encoding="utf-8",
    )
    (backlog / "items/B-0009-existing.md").write_text(
        "# B-0009 — Existing\n",
        encoding="utf-8",
    )
    (tmp_path / "active-task.json").write_text(
        '{"objective":"unchanged"}',
        encoding="utf-8",
    )
    return Intake(tmp_path)


@pytest.fixture
def payload() -> dict[str, Any]:
    """Discovery is untrusted data and contains no authority fields."""
    return {
        "kind": "bug",
        "title": "Repair supported Python compatibility",
        "summary": "A documented constructor failure remains unresolved.",
        "discovery": {"kind": "agent", "reference": "task-02/observation"},
        "parent": "B-0009",
        "resources": ["src/example.py"],
        "evidence": ["receipt.json#sha256:123"],
        "benefit": "Restore supported behavior.",
        "uncertainty": "Scope and fix need investigation.",
        "dependencies": [],
    }


def review(intake: Intake, identity: str, **changes: Any) -> dict[str, Any]:  # noqa: ANN401 -- fixture overrides
    """Synthetic host authority is confined to this test fixture."""
    arguments = {
        "decision": "APPROVED",
        "reviewer": "fixture-host",
        "reference": "fixture://host-decision",
        "rationale": "Backlog inclusion only",
        "duplicate_disposition": "Reviewed; distinct from existing work",
        "domain": "resources",
        "authorize": lambda _request: True,
        **changes,
    }
    return intake.review(identity, **arguments)


def test_capture_history_and_advice_do_not_authorize_work(
    intake: Intake,
    payload: dict[str, Any],
) -> None:
    """Capture and advice preserve identity/evidence without selecting active work."""
    identity = intake.capture(payload)
    before = (intake.root / "active-task.json").read_bytes()
    record = intake.get(identity)
    assert record["proposal"]["payload"] == payload
    assert record["state"] == "PENDING_REVIEW"
    review(intake, identity, decision="ADVISORY", authorize=None)
    assert intake.get(identity)["state"] == "PENDING_REVIEW"
    with pytest.raises(PermissionError, match="host-approved"):
        intake.promote(identity, authorize=lambda _: True)
    assert (intake.root / "active-task.json").read_bytes() == before
    assert len(intake.queue()["proposals"]) == 1


@pytest.mark.parametrize("source", ["human", "agent", "tool", "research"])
def test_independent_sources(
    intake: Intake,
    payload: dict[str, Any],
    source: str,
) -> None:
    """Different source provenance is preserved rather than interpreted as authority."""
    payload["discovery"]["kind"] = source
    identity = intake.capture(payload)
    assert intake.get(identity)["proposal"]["payload"]["discovery"]["kind"] == source


def test_duplicate_candidates_include_proposals_and_canonical_backlog(
    intake: Intake,
    payload: dict[str, Any],
) -> None:
    """Similar titles/shared resources surface candidates without automatic merger."""
    first = intake.capture(payload)
    second = intake.capture(payload)
    (intake.backlog / "items/B-0010-related.md").write_text(
        "# B-0010 — Other\nAffected: src/example.py",
        encoding="utf-8",
    )
    matches = intake.duplicates(second)
    assert {m["reference"] for m in matches} == {
        first,
        "docs/backlog/items/B-0010-related.md",
    }
    decision = review(
        intake,
        second,
        decision="DEFERRED",
        duplicate_disposition="Potential duplicate; retain both for review",
    )
    assert len(decision["duplicates"]) == 2
    assert intake.get(first)["state"] == "PENDING_REVIEW"


def test_defer_reconsider_reject_preserves_order(
    intake: Intake,
    payload: dict[str, Any],
) -> None:
    """Deferral is reviewable later; rejection retains all discovery/history."""
    identity = intake.capture(payload)
    original = intake.get(identity)["proposal"]
    review(intake, identity, decision="DEFERRED")
    review(intake, identity, decision="ADVISORY", authorize=None)
    assert intake.get(identity)["state"] == "DEFERRED"
    review(intake, identity, decision="REJECTED")
    record = intake.get(identity)
    assert record["proposal"] == original
    assert [r["decision"] for r in record["history"]] == [
        "DEFERRED",
        "ADVISORY",
        "REJECTED",
    ]
    with pytest.raises(ValueError, match="Terminal"):
        review(intake, identity)


@pytest.mark.parametrize("authority", [None, lambda _: False])
def test_unauthorized_review_and_promotion_refused(
    intake: Intake,
    payload: dict[str, Any],
    authority: Callable[[dict[str, Any]], bool] | None,
) -> None:
    """No grant in model/source data or a forged reviewer string is sufficient."""
    identity = intake.capture(payload)
    with pytest.raises(PermissionError, match="Host authorization"):
        review(intake, identity, authorize=authority)
    assert intake.get(identity)["history"] == []
    review(intake, identity)
    with pytest.raises(PermissionError, match="Host authorization"):
        intake.promote(identity, authorize=authority)


def test_approved_promotion_reuses_canonical_convention(
    intake: Intake,
    payload: dict[str, Any],
) -> None:
    """The authorized publication is a normal B-number Markdown record/index row."""
    identity = intake.capture(payload)
    observed = []

    def authorize(request: dict[str, Any]) -> bool:
        observed.append(request)
        return True

    decision = review(intake, identity, authorize=authorize)
    assert observed[0]["proposed_work"]["payload"] == payload
    assert "no execution authority" in decision["scope"]
    assert intake.promote(identity, authorize=lambda _: True) == "B-0010"
    publication = decision["publication"]
    assert (intake.backlog / publication["path"]).read_text(
        encoding="utf-8",
    ) == publication["text"]
    assert "- status: BACKLOG" in publication["text"]
    assert "- execution_authorization: NONE" in publication["text"]
    index = (intake.backlog / "overview.md").read_bytes()
    assert intake.promote(identity, authorize=lambda _: True) == "B-0010"
    assert (intake.backlog / "overview.md").read_bytes() == index
    assert index.decode().index(publication["row"]) < index.decode().index(
        "Footer retained.",
    )


def test_pending_approved_ids_are_reserved(
    intake: Intake,
    payload: dict[str, Any],
) -> None:
    """Approvals reserve distinct B-numbers before either is published."""
    a, b = intake.capture(payload), intake.capture(payload)
    assert review(intake, a)["publication"]["id"] == "B-0010"
    assert review(intake, b)["publication"]["id"] == "B-0011"


def test_interrupted_promotion_reconciles_without_overwrite(
    intake: Intake,
    payload: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Atomic item write followed by an interrupted index write is recoverable."""
    identity = intake.capture(payload)
    decision = review(intake, identity)
    real = filesystem_write

    def interrupt(file: File, *, overwrite: bool = True) -> None:
        if file.path.name == "overview.md":
            message = "interrupted index write"
            raise OSError(message)
        real(file, overwrite=overwrite)

    monkeypatch.setattr(module, "write", interrupt)
    with pytest.raises(OSError, match="interrupted"):
        intake.promote(identity, authorize=lambda _: True)
    path = intake.backlog / decision["publication"]["path"]
    original = path.read_bytes()
    monkeypatch.setattr(module, "write", real)
    intake.promote(identity, authorize=lambda _: True)
    assert path.read_bytes() == original
    path.write_text("conflicting external edit", encoding="utf-8")
    with pytest.raises(ValueError, match="Conflicting backlog item"):
        intake.promote(identity, authorize=lambda _: True)


@pytest.mark.parametrize("damage", ["partial", "payload", "review", "gap"])
def test_malformed_or_incomplete_records_fail_closed(
    intake: Intake,
    payload: dict[str, Any],
    damage: str,
) -> None:
    """Unreadable/corrupt history is surfaced, never silently reset to pending."""
    identity = intake.capture(payload)
    review(intake, identity, decision="ADVISORY")
    folder = intake.proposals / identity
    if damage == "partial":
        (folder / "proposal.json").write_text('{"partial":', encoding="utf-8")
    elif damage == "payload":
        value = json.loads((folder / "proposal.json").read_text())
        value["payload"]["benefit"] = "tampered"
        (folder / "proposal.json").write_text(json.dumps(value), encoding="utf-8")
    elif damage == "review":
        (folder / "review-0001.json").write_text("{}", encoding="utf-8")
    else:
        (folder / "review-0001.json").rename(folder / "review-0002.json")
    assert intake.queue()["errors"]
    with pytest.raises((ValueError, KeyError)):
        intake.promote(identity, authorize=lambda _: True)


def test_partial_capture_and_stale_writer_require_reconciliation(
    intake: Intake,
    payload: dict[str, Any],
) -> None:
    """A crash never allows blind overwrite or concurrent writer admission."""
    intake.proposals.mkdir()
    (intake.proposals / "broken").mkdir()
    assert intake.queue()["errors"]
    (intake.proposals / ".writer").mkdir()
    with pytest.raises(FileExistsError):
        intake.capture(payload)


@pytest.mark.parametrize(
    "change",
    [
        {"authorize": True},
        {"kind": "execute"},
        {"evidence": []},
        {"title": "bad\nheading"},
        {"discovery": {"kind": "unknown", "reference": "x"}},
    ],
)
def test_untrusted_input_cannot_broaden_schema(
    intake: Intake,
    payload: dict[str, Any],
    change: dict[str, Any],
) -> None:
    """No task execution or arbitrary authority knobs enter the proposal schema."""
    payload.update(change)
    with pytest.raises(ValueError, match=r"fields|kind|evidence|line|source"):
        intake.capture(payload)


def test_proposal_path_cannot_escape(intake: Intake) -> None:
    """Only host-generated valid identities are lookup paths."""
    with pytest.raises(ValueError, match="UUID"):
        intake.get("../../outside")


def test_cli_capture_list_and_advisory(
    intake: Intake,
    payload: dict[str, Any],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Noninteractive intake/advice are usable, but never grant promotion."""
    path = intake.root / "input.json"
    path.write_text(json.dumps(payload))
    base = ["--root", str(intake.root)]
    assert cli.main([*base, "capture", str(path)]) == 0
    identity = json.loads(capsys.readouterr().out)["id"]
    assert cli.main([*base, "list"]) == 0
    capsys.readouterr()
    assert cli.main([*base, "show", identity]) == 0
    capsys.readouterr()
    assert (
        cli.main(
            [
                *base,
                "review",
                identity,
                "--decision",
                "ADVISORY",
                "--reference",
                "fixture",
                "--rationale",
                "needs human review",
                "--duplicates",
                "none",
                "--advisor",
                "Codex (advisory)",
            ],
        )
        == 0
    )
    assert intake.get(identity)["state"] == "PENDING_REVIEW"


@pytest.mark.parametrize(
    ("answer", "allowed"),
    [("", False), ("n", False), ("y", True)],
)
def test_genuine_terminal_confirmation_defaults_no(
    monkeypatch: pytest.MonkeyPatch,
    answer: str,
    *,
    allowed: bool,
) -> None:
    """Only actual affirmative terminal input approves the exact displayed scope."""
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _: answer)
    assert cli.confirm({"scope": "fixture"}) is allowed


def test_noninteractive_review_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    """CLI flags alone never provide authorization."""
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    with pytest.raises(PermissionError, match="interactive terminal"):
        cli.confirm({"decision": "APPROVED"})


def test_review_write_failure_keeps_previous_state(
    intake: Intake,
    payload: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A failed canonical atomic write never erases or partially replaces history."""
    identity = intake.capture(payload)
    first = review(intake, identity, decision="ADVISORY")

    def fail(*_args: object, **_kwargs: object) -> None:
        message = "simulated write failure"
        raise OSError(message)

    monkeypatch.setattr(module, "write", fail)
    with pytest.raises(OSError, match="simulated"):
        review(intake, identity, decision="DEFERRED")
    assert intake.get(identity)["history"] == [first]
    assert intake.get(identity)["state"] == "PENDING_REVIEW"
    assert not (intake.proposals / ".writer").exists()


def test_cli_authoritative_review_refuses_noninteractive(
    intake: Intake,
    payload: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Supplying reviewer-like flags cannot authorize a model-originated decision."""
    identity = intake.capture(payload)
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    assert (
        cli.main(
            [
                "--root",
                str(intake.root),
                "review",
                identity,
                "--decision",
                "APPROVED",
                "--reference",
                "untrusted-message",
                "--rationale",
                "self approve",
                "--duplicates",
                "none",
                "--domain",
                "resources",
            ],
        )
        == 1
    )
    assert intake.get(identity)["history"] == []


def test_pending_filter_and_malformed_cli_reporting(
    intake: Intake,
    payload: dict[str, Any],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Deferred records stay in history while pending lookup retains errors."""
    identity = intake.capture(payload)
    review(intake, identity, decision="DEFERRED")
    base = ["--root", str(intake.root), "list", "--pending"]
    assert cli.main(base) == 0
    assert json.loads(capsys.readouterr().out)["proposals"] == []
    (intake.proposals / "interrupted-capture").mkdir()
    assert cli.main(base) == 1
    assert json.loads(capsys.readouterr().out)["errors"]


def test_index_conflict_never_overwritten(
    intake: Intake,
    payload: dict[str, Any],
) -> None:
    """A mismatched preexisting B-number index entry requires operator review."""
    identity = intake.capture(payload)
    review(intake, identity)
    overview = intake.backlog / "overview.md"
    overview.write_text(
        overview.read_text() + "| [B-0010](wrong.md) | conflict | BACKLOG | tools |\n",
    )
    before = overview.read_bytes()
    with pytest.raises(ValueError, match="Conflicting backlog index"):
        intake.promote(identity, authorize=lambda _: True)
    assert overview.read_bytes() == before


def test_interrupted_capture_with_valid_identity_is_reported(
    intake: Intake,
    payload: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A crash after directory creation surfaces the missing canonical JSON file."""

    def fail(*_args: object, **_kwargs: object) -> None:
        message = "capture interrupted before atomic publication"
        raise OSError(message)

    monkeypatch.setattr(module, "write", fail)
    with pytest.raises(OSError, match="capture interrupted"):
        intake.capture(payload)
    result = intake.queue()
    assert result["proposals"] == []
    assert len(result["errors"]) == 1
    assert "does not exist" in result["errors"][0]["error"]


def test_oversized_payload_rejected_before_capture(
    intake: Intake,
    payload: dict[str, Any],
) -> None:
    """Individually bounded references cannot produce an unreadable proposal."""
    payload["evidence"] = ["x" * 8000] * 10
    with pytest.raises(ValueError, match="64 KiB"):
        intake.capture(payload)
    assert intake.queue() == {"proposals": [], "errors": []}

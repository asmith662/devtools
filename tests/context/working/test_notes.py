# Copyright (c) 2026
# ruff: noqa: PLR2004, D103, ANN401, RUF001 -- finite invalid-input and Unicode controls
"""Source facts, fallible claims, freshness, scope and bounded reconstruction."""

from __future__ import annotations

import json
from dataclasses import replace
from typing import Any

import pytest

from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
)
from devtools.context.repository.snapshot import RepositorySnapshotId
from devtools.context.working import (
    NoteScope,
    SourceBinding,
    WorkingNote,
    WorkingNotes,
    coverage,
)


def binding(text: str = "αbcdefghij", *, live: bool = True) -> SourceBinding:
    """Use a canonical observed occurrence, never a copied repository tree."""
    resource = RepositoryResourceOccurrence(
        RepositoryResourceAddress("fixture.py"),
        ContentIdentity.from_text(text),
        text,
        "utf-8",
        len(text.encode()),
    )
    return SourceBinding(
        "candidate",
        resource,
        "subject:candidate",
        ((0, len(text)),),
        RepositorySnapshotId("a" * 64),
        live,
    )


def book(source: SourceBinding | None = None) -> WorkingNotes:
    """Keep role and episode separate from source identity."""
    source = source or binding()
    return WorkingNotes(
        NoteScope("task", "reviewer", "episode"),
        {source.reference: source},
    )


def test_coverage_merges_only_observed_ranges() -> None:
    assert coverage(40, ((20, 30), (0, 10), (5, 8), (10, 12), (12, 12))) == (
        ((0, 12), (20, 30)),
        ((12, 20), (30, 40)),
    )
    assert coverage(0, ()) == ((), ())
    assert coverage(3, ()) == ((), ((0, 3),))


@pytest.mark.parametrize(
    ("size", "spans"),
    [
        (-1, ()),
        (True, ()),
        (2, ((-1, 1),)),
        (2, ((1, 3),)),
        (2, ((True, 1),)),
        (2, ((0, False),)),
        (2, ((2, 1),)),
    ],
)
def test_invalid_ranges(size: Any, spans: Any) -> None:
    with pytest.raises(ValueError, match="ranges"):
        coverage(size, spans)


def test_source_anchors_are_literal_and_unicode_bound() -> None:
    source = binding()
    anchor = source.anchor(0, 1, "α")
    assert source.current(anchor)
    assert source.reopen(anchor)["read_source"] == {
        "path": "fixture.py",
        "start": 0,
        "end": 1,
    }
    archived = replace(source, live=False, snapshot=None)
    archived_anchor = archived.anchor(0, 1, "α")
    assert archived.reopen(archived_anchor)["origin"] == "retained-subject"
    assert archived.reopen(archived_anchor)["read_source"] is None
    assert not replace(source, snapshot=RepositorySnapshotId("b" * 64)).current(anchor)
    assert not binding("changed").current(anchor)
    with pytest.raises(ValueError, match="stale"):
        binding("changed").reopen(anchor)


@pytest.mark.parametrize(
    "change",
    [{"reference": " "}, {"receipt": ""}, {"resource": None}],
)
def test_binding_identity_validation(change: dict[str, Any]) -> None:
    source = binding()
    if "resource" in change:
        change["resource"] = replace(
            source.resource,
            content_identity=ContentIdentity.from_text("other"),
        )
    with pytest.raises(ValueError, match="authenticated"):
        replace(source, **change)


@pytest.mark.parametrize(
    ("start", "end", "quote"),
    [
        (True, 1, "α"),
        (0, False, ""),
        (-1, 1, "α"),
        (0, 11, "α"),
        (0, 1, "wrong"),
        (1, 1, ""),
        (3, 2, ""),
    ],
)
def test_bad_source_intervals(start: Any, end: Any, quote: str) -> None:
    with pytest.raises(ValueError, match="interval"):
        binding().anchor(start, end, quote)


def test_unread_source_and_quote_limit() -> None:
    with pytest.raises(ValueError, match="interval"):
        replace(binding(), spans=((0, 2),)).anchor(2, 3, "c")
    with pytest.raises(ValueError, match="interval"):
        binding("x" * 513).anchor(0, 513, "x" * 513)


@pytest.mark.parametrize(
    "scope",
    [("", "reviewer", "episode"), ("task", "x" * 257, "episode")],
)
def test_scope_requires_provenance(scope: tuple[str, str, str]) -> None:
    with pytest.raises(ValueError, match="identities"):
        NoteScope(*scope)


def test_model_claim_and_exact_fact_are_distinct() -> None:
    state = book()
    anchor = state.sources["candidate"].anchor(0, 1, "α")
    claim = state.record("source", "This proves a defect", "expected API", (anchor,))
    assert state.status(claim) == "provisional"
    literal = state.observe(anchor)
    assert literal.text == "α"
    assert state.status(literal) == "host-verified"
    assert literal.verification == "host:exact-source-quotation"


def test_whitespace_source_observation() -> None:
    state = book(binding(" "))
    assert state.observe(state.sources["candidate"].anchor(0, 1, " ")).text == " "


def test_relationships_questions_and_explicit_revision() -> None:
    state = book()
    anchor = state.sources["candidate"].anchor(0, 2, "αb")
    old = state.record(
        "relationship",
        "Helper yields pairs",
        "Caller unpacks pairs",
        (anchor,),
    )
    question = state.record(
        "question",
        "Where is the helper yield?",
        "",
        contradicts=(old.sequence,),
    )
    assert state.status(old) == "contested"
    assert state.status(question) == "provisional"
    fixed = state.record(
        "hypothesis",
        "Helper may yield nodes",
        "Inspect caller/helper",
        (anchor,),
        supersedes=(1,),
    )
    assert state.status(old) == "superseded"
    verified = state.attest(fixed.sequence, "host:checked-return-contract:receipt")
    assert state.status(fixed) == "superseded"
    assert state.status(verified) == "host-verified"
    with pytest.raises(ValueError, match="cannot supersede"):
        state.record(
            "hypothesis",
            "Override host",
            "contract",
            supersedes=(verified.sequence,),
        )
    assert len(state.notes) == 4


@pytest.mark.parametrize(
    "changes",
    [
        {"kind": "unknown"},
        {"text": " "},
        {"text": "x" * 1025},
        {"expected_contract": "x" * 1025},
        {"expected_contract": ""},
        {"kind": "source"},
        {"contradicts": (0,)},
        {"supersedes": (True,)},
    ],
)
def test_invalid_provisional_notes(changes: dict[str, Any]) -> None:
    value: dict[str, Any] = {
        "kind": "hypothesis",
        "text": "claim",
        "expected_contract": "contract",
    }
    value.update(changes)
    with pytest.raises(ValueError, match=r"bounds|predecessor"):
        book().record(**value)


def test_stale_and_unavailable_support_never_verifies_claims() -> None:
    state = book()
    anchor = state.sources["candidate"].anchor(0, 1, "α")
    with pytest.raises(ValueError, match="stale"):
        state.record(
            "hypothesis",
            "claim",
            "contract",
            (replace(anchor, reference="private"),),
        )
    with pytest.raises(ValueError, match="stale"):
        state.record(
            "hypothesis",
            "claim",
            "contract",
            (replace(anchor, snapshot=RepositorySnapshotId("b" * 64)),),
        )
    with pytest.raises(ValueError, match="bounds"):
        state.record("hypothesis", "claim", "contract", (anchor,) * 5)
    observed = state.observe(anchor)
    state.sources["candidate"] = binding("changed")
    assert state.status(observed) == "stale"
    state.sources.clear()
    assert state.status(observed) == "stale"


@pytest.mark.parametrize(
    ("sequence", "receipt"),
    [(0, "check"), (True, "check"), (1, ""), (1, "x" * 257)],
)
def test_invalid_host_verification(sequence: Any, receipt: str) -> None:
    state = book()
    state.record("conclusion", "claim", "contract")
    with pytest.raises(ValueError, match="verification"):
        state.attest(sequence, receipt)


def test_finite_history_and_projection() -> None:
    state = book()
    for _ in range(32):
        state.record("question", "unknown" * 30, "")
    with pytest.raises(ValueError, match="bounds"):
        state.record("question", "extra", "")
    view = state.project(1024)
    assert len(json.dumps(view, ensure_ascii=False).encode()) <= 1024
    assert view["omitted_notes"]
    minimum = WorkingNotes(state.scope, {}).project(4096)
    size = len(json.dumps(minimum, ensure_ascii=False).encode())
    view = state.project(size + 4)
    assert view["omitted_notes"] == 32
    assert view["omitted_sources"] == 1
    with pytest.raises(ValueError, match="cannot fit"):
        state.project(1)


@pytest.mark.parametrize("budget", [0, -1, True, float("inf")])
def test_projection_requires_finite_positive_integer(budget: Any) -> None:
    with pytest.raises(ValueError, match="positive finite"):
        book().project(budget)


def test_reconstruction_scope_and_new_source_invalidation() -> None:
    original = book()
    anchor = original.sources["candidate"].anchor(0, 1, "α")
    original.observe(anchor)
    reconstructed = book()
    reconstructed.restore(original.scope, original.notes)
    assert reconstructed.project(4096) == original.project(4096)
    assert original.checkpoint()["scope"] == {
        "task": "task",
        "role": "reviewer",
        "episode": "episode",
    }
    with pytest.raises(ValueError, match="incompatible"):
        reconstructed.restore(original.scope, original.notes)
    with pytest.raises(ValueError, match="incompatible"):
        book().restore(replace(original.scope, role="coder"), original.notes)
    with pytest.raises(ValueError, match="incompatible"):
        book().restore(original.scope, original.notes * 33)
    with pytest.raises(ValueError, match="sequence"):
        book().restore(original.scope, (WorkingNote(2, "question", "missing", ""),))
    stale = book(binding("new"))
    stale.restore(original.scope, original.notes)
    assert stale.status(stale.notes[0]) == "stale"

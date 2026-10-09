# Copyright (c) 2026
# ruff: noqa: COM812, S101, D103, PLR2004 -- controlled fixture assertions; formatter owns commas
"""Behavior equality excludes authorship only and detects native-result changes."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.localization.grounding.contract import AnchorGroundingDisposition
from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationTaskIdentity,
)
from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25Match,
    RepositoryTextLexicalBm25RetrievalResult,
    RepositoryTextLexicalBm25Settings,
    RepositoryTextLexicalBm25TermContribution,
    analyze_repository_text_lexical_query,
)
from experiments.codex_dogfood.case_0009.artifacts import put_text
from experiments.exact_hint_routing import behavior
from experiments.exact_hint_routing.extraction import extract
from experiments.exact_hint_routing.models import HintAssociation, ResolutionDisposition
from experiments.exact_hint_routing.presentation import present
from experiments.exact_hint_routing.routing import admit, resolve
from experiments.exact_hint_routing.serialization import encode
from experiments.exact_hint_routing.tests.conftest import make_frame

if TYPE_CHECKING:
    from pathlib import Path

    from experiments.exact_hint_routing.models import ExactHintRoutingView
    from experiments.exact_hint_routing.routing import ExactFrame


@pytest.fixture
def equivalent(
    tmp_path: Path,
) -> tuple[ExactFrame, ExactHintRoutingView, ExactHintRoutingView]:
    put_text(tmp_path / "docs/extra.md", "fixture fallback\n")
    frame, index = make_frame(tmp_path)
    # Synthetic native match objects: no lexical retrieval or Case 0012 input.
    lexical = RepositoryTextLexicalBm25RetrievalResult(
        analyze_repository_text_lexical_query(text="fixture"),
        index,
        RepositoryTextLexicalBm25Settings(),
        3,
        tuple(
            RepositoryTextLexicalBm25Match(
                stat,
                3.0 - n * 0.5,
                (
                    RepositoryTextLexicalBm25TermContribution(
                        "fixture",
                        1,
                        1,
                        0.5,
                        stat.document_length,
                        index.corpus_statistics.average_document_length,
                        2.0,
                    ),
                ),
                content_score=2.0,
                filename_score=1.0,
                filename_weight=0.25,
                weighted_filename_score=0.25,
            )
            for n, stat in enumerate(index.corpus_statistics.document_statistics)
        ),
    )
    hints = tuple(
        d.observation
        for d in extract(
            LocalizationTaskIdentity("behavior-fixture"),
            "file `src/pkg/native.py` then file `docs/notes.md`",
        )
        if d.observation is not None
    )
    views = []
    for arm in ("B", "C"):
        resolutions = []
        for h in hints:
            hint = (
                h
                if arm == "C"
                else replace(
                    h,
                    rule="caller-task-review-v1",
                    syntactic_form="caller-reviewed-task-syntax",
                    provenance=replace(
                        h.provenance, explanation="Caller reviewed fixture"
                    ),
                )
            )
            association = HintAssociation(
                h.identity,
                LocalizationObligationIdentity(h.task, "owner"),
                "Fixture clause",
                h.provenance,
            )
            resolutions.append(resolve(frame, admit(hint, association)))
        views.append(
            present(
                frame=frame,
                lane=resolutions[0].request.association.lane,
                lexical=lexical,
                global_safety=lexical,
                resolutions=tuple(resolutions),
                provenance=resolutions[0].request.hint.provenance,
            )
        )
    return frame, views[0], views[1]


def test_equivalent_behavior_keeps_native_authorship(
    equivalent: tuple[ExactFrame, ExactHintRoutingView, ExactHintRoutingView],
) -> None:
    frame, b, c = equivalent
    before = encode(b), encode(c)
    assert b != c
    assert before[0] != before[1]
    assert b.exact_resolutions[0].request != c.exact_resolutions[0].request
    assert (
        b.exact_resolutions[0].native_provenance[0].request.provenance
        != c.exact_resolutions[0].native_provenance[0].request.provenance
    )
    for left, right in zip(b.exact_resolutions, c.exact_resolutions, strict=True):
        assert behavior.route_input(frame, left.request) == behavior.route_input(
            frame, right.request
        )
        behavior.require_equivalent(
            behavior.resolution(frame, left), behavior.resolution(frame, right)
        )
    behavior.require_equivalent(
        behavior.presentation(frame, b), behavior.presentation(frame, c)
    )
    assert (encode(b), encode(c)) == before
    assert b"Caller reviewed fixture" in before[0]
    assert b"Task text only; no repository lookup" in before[1]


@pytest.mark.parametrize(
    "change", ["disposition", "referent", "evidence", "reason", "result_frame"]
)
def test_native_resolution_changes_are_defects(
    equivalent: tuple[ExactFrame, ExactHintRoutingView, ExactHintRoutingView],
    change: str,
) -> None:
    frame, b, _ = equivalent
    result = b.exact_resolutions[0]
    account = result.native_provenance[0]
    other = b.exact_resolutions[1].resources[0]
    if change == "disposition":
        changed = replace(
            result, disposition=ResolutionDisposition.UNRESOLVED, resources=()
        )
    elif change == "referent":
        changed = replace(
            result,
            native_provenance=(
                replace(
                    account,
                    candidates=(replace(account.candidates[0], referent=other),),
                ),
            ),
        )
    elif change == "evidence":
        changed = replace(
            result, native_provenance=(replace(account, native_evidence=(other,)),)
        )
    elif change == "reason":
        changed = replace(result, reason=result.reason + " changed")
    else:
        changed = replace(result, frame_identity="foreign")
    with pytest.raises(ValueError, match="EXPERIMENTAL_CONTRACT_DEFECT"):
        behavior.require_equivalent(
            behavior.resolution(frame, result), behavior.resolution(frame, changed)
        )


@pytest.mark.parametrize(
    "change",
    [
        "promoted_resource",
        "exact_order",
        "exact_position",
        "fallback_membership",
        "fallback_order",
        "rank",
        "score",
        "content_contribution",
        "weighted_filename",
        "global_safety",
    ],
)
def test_presentation_changes_are_defects(  # noqa: C901 -- independent field mutations in a controlled fixture
    equivalent: tuple[ExactFrame, ExactHintRoutingView, ExactHintRoutingView],
    change: str,
) -> None:
    frame, b, _ = equivalent
    if change.startswith("fallback"):
        b = replace(
            b,
            exact_resolutions=(),
            exact_first=tuple(replace(e, exact=None) for e in b.exact_first),
        )
    entries = list(b.exact_first)
    first = entries[0]
    if change == "promoted_resource":
        entries[0] = replace(first, resource=entries[1].resource)
    elif change in {"exact_order", "fallback_order"}:
        entries.reverse()
    elif change == "exact_position":
        assert first.exact is not None
        entries[0] = replace(first, exact=replace(first.exact, exact_tier_position=2))
    elif change == "fallback_membership":
        entries.pop()
    elif change == "rank":
        entries[0] = replace(first, native_lexical_rank=99)
    elif change == "global_safety":
        changed = replace(
            b,
            global_lexical_safety_lane=replace(
                b.global_lexical_safety_lane,
                matches=b.global_lexical_safety_lane.matches[::-1],
            ),
        )
    else:
        match = first.lexical_result_reference
        assert match is not None
        if change == "score":
            match = replace(match, score=match.score + 1)
        elif change == "weighted_filename":
            match = replace(
                match, weighted_filename_score=match.weighted_filename_score + 0.1
            )
        else:
            match = replace(
                match,
                term_contributions=(
                    replace(match.term_contributions[0], contribution=99.0),
                ),
            )
        entries[0] = replace(first, lexical_result_reference=match)
    if change != "global_safety":
        changed = replace(b, exact_first=tuple(entries))
    with pytest.raises(ValueError, match="EXPERIMENTAL_CONTRACT_DEFECT"):
        behavior.require_equivalent(
            behavior.presentation(frame, b), behavior.presentation(frame, changed)
        )


def test_different_frozen_inputs_are_a_distinct_precondition(
    equivalent: tuple[ExactFrame, ExactHintRoutingView, ExactHintRoutingView],
) -> None:
    frame, b, _ = equivalent
    left = behavior.resolution(frame, b.exact_resolutions[0])
    right = behavior.resolution(frame, b.exact_resolutions[1])
    with pytest.raises(ValueError, match="semantic route inputs differ"):
        behavior.require_equivalent(left, right)


def test_ambiguous_candidate_identities_and_order_are_retained(
    equivalent: tuple[ExactFrame, ExactHintRoutingView, ExactHintRoutingView],
) -> None:
    frame, b, _ = equivalent
    result = b.exact_resolutions[0]
    account = result.native_provenance[0]
    other = b.exact_resolutions[1].resources[0]
    candidates = (
        account.candidates[0],
        replace(account.candidates[0], referent=other, evidence=other),
    )
    account = replace(
        account, disposition=AnchorGroundingDisposition.AMBIGUOUS, candidates=candidates
    )
    ambiguous = replace(
        result,
        disposition=ResolutionDisposition.AMBIGUOUS,
        resources=(),
        native_provenance=(account,),
    )
    left = behavior.resolution(frame, ambiguous)
    assert len(left["native_accounts"][0]["candidates"]) == 2
    changed = replace(
        ambiguous, native_provenance=(replace(account, candidates=candidates[::-1]),)
    )
    with pytest.raises(ValueError, match="EXPERIMENTAL_CONTRACT_DEFECT"):
        behavior.require_equivalent(left, behavior.resolution(frame, changed))

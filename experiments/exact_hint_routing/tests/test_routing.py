# Copyright (c) 2026
# ruff: noqa: COM812, S101, D103, PT011, PLR2004 -- literal protocol prose or fixture assertions; formatter owns commas
"""Native exact fixtures, complete fallback and immutable score references."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationTaskIdentity,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.snapshot import RepositorySnapshotId
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.exact_hint_routing.extraction import extract
from experiments.exact_hint_routing.models import HintAssociation, ResolutionDisposition
from experiments.exact_hint_routing.presentation import present
from experiments.exact_hint_routing.routing import admit, resolve
from experiments.exact_hint_routing.serialization import encode
from experiments.exact_hint_routing.tests.conftest import make_frame

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )
    from experiments.exact_hint_routing.models import ExactHintRouteRequest
    from experiments.exact_hint_routing.routing import ExactFrame


def request(text: str) -> ExactHintRouteRequest:
    hint = next(
        d.observation
        for d in extract(LocalizationTaskIdentity("fixture-route"), text)
        if d.observation
    )
    return admit(
        hint,
        HintAssociation(
            hint.identity,
            LocalizationObligationIdentity(hint.task, "owner"),
            "Explicit fixture task clause",
            hint.provenance,
        ),
    )


@pytest.mark.parametrize(
    ("text", "status"),
    [
        ("file `src/pkg/native.py`", "RESOLVED"),
        ("module `pkg.native`", "RESOLVED"),
        ("function `pkg.native.build`", "RESOLVED"),
        ("class `pkg.native.Target`", "RESOLVED"),
        ("method `pkg.native.Target.run`", "RESOLVED"),
        ("class `Target`", "UNSUPPORTED"),
        ("module `absent.native`", "UNRESOLVED"),
        ("module `native`", "UNRESOLVED"),
        ("function `native.build`", "UNRESOLVED"),
        ("method `native.Target.run`", "UNRESOLVED"),
        ("function `pkg.native.missing`", "UNRESOLVED"),
        ("method `pkg.native.Target.missing`", "UNRESOLVED"),
        ("file `src/absent.py`", "UNRESOLVED"),
    ],
)
def test_native_routes(
    native: tuple[ExactFrame, RepositoryTextLexicalInvertedIndex],
    text: str,
    status: str,
) -> None:
    frame, _ = native
    result = resolve(frame, request(text))
    assert result.disposition.value == status
    assert bool(result.resources) == (status == "RESOLVED")
    assert encode(result) == encode(result)
    if result.resources:
        assert result.resources[0] is frame.snapshot.resource_at(
            result.resources[0].address
        )


@pytest.mark.parametrize(
    "source",
    ["class Target: pass\nclass Target: pass\n", "@decorate\nclass Target: pass\n"],
)
def test_repeated_or_decorated_source(tmp_path: Path, source: str) -> None:
    frame, _ = make_frame(tmp_path, source)
    result = resolve(frame, request("class `pkg.native.Target`"))
    expected = (
        ResolutionDisposition.AMBIGUOUS
        if source.count("class Target") == 2
        else ResolutionDisposition.RESOLVED
    )
    assert result.disposition is expected
    assert len(result.native_provenance[0].candidates) == source.count("class Target")
    assert bool(result.resources) == (expected is ResolutionDisposition.RESOLVED)


def test_native_parse_failure(tmp_path: Path) -> None:
    frame, _ = make_frame(tmp_path, "class Target:\n invalid syntax @\n")
    result = resolve(frame, request("class `pkg.native.Target`"))
    assert result.disposition is ResolutionDisposition.UNSUPPORTED
    assert not result.resources


@pytest.mark.parametrize(
    "text",
    [
        "module `pkg.native`",
        "class `pkg.native.Target`",
        "method `pkg.native.Target.run`",
    ],
)
def test_ambiguous_module_and_parent_no_promotion(tmp_path: Path, text: str) -> None:
    frame, index = make_frame(
        tmp_path, competing_source="class Target:\n    def run(self): pass\n"
    )
    result = resolve(frame, request(text))
    assert result.disposition is ResolutionDisposition.AMBIGUOUS
    assert not result.resources
    lexical = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="target"),
        index=index,
        maximum_results=3,
    )
    view = present(
        frame=frame,
        lane=result.request.association.lane,
        lexical=lexical,
        global_safety=lexical,
        resolutions=(result,),
        provenance=result.request.hint.provenance,
    )
    assert all(e.exact is None for e in view.exact_first)
    assert (
        tuple(e.lexical_result_reference for e in view.exact_first) == lexical.matches
    )


def test_two_exact_resources_order_and_forged_promotion(
    native: tuple[ExactFrame, RepositoryTextLexicalInvertedIndex],
) -> None:
    frame, index = native
    text = "file `src/pkg/native.py` then file `docs/notes.md`"
    hints = [
        d.observation
        for d in extract(LocalizationTaskIdentity("fixture-two-hints"), text)
        if d.observation
    ]
    routes = tuple(
        resolve(
            frame,
            admit(
                h,
                HintAssociation(
                    h.identity,
                    LocalizationObligationIdentity(h.task, "owner"),
                    "Task order",
                    h.provenance,
                ),
            ),
        )
        for h in hints
    )
    lexical = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="noise target"),
        index=index,
        maximum_results=2,
    )
    view = present(
        frame=frame,
        lane=routes[0].request.association.lane,
        lexical=lexical,
        global_safety=lexical,
        resolutions=routes[::-1],
        provenance=hints[0].provenance,
    )
    assert [e.resource.address.value for e in view.exact_first] == [
        "src/pkg/native.py",
        "docs/notes.md",
    ]
    assert [e.exact.exact_tier_position for e in view.exact_first if e.exact] == [1, 2]
    forged = replace(routes[0], resources=routes[1].resources)
    with pytest.raises(ValueError, match="native referent"):
        present(
            frame=frame,
            lane=routes[0].request.association.lane,
            lexical=lexical,
            global_safety=lexical,
            resolutions=(forged,),
            provenance=hints[0].provenance,
        )


def test_stale_foreign_frames(
    native: tuple[ExactFrame, RepositoryTextLexicalInvertedIndex],
) -> None:
    frame, _ = native
    for invalid in (
        replace(frame, snapshot_id=RepositorySnapshotId("a" * 64)),
        replace(
            frame,
            repository_id=RepositoryId.parse("00000000-0000-0000-0000-000000000072"),
        ),
        replace(
            frame,
            snapshot=replace(
                frame.snapshot,
                resources=(*frame.snapshot.resources, frame.snapshot.resources[0]),
            ),
        ),
        replace(
            frame,
            modules=replace(
                frame.modules,
                interpretations=(
                    replace(
                        frame.modules.interpretations[0], dotted_name="fabricated.name"
                    ),
                ),
            ),
        ),
    ):
        with pytest.raises(ValueError):
            resolve(invalid, request("class `pkg.native.Target`"))


def test_exact_first_complete_native_preservation(
    native: tuple[ExactFrame, RepositoryTextLexicalInvertedIndex],
) -> None:
    frame, index = native
    lexical = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="noise"),
        index=index,
        maximum_results=2,
    )
    safety = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="target noise"),
        index=index,
        maximum_results=2,
    )
    routes = tuple(
        resolve(frame, request(text))
        for text in (
            "class `pkg.native.Target`",
            "file `src/pkg/native.py`",
            "class `Unknown`",
            "file `src/absent.py`",
        )
    )
    view = present(
        frame=frame,
        lane=routes[0].request.association.lane,
        lexical=lexical,
        global_safety=safety,
        resolutions=routes,
        provenance=routes[0].request.hint.provenance,
    )
    assert view.original_lexical_acquisition is lexical
    assert view.global_lexical_safety_lane is safety
    assert len(view.exact_first) == 2
    first = view.exact_first[0]
    assert first.resource.address.value == "src/pkg/native.py"
    assert first.exact is not None
    assert first.exact.exact_tier_position == 1
    assert first.native_lexical_rank is None
    assert first.lexical_result_reference is None
    assert view.exact_first[1].lexical_result_reference is lexical.matches[0]
    assert view.exact_first[1].native_lexical_rank == 1
    assert {e.resource.address for e in view.exact_first} >= {
        m.document_statistics.analysis.document.resource.address
        for m in lexical.matches
    }
    assert view.exact_resolutions == routes
    assert encode(view) == encode(view)
    # Positive exact target keeps the same native match object/rank/score/contributions.
    positive = present(
        frame=frame,
        lane=routes[0].request.association.lane,
        lexical=safety,
        global_safety=safety,
        resolutions=routes,
        provenance=routes[0].request.hint.provenance,
    )
    for entry in positive.exact_first:
        if entry.lexical_result_reference:
            assert entry.native_lexical_rank is not None
            assert (
                entry.lexical_result_reference
                is safety.matches[entry.native_lexical_rank - 1]
            )
    with pytest.raises(ValueError):
        present(
            frame=frame,
            lane=LocalizationObligationIdentity(routes[0].request.hint.task, "foreign"),
            lexical=lexical,
            global_safety=safety,
            resolutions=routes,
            provenance=routes[0].request.hint.provenance,
        )
    with pytest.raises(ValueError):
        present(
            frame=frame,
            lane=routes[0].request.association.lane,
            lexical=replace(lexical, maximum_results=1),
            global_safety=safety,
            resolutions=routes,
            provenance=routes[0].request.hint.provenance,
        )

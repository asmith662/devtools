# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- formatter owns commas; bounded experiment validation
"""Exact-first presentation of complete native lanes without fusion or reranking."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context.localization.grounding.contract import AnchorGroundingDisposition
from devtools.context.repository.resource import RepositoryResourceOccurrence
from experiments.exact_hint_routing.models import (
    ExactFirstCandidate,
    ExactHintRoutingView,
    PresentationEntry,
    ResolutionDisposition,
)
from experiments.exact_hint_routing.routing import admit

if TYPE_CHECKING:
    from devtools.context.localization.identity import (
        LocalizationObligationIdentity,
        TaskProvenance,
    )
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25RetrievalResult,
    )
    from experiments.exact_hint_routing.models import (
        ExactHintResolution,
        GlobalTaskLane,
    )
    from experiments.exact_hint_routing.routing import ExactFrame


def _validate_lane(
    frame: ExactFrame, lane: RepositoryTextLexicalBm25RetrievalResult
) -> None:
    collection = lane.index.corpus_statistics.collection_analysis.document_collection
    if tuple(
        d.resource for d in collection.documents
    ) != frame.snapshot.resources or any(
        d.repository_id != frame.repository_id for d in collection.documents
    ):
        raise ValueError("Lexical lane differs from frozen frame")
    if lane.maximum_results < len(collection.documents):
        raise ValueError("Lexical lane truncated by candidate limit")
    resources = [m.document_statistics.analysis.document.resource for m in lane.matches]
    if len({r.address for r in resources}) != len(resources):
        raise ValueError("Native lexical lane repeats resources")
    if any(frame.snapshot.resource_at(r.address) != r for r in resources):
        raise ValueError("Stale or foreign lexical occurrence")


def present(  # noqa: C901, PLR0912, PLR0913 -- explicit lane/frame/provenance inputs and bounded order
    *,
    frame: ExactFrame,
    lane: LocalizationObligationIdentity | GlobalTaskLane,
    lexical: RepositoryTextLexicalBm25RetrievalResult,
    global_safety: RepositoryTextLexicalBm25RetrievalResult,
    resolutions: tuple[ExactHintResolution, ...],
    provenance: TaskProvenance,
) -> ExactHintRoutingView:
    """Promote resolved native resources and append every remaining positive row."""
    frame.validate()
    _validate_lane(frame, lexical)
    _validate_lane(frame, global_safety)
    ranked = {
        m.document_statistics.analysis.document.resource.address: (rank, m)
        for rank, m in enumerate(lexical.matches, 1)
    }
    for result in resolutions:
        if result.request != admit(result.request.hint, result.request.association):
            raise ValueError("Unadmitted resolution request")
        if (
            result.request.association.lane != lane
            or result.frame_identity != frame.identity
        ):
            raise ValueError("Resolution lane/frame differs")
        if (
            result.repository_id != frame.repository_id
            or result.snapshot_id != frame.snapshot_id
        ):
            raise ValueError("Foreign/stale resolution")
        if any(frame.snapshot.resource_at(r.address) != r for r in result.resources):
            raise ValueError("Resolution resource differs")
        if result.disposition is ResolutionDisposition.RESOLVED:
            account = result.native_provenance[-1]
            if account.disposition is not AnchorGroundingDisposition.RESOLVED:
                raise ValueError("Promoted result lacks resolved native provenance")
            if (
                account.request.repository_id != frame.repository_id
                or account.request.snapshot_id != frame.snapshot_id
                or account.request.task != result.request.hint.task
                or account.request.anchor.value != result.request.hint.identity.value
            ):
                raise ValueError("Native provenance differs from route/frame")
            referent = account.candidates[0].referent
            owner = (
                referent
                if isinstance(referent, RepositoryResourceOccurrence)
                else referent.resource
                if hasattr(referent, "resource")
                else frame.snapshot.resource_at(referent.support.resource_address)
            )
            if result.resources != (owner,):
                raise ValueError("Promoted resource differs from native referent")
    ordered = sorted(
        resolutions,
        key=lambda r: (
            r.request.hint.span.start,
            r.request.hint.span.end,
            r.request.identity,
        ),
    )
    entries: list[PresentationEntry] = []
    seen = set()
    for result in ordered:
        if result.disposition is not ResolutionDisposition.RESOLVED:
            continue
        for resource in sorted(
            result.resources, key=lambda r: (str(r.address), str(r.content_identity))
        ):
            if resource.address in seen:
                continue
            seen.add(resource.address)
            rank, match = ranked.get(resource.address, (None, None))
            candidate = ExactFirstCandidate(
                resource, result.request.hint, result, len(entries) + 1, rank, match
            )
            entries.append(
                PresentationEntry(resource, len(entries) + 1, candidate, rank, match)
            )
    for rank, match in enumerate(lexical.matches, 1):
        resource = match.document_statistics.analysis.document.resource
        if resource.address not in seen:
            seen.add(resource.address)
            entries.append(
                PresentationEntry(resource, len(entries) + 1, None, rank, match)
            )
    return ExactHintRoutingView(
        lane, lexical, resolutions, tuple(entries), global_safety, provenance
    )

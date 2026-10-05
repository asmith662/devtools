# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Generic human-only artifact roundtrips and strict provenance/budget guards."""

from __future__ import annotations

import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.localization import TaskProvenance
from devtools.context.localization.generation import (
    ProjectionKind,
    WitnessGenerationPlan,
    generate_witness_hypotheses,
)
from devtools.context.localization.grounding import ResourceAddressLocator
from devtools.context.localization.resolution import (
    HypothesisResolutionDisposition as H,
)
from devtools.context.localization.resolution import (
    MemberResolutionDisposition as M,
)
from devtools.context.localization.resolution import (
    WitnessResolutionView,
)
from devtools.context.repository.resource import ContentIdentity
from devtools.context.repository.resource import RepositoryResourceAddress as Address
from devtools.core.paths import resolve_path
from experiments.codex_dogfood.semantic_resolution import (
    AbstentionReason,
    ContentBounds,
    ContentCitation,
    FrozenContentSlice,
    ProducerKind,
    ProducerProvenance,
    ReviewDecision,
    SemanticArgument,
    SemanticDecisionBatch,
    SemanticDecisionLedger,
    SemanticDecisionRequest,
    SemanticMemberClaim,
    SemanticPolicyIdentity,
    SemanticResolutionProposal,
    SemanticResolutionReview,
    freeze,
    materialize_accepted_resolution,
    parse_proposal,
    proposal_payload,
    replay,
    serialize,
)
from experiments.codex_dogfood.semantic_resolution._identity import digest, text_digest
from tests.context.localization.association.test_hypothesis import (
    _frame,
    _hypothesis,
    _member,
    _view,
)
from tests.context.localization.generation.test_generation import (
    _frame as _structural_frame,
)
from tests.context.localization.generation.test_generation import (
    _ground,
    _recipe,
)
from tests.context.localization.generation.test_generation import (
    _member as _recipe_member,
)
from tests.context.localization.generation.test_imports import (
    _fixture as _import_fixture,
)
from tests.context.localization.generation.test_imports import _run as _import_run
from tests.context.localization.generation.test_references import (
    _fixture as _reference_fixture,
)
from tests.context.localization.generation.test_references import _run as _reference_run

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.localization.association import CandidateWitnessView


def _policy() -> SemanticPolicyIdentity:
    return SemanticPolicyIdentity(
        "explicit-human-pilot",
        "1",
        "caller-selected",
        "1",
        text_digest("no model; caller authors all proposals"),
    )


def _request(
    candidates: CandidateWitnessView | None = None,
    index: int = 0,
    member_index: int = 0,
) -> SemanticDecisionRequest:
    if candidates is None:
        frame = _frame()
        candidates = _view(frame, _hypothesis(frame))
    hypothesis = candidates.hypotheses[index]
    member = hypothesis.members[member_index]
    claim = SemanticMemberClaim(
        "contract",
        candidates.task.identity,
        hypothesis.identity.obligation,
        hypothesis.identity,
        member.target,
        "The disclosed resource establishes the named caller contract",
        "Caller selects a plausible unresolved witness",
        TaskProvenance("generic-task"),
    )
    content = FrozenContentSlice.select(member.target, 0, len(member.target.content))
    return SemanticDecisionRequest(
        _policy(),
        candidates,
        hypothesis,
        member,
        claim,
        ContentBounds(1, 4, 10000),
        (content,),
    )


def _proposal(
    request: SemanticDecisionRequest, disposition: M = M.SUPPORTED
) -> SemanticResolutionProposal:
    return SemanticResolutionProposal(
        request,
        disposition,
        "Explicit inspection rationale",
        ProducerProvenance(
            ProducerKind.HUMAN,
            "fixture-author",
            TaskProvenance("proposal-source"),
            request.identity,
        ),
        (ContentCitation(request.identity, request.disclosures[0]),),
        (request.supports[0],),
        SemanticArgument(
            "The cited text declares the contract",
            "That contract establishes the requested member claim",
        ),
        AbstentionReason.CAPABILITY_LIMIT if disposition is M.ABSTAINED else None,
    )


def _review(
    proposal: SemanticResolutionProposal,
    decision: ReviewDecision = ReviewDecision.ACCEPT,
) -> SemanticResolutionReview:
    return SemanticResolutionReview(
        proposal.identity,
        "human-reviewer",
        TaskProvenance("review-source"),
        decision,
        "I reviewed the claim, criterion and disclosed evidence",
    )


@pytest.mark.parametrize("disposition", [M.SUPPORTED, M.UNRESOLVED, M.ABSTAINED])
def test_human_roundtrip_and_explicit_materialization(disposition: M) -> None:
    request = _request()
    proposal = _proposal(request, disposition)
    parsed = parse_proposal(json.dumps(proposal_payload(proposal)), request)
    assert parsed == proposal
    assert parsed.identity == proposal.identity
    with pytest.raises(ValueError, match="ACCEPT review"):
        materialize_accepted_resolution(request, proposal, None, request.candidates)
    with pytest.raises(ValueError, match="ACCEPT review"):
        materialize_accepted_resolution(
            request,
            proposal,
            _review(proposal, ReviewDecision.REJECT),
            request.candidates,
        )
    review = _review(proposal)
    result = materialize_accepted_resolution(
        request, proposal, review, request.candidates
    )
    assert result.disposition is disposition
    assert result.member is request.member
    assert result.criterion is request.criterion
    assert result.claim == request.claim.statement
    assert result.basis[0].identity is request.supports[0].support
    assert result.provenance.source_identity == (
        "semantic-resolution-v1",
        request.identity,
        proposal.identity,
        review.identity,
    )
    assert all(
        not isinstance(reference.identity, ContentCitation)
        for reference in result.basis
    )
    assert (
        WitnessResolutionView(request.candidates).for_hypothesis(
            request.hypothesis.identity
        )
        is None
    )
    assert not hasattr(result, "readiness")
    assert not hasattr(result, "promoted_witness")
    if disposition is not M.SUPPORTED:
        empty = replace(proposal, citations=(), support_references=(), argument=None)
        resolution = materialize_accepted_resolution(
            request, empty, _review(empty), request.candidates
        )
        assert resolution.basis == ()


def test_content_bounds_offsets_and_canonical_disclosures() -> None:
    request = _request()
    content = request.member.target
    first = FrozenContentSlice.select(content, 0, 4)
    second = FrozenContentSlice.select(content, 4, 9)
    left = replace(request, disclosures=(second, first))
    right = replace(request, disclosures=(first, second))
    assert left.identity == right.identity
    assert serialize(left) == serialize(right)
    assert left.content_cost == (1, 2, 9)
    assert request.content_cost[2] == len(content.content.encode("utf-8"))
    for bounds in (
        ContentBounds(0, 4, 10000),
        ContentBounds(1, 1, 10000),
        ContentBounds(1, 4, 8),
    ):
        with pytest.raises(ValueError, match="exceeds"):
            replace(left, bounds=bounds)
    with pytest.raises(ValueError, match="repeats a disclosure"):
        replace(request, disclosures=(first, first))
    with pytest.raises(ValueError, match="exact member target"):
        replace(
            request, disclosures=(FrozenContentSlice.select(replace(content), 0, 4),)
        )
    empty = replace(request, disclosures=(), bounds=ContentBounds(0, 0, 0))
    assert empty.content_cost == (0, 0, 0)
    unicode_resource = replace(
        content,
        content="\u03b1🙂z",
        content_identity=ContentIdentity(text_digest("\u03b1🙂z")),
    )
    assert FrozenContentSlice.select(unicode_resource, 0, 2).utf8_bytes == 6
    for start, end in ((-1, 2), (0, 0), (3, 1), (0, 10000)):
        with pytest.raises(ValueError, match="offsets"):
            FrozenContentSlice.select(content, start, end)
    with pytest.raises(ValueError, match="excerpt digest"):
        replace(first, excerpt_digest="f" * 64)
    with pytest.raises(ValueError, match="exact member target"):
        replace(
            request,
            disclosures=(
                FrozenContentSlice.select(
                    replace(content, content_identity=ContentIdentity("f" * 64)), 0, 4
                ),
            ),
        )
    with pytest.raises(ValueError, match="nonnegative integers"):
        ContentBounds(max_resources=True, max_excerpts=1, max_utf8_bytes=1)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("disposition", "contradicted"),
        ("disposition", "unknown"),
        ("reason", ""),
        ("request_id", "foreign"),
        ("claim_id", "foreign"),
        ("policy_id", "foreign"),
        ("criterion", {"name": "other", "statement": "other"}),
        ("scope", {}),
        ("argument", None),
        ("support_keys", ["forged"]),
        ("citations", []),
        ("unexpected", "value"),
    ],
)
def test_strict_proposal_parser_rejects_invalid_fields(
    field: str, value: object
) -> None:
    request = _request()
    payload = proposal_payload(_proposal(request))
    payload[field] = value
    with pytest.raises(ValueError):  # noqa: PT011 - several independently valid rejection paths
        parse_proposal(json.dumps(payload), request)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("resource", "foreign.py"),
        ("content_identity", "f" * 64),
        ("start", -1),
        ("end", 100000),
        ("start", True),
        ("excerpt_digest", "f" * 64),
        ("request_id", "foreign"),
    ],
)
def test_parser_rejects_foreign_or_hallucinated_citations(
    field: str, value: object
) -> None:
    request = _request()
    payload = proposal_payload(_proposal(request))
    citations = payload["citations"]
    assert isinstance(citations, list)
    citations[0][field] = value
    with pytest.raises(ValueError):  # noqa: PT011 - citation errors vary by invalid field
        parse_proposal(json.dumps(payload), request)


def test_undisclosed_and_other_request_evidence_rejected() -> None:
    request = _request()
    shortened = replace(
        request, disclosures=(FrozenContentSlice.select(request.member.target, 0, 4),)
    )
    proposal = _proposal(shortened)
    with pytest.raises(ValueError, match="not disclosed"):
        replace(
            proposal,
            citations=(ContentCitation(shortened.identity, request.disclosures[0]),),
        )
    with pytest.raises(ValueError, match="not disclosed"):
        replace(
            proposal,
            citations=(ContentCitation(request.identity, shortened.disclosures[0]),),
        )
    with pytest.raises(ValueError, match="attached request"):
        replace(proposal, support_references=request.supports)
    copied = replace(request.supports[0], support=replace(request.member.lexical[0]))
    with pytest.raises(ValueError, match="attached request"):
        replace(_proposal(request), support_references=(copied,))
    with pytest.raises(ValueError, match="repeats"):
        replace(proposal, citations=(*proposal.citations, *proposal.citations))
    with pytest.raises(ValueError, match="capability reason"):
        replace(proposal, disposition=M.ABSTAINED)
    with pytest.raises(ValueError, match="exclude contradiction"):
        replace(proposal, disposition=M.CONTRADICTED)
    with pytest.raises(ValueError, match="Duplicate JSON"):
        parse_proposal('{"schema":"x","schema":"y"}', request)


def test_frame_review_and_producer_guards() -> None:
    request = _request()
    proposal = _proposal(request)
    with pytest.raises(ValueError, match="foreign or stale"):
        replace(request, hypothesis=replace(request.hypothesis))
    with pytest.raises(ValueError, match="foreign or stale"):
        replace(request, member=replace(request.member))
    with pytest.raises(ValueError, match="exact candidate/member"):
        replace(
            request, claim=replace(request.claim, target=replace(request.member.target))
        )
    with pytest.raises(ValueError, match="exact request"):
        materialize_accepted_resolution(
            request, proposal, _review(proposal), replace(request.candidates)
        )
    with pytest.raises(ValueError, match="ACCEPT review"):
        materialize_accepted_resolution(
            request,
            proposal,
            replace(_review(proposal), proposal_id="foreign"),
            request.candidates,
        )
    with pytest.raises(TypeError, match="Malformed human"):
        replace(_review(proposal), decision="accept")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="nonblank"):
        replace(_review(proposal), reviewer="")
    with pytest.raises(ValueError, match="model provenance"):
        replace(proposal.producer, model="unexpected")
    with pytest.raises(ValueError, match="model/provider"):
        replace(proposal.producer, kind=ProducerKind.EXTERNAL_MODEL)
    with pytest.raises(ValueError, match="input digest"):
        replace(
            proposal,
            producer=replace(proposal.producer, input_request_digest="foreign"),
        )
    with pytest.raises(ValueError, match="policy schema"):
        replace(request.policy, instruction_digest="invalid")


def test_batch_absence_reporting_and_serialization(tmp_path: Path) -> None:
    frame = _frame()
    candidates = _view(frame, _hypothesis(frame), _hypothesis(frame, key="competitor"))
    first, second = _request(candidates), _request(candidates, 1)
    batch = SemanticDecisionBatch(
        _policy(),
        candidates,
        (second, first),
        "Caller-frozen inclusion; recall not measured",
        TaskProvenance("batch-author"),
    )
    assert batch.identity == replace(batch, requests=(first, second)).identity
    assert batch.disclosed_utf8_bytes == first.content_cost[2] + second.content_cost[2]
    ledger = SemanticDecisionLedger(batch)
    assert ledger.unprocessed == batch.requests
    proposal = _proposal(first)
    unreviewed = replace(ledger, proposals=(proposal,))
    assert unreviewed.report()["unreviewed"] == 1
    accepted = replace(unreviewed, reviews=(_review(proposal),))
    assert accepted.report()["materialized_dispositions"] == []
    materialized = materialize_accepted_resolution(
        first, proposal, _review(proposal), candidates
    )
    assert accepted.report((materialized,))["materialized_dispositions"] == [
        "supported"
    ]
    assert accepted.unprocessed == (second,)
    assert len(candidates.hypotheses) == 2
    for value in (batch, first, proposal, _review(proposal), accepted):
        path = resolve_path(tmp_path / f"{type(value).__name__}.json")
        freeze(path, value)
        replay(path, value)
        with pytest.raises(FileExistsError):
            freeze(path, value)
        assert serialize(value) == serialize(value)
    with pytest.raises(ValueError, match="repeats"):
        replace(accepted, proposals=(proposal, proposal))
    with pytest.raises(ValueError, match="repeats"):
        replace(accepted, reviews=(_review(proposal), _review(proposal)))
    with pytest.raises(ValueError, match="repeats"):
        replace(batch, requests=(first, first))


def test_complementary_members_resolve_independently() -> None:
    frame = _frame()
    hypothesis = _hypothesis(
        frame, members=(_member(frame), _member(frame, "docs/alpha.md"))
    )
    candidates = _view(frame, hypothesis)
    first, second = _request(candidates), _request(candidates, member_index=1)
    proposal = _proposal(first)
    record = materialize_accepted_resolution(
        first, proposal, _review(proposal), candidates
    )
    partial = WitnessResolutionView(candidates, (record,))
    assert partial.unresolved[0].disposition is H.UNRESOLVED
    assert partial.for_member(hypothesis.identity, second.member.target) is None
    assert len(hypothesis.members) == 2


@pytest.mark.parametrize("channel", ["owner", "mirror", "reference", "import"])
def test_native_structural_support_channels(tmp_path: Path, channel: str) -> None:
    if channel in {"owner", "mirror"}:
        task, snapshot = _structural_frame()
        grounding = _ground(
            task, snapshot, ResourceAddressLocator(Address("src/devtools/alpha.py"))
        )
        generated = generate_witness_hypotheses(
            WitnessGenerationPlan(
                task,
                snapshot,
                (
                    _recipe(
                        task,
                        _recipe_member(
                            grounding,
                            projection=ProjectionKind.OWNER_RESOURCE
                            if channel == "owner"
                            else ProjectionKind.MIRRORED_RESOURCE,
                        ),
                    ),
                ),
            )
        )
    elif channel == "reference":
        generated = _reference_run(_reference_fixture(tmp_path))
    else:
        generated = _import_run(_import_fixture(tmp_path))
    request = _request(generated.association)
    assert json.loads(serialize(request))["payload"]["native_supports"]
    proposal = parse_proposal(json.dumps(proposal_payload(_proposal(request))), request)
    result = materialize_accepted_resolution(
        request, proposal, _review(proposal), request.candidates
    )
    assert result.basis[0].identity is request.member.structural[0]
    assert result.hypothesis.identity == request.hypothesis.identity
    assert digest(request.candidates)
    if len(request.candidates.hypotheses) > 1:
        sibling = _request(request.candidates, index=1)
        with pytest.raises(ValueError, match="attached request"):
            replace(proposal, support_references=sibling.supports)
        assert (
            WitnessResolutionView(request.candidates).for_hypothesis(
                sibling.hypothesis.identity
            )
            is None
        )


def test_proposal_evidence_order_is_semantically_stable() -> None:
    frame = _frame()
    candidates = _view(
        frame, _hypothesis(frame, members=(_member(frame, role=True, routed=True),))
    )
    request = _request(candidates)
    first = FrozenContentSlice.select(request.member.target, 0, 4)
    second = FrozenContentSlice.select(request.member.target, 4, 9)
    request = replace(request, disclosures=(first, second))
    proposal = replace(
        _proposal(request),
        citations=tuple(
            ContentCitation(request.identity, s) for s in request.disclosures
        ),
        support_references=request.supports,
    )
    reversed_proposal = replace(
        proposal,
        citations=tuple(reversed(proposal.citations)),
        support_references=tuple(reversed(proposal.support_references)),
    )
    assert reversed_proposal.identity == proposal.identity
    assert serialize(reversed_proposal) == serialize(proposal)


def test_role_routed_context_and_future_producer_metadata() -> None:
    frame = _frame()
    rich = _hypothesis(frame, members=(_member(frame, role=True, routed=True),))
    request = _request(_view(frame, rich))
    payload = json.loads(serialize(request))["payload"]
    assert {s["channel"] for s in payload["native_supports"]} == {
        "lexical",
        "roles",
        "routed",
    }
    assert payload["disclosures"][0]["text"] == request.member.target.content
    proposal = _proposal(request)
    producer = replace(
        proposal.producer,
        kind=ProducerKind.EXTERNAL_MODEL,
        model="fixture-model",
        provider="fixture-provider",
        runtime="fixture-runtime",
        configuration="fixture-settings",
    )
    modeled = replace(proposal, producer=producer)
    assert parse_proposal(json.dumps(proposal_payload(modeled)), request) == modeled
    with pytest.raises(TypeError, match="source artifact"):
        replace(_review(proposal), provenance=TaskProvenance(None))
    with pytest.raises(ValueError, match="Malformed producer"):
        replace(producer, source=TaskProvenance(None))


def test_replay_detects_tampering_and_frame_changes(tmp_path: Path) -> None:
    request = _request()
    path = resolve_path(tmp_path / "request.json")
    freeze(path, request)
    # Controlled corrupt archive fixture; no retained experiment is read or changed.
    data = path.value.read_bytes()
    path.value.write_bytes(
        data.replace(b'"semantic-resolution-v1"', b'"semantic-resolution-v0"')
    )
    with pytest.raises(ValueError, match="digest/bytes"):
        replay(path, request)
    frame = request.candidates
    with pytest.raises(ValueError, match="association frame"):
        replace(
            request,
            candidates=replace(
                frame,
                snapshot=replace(frame.snapshot, id=type(frame.snapshot.id)("b" * 64)),
            ),
        )


def test_ledger_foreign_proposals_reviews_and_recording_guards() -> None:
    request = _request()
    batch = SemanticDecisionBatch(
        _policy(),
        request.candidates,
        (request,),
        "caller inclusion",
        TaskProvenance("batch"),
    )
    proposal = _proposal(request)
    ledger = SemanticDecisionLedger(batch, (proposal,), (_review(proposal),))
    record = materialize_accepted_resolution(
        request, proposal, _review(proposal), request.candidates
    )
    with pytest.raises(ValueError, match="repeats a materialization"):
        ledger.report((record, record))
    with pytest.raises(ValueError, match="differs"):
        ledger.report((replace(record, reason="altered reason"),))
    with pytest.raises(ValueError, match="foreign/unreviewed"):
        ledger.report((replace(record, provenance=TaskProvenance("foreign")),))
    with pytest.raises(ValueError, match="foreign proposal"):
        replace(ledger, reviews=(replace(_review(proposal), proposal_id="foreign"),))
    with pytest.raises(ValueError, match="foreign request"):
        replace(ledger, proposals=(_proposal(_request()),))
    with pytest.raises(ValueError, match="one exact candidate"):
        replace(batch, candidates=replace(request.candidates))
    body = proposal_payload(proposal)
    del body["reason"]
    with pytest.raises(ValueError, match="Malformed proposal"):
        parse_proposal(json.dumps(body), request)

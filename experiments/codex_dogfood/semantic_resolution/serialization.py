# Copyright (c) 2026
# ruff: noqa: COM812
"""Strict proposals and deterministic artifacts over retained native context."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import TYPE_CHECKING

from devtools.context.localization.association import (
    LexicalMatchSupport,
    MirroredResourceSupport,
    OwnerResourceSupport,
    PythonImportDependencyResourceSupport,
    PythonReferenceResourceSupport,
    RoutedMatchSupport,
)
from devtools.context.localization.identity import TaskProvenance
from devtools.context.localization.resolution import MemberResolutionDisposition
from devtools.context.localization.roles.models import ResourceRoleEvidence
from devtools.resources.filesystem import FileFormat, TextFile, read, write
from experiments.codex_dogfood.semantic_resolution._identity import (
    canonical,
    digest,
    json_digest,
    native_descriptor,
)
from experiments.codex_dogfood.semantic_resolution.citations import (
    ContentCitation,
    FrozenContentSlice,
)
from experiments.codex_dogfood.semantic_resolution.contract import (
    SCHEMA,
    AbstentionReason,
    NativeSupportReference,
    ProducerKind,
    ProducerProvenance,
    SemanticArgument,
    SemanticDecisionBatch,
    SemanticDecisionRequest,
    SemanticResolutionProposal,
)
from experiments.codex_dogfood.semantic_resolution.review import (
    SemanticDecisionLedger,
    SemanticResolutionReview,
)

if TYPE_CHECKING:
    from devtools.core.paths import ResolvedPath

type Artifact = (
    SemanticDecisionBatch
    | SemanticDecisionRequest
    | SemanticResolutionProposal
    | SemanticResolutionReview
    | SemanticDecisionLedger
)


def _scope(request: SemanticDecisionRequest) -> dict[str, object]:
    return {
        "task": request.claim.task.value,
        "obligation": request.claim.obligation.value,
        "hypothesis": request.hypothesis.identity.value,
        "hypothesis_type": type(request.hypothesis.identity).__name__,
        "resource": request.member.target.address.value,
        "content_identity": request.member.target.content_identity.value,
        "repository": str(request.candidates.snapshot.repository_id),
        "snapshot": request.candidates.snapshot.id.value,
        "candidate_frame": request.candidate_frame_digest,
    }


def _slice(content: FrozenContentSlice) -> dict[str, object]:
    return {
        "resource": content.resource.address.value,
        "content_identity": content.resource.content_identity.value,
        "start": content.start,
        "end": content.end,
        "excerpt_digest": content.excerpt_digest,
    }


def _support(reference: NativeSupportReference) -> dict[str, object]:
    """Expose exact native observations without dumping nested undisclosed content."""
    support = reference.support
    data: dict[str, object] = {
        "key": reference.key,
        "channel": reference.channel,
        "type": type(support).__name__,
        "native_digest": digest(support),
    }
    if isinstance(support, LexicalMatchSupport):
        data["observation"] = {
            "query": None if support.query is None else support.query.value,
            "native_rank": support.native_rank,
            "matched_content_terms": [
                c.normalized_term for c in support.match.term_contributions
            ],
            "matched_filename_terms": [
                c.normalized_term for c in support.match.filename_term_contributions
            ],
        }
    elif isinstance(support, RoutedMatchSupport):
        data["observation"] = {
            "query": support.query.value,
            "tier": support.candidate.tier.value,
            "native_rank": support.candidate.native_rank,
            "routed_position": support.candidate.routed_position,
            "role_evidence": [r.identity for r in support.candidate.role_evidence],
        }
    elif isinstance(support, ResourceRoleEvidence):
        data["observation"] = {
            "role": support.role.value,
            "supports": [
                {
                    "kind": s.kind.value,
                    "source": s.source_address.value,
                    "native_identities": s.native_identities,
                    "observation": s.observation,
                }
                for s in support.supports
            ],
        }
    elif isinstance(
        support,
        (
            OwnerResourceSupport,
            MirroredResourceSupport,
            PythonReferenceResourceSupport,
            PythonImportDependencyResourceSupport,
        ),
    ):
        data["grounding"] = {
            "anchor": support.grounding.request.anchor.value,
            "locator_digest": digest(support.grounding.request.locator),
            "referent_digest": digest(support.grounding.candidates[0].referent),
            "resolver": support.grounding.resolver.value,
            "referent_type": type(support.grounding.candidates[0].referent).__name__,
            "declared_name": getattr(
                support.grounding.candidates[0].referent, "declared_name", None
            ),
        }
        if isinstance(support, MirroredResourceSupport):
            data["observation"] = {
                "source": support.correspondence.source.address.value,
                "test": support.correspondence.test.address.value,
                "correspondence": support.correspondence.identity,
            }
        elif isinstance(support, PythonReferenceResourceSupport):
            data["observation"] = {
                "reference_ids": [r.identity for r in support.references],
                "subject": digest(support.grounding.candidates[0].referent),
                "references": [
                    {
                        "identity": r.identity,
                        "target_declaration": r.target_declaration.identity,
                        "target_name": r.target_declaration.declared_name,
                        "resource": r.occurrence.resource_address.value,
                        "source_range": asdict(r.occurrence.source_range),
                        "route": r.route.value,
                        "direct_call_syntax": r.direct_call,
                    }
                    for r in support.references
                ],
            }
        elif isinstance(support, PythonImportDependencyResourceSupport):
            data["observation"] = {
                "relations": [
                    {
                        "identity": r.identity,
                        "source_module": r.source.identity,
                        "target_module": r.target.identity,
                        "declaration_digest": digest(r.declaration),
                    }
                    for r in support.relations
                ]
            }
        else:
            data["observation"] = "Exact native referent owner is the member target."
    else:
        msg = "Unsupported native support presentation."
        raise TypeError(msg)
    return data


def proposal_payload(proposal: SemanticResolutionProposal) -> dict[str, object]:
    """Expose strict future producer schema, with no automatic interpretation."""
    producer = proposal.producer
    return {
        "schema": SCHEMA,
        "request_id": proposal.request.identity,
        "scope": _scope(proposal.request),
        "claim_id": proposal.request.claim.identity,
        "criterion": asdict(proposal.request.criterion),
        "policy_id": proposal.request.policy.identity,
        "disposition": proposal.disposition.value,
        "reason": proposal.reason,
        "argument": None if proposal.argument is None else asdict(proposal.argument),
        "abstention": None
        if proposal.abstention is None
        else proposal.abstention.value,
        "citations": [
            {"request_id": c.request_id, **_slice(c.content)}
            for c in proposal.citations
        ],
        "support_keys": [s.key for s in proposal.support_references],
        "producer": {
            "kind": producer.kind.value,
            "identity": producer.identity,
            "source_identity": producer.source.source_identity,
            "source_explanation": producer.source.explanation,
            "input_request_digest": producer.input_request_digest,
            "model": producer.model,
            "provider": producer.provider,
            "runtime": producer.runtime,
            "configuration": producer.configuration,
        },
    }


def _request_payload(request: SemanticDecisionRequest) -> dict[str, object]:
    return {
        "scope": _scope(request),
        "policy": asdict(request.policy),
        "claim": {
            "identity": request.claim.identity,
            "key": request.claim.key,
            "statement": request.claim.statement,
            "reason": request.claim.reason,
            "provenance": native_descriptor(request.claim.provenance),
        },
        "criterion": asdict(request.criterion),
        "predicate": next(
            o.predicate
            for o in request.candidates.task.obligations
            if o.identity == request.claim.obligation
        ),
        "applicability_condition": next(
            o.applicability_condition
            for o in request.candidates.task.obligations
            if o.identity == request.claim.obligation
        ),
        "bounds": asdict(request.bounds),
        "content_cost": request.content_cost,
        "disclosures": [{**_slice(s), "text": s.text} for s in request.disclosures],
        "native_supports": [_support(s) for s in request.supports],
        "support_semantics": (
            "Proposal provenance, not votes or semantic proof; "
            "inspect retained native objects."
        ),
    }


def _payload(value: Artifact) -> dict[str, object]:
    if isinstance(value, SemanticDecisionRequest):
        return _request_payload(value)
    if isinstance(value, SemanticResolutionProposal):
        return proposal_payload(value)
    if isinstance(value, SemanticResolutionReview):
        return {
            "proposal_id": value.proposal_id,
            "reviewer": value.reviewer,
            "provenance": native_descriptor(value.provenance),
            "decision": value.decision.value,
            "reason": value.reason,
        }
    if isinstance(value, SemanticDecisionBatch):
        return {
            "policy": asdict(value.policy),
            "candidate_frame": value.requests[0].candidate_frame_digest,
            "inclusion_reason": value.inclusion_reason,
            "provenance": native_descriptor(value.provenance),
            "requests": [
                {"identity": r.identity, "payload": _request_payload(r)}
                for r in value.requests
            ],
        }
    return {
        "batch_id": value.batch.identity,
        "report": value.report(),
        "proposals": [proposal_payload(p) for p in value.proposals],
        "reviews": [_payload(r) for r in value.reviews],
    }


def serialize(value: Artifact) -> bytes:
    """Emit canonical UTF-8 JSON with payload digest, never pickle or native loading."""
    payload = _payload(value)
    return canonical(
        {
            "schema": SCHEMA,
            "kind": type(value).__name__,
            "artifact_id": value.identity,
            "payload": payload,
            "payload_digest": json_digest(payload),
        }
    )


def freeze(path: ResolvedPath, value: Artifact) -> None:
    """Use the canonical filesystem substrate, refusing existing destinations."""
    data = serialize(value)
    write(TextFile(path, data.decode("utf-8"), byte_size=len(data)), overwrite=False)


def replay(path: ResolvedPath, value: Artifact) -> None:
    """Read-only exact-byte replay with an explicitly supplied retained native frame."""
    expected = serialize(value)
    file = read(path, file_format=FileFormat.TEXT, max_bytes=len(expected))
    if not isinstance(file, TextFile) or file.content.encode("utf-8") != expected:
        msg = "Frozen decision artifact digest/bytes differ from retained context."
        raise ValueError(msg)


def _object(value: object, keys: set[str]) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        msg = "Malformed proposal object: missing or unexpected fields."
        raise ValueError(msg)
    return value


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            msg = "Duplicate JSON proposal field."
            raise ValueError(msg)
        result[key] = value
    return result


def _text(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        msg = "Proposal field requires nonblank text."
        raise ValueError(msg)
    return value


def _optional_text(value: object) -> str | None:
    return None if value is None else _text(value)


def _list(value: object) -> list[object]:
    if not isinstance(value, list):
        msg = "Proposal field requires an array."
        raise ValueError(msg)  # noqa: TRY004 - malformed external schema
    return value


def parse_proposal(
    data: bytes | str, request: SemanticDecisionRequest
) -> SemanticResolutionProposal:
    """Parse an external payload into a validated proposal, never a decision."""
    obj = _object(
        json.loads(data, object_pairs_hook=_pairs),
        {
            "schema",
            "request_id",
            "scope",
            "claim_id",
            "criterion",
            "policy_id",
            "disposition",
            "reason",
            "argument",
            "abstention",
            "citations",
            "support_keys",
            "producer",
        },
    )
    if (
        obj["schema"] != SCHEMA
        or obj["request_id"] != request.identity
        or obj["scope"] != _scope(request)
        or obj["claim_id"] != request.claim.identity
        or obj["criterion"] != asdict(request.criterion)
        or obj["policy_id"] != request.policy.identity
    ):
        msg = "Proposal request, claim, criterion or policy frame mismatch."
        raise ValueError(msg)
    producer = _object(
        obj["producer"],
        {
            "kind",
            "identity",
            "source_identity",
            "source_explanation",
            "input_request_digest",
            "model",
            "provider",
            "runtime",
            "configuration",
        },
    )
    provenance = ProducerProvenance(
        ProducerKind(_text(producer["kind"])),
        _text(producer["identity"]),
        TaskProvenance(
            _text(producer["source_identity"]),
            explanation=_optional_text(producer["source_explanation"]),
        ),
        _text(producer["input_request_digest"]),
        *(
            _optional_text(producer[k])
            for k in ("model", "provider", "runtime", "configuration")
        ),
    )
    citations = []
    for raw in _list(obj["citations"]):
        c = _object(
            raw,
            {
                "request_id",
                "resource",
                "content_identity",
                "start",
                "end",
                "excerpt_digest",
            },
        )
        if (
            c["resource"] != request.member.target.address.value
            or c["content_identity"] != request.member.target.content_identity.value
        ):
            msg = "Proposal cites foreign resource/content identity."
            raise ValueError(msg)
        if type(c["start"]) is not int or type(c["end"]) is not int:
            msg = "Citation offsets must be integer code-point positions."
            raise ValueError(msg)
        citations.append(
            ContentCitation(
                _text(c["request_id"]),
                FrozenContentSlice(
                    request.member.target,
                    c["start"],
                    c["end"],
                    _text(c["excerpt_digest"]),
                ),
            )
        )
    native = {s.key: s for s in request.supports}
    references = []
    for key in _list(obj["support_keys"]):
        handle = _text(key)
        if handle not in native:
            msg = "Unknown or forged native support key."
            raise ValueError(msg)
        references.append(native[handle])
    argument = None
    if obj["argument"] is not None:
        a = _object(obj["argument"], {"observation", "criterion_link"})
        argument = SemanticArgument(_text(a["observation"]), _text(a["criterion_link"]))
    return SemanticResolutionProposal(
        request,
        MemberResolutionDisposition(_text(obj["disposition"])),
        _text(obj["reason"]),
        provenance,
        tuple(citations),
        tuple(references),
        argument,
        None
        if obj["abstention"] is None
        else AbstentionReason(_text(obj["abstention"])),
    )

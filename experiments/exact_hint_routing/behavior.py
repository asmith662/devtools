# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, TRY003 -- literal protocol prose; formatter owns commas
"""Versioned B/C behavioral equality, without rewriting complete native objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.exact_hint_routing.serialization import encode, project

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25Match,
        RepositoryTextLexicalBm25RetrievalResult,
    )
    from experiments.exact_hint_routing.models import (
        ExactHintResolution,
        ExactHintRouteRequest,
        ExactHintRoutingView,
    )
    from experiments.exact_hint_routing.routing import ExactFrame

SCHEMA = "exact-hint-behavior-projection-v1"
CONTRACT = {
    "schema": SCHEMA,
    "purpose": "B/C treatment-equivalence validation only; no alteration of native artifacts, extraction evaluation, routing, scores or effectiveness.",
    "task_extraction_provenance": [
        "arm/source inventory identity",
        "extraction-rule identity",
        "caller-versus-rule author identity",
        "syntactic-form descriptor",
        "treatment-authorship explanation",
        "task-observation extraction provenance",
        "experimental routing-view construction provenance",
    ],
    "required_input_fields": [
        "route-request identity",
        "hint semantic identity",
        "exact task text/span",
        "associated obligation",
        "locator family/input",
        "selected mechanism",
        "frozen repository/snapshot/frame bindings",
    ],
    "required_behavior_fields": [
        "resolution disposition",
        "native resolved/ambiguous referent identities",
        "native candidate identities/order",
        "native repository evidence identities",
        "native resource occurrences",
        "resolution reason",
        "repository-resolution accounts/bindings",
        "promoted resource set",
        "exact-tier order/positions",
        "routed positions/resource sequence",
        "complete lexical membership/native order",
        "native ranks/scores",
        "content and weighted filename scores",
        "all term contributions",
        "index/query/settings bindings",
        "unchanged global safety lane",
    ],
    "native_boundary": "Only AnchorGrounding.request.provenance is excluded from each comparison copy: it is the original task-extraction provenance passed through by the caller. All other native grounding fields, including locator/class-parent source provenance, candidates, evidence, reason and universe, remain authenticated. No recursive provenance-name stripping.",
    "identities": "Native value identities include fully qualified native type plus SHA-256 of canonical complete native serialization. Grounding account SHA-256 covers its complete projection with only request.provenance excluded. Original artifacts retain all excluded values. Ordered identity lists retain cardinality and multiplicity; scores remain exact floats without rounding.",
    "reason_policy": "Keep resolution reasons verbatim. V1 does not remove reason text; any reason difference is behavioral unless frozen semantic inputs are first proven different.",
}


def _native(value: object) -> dict[str, str]:
    return {
        "native_type": type(value).__module__ + "." + type(value).__qualname__,
        "canonical_sha256": digest(encode(value)),
    }


def route_input(frame: ExactFrame, request: ExactHintRouteRequest) -> dict[str, Any]:
    """Retain frozen semantic inputs, excluding extraction-authorship descriptors."""
    return {
        "route_request_identity": request.identity,
        "hint_identity": project(request.hint.identity),
        "task": project(request.hint.task),
        "text": request.hint.text,
        "span": project(request.hint.span),
        "category": request.hint.category.value,
        "associated_obligation": project(request.association.lane),
        "locator_family": type(request.locator).__qualname__
        if request.locator is not None
        else "UNSUPPORTED",
        "locator": project(request.locator),
        "mechanism": request.mechanism,
        "repository_id": str(frame.repository_id),
        "snapshot_id": str(frame.snapshot_id),
        "frame_identity": frame.identity,
    }


def resolution(frame: ExactFrame, result: ExactHintResolution) -> dict[str, Any]:
    """Compare native repository evidence without task-author provenance leakage."""
    accounts = []
    for account in result.native_provenance:
        native = project(account)
        # Exact, typed owner boundary: never remove similarly named native fields.
        if set(native["request"]) != {
            "task",
            "anchor",
            "repository_id",
            "snapshot_id",
            "locator",
            "provenance",
        }:
            raise ValueError("Native grounding request schema changed")
        del native["request"]["provenance"]
        accounts.append(
            {
                "request": native["request"],
                "disposition": native["disposition"],
                "resolver": native["resolver"],
                "reason": native["reason"],
                "candidates": [
                    {"referent": _native(c.referent), "evidence": _native(c.evidence)}
                    for c in account.candidates
                ],
                "native_evidence": [_native(e) for e in account.native_evidence],
                "repository_account_sha256": digest(json_bytes(native)),
            }
        )
    return {
        "schema": SCHEMA,
        "kind": "resolution",
        "semantic_inputs": route_input(frame, result.request),
        "repository_id": str(result.repository_id),
        "snapshot_id": str(result.snapshot_id),
        "frame_identity": result.frame_identity,
        "disposition": result.disposition.value,
        "resources": [_native(r) for r in result.resources],
        "native_accounts": accounts,
        "reason": result.reason,
    }


def _match(
    match: RepositoryTextLexicalBm25Match | None, rank: int | None
) -> dict[str, Any]:
    if match is None:
        return {"rank": rank, "match": None}
    return {
        "rank": rank,
        "resource": _native(match.document_statistics.analysis.document.resource),
        "match": _native(match),
        "score": match.score,
        "content_score": match.content_score,
        "filename_score": match.filename_score,
        "filename_weight": match.filename_weight,
        "weighted_filename_score": match.weighted_filename_score,
        "content_contributions": project(match.term_contributions),
        "filename_contributions": project(match.filename_term_contributions),
    }


def _lexical(lane: RepositoryTextLexicalBm25RetrievalResult) -> dict[str, Any]:
    return {
        "query": project(lane.query),
        "index": _native(lane.index),
        "filename_index": _native(lane.filename_index),
        "settings": project(lane.settings),
        "maximum_results": lane.maximum_results,
        "native_order": [_match(m, n) for n, m in enumerate(lane.matches, 1)],
    }


def presentation(frame: ExactFrame, view: ExactHintRoutingView) -> dict[str, Any]:
    """Authenticate exact order, every lexical row and native score evidence."""
    entries = []
    for entry in view.exact_first:
        exact = entry.exact
        entries.append(
            {
                "resource": _native(entry.resource),
                "position": entry.position,
                "lexical": _match(
                    entry.lexical_result_reference, entry.native_lexical_rank
                ),
                "exact": None
                if exact is None
                else {
                    "resource": _native(exact.resource),
                    "hint_identity": project(exact.hint.identity),
                    "exact_tier_position": exact.exact_tier_position,
                    "resolution": resolution(frame, exact.resolution),
                    "lexical": _match(
                        exact.lexical_result_reference, exact.native_lexical_rank
                    ),
                },
            }
        )
    return {
        "schema": SCHEMA,
        "kind": "presentation",
        "semantic_inputs": {
            "lane": project(view.lane),
            "routes": [route_input(frame, r.request) for r in view.exact_resolutions],
        },
        "resolutions": [resolution(frame, r) for r in view.exact_resolutions],
        "original_lexical": _lexical(view.original_lexical_acquisition),
        "global_safety": _lexical(view.global_lexical_safety_lane),
        "entries": entries,
        "promoted_resource_set": sorted(
            json_bytes(e["resource"]).decode()
            for e in entries
            if e["exact"] is not None
        ),
        "exact_tier_order": [e for e in entries if e["exact"] is not None],
        "fallback_native_order": [e for e in entries if e["exact"] is None],
        "final_resource_sequence": [_native(e.resource) for e in view.exact_first],
    }


def require_equivalent(left: dict[str, Any], right: dict[str, Any]) -> None:
    """Reject behavioral differences, distinguish the frozen-input precondition."""
    if left.get("schema") != SCHEMA or right.get("schema") != SCHEMA:
        raise ValueError("Behavioral projection schema differs")
    if left["semantic_inputs"] != right["semantic_inputs"]:
        raise ValueError(
            "Frozen semantic route inputs differ; equivalence precondition not met"
        )
    if json_bytes(left) != json_bytes(right):
        raise ValueError(
            "EXPERIMENTAL_CONTRACT_DEFECT: B/C repository behavior differs"
        )

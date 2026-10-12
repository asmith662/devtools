# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812
"""Deterministic experimental evidence projection, not a durable native schema."""

from __future__ import annotations

import dataclasses
import math
from enum import Enum
from typing import TYPE_CHECKING

from devtools.context.python.function.materialization import _extract_source_segment
from devtools.core.identity import Identity
from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.task_conditioned_graph.ranking import require_ranking

if TYPE_CHECKING:
    from experiments.task_conditioned_graph.ranking import Ranking


def native(value: object) -> object:
    """Project all native dataclass fields losslessly with type and identity.

    This is inspection evidence only. The original native objects remain the
    authoritative replay input; this is not a wire decoder or guessed schema.
    """
    if isinstance(value, Enum):
        return {"type": type(value).__qualname__, "value": value.value}
    if isinstance(value, Identity):
        return {
            "native_type": type(value).__module__ + "." + type(value).__qualname__,
            "value": str(value),
        }
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("Nonfinite evidence")
        return {"float_hex": value.hex()}
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, (tuple, list)):
        return [native(item) for item in value]
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        result = {
            field.name: native(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
        result["native_type"] = type(value).__module__ + "." + type(value).__qualname__
        identity = getattr(value, "identity", None)
        if identity is not None:
            result["native_identity"] = str(identity)
        return result
    raise TypeError("Unsupported native evidence value: " + type(value).__qualname__)


def graph_evidence(result: Ranking) -> bytes:
    """Retain exact graph/seed/frame/rank evidence and full RI fact support."""
    snapshot = result.view.snapshot
    require_ranking(result)
    facts = {}
    for edge in result.view.edges:
        for fact in edge.references:
            source = snapshot.resource_at(fact.occurrence.resource_address)
            facts[fact.identity] = {
                "native": native(fact),
                "referenced_expression": _extract_source_segment(
                    source.content, fact.occurrence.source_range
                ),
                "source_content_identity": str(source.content_identity),
                "target_content_identity": str(fact.target_resource.content_identity),
            }
    return json_bytes(
        {
            "schema": "graph3-experimental-reference-evidence-v1",
            "repository_id": str(snapshot.repository_id),
            "snapshot_id": str(snapshot.id),
            "nodes": [
                {
                    "address": str(n),
                    "content_identity": str(snapshot.resource_at(n).content_identity),
                }
                for n in result.view.nodes
            ],
            "edges": [
                {
                    "source": str(e.source),
                    "target": str(e.target),
                    "raw_reference_count": len(e.references),
                    "weight_hex": e.weight.hex(),
                    "probability_hex": e.probability.hex(),
                    "facts": [r.identity for r in e.references],
                }
                for e in result.view.edges
            ],
            "facts": facts,
            "seeds": list(map(str, result.seeds)),
            "exact_native_resources": native(result.exact),
            "lexical_query": result.lexical.query.text,
            "lexical_seed_resources": [
                str(m.document_statistics.analysis.document.resource.address)
                for m in result.lexical.matches[:10]
            ],
            "settings": native(result.settings),
            "iterations": result.iterations,
            "converged": True,
            "ranked_resources": native(result.resources),
            "flow_meaning": (
                "restart = direct seed, dangling = personalized return, incoming = "
                "propagated stationary edge flow; edge index resolves exact provenance"
            ),
        }
    )


def validate_evidence(raw: bytes, result: Ranking) -> None:
    """Reject byte tamper without rerunning retrieval or stationary iteration."""
    if raw != graph_evidence(result):
        raise ValueError("Graph evidence tamper/identity mismatch")

# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812
"""Experiment-only definition map diagnostic; never an effectiveness arm."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from devtools.context.python.function.materialization import _extract_source_segment
from experiments.task_conditioned_graph.ranking import require_ranking

if TYPE_CHECKING:
    from experiments.task_conditioned_graph.ranking import Ranking

MAP_BYTES = 8192
HEADER_CHARACTERS = 240


@dataclass(frozen=True)
class DefinitionProjection:
    """RI definition identity plus parent score and exact incoming flow sources."""

    address: str
    definition: str
    subject: str
    name: str
    location: tuple[int, int, int, int]
    header: str
    parent_rank: int
    parent_score: float
    incoming_flow: float
    reference_flows: tuple[tuple[str, float], ...]


def definitions(result: Ranking) -> tuple[DefinitionProjection, ...]:
    """Split each resource edge flow evenly over its retained native references.

    Only referenced definitions in positively ranked owners participate. Native
    source extraction is reused; first declaration line is an excerpt, not a
    complete signature/body or decorators. This projection never changes ranks.
    """
    require_ranking(result)
    rows = {r.address: r for r in result.resources}
    grouped: dict[str, list[tuple[Any, float]]] = {}
    for row in rows.values():
        for edge_index, flow in row.incoming:
            edge = result.view.edges[edge_index]
            for reference in edge.references:
                grouped.setdefault(reference.target_declaration.identity, []).append(
                    (reference, flow / len(edge.references))
                )
    projected = []
    for identity, supports in grouped.items():
        declaration = supports[0][0].target_declaration
        address = declaration.support.resource_address
        row = rows[address]
        span = declaration.support.source_range
        content = result.view.snapshot.resource_at(address).content
        text = _extract_source_segment(content, span)
        first = text.splitlines()[0]
        header = first[:HEADER_CHARACTERS]
        if len(first) > HEADER_CHARACTERS or len(text.splitlines()) > 1:
            header += " … [declaration excerpt]"
        projected.append(
            DefinitionProjection(
                str(address),
                identity,
                declaration.subject.identity,
                declaration.declared_name,
                (
                    span.start_line,
                    span.start_column_utf8,
                    span.end_line,
                    span.end_column_utf8,
                ),
                header,
                row.rank,
                row.score,
                sum(flow for _, flow in supports),
                tuple(sorted((ref.identity, flow) for ref, flow in supports)),
            )
        )
    return tuple(
        sorted(projected, key=lambda r: (r.parent_rank, -r.incoming_flow, r.definition))
    )


def render_map(
    projected: tuple[DefinitionProjection, ...], *, budget: int = MAP_BYTES
) -> dict[str, Any]:
    """Admit whole ordered lines under exact rendered UTF-8 byte ceiling.

    No token estimator or production Context policy. Stop at first blocked line;
    omissions are metadata, not silently truncated declarations or reranking.
    """
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 0:
        raise ValueError("Map diagnostic requires a nonnegative integer byte budget")
    text = ""
    admitted = 0
    for row in projected:
        line = f"{row.address}:{row.location[0]} {row.name} | {row.header}\n"
        if len((text + line).encode("utf-8")) > budget:
            break
        text += line
        admitted += 1
    return {
        "text": text,
        "utf8_bytes": len(text.encode("utf-8")),
        "budget": budget,
        "admitted": admitted,
        "omitted": len(projected) - admitted,
        "effectiveness_arm": False,
    }

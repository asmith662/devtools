# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003
"""Timing adapters for frozen computational semantics, with retained state.

These experiment-only projections remove audit/representation work, not arithmetic.
Every full output is checked against committed native A/B/C results outside timing.
Production BM25, stationary walk and RRF are called directly and remain unchanged.
"""

from __future__ import annotations

import math
from contextlib import suppress
from typing import Any

from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.fusion import _fused_resource_order
from devtools.context.retrieval.graph.walk import stationary_distribution
from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25Match,
    RepositoryTextLexicalBm25Settings,
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)

SETTINGS = RepositoryTextLexicalBm25Settings(k1=1.2, b=0.75)


def lexical(index: Any, text: str) -> Any:
    """Measure the exact current canonical API, including filename-index rebuild."""
    return retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text=text),
        index=index,
        maximum_results=514,
        settings=SETTINGS,
    )


def addresses(result: Any) -> tuple[Any, ...]:
    """Project canonical matches to exact native addresses."""
    return tuple(
        m.document_statistics.analysis.document.resource.address for m in result.matches
    )


def final_lexical_ranking(index: Any, content: Any, filenames: Any) -> tuple[Any, ...]:
    """Isolate canonical final combination/match construction/sort, unchanged ties."""
    collection = index.corpus_statistics.collection_analysis.document_collection
    content_matches = {
        id(m.document_statistics.analysis.document): m for m in content.matches
    }
    statistics = {
        id(item.analysis.document): item
        for item in index.corpus_statistics.document_statistics
    }
    ranked = []
    for position, document in enumerate(collection.documents):
        match = content_matches.get(id(document))
        content_score = match.content_score if match else 0.0
        terms = filenames.get(id(document), ())
        filename_score = sum(item.contribution for item in terms)
        final = content_score + 0.25 * filename_score
        if final > 0:
            ranked.append(
                (
                    position,
                    RepositoryTextLexicalBm25Match(
                        document_statistics=statistics[id(document)],
                        score=final,
                        term_contributions=match.term_contributions if match else (),
                        content_score=content_score,
                        filename_score=filename_score,
                        filename_weight=0.25,
                        weighted_filename_score=0.25 * filename_score,
                        filename_term_contributions=terms,
                    ),
                ),
            )
    ranked.sort(key=lambda item: (-item[1].score, item[0]))
    return tuple(match for _, match in ranked[:514])


def graph_build(snapshot: Any, descriptors: list[Any]) -> tuple[Any, Any]:
    """Build nodes/pairs/sqrt weights/normalized rows from authenticated fact keys.

    Native fact identities and endpoint provenance are snapshot state, prepared
    outside this computational boundary. Pair and occurrence deduplication remain.
    Source row totals follow the exact frozen sorted-pair math.fsum order.
    """
    nodes = tuple(sorted((r.address for r in snapshot.resources), key=str))
    grouped: dict[Any, dict[str, Any]] = {}
    occurrences: dict[Any, str] = {}
    for identity, source, target, occurrence in descriptors:
        key = (str(source), occurrence)
        if key in occurrences and occurrences[key] != identity:
            raise ValueError("Conflicting native occurrence")
        occurrences[key] = identity
        grouped.setdefault((source, target), {})[identity] = identity
    weights = {pair: math.sqrt(len(facts)) for pair, facts in grouped.items()}
    totals = {
        node: math.fsum(
            w for (source, _), w in sorted(weights.items(), key=str) if source == node
        )
        for node in nodes
    }
    edges = tuple(
        (
            source,
            target,
            tuple(sorted(facts)),
            weights[source, target],
            weights[source, target] / totals[source],
        )
        for (source, target), facts in sorted(
            grouped.items(),
            key=lambda item: tuple(map(str, item[0])),
        )
    )
    return nodes, edges


def seed_vector(
    snapshot: Any,
    nodes: Any,
    result: Any,
    locators: Any,
) -> tuple[Any, list[float]]:
    """Use actual resource_at hits/misses and frozen uniform exact/top-ten union."""
    exact = []
    for locator in locators:
        with suppress(ValueError):
            exact.append(
                snapshot.resource_at(RepositoryResourceAddress(locator)).address,
            )
    seeds = tuple(sorted({*exact, *addresses(result)[:10]}, key=str))
    return seeds, [1 / len(seeds) if node in seeds else 0.0 for node in nodes]


def kernel(outgoing: Any, personalization: Any) -> Any:
    """Call the production kernel directly, without a profiler in timed loops."""
    return stationary_distribution(
        outgoing,
        personalization,
        damping=0.85,
        tolerance=1e-10,
        maximum_iterations=200,
    )


def pair_flow(edges: Any, positions: Any, scores: Any) -> list[float]:
    """Preserve frozen multiplication order d * pi(source) * transition."""
    return [0.85 * scores[positions[e.source]] * e.probability for e in edges]


def accumulate(nodes: Any, edges: Any, flows: Any) -> dict[Any, float]:
    """Use per-target math.fsum over edge-order incoming flow, including zeros."""
    incoming: dict[Any, list[float]] = {}
    for edge, flow in zip(edges, flows, strict=True):
        incoming.setdefault(edge.target, []).append(flow)
    return {node: math.fsum(incoming.get(node, ())) for node in nodes}


def ordered_flow(incoming: Any) -> tuple[Any, ...]:
    """Filter strictly positive membership; score/address tie rules unchanged."""
    return tuple(
        sorted(
            (n for n in incoming if incoming[n] > 0),
            key=lambda n: (-incoming[n], str(n)),
        ),
    )


def projection(nodes: Any, edges: Any, positions: Any, scores: Any) -> Any:
    """Pure propagated B projection without diagnostic incoming-state sorting."""
    flows = pair_flow(edges, positions, scores)
    incoming = accumulate(nodes, edges, flows)
    return ordered_flow(incoming), incoming, flows


def rrf(a: Any, b: Any) -> Any:
    """Invoke the actual production RRF primitive over already-materialized ranks."""
    return _fused_resource_order(a, b)


def warm(  # noqa: PLR0913, PLR0917 -- explicit retained-state timing boundary
    snapshot: Any,
    index: Any,
    view: Any,
    outgoing: Any,
    positions: Any,
    text: str,
    locators: Any,
) -> Any:
    """Complete production-shaped computation with all snapshot state retained."""
    a = lexical(index, text)
    seeds, personalization = seed_vector(snapshot, view.nodes, a, locators)
    scores, iterations, converged = kernel(outgoing, personalization)
    b, incoming, flows = projection(view.nodes, view.edges, positions, scores)
    c = rrf(
        {address: rank for rank, address in enumerate(addresses(a), 1)},
        {address: rank for rank, address in enumerate(b, 1)},
    )
    return a, b, c, scores, iterations, converged, seeds, incoming, flows


def definition_projection(ranking: Any, retained: Any) -> Any:
    """Split actual pair flow across native occurrences and order definitions.

    Query-independent identities, source excerpts and definition metadata are
    retained context state. No validation or serialization occurs here.
    """
    grouped: dict[str, list[float]] = {}
    metadata = {}
    parents = {row.address: row for row in ranking.resources}
    states = {row.address: row for row in ranking.states}
    for row in ranking.resources:
        for edge_index, flow in states[row.address].incoming:
            if flow <= 0:
                continue
            edge = ranking.view.edges[edge_index]
            for reference in edge.references:
                identity = retained[id(reference)]
                grouped.setdefault(identity, []).append(flow / len(edge.references))
                metadata[identity] = edge.target
    result = [
        (identity, metadata[identity], math.fsum(flows))
        for identity, flows in grouped.items()
    ]
    return tuple(
        sorted(result, key=lambda item: (-item[2], parents[item[1]].rank, item[0])),
    )

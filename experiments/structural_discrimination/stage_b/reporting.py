# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, E501, PLR2004 -- exact frozen numeric settings at artifact boundary
"""Reconstruct complete mechanical artifacts from retained returns, never treatments."""

from __future__ import annotations

import gzip
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.codex_dogfood.verification.native import NativeMemo
from experiments.structural_discrimination.stage_b.capture import (
    identity,
    validate_references,
    validate_surface,
)


def resource_row(document: Any, rank: int) -> dict[str, Any]:
    """Expose an exact native acquired document identity."""
    return identity(document.resource, document.id, rank)


def fact_row(fact: Any) -> dict[str, Any]:
    """Retain content-addressed links to the full canonical native RI graph."""
    span = fact.occurrence.source_range
    return {
        "fact_identity": fact.identity,
        "derivation_identity": fact.derivation_identity,
        "source_snapshot_id": str(fact.occurrence.snapshot_id),
        "source_address": str(fact.occurrence.resource_address),
        "source_range_utf8": {
            "start_line": span.start_line,
            "start_column_utf8": span.start_column_utf8,
            "end_line": span.end_line,
            "end_column_utf8": span.end_column_utf8,
        },
        "target_address": str(fact.target_resource.address),
        "target_content_identity": str(fact.target_resource.content_identity),
        "target_snapshot_id": str(fact.target_declaration.support.snapshot_id),
        "target_declaration_identity": fact.target_declaration.identity,
        "target_subject_identity": fact.target_subject.identity,
        "native_route": fact.route.value,
        "direct_call_tag_diagnostic_only": fact.direct_call,
        "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
    }


def derive(marker: Any, values: Any) -> dict[str, bytes]:
    """Validate/encode expected artifacts once from actual retained native returns."""
    design = marker["design"]
    frame = values["frame:prepare"]
    prepared = values["references:prepare"]
    analyses = {
        key.removeprefix("ri:references:"): value
        for key, value in values.items()
        if key.startswith("ri:references:")
    }
    ri = validate_references(frame, analyses, prepared)
    facts = tuple(fact_row(f) for f in prepared.facts)
    fact_map = {f["fact_identity"]: f for f in facts}
    queries = []
    for obligation in design["obligations"]:
        query = obligation["query_identity"]["value"]
        prefix = "query:" + query + ":"
        acquisition, annotated, pair_return = (
            values[prefix + name] for name in ("A", "annotation", "pairs")
        )
        lexical, surface = acquisition["result"], annotated["result"]
        if (
            surface.lexical_result is not lexical
            or lexical.query.text != obligation["query"]
            or lexical.settings.k1 != 1.2
            or lexical.settings.b != 0.75
            or lexical.maximum_results != design["parent_frame"]["resource_count"]
        ):
            raise ValueError("Frozen A identity/settings/query differs")
        check = validate_surface(prepared, surface, pair_return["result"])
        if values[prefix + "validate"] != check:
            raise ValueError("Captured validation differs")
        ranked = [
            {
                **resource_row(match.document_statistics.analysis.document, rank),
                "score": match.score,
                "content_score": match.content_score,
                "filename_score": match.filename_score,
                "filename_weight": match.filename_weight,
                "weighted_filename_score": match.weighted_filename_score,
            }
            for rank, match in enumerate(lexical.matches, 1)
        ]
        if any(
            row["score"] <= 0 or row["filename_weight"] != 0.25 for row in ranked
        ) or [row["score"] for row in ranked] != sorted(
            (row["score"] for row in ranked),
            reverse=True,
        ):
            raise ValueError("A positive ordering/filename settings differ")
        annotations = []
        for target in surface.annotations:
            sources = [
                {
                    **identity(source.resource, source.document_id, source.a_rank),
                    "snapshot_id": str(frame.snapshot.id),
                    "supports": [fact_map[s.fact.identity] for s in source.supports],
                }
                for source in target.sources
            ]
            annotations.append(
                {
                    "target": identity(
                        target.resource,
                        target.document_id,
                        target.a_rank,
                    ),
                    "sources": sources,
                    "distinct_supporting_source_count": target.distinct_source_count,
                    "native_occurrence_count": target.occurrence_count,
                    "best_supporting_source_rank": target.best_source_rank,
                },
            )
        timings = {
            "canonical_a_ns": acquisition["online_ns"],
            "support_projection_ns": annotated["support_projection_ns"],
            "annotation_construction_ns": annotated["annotation_construction_ns"],
            "predecessor_pairs_ns": pair_return["online_ns"],
        }
        timings["complete_online_equivalent_ns"] = sum(timings.values())
        if annotated["online_ns"] != timings["support_projection_ns"] + timings[
            "annotation_construction_ns"
        ] or any(v < 0 for v in timings.values()):
            raise ValueError("Timing arithmetic differs")
        queries.append(
            {
                "obligation": obligation["id"],
                "query_identity": obligation["query_identity"],
                "query": obligation["query"],
                "information_need": obligation["need"],
                "task_identity": design["task_identity"],
                "frame": marker["frame"],
                "A": ranked,
                "annotations": annotations,
                "local_pairs": pair_return["result"],
                "counts": check,
                "timings": timings,
            },
        )
    if values["annotation:ablation"] != {
        "status": "PASS",
        "primary_annotation_passes": 3,
        "empty_reference_validation_ablations": 3,
        "ranking_side_effect": "NONE",
    }:
        raise ValueError("Ablation differs")
    summary = {
        "case": marker["case"],
        "execution": marker["execution"],
        "status": "CAPTURED; NO GOLD; NO EFFECTIVENESS INTERPRETATION",
        "task": design["task_text"],
        "frame": design["parent_frame"],
        "interpretation_gaps": design["interpretation_gaps"],
        "ri": ri,
        "queries": [
            {
                "obligation": q["obligation"],
                "a_results": len(q["A"]),
                **q["counts"],
                "timings": q["timings"],
            }
            for q in queries
        ],
        "ablation": values["annotation:ablation"],
        "ppr_executions": 0,
        "rrf_executions": 0,
        "graph_only_admissions": 0,
        "rank_modifications": 0,
        "holdout_access": "NO",
        "gold_access": "NO",
        "confirmation_reserve_access": "NO",
    }
    if values["capture:validate"] != ri:
        raise ValueError("Capture-wide RI validation differs")
    trace = {
        "scope": "MECHANICAL_ONLY",
        "summary": summary,
        "queries": queries,
        "positive_references": facts,
    }
    validation = {
        "status": "PASS",
        "checks": [
            "exact Stage A/frame",
            "one RI derivation per Python resource",
            "positive/negative coverage",
            "three A/annotation/pair passes",
            "complete exact stronger-source support",
            "original immediate predecessor",
            "exact A ablation",
            "no graph ranking/PPR/RRF",
            "timing arithmetic",
        ],
        "interpretation": "NO SEMANTIC LABELS OR CASE CATEGORY",
    }
    review = (
        "# Direct structural discrimination Stage B mechanical review\n\nNo semantic gold, usefulness, pair utility or case outcome is inferred.\n\n## Capture summary\n\n```json\n"
        + json_bytes(summary).decode()
        + "```\n\n## Complete A/support/pair trace\n\n```json\n"
        + json_bytes(queries).decode()
        + "```\n\nComplete positive native Reference identities are in references.json.gz; all positive and negative native RI state is in ri_native.json.gz and the immutable journal.\n"
    )
    # Complete graph retains every native field/order/alias once, not only positive relations.
    native = NativeMemo().encoding.encode(tuple(analyses.values()))
    return {
        "summary.json": json_bytes(summary),
        "trace.json.gz": gzip.compress(json_bytes(trace), mtime=0),
        "arm_a.json.gz": gzip.compress(json_bytes(queries), mtime=0),
        "references.json.gz": gzip.compress(json_bytes(facts), mtime=0),
        "ri_native.json.gz": gzip.compress(native, mtime=0),
        "STAGE_B_REVIEW.md": review.encode(),
        "validation.json": json_bytes(validation),
    }


def canonical_validate(trace: Any) -> None:  # noqa: C901 -- sealed scientific consistency boundary
    """Validate canonical consistency without native decoding or treatment execution."""
    facts = {f["fact_identity"]: f for f in trace["positive_references"]}
    for query in trace["queries"]:
        ranked = query["A"]
        by_address = {r["address"]: r for r in ranked}
        if len(by_address) != len(ranked) or [r["a_rank"] for r in ranked] != list(
            range(1, len(ranked) + 1),
        ):
            raise ValueError("Canonical A identities/order differ")
        eligible = {
            (f["source_address"], f["target_address"], f["fact_identity"])
            for f in facts.values()
            if f["source_address"] in by_address
            and f["target_address"] in by_address
            and by_address[f["source_address"]]["a_rank"]
            < by_address[f["target_address"]]["a_rank"]
        }
        actual = set()
        targets = []
        for annotation in query["annotations"]:
            target = annotation["target"]
            expected_target = {k: by_address[target["address"]][k] for k in target}
            if target != expected_target:
                raise ValueError("Canonical target binding differs")
            targets.append(target["a_rank"])
            for source in annotation["sources"]:
                if any(
                    source[k] != by_address[source["address"]][k]
                    for k in (
                        "address",
                        "content_identity",
                        "document_identity",
                        "a_rank",
                    )
                ):
                    raise ValueError("Canonical source binding differs")
                for support in source["supports"]:
                    if facts.get(support["fact_identity"]) != support:
                        raise ValueError("Canonical native fact binding differs")
                    actual.add(
                        (
                            source["address"],
                            target["address"],
                            support["fact_identity"],
                        ),
                    )
        if (
            actual != eligible
            or targets != sorted(set(targets))
            or len(query["local_pairs"]) != len(targets)
        ):
            raise ValueError("Canonical evidence/pair completeness differs")
        for annotation, pair in zip(
            query["annotations"],
            query["local_pairs"],
            strict=True,
        ):
            target = annotation["target"]
            predecessor = ranked[target["a_rank"] - 2]
            if pair["target"] != target or pair["predecessor"] != {
                k: predecessor[k] for k in target
            }:
                raise ValueError("Canonical predecessor differs")

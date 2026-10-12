# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, E501, PLR0915, C901, PLR0912, PLR2004, TC003
"""Reconstruct only immutable native returns; never execute treatment functions."""

from __future__ import annotations

import gzip
import json
import math
import time
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

from devtools.context.python.function.materialization import _extract_source_segment
from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    json_bytes,
    put_binary,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0012.stage_b.durability import exclusive
from experiments.codex_dogfood.case_0012.stage_b.graph import describe
from experiments.codex_dogfood.case_0015.stage_b.execute import union_statistics
from experiments.codex_dogfood.case_0015.stage_b.validation import (
    native_surface,
    validate_fields,
    validate_native,
)
from experiments.codex_dogfood.case_0016 import freeze, protocol
from experiments.codex_dogfood.case_0016.stage_b.authenticate import (
    EXECUTION,
    SCHEDULE_PATH,
    STAGE_A,
    source_hashes,
)
from experiments.codex_dogfood.case_0016.stage_b.durability import (
    Journal,
    checkpoint_bytes,
)
from experiments.codex_dogfood.case_0016.stage_b.execute import schedule
from experiments.task_conditioned_graph.ranking import SETTINGS, require_ranking
from experiments.task_conditioned_graph.view import require_view


def near(actual: float, expected: float, tolerance: float = 2e-10) -> None:
    """Apply the frozen accounting convention, never ranking tolerances."""
    if not math.isfinite(actual) or abs(actual - expected) > tolerance:
        raise ValueError("Captured flow accounting differs")


def validate_projection(projected: Any, ranking: Any, rendered: dict[str, Any]) -> None:
    """Independently reconcile occurrences/definitions and reconstruct map text."""
    states = {s.address: s for s in ranking.states}
    members = {r.address: r for r in ranking.resources}
    expected: dict[str, tuple[Any, float]] = {}
    for edge in ranking.view.edges:
        pair = (
            ranking.settings.damping
            * states[edge.source].stationary_mass
            * edge.probability
        )
        if pair <= 0:
            continue
        near(math.fsum(pair / len(edge.references) for _ in edge.references), pair)
        for reference in edge.references:
            expected[reference.identity] = (reference, pair / len(edge.references))
    actual = {}
    for row in projected:
        owner = ranking.view.snapshot.resource_at(
            next(r for r in members if str(r) == row.address),
        )
        parent = members[owner.address]
        if row.parent_rank != parent.rank or row.parent_score != parent.score:
            raise ValueError("Definition parent propagated score/rank differs")
        supports = []
        for occurrence in row.occurrence_flows:
            reference = occurrence.reference
            captured, flow = expected[reference.identity]
            if (
                reference != captured
                or reference.identity in actual
                or occurrence.definition_identity
                != reference.target_declaration.identity
                or row.definition != occurrence.definition_identity
                or occurrence.definition_owner != row.address
                or occurrence.target_resource != row.address
                or occurrence.source_resource
                != str(reference.occurrence.resource_address)
                or occurrence.per_occurrence_flow != flow
            ):
                raise ValueError("Native definition/reference projection differs")
            source = ranking.view.snapshot.resource_at(
                reference.occurrence.resource_address,
            )
            if occurrence.referenced_expression != _extract_source_segment(
                source.content,
                reference.occurrence.source_range,
            ):
                raise ValueError("Reference expression/span differs")
            edge = next(
                e
                for e in ranking.view.edges
                if str(e.source) == occurrence.source_resource
                and str(e.target) == occurrence.target_resource
            )
            if (
                occurrence.pair_flow
                != ranking.settings.damping
                * states[edge.source].stationary_mass
                * edge.probability
            ):
                raise ValueError("Definition pair flow differs")
            declaration = reference.target_declaration
            span = declaration.support.source_range
            location = (
                span.start_line,
                span.start_column_utf8,
                span.end_line,
                span.end_column_utf8,
            )
            text = _extract_source_segment(owner.content, span)
            first = text.splitlines()[0]
            header = first[:240] + (
                " … [declaration excerpt]"
                if len(first) > 240 or len(text.splitlines()) > 1
                else ""
            )
            if (
                row.location != location
                or row.subject != declaration.subject.identity
                or row.name != declaration.declared_name
                or row.header != header
            ):
                raise ValueError("Definition identity/location/excerpt differs")
            actual[reference.identity] = flow
            supports.append(flow)
        if row.incoming_flow != math.fsum(supports) or row.reference_flows != tuple(
            sorted(
                (o.reference.identity, o.per_occurrence_flow)
                for o in row.occurrence_flows
            ),
        ):
            raise ValueError("Definition flow aggregation differs")
    if set(actual) != set(expected) or tuple(projected) != tuple(
        sorted(
            projected,
            key=lambda r: (-r.incoming_flow, r.parent_rank, r.definition),
        ),
    ):
        raise ValueError("Definition occurrence membership/order differs")
    for address, parent in members.items():
        near(
            math.fsum(r.incoming_flow for r in projected if r.address == str(address)),
            parent.score,
        )
    text, admitted = "", 0
    for row in projected:
        line = f"{row.address}:{row.location[0]} {row.name} | {row.header}\n"
        if len((text + line).encode()) > 8192:
            break
        text += line
        admitted += 1
    expected_map = {
        "text": text,
        "utf8_bytes": len(text.encode()),
        "budget": 8192,
        "admitted": admitted,
        "omitted": len(projected) - admitted,
        "effectiveness_arm": False,
    }
    if rendered != expected_map:
        raise ValueError("Frozen diagnostic map differs")


def reconstruct(root: Path) -> tuple[dict[str, Any], dict[str, Any], Journal]:
    """Complete real-capture integrity reader; no PPR/retrieval/fusion/RI calls."""
    journal = Journal.load(root)
    journal.ready()
    marker = journal.state["marker"]
    values = journal.state["values"]
    rows = json.loads(gzip.decompress(binary(freeze.CASE / "resources.json.gz")))
    design = read_json(freeze.CASE / "protocol.json")
    metadata = read_json(freeze.CASE / "frame.json")
    if (
        journal.state["state"] != "NATIVE_CAPTURE_COMPLETE"
        or marker["execution"] != EXECUTION
        or marker["stage_a"] != STAGE_A
        or marker["protocol_sha256"] != digest(binary(freeze.CASE / "protocol.json"))
        or marker["initial_counts"] != protocol.COUNTS
        or marker["implementation_sha256"] != source_hashes()
        or tuple(marker["operation_schedule"]) != schedule(rows)
        or tuple(o["identity"] for o in journal.state["operations"]) != schedule(rows)
    ):
        raise ValueError("Complete frozen execution/source/schedule binding differs")
    schedule_path = root.parent.parent / SCHEDULE_PATH.name
    if marker["schedule_sha256"] != digest(binary(schedule_path)):
        raise ValueError("Preclaim operation schedule differs")
    frame, state = values["frame:prepare"], values["lexical:index"]
    if len(frame.snapshot.resources) != 514 or (
        str(frame.snapshot.repository_id),
        str(frame.snapshot.id),
        str(frame.documents.corpus.id),
    ) != tuple(metadata[k] for k in ("repository_id", "snapshot_id", "corpus_id")):
        raise ValueError("Exact 514-resource frame differs")
    for document, row in zip(frame.documents.documents, rows, strict=True):
        if (
            str(document.id),
            str(document.resource.content_identity),
            str(document.resource.address),
            document.text,
        ) != (
            row["document_identity"],
            row["content_identity"],
            row["address"],
            row["content"],
        ):
            raise ValueError("Retained resource/document/content identity differs")
    union = union_statistics(
        state,
    )  # Mechanical field memberships only; no query/scorer.
    surface = validate_fields(state, union)
    assessments = [
        values["ri:references:" + r["address"]]
        for r in rows
        if r["address"].endswith(".py")
    ]
    modules = values["ri:module-universe"]
    outcomes: Counter[str] = Counter()
    references = []
    for row, analysis in zip(
        (r for r in rows if r["address"].endswith(".py")),
        assessments,
        strict=True,
    ):
        if (
            str(analysis.derivation.dependency.resource.address) != row["address"]
            or analysis.derivation.module_universe_identity != modules.identity
        ):
            raise ValueError("Reference derivation input differs")
        if (
            analysis.coverage.assessed_count != len(analysis.assessments)
            or analysis.coverage.reference_count != len(analysis.references)
            or tuple(
                a.reference for a in analysis.assessments if a.reference is not None
            )
            != analysis.references
        ):
            raise ValueError("Native positive/negative assessment account differs")
        for assessment in analysis.assessments:
            resource = frame.snapshot.resource_at(
                assessment.occurrence.resource_address,
            )
            if assessment.source_text != _extract_source_segment(
                resource.content,
                assessment.occurrence.source_range,
            ):
                raise ValueError("Native reference assessment span differs")
            outcomes[assessment.outcome.value] += 1
        references.extend(analysis.references)
    view = values["graph:construct"]
    require_view(frame.snapshot, view)
    if {r.identity for e in view.edges for r in e.references} != {
        r.identity for r in references
    }:
        raise ValueError("Reference graph/native resolved membership differs")
    graph = {
        "nodes": len(view.nodes),
        "directed_pairs": len(view.edges),
        "resolved_occurrences": sum(len(e.references) for e in view.edges),
        "self_pairs": sum(e.source == e.target for e in view.edges),
        "self_occurrences": sum(
            len(e.references) for e in view.edges if e.source == e.target
        ),
        "dangling_nodes": len(set(view.nodes) - {e.source for e in view.edges}),
        "raw_count_distribution": dict(
            sorted(Counter(len(e.references) for e in view.edges).items()),
        ),
        "sqrt_weights": "PASS",
        "normalized_rows": "PASS",
        "no_paths_frontier_reverse_edges": "PASS",
    }
    query_reports, arms, graphs, seeds, ppr, flows, fused, projected_rows, maps = (
        [],
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
    )
    for i, obligation in enumerate(design["requirement_matrix"], 1):
        query_id = f"Q{i}"
        lexical = values[f"query:{query_id}:A"]
        if lexical.query.text != obligation["query"]:
            raise ValueError("Exact obligation query differs")
        query = {
            "analysis": asdict(lexical.query),
            "normalized_terms": list(lexical.query.normalized_terms),
        }
        validate_native(lexical, state, surface, union, query)
        exact = values[f"query:{query_id}:exact"]
        locators = design["seed_policy"]["exact_locators"][query_id]
        if tuple(map(str, exact.locators)) != tuple(locators):
            raise ValueError("Exact locator literals differ")
        expected_exact = tuple(
            frame.snapshot.resource_at(type(view.nodes[0])(s))
            for s in locators
            if any(str(n) == s for n in view.nodes)
        )
        if exact.resources != expected_exact or tuple(map(str, exact.absent)) != tuple(
            s for s in locators if not any(str(n) == s for n in view.nodes)
        ):
            raise ValueError("Captured exact native resolution differs")
        observed = values[f"query:{query_id}:B"]
        ranking = observed["ranking"]
        require_ranking(ranking)
        if (
            ranking.settings != SETTINGS
            or ranking.lexical is not lexical
            or ranking.view is not view
            or ranking.exact != exact.resources
        ):
            raise ValueError("Frozen B native input/settings differ")
        a = [
            str(m.document_statistics.analysis.document.resource.address)
            for m in lexical.matches
        ]
        b = [str(r.address) for r in ranking.resources]
        captured_c = values[f"query:{query_id}:C"]
        c = [str(address) for address, _score in captured_c]
        expected_seeds = sorted(set(a[:10]) | {str(r.address) for r in exact.resources})
        if (
            list(map(str, ranking.seeds)) != expected_seeds
            or values[f"query:{query_id}:seeds"] != ranking.seeds
        ):
            raise ValueError("Frozen exact/lexical seed union differs")
        kernel = observed["kernel_observations"]
        if (len(kernel) != (1 if ranking.seeds else 0)) or (
            kernel
            and (
                not kernel[0]["converged"]
                or kernel[0]["iterations"] != ranking.iterations
                or not 0 <= kernel[0]["final_delta"] <= 1e-10
            )
        ):
            raise ValueError("Single native PPR convergence account differs")
        ar, br = {s: n for n, s in enumerate(a, 1)}, {s: n for n, s in enumerate(b, 1)}
        contribution: list[dict[str, Any]] = [
            {
                "address": s,
                "a_rank": ar.get(s),
                "b_rank": br.get(s),
                "a_contribution": 1 / (60 + ar[s]) if s in ar else 0.0,
                "b_contribution": 1 / (60 + br[s]) if s in br else 0.0,
                "score": (1 / (60 + ar[s]) if s in ar else 0.0)
                + (1 / (60 + br[s]) if s in br else 0.0),
                "graph_channel_ablated_a_rank": ar.get(s),
            }
            for s in set(a) | set(b)
        ]
        contribution.sort(
            key=lambda r: (
                -r["score"],
                r["a_rank"] if r["a_rank"] is not None else math.inf,
                r["address"],
            ),
        )
        if [r["address"] for r in contribution] != c:
            raise ValueError("Production RRF reconstruction/order/union differs")
        if [r["score"] for r in contribution] != [
            score for _address, score in captured_c
        ]:
            raise ValueError("Production RRF captured scores differ")
        for n, item in enumerate(contribution, 1):
            item["rank"] = n
        accounting = [
            {
                "address": str(s.address),
                "stationary_mass": s.stationary_mass,
                "direct_restart_mass": s.direct_restart_mass,
                "dangling_return_mass": s.dangling_return_mass,
                "incoming_structural_flow": s.incoming_structural_flow,
                "seed": s.seed,
                "in_b": str(s.address) in br,
                "incoming": s.incoming,
            }
            for s in ranking.states
        ]
        for item in accounting:
            if item["incoming_structural_flow"] == 0 and item["in_b"]:
                raise ValueError("Seed-only/non-flow node entered B")
            if (
                item["address"] not in br
                and item["address"] in {str(s) for s in ranking.seeds}
                and any(
                    r["address"] == item["address"] and r["b_contribution"] != 0
                    for r in contribution
                )
            ):
                raise ValueError("Restart/dangling carryover fused")
        pair_flows = [
            {
                "edge_index": n,
                "source": str(e.source),
                "target": str(e.target),
                "raw_count": len(e.references),
                "weight": e.weight,
                "transition": e.probability,
                "pair_flow": ranking.settings.damping
                * next(
                    s.stationary_mass for s in ranking.states if s.address == e.source
                )
                * e.probability,
                "reference_identities": [r.identity for r in e.references],
            }
            for n, e in enumerate(view.edges)
        ]
        projected = values[f"query:{query_id}:definitions"]
        rendered = values[f"query:{query_id}:map"]
        validate_projection(projected, ranking, rendered)
        seeded = [s for s in ranking.states if s.seed]
        query_reports.append(
            {
                "query": query_id,
                "obligation": obligation["obligation"],
                "A_candidates": len(a),
                "B_candidates": len(b),
                "C_candidates": len(c),
                "A_intersection_B": len(set(a) & set(b)),
                "A_only": len(set(a) - set(b)),
                "B_only": len(set(b) - set(a)),
                "A_union_B": len(set(a) | set(b)),
                "A_only_addresses": sorted(set(a) - set(b)),
                "B_only_addresses": sorted(set(b) - set(a)),
                "lexical_seeds": a[:10],
                "exact_seeds": [str(r.address) for r in exact.resources],
                "exact_absent": list(map(str, exact.absent)),
                "exact_locators": locators,
                "unique_seed_count": len(ranking.seeds),
                "PPR_iterations": ranking.iterations,
                "PPR_final_delta": kernel[0]["final_delta"] if kernel else 0.0,
                "stationary_mass": math.fsum(s.stationary_mass for s in ranking.states),
                "restart_mass": math.fsum(
                    s.direct_restart_mass for s in ranking.states
                ),
                "dangling_return_mass": math.fsum(
                    s.dangling_return_mass for s in ranking.states
                ),
                "incoming_structural_flow": math.fsum(
                    s.incoming_structural_flow for s in ranking.states
                ),
                "seed_only_count": sum(s.incoming_structural_flow == 0 for s in seeded),
                "seeded_positive_flow": sum(
                    s.incoming_structural_flow > 0 for s in seeded
                ),
                "nonseed_B_members": sum(not r.seed for r in ranking.resources),
                "top10_A": a[:10],
                "top10_B": b[:10],
                "top10_C": c[:10],
                "overlap": {
                    str(k): {
                        "A_B": len(set(a[:k]) & set(b[:k])),
                        "A_C": len(set(a[:k]) & set(c[:k])),
                        "B_C": len(set(b[:k]) & set(c[:k])),
                    }
                    for k in (10, 20, 50)
                },
                "definition_flow_count": len(projected),
                "map_admitted": rendered["admitted"],
                "map_omitted": rendered["omitted"],
                "map_utf8_bytes": rendered["utf8_bytes"],
                "seed_accounting": [r for r in accounting if r["seed"]],
            },
        )
        arms[query_id] = native_surface(lexical)
        graphs[query_id] = [
            {
                "address": str(r.address),
                "rank": r.rank,
                "score": r.score,
                "score_hex": r.score.hex(),
                "seed": r.seed,
            }
            for r in ranking.resources
        ]
        seeds[query_id] = {
            "exact": describe(exact),
            "lexical": a[:10],
            "unique": expected_seeds,
            "uniform_probability": 1 / len(expected_seeds) if expected_seeds else 0.0,
        }
        (
            ppr[query_id],
            flows[query_id],
            fused[query_id],
            projected_rows[query_id],
            maps[query_id],
        ) = accounting, pair_flows, contribution, describe(projected), rendered
    reference = values["query:reference"]
    if reference.query.text != design["task_text"]:
        raise ValueError("Whole-task separate reference lane changed")
    validate_native(
        reference,
        state,
        surface,
        union,
        {
            "analysis": asdict(reference.query),
            "normalized_terms": list(reference.query.normalized_terms),
        },
    )
    summary = {
        "case": "0016",
        "execution": EXECUTION,
        "stage_a": STAGE_A,
        "stage_b": "CAPTURED",
        "attempt_1": "FAILED_AUDIT_ONLY",
        "attempt_2": "AUTHORITATIVE",
        "frame": marker["frame"],
        "resources": len(rows),
        "operations": len(journal.state["operations"]),
        "journal_events": journal.events,
        "retries": 0,
        "failures": 0,
        "python_resources_assessed": len(assessments),
        "reference_assessment_outcomes": dict(sorted(outcomes.items())),
        "native_assessments": sum(outcomes.values()),
        "graph": graph,
        "queries": query_reports,
        "reference_candidates": len(reference.matches),
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "outcome": "NOT_SELECTED",
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
        "production_behavior": "UNCHANGED",
        "feature_implementation": "NOT_IMPLEMENTED",
        "confirmation_reserve": "NOT_ACCESSED",
        "historical_mechanical_comparison": {
            "Graph_1": "704 retained novel resource pairs / 10,550 paths across 24 obligations",
            "Graph_2": "987 retained resource pairs / 85,015 novel paths / 294,154 complete paths",
            "Graph_3": "Ranked positive B flow counts only; zero path-family enumeration. Different tasks; no superiority or usefulness comparison before gold.",
        },
    }
    artifacts = {
        "lexical_fields": surface,
        "native_statistics": describe(
            (state.content.corpus_statistics, state.filename),
        ),
        "ri_assessments": describe(tuple(assessments)),
        "reference_graph": describe(view),
        "arm_a": arms,
        "exact_seeds_personalization": seeds,
        "ppr_states": ppr,
        "pair_flows": flows,
        "arm_b": graphs,
        "definitions": projected_rows,
        "arm_c": fused,
        "reference": native_surface(reference),
        "maps": maps,
    }
    return summary, artifacts, journal


def render(summary: dict[str, Any], costs: dict[str, Any]) -> str:
    """Expose all mechanical facts and complete ranked diagnostic evidence."""
    text = "# Case 0016 Graph-3 Stage B mechanical capture\n\nGOLD = ABSENT\nEFFECTIVENESS = UNKNOWN\nOUTCOME = NOT_SELECTED\nSEARCH_POLICY_FAILURE = NOT_ASSESSED\n\nNo semantic adjudication or effectiveness interpretation. Production behavior unchanged. Resource-pointer feature not implemented. Confirmation/reserve not accessed.\n\n"
    text += "The amended Stage A is immutable. B ranks only positive incoming structural reference flow; stationary/restart/dangling mass cannot rank or fuse. A seed with zero incoming flow is excluded from B. The definition map is diagnostic only. No paths/frontier/reverse relations are acquired.\n\n"
    text += "All validation reconstructs the durable native returns, with no query/RI/PPR/fusion rerun. The PPR return profiler observes the one native final delta. Its overhead belongs to experimental single-run timing.\n\n"
    text += (
        "```json\n"
        + json_bytes(summary).decode()
        + "```\n\n## Single-run costs\n\n```json\n"
        + json_bytes(costs).decode()
        + "```\n\n"
    )
    text += "Native journal archives retain every field, identity, occurrence, span, route, alias, and exact float. Deterministic gzip inspection artifacts expose native statistics/assessments/graph, all A/B/C ranks and RRF channels, seeds, complete stationary accounting, pair flows, definition flows, map outputs and unchanged reference results. Decimal JSON floats are round-trip exact; graph scores additionally expose float.hex. Pure graph/definition/map reconstructions are validation, not additional treatment invocations.\n"
    return text


def derived(root: Path) -> dict[str, bytes]:
    """Deterministic serialization solely from already-captured returns/times."""
    summary, artifacts, journal = reconstruct(root)
    costs = {
        "operations": [
            {
                "operation": o["identity"],
                "runtime_ns": o["runtime_ns"],
                "human_seconds": o["runtime_ns"] / 1e9,
                "wall_call_ns": o["wall_call_ns"],
                "durability_inside_call_ns": o["durability_inside_call_ns"],
            }
            for o in journal.state["operations"]
        ],
        **read_json(root / "capture_costs.json"),
        "interpretation": "Single run, descriptive only; no effectiveness/cost gate or production extrapolation. Operation runtime and durability are separate, never added twice.",
    }
    files = {
        name + ".json.gz": gzip.compress(json_bytes(value), mtime=0)
        for name, value in artifacts.items()
    }
    files["summary.json"] = json_bytes(summary)
    files["raw_checkpoint.json"] = checkpoint_bytes(journal)
    files["costs.json"] = json_bytes(costs)
    validation = {
        "mechanical_capture": "PASS",
        "frame": "PASS",
        "stage_a_and_original_seals": "PASS",
        "lexical_native_reconstruction": "PASS",
        "ri_assessment_account": "PASS",
        "reference_provenance_graph_sqrt_rows": "PASS",
        "PPR_convergence_and_stationary_accounting": "PASS",
        "pair_resource_definition_flow": "PASS",
        "seed_only_exclusion": "PASS",
        "production_RRF_reconstruction": "PASS",
        "diagnostic_map_reconstruction": "PASS",
        "reference_lane": "PASS",
        "journal_schedule_durability_at_most_once": "PASS",
        "no_scientific_replay": True,
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "outcome": "NOT_SELECTED",
    }
    files["validation.json"] = json_bytes(validation)
    trace = {
        "authentication": journal.state["marker"]["authentication"],
        "operation_schedule": journal.state["marker"]["operation_schedule"],
        "operations": journal.state["operations"],
        "summary": summary,
        "validation": validation,
        "artifacts": {k: digest(v) for k, v in files.items()},
    }
    files["trace.json"] = json_bytes(trace)
    review = render(summary, costs).encode()
    files["STAGE_B_REVIEW.md"] = review
    files["TRACE.md"] = review
    return files


def publish(root: Path) -> None:
    """Exclusive deterministic publication; scientific calls are unavailable."""
    if (root / "integrity.json").exists() or (root / "summary.json").exists():
        raise FileExistsError("Stage B publication overwrite refused")
    started = time.perf_counter_ns()
    files = derived(root)
    construction = time.perf_counter_ns() - started
    started = time.perf_counter_ns()
    for name, raw in files.items():
        if name.endswith(".gz"):
            put_binary(root / name, raw)
        else:
            put_text(root / name, raw.decode())
    exclusive(
        root / "publication_costs.json",
        {
            "deterministic_construction_validation_ns": construction,
            "derived_artifact_publication_ns": time.perf_counter_ns() - started,
            "note": "Measured once. Excludes final integrity publication and subsequent read-only verification.",
        },
    )
    hashes = {
        p.relative_to(root).as_posix(): digest(binary(p))
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }
    exclusive(
        root / "integrity.json",
        {
            "schema": "case-0016-stage-b-integrity-v1",
            "execution": EXECUTION,
            "implementation_sha256": source_hashes(),
            "sha256": hashes,
            "schedule_sha256": digest(
                binary(root.parent.parent / SCHEDULE_PATH.name),
            ),
            "gold": "ABSENT",
            "outcome": "NOT_SELECTED",
        },
    )
    verify(root)


def verify(root: Path) -> None:
    """Reject missing/extra/tampered bytes, source drift and derived mismatch."""
    seal = read_json(root / "integrity.json")
    actual = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and p.name != "integrity.json"
    }
    if (
        actual != set(seal["sha256"])
        or any(digest(binary(root / p)) != h for p, h in seal["sha256"].items())
        or seal["implementation_sha256"] != source_hashes()
        or (root / "capture_failure.json").exists()
    ):
        raise ValueError("Capture physical/source/complete integrity differs")
    for name, raw in derived(root).items():
        if binary(root / name) != raw:
            raise ValueError("Deterministic captured-return replay differs: " + name)

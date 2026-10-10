# Copyright (c) 2026
# ruff: noqa: ANN401, COM812, E501, EM101, TRY003 -- bounded mechanical evidence projections
"""Mechanical capture reconstruction; no gold, relevance or effectiveness decisions."""

from __future__ import annotations

from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.codex_dogfood.case_0012 import amendment
from experiments.codex_dogfood.case_0012.stage_b.canonical import (
    compressed,
    projection_adapter,
)
from experiments.exact_hint_routing import behavior
from experiments.exact_hint_routing.serialization import project

SCORE_TOLERANCE = 1e-10


def lexical_rows(lane: Any) -> list[dict[str, Any]]:
    """Retain every native positive match and its complete score contributions."""
    rows = []
    for rank, match in enumerate(lane.matches, 1):
        r = match.document_statistics.analysis.document.resource
        rows.append(
            {
                "address": str(r.address),
                "content_identity": str(r.content_identity),
                "rank": rank,
                "score": match.score,
                "content_score": match.content_score,
                "filename_score": match.filename_score,
                "filename_weight": match.filename_weight,
                "weighted_filename_score": match.weighted_filename_score,
                "content_terms": project(match.term_contributions),
                "filename_terms": project(match.filename_term_contributions),
            }
        )
    if len({r["address"] for r in rows}) != len(rows):
        raise ValueError("Duplicate native resource")
    for row in rows:
        if (
            row["score"] <= 0
            or abs(row["score"] - row["content_score"] - row["weighted_filename_score"])
            > SCORE_TOLERANCE
        ):
            raise ValueError("Native score identity differs")
    if [r["score"] for r in rows] != sorted((r["score"] for r in rows), reverse=True):
        raise ValueError("Native score order differs")
    return rows


def artifacts(state: dict[str, Any]) -> dict[str, bytes]:  # noqa: C901, PLR0912, PLR0915 -- complete bounded capture partitions
    """Derive every publication from the captured graph, never rerun treatment."""
    values = state["values"]
    frame, treatment = values["frame"], values["treatment"]
    frame.validate()
    operations = state["operations"]
    if len({o["identity"] for o in operations}) != len(operations) or any(
        o["prior_operations"] != [p["identity"] for p in operations[:n]]
        for n, o in enumerate(operations)
    ):
        raise ValueError("Operation chain coverage differs")
    if any(o["invocations"] != 1 or o["status"] != "RETURNED" for o in operations):
        raise ValueError("Invocation/return coverage differs")
    runtime = {o["identity"]: o["runtime_ns"] for o in operations}
    lexical = values["arm:A"]
    expected_keys = {
        "index-build",
        "arm:A",
        "arm:B",
        "arm:C",
        "inventory:B",
        "inventory:C",
        "lexical:global",
        *("lexical:" + o["key"] for o in treatment["obligations"]),
        *(f"route:{arm}:H{n:02}" for arm in ("B", "C") for n in range(1, 11)),
        *(
            f"present:{arm}:{o['key']}"
            for arm in ("B", "C")
            for o in treatment["obligations"]
        ),
    }
    actual_keys = {o["identity"] for o in operations}
    grounding_keys = {k for k in actual_keys if k.startswith("ground:")}
    if actual_keys - grounding_keys != expected_keys:
        raise ValueError("Exactly-once frozen operation coverage differs")
    for arm in ("B", "C"):
        for n, result in enumerate(values["arm:" + arm]["resolutions"], 1):
            key = f"route:{arm}:H{n:02}"
            op = next(o for o in operations if o["identity"] == key)
            if op["inputs"] != project(result.request) or values[key] is not result:
                raise ValueError("Frozen/native exact request identity differs")
            if len(result.native_provenance) != len(
                [k for k in grounding_keys if k.startswith(f"ground:{arm}:H{n:02}:")]
            ):
                raise ValueError("Native grounding subcall coverage differs")
            if {
                **project(result.request),
                "identity": result.request.identity,
            } != treatment["exact_route_requests"][arm][n - 1]:
                raise ValueError("Frozen route request changed")
    query_capture = {
        k: {
            "query_identity": treatment["task_identity"]
            + ("/global" if k == "global" else "/obligation/" + k),
            "query_text": v.query.text,
            "analyzed_terms": list(v.query.normalized_terms),
            "rows": lexical_rows(v),
            "runtime_ns": runtime["lexical:" + k],
        }
        for k, v in lexical.items()
    }
    if set(lexical) != {"global", *(o["key"] for o in treatment["obligations"])}:
        raise ValueError("Query lane coverage differs")
    for o in treatment["obligations"]:
        if query_capture[o["key"]]["query_text"] != o["query"]:
            raise ValueError("Frozen query differs")
    order = {str(r.address): n for n, r in enumerate(frame.snapshot.resources)}
    for capture in query_capture.values():
        if capture["rows"] != sorted(
            capture["rows"], key=lambda r: (-r["score"], order[r["address"]])
        ):
            raise ValueError("Native tie ordering differs")
    if query_capture["global"]["query_text"] != treatment["task_text"]:
        raise ValueError("Global safety query differs")
    projections: dict[str, Any] = {}
    routed: dict[str, Any] = {}
    hint_rows = []
    with projection_adapter():
        for arm in ("B", "C"):
            native = values["arm:" + arm]
            projections[arm] = {
                "resolutions": [
                    behavior.resolution(frame, r) for r in native["resolutions"]
                ],
                "presentations": {
                    k: behavior.presentation(frame, v)
                    for k, v in native["views"].items()
                },
            }
            routed[arm] = {}
            for key, view in native["views"].items():
                if (
                    view.original_lexical_acquisition is not lexical[key]
                    or view.global_lexical_safety_lane is not lexical["global"]
                ):
                    raise ValueError("Native lexical/safety reference changed")
                expected = [
                    m
                    for m in lexical[key].matches
                    if m.document_statistics.analysis.document.resource.address
                    not in {e.resource.address for e in view.exact_first if e.exact}
                ]
                if [
                    e.lexical_result_reference
                    for e in view.exact_first
                    if e.exact is None
                ] != expected:
                    raise ValueError("Lexical fallback differs")
                ranks = {
                    m.document_statistics.analysis.document.resource.address: (n, m)
                    for n, m in enumerate(lexical[key].matches, 1)
                }
                entries = []
                for pos, entry in enumerate(view.exact_first, 1):
                    if (
                        entry.position != pos
                        or frame.snapshot.resource_at(entry.resource.address)
                        != entry.resource
                    ):
                        raise ValueError("Routed occurrence/position differs")
                    rank, match = ranks.get(entry.resource.address, (None, None))
                    if (
                        entry.native_lexical_rank != rank
                        or entry.lexical_result_reference is not match
                    ):
                        raise ValueError("Original rank/match identity lost")
                    entries.append(
                        {
                            "address": str(entry.resource.address),
                            "content_identity": str(entry.resource.content_identity),
                            "position": pos,
                            "native_rank": rank,
                            "exact_tier_position": None
                            if entry.exact is None
                            else entry.exact.exact_tier_position,
                            "originating_hint": None
                            if entry.exact is None
                            else entry.exact.hint.text,
                            "score": None if match is None else match.score,
                            "native_row_reference": None
                            if rank is None
                            else {"lane": key, "rank": rank},
                        }
                    )
                if len({e["address"] for e in entries}) != len(entries) or not set(
                    ranks
                ) <= {e.resource.address for e in view.exact_first}:
                    raise ValueError("Candidate deduplication/reach differs")
                routed[arm][key] = {
                    "entries": entries,
                    "presentation_runtime_ns": runtime[f"present:{arm}:{key}"],
                    "construction_provenance": project(view.provenance),
                }
            for n, result in enumerate(native["resolutions"], 1):
                hint = f"H{n:02}"
                family = next(f for f, ids in amendment.FAMILIES.items() if hint in ids)
                request = result.request
                key = request.association.lane.value
                targets = []
                for r in result.resources:
                    e = next(
                        e
                        for e in routed[arm][key]["entries"]
                        if e["address"] == str(r.address)
                    )
                    targets.append(
                        {
                            "address": str(r.address),
                            "content_identity": str(r.content_identity),
                            "native_rank": e["native_rank"],
                            "exact_tier_position": e["exact_tier_position"],
                            "routed_position": e["position"],
                            "depth_saved": None
                            if e["native_rank"] is None
                            else e["native_rank"] - e["position"],
                        }
                    )
                hint_rows.append(
                    {
                        "arm": arm,
                        "hint": hint,
                        "text": request.hint.text,
                        "span": project(request.hint.span),
                        "hint_identity": request.hint.identity.value,
                        "family": family,
                        "obligation": key,
                        "locator": project(request.locator),
                        "mechanism": request.mechanism,
                        "task_extraction_provenance": project(request.hint),
                        "disposition": result.disposition.value,
                        "reason": result.reason,
                        "targets": targets,
                        "runtime_ns": runtime[f"route:{arm}:{hint}"],
                        "native_evidence_reference": {
                            "artifact": "exact_resolutions.json.gz",
                            "arm": arm,
                            "ordinal": n,
                        },
                        "native_candidates": [
                            p
                            for account in projections[arm]["resolutions"][n - 1][
                                "native_accounts"
                            ]
                            for p in account["candidates"]
                        ],
                        "grounding_accounts": [
                            {
                                "request": project(a.request),
                                "resolver": project(a.resolver),
                                "disposition": a.disposition.value,
                                "native_referents": [
                                    project(c.referent) for c in a.candidates
                                ],
                                "reason": a.reason,
                            }
                            for a in result.native_provenance
                        ],
                    }
                )
        for b, c in zip(
            projections["B"]["resolutions"],
            projections["C"]["resolutions"],
            strict=True,
        ):
            behavior.require_equivalent(b, c)
        for key in projections["B"]["presentations"]:
            behavior.require_equivalent(
                projections["B"]["presentations"][key],
                projections["C"]["presentations"][key],
            )
    if values["arm:B"]["resolutions"] == values["arm:C"]["resolutions"]:
        raise ValueError("Task-extraction provenance was normalized")
    families: dict[str, Any] = {}
    for arm in ("B", "C"):
        families[arm] = {}
        for family, ids in amendment.FAMILIES.items():
            selected = [h for h in hint_rows if h["arm"] == arm and h["hint"] in ids]
            family_lanes = sorted({h["obligation"] for h in selected})
            families[arm][family] = {
                "hint_count": len(selected),
                "obligations": family_lanes,
                "admitted_routes": sum(h["locator"] is not None for h in selected),
                **{
                    s: sum(h["disposition"] == s for h in selected)
                    for s in ("RESOLVED", "AMBIGUOUS", "UNRESOLVED", "UNSUPPORTED")
                },
                "unique_resolved_resources": sorted(
                    {t["address"] for h in selected for t in h["targets"]}
                ),
                "native_ranks": [
                    t["native_rank"] for h in selected for t in h["targets"]
                ],
                "routed_positions": [
                    t["routed_position"] for h in selected for t in h["targets"]
                ],
                "depth_saved": [
                    t["depth_saved"] for h in selected for t in h["targets"]
                ],
                "resolution_ns": sum(h["runtime_ns"] for h in selected),
                "presentation_ns": sum(
                    runtime[f"present:{arm}:{k}"] for k in family_lanes
                ),
                "presentation_cost_scope": "Lane cost shared across families in the same lane; not additive family costs",
                "gold_dependent_fields": "UNAVAILABLE",
            }
    arm_counts = {}
    for arm in ("A", "B", "C"):
        lanes = (
            {k: v["rows"] for k, v in query_capture.items() if k != "global"}
            if arm == "A"
            else {k: v["entries"] for k, v in routed[arm].items()}
        )
        occurrences = sum(len(rows) for rows in lanes.values())
        unique = len({r["address"] for rows in lanes.values() for r in rows})
        arm_counts[arm] = {
            "lanes": {k: len(v) for k, v in lanes.items()},
            "occurrences": occurrences,
            "unique_resources": unique,
            "duplicates": occurrences - unique,
        }
    summary = {
        "stage_a": "FROZEN",
        "stage_b": "CAPTURED",
        "execution": state["marker"]["execution"],
        "operations": len(operations),
        "counts": {
            "index_build": 1,
            "obligation_queries": 9,
            "global_query": 1,
            "admitted_exact_routes": sum(
                o["identity"].startswith("route:")
                and o["inputs"]["locator"] is not None
                for o in operations
            ),
            "unsupported_accounts": 4,
            "native_grounding_subcalls": sum(
                o["identity"].startswith("ground:") for o in operations
            ),
            "presentation_calls": 18,
            "arm_calls": 3,
        },
        "arms": arm_counts,
        "global_positive_rows": len(query_capture["global"]["rows"]),
        "behavioral_resolution_equality": True,
        "behavioral_presentation_equality": True,
        "native_object_equality": False,
        "task_extraction_provenance": "PRESERVED",
        "lexical_fallback": "PRESERVED",
        "global_safety": "PRESERVED",
        "runtime_ns": runtime,
        "runtime_scope": "Single measured execution; not a latency benchmark. runtime_ns excludes measured nested checkpoint/serialization overhead; wall_call_ns and durability_inside_call_ns retained per operation. Arm totals include child native runtimes and must not be summed with children. Finalization/behavioral validation is not treatment time.",
        "families": families,
        "hint_rows": hint_rows,
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "final_u2_outcome": "NOT_SELECTED",
        "search_policy_failure": "NOT_ASSESSED",
    }
    native_exact = {arm: values["arm:" + arm]["resolutions"] for arm in ("B", "C")}
    trace = {
        "schema": "case-0012-stage-b-trace-v1",
        "stage_a_layer": "../trace.json",
        "stage_a_layer_sha256": state["marker"]["stage_a_trace_sha256"],
        "stage_b": summary,
        "lexical": query_capture,
        "routed": routed,
    }
    return {
        "summary.json": json_bytes(summary),
        "lexical.json": json_bytes(query_capture),
        "arm_a.json": json_bytes(
            {k: v for k, v in query_capture.items() if k != "global"}
        ),
        "arm_b.json": json_bytes(routed["B"]),
        "arm_c.json": json_bytes(routed["C"]),
        "behavior_b.json": json_bytes(projections["B"]),
        "behavior_c.json": json_bytes(projections["C"]),
        "exact_resolutions.json.gz": compressed(native_exact),
        "route_families.json": json_bytes(families),
        "TRACE.md": review(treatment, summary, query_capture, routed).encode(),
        "STAGE_B_REVIEW.md": review(treatment, summary, query_capture, routed).encode(),
        "trace.json": json_bytes(trace),
        "operations.json": json_bytes(operations),
        "native_lexical.json": json_bytes(
            {
                "source": "raw_checkpoint.json authenticated native graph",
                "sections": ["values.lexical:" + k for k in lexical],
                "original_objects_preserved": True,
            }
        ),
        "VALIDATION.md": b"# Capture validation\n\nDurable native checkpoint replay; operation counts; B/C frozen behavioral equality; complete lexical fallback/native scores/contributions; global safety; exact-frame identity and deterministic publication PASS. No gold or outcome selected.\n",
    }


def review(
    treatment: dict[str, Any],
    summary: dict[str, Any],
    lexical: dict[str, Any],
    routed: dict[str, Any],
) -> str:
    """Expose all ranked rows and causal route evidence without gold labels."""
    import json  # noqa: PLC0415

    lines = [
        "# Case 0012 Stage B mechanical review",
        "",
        "GOLD = ABSENT; EFFECTIVENESS = UNKNOWN; FINAL U2 OUTCOME = NOT SELECTED; SEARCH_POLICY_FAILURE = NOT_ASSESSED.",
        "",
        "Native B/C authorship is preserved and differs; frozen behavioral projection equality PASS. No route-family empirical-support conclusion. H03 choices-only; H05/H06 unsupported and unpromoted. Global safety is unchanged and separate from Arm A's obligation baseline.",
        "",
        "## Original task",
        "",
        "```text",
        treatment["task_text"].rstrip(),
        "```",
        "",
        "## Complete hint and family mechanics",
        "",
        "```json",
        json.dumps(
            {
                "hints": summary["hint_rows"],
                "families": summary["families"],
                "runtime_ns": summary["runtime_ns"],
            },
            indent=2,
        ),
        "```",
        "",
        "Full native candidates, source selection/grounding evidence and repository provenance are retained in exact_resolutions.json.gz; each hint provides its exact arm/ordinal. Raw checkpoint retains original objects and all intermediate native grounding returns.",
        "",
    ]
    for o in treatment["obligations"]:
        key = o["key"]
        lines += [
            "## " + key,
            "",
            o["statement"],
            "",
            "Criterion: " + o["criterion"],
            "",
            "Exact query: `" + o["query"] + "`",
            "",
            "Analyzed terms: " + json.dumps(lexical[key]["analyzed_terms"]),
            "",
            f"Complete positive rows: {len(lexical[key]['rows'])}; query runtime ns: {lexical[key]['runtime_ns']}",
            "",
            "### Arm A complete ranking (first ten are the top results)",
            "",
            "| Rank | Resource | Score | Content | Weighted filename |",
            "| --- | --- | --- | --- | --- |",
        ]
        lines += [
            f"| {r['rank']} | {r['address']} | {r['score']:.17g} | {r['content_score']:.17g} | {r['weighted_filename_score']:.17g} |"
            for r in lexical[key]["rows"]
        ]
        lines += [
            "",
            "All term contributions are in lexical.json at this lane/rank.",
            "",
        ]
        for arm in ("B", "C"):
            lines += [
                "### Arm " + arm + " complete exact-first presentation",
                "",
                "| Position | Resource | Exact tier | Native rank | Score |",
                "| --- | --- | --- | --- | --- |",
            ]
            lines += [
                f"| {r['position']} | {r['address']} | {r['exact_tier_position']} | {r['native_rank']} | {r['score']} |"
                for r in routed[arm][key]["entries"]
            ]
            lines += [""]
    lines += [
        "## Global safety lane",
        "",
        f"Positive rows: {len(lexical['global']['rows'])}; unchanged full-task query and complete ranking retained in lexical.json/global.",
        "",
        "Next: maintainer reviews this trace, then a completely fresh sterile Stage C session adjudicates independent truth. No adjudication occurs here.",
    ]
    return "\n".join(lines).rstrip() + "\n"

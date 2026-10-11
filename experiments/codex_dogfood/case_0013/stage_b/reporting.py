# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, TRY003, PLR2004 -- complete frozen mechanical JSON boundary
"""Validate captured native mechanics and render every lane without gold analysis."""

from __future__ import annotations

import gzip
import json
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.codex_dogfood.case_0012.stage_b.graph import describe
from experiments.codex_dogfood.case_0012.stage_b.reporting import lexical_rows
from experiments.exact_hint_routing.models import ResolutionDisposition
from experiments.exact_hint_routing.serialization import project

FAMILIES = (
    "RESOURCE_ADDRESS",
    "PYTHON_MODULE",
    "PYTHON_DIRECT_FUNCTION",
    "PYTHON_DIRECT_CLASS",
    "PYTHON_DIRECT_METHOD",
)


def artifacts(state: dict[str, Any]) -> dict[str, bytes]:  # noqa: C901, PLR0912, PLR0915 -- explicit complete mechanical invariants
    """Reconstruct only from returned native values, preserving original aliases."""
    v, operations = state["values"], state["operations"]
    t, frame = v["treatment"], v["frame:assembly"]
    frame.validate()
    runtime = {o["identity"]: o["runtime_ns"] for o in operations}
    expected = {
        "frame:resources",
        "frame:modules",
        "frame:declarations",
        "frame:assembly",
        "index-build",
        "arm:A",
        "arm:B",
        "arm:C",
        "purposes:shared",
        "policy:B",
        "policy:C",
        *("lexical:" + k for k in ("global", *[o["key"] for o in t["obligations"]])),
    }
    # Frozen requests identify hints by the nested task observation identity.
    hint_keys = {h["identity"]["value"]: h["key"] for h in t["hint_inventory"]}
    expected.update(
        f"route:{a}:{hint_keys[r['association']['hint']['value']]}"
        for a in ("B", "C")
        for r in t["exact_route_requests"][a]
    )
    expected.update(
        f"present:{a}:{o['key']}" for a in ("B", "C") for o in t["obligations"]
    )
    ground_keys = {k for k in runtime if k.startswith("ground:")}
    if (
        set(runtime) - ground_keys != expected
        or len(runtime) != len(operations)
        or any(
            o["invocations"] != 1
            or o["status"] != "RETURNED"
            or o["prior_operations"] != [p["identity"] for p in operations[:n]]
            for n, o in enumerate(operations)
        )
    ):
        raise ValueError("Exactly-once operation schedule differs")
    lexical = v["arm:A"]
    if set(lexical) != {"global", *[o["key"] for o in t["obligations"]]}:
        raise ValueError("Captured lexical lanes differ")
    order = {str(r.address): n for n, r in enumerate(frame.snapshot.resources)}
    queries = {
        "global": t["global_safety_query"]["text"],
        **{o["key"]: o["query"] for o in t["obligations"]},
    }
    query_capture = {}
    for k, lane in lexical.items():
        if (
            lane is not v["lexical:" + k]
            or lane.index is not v["index-build"]
            or lane.query.text != queries[k]
            or lane.maximum_results != len(frame.snapshot.resources)
        ):
            raise ValueError("Native lexical identity/query/index differs")
        if (lane.settings.k1, lane.settings.b) != (
            1.2,
            0.75,
        ):
            raise ValueError("Native BM25 settings differ")
        rows = lexical_rows(lane)
        if any(row["filename_weight"] != 0.25 for row in rows):
            raise ValueError("Native filename weight differs")
        if rows != sorted(rows, key=lambda r: (-r["score"], order[r["address"]])):
            raise ValueError("Native tie order differs")
        query_capture[k] = {
            "query_text": lane.query.text,
            "query_identity": t["task_identity"]
            + ("/global" if k == "global" else "/obligation/" + k),
            "analyzed_terms": list(lane.query.normalized_terms),
            "rows": rows,
            "runtime_ns": runtime["lexical:" + k],
        }
    routed: dict[str, Any] = {}
    hint_rows: list[dict[str, Any]] = []
    policy_capture: dict[str, Any] = {}
    exact_by_arm = {}
    for a in ("B", "C"):
        arm = v["arm:" + a]
        plan = arm["policy"]
        policy_capture[a] = [{"identity": d.identity, **project(d)} for d in plan]
        if plan is not v["policy:" + a] or policy_capture[a] != t["route_decisions"][a]:
            raise ValueError("Captured frozen policy differs")
        exact_by_arm[a] = arm["resolutions"]
        if [
            {"identity": r.request.identity, **project(r.request)}
            for r in arm["resolutions"]
        ] != t["exact_route_requests"][a]:
            raise ValueError("Frozen exact request set differs")
        routed[a] = {}
        for o in t["obligations"]:
            key = o["key"]
            view = arm["views"][key]
            if (
                view is not v[f"present:{a}:{key}"]
                or view.original_lexical_acquisition is not lexical[key]
                or view.global_lexical_safety_lane is not lexical["global"]
            ):
                raise ValueError("Original lexical/global alias lost")
            resolutions = tuple(
                r for r in arm["resolutions"] if r.request.association.lane.value == key
            )
            if view.exact_resolutions != resolutions or any(
                x is not y
                for x, y in zip(view.exact_resolutions, resolutions, strict=True)
            ):
                raise ValueError("Native lane exact capture differs")
            positive = {
                m.document_statistics.analysis.document.resource.address: (n, m)
                for n, m in enumerate(lexical[key].matches, 1)
            }
            promoted = []
            for r in sorted(
                resolutions,
                key=lambda r: (
                    r.request.hint.span.start,
                    r.request.hint.span.end,
                    r.request.identity,
                ),
            ):
                if (
                    r.repository_id != frame.repository_id
                    or r.snapshot_id != frame.snapshot_id
                    or r.frame_identity != frame.identity
                ):
                    raise ValueError("Foreign exact outcome")
                if r.disposition is ResolutionDisposition.RESOLVED:
                    if len(r.resources) != 1 or not r.native_provenance:
                        raise ValueError("Unsound resolved promotion")
                    resource = r.resources[0]
                    if resource not in promoted:
                        promoted.append(resource)
                elif r.resources:
                    raise ValueError("Nonresolved promotion")
            expected_resources = promoted + [
                m.document_statistics.analysis.document.resource
                for m in lexical[key].matches
                if m.document_statistics.analysis.document.resource not in promoted
            ]
            if [e.resource for e in view.exact_first] != expected_resources:
                raise ValueError("Exact-first order/fallback loss")
            entries = []
            for pos, e in enumerate(view.exact_first, 1):
                rank, match = positive.get(e.resource.address, (None, None))
                if (
                    e.position != pos
                    or e.native_lexical_rank != rank
                    or e.lexical_result_reference is not match
                    or frame.snapshot.resource_at(e.resource.address) != e.resource
                ):
                    raise ValueError(
                        "Rank/score/contribution/resource preservation differs"
                    )
                if (pos <= len(promoted)) != (e.exact is not None) or (
                    e.exact is not None and e.exact.exact_tier_position != pos
                ):
                    raise ValueError("Exact tier position differs")
                entries.append(
                    {
                        "address": str(e.resource.address),
                        "content_identity": str(e.resource.content_identity),
                        "position": pos,
                        "native_rank": rank,
                        "exact_tier_position": None
                        if e.exact is None
                        else e.exact.exact_tier_position,
                        "score": None if match is None else match.score,
                        "native_row_reference": None
                        if rank is None
                        else {"lane": key, "rank": rank},
                        "originating_hint": None
                        if e.exact is None
                        else e.exact.hint.text,
                    }
                )
            if len({e.resource.address for e in view.exact_first}) != len(
                view.exact_first
            ) or not set(positive) <= {e.resource.address for e in view.exact_first}:
                raise ValueError("Candidate loss or duplicate")
            routed[a][key] = {
                "entries": entries,
                "presentation_runtime_ns": runtime[f"present:{a}:{key}"],
                "provenance": project(view.provenance),
            }
        for ordinal, r in enumerate(arm["resolutions"], 1):
            h = hint_keys[r.request.hint.identity.value]
            opkey = f"route:{a}:{h}"
            operation = next(o for o in operations if o["identity"] == opkey)
            if v[opkey] is not r or operation["inputs"] != {
                "arm": a,
                "request": project(r.request),
                "request_identity": r.request.identity,
            }:
                raise ValueError("Arm-bound native route account differs")
            if len(r.native_provenance) != sum(
                k.startswith(f"ground:{a}:{h}:") for k in ground_keys
            ):
                raise ValueError("Grounding subcall coverage differs")
            basis = next(
                d.basis
                for d in plan
                if d.request is not None and d.request.identity == r.request.identity
            )
            key = r.request.association.lane.value
            targets = []
            for resource in r.resources:
                e = next(
                    e
                    for e in routed[a][key]["entries"]
                    if e["address"] == str(resource.address)
                )
                targets.append(
                    {
                        "address": str(resource.address),
                        "content_identity": str(resource.content_identity),
                        "native_rank": e["native_rank"],
                        "exact_tier_position": e["exact_tier_position"],
                        "routed_position": e["position"],
                        "depth_saved": None
                        if e["native_rank"] is None
                        else e["native_rank"] - e["position"],
                    }
                )
            accounts = [
                {
                    "request": project(account.request),
                    "resolver": project(account.resolver),
                    "disposition": account.disposition.value,
                    "reason": account.reason,
                    "candidates": [
                        {
                            "referent": project(c.referent),
                            "evidence_type": type(c.evidence).__module__
                            + "."
                            + type(c.evidence).__qualname__,
                        }
                        for c in account.candidates
                    ],
                    "complete_native_evidence": {
                        "artifact": "exact_resolutions.json.gz",
                        "arm": a,
                        "ordinal": ordinal,
                        "graph_sha256": digest(json_bytes(describe(account))),
                    },
                }
                for account in r.native_provenance
            ]
            hint_rows.append(
                {
                    "arm": a,
                    "hint": h,
                    "hint_identity": r.request.hint.identity.value,
                    "text": r.request.hint.text,
                    "span": project(r.request.hint.span),
                    "family": r.request.hint.category.value,
                    "obligation": key,
                    "purpose": basis.need.statement,
                    "role": basis.role.value,
                    "locator": project(r.request.locator),
                    "mechanism": r.request.mechanism,
                    "request_identity": r.request.identity,
                    "disposition": r.disposition.value,
                    "reason": r.reason,
                    "targets": targets,
                    "native_accounts": accounts,
                    "runtime_ns": runtime[opkey],
                }
            )
    for c in exact_by_arm["C"]:
        b = next(
            r for r in exact_by_arm["B"] if r.request.identity == c.request.identity
        )
        if b is c or any(
            x is y
            for x, y in zip(b.native_provenance, c.native_provenance, strict=True)
        ):
            raise ValueError("Cross-arm exact outcome reuse")
    skipped = []
    for d in v["arm:C"]["policy"]:
        if d.basis.hint is None or d.request is not None:
            continue
        h = hint_keys[d.basis.hint.identity.value]
        b = next(row for row in hint_rows if row["arm"] == "B" and row["hint"] == h)
        skipped.append(
            {
                "hint": h,
                "hint_identity": d.basis.hint.identity.value,
                "role": d.basis.role.value,
                "purpose": d.basis.need.statement,
                "C_disposition": d.disposition,
                "C_native_outcome": None,
                "C_invocations": 0,
                "B_mechanism": b["mechanism"],
                "B_locator": b["locator"],
                "B_disposition": b["disposition"],
                "B_targets": b["targets"],
                "scope": "Intentionally not invoked in C; no effectiveness classification",
            }
        )
    families: dict[str, Any] = {}
    for a in ("B", "C"):
        families[a] = {}
        for f in FAMILIES:
            hs = [row for row in hint_rows if row["arm"] == a and row["family"] == f]
            family_lanes = sorted({row["obligation"] for row in hs})
            families[a][f] = {
                "hint_count": sum(h["category"] == f for h in t["hint_inventory"]),
                "admitted_requests": len(hs),
                **{
                    s: sum(row["disposition"] == s for row in hs)
                    for s in ("RESOLVED", "AMBIGUOUS", "UNRESOLVED", "UNSUPPORTED")
                },
                "unique_resolved_resources": sorted(
                    {target["address"] for row in hs for target in row["targets"]}
                ),
                "target_positions": [
                    {"hint": row["hint"], **target}
                    for row in hs
                    for target in row["targets"]
                ],
                "route_ns": sum(row["runtime_ns"] for row in hs),
                "presentation_ns": sum(
                    runtime[f"present:{a}:{key}"] for key in family_lanes
                ),
                "presentation_scope": "Full lane timings; shared across families in same lane, not additive family costs",
            }
    counts = {}
    for a in ("A", "B", "C"):
        lanes = (
            {k: query_capture[k]["rows"] for k in queries if k != "global"}
            if a == "A"
            else {k: routed[a][k]["entries"] for k in routed[a]}
        )
        occurrences = sum(len(rows) for rows in lanes.values())
        unique = len({row["address"] for rows in lanes.values() for row in rows})
        counts[a] = {
            "lanes": {k: len(rows) for k, rows in lanes.items()},
            "occurrences": occurrences,
            "unique_resources": unique,
            "duplicates_across_lanes": occurrences - unique,
        }
    common_index = runtime["index-build"]
    common_queries = sum(runtime["lexical:" + k] for k in queries)
    costs = {
        "common_frame_preparation_ns": {
            k: runtime[k]
            for k in (
                "frame:resources",
                "frame:modules",
                "frame:declarations",
                "frame:assembly",
            )
        },
        "native_index_ns": common_index,
        "shared_queries_ns": common_queries,
        "shared_purposes_hint_extraction_ns": runtime["purposes:shared"],
        "arm_A_assembly_ns": runtime["arm:A"],
        "arms": {},
        "scope": "Single-run captured ns. Composite includes children and excludes measured nested journal overhead; composite and child timings never added together. Frame/publication/durability separate from charged totals.",
    }
    for a in ("A", "B", "C"):
        routes = sum(row["runtime_ns"] for row in hint_rows if row["arm"] == a)
        presentation = sum(
            runtime.get(f"present:{a}:{key}", 0) for key in routed.get(a, {})
        )
        policy = runtime.get("policy:" + a, 0)
        purposes = 0 if a == "A" else runtime["purposes:shared"]
        costs["arms"][a] = {
            "policy_ns": policy,
            "route_ns": routes,
            "presentation_ns": presentation,
            "mechanism_ns": routes + presentation,
            "charged_ns": common_index
            + common_queries
            + purposes
            + policy
            + routes
            + presentation,
            "composite_ns": runtime["arm:" + a],
            "composite_wall_ns": next(
                o["wall_call_ns"] for o in operations if o["identity"] == "arm:" + a
            ),
        }
    summary = {
        "stage_a": "FROZEN",
        "stage_b": "CAPTURED",
        "execution": state["marker"]["execution"],
        "scope": "TASK-ROLE-CONDITIONED EXACT-ROUTE ADMISSION",
        "counts": {
            "index_builds": 1,
            "obligation_queries": len(t["obligations"]),
            "global_queries": 1,
            "A_exact_requests": 0,
            "B_exact_requests": len(exact_by_arm["B"]),
            "C_exact_requests": len(exact_by_arm["C"]),
            "native_grounding_subcalls": len(ground_keys),
            "presentation_calls": 2 * len(t["obligations"]),
            "arm_calls": 3,
            "operations": len(operations),
        },
        "arms": counts,
        "global_positive_rows": len(query_capture["global"]["rows"]),
        "hint_rows": hint_rows,
        "C_skipped": skipped,
        "families": families,
        "costs": costs,
        "runtime_ns": runtime,
        "lexical_fallback": "PRESERVED",
        "global_safety": "PRESERVED",
        "native_rank_score_contributions": "PRESERVED",
        "cross_arm_exact_outcomes": "INDEPENDENT",
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "u3_outcome": "NOT_SELECTED",
        "search_policy_failure": "NOT_ASSESSED",
        "admission_scope": "B-to-C 10-to-6 is a frozen policy difference, not effectiveness evidence",
    }
    trace = {
        "schema": "case-0013-stage-b-trace-v1",
        "stage_a_trace_sha256": state["marker"]["stage_a_trace_sha256"],
        "task": t["task_text"],
        "obligations": t["obligations"],
        "purposes": t["acquisition_intents"],
        "hints": t["hint_inventory"],
        "roles": t["intent_taxonomy"],
        "route_policy": policy_capture,
        "summary": summary,
        "lexical": query_capture,
        "routed": routed,
    }
    review_text = review(trace)
    return {
        "summary.json": json_bytes(summary),
        "lexical.json": json_bytes(query_capture),
        "native_lexical.json.gz": gzip.compress(json_bytes(describe(lexical)), mtime=0),
        "exact_resolutions.json.gz": gzip.compress(
            json_bytes(describe(exact_by_arm)), mtime=0
        ),
        "arm_a.json": json_bytes(
            {k: row for k, row in query_capture.items() if k != "global"}
        ),
        "arm_b.json": json_bytes(routed["B"]),
        "arm_c.json": json_bytes(routed["C"]),
        "route_policy.json": json_bytes(policy_capture),
        "route_families.json": json_bytes(families),
        "costs.json": json_bytes(costs),
        "operations.json": json_bytes(operations),
        "trace.json": json_bytes(trace),
        "TRACE.md": review_text.encode(),
        "STAGE_B_REVIEW.md": review_text.encode(),
        "validation.json": json_bytes(
            {
                "mechanical_capture": "PASS",
                "exactly_once_schedule": "PASS",
                "cross_arm_outcomes": "INDEPENDENT",
                "frame_query_native_identity": "PASS",
                "fallback_rank_score_contributions": "PASS",
                "global_safety": "PASS",
                "serialization_reconstruction": "PASS",
                "gold": "ABSENT",
                "effectiveness": "UNKNOWN",
                "u3_outcome": "NOT_SELECTED",
            }
        ),
    }


def review(trace: dict[str, Any]) -> str:
    """Expose every mechanical row and exact native account reference."""
    s = trace["summary"]
    lines = [
        "# Case 0013 Stage B mechanical review",
        "",
        "**GOLD = ABSENT; EFFECTIVENESS = UNKNOWN; U3 OUTCOME = NOT_SELECTED.**",
        "",
        "**B→C INVOCATION REDUCTION IS A FROZEN POLICY DIFFERENCE, NOT EFFECTIVENESS EVIDENCE BY ITSELF.**",
        "",
        "Scope: TASK-ROLE-CONDITIONED EXACT-ROUTE ADMISSION, first U3 slice. No universal, optimal, graph, semantic, learned or sequential routing claim. SEARCH_POLICY_FAILURE=NOT_ASSESSED.",
        "",
        "## Exact task",
        "",
        "```text",
        trace["task"].rstrip(),
        "```",
        "",
        "## Purposes, hints, roles and frozen policy",
        "",
        "```json",
        json.dumps(
            {k: trace[k] for k in ("purposes", "hints", "roles", "route_policy")},
            indent=2,
        ),
        "```",
        "",
        "## Every exact native outcome and skipped C request",
        "",
        "```json",
        json.dumps({"outcomes": s["hint_rows"], "C_skipped": s["C_skipped"]}, indent=2),
        "```",
        "",
        "Native complete repository evidence/provenance is in exact_resolutions.json.gz, a canonical native graph with type/field/order/alias preservation, and immutable operations/*.returned.json. These are capture codecs, never blind inputs.",
        "",
        "## Family mechanics, counts and costs",
        "",
        "```json",
        json.dumps(
            {
                k: s[k]
                for k in (
                    "families",
                    "counts",
                    "arms",
                    "global_positive_rows",
                    "costs",
                    "runtime_ns",
                )
            },
            indent=2,
        ),
        "```",
        "",
        "Family presentation timings overlap when families share a lane; do not add them. Method grounding and arm composite timings contain children; charged totals use nonoverlapping top-level resolution/presentation/policy plus common lexical costs. Durability/publication is separate.",
        "",
    ]
    for o in trace["obligations"]:
        k = o["key"]
        lane = trace["lexical"][k]
        lines += [
            "## " + k,
            "",
            o["statement"],
            "",
            "Criterion: " + o["criterion"],
            "",
            "Frozen query: `" + lane["query_text"] + "`",
            "",
            "### Arm A complete positive ranking",
            "",
            "| Rank | Resource | Score | Content | Weighted filename |",
            "| --- | --- | --- | --- | --- |",
        ]
        lines += [
            f"| {r['rank']} | {r['address']} | {r['score']:.17g} | {r['content_score']:.17g} | {r['weighted_filename_score']:.17g} |"
            for r in lane["rows"]
        ]
        lines += [
            "",
            "Every content/filename contribution is queryable in lexical.json at this exact lane/rank.",
            "",
        ]
        for a in ("B", "C"):
            lines += [
                "### Arm " + a + " complete presentation",
                "",
                "| Position | Resource | Exact tier | Native rank/miss | Score |",
                "| --- | --- | --- | --- | --- |",
            ]
            lines += [
                f"| {e['position']} | {e['address']} | {e['exact_tier_position']} | {e['native_rank']} | {e['score']} |"
                for e in trace["routed"][a][k]["entries"]
            ]
            lines += [""]
    lines += [
        "## Global safety lane",
        "",
        "| Rank | Resource | Score |",
        "| --- | --- | --- |",
    ]
    lines += [
        f"| {r['rank']} | {r['address']} | {r['score']:.17g} |"
        for r in trace["lexical"]["global"]["rows"]
    ]
    lines += [
        "",
        "Global task query, native index/settings, ranks and contributions remain unchanged in all arms. No task-global acquisition order or witness interpretation is invented.",
        "",
        "Next: maintainer reviews this record, then one completely fresh GPT-6 Astra / High sterile session performs treatment-blind gold. No gold or effectiveness is created here.",
        "",
    ]
    return "\n".join(lines)

# Copyright (c) 2026
# ruff: noqa: E501, RUF001 -- mathematical notation in scientific review prose
"""Render exact inputs, responsibility, rankings and case-local conclusions."""

from __future__ import annotations

import json
from typing import Any

from experiments.codex_dogfood.case_0011.stage_d.metrics import LABELS, explain, label

MISSING = {
    "U02": "No need seeks the complete qualified admission/re-admission contract: purpose, derivation/coverage, analysis membership, target type and route checks.",
    "U03": "The entry-point question leaves pre-collection exclusion, retained pytest/100% branch gate, exit status and confirmation-authorization boundary unrequested as a complete contract.",
    "U04": "Rendered/copied Context documentation questions do not seek the complete materialization/native-provenance/two-choice contract and current-versus-future budget distinction.",
    "U07": "Strictly neither frame binding nor item retention alone seeks both validated source/target bindings and renderer/text/native-value handoff; the accepted N09/N10 collective set repairs only the secondary diagnostic.",
    "U10": "Frame checks/item retention do not seek the complete ordered realization, returned identity/representation validation and all-items-success-before-publication contract.",
    "U12": "The validation entry/configuration questions do not seek every separate lint, format, mypy and unstaged/staged diff-check instruction.",
    "U14": "Frame-binding/item-retention questions do not seek all plan-construction rejections: blank purpose, empty/duplicate choices and mixed purposes/frames.",
    "U15": "Owner/dependency questions do not require the complete exact import/type-only ContextDisclosure contract together with absence of adapter/Retrieval imports.",
    "U16": "Assembly rejection/ownership questions leave the entire existing keyword-only RenderedContextDisclosure signature, absence of a limit and final replace-only publication point incomplete.",
    "U17": "Boundary/task-preservation questions do not require both unchanged outer envelopes, separately reported Context/task byte lengths and all embedded newline bytes as one complete fact.",
    "U19": "No need seeks qualified test-option construction through module interpretation and production reference analysis before retained-reference choice.",
    "U20": "The public planning-package inventory does not require the complete outer Context facade imports and __all__ companion exports.",
    "U24": "Generic frame binding does not require every target support/declaration-analysis frame and declaration-membership check.",
    "U25": "Assembly ownership does not require the complete ordered planning/faithful-realization/rendering/assembly lifecycle and independence from automatic selection.",
    "U28": "Neither frame-binding nor item-retention singleton seeks the complete whole-resource validation plus unchanged-content/identity/native-occurrence retention; N09/N10 is collectively sufficient only diagnostically.",
    "U30": "Neither singleton seeks every immutable item field and ContextDisclosure ordered plan/item agreement; N09/N10 establishes the full fact collectively only in the secondary diagnostic.",
    "U32": "Focused text/frame/preservation questions do not require the entire mixed-plan CRLF/non-ASCII fixture plus exact-source, native whole-resource provenance and ordered-render assertions.",
}


def table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    """Render finite tables with safe literal cells."""

    def cell(v: object) -> str:
        return str(v).replace("|", "\\|").replace("\n", "<br>").replace("\r", "")

    return [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        *("| " + " | ".join(cell(v) for v in row) + " |" for row in rows),
        "",
    ]


def metrics(b: dict[str, Any]) -> list[Any]:
    """Use the same visible burden columns throughout."""
    return [
        b["occurrences"],
        b["unique_resources"],
        b["duplicates"],
        *(b["occurrence_labels"][k] for k in LABELS),
        b["utf8_bytes"],
    ]


def enrich(d: dict[str, Any], s: dict[str, Any]) -> dict[str, Any]:
    """Add a distinct D layer while retaining links to immutable A/B bytes."""
    queries = []
    for qid, q in s["queries"].items():
        capture = s["capture"]["queries"][qid]
        related = [
            u
            for u in d["unit_failures"]
            if q["arm"] == "A"
            or (q["arm"] == "B" and q["obligation"] in u["obligations"])
            or (
                q["arm"] == "C"
                and q["information_need"] in u["direct_needs"] + u["partial_needs"]
            )
        ]
        resources = sorted({p for u in related for p in u["resources"]})
        queries.append(
            {
                **q,
                "captured_query_text": capture["query_text"],
                "execution_count": capture["execution_count"],
                "capture_binding": {
                    "artifact": "../results.json.gz",
                    "archive_sha256": s["projection"].get(
                        "retrieval_archive_sha256",
                        d["provenance"]["chain"][1]["artifact_sha256"][
                            "experiments/codex_dogfood/case_0011/results.json.gz"
                        ],
                    ),
                    "query_identity": qid,
                },
                "query_seconds": d["arms"][q["arm"]]["query_costs"][qid],
                "reviewed_query_profile": d["diagnostics"]["query_profiles"][qid],
                "ranked_results": [
                    {**r, "reviewed_label": label(s, q["obligation"], r["address"])}
                    for r in capture["rows"]
                ],
                "required_unit_links": [u["unit"] for u in related],
                "required_resource_inspection": [
                    explain(s, qid, p, q["obligation"]) for p in resources
                ],
                "completion_status": d["arms"]["C"]["completion"]["semantic_completion"]
                if q["arm"] == "C"
                else "COMPLETE_VALID_ALTERNATIVE",
                "strict_responsible_prefix_depth": d["strict_subset"]["C"][
                    "prefix_depths"
                ].get(qid, 0)
                if q["arm"] == "C"
                else None,
                "granularity_responsible_prefix_depth": d["granularity_subset"]["C"][
                    "prefix_depths"
                ].get(qid, 0)
                if q["arm"] == "C"
                else None,
                "direct_subset_status": "COMPLETE_RESPONSIBLE_DIRECT_SUBSET"
                if q["arm"] == "C" and qid in d["strict_subset"]["C"]["prefix_depths"]
                else "NO_DIRECT_RESPONSIBILITY"
                if q["arm"] == "C"
                else None,
                "failure_classes": sorted({u["earliest_failure"] for u in related}),
            },
        )
    return {
        "schema": "case-0011-stage-d-trace-v1",
        "join_integrity": d["join_integrity"],
        "frozen_trace_layers": {
            "A": "../stage_a_trace.json",
            "B": "../trace.json",
            "human_B": "../TRACE.md",
            "mutated": False,
        },
        "original_task": s["treatment"]["task"],
        "task_basis_and_obligations": s["treatment"]["obligations"],
        "reviewed_required_units": [
            {**u, "missing_semantic_component_summary": MISSING.get(u["alias"])}
            for u in d["unit_failures"]
        ],
        "information_needs": s["treatment"]["information_needs"],
        "reviewed_need_classifications": s["semantic"]["need_classifications"],
        "reviewed_need_unit_mappings": s["semantic"]["mappings"],
        "collective_sets": s["semantic"]["collective_coverage"],
        "queries": queries,
        "strict_subset": d["strict_subset"],
        "granularity_subset": d["granularity_subset"],
        "diagnostics": d["diagnostics"],
        "final_outcome": d["outcome"],
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
    }


def report(d: dict[str, Any]) -> str:
    """Summarize the joined result with complete numerical and semantic surfaces."""
    a, b = d["arms"]["A"]["completion"], d["arms"]["B"]["completion"]
    strict, gran = d["strict_subset"], d["granularity_subset"]
    lines = [
        "# Case 0011 Stage D",
        "",
        "## Join integrity — PASSED",
        "",
        "Case/task/RepositoryId/SnapshotId/CorpusId, 531 resource/content identities, nine obligations, 4,779 cells, 32 exact reviewed unit identities/statements, 18 exact needs and 576 pair mappings join without duplicate, missing or unexpected entries. All 28 captured literal queries ran once and retain exact route, terms, ranks, scores, contributions and tie order. No retrieval was rerun.",
        "",
        "Frozen chain ancestry and exact selected committed blobs pass. Stage A's C5_PROTOCOL.md placeholder was intentionally superseded at 918e90bc; both protocol versions are pinned at their proper commits. The primary C.5 PUBLICATION.md also gained a historical-status preface at 53e1681; both committed versions are authenticated separately from immutable adjudication data. The original Stage A current-worktree verifier cannot replay the superseded placeholder; Stage D retains scientific checks and authenticates the documented history. No frozen treatment, gold, mapping or A/B trace changed.",
        "",
        "```json",
        json.dumps(d["join_integrity"], indent=2),
        "```",
        "",
        "## DID WE IMPROVE?",
        "",
        f"**Frozen outcome: {d['outcome']}.** Two completely unrequested units (U02/U19) trigger the literal omitted-unit precedence. Partial coverage alone does not imply a MISFORMULATED need. This one need set provides local rank gains but worsens aggregate responsible subset burden and fails full semantic completeness.",
        "",
    ]
    lines += table(
        ["Dimension", "Observed result"],
        [
            [
                "Semantic completeness",
                "Strict C: 15/32 units and 0/12 alternatives; secondary collective diagnostic: 18/32 and 0/12. Neither completes any obligation.",
            ],
            [
                "Required reach",
                "A/B/C all reach 16 resources, 23 owning cells, 32 distinct units (34 obligation/unit pairs), 15 indispensable resources. No reach rescue or loss.",
            ],
            [
                "Covered-unit depth",
                "C improves 5 and regresses 10 against B; no ties/misses. U26 retains both B owning lanes separately.",
            ],
            [
                "Unique prefix union",
                "A→B: 370→269 (-101, -27.297%). Same 15-unit B→C: 220→371 (+151, +68.636%).",
            ],
            [
                "Unnecessary prefix occurrences",
                "A→B: 331→513 (+182, +54.985%); labels use global scope for A and owning obligation scope for B. Same-subset B→C: 337→737 (+400, +118.694%).",
            ],
            [
                "Execution cost",
                "A/B/C: 1/9/18 queries; 0.021986300 / 0.066727000 / 0.159203800 seconds. C costs +0.092476800 seconds (+138.590%) over B.",
            ],
            [
                "Raw candidate duplication",
                "A/B/C: 0 / 2,039 / 4,269 duplicate occurrences. C adds 2,230 duplicates to B.",
            ],
            [
                "Content volume",
                "A→B: 3,104,937→2,656,630 bytes (-448,307, -14.438%). Same-subset B→C: 2,315,351→2,689,816 bytes (+374,465, +16.173%).",
            ],
        ],
    )
    lines += [
        "All prefix metrics describe **counterfactual completion-prefix inspection burden**. Actual evidence-inspection cost is **NOT MEASURED**. Positive counts, raw recall and prefix volumes are separate measurements.",
        "",
        "### Exact magnitude of each burden change",
        "",
    ]
    for name, changes in d["comparisons"].items():
        lines += [f"#### {name}", ""]
        lines += table(
            ["Metric", "Baseline", "Changed", "Delta", "Percent change", "Result"],
            [
                [
                    key,
                    value["baseline"],
                    value["changed"],
                    value["delta"],
                    f"{value['percent_change']:.6f}%"
                    if value["percent_change"] is not None
                    else "undefined zero baseline",
                    "IMPROVED"
                    if value["delta"] < 0
                    else "WORSENED"
                    if value["delta"] > 0
                    else "TIED",
                ]
                for key, value in changes.items()
            ],
        )
    lines += [
        "## Reviewed references",
        "",
        "Task gold: 531 resources × nine obligations = 4,779 cells; REQUIRED 23, HELPFUL_ONLY 84, UNNECESSARY 4,672, UNRESOLVED 0. Thirty-two required units; 16-resource union, 12 acceptable alternatives, six complete task combinations, two distinct resource unions; minimum 15, maximum 16 sufficient resources; 15 indispensable resources and 30 indispensable units. Task gap NONE; repository-information gap NONE. The 16-resource REQUIRED union is not simultaneously necessary.",
        "",
        "C.5: 576 pairs = 15 DIRECTLY_COVERS + 55 PARTIALLY_COVERS + 506 DOES_NOT_COVER + 0 AMBIGUOUS. Strict units: 15 COVERED, 15 PARTIAL_ONLY, two UNCOVERED. Needs: ten NECESSARY, eight PARTIAL_ONLY, all other classifications zero. Granularity: 26 atomic, six collectively coverable, zero overcompound/ambiguous. Accepted N09/N10 sets cover U07/U28/U30 only. Diagnostic units: 18 covered, 12 partial, two uncovered. All 12 alternatives remain incomplete under both rules.",
        "",
        "## Raw acquisition and required reach",
        "",
    ]
    lines += table(
        [
            "Arm",
            "Queries",
            "Query seconds",
            "Positive occurrences",
            "Unique positive",
            "Duplicates",
            "R resources",
            "R cells",
            "R units",
            "Indispensable",
        ],
        [
            [
                arm,
                x["query_count"],
                f"{x['query_seconds']:.9f}",
                x["positive_occurrences"],
                x["unique_positive_resources"],
                x["duplicate_occurrences"],
                *(
                    len(x["reach"][k])
                    for k in ("resources", "cells", "units", "indispensable_resources")
                ),
            ]
            for arm, x in d["arms"].items()
        ],
    )
    lines += [
        f"Pair overlaps: `{json.dumps(d['overlap'], sort_keys=True)}`. All required entities are common to all arms; A-only/B-only/C-only/missed-all sets are empty for required resources/cells/units/indispensable resources. C's unique raw universe grows by 13 and occurrences by 2,243 over B, without any required-reach gain.",
        "",
        f"Shared content index: {d['cost_scope']['shared_content_index_seconds']:.9f}s. Content index reused; native per-query filename index build is included in query timing. R1.5 projection is separately timed in the frozen costs artifact. Single-run timings are descriptive, not latency benchmarks.",
        "",
        "## Arm A — valid whole-task completion",
        "",
        f"Best valid task-alternative depth {a['depth']}; last indispensable-resource rank {a['last_indispensable_resource_rank']}. Prefix has {a['unique_resources']} unique resources, {a['utf8_bytes']:,} UTF-8 bytes, excess {a['excess_over_15_minimum']} over the 15-resource minimum, ratio 370/15 = 24.667. All six combinations are evaluated independently; no all-16 requirement was imposed.",
        "",
    ]
    lines += table(
        [
            "Combination",
            "Sufficient resources",
            "Completion depth",
            "Alternative identities",
        ],
        [
            [i, len(c["resources"]), c["depth"], ", ".join(c["alternatives"])]
            for i, c in enumerate(a["combinations"], 1)
        ],
    )
    lines += [
        "## Arm B — obligation-query completion",
        "",
        "Each alternative uses all complementary resources; choice is minimum depth, then exact alternative identity. Every alternative, identity and member set is retained in analysis.json.",
        "",
    ]
    lines += table(
        [
            "Obligation",
            "Depth",
            "Occurrences",
            "Unique",
            "Duplicates",
            "R",
            "H",
            "U",
            "UTF-8 bytes",
        ],
        [
            [ob, x["selected"]["depth"], *metrics(x["burden"])]
            for ob, x in b["obligations"].items()
        ],
    )
    lines += ["## Prefix burdens — keep comparison targets separate", ""]
    lines += table(
        [
            "Surface",
            "Occurrences",
            "Unique",
            "Duplicates",
            "R",
            "H",
            "U",
            "UTF-8 bytes",
        ],
        [
            ["A valid complete task", *metrics(a)],
            ["B valid complete task", *metrics(b)],
            ["B same 15 covered units", *metrics(strict["B_same_units"])],
            ["C STRICT_COVERED_SUBSET_DIAGNOSTIC", *metrics(strict["C"])],
            ["B same 18 diagnostic units", *metrics(gran["B_same_units"])],
            ["C GRANULARITY_AWARE_SUBSET_DIAGNOSTIC", *metrics(gran["C"])],
        ],
    )
    lines += [
        f"B has excess {b['excess_over_15_minimum']} over minimum, ratio 269/15 = 17.933. B's summed prefixes are 589 occurrences although its deduplicated union is 269. A→B saves unique resources and bytes but adds occurrences/noise and eight query executions; scope-specific label counts cannot be read as a single scalar winner.",
        "",
        "## Arm C — frozen official result",
        "",
        "**Semantic completion = INCOMPLETE_INFORMATION_NEED_COVERAGE** for every one of the 12 alternatives and every obligation. Official full completion depth and burden remain null. Covered-subset metrics cannot substitute for full completion.",
        "",
        "Strict subset uses ten responsible queries: 809 rows, 371 unique resources, 438 duplicates; 24.733 resources per covered unit. Granularity-aware subset uses 11 responsible queries, including both N09/N10 for each accepted collective unit: 920 rows, 391 unique, 529 duplicates; 21.722 resources per covered unit. The latter is still 12 partial + two uncovered units short.",
        "",
        "## B versus C — directly covered units only",
        "",
    ]
    lines += table(
        [
            "Unit",
            "Owning obligation(s)",
            "B depth",
            "C responsible depth",
            "C−B",
            "Outcome",
            "C route",
        ],
        [
            [
                u["alias"],
                ", ".join(u["obligations"]),
                u["B_max_depth"],
                u["C_max_depth"],
                u["depth_delta"],
                u["comparison"],
                ", ".join(r["query"] for r in u["responsible_routes"]),
            ]
            for u in strict["units"]
        ],
    )
    lines += [
        "The gains are U08/U22 (88→61, -27 each), U09 (3→2, -1), U23 (96→26, -70), U26 (122→6, -116; its ceiling lane regresses 2→6). Focused frame/rejection, architecture and numeric-validation vocabulary improves those routes. Regressions include U05 96→273 (+177), U06 96→162 (+66), U27 10→64 (+54), U13 47→76 (+29); generic or poorly discriminating terms omit useful owner/type vocabulary or fail to match whole canonical identifiers. Exact per-resource B/C terms, scores and unnecessary overtakers are in the Stage D review/trace.",
        "",
        "Granularity-aware same-unit comparison: B→C unique 250→391 (+141), occurrences 464→920 (+456), unnecessary 404→831 (+427), bytes 2,552,629→2,897,119 (+344,490). Adding collective semantic credit still fails both completeness and the secondary quantitative burden gate.",
        "",
        "## Partial-only and uncovered units",
        "",
        "The following exact statements remain immutable gold. Missing-component summaries are Stage D interpretations grounded in the reviewed mapping rationales; they do not amend those judgments.",
        "",
    ]
    lines += table(
        [
            "Unit",
            "Obligation",
            "Status",
            "Exact unit statement",
            "Partial frozen needs",
            "Missing component",
            "Any C reaches supports?",
            "Best all-C unit depth (oracle)",
        ],
        [
            [
                u["alias"],
                ", ".join(u["obligations"]),
                u["strict_status"],
                u["statement"],
                ", ".join(u["partial_needs"]) or "NONE",
                MISSING[u["alias"]],
                u["any_C_resource_reach"],
                u["oracle_unit_depth"],
            ]
            for u in d["unit_failures"]
            if u["strict_status"] != "COVERED"
        ],
    )
    lines += [
        "Incidental retrieval by unrelated or partial needs does not acquire the complete fact through a semantically responsible route. Every partial mapping rationale and exact need/unit identity is retained in trace.json.",
        "",
        "## UNCONSTRAINED_QUERY_ORACLE — secondary only",
        "",
        "Best rank of every required resource/unit across all 18 queries is retained. All six valid combinations are projected without mixing incompatible alternatives. The selected per-resource-best-rank projection has maximum best-resource rank 104, seven queries, 183 prefix occurrences, 135 unique resources, 48 duplicates, 144 owning-lane unnecessary occurrences and 1,535,291 UTF-8 bytes. It includes a valid 15-resource sufficient alternative. This is neither a globally optimized prefix union nor an executed/responsible policy, and earns no U1 gate credit. It shows lexical routes exist even for unrequested or incompletely requested facts: semantic omission is the earliest completeness failure, while bad query discrimination separately worsens responsible subset burden.",
        "",
        "## Exact hints and query dilution",
        "",
    ]
    lines += table(
        ["Hint", "Exact declaration owner", "Containing-query owner ranks"],
        [
            [
                h["hint"],
                h["declaration_resource"],
                ", ".join(
                    f"{q['query']}: {q['declaration']['rank']}" for q in h["queries"]
                ),
            ]
            for h in d["diagnostics"]["exact_hints"]
        ],
    )
    lines += [
        "ModelRequest, ContextDisclosure and DisclosurePlan remain lexical-only. Single frozen owner declarations provide deterministic targets for a future U2 experiment; exact lookup was not executed and cannot supply missing task contracts automatically. All containing query texts, declaration/assembly ranks and unnecessary overtakers appear in the trace.",
        "",
        "MIXED_INTENT_EVIDENCE_PRESENT is established locally for C.tests.request-preservation: N14 seeks both U05 preservation tests and U26 invalid-numeric tests. The U05 planning test scores 0.732784534 from 'tests' alone at rank 273; the unnecessary Codex CLI document scores 9.522116872, dominated by request/invalid/argument (8.636011463). The same query reaches U26 at rank six. This is contribution-backed competition between distinct concerns, not an inference from DF. QUERY_DILUTION is a contributor; no ablation or rewritten query was run.",
        "",
        "U27 also exposes a representation limitation: 'rendered' in RenderedContextDisclosure is analyzed as the whole 'renderedcontextdisclosure'. Its literal query matches the owner only on 'context' (1.692466004), giving rank 64. No identifier-aware treatment was run; its prospective rank effect is unknown. U06 may involve descriptive-vocabulary versus fixture-byte mismatch; that remains POSSIBLE_VOCABULARY_SEMANTIC_MISMATCH. Every query's R1.5 DF/IDF/field fraction, reviewed required/helpful/unnecessary yield and score contributions are in the review/trace.",
        "",
        "## Earliest failure attribution",
        "",
    ]
    lines += table(
        ["Unit", "Stage", "Earliest class", "Contributors", "What must change"],
        [
            [
                u["alias"],
                u["failed_stage"],
                u["earliest_failure"],
                ", ".join(u["contributing_factors"]),
                u["what_would_have_to_change"],
            ]
            for u in d["unit_failures"]
        ],
    )
    lines += [
        f"Disjoint earliest-stage totals: `{json.dumps(d['failure_class_totals'], sort_keys=True)}`. Ranking attribution uses R1.5's existing descriptive threshold of 20 unnecessary overtakers; all smaller counts remain visible without a substantial-failure claim. No required resource is absent from all positive sets. Contributors are not added to earliest-stage totals. SEARCH_POLICY_FAILURE = NOT_ASSESSED because U1 executed no sequential frontier/action policy.",
        "",
        "## Frozen gates and outcome precedence",
        "",
    ]
    lines += table(
        ["Gate", "Result", "Evidence"],
        [
            [
                "No loss of B required resource/cell/unit sets",
                d["gates"]["required_reach_safe"],
                "Exact set differences empty",
            ],
            [
                "100% direct reviewed-unit mapping",
                False,
                "15/32; two absent and 15 partial",
            ],
            [
                "≥20% union OR noise reduction; other ≤1.05×",
                False,
                "Official C complete-prefix metrics undefined; cannot pass. Same-subset union 371/220 and noise 737/337 also fail.",
            ],
            [
                "Every mandatory C union ≤1.25× B depth",
                False,
                "Every C complete-alternative prefix is null; no obligation can pass a complete-treatment gate.",
            ],
            ["Additional query cost disclosed", True, "18 versus nine; +0.092476800s"],
        ],
    )
    lines += [
        "The literal frozen precedence is:",
        "",
        "```text",
        d["decision_rule"]["precedence"],
        "```",
        "",
        "Contract identity/score/packet/mapping checks pass. U02/U19 are completely unrequested, so omitted-unit precedence selects INFORMATION_NEED_AUTHORING_DEFECT before any complementary/no-value interpretation. Granularity does not invalidate the experiment: 26 atomic targets exist and 11 atomic units still lack direct coverage. No collective coverage is promoted into the frozen success rule.",
        "",
        "## Case-local limits and exact next step",
        "",
        "Tested: one manually authored need set, one devtools task, canonical BM25, no exact routing, mechanism routing, feedback or reformulation. This does not show that all manual or automatic decomposition fails, establish an optimal need count, generalize across repositories, or reject U2/U3/BM25F. Need completeness and query discrimination both require work in this case.",
        "",
        "Next step: prepare a separately authorized U2 exact-hint extraction and deterministic-routing experiment with a reviewed complete semantic target. U3 remains future; R1.7 remains retained after upstream evidence; R2 true BM25F remains unconditional and mandatory. No next increment is implemented. No production source, frozen treatment/gold/mapping or confirmation/reserve data changed or was accessed.",
        "",
        "## Validation and inspection navigation",
        "",
        "Deterministic publication/verification: `uv run python -B -m experiments.codex_dogfood.case_0011.stage_d.analyze build|verify`. R1.5 replay: `uv run python -B -m experiments.codex_dogfood.case_0011.stage_d.analyze verify`. Use `-B` to keep sterile packet directories free of import caches. Focused tests validate bindings, alternative completion, owner responsibility, unions/bytes, partitions, exact arithmetic/precedence, output correspondence, no native retrieval and overwrite refusal. Static/diff checks and exact command outcomes are recorded in validation.md.",
        "",
        "[Practical per-query review](STAGE_D_REVIEW.md) prints every input, need, top result, required resource, score evidence, need/unit responsibility and failure. [Machine trace](trace.json) retains complete positive rows and all 576 reviewed mappings; [human trace](TRACE.md) is the separate D layer. Parent ../TRACE.md and ../trace.json remain sealed Stage B artifacts.",
        "",
    ]
    return "\n".join(lines)


def score_terms(row: dict[str, Any] | None) -> str:
    """Print exact observed terms and contributions without reranking."""
    if row is None:
        return "NO POSITIVE MATCH"
    return "; ".join(
        f"{field}:{t['term']}={t['contribution']:.9f}"
        for field in ("content", "filename")
        for t in row[f"{field}_terms"]
    )


def review(d: dict[str, Any], trace: dict[str, Any]) -> str:
    """Give maintainers a complete input-to-failure inspection surface."""
    lines = [
        "# Case 0011 Stage D practical review",
        "",
        "Join integrity PASSED. Treatment blindness intentionally lifted only at D. Frozen A/B traces remain unchanged; this is the distinct joined layer. Top five is an inspection window; complete positive rankings and exact contributions remain in the machine trace.",
        "",
        f"Outcome: **{d['outcome']}**. Official C completion: **INCOMPLETE_INFORMATION_NEED_COVERAGE**. Actual evidence-inspection cost NOT MEASURED.",
        "",
        "## Original exact task",
        "",
        "```text",
        trace["original_task"].removesuffix("\n"),
        "```",
        "",
        "Terminal LF is retained in machine exact task/query values.",
        "",
    ]
    units = {u["unit"]: u for u in trace["reviewed_required_units"]}
    needs = {n["identity"]: n for n in trace["information_needs"]}
    for ob in trace["task_basis_and_obligations"]:
        lines += [
            f"## Obligation {ob['identity']}",
            "",
            "Exact predicate: " + ob["predicate"],
            "",
            "Exact criterion: " + ob["criterion"]["statement"],
            "",
            "Exact task basis:",
            "",
            "```text",
            "".join(b["text"] for b in ob["task_basis"]).removesuffix("\n"),
            "```",
            "",
        ]
        lines += table(
            [
                "Reviewed unit",
                "Exact statement",
                "Strict status",
                "Failure",
                "Required resources",
            ],
            [
                [
                    u["alias"],
                    u["statement"],
                    u["strict_status"],
                    u["earliest_failure"],
                    ", ".join(u["resources"]),
                ]
                for u in units.values()
                if ob["identity"] in u["obligations"]
            ],
        )
        b = d["arms"]["B"]["completion"]["obligations"][ob["identity"]]
        lines += [
            f"Best B alternative: `{b['selected']['alternative']}`, depth {b['selected']['depth']}. C: semantically incomplete for every acceptable alternative.",
            "",
        ]
    for q in trace["queries"]:
        lines += [
            f"## Query {q['identity']} — Arm {q['arm']}",
            "",
            f"Obligation: {q['obligation']}; InformationNeed: {q['information_need']}.",
            "",
        ]
        if q["information_need"]:
            n = needs[q["information_need"]]
            lines += [
                "Exact need: " + n["statement"],
                "",
                "Reason: " + n["reason"],
                "",
                "Task basis:",
                "",
                "```text",
                "".join(b["text"] for b in n["task_basis"]).removesuffix("\n"),
                "```",
                "",
            ]
        lines += [
            "Exact query:",
            "",
            "```text",
            q["text"].removesuffix("\n"),
            "```",
            "",
            "Analyzer terms: `" + ", ".join(q["analyzed_terms"]) + "`.",
            "",
            f"Route: `{json.dumps(q['route'], sort_keys=True)}`. Execution count {q['execution_count']}; captured query time {q['query_seconds']:.9f}s; positive rows {len(q['ranked_results'])}. Completion: {q['completion_status']}. Failure classes: {q['failure_classes']}.",
            f"Direct-subset status: {q['direct_subset_status']}; strict prefix {q['strict_responsible_prefix_depth']}; granularity-aware prefix {q['granularity_responsible_prefix_depth']}. Zero-direct-unit needs retain full query cost and candidate counts above.",
            "",
        ]
        lines += table(
            [
                "Top rank",
                "Resource",
                "Reviewed label",
                "Score",
                "Content",
                "Filename weighted",
                "Exact term contributions",
            ],
            [
                [
                    r["rank"],
                    r["address"],
                    r["reviewed_label"],
                    f"{r['score']:.9f}",
                    f"{r['content_score']:.9f}",
                    f"{r['weighted_filename_score']:.9f}",
                    score_terms(r),
                ]
                for r in q["ranked_results"][:5]
            ],
        )
        lines += [
            "Required evidence in this obligation/need's reviewed direct or partial semantic scope:",
            "",
        ]
        lines += table(
            [
                "Required resource",
                "Rank",
                "Score",
                "Unnecessary overtakers",
                "Exact term contributions",
                "Mechanical cause",
            ],
            [
                [
                    e["resource"],
                    e["rank"],
                    f"{e['score_evidence']['score']:.9f}"
                    if e["score_evidence"]
                    else None,
                    e["unnecessary_overtaker_count"],
                    score_terms(e["score_evidence"]),
                    e["mechanical_cause"],
                ]
                for e in q["required_resource_inspection"]
            ],
        )
        lines += table(
            [
                "Unit",
                "Exact identities",
                "Strict status",
                "Need relation",
                "Earliest failure",
                "Missing semantic component",
            ],
            [
                [
                    units[uid]["alias"],
                    f"{uid}; {units[uid]['gold_unit']}",
                    units[uid]["strict_status"],
                    "DIRECTLY_COVERS"
                    if q["information_need"] in units[uid]["direct_needs"]
                    else "PARTIALLY_COVERS"
                    if q["information_need"] in units[uid]["partial_needs"]
                    else "B/A obligation target",
                    units[uid]["earliest_failure"],
                    units[uid]["missing_semantic_component_summary"],
                ]
                for uid in q["required_unit_links"]
            ],
        )
        lines += ["R1.5 term profiles and independently reviewed yields:", ""]
        termrows = []
        for p in q["reviewed_query_profile"]["terms"]:
            cf = next(f for f in p["fields"] if f["field"] == "content")
            ff = next(f for f in p["fields"] if f["field"] == "filename")
            counts = p["reviewed_yield_counts"]
            termrows.append(
                [
                    p["term"],
                    cf["df"],
                    f"{cf['idf']:.9f}",
                    f"{cf['fraction_of_frame']:.6f}",
                    ff["df"],
                    f"{ff['idf']:.9f}",
                    f"{p['matched_frame_fraction']:.6f}",
                    *(counts[k] for k in LABELS),
                ],
            )
        lines += table(
            [
                "Term",
                "Content DF",
                "IDF",
                "Content fraction",
                "Filename DF",
                "IDF",
                "Effective fraction",
                "R yield",
                "H yield",
                "U yield",
            ],
            termrows,
        )
    lines += ["## Responsible covered-subset and collective inspection", ""]
    for subset in (d["strict_subset"], d["granularity_subset"]):
        lines += [
            f"### {subset['label']}",
            "",
            f"{subset['unit_count']} units; query depths: `{json.dumps(subset['C']['prefix_depths'], sort_keys=True)}`. All named collective members are required; no best-performing need substitution.",
            "",
        ]
        lines += table(
            [
                "Unit",
                "Resource(s)",
                "Every responsible need/query depth",
                "B owning depths",
                "C−B",
            ],
            [
                [
                    u["alias"],
                    ", ".join(u["resources"]),
                    "; ".join(
                        f"{r['need']} / {r['query']}: {r['depth']}"
                        for r in u["responsible_routes"]
                    ),
                    "; ".join(f"{r['query']}: {r['depth']}" for r in u["B_routes"]),
                    u["depth_delta"],
                ]
                for u in subset["units"]
            ],
        )
    lines += ["## Exact reviewed units and semantic responsibility", ""]
    for u in units.values():
        lines += [
            f"### {u['alias']} — {u['unit']}",
            "",
            f"Gold identity: `{u['gold_unit']}`. Owning obligations: {u['obligations']}.",
            "",
            u["statement"],
            "",
            f"Strict: {u['strict_status']}; secondary: {u['granularity_aware_status']}. Direct needs: {u['direct_needs']}; partial needs: {u['partial_needs']}.",
            "",
            f"Earliest stage/class: {u['failed_stage']} / {u['earliest_failure']}. Contributors: {u['contributing_factors']}.",
            "",
            "Missing component: " + str(u["missing_semantic_component_summary"]),
            "",
            "What must change: " + u["what_would_have_to_change"],
            "",
            f"Incidental all-C resource routes: `{json.dumps(u['oracle_resource_ranks'], sort_keys=True)}`. Oracle depth {u['oracle_unit_depth']}; no responsible semantic credit.",
            "",
        ]
        for mapping in u["partial_mapping_evidence"]:
            lines += [
                f"Partial mapping `{mapping['need']}` → `{mapping['unit']}`:",
                "",
                "```json",
                json.dumps(mapping, ensure_ascii=False, sort_keys=True, indent=2),
                "```",
                "",
            ]
    lines += [
        "## Contributor interpretation",
        "",
        "```json",
        json.dumps(
            {
                k: v
                for k, v in d["diagnostics"].items()
                if k
                in (
                    "mixed_intent",
                    "representation_example",
                    "vocabulary_example",
                    "exact_hints",
                )
            },
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        ),
        "```",
        "",
        "SEARCH_POLICY_FAILURE = NOT_ASSESSED. See analysis.md for strict gates, full comparisons, case-local limits and future U2/U3/R1.7/mandatory BM25F sequencing.",
        "",
    ]
    return "\n".join(lines)

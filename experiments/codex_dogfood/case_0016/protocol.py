# Copyright (c) 2026
# ruff: noqa: E501, COM812
"""Prospective Graph-3 contract; authoring only, no acquisition imports."""

from __future__ import annotations

from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import ROOT, binary

START = "941678aab144b274216ab1482843ab194a1f5e88"
CASE = ROOT / "experiments/codex_dogfood/case_0016"
PACKAGE = ROOT / "experiments/task_conditioned_graph"
COUNTS: dict[str, int | str] = dict.fromkeys(
    (
        "lexical_query_executions",
        "exact_seed_resolutions",
        "ri_reference_derivations",
        "graph_construction_executions",
        "pagerank_executions",
        "fusion_executions",
        "treatment_rankings",
        "reference_query_executions",
        "repository_map_diagnostics",
    ),
    0,
)
COUNTS["gold"] = "ABSENT"

QUERIES = (
    "repository resource pointer observed snapshot content identity src/devtools/context/planning/resource.py",
    "PlannedDisclosure DisclosurePlan materialize_disclosure_plan purpose identity ordered choices duplicate frame",
    "RepositorySnapshot resource_at MaterializedDisclosureItem retained native provenance stale missing changed content",
    "resource pointer representation source not disclosed UTF-8 byte count content identity non-ASCII",
    "render_context_disclosure assemble_context_disclosure_model_request ModelRequest prompt role mixed plan public exports",
    "pointer disclosure tests documentation architecture validation scripts/validate_development.py",
)
CRITERIA = (
    "Pointer identifies existing observed resource with exact repository/snapshot/address/content identity and no source body; no relevance/sufficiency claim.",
    "Immutable choice conforms to existing PlannedDisclosure/DisclosurePlan/materialization, deterministic identity, mixed caller order and duplicate/frame rejection.",
    "Retained-state resource lookup authenticates native provenance and rejects foreign/stale/missing/changed resources, with no reacquisition or source expansion.",
    "Exact deterministic pointer text exposes prescribed identity/purpose/observed source bytes, explicit source omission and aligned supports including non-ASCII.",
    "Existing common rendering/copied ModelRequest and choices remain compatible; exports and dependency direction preserved.",
    "Focused tests, authoritative/package docs and protected validation cover exact fidelity/rejections/nonclaims without changing production test policy.",
)
FAILURES = (
    "GRAPH_VIEW_CONSTRUCTION_DEFECT",
    "REFERENCE_RESOLUTION_DEFECT",
    "GRAPH_EDGE_PROVENANCE_DEFECT",
    "PERSONALIZATION_DEFECT",
    "PAGERANK_APPLICATION_DEFECT",
    "FUSION_APPLICATION_DEFECT",
    "SEED_CARRYOVER_WITHOUT_PROPAGATED_VALUE",
    "DEGREE_DILUTION",
    "HUB_DOMINANCE",
    "AMBIGUOUS_IDENTIFIER_FANOUT",
    "REVERSE_DEPENDENCY_NOISE",
    "GRAPH_PROPAGATION_NOISE",
    "GRAPH_MISSES_DISCONNECTED_REQUIRED_EVIDENCE",
    "LEXICAL_ONLY_REQUIRED_EVIDENCE",
    "EXPERIMENTAL_CONTRACT_DEFECT",
)
METRICS = (
    "REQUIRED resource/cell reach",
    "Required repository-supported and all semantic-unit reach (task-backed units unranked)",
    "Every reviewed witness completion depth and stable minimum complete selected witness per obligation",
    "Obligation completeness",
    "Obligation/task-indispensable ranks",
    "Every REQUIRED-cell rank, gain, regression and reach rescue",
    "Graph-novel REQUIRED / HELPFUL_ONLY / UNNECESSARY resources after gold",
    "A-only, B-only, A intersection B, C union and graph-novel resources before labels",
    "Selected completion-prefix union unique resources, repeated occurrences, duplicate occurrences",
    "Obligation-relative REQUIRED / HELPFUL_ONLY / UNNECESSARY occurrences",
    "Distinct UTF-8 resource bytes in selected prefix union",
    "Captured single-run execution/preparation/publication cost without outcome threshold",
)


def authored() -> dict[str, Any]:
    """Return the complete prospective design without accessing retrieval state."""
    task = binary(CASE / "task.txt").decode()
    return {
        "case": "0016",
        "increment": "GRAPH-3 / TASK-CONDITIONED REPOSITORY-MAP RETRIEVAL",
        "source_head": START,
        "task_identity": "case-0016-resource-pointer-disclosure-v1",
        "task_text": task,
        "requirement_matrix": [
            {
                "obligation": f"O{i}",
                "query_id": f"Q{i}",
                "mandatory": True,
                "task_clause": task.split(f"O{i}. ", 1)[1].split("\n\n", 1)[0],
                "satisfaction_criteria": criterion,
                "query": query,
            }
            for i, (criterion, query) in enumerate(
                zip(CRITERIA, QUERIES, strict=True), 1
            )
        ],
        "arms": {
            "A": "CANONICAL_BM25",
            "B": "TASK_CONDITIONED_REFERENCE_PPR",
            "C": "BM25_GRAPH_RRF",
        },
        "comparisons": {
            "primary": "C versus A",
            "diagnostic": "B versus A",
            "reference": "Whole exact task canonical BM25, unchanged separate lane; never treatment/rescue",
        },
        "canonical_bm25": {
            "analyzer": "Native Unicode word spans/casefold, distinct query terms",
            "k1": 1.2,
            "b": 0.75,
            "filename_weight": 0.25,
            "score": "Native content BM25 + .25 independent filename-stem BM25",
            "maximum_results": "All positive matches, bound = frame resource count",
            "ties": "Native collection order",
        },
        "ri_fact_contract": {
            "derivation": "derive_python_declaration_references",
            "input": "Frozen retained snapshot only",
            "module_roots": ["src", "."],
            "module_addresses": "All frame .py resources interpreted under src for src/ paths, under . otherwise; no automatic root guesses",
            "reference_sources": "Each frame .py resource once, address order, supplied native universe/source interpretations",
            "coverage": "Native bounded non-exhaustive assessment outcomes retained; unsupported/ambiguous/unresolved creates no edge; parse/derivation error is contract/ranking defect, no scientific retry",
            "native_support": "Definition/reference subjects, occurrences, derivations, source/target resources, spans, import/member/module route provenance; no guessed truth",
        },
        "graph_projection": {
            "nodes": "Every eligible observed repository resource occurrence, address order, bound N",
            "edges": "REFERENCER_RESOURCE -> DEFINER_RESOURCE for each positive resolved declaration Reference; retain self references",
            "families": ["REFERENCE"],
            "call_import_tags": "Native reference qualification/Call tags only; no separate edge or weight",
            "excluded_families": [
                "Imports as separate edge",
                "Calls as separate edge",
                "tests",
                "inheritance",
                "containment",
                "configuration",
                "directory adjacency",
                "reverse edges",
            ],
            "raw_count": "Distinct native resolved reference occurrences per directed resource pair; duplicate identical fact counts once, conflicting same-occurrence facts rejected",
            "weight": "sqrt(raw_reference_count)",
            "normalization": "weight / fsum(outgoing pair weights), canonical source/target order",
            "provenance": "Retain native fact objects unmodified; compact serialization retains fact/derivation/occurrence/subject/definition/route/content identities, spans, identifier expression and full native route support. Derived identity is not a replacement for support.",
            "no_paths": "No BFS/frontier/path enumeration generates or scores candidates; optional distance only after ranking, not effectiveness metric",
        },
        "seed_policy": {
            "exact": "Caller-frozen literal resource-address locators in owning query; existing RepositorySnapshot.resource_at only; retain native resolved/absent result. No prospective resolution at Stage A.",
            "exact_locators": {
                "Q1": ["src/devtools/context/planning/resource.py"],
                "Q6": ["scripts/validate_development.py"],
                "Q2": [],
                "Q3": [],
                "Q4": [],
                "Q5": [],
            },
            "lexical": "First K unique positive native Arm A resources for same obligation query",
            "K": 10,
            "union": "Exact existing resources UNION lexical top K; canonical address deduplication",
            "personalization": "Uniform 1 / number of unique seeds; normalized",
            "fallback": "Exact seeds suffice when no lexical positives. If neither signal resolves a seed, NO_SEEDS/empty B, iterations=0; C=A; never global PageRank",
            "future_resource": "A requested future pointer implementation file is not an existing seed; no new hint/extraction/fuzzy heuristic",
        },
        "pagerank": {
            "kernel": "devtools.context.retrieval.graph.walk.stationary_distribution",
            "damping": 0.85,
            "restart": 0.15,
            "tolerance": 1e-10,
            "maximum_iterations": 200,
            "initial": "personalization",
            "dangling": "personalization",
            "convergence": "L1 delta <= tolerance, deterministic supplied node/row order; normalize returned mass. Nonconvergence is PAGERANK_APPLICATION_DEFECT; no silent fallback or parameter change.",
            "result": "All positive resource mass bounded by N; descending score then canonical address (no lexical-rank tie preference)",
            "trace": "Exact/lexical seed provenance, score, seed flag, direct restart, dangling return, incoming edge stationary flows. Edge flow divided equally among its native occurrences for definition diagnostics; scores are not relevance probabilities.",
        },
        "definition_projection": "Referenced native definitions in positively ranked owners; definition/subject identity, name, exact native span, incoming per-reference flow and parent resource rank/score. No symbol aggregation changes resource ranks.",
        "map_diagnostic": {
            "owner_boundary": "Experiment rendering only; production Context representation remains a later decision",
            "effectiveness_arm": False,
            "maximum_utf8_bytes": 8192,
            "header_characters": 240,
            "representation": "Exact first native declaration line excerpt plus explicit excerpt marker, name/address/location; not complete signature/body/decorators",
            "budget": "Whole lines in parent-rank / incoming-flow / definition-identity order, stop at first blocked line; omissions metadata; no token estimator",
            "score_effect": "NONE",
        },
        "fusion": {
            "implementation": "devtools.context.retrieval.fusion._fused_resource_order",
            "rank_constant": 60,
            "lexical_weight": 1,
            "graph_weight": 1,
            "score": "1/(60+A_rank) + 1/(60+B_rank)",
            "missing_view": "Zero contribution; union membership",
            "ties": "Descending score, lexical rank (missing infinity), canonical address",
            "limit": "Entire union bounded by N",
            "dependence": "B seeded by A; agreement is not independent corroboration",
        },
        "metrics": METRICS,
        "measurement_semantics": {
            "joins": "Exact case/task/obligation/query/repository/snapshot/corpus/address/document/content identity; no filename-only mapping; Q1-Q6 own O1-O6 respectively",
            "resource_reach": "Distinct REQUIRED union resources reached in owning REQUIRED cells; cell reach is owning-query membership, never rank under another obligation",
            "unit_reach": "A repository-supported unit is reached when one complete reviewed support alternative is reached under its owning obligation query; never mix members from different alternatives. Task-backed units are available from task, have no retrieval rank; report repository-supported and all units separately.",
            "witnesses": "For each reviewed witness independently, all repository members must be reached; depth=max owning-query ranks, empty witness=0; incomplete=None. Prefix occurrences are owning-query ranks 1..depth. Select minimum complete depth then reviewed stable identity; no complete witness means incomplete, no fabricated prefix/depth.",
            "incomplete_burden": "Report incomplete obligations separately; strong burden comparison not eligible if either arm has an incomplete selected mandatory obligation. A-incomplete/C-complete may still support through safe material reach rescue or complementary value, never fictional baseline completion burden.",
            "indispensability": "Obligation intersection of reviewed minimal witnesses; task intersection of reviewed complete task combinations; task-backed units have no rank",
            "burden": "Only selected mandatory owning-query prefixes. Count repeated resources per query separately; distinct resource/UTF-8 byte union counts each exact content occurrence once. Label occurrences against their own obligation; all candidate/gold joins must validate.",
            "candidate_safety": "A/B membership may differ; C=union(A,B) with full frame-size result bound. No retrospective pruning or candidate removal. Compare reach, noise and concentration only after blind gold.",
        },
        "diagnostics": [
            "Top-K overlap/entered/exited/inversions at 10/20/50, labels only after blind gold",
            "Seed versus propagated mass/rank share, top incoming contributors and responsible reference identifiers",
            "Structural distance from seeds after ranking only",
            "A/B native rank contributions to C; removing B from frozen RRF (A order) explains hybrid movement without a new treatment",
        ],
        "historical_comparison": "Later compare retained Graph-1/2 expansion size, ranked concentration, novel evidence yield, path explosion, reverse/fan-out noise and discovered required evidence; nonmatched cases prohibit a controlled causal superiority claim. No historical rerun or raw path-count effectiveness metric.",
        "failure_taxonomy": FAILURES,
        "attribution_policy": "Graph-contributed gain requires captured B membership/rank/propagated-reference flow and deterministic RRF ablation showing the necessary-evidence/witness gain disappears without B. Seed-only rank carryover must be reported separately; no propagation claim from seed status alone. Noise/hub/dilution classifications require demonstrated necessary-evidence/overtaker consequence, not raw degree/score. B-only poor ordering does not itself select hybrid failure.",
        "decision_rule": {
            "implementation": "experiments/task_conditioned_graph/gates.py",
            "primary": "C versus A only",
            "meaningful_witness": "A incomplete and C complete OR A_depth > 0 AND 5*C_depth <= 4*A_depth",
            "meaningful_required_rank": "Both reached, A_rank-C_rank >= 2 AND 5*C_rank <= 4*A_rank",
            "reach_rescue": "A REQUIRED cell unreached and C reached, minimum one cell; no fabricated A rank; resource/unit reach also retained",
            "selected_witness": "Minimum complete depth, then stable reviewed witness identity; never mix members from alternative witnesses",
            "zero_resource_witness": "Complete at depth 0, zero prefix/burden, task-backed units unranked; 0-to-0 not meaningful, no division",
            "bounds": "Baseline-complete selected depths remain complete; 5*C_depth <= 6*A_depth AND C-A <= 5; baseline-reached REQUIRED ranks retained, 5*C_rank <= 6*A_rank AND C-A <= 10; every regression independently bounded",
            "strong_burden": "Positive baseline unique and occurrence counts; (10*C_unique <= 9*A_unique OR 10*C_occurrences <= 9*A_occurrences) AND all unique/occurrence/distinct-byte dimensions nonincreasing",
            "safe_material_gain": "At least one graph-contributed REQUIRED-cell reach rescue, no baseline-complete depth or baseline-reached REQUIRED-rank worsening, no required-unit reach loss",
            "burden_scope": "Selected mandatory witness prefixes only; union resources/bytes across obligations, retain repeated occurrences and obligation-relative labels; no fictional global task ranking",
            "precedence": [
                "Contract defect => EXPERIMENTAL_CONTRACT_DEFECT",
                "RI/view/provenance/personalization/PPR/fusion implementation defect => GRAPH_RANKING_DEFECT",
                "REQUIRED resource/cell/unit reach loss OR baseline completion loss OR any unbounded required rank/selected depth regression => GRAPH_HARMFUL",
                "Valid and no loss/unbounded regression, graph-contributed meaningful witness gain or REQUIRED reach rescue AND (strong burden improvement OR safe material reach gain) => GRAPH_HYBRID_SUPPORTED",
                "No loss/unbounded regression, graph-contributed meaningful rank/witness gain or novel REQUIRED reach rescue => COMPLEMENTARY_GRAPH_VALUE",
                "Otherwise => NO_MATERIAL_VALUE",
            ],
            "implementation_checks": "Native RI frame/content/support, reference-only projection, occurrence count/sqrt/row arithmetic, seed sources/K/uniform mass, dangling/restart/convergence, full positive ranks/ties, RRF union/arithmetic, exact native joins, unchanged reference lane, once-only execution and valid blind gold",
            "cost_and_map": "Descriptive only; no outcome threshold",
        },
        "gold_policy": {
            "MODEL": "GPT-6 Astra",
            "REASONING": "High",
            "treatment_blind": True,
            "automatic_second_reviewer": False,
            "allowed": [
                "case/task identity",
                "exact task",
                "obligations/satisfaction criteria without queries",
                "eligible resource identities/content",
            ],
            "excluded": [
                "queries",
                "seed identities",
                "lexical ranks",
                "exact-route results",
                "graph nodes/edges/reference graph",
                "PPR parameters/scores",
                "graph/fusion ranks",
                "repository-map diagnostic",
                "candidate results",
                "metrics",
                "costs",
                "gates",
                "outcomes",
            ],
            "natural_text": "Unchanged; no treatment-origin metadata or text rewriting",
            "reviewers": "One clean primary; no automatic second reviewer/reconciliation",
        },
        "durable_state": {
            "U1": "COMPLETE / INFORMATION_NEED_AUTHORING_DEFECT",
            "U2": "COMPLETE / EXACT_HINT_ROUTING_SUPPORTED",
            "U3": "COMPLETE / SELECTIVE_MECHANISM_ROUTING_SUPPORTED",
            "R1.7": "COMPLETE / QUERY_TERM_WEIGHTING_HARMFUL",
            "R2": "COMPLETE / BM25F_HARMFUL",
            "R1": "Separate identifier-aware view",
            "R1.7_scope": "Query-side evidence",
            "R2_scope": "Document-field-combination evidence",
            "next_direction": "GRAPH / REPOSITORY-MAP RETRIEVAL",
        },
        "exclusions": {
            "production_behavior": "UNCHANGED",
            "confirmation_reserve": "NOT_ACCESSED",
            "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
            "feature_implementation": "NOT_AUTHORIZED",
            "prospective_execution": "NOT_EXECUTED",
            "no_tuning": True,
        },
        "no_execution": COUNTS,
    }

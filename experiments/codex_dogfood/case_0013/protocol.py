# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, TRY003 -- literal prospective protocol and validation
"""Task-only U3 authoring; no repository result or gold enters routing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from devtools.context.localization import (
    LocalizationAnchor,
    LocalizationObligation,
    LocalizationTaskInterpretation,
    ObligationLexicalQuery,
    RequirementStatus,
    SatisfactionCriterion,
)
from devtools.context.localization.identity import (
    LocalizationAnchorIdentity,
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
    LocalizationTaskIdentity,
    TaskProvenance,
    TaskTextSpan,
)
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
)
from experiments.codex_dogfood.acquisition.needs import InformationNeed
from experiments.codex_dogfood.case_0009.artifacts import binary, digest
from experiments.exact_hint_routing.extraction import caller_observation, extract
from experiments.exact_hint_routing.models import HintAssociation, HintCategory
from experiments.exact_hint_routing.serialization import project
from experiments.mechanism_routing.policy import (
    Arm,
    IntentRole,
    RoutingBasis,
    decisions,
)

CASE = Path(__file__).resolve().parent
START = "b42dcb3fd93bd6ddb8af35f1cf8b3273f6486b4b"
TASK_ID = LocalizationTaskIdentity("case-0013-context-disclosure-manifest")
OBLIGATIONS = (
    (
        "structure",
        "Preserve exact materialized plan/item structure and native provenance.",
        "Plan purpose, frame, identities, ordered one-item-per-choice and representations are preserved.",
        (1, 2, 4),
        "ContextDisclosure materialized disclosure plan purpose snapshot ordered items option identity representation native provenance",
    ),
    (
        "integrity",
        "Authenticate manifest support against retained native snapshot before publication.",
        "Foreign stale missing content mismatch and misaligned support are rejected without reacquisition or rematerialization.",
        (3,),
        "RepositorySnapshot resource_at content identity foreign stale missing resources support validation materialization",
    ),
    (
        "manifest",
        "Implement the future explicit manifest operation in common Context Planning.",
        "Every item and repeated support occurrence is correlated with exact resource/content identities, byte counts and native provenance.",
        (4,),
        "Context planning disclosure manifest items support resource content identities repeated order byte count native provenance",
    ),
    (
        "projection",
        "Provide deterministic JSON-compatible presentation and distinct byte accounting.",
        "Stable fields, exact ordered support, total item bytes versus unique supporting resource bytes and scope limits are established.",
        (5,),
        "deterministic Context disclosure projection JSON stable identity UTF-8 byte count unique resource item text native provenance",
    ),
    (
        "compatibility",
        "Preserve rendering and copied request assembly.",
        "Existing output, original request role fields tools settings and task-before-Context assembly remain unchanged.",
        (6,),
        "Context planning rendering assemble copied ModelRequest prompt role settings tools task unchanged",
    ),
    (
        "exports",
        "Expose both public facades with existing dependency ownership.",
        "Common planning and outer Context exports are coherent; no Retrieval dependency or relocation of Python-specific semantics.",
        (6,),
        "Context planning __init__ exports public facade dependency Python qualified reference Retrieval",
    ),
    (
        "tests",
        "Establish focused and regression coverage for every new and preserved contract.",
        "Mixed choices duplicate support order UTF-8 CRLF native provenance determinism and all rejection cases plus old regressions are covered.",
        (7,),
        "Context planning tests mixed whole resource qualified reference duplicate support non ASCII CRLF rejection provenance rendering copied request",
    ),
    (
        "documentation",
        "Explain manifest fidelity applicability and limits in existing package documentation.",
        "Byte accounting, non-persistence, no automatic selection, sufficiency or disclosure authority are documented.",
        (8,),
        "Context planning documentation manifest fidelity applicability byte accounting persistence completeness authorization",
    ),
    (
        "validation",
        "Preserve the protected development and static validation contract.",
        "Protected profile coverage strict mypy Ruff format worktree/index checks and restricted/live boundaries are established.",
        (9,),
        "protected development validation pytest coverage pyproject strict mypy Ruff formatting confirmation exclusion",
    ),
)
HINTS = (
    (
        "devtools.context.planning.materialization.ContextDisclosure",
        "PYTHON_DIRECT_CLASS",
        "structure",
        "INSPECT_EXISTING",
    ),
    (
        "devtools.context.planning.materialization.materialize_disclosure_plan",
        "PYTHON_DIRECT_FUNCTION",
        "structure",
        "INSPECT_EXISTING",
    ),
    (
        "devtools.context.repository.snapshot.RepositorySnapshot.resource_at",
        "PYTHON_DIRECT_METHOD",
        "integrity",
        "INSPECT_EXISTING",
    ),
    (
        "devtools.context.planning.manifest.ContextDisclosureManifest",
        "PYTHON_DIRECT_CLASS",
        "manifest",
        "INTRODUCE_NEW",
    ),
    (
        "devtools.context.planning.manifest.describe_context_disclosure",
        "PYTHON_DIRECT_FUNCTION",
        "manifest",
        "INTRODUCE_NEW",
    ),
    (
        "src/devtools/context/planning/manifest.py",
        "RESOURCE_ADDRESS",
        "manifest",
        "INTRODUCE_NEW",
    ),
    (
        "devtools.context.planning.rendering",
        "PYTHON_MODULE",
        "compatibility",
        "INSPECT_EXISTING",
    ),
    (
        "tests/context/planning/test_manifest.py",
        "RESOURCE_ADDRESS",
        "tests",
        "INTRODUCE_NEW",
    ),
    (
        "src/devtools/context/planning/docs/overview.md",
        "RESOURCE_ADDRESS",
        "documentation",
        "INSPECT_EXISTING",
    ),
    ("pyproject.toml", "RESOURCE_ADDRESS", "validation", "INSPECT_EXISTING"),
)
FAILURES = [
    "ROUTE_SELECTION_MISS",
    "ROUTE_SELECTION_OVERREACH",
    "UNSUPPORTED_ROUTE",
    "AMBIGUOUS_ROUTE",
    "UNRESOLVED_ROUTE",
    "SELECTED_ROUTE_TARGET_NOT_REQUIRED",
    "SELECTED_ROUTE_NOT_COMPLETION_BOTTLENECK",
    "LEXICAL_FALLBACK_RANKING_FAILURE",
    "ACQUISITION_INTENT_AUTHORING_DEFECT",
    "EXPERIMENTAL_CONTRACT_DEFECT",
]
RULE = {
    "contract": "Exact task/obligation/query/frame joins, blind gold and complete candidate/native match/global safety preservation; complete mandatory task interpretation, truthful full per-arm route/cost disclosure. Invalid or unassessable required evidence => EXPERIMENTAL_CONTRACT_DEFECT; do not fill missing measures with zero.",
    "soundness": "C decisions must equal frozen task-only policy; locators derive only from literal explicit hint components. Every promotion uniquely native RESOLVED in the frozen frame; no invented owner. Violations => ROUTER_DEFECT. Genuine unsupported/ambiguous/unresolved native outcomes alone are scope outcomes.",
    "reach": "C loses no A- or B-reached REQUIRED resources, owning cells or distinct/owning semantic units. All original lexical positive matches, ranks, scores and contributions survive; the global safety lane is unchanged. Loss => ROUTER_DEFECT.",
    "completion": "For each mandatory applicable obligation evaluate every complete reviewed witness, ALL members jointly necessary, ANY complete alternative admissible. Select minimum completion depth then stable reviewed witness identity. Missing completion is null; null cannot pass numeric gates. Do not mix alternatives or invent task-global ranking. Chosen mandatory prefixes are unioned; occurrences remain repeated and labels are owning-obligation relative. Resource bytes count distinct exact UTF-8 whole-resource contents. Task combinations constrain reported semantic sufficiency, not a fabricated global treatment order.",
    "obligation_safety": "Every B-complete mandatory obligation remains C-complete; C selected completion depth and unique prefix count each <= B. Failure => ROUTER_DEFECT. An undefined complete B baseline makes selective-support gates unassessable, not successful.",
    "meaningful_B_gain": "A B-versus-A obligation gain is meaningful when A is incomplete and B completes, or A depth >0 and 5*B_depth <=4*A_depth. All such B improvements must retain C_depth <= B_depth for branch 1. Report every skipped useful B route even outside this threshold.",
    "branch_1": "At least one meaningful B-versus-A witness gain retained; C preserves every such gain; native admitted top-level route invocations reduced at least 25% (4*C<=3*B); exact-resolution-plus-presentation aggregate cost reduced at least 10% (10*C<=9*B); charged treatment cost no more than 5% higher (20*C<=21*B). B invocation and cost denominators must be positive.",
    "branch_2": "Case-wide chosen completion-prefix unique resources reduced at least 10% over B (10*C<=9*B, B>0); unique UTF-8 bytes <= B; charged C cost <= B with positive B cost. Obligation safety and required reach still mandatory.",
    "precedence": "1 contract defect; 2 router soundness/reach/obligation defect; 3 all safety gates plus either selective-value branch => SELECTIVE_MECHANISM_ROUTING_SUPPORTED; 4 sound reach/obligation-safe C has any strict positive C-over-B depth, unique prefix, occurrences, unnecessary, bytes, invocation or mechanism-cost reduction => COMPLEMENTARY_BUT_NOT_CLEARLY_BETTER; 5 otherwise NO_MATERIAL_VALUE. Equality with B never supplies selective value. Use gates.evaluate integer arithmetic; no tuned thresholds or rounded decisions.",
    "undefined": "Report NOT_ASSESSED for individual missing metrics. If missing data prevents contract/safety or selected-branch evaluation, classify contract defect, rather than constructing GateEvidence with a synthetic zero. Zero B noise supplies no reduction evidence; positive counters only define reduction percentages.",
    "attribution": "ROUTE_SELECTION_MISS means a frozen task-visible intent's applicable sound B route was skipped by C and either supplies REQUIRED witness evidence absent from C exact routes or preserves a B witness-depth gain lost by C. Report witness membership and actual depth effect separately. Low-value avoided routes: genuine native nonresolution, non-REQUIRED targets, or REQUIRED targets with no B-versus-A selected witness completion improvement; report these subtypes separately, not as universal uselessness. OVERREACH means C admission violates the explicit frozen role or native scope. Authoring defect concerns incomplete/contradictory task-only intent meaning, not poor retrieval alone. SEARCH_POLICY_FAILURE=NOT_ASSESSED; no sequential pursuit.",
    "threshold_rationale": "25% fewer native route requests is an operationally noticeable discrete reduction; 10% mechanism cost or task union improvement requires a measurable benefit beyond equality; 5% charged-cost tolerance bounds added classification overhead. These are prospective development thresholds, not fitted to Case 0013 outcomes or Case 0012 ranks.",
}
COST = {
    "shared": "Observe committed broad frame, address-only module universe and document representation separately; charge equally. Native lexical index build and identical nine obligation plus global queries execute once and are captured, reused unchanged by A/B/C.",
    "arm": "B/C use identical task-only hint inventory and associations. Charge common hint projection/extraction to B/C, isolated arm policy time (B always-on, C classify/select), each admitted top-level native route separately, and each obligation presentation. A retains unmodified lexical output with zero exact/policy overhead.",
    "mechanism": "Sum nonoverlapping per-request resolution elapsed ns plus nonoverlapping per-lane presentation ns. A direct-method timer includes parent selection and method containment; child timings are descriptive, never added. Unsupported admission attempts and selected/skipped requests counted separately from admitted native invocations.",
    "charged": "Common index + common query elapsed + common hint projection for B/C + arm policy + exact resolution + presentation; no nested composite plus children. Frame setup and durability/publication wall time reported separately; arm composites descriptive cross-checks. No benchmarks/reruns. Captured single-run timings are descriptive development evidence, not calibrated causal speed estimates.",
    "inspection": "Prefix burden is counterfactual complete-evidence inspection, not measured human effort. No actual coding or model execution.",
}
METRICS = [
    "required_resource_reach",
    "required_cell_reach",
    "required_semantic_unit_reach",
    "all_witness_completion_depths",
    "chosen_witness_depth",
    "unique_completion_prefix_resources",
    "prefix_occurrences",
    "duplicate_occurrences",
    "unnecessary_occurrences",
    "owning_label_composition",
    "unique_UTF8_bytes",
    "admitted_native_invocations",
    "selected_skipped_unsupported_requests",
    "ambiguous_unresolved_resolved_requests",
    "resolution_presentation_ns",
    "charged_treatment_ns",
    "useful_routes_avoided",
    "low_value_routes_avoided",
    "selected_REQUIRED_HELPFUL_ONLY_UNNECESSARY_targets",
    "family_specific_effectiveness",
    "bottleneck_shifts",
]


def definition() -> dict[str, Any]:
    """Build the complete prospective interpretation before broad frame observation."""
    text = binary(CASE / "task.txt").decode()
    bases: list[dict[str, Any]] = []
    offset = 0
    for line in text.splitlines(keepends=True):
        bases.append({"start": offset, "end": offset + len(line), "text": line})
        offset += len(line)
    obligations: list[dict[str, Any]] = [
        {
            "identity": f"{TASK_ID.value}/{key}",
            "key": key,
            "statement": statement,
            "criterion": criterion,
            "applicability": "MANDATORY; later independent gold may mark NOT_APPLICABLE only with exact task-supported rationale",
            "task_basis": [bases[n - 1] for n in numbers],
            "query": query,
            "analyzed_terms": list(
                analyze_repository_text_lexical_query(text=query).normalized_terms
            ),
        }
        for key, statement, criterion, numbers, query in OBLIGATIONS
    ]
    hints = []
    associations = []
    routing_bases = []
    for number, (literal, category, lane, role) in enumerate(HINTS, 1):
        token = f"`{literal}`"
        if text.count(token) != 1:
            raise ValueError("Hint token must occur exactly once")
        start = text.index(token) + 1
        hint = caller_observation(
            TASK_ID,
            text,
            start=start,
            end=start + len(literal),
            category=HintCategory(category),
            rationale="Task-only caller syntax reference before frame preparation",
        )
        obligation = LocalizationObligationIdentity(TASK_ID, lane)
        association = HintAssociation(
            hint.identity,
            obligation,
            "Explicit task clause associates this hint with this obligation, without gold",
            hint.provenance,
        )
        prefix = "Inspect existing " if role == "INSPECT_EXISTING" else "Introduce new "
        purpose = (
            ": establish its native contract specified by this task clause"
            if role == "INSPECT_EXISTING"
            else ": establish surrounding integration contracts; this literal "
            "is a future destination, not an existing-evidence request"
        )
        need = InformationNeed(
            f"I{number:02}",
            obligation,
            prefix + literal + purpose,
            "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            hint.provenance,
            (LocalizationAnchorIdentity(TASK_ID, hint.identity.value),),
        )
        routing_bases.append(RoutingBasis(need, hint, association, hint.provenance))
        hints.append(hint)
        associations.append(association)
    # Full conceptual coverage supplements exact intents, without defining a need-only query lane.
    for o in obligations:
        basis = o["task_basis"][0]
        provenance = TaskProvenance(
            TASK_ID.value,
            TaskTextSpan(basis["start"], basis["end"]),
            "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage",
        )
        need = InformationNeed(
            "conceptual/" + o["key"],
            LocalizationObligationIdentity(TASK_ID, o["key"]),
            "Understand " + o["statement"],
            "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            provenance,
        )
        routing_bases.append(RoutingBasis(need, None, None, provenance))
    extracted = extract(TASK_ID, text)
    rule_hints = tuple(d.observation for d in extracted if d.observation is not None)
    if {(h.identity, h.category) for h in hints} != {
        (h.identity, h.category) for h in rule_hints
    }:
        raise ValueError(
            "Task-syntax extraction requires pre-execution authoring review"
        )
    anchors = tuple(
        LocalizationAnchor(
            LocalizationAnchorIdentity(TASK_ID, h.identity.value), h.text, h.provenance
        )
        for h in hints
    )
    native_obligations = tuple(
        LocalizationObligation(
            LocalizationObligationIdentity(TASK_ID, o["key"]),
            o["statement"],
            tuple(
                a.identity
                for a in anchors
                if any(
                    s.hint.value == a.identity.value
                    and s.lane == LocalizationObligationIdentity(TASK_ID, o["key"])
                    for s in associations
                )
            ),
            TaskProvenance(
                TASK_ID.value,
                TaskTextSpan(o["task_basis"][0]["start"], o["task_basis"][-1]["end"]),
                "Caller complete task interpretation, no witness gold",
            ),
            RequirementStatus.MANDATORY,
            SatisfactionCriterion(o["key"], o["criterion"]),
            (),
            o["applicability"],
        )
        for o in obligations
    )
    native_task = LocalizationTaskInterpretation(
        TASK_ID,
        TaskProvenance(TASK_ID.value, explanation="Exact prospective manifest task"),
        anchors,
        native_obligations,
    )
    queries = tuple(
        ObligationLexicalQuery(
            LocalizationQueryIdentity(TASK_ID, "obligation/" + o["key"]),
            n.identity,
            o["query"],
        )
        for o, n in zip(obligations, native_obligations, strict=True)
    )
    matrix = []
    for n, b in enumerate(bases, 1):
        owners = [o["key"] for o in obligations if b in o["task_basis"]]
        operational = b["text"].startswith("Operational exclusion:")
        if not owners and not operational:
            raise ValueError("Unmapped substantive task clause")
        matrix.append(
            {
                "requirement": f"R{n:02}",
                "basis": b,
                "obligations": owners,
                "exclusion": "NON_FEATURE/OPERATIONAL; explicitly no feature implementation or scientific treatment"
                if operational
                else None,
            }
        )
    arm_decisions = {a.name: decisions(a, tuple(routing_bases)) for a in Arm}
    return {
        "schema": "case-0013-stage-a-v1",
        "task_identity": TASK_ID.value,
        "task_text": text,
        "task_sha256": digest(text.encode()),
        "task_requirement_matrix": matrix,
        "obligations": obligations,
        "native_task_interpretation": project(native_task),
        "native_obligation_queries": project(queries),
        "hint_inventory": [
            {"key": f"H{n:02}", **project(h), "identity": project(h.identity)}
            for n, h in enumerate(hints, 1)
        ],
        "hint_associations": project(associations),
        "extraction_decisions": project(extracted),
        "extraction_agreement": {
            "caller": len(hints),
            "rule": len(rule_hints),
            "false": 0,
            "missing": 0,
            "type_disagreement": 0,
            "scope": "Task-syntax reference only, not repository or relevance truth",
        },
        "acquisition_intents": [
            {"identity": b.need.identity, "role": b.role.value, **project(b)}
            for b in routing_bases
        ],
        "intent_taxonomy": [r.value for r in IntentRole],
        "route_decisions": {
            a: [{"identity": d.identity, **project(d)} for d in ds]
            for a, ds in arm_decisions.items()
        },
        "exact_route_requests": {
            a: [
                {"identity": d.request.identity, **project(d.request)}
                for d in ds
                if d.request is not None
            ]
            for a, ds in arm_decisions.items()
        },
        "arms": {a.name: a.value for a in Arm},
        "router_rules": "A lexical only; B every admissible explicit hint; C only INSPECT_EXISTING admissible hints. INTRODUCE_NEW/CONCEPTUAL lexical only; unsupported explicit native scopes preserve fallback. Same inventory and lexical coverage, no repository inputs.",
        "settings": {
            "k1": 1.2,
            "b": 0.75,
            "filename_weight": 0.25,
            "maximum_results": "entire frozen resource count; all positive native rows",
            "tokenizer": "unicode-word-span-casefold-v1",
            "representation": "whole-resource-exact-text-v1",
            "tie_order": "native descending score then frozen document order",
            "fusion": False,
            "reformulation": False,
            "BM25F": False,
            "identifier_aware_view": False,
        },
        "global_safety_query": {
            "text": text,
            "analyzed_terms": list(
                analyze_repository_text_lexical_query(text=text).normalized_terms
            ),
            "scope": "unchanged reporting safety lane, not a fictional task-global acquisition order",
        },
        "metrics": METRICS,
        "failure_taxonomy": FAILURES,
        "search_policy_failure": "NOT_ASSESSED",
        "decision_rule": RULE,
        "cost_accounting": COST,
        "future_gold": {
            "model": "GPT-6 Astra",
            "reasoning": "High",
            "policy": "One clean treatment-blind primary adjudication of complete resource-by-obligation cells, semantic units, complete witnesses/alternatives, gaps and limitations. No automatic second adjudication. Separately authorized reliability uses same model family and reasoning.",
            "packet_allowlist": [
                "case",
                "task_identity",
                "task_text",
                "obligations",
                "resources",
            ],
            "excluded": [
                "queries",
                "intents",
                "router roles",
                "hints metadata",
                "locators",
                "arms",
                "decisions",
                "costs",
                "results",
                "ranks",
                "scores",
                "treatment reports",
            ],
        },
        "execution": {
            "retrieval": 0,
            "exact_routes": 0,
            "specialized_mechanisms": 0,
            "treatments": 0,
            "index_builds": 0,
        },
        "stage_b": "NOT_EXECUTED",
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "excluded": [
            "production routing",
            "manifest feature implementation",
            "R1.7",
            "BM25F",
            "confirmation/reserve",
            "sequential search",
            "gold adjudication",
            ".local/codex-result.md as scientific input",
        ],
    }

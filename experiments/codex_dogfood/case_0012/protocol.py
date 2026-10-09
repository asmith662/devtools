# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, TRY003 -- literal protocol prose or fixture assertions; formatter owns commas
"""Pre-content authored task semantics, hint reference, associations and queries."""

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
from experiments.codex_dogfood.case_0009.artifacts import binary, digest
from experiments.exact_hint_routing.extraction import caller_observation, extract
from experiments.exact_hint_routing.models import HintAssociation, HintCategory
from experiments.exact_hint_routing.routing import admit
from experiments.exact_hint_routing.serialization import project

CASE = Path(__file__).resolve().parent
START = "0c0029a2d608bafe95c6792fe04b4127e17f0304"
TASK_ID = LocalizationTaskIdentity("case-0012-direct-source-disclosure")
# Independently caller-authored before frame construction; never derived from rules.
CALLER_HINTS = (
    (
        "devtools.context.python.modules.selection.select_python_module_source_declarations",
        "PYTHON_DIRECT_FUNCTION",
        ("source",),
    ),
    (
        "devtools.context.planning.plan.DisclosurePlan",
        "PYTHON_DIRECT_CLASS",
        ("choices",),
    ),
    ("devtools.context.planning", "PYTHON_MODULE", ("choices",)),
    (
        "devtools.context.repository.snapshot.RepositorySnapshot.resource_at",
        "PYTHON_DIRECT_METHOD",
        ("integrity",),
    ),
    ("ContextDisclosure", "PYTHON_DIRECT_CLASS", ("materialization",)),
    ("ModelRequest", "PYTHON_DIRECT_CLASS", ("assembly",)),
    (
        "src/devtools/context/planning/docs/overview.md",
        "RESOURCE_ADDRESS",
        ("documentation",),
    ),
    ("docs/architecture.md", "RESOURCE_ADDRESS", ("documentation",)),
    ("scripts/validate_development.py", "RESOURCE_ADDRESS", ("validation",)),
    ("pyproject.toml", "RESOURCE_ADDRESS", ("validation",)),
)
# Exact statement, bounded satisfaction criterion, task line basis, exact query.
OBLIGATIONS = (
    (
        "source",
        "Establish supported direct function/class source selection and native direct-method containment, with source/binding scope distinctions.",
        "Complete native selection/containment contracts and unsupported runtime/import/inherited/semantic boundaries are established.",
        (1, 2),
        "Python direct source declaration selection class function method containment decorated repeated declarations",
    ),
    (
        "choices",
        "Establish explicit immutable ordered Context Planning choice integration and compatibility.",
        "Purpose, frame, ordered choice invariants, admission and existing qualified-reference/whole-resource compatibility are established.",
        (1, 3),
        "DisclosurePlan Context Planning explicit choice immutable purpose snapshot ordered qualified reference whole resource",
    ),
    (
        "integrity",
        "Establish native frame/content/declaration validation before disclosure publication without reacquisition.",
        "Foreign/stale/content/missing-resource/scope/returned-identity checks and publication ordering are established.",
        (4,),
        "RepositorySnapshot native declaration materialization stale foreign content identity missing resource validation",
    ),
    (
        "materialization",
        "Establish exact source-segment materialization, provenance, UTF-8 boundaries and faithful mixed-plan order.",
        "Source-range, derivation, owner provenance, decorators, CRLF/non-ASCII and ordered mixed representations are established without implicit expansion or sufficiency.",
        (5,),
        "ContextDisclosure source segment native provenance source range UTF-8 decorators CRLF non ASCII mixed plan order",
    ),
    (
        "assembly",
        "Establish unchanged rendering and copied-request semantics without new budgets.",
        "Original fields/tools and prompt role, task-before-Context copying, rendering compatibility and absence of truncation changes are established.",
        (6,),
        "ModelRequest copied prompt role settings conversation provider tools rendering Context task unchanged assembly",
    ),
    (
        "exports",
        "Establish common planning and outer facade exports and permitted dependency ownership.",
        "Both public boundaries and absence of Retrieval/language-specific common assembly dependencies are established.",
        (7,),
        "Context planning public facade exports __all__ dependency Retrieval common assembly",
    ),
    (
        "tests",
        "Establish focused and regression test conventions for every new and preserved contract.",
        "Direct/decorated/repeated declarations, mixed exact provenance, rejection, old choices and copied-request preservation tests are established.",
        (8,),
        "Context planning tests direct function class method decorated repeated declaration mixed plan provenance stale rejection copied request",
    ),
    (
        "documentation",
        "Establish package and architecture documentation to update with supported/deferred source-disclosure scope.",
        "Source versus runtime binding, explicit admission, compatibility and no automatic relevance/readiness claims are documented.",
        (9,),
        "Context planning documentation architecture direct source runtime binding explicit representation admission compatibility",
    ),
    (
        "validation",
        "Establish the complete protected validation/tooling contract and preserved configuration.",
        "Protected development entry/scope and pytest/coverage retention, Ruff lint/format, strict mypy, worktree/index checks and excluded confirmation boundary are established.",
        (10,),
        "protected development validation pytest coverage configuration Ruff format strict mypy staged diff whitespace",
    ),
)
DECISION = {
    "scientific_safety": "Compare exact independent-gold REQUIRED resource, owning-cell and distinct/owning-unit reach sets: B and C must lose none of A. Candidate union cannot lose any original positive lexical resource.",
    "soundness": "Every promoted occurrence has one RESOLVED supported native route in the frozen frame. AMBIGUOUS/UNRESOLVED/UNSUPPORTED promote nothing. All original lexical positive rows survive with exact native scores/ranks/contributions; global safety lane is unchanged.",
    "extraction": "Report accepted rule/reference pairs, false rule extractions, caller-only hints, type disagreements and explicit denominators. Caller review is a task-text reference, not universal truth. No fabricated locator or inferred unqualified owner is permitted.",
    "completion": "Independent blind gold defines units, applicability and complete witness alternatives. Evaluate all complementary members in each alternative. Choose minimum lane completion depth, then deterministic gold alternative identity; never combine alternative members. Missing completion is null. Case union is deduplicated across mandatory applicable chosen prefixes; occurrences remain repeated. Labels are owning-obligation-relative; bytes count unique UTF-8 resource content.",
    "meaningful_value": "At least one: (1) a REQUIRED hint-associated target with native owning-lane lexical rank >20 reaches routed position <=3; OR (2) one hint-supported obligation has exact-first unique prefix <=4/5*A and case-wide unique union <=21/20*A; OR (3) summed unnecessary prefix occurrences over hint-supported obligations <=4/5*A and case-wide unique union <=21/20*A. A zero unnecessary baseline requires zero changed noise and supplies no reduction evidence. A null/undefined baseline cannot pass a numeric gate.",
    "obligation_safety": "Every mandatory applicable obligation's exact-first unique completion prefix <=5/4*A's best valid prefix. Undefined complete baseline cannot pass support. No averaging across obligations.",
    "cost": "Report hint extraction, module/universe construction, index build, each exact request and presentation, all queries and shared costs. Treatment charged time = common native lexical build + obligation/full-task query time + arm-specific extraction/reference projection + exact resolution + presentation. B/C <=3*A using exact integer nanoseconds. Common frame construction reported separately and charged equally. Query strings execute once each and their captured rows are reused unchanged across arms; each B/C route request executes once per arm with no cross-arm outcome cache.",
    "precedence": "1 Invalid frame/identity/query/score/gold/blindness/promotion/fallback contracts or independently demonstrated incomplete mandatory task interpretation => EXPERIMENTAL_CONTRACT_DEFECT. 2 Any false rule extraction, type disagreement, or caller-only hint that B soundly resolves to REQUIRED evidence => EXTRACTION_OR_RESOLUTION_DEFECT. Genuine ambiguous/unresolved/unsupported native scope outcomes alone are not defects. 3 C passes scientific safety, soundness, extraction quality, meaningful value, obligation safety and cost => EXACT_HINT_ROUTING_SUPPORTED. 4 Sound reach-safe B or C offers positive target depth/prefix/byte value but not all C gates => COMPLEMENTARY_BUT_LIMITED. 5 Otherwise NO_MATERIAL_VALUE. Evaluate B and C gates separately and report any C loss of caller route value.",
    "arithmetic": "Use integer cross products for 4/5,21/20,5/4,3/1; do not round before decisions. Null never equals a synthetic rank; zero denominators are explicit. Actual evidence-inspection cost NOT MEASURED; prefixes describe counterfactual completion-prefix inspection burden.",
    "failure_attribution": [
        "HINT_EXTRACTION_MISS",
        "FALSE_HINT_EXTRACTION",
        "HINT_TYPE_MISCLASSIFICATION",
        "UNSUPPORTED_EXACT_HINT",
        "AMBIGUOUS_EXACT_HINT",
        "UNRESOLVED_EXACT_HINT",
        "EXACT_ROUTE_TARGET_NOT_REQUIRED",
        "EXACT_HINT_NOT_ROUTED",
        "LEXICAL_FALLBACK_RANKING_FAILURE",
        "INFORMATION_NEED_AUTHORING_FAILURE",
    ],
    "search_policy_failure": "NOT_ASSESSED; no iterative sequential search policy",
    "outcomes": [
        "EXACT_HINT_ROUTING_SUPPORTED",
        "COMPLEMENTARY_BUT_LIMITED",
        "NO_MATERIAL_VALUE",
        "EXTRACTION_OR_RESOLUTION_DEFECT",
        "EXPERIMENTAL_CONTRACT_DEFECT",
    ],
}


def definition() -> dict[str, Any]:
    """Project independently authored task semantics without native hint resolution."""
    text = binary(CASE / "task.txt").decode("utf-8")
    lines = text.splitlines(keepends=True)
    bases: list[dict[str, Any]] = []
    offset = 0
    for line in lines:
        bases.append({"start": offset, "end": offset + len(line), "text": line})
        offset += len(line)
    obligations: list[dict[str, Any]] = [
        {
            "identity": f"{TASK_ID.value}/{key}",
            "key": key,
            "statement": statement,
            "criterion": criterion,
            "applicability": "MANDATORY for the selected future source-disclosure task; independent gold may retain NOT_APPLICABLE only with explicit rationale",
            "task_basis": [bases[n - 1] for n in numbers],
            "query": query,
            "analyzed_terms": list(
                analyze_repository_text_lexical_query(text=query).normalized_terms
            ),
        }
        for key, statement, criterion, numbers, query in OBLIGATIONS
    ]
    caller = []
    associations: list[HintAssociation] = []
    for literal, category, lanes in CALLER_HINTS:
        # Match exact code token, never a repository name/owner search.
        token = f"`{literal}`"
        if text.count(token) != 1:
            raise ValueError("Caller hint token not unique in authored task")
        start = text.index(token) + 1
        hint = caller_observation(
            TASK_ID,
            text,
            start=start,
            end=start + len(literal),
            category=HintCategory(category),
            rationale="Caller task-syntax review: explicitly introduced code reference; no repository contents, ranks, gold or resolutions inspected",
        )
        caller.append(hint)
        associations.extend(
            HintAssociation(
                hint.identity,
                LocalizationObligationIdentity(TASK_ID, lane),
                "The exact task clause containing this hint is interpreted by this obligation; association makes no relevance/satisfaction claim",
                TaskProvenance(
                    TASK_ID.value,
                    hint.span,
                    "Caller-authored task-only association before native frame lookup",
                ),
            )
            for lane in lanes
        )
    decisions = extract(TASK_ID, text)
    rule = tuple(d.observation for d in decisions if d.observation is not None)
    by_identity = {h.identity: h for h in caller}
    rule_ids = {h.identity for h in rule}
    anchors = tuple(
        LocalizationAnchor(
            LocalizationAnchorIdentity(TASK_ID, h.identity.value), h.text, h.provenance
        )
        for h in caller
    )
    native_obligations = tuple(
        LocalizationObligation(
            LocalizationObligationIdentity(TASK_ID, o["key"]),
            o["statement"],
            tuple(
                a.identity
                for a in anchors
                if any(
                    s.hint.value == a.identity.value and s.lane.value == o["key"]
                    for s in associations
                )
            ),
            TaskProvenance(
                TASK_ID.value,
                TaskTextSpan(o["task_basis"][0]["start"], o["task_basis"][-1]["end"]),
                "Caller task-clause interpretation; no witness gold",
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
        TaskProvenance(
            TASK_ID.value, explanation="Exact future feature task; task-only authoring"
        ),
        anchors,
        native_obligations,
    )
    native_queries = tuple(
        ObligationLexicalQuery(
            LocalizationQueryIdentity(TASK_ID, "obligation/" + o["key"]),
            n.identity,
            o["query"],
        )
        for o, n in zip(obligations, native_obligations, strict=True)
    )
    routes = {
        "B": [
            admit(h, a) for h in caller for a in associations if a.hint == h.identity
        ],
        "C": [admit(h, a) for h in rule for a in associations if a.hint == h.identity],
    }
    if any(h.identity not in by_identity for h in rule):
        raise ValueError(
            "Unassociated rule-only extraction requires pre-execution caller association review"
        )
    matrix = []
    for n, basis in enumerate(bases, 1):
        owners = [
            o["key"] for o in obligations if any(b == basis for b in o["task_basis"])
        ]
        operational = basis["text"].startswith("Operational:")
        if not owners and not operational:
            raise ValueError("Task clause lacks obligation or operational exclusion")
        matrix.append(
            {
                "requirement": f"R{n:02}",
                "basis": basis,
                "obligations": owners,
                "exclusion": "OPERATIONAL_ONLY; no repository semantics/hints/queries/witnesses or scientific frame membership"
                if operational
                else None,
            }
        )
    return {
        "schema": "case-0012-stage-a-treatment-v1",
        "task_identity": TASK_ID.value,
        "task_text": text,
        "task_sha256": digest(text.encode()),
        "task_requirement_matrix": matrix,
        "native_task_interpretation": project(native_task),
        "native_obligation_queries": project(native_queries),
        "hint_inventory": [
            {
                **project(h),
                "identity": project(h.identity),
                "rule_extracted": h.identity in rule_ids,
                "caller_reviewed": True,
            }
            for h in caller
        ],
        "obligations": obligations,
        "caller_reviewed_hint_reference": [
            {**project(h), "identity": project(h.identity)} for h in caller
        ],
        "rule_extracted_hints": [
            {**project(h), "identity": project(h.identity)} for h in rule
        ],
        "extraction_decisions": project(decisions),
        "hint_associations": project(associations),
        "exact_route_requests": {
            arm: [{**project(r), "identity": r.identity} for r in requests]
            for arm, requests in routes.items()
        },
        "extraction_agreement": {
            "caller_count": len(caller),
            "rule_count": len(rule),
            "accepted_rule_hints": len(rule_ids & by_identity.keys()),
            "false_rule_extractions": len(rule_ids - by_identity.keys()),
            "caller_only_hints": len(by_identity.keys() - rule_ids),
            "type_disagreements": sum(
                h.category != by_identity[h.identity].category for h in rule
            ),
            "scope": "Task-text caller reference agreement; no repository resolution or universal truth claim",
        },
        "non_hint_conceptual_requirements": list(obligations),
        "global_safety_query": {
            "text": text,
            "analyzed_terms": list(
                analyze_repository_text_lexical_query(text=text).normalized_terms
            ),
            "route": "UNCHANGED_CANONICAL_RESOURCE_BM25_SAFETY_REFERENCE",
        },
        "settings": {
            "maximum_results": "entire frozen resource count; all positive native rows",
            "k1": 1.2,
            "b": 0.75,
            "filename_weight": 0.25,
            "tokenizer": "unicode-word-span-casefold-v1",
            "representation": "whole-resource-exact-text-v1",
            "tie_order": "native descending score then frozen document order",
            "fusion": False,
            "reformulation": False,
            "BM25F": False,
            "identifier_aware_view": False,
        },
        "arms": {
            "A": "LEXICAL_ONLY: identical nine obligation queries; no exact routing",
            "B": "CALLER_HINT_EXACT_FIRST: caller task-only reference; supported exact routes + complete unchanged lexical fallback; route-value upper bound under this reviewed task-text inventory, not a universal oracle",
            "C": "RULE_EXTRACTED_EXACT_FIRST: mechanically extracted hints only; same supported routing and complete unchanged lexical fallback",
        },
        "decision_rule": DECISION,
        "treatment_executions": 0,
        "lexical_query_executions": 0,
        "exact_route_executions": 0,
        "stage_b": "NOT_EXECUTED",
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "excluded": [
            "repository hint resolution outcomes",
            "ranks",
            "scores",
            "gold",
            "treatment results",
            "confirmation/reserve",
            ".local/codex-result.md as scientific/task input",
        ],
    }

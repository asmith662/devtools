# Copyright (c) 2026
# ruff: noqa: E501, INP001, COM812
"""Case 0006 caller intent, authored before any treatment execution."""

from __future__ import annotations

TASK = "Implement the first production candidate-witness resolution-recording capability for Localization around `CandidateWitnessHypothesis` and generated witness candidates. The capability should let callers record explicit evidence-based dispositions for unresolved competing hypotheses and complementary members while preserving native evidence provenance, repository/snapshot identity, and the distinction between candidate hypotheses and accepted witnesses. Provide a validated seam for promoting a completely supported candidate hypothesis into the existing `WitnessSet`, `SupportedWitness`, `LocalizationAssessment`, and readiness flow without inferring support from rank, routing tier, role evidence, or evidence count. Integrate coherently with the existing `CandidateWitnessView`, `WitnessGenerationView`, and `AnchorGroundingView`, add rigorous tests and authoritative architecture/development documentation, preserve package/API conventions where applicable, and pass protected development validation. Do not implement an automatic resolution policy, candidate elimination, numeric confidence, learned ranking, autonomous sequential acquisition, or Context Planning admission."
PURPOSE = (
    "Acquire and generate repository information needed to implement the frozen "
    "candidate-witness resolution-recording capability while independently "
    "measuring global lexical, obligation lexical, role-routed and bounded "
    "structurally generated candidate surfaces."
)

ANCHORS = {
    "hypothesis": "CandidateWitnessHypothesis",
    "candidate-view": "CandidateWitnessView",
    "generation-view": "WitnessGenerationView",
    "grounding-view": "AnchorGroundingView",
    "witness-set": "WitnessSet",
    "supported-witness": "SupportedWitness",
    "assessment": "LocalizationAssessment",
    "readiness": "readiness flow",
    "provenance": "native evidence provenance and repository/snapshot identity",
    "quality": "rigorous tests, authoritative documentation and protected validation",
}

# identity, predicate, anchors, named criterion, criterion statement, condition
OBLIGATIONS = (
    (
        "hypothesis-records",
        "Establish unresolved candidate hypothesis and view contracts needed for explicit evidence-based disposition records without automatic resolution.",
        ("hypothesis", "candidate-view"),
        "unresolved-disposition-contract",
        "Identify hypothesis and view identity, membership, competition and unresolved boundaries needed to record explicit caller dispositions.",
        None,
    ),
    (
        "member-complementarity",
        "Establish how complementary hypothesis members and competing alternatives relate to accepted WitnessSet algebra.",
        ("hypothesis", "witness-set"),
        "complementary-member-algebra",
        "Identify the all-members/any-alternative contracts and the evidence needed to avoid partial promotion.",
        None,
    ),
    (
        "generated-integration",
        "Establish integration of generated candidates and grounded task anchors with explicit resolution records.",
        ("generation-view", "grounding-view", "hypothesis"),
        "generated-grounded-seam",
        "Identify how generation attempts, hypotheses and grounding outcomes retain task-relative provenance without implying resolution.",
        None,
    ),
    (
        "accepted-promotion",
        "Establish a validated seam from a completely supported candidate hypothesis to WitnessSet and SupportedWitness without inference from rank, tier, role or evidence count.",
        ("hypothesis", "witness-set", "supported-witness"),
        "complete-supported-promotion",
        "Identify accepted target and evidence contracts sufficient to require every complementary member's explicit support before promotion.",
        None,
    ),
    (
        "assessment-readiness",
        "Establish LocalizationAssessment disposition and readiness contracts governing promotion into satisfaction flow.",
        ("assessment", "readiness", "supported-witness"),
        "assessment-readiness-boundary",
        "Identify assessment and readiness validation such that a candidate record alone does not satisfy an obligation.",
        None,
    ),
    (
        "provenance-frame",
        "Establish native evidence and repository/snapshot/task-frame compatibility for candidate dispositions and promoted supports.",
        ("provenance", "hypothesis", "supported-witness"),
        "native-evidence-frame",
        "Identify native evidence references and identity checks needed to reject foreign or stale candidate and promotion data.",
        None,
    ),
    (
        "package-integration",
        "Establish applicable Localization package/API conventions for the resolution-recording capability.",
        ("candidate-view", "generation-view", "grounding-view"),
        "coherent-package-api",
        "Identify governing public package conventions if they apply to exposing this capability.",
        "Existing package/API conventions govern exposure of the new capability.",
    ),
    (
        "tests",
        "Establish test conventions and cases for complementary and competing dispositions, promotion, native provenance, snapshot failures and semantic non-claims.",
        ("hypothesis", "generation-view", "quality"),
        "resolution-boundary-tests",
        "Identify rigorous neighboring tests and conventions for valid, invalid, unresolved and no-inference behavior.",
        None,
    ),
    (
        "documentation",
        "Establish authoritative Localization architecture and development documentation ownership for the new capability and exclusions.",
        ("quality", "hypothesis"),
        "authoritative-resolution-documentation",
        "Identify governing documentation and update conventions for resolution records and their boundary with accepted witnesses.",
        None,
    ),
    (
        "validation",
        "Establish protected development validation and static quality-gate contract.",
        ("quality",),
        "protected-validation-contract",
        "Identify canonical command, profile and static gates; future pass/fail execution is not a repository witness.",
        None,
    ),
)

# One explicit lexical lane and one non-weighted role preference per obligation.
QUERIES = (
    (
        "hypothesis-records",
        "CandidateWitnessHypothesis CandidateWitnessView unresolved competing hypotheses explicit evidence disposition",
        ("PYTHON_CODE",),
    ),
    (
        "member-complementarity",
        "CandidateWitnessHypothesis complementary members competing alternatives WitnessSet all members any alternative",
        ("PYTHON_CODE",),
    ),
    (
        "generated-integration",
        "WitnessGenerationView AnchorGroundingView generated witness candidates grounding attempts provenance",
        ("PYTHON_CODE",),
    ),
    (
        "accepted-promotion",
        "WitnessSet SupportedWitness completely supported candidate hypothesis evidence promotion",
        ("PYTHON_CODE",),
    ),
    (
        "assessment-readiness",
        "LocalizationAssessment readiness resolved supported witnesses obligation disposition",
        ("PYTHON_CODE",),
    ),
    (
        "provenance-frame",
        "native evidence provenance repository snapshot task frame candidate witness support compatibility",
        ("PYTHON_CODE",),
    ),
    (
        "package-integration",
        "Localization package API exports CandidateWitnessView WitnessGenerationView AnchorGroundingView",
        ("PACKAGE_SURFACE", "PACKAGE_MEMBER"),
    ),
    (
        "tests",
        "Localization candidate witness resolution generated hypotheses complementary competing provenance snapshot tests",
        ("TEST",),
    ),
    (
        "documentation",
        "Localization candidate witness resolution architecture development documentation accepted witness boundaries",
        ("DOCUMENTATION",),
    ),
    (
        "validation",
        "protected development validation command coverage Ruff mypy format quality gates",
        (),
    ),
)

# Only public export surfaces and their direct import declarations were consulted.
# A request identity is local to this treatment; no resolver is invoked here.
LOCATORS = (
    (
        "g-hypothesis",
        "hypothesis",
        "PYTHON_DECLARATION",
        "devtools.context.localization.association.hypothesis",
        "CandidateWitnessHypothesis",
        "association/__init__.py exports the class from its direct declaration module",
    ),
    (
        "g-candidate-view",
        "candidate-view",
        "PYTHON_DECLARATION",
        "devtools.context.localization.association.hypothesis",
        "CandidateWitnessView",
        "association/__init__.py exports the class from its direct declaration module",
    ),
    (
        "g-generation-view",
        "generation-view",
        "PYTHON_DECLARATION",
        "devtools.context.localization.generation.contract",
        "WitnessGenerationView",
        "generation/__init__.py exports the class from its direct declaration module",
    ),
    (
        "g-grounding-view",
        "grounding-view",
        "PYTHON_DECLARATION",
        "devtools.context.localization.grounding.view",
        "AnchorGroundingView",
        "grounding/__init__.py exports the class from its direct declaration module",
    ),
    (
        "g-witness-set",
        "witness-set",
        "PYTHON_DECLARATION",
        "devtools.context.localization.obligation",
        "WitnessSet",
        "localization/__init__.py exports the class from its direct declaration module",
    ),
    (
        "g-supported-witness",
        "supported-witness",
        "PYTHON_DECLARATION",
        "devtools.context.localization.assessment",
        "SupportedWitness",
        "localization/__init__.py exports the class from its direct declaration module",
    ),
    (
        "g-assessment",
        "assessment",
        "PYTHON_DECLARATION",
        "devtools.context.localization.assessment",
        "LocalizationAssessment",
        "localization/__init__.py exports the class from its direct declaration module",
    ),
    (
        "g-readiness",
        "readiness",
        "PYTHON_DECLARATION",
        "devtools.context.localization.readiness",
        "LocalizationReadiness",
        "localization/__init__.py exports the public readiness value; task explicitly requires its flow",
    ),
    (
        "g-validation",
        "quality",
        "RESOURCE_ADDRESS",
        "scripts/validate_development.py",
        None,
        "AGENTS.md gives the exact protected validation entry point",
    ),
)

# One tuple per caller-authored alternative; members are ALL, alternatives ANY.
# Each member is (stable key, grounding request identity, exact operator, reason).
RECIPES = (
    (
        "hypothesis-records",
        "hypothesis-contract",
        (
            (
                "hypothesis",
                "g-hypothesis",
                "OWNER_RESOURCE",
                "The named hypothesis declaration can explain unresolved identity and membership.",
            ),
        ),
    ),
    (
        "hypothesis-records",
        "view-contract",
        (
            (
                "view",
                "g-candidate-view",
                "OWNER_RESOURCE",
                "The named candidate view declaration can explain unresolved collection semantics.",
            ),
        ),
    ),
    (
        "member-complementarity",
        "hypothesis-plus-accepted-algebra",
        (
            (
                "hypothesis",
                "g-hypothesis",
                "OWNER_RESOURCE",
                "Candidate complementarity must be understood.",
            ),
            (
                "accepted",
                "g-witness-set",
                "OWNER_RESOURCE",
                "Accepted witness conjunction must be understood separately.",
            ),
        ),
    ),
    (
        "generated-integration",
        "generation-plus-grounding",
        (
            (
                "generation",
                "g-generation-view",
                "OWNER_RESOURCE",
                "Generated candidate view contract is relevant.",
            ),
            (
                "grounding",
                "g-grounding-view",
                "OWNER_RESOURCE",
                "Grounding view outcome contract is relevant.",
            ),
        ),
    ),
    (
        "accepted-promotion",
        "accepted-types",
        (
            (
                "set",
                "g-witness-set",
                "OWNER_RESOURCE",
                "Accepted alternative membership contract is relevant.",
            ),
            (
                "support",
                "g-supported-witness",
                "OWNER_RESOURCE",
                "Supported member evidence contract is relevant.",
            ),
        ),
    ),
    (
        "assessment-readiness",
        "assessment-plus-readiness",
        (
            (
                "assessment",
                "g-assessment",
                "OWNER_RESOURCE",
                "Assessment disposition contract is relevant.",
            ),
            (
                "readiness",
                "g-readiness",
                "OWNER_RESOURCE",
                "Readiness contract is relevant.",
            ),
        ),
    ),
    (
        "provenance-frame",
        "candidate-plus-evidence",
        (
            (
                "candidate",
                "g-hypothesis",
                "OWNER_RESOURCE",
                "Candidate frame validation is relevant.",
            ),
            (
                "support",
                "g-supported-witness",
                "OWNER_RESOURCE",
                "Accepted evidence frame is relevant.",
            ),
        ),
    ),
    (
        "tests",
        "association-mirror",
        (
            (
                "association-test",
                "g-hypothesis",
                "MIRRORED_RESOURCE",
                "An observed mirror may expose analogous hypothesis tests.",
            ),
        ),
    ),
    (
        "tests",
        "generation-mirror",
        (
            (
                "generation-test",
                "g-generation-view",
                "MIRRORED_RESOURCE",
                "An observed mirror may expose analogous generation tests.",
            ),
        ),
    ),
)

MISS_CATEGORIES = (
    "NO_GROUNDING_REQUEST",
    "GROUNDING_UNRESOLVED",
    "GROUNDING_AMBIGUOUS",
    "GROUNDING_UNSUPPORTED",
    "NO_RECIPE",
    "PROJECTION_NO_TARGET",
    "PROJECTION_ABSTAINED",
    "WRONG_STRUCTURAL_TARGET",
    "OPERATOR_CAPABILITY_GAP",
    "CROSS_ROLE_NONSTRUCTURAL",
    "TASK_INTERPRETATION_GAP",
    "OTHER_WITH_EXPLANATION",
)


def treatment() -> dict:
    """Serialize caller-authored intent; never resolve a locator or query."""
    provenance = {
        "source": "exact-frozen-task",
        "explanation": "Caller interpretation before treatment execution.",
    }
    obligations = [
        {
            "identity": identity,
            "predicate": predicate,
            "anchors": list(anchors),
            "provenance": provenance,
            "requirement": "mandatory",
            "satisfaction": {"name": criterion, "statement": statement},
            "witness_alternatives": [],
            "applicability_condition": condition,
        }
        for identity, predicate, anchors, criterion, statement, condition in OBLIGATIONS
    ]
    queries = [
        {
            "identity": f"q-{identity}",
            "obligation": identity,
            "text": query,
            "ordinal": ordinal,
            "preferred_roles": list(roles),
            "preference_rationale": "Caller preference follows the information requirement, before role evidence; empty when no single supported role covers the contract."
            if not roles
            else "Caller preference follows the information requirement, before role evidence.",
        }
        for ordinal, (identity, query, roles) in enumerate(QUERIES, 1)
    ]
    groundings = [
        {
            "identity": identity,
            "anchor": anchor,
            "locator_kind": kind,
            "locator": {"module": value, "name": name, "declaration_kind": "CLASS"}
            if kind == "PYTHON_DECLARATION"
            else {"address": value},
            "interpretation_provenance": {
                "source": "public-surface-or-repository-policy",
                "explanation": reason,
            },
        }
        for identity, anchor, kind, value, name, reason in LOCATORS
    ]
    recipes = [
        {
            "obligation": obligation,
            "identity": identity,
            "provenance": provenance,
            "members": [
                {
                    "identity": key,
                    "grounding_request": request,
                    "projection": projection,
                    "reason": reason,
                    "provenance": provenance,
                }
                for key, request, projection, reason in members
            ],
        }
        for obligation, identity, members in RECIPES
    ]
    return {
        "schema": "codex-bounded-generation-treatment-v1",
        "case": "case_0006",
        "status": "FROZEN BEFORE RETRIEVAL, ROUTING, GROUNDING, GENERATION AND ADJUDICATION",
        "starting_head": "492229e0e0d4661cf5287c26d18c6488a80fe8ce",
        "task_identity": "codex-dogfood-case-0006-resolution-recording",
        "task_full_prompt": TASK,
        "purpose": PURPOSE,
        "anchors": [
            {"identity": identity, "text": text, "provenance": provenance}
            for identity, text in ANCHORS.items()
        ],
        "obligations": obligations,
        "global_lane": {
            "identity": "global-full-task",
            "query_text": TASK,
            "routed": False,
        },
        "obligation_queries": queries,
        "grounding_requests": groundings,
        "generation_recipes": recipes,
        "ungrounded_anchors": {
            "provenance": "No exact single task-named RI referent follows from the abstract evidence/frame requirement."
        },
        "no_recipe_obligations": {
            "package-integration": "Owner/mirror projections do not establish public API convention.",
            "documentation": "No exact task-named documentation locator or documentation projection exists.",
            "validation": "Exact validation entry point is grounded, but owner/mirror projection does not establish the full validation contract.",
        },
        "eligibility": {
            "areas": ["src/", "docs/", "tests/"],
            "suffixes": [".py", ".md", ".toml", ".yaml", ".yml"],
            "explicit_inclusions": [
                "README.md",
                "AGENTS.md",
                "pyproject.toml",
                "scripts/validate_development.py",
            ],
            "exclusions": [
                "docs/implementation_ledger.md",
                "tests/experiments/",
                "all experiments/",
                "other scripts/",
                "caches",
                "untracked/local",
                "binaries",
            ],
            "rationale": "Established broad prospective source, ordinary-test, documentation and configuration frame, selected from starting commit only.",
        },
        "role_inputs_recipe": {
            "module_roots": ["src", "tests"],
            "resource_selection": "Every eligible Python resource beneath each root in lexical address order.",
            "memberships": "Canonical immediate package membership per root analysis.",
            "mirrors": "Canonical observed Python source/test path correspondences over frozen snapshot.",
            "configuration_resources": ["pyproject.toml"],
            "configuration_resolution": "Canonical project declarations/selectors, module universe from both roots, explicit working-directory and pytest root '.'.",
            "retention": "Retain native analyses and derived role view; do not inspect assignments to tune treatment.",
        },
        "routing": {
            "identity": "caller-role-or-stable-two-tier-v1",
            "owner": "devtools.context.localization.routing",
            "tiers": ["PREFERRED_ROLE_SUPPORTED", "ESCAPE"],
            "matching": "ANY selected positive role; empty preference is escape-only.",
            "order": "Preferred before escape, native order within tiers; preserve native rank and every candidate.",
            "global": "Native and unrouted.",
            "candidate_retention": "All native candidates survive.",
        },
        "generation_execution": {
            "grounding": "Execute each frozen request exactly once with retained native module universe.",
            "binding": "Bind exact result to each member specification without repair. Construct production GroundedMemberRecipe and WitnessGenerationRecipe values for all syntactically valid specifications; unresolved/ambiguous/unsupported results remain production attempt outcomes. If construction fails, retain explicit abstention.",
            "plan": "Run one production WitnessGenerationPlan per task/frame with all frozen recipes, acquisition, role view and routed view; no lexical-only generation.",
            "operator_vocabulary": ["OWNER_RESOURCE", "MIRRORED_RESOURCE"],
            "multi_target": "Single-target admission; no Cartesian expansion or selection among ambiguous results.",
        },
        "measurements": {
            "surfaces": [
                "A global native lexical BM25",
                "B own-obligation native lexical BM25",
                "C own-obligation positive role-routed presentation",
                "D unranked generated hypothesis targets",
            ],
            "generated_size": [
                "requests",
                "grounding dispositions",
                "recipes attempted",
                "member projection attempts",
                "successful and abstained recipes",
                "hypotheses",
                "members",
                "obligation/resource occurrences",
                "unique generated resources",
            ],
            "gold_coverage": [
                "required occurrence coverage by obligation",
                "unique required-resource coverage",
                "per-obligation required-resource coverage",
                "complete mandatory obligation alternative coverage",
            ],
            "structure": "Separately report resource presence and exact generated hypothesis containing one complete acceptable adjudicated alternative with correct complementary members; no credit from mere resource presence for structure.",
            "precision": "Required generated obligation/resource occurrences divided by all generated obligation/resource occurrences; report helpful, unnecessary and unresolved separately with competing alternatives preserved.",
            "baselines": "For each applicable mandatory obligation calculate every acceptable alternative's complete global/native/routed depth or miss; choose best finite separately by surface. Report global task-complete depth, obligation-wise native/routed maxima and finite completion-prefix summed occurrences and unique unions. An incomplete obligation makes whole-case prefix comparison incomplete.",
            "sufficient_union": "Minimum unique adjudicated resource union over one complete accepted alternative per applicable mandatory obligation, independent of rank; report candidate union divided by and minus this bound only if defined. This is not an implementation file set.",
            "miss_categories": list(MISS_CATEGORIES),
            "support_attachment": [
                "global lexical",
                "own-obligation lexical",
                "positive role evidence",
                "preferred routing",
                "escape routing",
                "structural only",
            ],
            "work_fanout": [
                "grounding request count/dispositions",
                "projection counts",
                "examined resources",
                "result counts",
                "truncation/frontier",
                "hypotheses per obligation",
                "targets per hypothesis",
            ],
            "interpretation": "Descriptive candidate size versus coverage only; no numeric pass threshold or generated rank/depth.",
        },
        "blind_adjudication": {
            "allowed": [
                "exact task",
                "purpose",
                "anchors",
                "obligations and criteria",
                "eligible resource identities/content",
                "governing architecture in frozen contents",
            ],
            "forbidden": [
                "lexical queries",
                "role preferences or assignments",
                "retrieval/routing results",
                "grounding requests/locators/results",
                "recipe specs/operators",
                "generated targets/hypotheses/outcomes",
                "ranks/scores/positions",
                "treatment provenance",
            ],
            "judgments": [
                "applicability",
                "REQUIRED",
                "HELPFUL_ONLY",
                "UNNECESSARY",
                "unresolved",
                "acceptable witness alternatives",
                "task-start inferability",
                "inherent discovery prerequisites",
                "task-interpretation gaps",
            ],
            "method": "Fresh-session independent blind Stage C after treatment-free packet; no implementation or treatment outcomes used as gold.",
        },
        "authoring_surfaces": [
            "AGENTS.md",
            "src/devtools/context/localization/docs/overview.md",
            "src/devtools/context/localization/__init__.py",
            "src/devtools/context/localization/association/__init__.py",
            "src/devtools/context/localization/generation/__init__.py",
            "src/devtools/context/localization/grounding/__init__.py",
        ],
        "firewall": dict.fromkeys(
            (
                "lexical_acquisition_executed",
                "role_routing_executed",
                "exact_grounding_executed",
                "witness_generation_executed",
                "adjudication_performed",
                "development_task_implemented",
                "historical_gold_used",
                "confirmation_accessed",
            ),
            False,
        ),
        "post_freeze_changes": "Never repair this treatment after results. Material correction requires a separately named treatment preserving this original case.",
    }

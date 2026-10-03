"""Case 0006 manual blind judgments; no production imports or acquisition."""

from inspect_blind import resources

BASE = "src/devtools/context/localization/"


def authored():
    """Return the manually reviewed units and obligation-specific decisions."""
    frame = {r["address"]: r for r in resources()}
    units = {}

    def unit(key, path, ranges, information):
        resource = frame[path]
        units[key] = {
            "identity": key,
            "resource_identity": resource["identity"],
            "line_ranges": ranges,
            "information": information,
            "precision_rationale": "Selected declaration/function or coherent contract section; unrelated file content is not required.",
        }

    unit(
        "candidate-key",
        BASE + "association/hypothesis.py",
        [[39, 50]],
        "WitnessHypothesisIdentity is obligation-scoped with a nonblank caller key; same textual key in a different obligation is a different identity.",
    )
    unit(
        "candidate-member",
        BASE + "association/hypothesis.py",
        [[53, 136]],
        "Member target is an observed resource; reason and positive native support are required. Lexical, role, routed and structural supports remain separate, deduplicated and deterministically ordered.",
    )
    unit(
        "candidate-shape",
        BASE + "association/hypothesis.py",
        [[139, 212]],
        "Nonempty distinct resource members are conjunctive; hypothesis peers compete within an obligation. CandidateWitnessView retains task/snapshot/native inputs and exposes unresolved obligation/target queries without accepted-witness state.",
    )
    unit(
        "candidate-validation",
        BASE + "association/hypothesis.py",
        [[215, 357]],
        "Builder validates full task and repository/snapshot frames, known unique hypotheses, exact observed targets, native support object membership and obligation lanes; structural validation is delegated. Preserve and reuse this boundary instead of deriving support strength.",
    )
    unit(
        "accepted-algebra",
        BASE + "obligation.py",
        [[41, 95]],
        "WitnessSet requires nonempty distinct hashable targets. LocalizationObligation retains caller-declared ANY alternatives of ALL members, requirement, applicability and satisfaction criterion; equivalent alternatives are forbidden.",
    )
    unit(
        "accepted-evidence",
        BASE + "assessment.py",
        [[37, 62]],
        "LocalizationEvidenceReference retains hashable caller/native identity with repository and snapshot. SupportedWitness has a hashable exact target and nonempty evidence references, not a score or candidate support count.",
    )
    unit(
        "assessment-value",
        BASE + "assessment.py",
        [[18, 35], [80, 114]],
        "Assessment states and applicability are separate. LocalizationAssessment binds one obligation to repository/snapshot, aggregate distinct supported targets and explicit deferred/explanation structure.",
    )
    unit(
        "readiness-contract",
        BASE + "readiness.py",
        [[107, 387]],
        "Exact assessment identity coverage and evidence frames gate readiness. RESOLVED requires a completely supported declared alternative; OPEN cannot carry a satisfied alternative. Applicability evidence is explicit; stale/foreign/inconsistent frames are invalid. Candidate state alone never enters readiness.",
    )
    unit(
        "task-frame",
        BASE + "task.py",
        [[33, 64]],
        "Interpretation is an immutable full value of task identity, provenance, anchors and obligations; foreign, duplicate and unknown anchor references are rejected. Comparing only task key is weaker than retaining the interpreted frame.",
    )
    unit(
        "generation-view",
        BASE + "generation/contract.py",
        [[131, 224]],
        "Attempts retain recipes, member outcomes, native targets/supports and an optional hypothesis; WitnessGenerationView retains plan, attempts and validated association. Its generated property is unresolved association hypotheses; failures are not partial accepted witnesses.",
    )
    unit(
        "grounding-account",
        BASE + "grounding/contract.py",
        [[128, 214]],
        "Grounding account retains task/anchor/repository/snapshot request provenance, native candidates and evidence, bounded outcome and module universe. Unique resolved cardinality means a bounded referent, not semantic witness acceptance.",
    )
    unit(
        "grounding-view",
        BASE + "grounding/view.py",
        [[32, 134]],
        "AnchorGroundingView retains task/snapshot/all accounts, anchor and referent queries, unresolved/unrequested anchors and deterministic construction through native resolver; it does not assign obligation satisfaction.",
    )
    unit(
        "exports-kernel",
        BASE + "__init__.py",
        [[4, 72]],
        "Kernel facade explicitly imports public assessment, obligation, identity, task and readiness APIs and declares __all__; candidate subpackages are not flattened into this facade.",
    )
    unit(
        "exports-association",
        BASE + "association/__init__.py",
        [[4, 28]],
        "Neighboring association package publishes responsibility-owned candidate types, structural supports and builder through explicit imports and __all__.",
    )
    unit(
        "exports-generation",
        BASE + "generation/__init__.py",
        [[4, 28]],
        "Neighboring generation package publishes responsibility-owned contract types and operation through explicit imports and __all__.",
    )
    unit(
        "test-association",
        "tests/context/localization/association/test_hypothesis.py",
        [[7, 44], [138, 280]],
        "Pytest assertions, dataclasses.replace counterexamples, parameterized foreign/stale inputs, native object retention, complementarity/competition, deterministic ordering and unchanged readiness establish neighboring test conventions.",
    )
    unit(
        "test-generation",
        "tests/context/localization/generation/test_generation.py",
        [[277, 428], [583, 651]],
        "An independently sufficient neighboring example of asserts, replace and raises covers complementary/competing shapes, supplemental native evidence, unchanged readiness, forgery and foreign/stale frames. Fixture helpers need not be copied to author new tests.",
    )
    unit(
        "docs-authority",
        "docs/documentation_map.md",
        [[3, 101]],
        "Map assigns architecture, taxonomy, package behavior, roadmap sequencing, backlog pressure and ledger history distinct authority. Localization package overview owns association, grounding and generation contracts.",
    )
    unit(
        "docs-architecture",
        "docs/architecture.md",
        [[841, 927]],
        "Current accepted Localization ownership and candidate/accepted/readiness boundaries and present unimplemented resolution claims that the new production capability must update.",
    )
    unit(
        "docs-package",
        BASE + "docs/overview.md",
        [[129, 160], [162, 321]],
        "Detailed current kernel, grounding, association and generation behavior; explicitly future resolution and no accepted witnesses/readiness from candidate evidence. These behavior claims require a coherent resolution-seam update.",
    )
    unit(
        "docs-roadmap",
        "docs/roadmap.md",
        [[42, 54]],
        "Current development sequencing says association/generation are implemented and resolution remains separate. Updating development state must distinguish explicit recording from automatic policy or empirical effectiveness.",
    )
    unit(
        "validation-contract",
        "docs/development/validation.md",
        [[3, 44]],
        "Canonical protected development command excludes experiments before collection and retains configured strict/branch/100% production gate; separate Ruff, format, mypy and both Git diff gates. Confirmation requires separate authorization.",
    )

    decisions = []

    def obligation(key, alternatives, reason, helpful=()):
        required = sorted({member for alt in alternatives for member in alt})
        decisions.append(
            {
                "identity": key,
                "applicability": "APPLICABLE",
                "applicability_rationale": (
                    "Explicit kernel imports/__all__ and an adjacent responsibility-owned facade affirm actual public API conventions, rather than mere initializer existence."
                    if key == "package-integration"
                    else "Frozen task explicitly requires this behavior; frozen contracts establish its implemented integration boundary."
                ),
                "required_units": [
                    {
                        "unit_identity": member,
                        "classification": "REQUIRED",
                        "rationale": reason
                        + " Exact supplied information: "
                        + units[member]["information"],
                        "inferability": "INFERABLE_AT_START",
                        "inferability_rationale": "Task names this boundary; deterministic static inspection of the frozen package or governing document establishes the need before implementation.",
                        "inherent_discovery_prerequisites": None,
                        "manual_required_review": {
                            "necessity": "Removing this member leaves a named existing contract or governing convention unestablished within this alternative; an implementation based only on names could violate it.",
                            "smaller_unit_review": units[member]["precision_rationale"],
                            "relationship": "ALL complementary members in each alternative; ANY complete alternative suffices. Repeated units across alternatives are shared prerequisites, not votes.",
                            "blind_evidence_only": True,
                        },
                    }
                    for member in required
                ],
                "acceptable_witness_alternatives": [
                    {"identity": f"{key}-alternative-{i}", "all": list(alt)}
                    for i, alt in enumerate(alternatives, 1)
                ],
                "alternative_rationale": (
                    "Both neighboring facades independently establish explicit subpackage exposure; the parent kernel facade is complementary and establishes the existing boundary."
                    if key == "package-integration"
                    else "Either neighboring test example establishes rigorous local test conventions; candidate validation and readiness source contracts jointly supply exact expected behavior for new disposition/promotion cases. Existing kernel tests are corroboration."
                    if key == "tests"
                    else "One defensible complete alternative: the members provide different contracts and cannot substitute for one another. No extra alternative is claimed merely from overlapping terminology."
                ),
                "helpful_resources": [
                    {
                        "resource_identity": frame[path]["identity"],
                        "classification": "HELPFUL_ONLY",
                        "rationale": why,
                    }
                    for path, why in helpful
                ],
                "unresolved": [],
                "default_resource_classification": "UNNECESSARY",
                "default_rationale": "Within this obligation and the specified complete alternatives, all remaining eligible resources supply neither a missing contract nor material task-specific orientation. Excluded search/ranking/policy mechanisms and unrelated domains are not needed; redundant detail is not automatically helpful.",
            }
        )

    overview = (
        BASE + "docs/overview.md",
        "Readable corroboration of the same implemented boundary; selected source already establishes the precise contract.",
    )
    structural = (
        BASE + "association/structural.py",
        "Explains delegated native replay in detail; callers can reuse the association validator and retain supports without reimplementing it.",
    )
    obligation(
        "hypothesis-records",
        [
            [
                "candidate-key",
                "candidate-member",
                "candidate-shape",
                "candidate-validation",
            ]
        ],
        "Explicit hypothesis/member recording must bind the correct existing identities, retain supports and validate the unresolved view. The member schema and frame builder are complementary, not alternative descriptions.",
        [overview],
    )
    obligation(
        "member-complementarity",
        [["candidate-shape", "accepted-algebra"]],
        "Candidate member grouping and accepted ALL/ANY target grouping must both be known to avoid converting a partial complementary hypothesis into an accepted alternative.",
        [
            overview,
            (
                "tests/context/localization/test_kernel.py",
                "Concrete all-members/any-alternative examples corroborate the two source contracts.",
            ),
        ],
    )
    obligation(
        "generated-integration",
        [["candidate-shape", "generation-view", "grounding-account", "grounding-view"]],
        "The integration requires the validated unresolved association, the generation attempts/plan linkage and the grounding view/account provenance; one view cannot establish another view's retained boundary.",
        [
            overview,
            (
                BASE + "generation/generate.py",
                "Shows how the existing generator constructs the association and attaches supplemental supports; no generator redesign is needed.",
            ),
            structural,
        ],
    )
    obligation(
        "accepted-promotion",
        [
            [
                "candidate-member",
                "candidate-shape",
                "candidate-validation",
                "accepted-algebra",
                "accepted-evidence",
            ]
        ],
        "Promotion must know every candidate member, validate its retained native frame, map a complete alternative to distinct accepted targets, and require explicit snapshot-qualified support for each. Existing candidate support positivity does not establish acceptance.",
        [
            overview,
            (
                BASE + "assessment.py",
                "The remaining assessment structure is governed separately by assessment-readiness; not an additional promotion target contract.",
            ),
        ],
    )
    # Remove a whole-resource helpful label where finer required units already govern it.
    decisions[-1]["helpful_resources"] = decisions[-1]["helpful_resources"][:1]
    obligation(
        "assessment-readiness",
        [["assessment-value", "accepted-algebra", "readiness-contract"]],
        "Constructing an assessment correctly requires its disposition structure and declared witness algebra, while readiness defines exact coverage and rejection of premature/stale satisfaction. An accepted support value alone cannot establish readiness.",
        [
            overview,
            (
                "tests/context/localization/test_kernel.py",
                "Accepted/incomplete/conditional examples corroborate readiness semantics without being the sole specification.",
            ),
        ],
    )
    obligation(
        "provenance-frame",
        [["candidate-validation", "accepted-evidence", "task-frame"]],
        "Native membership validation, snapshot-qualified accepted evidence and the full interpreted task frame are complementary; preserving only resource paths or task keys would permit stale or foreign data.",
        [
            structural,
            (
                BASE + "identity.py",
                "Additional anchor/query/provenance declarations orient implementation; task and candidate identities already establish required scoping.",
            ),
            (
                "src/devtools/context/repository/resource.py",
                "Explains native addressed content occurrences already compared by association validation.",
            ),
            (
                "src/devtools/context/repository/snapshot.py",
                "Details the existing exact resource lookup already used by association validation.",
            ),
            (
                BASE + "grounding/resolve.py",
                "Explains delegated grounding frame checks; required recording can reuse the existing validation boundary.",
            ),
        ],
    )
    obligation(
        "package-integration",
        [
            ["exports-kernel", "exports-association"],
            ["exports-kernel", "exports-generation"],
        ],
        "Coherent public exposure must respect the kernel facade and the existing subpackage import/__all__ convention. Either inspected neighboring facade demonstrates that convention independently.",
        [
            (
                BASE + "grounding/__init__.py",
                "Another analogous facade; adds confidence but no distinct required convention.",
            )
        ],
    )
    obligation(
        "tests",
        [
            ["candidate-validation", "readiness-contract", "test-association"],
            ["candidate-validation", "readiness-contract", "test-generation"],
        ],
        "Rigorous new tests need the exact native/frame rejection and readiness expectations plus one sufficient neighboring test convention example. Test names alone or generic pytest familiarity do not establish these repository-specific boundaries.",
        [
            (
                "tests/context/localization/test_kernel.py",
                "Additional readiness assertions corroborate expected invalid/complete dispositions already specified by required source.",
            ),
            (
                "tests/context/localization/grounding/test_grounding.py",
                "Additional bounded grounding negative cases help confidence; no grounding resolver change is required.",
            ),
            (
                "tests/context/localization/test_lexical.py",
                "Existing fixture helpers can reduce setup work but new tests may author bounded native fixtures independently.",
            ),
        ],
    )
    obligation(
        "documentation",
        [["docs-authority", "docs-architecture", "docs-package", "docs-roadmap"]],
        "Task requires authoritative architecture and development documentation: authority map identifies distinct owners, central architecture and package overview hold current behavior claims, and roadmap owns development sequencing. None alone supplies all four responsibilities.",
        [
            (
                "docs/architecture/taxonomy.md",
                "Semantic vocabulary corroborates boundaries already explicit in current architecture and package contract; no terminology migration is requested.",
            ),
            (
                "docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md",
                "Accepted rationale supports review, but current architecture/map/package already establish behavior and authority.",
            ),
            (
                "docs/backlog/epics/B-0002-coding-context-substrate.md",
                "Records unresolved pressure and earlier increments; does not require closing or rewriting the epic for a bounded recording capability.",
            ),
            (
                "AGENTS.md",
                "Operating update rules corroborate authority map; task authorizes the bounded documentation update.",
            ),
        ],
    )
    obligation(
        "validation",
        [["validation-contract"]],
        "The canonical document explicitly gives command, protected profile and every static gate. Executing validation or inspecting its implementation is not needed to KNOW this contract.",
        [
            (
                "pyproject.toml",
                "Exact strict pytest/100% branch configuration and mypy/Ruff settings corroborate the canonical documented gates.",
            ),
            (
                "scripts/validate_development.py",
                "Implementation corroborates protected selection; document already states command and exclusion.",
            ),
            (
                "AGENTS.md",
                "Repeats the command and points to canonical development validation documentation.",
            ),
        ],
    )
    return units, decisions

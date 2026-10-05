# Copyright (c) 2026
# ruff: noqa: INP001, COM812, E501
"""Case 0008 manually adjudicated information units; no acquisition machinery."""

from __future__ import annotations

from stage_c import load_packet, serialize, validate

LOCAL = "src/devtools/context/localization/"
ADR = (
    "docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md"
)

# Each selection is a manual semantic judgment, not a search result.
# Inclusive line spans refer exclusively to the archived text.
SELECTIONS = [
    (
        "states",
        LOCAL + "assessment.py",
        [(18, 34)],
        "Applicability and disposition are separate; OPEN, ABSTAINED, deferred, resolved and non-applicable are distinct.",
    ),
    (
        "deferred",
        LOCAL + "assessment.py",
        [(65, 77)],
        "DeferredDiscovery requires a named observation and reason; acceptance for handoff defaults false.",
    ),
    (
        "assessment",
        LOCAL + "assessment.py",
        [(80, 114)],
        "Assessment carries obligation, repository/snapshot, applicability evidence, accepted supports and disposition-specific deferred data.",
    ),
    (
        "obligation",
        LOCAL + "obligation.py",
        [(62, 95)],
        "Obligation predicate, task-local anchors, provenance, requirement, satisfaction criterion, alternatives and conditional applicability are caller authored.",
    ),
    (
        "evidence",
        LOCAL + "assessment.py",
        [(37, 47)],
        "Evidence references retain caller/native hashable identity plus repository and snapshot qualification.",
    ),
    (
        "positive-support",
        LOCAL + "assessment.py",
        [(50, 62)],
        "SupportedWitness needs a hashable target and nonempty positive evidence; a request cannot supply that support.",
    ),
    (
        "witness-set",
        LOCAL + "obligation.py",
        [(41, 59)],
        "WitnessSet contains distinct hashable targets, all jointly needed.",
    ),
    (
        "condition-check",
        LOCAL + "readiness.py",
        [(294, 321), (340, 361)],
        "Conditional applicability needs same-frame affirmative evidence; non-applicability forbids accepted supports; unresolved states cannot contain a complete accepted alternative.",
    ),
    (
        "alternative-check",
        LOCAL + "readiness.py",
        [(324, 337)],
        "Any one entirely supported declared alternative satisfies; partial members do not.",
    ),
    (
        "handoff-check",
        LOCAL + "readiness.py",
        [(253, 291)],
        "Open/abstained/unaccepted deferred mandatory obligations block; accepted deferral is conditional rather than ready.",
    ),
    (
        "frame-check",
        LOCAL + "readiness.py",
        [(107, 155), (364, 387)],
        "Exact assessment coverage and all evidence frames are checked; missing, duplicate, foreign or stale inputs invalidate handoff.",
    ),
    (
        "task-identities",
        LOCAL + "identity.py",
        [(13, 51), (82, 99)],
        "Task, anchor and obligation identities are stable caller keys scoped to task; task provenance refers to a hashable source with optional span/explanation.",
    ),
    (
        "task-frame",
        LOCAL + "task.py",
        [(33, 64)],
        "Interpretation holds task provenance, anchors and obligations; foreign/duplicate identities and unknown anchor references are rejected.",
    ),
    (
        "candidate-identities",
        LOCAL + "association/hypothesis.py",
        [(44, 120)],
        "Caller alternatives and generated family/child identities differ; child identity retains obligation, member, repository, snapshot and exact target with collision-safe stable encoding.",
    ),
    (
        "candidate-members",
        LOCAL + "association/hypothesis.py",
        [(140, 229)],
        "Candidate members retain exact occurrence, reason and individual native support; all members complement inside an unresolved hypothesis with canonical order.",
    ),
    (
        "candidate-view",
        LOCAL + "association/hypothesis.py",
        [(232, 265), (322, 359)],
        "View retains task, snapshot, hypotheses and native input views; unknown/duplicate hypotheses, foreign children and mismatched targets are rejected.",
    ),
    (
        "generation-lineage",
        LOCAL + "generation/contract.py",
        [(73, 81), (107, 114), (144, 155), (314, 375), (392, 395), (419, 439)],
        "Generation plan, member and family provenance, attempts, children and association view retain failed and successful lineage; generated candidates remain unresolved.",
    ),
    (
        "grounding-account",
        LOCAL + "grounding/contract.py",
        [(132, 147), (161, 218)],
        "Grounding retains task/anchor/frame/provenance, exact native referent and supporting observation; bounded outcomes do not assert witness acceptance.",
    ),
    (
        "grounding-view",
        LOCAL + "grounding/view.py",
        [(32, 48), (69, 102)],
        "Task/snapshot view retains independent grounding accounts, unresolved or unrequested anchors and native referent-to-anchor links.",
    ),
    (
        "grounding-replay",
        LOCAL + "association/structural.py",
        [(72, 98)],
        "Canonical structural-support validation replays the exact retained grounding and rejects forged/stale support; higher layers can reuse it without duplicating resolvers.",
    ),
    (
        "repository-id",
        "src/devtools/context/repository/identity.py",
        [(11, 29)],
        "Logical RepositoryId is nominal and independent of location/state; parse/string conventions preserve the native identity.",
    ),
    (
        "snapshot",
        "src/devtools/context/repository/snapshot.py",
        [(19, 61)],
        "Snapshot identity and observed occurrence collection are explicit; exact resource lookup uses retained state rather than current filesystem.",
    ),
    (
        "occurrence",
        "src/devtools/context/repository/resource.py",
        [(49, 72)],
        "Native occurrence comprises address and content identity, distinct from content alone, and retains observed text/encoding/size.",
    ),
    (
        "purpose-taxonomy",
        "docs/architecture/taxonomy.md",
        [(594, 605)],
        "Information purpose and acceptable-information constraints differ from query/strategy, budget and satisfaction; no standalone need identity is mandatory.",
    ),
    (
        "purpose-adr",
        "docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md",
        [(114, 150)],
        "Equivalent purpose/constraint boundary: strongly typed clues and provenance do not select a retriever; mechanism choice belongs to planning.",
    ),
    (
        "request-direction",
        ADR,
        [(82, 88), (213, 246)],
        "Open obligations retain missing observations, prerequisites, limits, stop reasons and proposed acquisitions; partial acquisition cannot prove absence, satisfaction or disclosure completeness.",
    ),
    (
        "ownership-adr",
        ADR,
        [(48, 64), (72, 80)],
        "Localization owns requests, native owners retain identities, authorized caller owns execution/retry/escalation; no reverse dependency on Context Planning, Agent loops or experiments.",
    ),
    (
        "ownership-current",
        "docs/architecture.md",
        [(901, 908), (919, 926)],
        "Current ownership independently states purpose/query separation, scoped handoff and caller-owned further acquisition/retries; Context owns representation.",
    ),
    (
        "facade",
        LOCAL + "__init__.py",
        [(1, 72)],
        "Explicit imports and __all__ define the public Localization kernel facade; integrating a new supported assessment capability requires respecting this exposure convention.",
    ),
    (
        "doc-authority",
        "docs/documentation_map.md",
        [(3, 34), (75, 103)],
        "Central architecture, taxonomy, package docs, source/tests, roadmap/backlog and historical ledger have different authorities; Localization contract navigation is explicit.",
    ),
    (
        "architecture-claims",
        "docs/architecture.md",
        [(841, 926)],
        "Current system ownership and implementation/future claims around Localization must reflect the new capability.",
    ),
    (
        "taxonomy-claims",
        "docs/architecture/taxonomy.md",
        [(641, 690), (708, 714)],
        "Semantic definitions of obligations, candidate/accepted distinctions and readiness constrain terminology updates.",
    ),
    (
        "package-claims",
        LOCAL + "docs/overview.md",
        [(9, 31), (129, 160), (211, 275)],
        "Detailed implemented package behavior and integration claims must describe the new frontier/request seam coherently.",
    ),
    (
        "development-claims",
        "docs/roadmap.md",
        [(3, 9), (42, 74)],
        "Roadmap owns selected development sequencing and current capability status, not API truth or new authorization.",
    ),
    (
        "validation-profile",
        "docs/development/validation.md",
        [(3, 44)],
        "Protected test command, experiment exclusion before collection, 100% branch coverage, Ruff/format/mypy and both diff checks; confirmation needs separate authorization.",
    ),
]

# Alternatives contain ALL members; different alternatives are ANY-of.
REQUIRED = {
    "frontier-semantics": [
        ["states", "deferred", "assessment", "obligation", "request-direction"]
    ],
    "assessment-applicability": [
        ["states", "assessment", "obligation", "condition-check"]
    ],
    "candidate-integration": [
        [
            "candidate-identities",
            "candidate-members",
            "candidate-view",
            "generation-lineage",
        ]
    ],
    "witness-boundary": [
        [
            "positive-support",
            "witness-set",
            "alternative-check",
            "condition-check",
            "candidate-members",
        ]
    ],
    "acquisition-contract": [
        ["purpose-taxonomy", "obligation", "request-direction", "ownership-adr"],
        ["purpose-adr", "obligation", "request-direction", "ownership-adr"],
    ],
    "grounding-provenance": [
        [
            "grounding-account",
            "grounding-view",
            "grounding-replay",
            "evidence",
            "occurrence",
        ]
    ],
    "frame-identity": [
        [
            "task-identities",
            "task-frame",
            "evidence",
            "repository-id",
            "snapshot",
            "occurrence",
            "candidate-identities",
            "candidate-view",
            "frame-check",
        ]
    ],
    "readiness-integration": [
        [
            "states",
            "deferred",
            "handoff-check",
            "condition-check",
            "alternative-check",
            "frame-check",
        ]
    ],
    "orchestration-boundary": [["ownership-adr"], ["ownership-current"]],
    "package-api": [["facade", "ownership-adr"]],
    "tests": [
        [
            "states",
            "assessment",
            "deferred",
            "condition-check",
            "alternative-check",
            "handoff-check",
            "frame-check",
            "task-frame",
            "candidate-identities",
            "candidate-members",
            "candidate-view",
            "generation-lineage",
            "grounding-account",
            "grounding-replay",
            "evidence",
            "snapshot",
            "request-direction",
            "ownership-adr",
        ]
    ],
    "documentation": [
        [
            "doc-authority",
            "architecture-claims",
            "taxonomy-claims",
            "package-claims",
            "development-claims",
        ]
    ],
    "validation": [["validation-profile"]],
}

REASONS = {
    "frontier-semantics": "Without the existing predicate, incomplete states, deferred observation and accepted architectural frontier constraints, a new missing-evidence representation could assert absence or collapse deferral into resolution. These contracts jointly constrain semantics; no future implementation is a witness.",
    "assessment-applicability": "The assessment fields and readiness's actual consistency checks jointly define the implemented applicability distinction. Enums alone do not establish the affirmative evidence condition for NOT_APPLICABLE or prevent unresolved states from claiming full support.",
    "candidate-integration": "Exact candidate and generated-child types plus retained generation lineage are needed to link unresolved hypotheses without resolving, eliminating or flattening family/child provenance. Native mechanism implementation internals can be reused without inspection.",
    "witness-boundary": "Positive support, conjunctive targets, any-of satisfaction, disposition consistency and the unresolved candidate type are complementary. Omitting any loses a distinct boundary explicitly required by the task.",
    "acquisition-contract": "Purpose constraints, obligation predicate and the accepted request/ownership direction are necessary to design a coherent new contract. The two purpose passages independently establish the same requirement and genuinely compete. Existing Retrieval execution and generation quota implementations are useful examples, not necessary request-design contracts; the exact task supplies the mandatory explicit-bounds requirement.",
    "grounding-provenance": "Grounding account/view, native occurrence and qualified evidence contract are needed to retain exact links. The existing replay entry point establishes integrity without requiring each Python resolver implementation or reconstructing native proofs.",
    "frame-identity": "Native identity representations, task membership, candidate links, retained snapshot lookup and assessment coverage establish deterministic frame validation. Generic UUID generation, snapshot acquisition and corpus construction are not required to reference this existing frame.",
    "readiness-integration": "The implemented consistency, any-of coverage, mandatory state and exact-frame rules jointly determine whether a frontier blocks or permits only accepted conditional handoff. A new request supplies no accepted support.",
    "orchestration-boundary": "Either accepted ADR ownership or the current architecture's ownership statement independently establishes the required non-authorizing representation/execution/Context boundary. No future controller API is needed.",
    "package-api": "APPLICABLE: this is a production reusable assessment/request capability integrating publicly exported kernel contracts. The explicit facade and accepted dependency direction together constrain exposure. Applicability follows the task's supported integration plus explicit exports, not merely an initializer's existence.",
    "tests": "Behavioral contract spans are necessary to know the test oracle for positive/negative states, candidate lineage, exact grounding/evidence/frame validation, deterministic replay, readiness and request nonclaims. Existing tests are substitutable implementation examples, not indispensable correctness information. The frozen task supplies new request/bounds test requirements; no nonexistent frontier test is required.",
    "documentation": "Authority/navigation and current claims in system architecture, taxonomy, package documentation and roadmap jointly identify what must be reconciled. Historical ledger is excluded from the packet and is a limitation rather than an invented witness. Updating accepted decision history is not required merely because a new capability implements it.",
    "validation": "The authoritative development validation section completely states how to know protected command, coverage/static gates and confirmation exclusion. Config and runner are independent corroboration, not needed in addition to the complete documented contract; future outcomes are not repository witnesses.",
}


def build() -> dict:  # noqa: C901, PLR0912
    """Construct gold from manual decisions and the two verified blind inputs."""
    manifest, archive = load_packet()
    resources = {item["address"]: item for item in archive["resources"]}
    units = []
    for identity, address, spans, information in SELECTIONS:
        resource = resources[address]
        lines = resource["content"].splitlines()
        units.append(
            {
                "identity": identity,
                "resource": resource["occurrence_identity"],
                "spans": [
                    {
                        "start_line": start,
                        "end_line": end,
                        "excerpt": "\n".join(lines[start - 1 : end]),
                    }
                    for start, end in spans
                ],
                "information": information,
            }
        )
    by_unit = {u["identity"]: u for u in units}
    obligations = []
    for frozen in manifest["obligations"]:
        identity = frozen["identity"]
        alternatives = REQUIRED[identity]
        selected = sorted({u for alternative in alternatives for u in alternative})
        obligations.append(
            {
                "frozen_obligation": frozen,
                "applicability": "APPLICABLE",
                "applicability_rationale": REASONS[identity],
                "unit_judgments": [
                    {
                        "unit": u,
                        "judgment": "REQUIRED",
                        "rationale": by_unit[u]["information"]
                        + " "
                        + REASONS[identity],
                        "inferability": "INFERABLE_AT_START",
                        "discovery": None,
                        "manual_review": {
                            "obligation": identity,
                            "information": by_unit[u]["information"],
                            "necessity": REASONS[identity],
                            "granularity": "Only the selected archived contract/claim spans are needed; surrounding implementation is not required.",
                            "relationship": "ALL inside each alternative; ANY between alternatives. Competition exists only for the explicitly equivalent purpose or ownership statements.",
                            "task_start": "Existing frozen static contract; locating it needs no later observation.",
                            "blind_basis": "Only verified manifest and archived resource text.",
                        },
                    }
                    for u in selected
                ],
                "acceptable_alternatives": [
                    {
                        "identity": f"{identity}-{i + 1}",
                        "all_units": a,
                        "rationale": REASONS[identity],
                    }
                    for i, a in enumerate(alternatives)
                ],
            }
        )
    # Helpful judgments are explicit, obligation relative, and never witnesses.
    helpful = {o["identity"]: {} for o in manifest["obligations"]}

    def help_for(obligation: str, address: str, rationale: str) -> None:
        helpful[obligation][address] = rationale

    for obligation in helpful:
        if obligation not in {"documentation", "validation"}:
            help_for(
                obligation,
                LOCAL + "docs/overview.md",
                "Package prose orients the implementation and corroborates source contracts; it does not replace the exact required API spans.",
            )
        help_for(
            obligation,
            "AGENTS.md",
            "Operating guide helps perform bounded development and avoid architectural expansion; the exact task and required authoritative contracts already constrain correctness.",
        )
    for obligation in [
        "frontier-semantics",
        "assessment-applicability",
        "witness-boundary",
        "readiness-integration",
        "tests",
    ]:
        help_for(
            obligation,
            "tests/context/localization/test_kernel.py",
            "Existing positive/negative fixtures corroborate the contracts; competent tests can be authored from the source oracle without copying these examples.",
        )
    for obligation in ["candidate-integration", "frame-identity", "tests"]:
        for address in [
            "tests/context/localization/association/test_hypothesis.py",
            "tests/context/localization/generation/test_branching.py",
        ]:
            help_for(
                obligation,
                address,
                "Candidate/frame/lineage examples improve confidence and fixture design; source contracts already specify the necessary behavior.",
            )
    for obligation in ["grounding-provenance", "frame-identity", "tests"]:
        help_for(
            obligation,
            "tests/context/localization/grounding/test_grounding.py",
            "Grounding identity and stale-frame examples corroborate required contracts; no unique test-only oracle is needed.",
        )
    for obligation in ["candidate-integration", "acquisition-contract", "tests"]:
        help_for(
            obligation,
            LOCAL + "generation/contract.py",
            "Existing independent quotas and incomplete-enumeration diagnostics are useful design examples; new acquisition bounds do not have to duplicate generation quotas.",
        )
    for obligation in ["candidate-integration", "grounding-provenance", "tests"]:
        help_for(
            obligation,
            LOCAL + "generation/generate.py",
            "Existing composition demonstrates validation reuse; the new representation needs contracts rather than generation execution internals.",
        )
    for obligation in ["grounding-provenance", "tests"]:
        help_for(
            obligation,
            LOCAL + "grounding/resolve.py",
            "Resolver internals corroborate staleness and native frame checking; canonical retained-account replay can be reused without duplicating these internals.",
        )
    for obligation in [
        "acquisition-contract",
        "orchestration-boundary",
        "package-api",
        "documentation",
    ]:
        help_for(
            obligation,
            "src/devtools/context/planning/docs/overview.md",
            "Neighboring representation ownership provides useful orientation; accepted Localization ownership already establishes the necessary boundary.",
        )
    for obligation in [
        "acquisition-contract",
        "orchestration-boundary",
        "documentation",
    ]:
        help_for(
            obligation,
            ADR,
            "Decision rationale corroborates ownership and incomplete handoff; redundant passages are not additional mandatory witnesses.",
        )
    for obligation in ["documentation", "package-api"]:
        help_for(
            obligation,
            "docs/backlog/epics/B-0002-coding-context-substrate.md",
            "Unresolved pressure and promotion context help scope work; they do not authorize or specify this capability.",
        )
    for address in ["pyproject.toml", "scripts/validate_development.py"]:
        help_for(
            "validation",
            address,
            "Config/runner corroborate the complete authoritative validation instructions; neither adds necessary knowledge to that section.",
        )
    help_for(
        "tests",
        "pyproject.toml",
        "Pytest and strict/static configuration guide execution; semantic test correctness is specified by required contracts and the exact task.",
    )
    cells = []
    for resource in archive["resources"]:
        for obligation in obligations:
            identity = obligation["frozen_obligation"]["identity"]
            required_units = [
                j["unit"]
                for j in obligation["unit_judgments"]
                if by_unit[j["unit"]]["resource"] == resource["occurrence_identity"]
            ]
            if required_units:
                label = "REQUIRED"
                reason = "Contains the exact REQUIRED units listed; no whole-file necessity is implied."
            elif resource["address"] in helpful[identity]:
                label = "HELPFUL_ONLY"
                reason = helpful[identity][resource["address"]]
            else:
                label = "UNNECESSARY"
                reason = (
                    "No additional necessary or materially useful information for this obligation: "
                    "outside its representation/integration/validation responsibility, or redundant general "
                    "mechanism/background. Existing execution, resolution and unrelated domain internals "
                    "are not required by this bounded task. This is obligation-relative, not global irrelevance."
                )
            cells.append(
                {
                    "resource": resource["occurrence_identity"],
                    "obligation": identity,
                    "judgment": label,
                    "required_units": required_units,
                    "rationale": reason,
                }
            )
    gold = {
        "schema": "case-0008-stage-c-judgments-v1",
        "case_identity": manifest["case_identity"],
        "task_identity": manifest["task_identity"],
        "exact_task": manifest["task"],
        "repository_id": manifest["repository_id"],
        "snapshot_id": manifest["snapshot_id"],
        "corpus_id": manifest["corpus_id"],
        "blind_digests": {
            "blind_manifest.json": "d1096ba811f050a74a0232caa34245bc6de7f263494155e97c3e0ebbf147b6e0",
            "blind_resources.json.gz": manifest["blind_resources"]["sha256"],
        },
        "method": {
            "evidence_universe": "Two verified blind inputs only; current task-relevant filesystem source was never read.",
            "inspection": "Enumerated all archived identities; exact whole-archive textual search and manual selected source/doc/test span inspection. No task-relative retrieval or graph/projection APIs.",
            "necessity": "Counterfactual correctness with all complementary witnesses available; matching vocabulary, modification likelihood and adjacency do not imply necessity.",
            "resource_rule": "One explicit cell for each archive occurrence and frozen obligation. REQUIRED iff it contains a REQUIRED unit for that obligation; HELPFUL_ONLY for explicit corroboration/orientation; otherwise UNNECESSARY under the bounded task.",
            "alternatives": "All members within each alternative; any complete alternative. Only equivalent purpose and execution-ownership passages compete. No search/operator structure influences the gold.",
            "inferability": "All required information is frozen static text. No inherent discovery was necessary to determine repository-information needs.",
        },
        "obligations": obligations,
        "information_units": units,
        "resource_judgments": cells,
        "task_gaps": [],
        "task_gap_review": "no obvious mandatory task-interpretation gap found; exclusions, explicit bounded requests, identity/replay, integrations, tests/docs and protected validation are represented by the frozen frame",
        "packet_limitations": [
            "Historical implementation ledger and research resources referenced by navigation are outside the 523-resource frame; their contents cannot be adjudicated or required as available witnesses.",
            "No future frontier/request implementation or future validation outcomes exist in the evidence universe; exact task and existing constraints supply the new representation requirements.",
            "Archived ADR-0005 status is historical accepted direction; central architecture has a narrower generation summary than current taxonomy/source. Current source defines implemented behavior; documentation drift is recorded, not silently used as a narrower API specification.",
            "Request design has no canonical algorithm-independent production request type in the inspected packet; quota examples do not fix future representation or execution policy.",
        ],
        "blindness_attestation": {
            "blind_manifest_accessed": True,
            "blind_resources_accessed": True,
            "other_preexisting_case_artifacts_accessed": False,
            "lexical_experiment_accessed": False,
            "role_experiment_accessed": False,
            "grounding_experiment_accessed": False,
            "generation_experiment_accessed": False,
            "reference_experiment_accessed": False,
            "import_experiment_accessed": False,
            "recovery_history_accessed": False,
            "current_task_relevant_source_accessed": False,
            "stage_d_performed": False,
            "effectiveness_analysis_performed": False,
            "confirmation_accessed": False,
        },
    }
    validate(gold, manifest, archive)
    return gold


if __name__ == "__main__":
    print(serialize(build()).decode(), end="")  # noqa: T201

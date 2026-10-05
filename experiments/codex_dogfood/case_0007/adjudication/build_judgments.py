# Copyright (c) 2026
# ruff: noqa: INP001, E501, T201
"""Encode manually adjudicated Case 0007 gold, without a retrieval mechanism."""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

from freeze_judgments import (
    ARCHIVE_SHA,
    HERE,
    MANIFEST_SHA,
    canonical,
    packet,
    sha,
    statistics,
    validate,
)

# Resource ordinals refer only to the pinned blind JSON array. They are not
# evidence order, priority, or experimental positions. Emitted units use exact
# native resource identities; ordinals are absent from adjudicated gold.
# Each entry was manually read and reviewed before inclusion.
UNIT_SPECS = {
    "function-subject": (
        129,
        [(146, 201)],
        "Native function subject and declaration value, ordinal/definition/dependency identity, exact source support, sync/async kind.",
        "Name or range alone cannot preserve existing function identity; these two adjacent value contracts are the minimum interface, excluding retrieval, aggregation and containment.",
    ),
    "class-subject": (
        123,
        [(88, 109), (147, 181)],
        "Native direct class subject and declaration knowledge, structural ordinal/dependency identity and source/base-syntax support.",
        "Class identity is separate from functions; direct class values suffice. Method subjects, base resolution and class containment are not needed for this export increment.",
    ),
    "source-selection": (
        150,
        [(29, 72), (80, 98)],
        "Canonical kind/name selection of all direct native class/function source declarations; decorators and rebinding do not erase source facts.",
        "This public selector and result contract suffice; no parallel parser or binding-policy change is needed. Its snapshot guard is judged separately.",
    ),
    "import-declaration": (
        139,
        [(23, 68), (99, 119)],
        "Native import occurrence/declaration/analysis vocabulary and direct-body alias extraction: module, relative level, imported name and local alias remain distinct.",
        "Value fields alone do not show which spelling an Import versus ImportFrom retains. The small extraction loop complements those fields; error/hash helpers are unnecessary.",
    ),
    "import-resolution": (
        142,
        [(28, 183)],
        "Qualified module-only import resolution, explicit universe, relative package interpretation, duplicate/missing targets, retained source and outcome.",
        "The resolver contract and relative-source rules jointly constrain facade resolution. Exclude digest mechanics; do not require module relation derivation.",
    ),
    "facade-resolution": (
        140,
        [(44, 146), (149, 345), (355, 425)],
        "Existing one-facade imported-function result/provenance and alias rules, competing/nested/star guards, zero/multiple candidates, no recursion and no export analysis.",
        "The value and bounded resolution rules are complementary; keeping just the positive branch hides unsupported forms. Snapshot validation and span/hash/result-construction helpers are separate or unnecessary.",
    ),
    "direct-binding": (
        145,
        [(33, 84), (95, 192)],
        "Shared module declaration binding lookup; unique undecorated native class/function, competing assignments/imports, wildcard/dynamic namespace guards and qualified outcomes.",
        "These value/result rules prevent equating a source declaration with its binding. Input validation duplicates the selected frame guard and is omitted; digest code is unnecessary.",
    ),
    "module-interpretation": (
        147,
        [(27, 153), (156, 243)],
        "Explicit-root module/package kind and interpretation/universe contracts, observed occurrence identity, exclusions, root-level initializer and identifier policy, duplicate interpretations without precedence.",
        "Interpretation values plus root-to-name rules are the native integration surface. Exclude digest implementation; do not require source-root configuration inference.",
    ),
    "package-membership": (
        149,
        [(34, 150), (153, 243)],
        "Immediate observed package membership, endpoint/derivation/coverage/assessment contracts and unique PACKAGE parent rule; missing selection and competing interpretations remain qualified.",
        "Values and immediate-parent rule are jointly needed to preserve membership distinct from exposure. The shared freshness principle is witnessed separately; no transitive tree is required.",
    ),
    "ri-architecture": (
        4,
        [(179, 235)],
        "Accepted definition/derivation/result separation, dependency versus support provenance, immutable qualified RI, coverage and justified absence.",
        "This concise accepted contract constrains new export facts. Broad graph, capability registration, retrieval and execution architecture is omitted.",
    ),
    "ri-taxonomy": (
        10,
        [(378, 419), (442, 460)],
        "Taxonomy definitions of derivation, dependency/provenance, qualified immutable RI, applicability and non-negative unsupported territory.",
        "These two sections independently express the same design constraints as the accepted architecture section; unrelated taxonomy domains do not contribute.",
    ),
    "ri-adr": (
        6,
        [(229, 268), (293, 326), (385, 408)],
        "Accepted definition/result vocabulary and identity compatibility, immutable derived knowledge, explicit dependencies, coverage and unknown versus absence.",
        "The three paragraphs are complementary parts of the same substitute contract, not three independent mandatory documents. ADR graph and realization sections are unnecessary.",
    ),
    "repository-id": (
        170,
        [(11, 29)],
        "Canonical nominal RepositoryId wrapper and construction/text contract; repository identity is independent of location/state.",
        "Only the existing semantic identity wrapper is needed; core UUID internals and generic identity tests are unnecessary.",
    ),
    "resource-value": (
        172,
        [(49, 72)],
        "ContentIdentity and retained resource occurrence fields with exact address, decoded content, encoding and byte size.",
        "The native values are sufficient; export RI does not own path normalization or generic content hashing.",
    ),
    "snapshot-value": (
        173,
        [(19, 61)],
        "Canonical RepositorySnapshotId and RepositorySnapshot fields, exact resource access, missing-address failure and bounded snapshot scope.",
        "This native container contract suffices; observation filesystem internals and persistence are outside export RI.",
    ),
    "source-dependency": (
        129,
        [(51, 143)],
        "Canonical Python source coordinates/occurrences, exact repository/snapshot/content resource dependency, parser/grammar definition identity and derivation.",
        "These values are reused by existing Python RI and must qualify new provenance. General time/identity/path mechanisms and other RI families are unnecessary.",
    ),
    "frame-validation": (
        140,
        [(443, 474)],
        "Existing membership, repository, snapshot, retained-resource and universe checks before importing bounded RI evidence.",
        "This single native validation contract is enough to establish stale/foreign-frame rejection. Equivalent guards in every neighboring module are helpful rather than additional REQUIRED witnesses.",
    ),
    "reference-model": (
        162,
        [(35, 166)],
        "Reference target union, routes/outcomes, target_subject as existing declaration subject, exact resource/source/import support and non-exhaustive coverage.",
        "Use the active declaration Reference model only; obsolete function-only archive types and unrelated analysis helpers are not needed.",
    ),
    "reference-routes": (
        163,
        [(127, 234)],
        "Reference import/module resolution, shared direct lookup, preserved one-facade fallback, imported and module-qualified routes without public exposure.",
        "Only imported routes can interact with the new exposure boundary. Method dispatch and lexical-scope implementation detail do not constrain export RI.",
    ),
    "reference-syntax": (
        160,
        [(42, 49), (97, 170), (173, 195)],
        "Active derivation signature, exact outermost Name/Attribute loads, result construction and direct_call solely as Call.func syntax.",
        "This is the occurrence/Call contract, not a runtime call graph. Parsing/setup and duplicated frame checks are unnecessary in this alternative.",
    ),
    "reference-contract": (
        164,
        [(3, 58)],
        "Complete active Reference semantic contract: native declaration targets, exact expressions, imported/direct/one-facade/module-qualified routes, conservative guards, direct Call syntax, non-exhaustiveness and consumer nonclaims.",
        "This bounded package section can establish the integration boundary without implementation internals. Localization consumer implementation and projection details are excluded.",
    ),
    "module-facade": (
        144,
        [(1, 44)],
        "Neighboring Python modules package exposes named imports and an explicit literal __all__ list of public RI values/operations.",
        "The small complete facade shows the convention. Any one of the reviewed neighboring facades independently establishes it; neither every initializer nor a global top-level export update is required.",
    ),
    "import-facade": (
        138,
        [(1, 56)],
        "Neighboring Python imports package exposes named imports and a literal __all__ of supported RI contracts.",
        "This small complete facade substitutes for the modules/references/Python facade convention; importing names does not itself assert export RI truth.",
    ),
    "reference-facade": (
        157,
        [(1, 26)],
        "Active Python References package public named-import and explicit __all__ convention.",
        "This concise facade independently supplies the same public API convention; other initializers are not complementary requirements.",
    ),
    "python-facade": (
        119,
        [(1, 28)],
        "Python-wide public facade with named imports and literal __all__, exposing bounded RI conventions.",
        "One complete nearby facade establishes the convention. Its location does not require putting every new API at the Python-wide facade.",
    ),
    "documentation-authority": (
        61,
        [(3, 39), (365, 371)],
        "Documentation authority and update workflow: current central architecture, taxonomy meanings, package/source API authority, historical ADR/research distinction and package-first updates.",
        "Authority and update rule are complementary; unrelated mechanism inventory and historical experiment navigation are unnecessary.",
    ),
    "architecture-current-boundary": (
        4,
        [(549, 577)],
        "Current architecture's imported-member non-export/non-__all__ scope and active Reference boundary that the new production capability must update accurately.",
        "This is the current claim being extended, not the entire architecture document. A new package overview alone would leave this authoritative current-state description incomplete.",
    ),
    "python-documentation-surface": (
        125,
        [(1, 15)],
        "Existing Python RI navigation explicitly sends readers to configuration's deferred public-export inventory and separates RI from Retrieval.",
        "Only current package navigation/deferral claim needs review when adding supported export RI; mirrored-path history is unrelated.",
    ),
    "documentation-policy": (
        2,
        [(220, 226)],
        "Repository policy requires package/architecture/map/backlog/historical-ledger impact checks as applicable, accurate behavior claims and preserved history.",
        "This exact checklist adds the operating requirement to the map's authority/update contract; no unrelated governance or Git sections are required for the frozen development task.",
    ),
    "validation-contract": (
        60,
        [(1, 44)],
        "Canonical protected test invocation, pre-collection experiment exclusion, strict/branch 100% production coverage and separate Ruff format/lint, mypy and staged/unstaged diff checks; confirmation is separate.",
        "The whole short validation contract is the minimum single-source alternative. Config and runner corroborate it but are not required alongside this complete contract.",
    ),
}

RI_ALTERNATIVES = [["ri-architecture"], ["ri-taxonomy"], ["ri-adr"]]
REFERENCE_ALTERNATIVES = [
    ["reference-contract"],
    ["reference-model", "reference-routes", "reference-syntax"],
]
TEST_CORE = [
    "function-subject",
    "class-subject",
    "source-selection",
    "import-declaration",
    "facade-resolution",
    "direct-binding",
    "module-interpretation",
    "package-membership",
    "frame-validation",
]
ALTERNATIVES = {
    "declaration-identity": [["function-subject", "class-subject", "source-selection"]],
    "binding-reexports": [
        [
            "import-declaration",
            "import-resolution",
            "facade-resolution",
            "direct-binding",
        ]
    ],
    "module-membership": [["module-interpretation", "package-membership"]],
    "explicit-exposure": [
        [
            "source-selection",
            "import-declaration",
            "facade-resolution",
            "direct-binding",
            "module-interpretation",
            *a,
        ]
        for a in RI_ALTERNATIVES
    ],
    "unsupported-behavior": [
        ["direct-binding", "facade-resolution", *a] for a in RI_ALTERNATIVES
    ],
    "snapshot-provenance": [
        [
            "repository-id",
            "resource-value",
            "snapshot-value",
            "source-dependency",
            "frame-validation",
            *a,
        ]
        for a in RI_ALTERNATIVES
    ],
    "reference-integration": REFERENCE_ALTERNATIVES,
    "package-api": [
        ["module-facade"],
        ["import-facade"],
        ["reference-facade"],
        ["python-facade"],
    ],
    "tests": [[*TEST_CORE, *a] for a in REFERENCE_ALTERNATIVES],
    "documentation": [
        [
            "documentation-authority",
            "architecture-current-boundary",
            "python-documentation-surface",
            "documentation-policy",
        ]
    ],
    "validation": [["validation-contract"]],
}

APPLICABILITY = {
    "declaration-identity": "The task explicitly requires source declaration identity distinct from import binding; native functions and classes are present in frozen RI.",
    "binding-reexports": "Direct package-facade re-exports and existing import/member integration are explicit task requirements, and the archive contains that implementation.",
    "module-membership": "The task explicitly distinguishes module/package API surfaces and package membership; an explicit-root interpretation/membership API exists.",
    "explicit-exposure": "This is the requested new capability: explicit exposure, direct re-exports and statically explicit __all__. Its absence is a design requirement, not non-applicability.",
    "unsupported-behavior": "The task mandates ambiguity/abstention for unsupported/dynamic exports and explicitly excludes runtime import, dynamic __getattr__ and unrestricted star closure.",
    "snapshot-provenance": "Preserving native repository/snapshot identity and provenance is explicit; all adjacent RI APIs retain observed dependencies.",
    "reference-integration": "The task explicitly requires coherent Reference integration. Coherence is boundary preservation, not automatically extending Reference targets or truth.",
    "package-api": "The conditional convention clause applies affirmatively: frozen neighboring Python RI packages expose named public imports with static __all__ lists.",
    "tests": "The task explicitly requires rigorous tests for the new supported and rejected semantics plus neighboring-contract regressions.",
    "documentation": "The task explicitly requires authoritative architecture/development documentation, and frozen policy assigns authority and update duties.",
    "validation": "The task explicitly requires protected development validation; the frozen validation document specifies the command and static gates.",
}

# Additional orientation only. No classification is produced by textual scoring.
HELPFUL = {
    "declaration-identity": [124, 131, 146, 376, 382],
    "binding-reexports": [4, 61, 138, 146, 164, 391, 392, 394],
    "module-membership": [146, 396, 397],
    "explicit-exposure": [119, 138, 144, 146, 153, 157, 240, 259, 392],
    "unsupported-behavior": [124, 146, 153, 164, 392, 404],
    "snapshot-provenance": [147, 149, 150, 160, 171, 376, 382, 392, 394, 397, 404],
    "reference-integration": [145, 157, 161, 392, 404],
    "package-api": [4, 61, 82, 125, 146, 153],
    "tests": [124, 131, 146, 164, 171, 376, 382, 391, 392, 394, 396, 397, 404, 63],
    "documentation": [6, 10, 60, 62, 124, 131, 146, 153, 164],
    "validation": [2, 63, 64],
}

NECESSITY = {
    "function-subject": "Export/source identity assertions would otherwise have no contract for retaining native function subjects, distinguishing repeated names, or retaining exact support. Class subjects cannot establish the function identity interface.",
    "class-subject": "The function contract cannot identify native classes. A new exposure value needs the existing class identity and declaration support rather than inventing an export-specific class subject.",
    "source-selection": "Binding lookup drops decorated/rebound declarations. Without the separate canonical source selector, exposure implementation/tests can incorrectly equate a rejected binding with a missing source declaration or duplicate canonical source parsing.",
    "import-declaration": "Facade resolution results alone do not define the native syntactic import occurrence, relative level, imported name versus local alias, or direct-body scope needed to represent a declared re-export independently of successful target binding.",
    "import-resolution": "A facade import's source package and explicit universe determine relative module targets. The member outcome alone does not define missing/competing relative source interpretations, beyond-package rejection or module-only resolution; guessed Python runtime import behavior would be incorrect.",
    "facade-resolution": "Correct integration/regression assertions must preserve the existing function-only one-facade route, alias names, support chain and rejected outcomes. Neither module-only import resolution nor the new task's exposure intent specifies these native rules.",
    "direct-binding": "The source selector deliberately ignores runtime binding competition. Without shared lookup's guarded target/outcome contract, new export targets or tests could incorrectly treat decorated, rebound, wildcard or dynamic namespace source as uniquely supported bindings.",
    "module-interpretation": "Package facade identity requires the existing explicit-root PACKAGE interpretation and resource/universe qualification. A path ending in __init__.py alone cannot supply canonical interpretation identity, exclusions or competing roots.",
    "package-membership": "Module dotted names alone do not state the accepted immediate-parent relation: an observed unique PACKAGE parent is necessary, and missing/ambiguous selections retain assessments. Exposure must not substitute for that relation; tests need its actual contract.",
    "ri-architecture": "Native dataclass examples do not define the accepted architectural separation of semantic dependencies, result support, immutable knowledge and coverage. New export design and qualified unknown outcomes need this contract or a complete documentary substitute.",
    "ri-taxonomy": "This is a competing complete source of the semantic-dependency, immutable-result and coverage constraints; the requirement is the information, not reading taxonomy in addition to an equivalent accepted architecture/ADR witness.",
    "ri-adr": "This accepted decision can substitute for the same identified-computation, qualified-result and justified-absence contract. It is not an extra historical reading requirement once an equivalent complete contract is available.",
    "repository-id": "Snapshot/resource values reference RepositoryId but do not define its canonical nominal wrapper. Preserving native logical identity requires that interface, not a newly generated string or a checkout-derived identity.",
    "resource-value": "Source anchors alone do not define the retained occurrence/content values that exposure provenance and dependency validation must carry. The exact native resource fields are necessary for integration rather than a parallel representation.",
    "snapshot-value": "RepositoryId and source dependencies do not define SnapshotId/RepositorySnapshot or exact retained-resource access and missing-state failure. Export derivation must consume that container and tests must validate the correct state.",
    "source-dependency": "Native subjects refer to a resource-dependency identity but do not specify its snapshot/repository/content construction or the AST coordinate contract. These shared Python values prevent new incompatible provenance and unidentified parser semantics.",
    "frame-validation": "Nominal IDs alone are insufficient: the existing contract also checks analysis membership and retained resource content/universe state. This gives the necessary stale/foreign-frame rejection rule and native negative assertions, beyond value definitions.",
    "reference-model": "In the source alternative, this supplies the exact target subject API, target-resource and support fields and non-exhaustive outcome model. The route implementation and Call tagging alone cannot establish those value contracts.",
    "reference-routes": "In the source alternative, model enum names alone cannot establish how direct lookup precedes the one-facade fallback or how imported versus module-qualified evidence is retained. Those routes must remain distinct from new public exposure.",
    "reference-syntax": "In the source alternative, target/route types alone cannot establish exact outermost expression occurrences or direct_call as Call.func syntax. Export exposure must not silently become Reference or invocation truth; tests need the existing derivation interface.",
    "reference-contract": "This complete package contract supplies the same native target/route/expression/nonclaim information as the three source units. A competent implementer can preserve Reference coherence from it without modifying or understanding unrelated resolver internals.",
    "module-facade": "One reviewed neighboring facade is needed to establish the applicable existing package API convention rather than guessing whether a new public Python RI API should have named re-exports and an explicit list. This facade is replaceable by any other complete listed facade.",
    "import-facade": "This is a complete substitute for the same applicable local public import/__all__ convention, not an additional requirement to edit the imports package or establish export truth from syntax alone.",
    "reference-facade": "This is a complete substitute for the same local package/API convention; its short initializer establishes the pattern without requiring every facade or a Reference API redesign.",
    "python-facade": "This is a complete substitute for the applicable Python RI public facade convention. It does not mandate exposing the new capability in every ancestor package.",
    "documentation-authority": "The task asks for authoritative documentation. Without the authority/update rules, source comments or historical evidence could incorrectly replace current package/architecture claims, and navigation changes could be missed.",
    "architecture-current-boundary": "The map states that central architecture owns current implemented boundaries. Its existing imported-member non-export scope and Reference description must be understood to add the new supported capability accurately; the package navigation does not contain this current central claim.",
    "python-documentation-surface": "The package's current navigation describes public exports as deferred. Correct authoritative package documentation for a new supported capability must reconcile this wording; central architecture does not supply this package-local claim.",
    "documentation-policy": "The map's update workflow does not contain the operating policy's backlog and historical-ledger impact check. That conditional duty must be known without assuming an absent ledger is irrelevant or rewriting history.",
    "validation-contract": "Future pass/fail results cannot supply the repository's required validation procedure. This complete contract specifies the protected command, experiment exclusion, coverage gate, separate static/diff gates and confirmation boundary; no extra runner/config witness is necessary to know them.",
}


def build() -> dict[str, Any]:
    """Encode reviewed units, obligation-relative judgments and exact default coverage."""
    manifest, resources = packet()
    units = []
    for name, (index, spans, information, smaller_review) in UNIT_SPECS.items():
        resource = resources[index]
        lines = resource["content"].splitlines()
        excerpt = (
            "\n".join(line for start, end in spans for line in lines[start - 1 : end])
            + "\n"
        )
        units.append(
            {
                "unit_id": name,
                "resource_occurrence_identity": resource[
                    "resource_occurrence_identity"
                ],
                "address": resource["address"],
                "line_spans": spans,
                "excerpt_sha256": sha(excerpt.encode()),
                "information": information,
                "smaller_unit_review": smaller_review,
                "inferability": "INFERABLE_AT_START",
                "inherent_discovery": None,
                "manually_reviewed": True,
                "blind_evidence_only": True,
            }
        )
    by_unit = {u["unit_id"]: u for u in units}
    obligations = []
    overrides = []
    for frozen in manifest["obligations"]:
        name = frozen["identity"]
        alternatives = ALTERNATIVES[name]
        used = sorted({u for members in alternatives for u in members})
        reviews = {}
        for unit_id in used:
            unit = by_unit[unit_id]
            reviews[unit_id] = {
                "why_required": f"For {name}: {NECESSITY[unit_id]}",
                "counterfactual": NECESSITY[unit_id]
                + " Remove this information, including accepted substitutes, and other complementary witnesses do not supply the missing contract. A complete competing substitute makes this particular resource dispensable; REQUIRED is conditional alternative membership.",
                "structure_review": unit["smaller_unit_review"]
                + " Within each listed alternative all member information is needed; alternatives are ANY, not cumulative. Already acquired required information can be reused across obligations.",
                "inferability_review": "INFERABLE_AT_START: the exact task names this responsibility and frozen static package/API/documentation inspection establishes its owning contract. No later execution observation is needed; locating it is not inherent discovery.",
            }
        obligations.append(
            {
                **{
                    k: frozen[k]
                    for k in (
                        "identity",
                        "desired_information",
                        "anchors",
                        "provenance",
                        "requirement",
                        "satisfaction_criterion",
                    )
                },
                "frozen_applicability": frozen["applicability"],
                "applicability": "APPLICABLE",
                "applicability_rationale": APPLICABILITY[name],
                "applicability_evidence": [
                    "frozen-task",
                    *sorted({by_unit[u]["resource_occurrence_identity"] for u in used}),
                ],
                "acceptable_witness_alternatives": [
                    {
                        "alternative_id": f"{name}-alternative-{number}",
                        "members": members,
                        "combination_rule": "ALL",
                        "complementarity": "Distinct native contracts inside this alternative jointly supply the obligation's information. Reused contracts are not extra retrieval demands. The task and frozen manifest are always given.",
                        "competition": "ANY one complete alternative suffices. Alternatives substitute the same architectural semantic contract, Reference boundary, or public facade convention; they do not represent alternate task interpretations."
                        if len(alternatives) > 1
                        else "One sufficient information set; no competing substitute has been established in the blind evidence.",
                        "resource_identity_alone_suffices": False,
                    }
                    for number, members in enumerate(alternatives, 1)
                ],
                "required_unit_reviews": reviews,
            }
        )
        per_resource = defaultdict(list)
        for unit_id in used:
            per_resource[by_unit[unit_id]["resource_occurrence_identity"]].append(
                unit_id
            )
        for identity, unit_ids in sorted(per_resource.items()):
            overrides.append(
                {
                    "resource_occurrence_identity": identity,
                    "obligation": name,
                    "judgment": "REQUIRED",
                    "unit_ids": unit_ids,
                    "rationale": "Contains the reviewed information units named here, necessary within at least one complete acceptable alternative. Only those units are required; the rest of the file is not promoted.",
                }
            )
        for index in HELPFUL[name]:
            resource = resources[index]
            identity = resource["resource_occurrence_identity"]
            if identity not in per_resource:
                overrides.append(
                    {
                        "resource_occurrence_identity": identity,
                        "obligation": name,
                        "judgment": "HELPFUL_ONLY",
                        "unit_ids": [],
                        "rationale": f"For {name}, {resource['address']} provides a corroborating contract, nearby facade example, test pattern or navigation/validation context. Correctness can proceed using the complete required alternative; this is not indispensable additional information.",
                    }
                )
    judgments = {
        "schema": "case-0007-obligation-judgments-v1",
        **{
            k: manifest[k]
            for k in (
                "case_identity",
                "task_identity",
                "task",
                "purpose",
                "repository_id",
                "snapshot_id",
                "corpus_id",
                "shared_anchors",
            )
        },
        "blind_packet_digests": {
            "blind_manifest.json": MANIFEST_SHA,
            "blind_resources.json.gz": ARCHIVE_SHA,
        },
        "adjudication_method": {
            "operations": [
                "Load only blind manifest and gzip archive",
                "Pin input bytes and reproduce native content/snapshot/corpus identities",
                "Enumerate all 521 exact addresses",
                "Exact textual search, numbered source/section reads, static imports and public facade inspection",
                "Manually define narrow units and review all REQUIRED units",
                "Exact Cartesian identity accounting and gold-only alternative union enumeration",
            ],
            "interpretation": "The verbatim frozen task and all 11 frozen mandatory obligations are retained. Judgments concern implementation information; no treatment is inferred. A literal __all__ declaration records explicit intended exposure separately from binding resolution, importability and package membership. Unsupported/dynamic forms require qualified abstention, not absence. No nonexistent export implementation is required.",
            "required_review": "Each REQUIRED unit was manually read. Required source contracts supply native types/semantics; documentary alternatives are accepted only when they completely establish the same needed boundary. Existing test trees are not REQUIRED merely for pattern reuse. Tests reuse the required semantic contracts to construct assertions; fixtures/examples improve efficiency. All prerequisites are statically inferable. Resource-level REQUIRED means relevant unit membership in an ANY alternative, never all competing resources simultaneously.",
            "inspection_record": sorted(
                {
                    resources[i]["resource_occurrence_identity"]
                    for i in [
                        2,
                        4,
                        6,
                        10,
                        12,
                        60,
                        61,
                        62,
                        63,
                        64,
                        82,
                        119,
                        123,
                        124,
                        125,
                        129,
                        131,
                        138,
                        139,
                        140,
                        142,
                        144,
                        145,
                        146,
                        147,
                        149,
                        150,
                        153,
                        157,
                        160,
                        161,
                        162,
                        163,
                        164,
                        167,
                        170,
                        171,
                        172,
                        173,
                        240,
                        259,
                        349,
                        376,
                        382,
                        391,
                        392,
                        394,
                        396,
                        397,
                        404,
                        452,
                    ]
                }
            ),
            "excluded_information": "No live source, Case treatment/history/capture/results, confirmation, retrieval or structural APIs were used. Archive-wide exact __all__/__getattr__ searches included literal occurrences only; those are repository source data, not Case experimental metadata.",
        },
        "resource_frame": [
            {k: v for k, v in resource.items() if k != "content"}
            for resource in resources
        ],
        "obligations": obligations,
        "information_units": units,
        "resource_classifications": {
            "default": "UNNECESSARY",
            "default_rationale": "Within the complete frozen address frame, cells without an override supply no additional material task information beyond the reviewed native contracts. The excluded model/runtime/agent, unrelated RI, retrieval/ranking and generic substrate domains do not constrain this bounded export task. Address screening and exact archive searches account for the full universe; this does not assert every unselected file was read line by line or is empty. Nearness/vocabulary alone is insufficient relevance.",
            "required_semantics": "Obligation-relative necessary information, conditional on an acceptable alternative. ALL units in one alternative; ANY complete alternative. A resource label is a projection of the named units, not a whole-file necessity claim or demand to acquire all alternatives.",
            "overrides": sorted(
                overrides,
                key=lambda c: (c["resource_occurrence_identity"], c["obligation"]),
            ),
        },
        "task_interpretation_gaps": [],
        "task_gap_review": "no obvious mandatory task-interpretation gap found. Reviewed every task clause: deterministic public exports/re-exports, identity/binding/membership/exposure separation, static __all__, native provenance, ambiguity/abstention, all neighboring RI integrations, future Localization foundation with no operator, tests, authoritative documentation, applicable API conventions and protected validation. Deterministic ordering/replay belong to explicit-exposure and snapshot-provenance; no ranking, graph expansion, automatic witnesses or runtime semantics are required.",
        "packet_limitations": [
            "The eligible frame contains no docs/implementation_ledger.md or historical reports/research artifacts linked by documentation. Their contents and any additional historical handoff requirements cannot be adjudicated; no extra mandatory witness is invented.",
            "No export implementation or export-specific tests exist in this packet. Static list __all__ is demonstrated in RI facades; an annotated empty tuple occurs in the benchmark facade. The search also finds a dynamic __all__ fixture in a different bounded RI test. These examples do not supply a complete future language for static __all__, reassignment/mutation, unsupported __getattr__, or general public API policy; the task authorizes conservative bounded design, not inference from every occurrence.",
            "Imported-member resolution's function-only one-facade contract is narrower/different from shared conservative direct class/function binding lookup. Its target selection is native declaration matching, not a universal runtime/decorator binding proof. Preserve the actual contracts; do not silently broaden or repair existing RI under the export task. No execution outcomes or future validation pass/fail evidence are available or claimed.",
            "Independent session work used only the supplied user task and blind packet. Runtime model identity/effort is selected by the host; the adjudication artifacts make no unverifiable model or session-reset attestation.",
        ],
        "coverage_diagnostics": {
            "expected_resources": 521,
            "observed_resources": 521,
            "expected_obligations": 11,
            "observed_obligations": 11,
            "expected_cells": 5731,
            "observed_cells": 5731,
            "duplicate_expected_identities": 0,
            "duplicate_observed_identities": 0,
            "missing_identities": 0,
            "unexpected_identities": 0,
        },
        "blindness_declaration": {
            "blind_manifest_accessed": True,
            "blind_resources_accessed": True,
            "other_preexisting_case_artifacts_accessed": False,
            "lexical_treatment_or_results_accessed": False,
            "role_treatment_or_results_accessed": False,
            "grounding_treatment_or_results_accessed": False,
            "generation_treatment_or_results_accessed": False,
            "branching_or_reference_treatment_metadata_accessed": False,
            "current_task_relevant_checkout_source_accessed": False,
            "effectiveness_analysis_performed": False,
            "stage_d_performed": False,
            "confirmation_accessed": False,
        },
    }
    judgments["gold_statistics"] = statistics(judgments)
    validate(judgments)
    return judgments


def main() -> None:
    """Create deterministic judgments once; never overwrite an existing artifact."""
    judgments = build()
    with (HERE / "judgments.json").open("xb") as output:
        output.write(canonical(judgments))
    print(
        json.dumps(
            {
                k: v
                for k, v in judgments["gold_statistics"].items()
                if not k.endswith("union")
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

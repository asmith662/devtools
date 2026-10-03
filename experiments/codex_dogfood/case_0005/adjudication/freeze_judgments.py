# Copyright (c) 2026
# Case-specific assertion checks, explicit judgment tables and CLI reporting.
# ruff: noqa: ANN001, ANN201, D103, INP001, S101, PLR2004, PERF401, PLR0913, PLR0917, E501
"""Freeze and replay Case 0005 independent blind Stage C judgments.

Only the two blind inputs and this adjudication directory are read or written.
The coverage primitive is executed from its frozen archive source, never imported
from the current checkout. Labels and witness semantics are experiment owned.
"""

import hashlib
import json
import sys
import types
from dataclasses import asdict

from inspect_blind import (
    ARCHIVE_BYTES,
    BASE,
    BY_PATH,
    MANIFEST,
    MANIFEST_BYTES,
    RESOURCES,
    validate_packet,
)

UNITS = {}
DECISIONS = {}
LOC = "src/devtools/context/localization/"


def unit(key, path, spans, information):
    resource = BY_PATH[path]
    lines = resource["content"].splitlines()
    assert all(1 <= start <= end <= len(lines) for start, end in spans)
    text = "\n".join("\n".join(lines[start - 1 : end]) for start, end in spans)
    UNITS[key] = {
        "identity": key,
        "resource_identity": resource["resource_identity"],
        "line_spans_inclusive": spans,
        "selected_text_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "information": information,
    }


unit(
    "owner-overview",
    LOC + "docs/overview.md",
    [(9, 31), (129, 160)],
    "Localization owns caller obligations, assessments and scoped readiness; "
    "acquisition, role hints, Context selection and agent execution "
    "remain distinct.",
)
unit(
    "owner-architecture",
    "docs/architecture.md",
    [(841, 910)],
    "Canonical current Localization ownership, native "
    "evidence/routing boundaries, "
    "dependency direction, unresolved alternatives and non-claims.",
)
unit(
    "kernel-assessment",
    LOC + "assessment.py",
    [(18, 63), (80, 114)],
    "Existing applicability/disposition vocabulary, snapshot-"
    "qualified evidence "
    "references, supported witness shape and immutable assessment "
    "fields/invariants.",
)
unit(
    "kernel-readiness-boundary",
    LOC + "readiness.py",
    [(278, 291), (340, 361)],
    "Existing readiness and disposition rules: unresolved evidence cannot be "
    "published as resolution; conditional applicability needs support.",
)
unit(
    "witness-declarations",
    LOC + "obligation.py",
    [(41, 95)],
    "Hashable nonempty distinct witness members; ordered caller alternatives, "
    "duplicate equivalent-set rejection and retained criterion/task scope.",
)
unit(
    "witness-evaluation",
    LOC + "readiness.py",
    [(324, 337)],
    "A complete caller set requires all members; the first complete "
    "alternative "
    "is returned, with no lexical or role shortcut.",
)
unit(
    "candidate-semantics",
    "docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md",
    [(131, 155)],
    "Candidate association is a local native-referent/rule/reason record; "
    "competition requires a unique-owner criterion, incomplete/unsupported "
    "hypotheses remain visible and native supports are not extra votes.",
)
unit(
    "native-lanes",
    LOC + "lexical.py",
    [(48, 81)],
    "Obligation lane retains its request and exact native result; acquisition "
    "retains caller frame, purpose, repository/snapshot and separate "
    "global lane.",
)
unit(
    "native-results",
    "src/devtools/context/retrieval/lexical/bm25.py",
    [(97, 125)],
    "Exact native match and result shapes retain document statistics, local "
    "contributions, query, index, settings, bounds and filename evidence.",
)
unit(
    "role-support-contract",
    LOC + "roles/models.py",
    [(81, 99), (112, 177)],
    "Positive support basis/source/native references; evidence identity binds "
    "repository, snapshot, derivation, resource and support membership. Full "
    "frame and native inputs are retained; empty known-resource "
    "support is not negative.",
)
unit(
    "routing-view-contract",
    LOC + "routing/models.py",
    [(59, 92)],
    "Routed candidates point at native matches and original role "
    "evidence; lane "
    "retains native lane, and whole view retains acquisition/global result. "
    "Presentation metadata must remain distinct from witness satisfaction.",
)
unit(
    "task-local-identities",
    LOC + "identity.py",
    [(13, 23), (40, 65)],
    "Task, anchor, obligation and acquisition-lane keys are scoped immutable "
    "caller identities, distinct from repository/resource identity.",
)
unit(
    "task-frame-contract",
    LOC + "task.py",
    [(33, 64)],
    "Exact immutable interpretation owns anchor/obligation membership, rejects "
    "foreign/duplicate keys and unresolved anchor references.",
)
unit(
    "resource-contract",
    "src/devtools/context/repository/resource.py",
    [(13, 46), (49, 72)],
    "Canonical repository-relative address and independent content identity "
    "compose an observed resource occurrence; a path alone does not "
    "prove freshness.",
)
unit(
    "snapshot-contract",
    "src/devtools/context/repository/snapshot.py",
    [(19, 61)],
    "Snapshot identity is distinct from repository identity and "
    "contains explicit "
    "observed occurrences; resource_at is the bounded exact lookup contract.",
)
unit(
    "lexical-frame-check",
    "src/devtools/context/retrieval/composition.py",
    [(142, 181)],
    "Canonical existing validation checks the entire native corpus, documents "
    "and index statistics against exact snapshot occurrences, not "
    "only surfaced matches.",
)
unit(
    "role-native-frame-check",
    LOC + "routing/derive.py",
    [(70, 155)],
    "Existing role/native integration rejects foreign, stale, duplicate or "
    "out-of-frame evidence and sources, invalid caller lanes, inconsistent "
    "native corpora and matches outside their own index.",
)
unit(
    "public-facade",
    LOC + "__init__.py",
    [(4, 72)],
    "Localization explicitly imports and lists supported public "
    "values/functions "
    "in __all__; the association API must integrate with this "
    "established surface.",
)
unit(
    "test-kernel-idiom",
    "tests/context/localization/test_kernel.py",
    [(249, 290)],
    "Existing semantic contract tests use dataclasses.replace to vary"
    " immutable "
    "inputs and pytest.raises(ValueError, match=...) for invalid boundaries.",
)
unit(
    "test-lexical-idiom",
    "tests/context/localization/test_lexical.py",
    [(392, 410)],
    "Analogous immutable native-acquisition tests vary frames with replace and "
    "assert scoped ValueError messages using pytest.raises.",
)
unit(
    "test-routing-idiom",
    "tests/context/localization/routing/test_routing.py",
    [(239, 274)],
    "Analogous native/role integration tests use replace and pytest.raises for "
    "foreign frames and stale nested support; same package test conventions.",
)
unit(
    "documentation-authority",
    "docs/documentation_map.md",
    [(3, 39), (74, 92), (354, 360)],
    "Current architecture versus accepted decisions versus package contracts "
    "versus historical development records, plus package-first update workflow.",
)
unit(
    "development-tracking",
    "docs/roadmap.md",
    [(50, 62)],
    "Current development sequence records the implemented role and "
    "routing slices; "
    "it is the available development-tracking surface for the next capability.",
)
unit(
    "validation-contract",
    "docs/development/validation.md",
    [(3, 44)],
    "Canonical protected test command, precollection exclusion, strict pytest/"
    "branch/100% production gate, separate Ruff/format/mypy/diff checks and "
    "confirmation authorization boundary; future pass/fail is not a witness.",
)
unit(
    "static-configuration",
    "pyproject.toml",
    [(57, 78)],
    "Applicable Ruff target/line length/ALL rules/test exception and "
    "strict mypy "
    "Python version, checked roots and package/path settings.",
)


def decide(obligation, alternatives, reasons, helpful, rationale, applicability=None):
    required = list(dict.fromkeys(key for group in alternatives for key in group))
    assert set(reasons) == set(required)
    units = []
    for key in required:
        units.append(
            {
                "unit_identity": key,
                "judgment": "REQUIRED",
                "inferability": "INFERABLE_AT_START",
                "inherent_discovery": None,
                "required_review": {
                    "obligation": obligation,
                    "exact_information": UNITS[key]["information"],
                    "necessity": reasons[key],
                    "smaller_unit_review": "Selected declarations, functions or named "
                    "sections contain the governing contract. Omitted unrelated bodies "
                    "are not required. Adjacent selected declarations form one coherent "
                    "contract; their fields/invariants cannot honestly be dropped.",
                    "relationship": "Conjunctive with other members of its listed "
                    "alternative; competing only where another complete alternative "
                    "is explicitly listed. No independent vote or score is implied.",
                    "start_identification": "Frozen task names this responsibility; "
                    "archive package layout and bounded static inspection identify "
                    "this contract before implementation.",
                    "blind_basis": "Frozen archive contents only.",
                },
            }
        )
    DECISIONS[obligation] = {
        "applicability": "APPLICABLE",
        "applicability_rationale": applicability
        or "The frozen task explicitly requires this capability/quality boundary, "
        "and the named frozen contracts exist. No conditional exemption applies.",
        "rationale": rationale,
        "information_unit_judgments": units,
        "acceptable_witness_alternatives": [
            {"identity": f"{obligation}-alternative-{i}", "all_members": group}
            for i, group in enumerate(alternatives, 1)
        ],
        "helpful_resource_rationales": helpful,
        "unresolved_judgments": [],
    }


decide(
    "semantic-ownership",
    [
        ["owner-overview", "kernel-assessment", "kernel-readiness-boundary"],
        ["owner-architecture", "kernel-assessment", "kernel-readiness-boundary"],
    ],
    {
        "owner-overview": "Existing owner and non-claims must be established; "
        "this current package contract can supply that information instead of "
        "the central architecture section.",
        "owner-architecture": "The canonical current section independently "
        "supplies the owner/boundary information instead of the package overview.",
        "kernel-assessment": "Correct integration cannot invent a second "
        "assessment/witness shape or confuse a hypothesis with supported "
        "resolution.",
        "kernel-readiness-boundary": "Association must preserve implemented "
        "readiness/disposition behavior, including rejection of an open claim "
        "that already carries a complete supported set.",
    },
    {
        "docs/architecture/taxonomy.md": "Terminology corroborates owner boundaries "
        "already supplied by either required owner witness.",
        "docs/architecture/decisions/ADR-0005-obligation-driven-"
        "repository-localization.md": "Accepted rationale is useful; current ownership plus source contracts "
        "establish this obligation without the historical implementation inventory.",
    },
    "One current owner description plus the actual assessment and readiness "
    "seams is sufficient. Architecture and package overview compete for owner "
    "information; implemented contracts complement either description.",
)
decide(
    "witness-algebra",
    [["witness-declarations", "witness-evaluation", "candidate-semantics"]],
    {
        "witness-declarations": "Caller witness representation and its equality/"
        "uniqueness rules cannot be inferred solely from generic all/any prose.",
        "witness-evaluation": "Must preserve exact implemented all-members and "
        "first-alternative semantics when exposing associated hypotheses.",
        "candidate-semantics": "The existing kernel has no candidate-hypothesis "
        "type; accepted association/competition and incompleteness boundaries "
        "are needed to add the first capability without inventing satisfaction.",
    },
    {
        LOC + "assessment.py": "Existing supported-witness shapes aid design; their "
        "integration is already required under semantic ownership.",
        LOC + "docs/overview.md": "Readable all/any description corroborates source.",
        "tests/context/localization/test_kernel.py": "Concrete all/any examples "
        "improve confidence but the source defines exact behavior.",
    },
    "Representation, executed satisfaction algebra and accepted unresolved "
    "candidate semantics complement each other. No independent sufficient "
    "alternative to this combined contract was established.",
)
decide(
    "native-evidence",
    [["native-lanes", "native-results"]],
    {
        "native-lanes": "Must attach to the existing caller frame and independent "
        "native lanes rather than collapse a resource observed by several lanes.",
        "native-results": "Faithful preservation requires the actual native "
        "candidate/result shape and its retained provenance fields.",
    },
    {
        "src/devtools/context/retrieval/composition.py": "Shows canonical candidate "
        "resource access and validation; exact frame checks belong to "
        "snapshot-frame.",
        "src/devtools/context/retrieval/lexical/statistics.py": "Explains the nested "
        "document/statistics link visible already in required integration code.",
        "src/devtools/context/retrieval/lexical/analysis.py": "Explains retained "
        "observations without adding an association requirement.",
        "src/devtools/context/repository/document.py": "Documents resource-backed "
        "representation; no new representation is requested.",
        LOC
        + "docs/overview.md": "Readable native-provenance/non-satisfaction account.",
        "tests/context/localization/test_lexical.py": "Native identity-retention examples.",
    },
    "The task's existing lexical/routing seam supports a bounded first native "
    "association. BM25 execution/scoring internals, structural/graph Retrieval "
    "expansion and a universal evidence ontology are not necessary.",
)
decide(
    "role-routing-integration",
    [["role-support-contract", "routing-view-contract"]],
    {
        "role-support-contract": "Role observations must keep exact positive "
        "support identity, native basis and frame instead of being copied as "
        "unqualified truth or inferred negative evidence.",
        "routing-view-contract": "Integration must reference the original "
        "matches/lanes/global inventory and preserve the view seam, independent "
        "of presentation order or support-based satisfaction.",
    },
    {
        LOC + "routing/derive.py": "Explains construction and checks; compatibility "
        "checks are required for snapshot-frame, tier construction need not change.",
        LOC
        + "routing/docs/overview.md": "Corroborating explanation of lossless views.",
        LOC + "roles/docs/overview.md": "Support vocabulary and limits in prose.",
        "tests/context/localization/routing/test_routing.py": "Lossless-view examples.",
    },
    "Two native value contracts complement one another. Consuming retained "
    "role observations does not require reading every RI derivation "
    "that produced them.",
)
decide(
    "snapshot-frame",
    [
        [
            "task-local-identities",
            "task-frame-contract",
            "resource-contract",
            "snapshot-contract",
            "lexical-frame-check",
            "role-native-frame-check",
        ]
    ],
    {
        "task-local-identities": "Must distinguish task-local obligation/lane "
        "keys from repository identity to reject a foreign caller frame.",
        "task-frame-contract": "Must respect exact interpretation membership "
        "and detect an unknown or changed obligation, not merely equal task labels.",
        "resource-contract": "Stale occurrence rejection needs canonical address "
        "plus content/occurrence identity, not a filename-only association.",
        "snapshot-contract": "Must bind to the actual explicit repository snapshot "
        "and reuse its native resource lookup rather than inventing a frame.",
        "lexical-frame-check": "Canonical whole-corpus compatibility already "
        "owns native lexical snapshot validation and must be reused.",
        "role-native-frame-check": "Stamped IDs alone are insufficient for "
        "forged/stale role entries and malformed native lanes; current integration "
        "checks define the exact nested/frame constraints to preserve.",
    },
    {
        LOC + "assessment.py": "Snapshot-qualified reference structure corroborates "
        "already-required assessment integration.",
        "src/devtools/context/repository/identity.py": "Nominal RepositoryId implementation "
        "aids fixture construction; other required contracts show its use.",
        LOC + "roles/models.py": "Role digest fields corroborate identity checks.",
        "src/devtools/evaluation/coverage.py": "Reusable coverage mechanics if needed; "
        "does not define association frame or judgment semantics.",
    },
    "Task membership, occurrence identity, snapshot lookup and the "
    "two existing "
    "compatibility seams are complementary. No persisted schema migration or "
    "live filesystem observation is required by this increment.",
)
decide(
    "package-integration",
    [["public-facade"]],
    {
        "public-facade": "Existing explicit Localization imports/__all__ govern "
        "coherent API exposure; bypassing this surface silently omits supported "
        "capability from the established caller entry point."
    },
    {
        LOC + "roles/__init__.py": "Sibling explicit facade confirms convention.",
        LOC
        + "routing/__init__.py": "Sibling models/derive facade confirms convention.",
        "tests/context/localization/test_kernel.py": "Consumers use the root facade.",
        "pyproject.toml": "Wheel packages the src/devtools tree; no extra registry "
        "or package declaration is needed.",
    },
    "Applicability follows explicit exports and demonstrated public consumers, "
    "not a PACKAGE_SURFACE role or initializer filename alone.",
    "Condition holds affirmatively: root __init__.py imports supported kernel/"
    "lexical APIs and lists __all__; tests import those APIs through "
    "it. Sibling "
    "roles and routing facades use the same convention. This governs new API "
    "integration; it does not authorize generic public-export RI.",
)
decide(
    "tests",
    [["test-kernel-idiom"], ["test-lexical-idiom"], ["test-routing-idiom"]],
    dict.fromkeys(
        ("test-kernel-idiom", "test-lexical-idiom", "test-routing-idiom"),
        "The frozen testing obligation needs repository test-convention "
        "information, not every analogous case. This concrete immutable-"
        "input/invalid-boundary pattern independently supplies "
        "pytest/replace/assertion idioms. Other required semantic "
        "contracts supply the positive, all/any, provenance and non-claim"
        " test requirements. Either other listed example can replace this"
        " one; exact fixture helpers need not be reused.",
    ),
    {
        "tests/context/localization/roles/test_evidence.py": "Examples of positive "
        "multi-label support and bounded input normalization.",
        "pyproject.toml": "Collection and strict/static gates already supplied "
        "by validation; no independent second testing framework is present.",
    },
    "Three examples compete as sufficient sources of the same testing idiom. "
    "Required source contracts elsewhere define what to assert. The remaining "
    "parts of these three test files are helpful precedent, not "
    "required units. "
    "No entire test tree or particular fixture reuse is required.",
)
decide(
    "documentation",
    [
        [
            "documentation-authority",
            "owner-architecture",
            "owner-overview",
            "development-tracking",
        ]
    ],
    {
        "documentation-authority": "Must distinguish authoritative current "
        "architecture/package contracts from research/history and follow the "
        "established behavior-change update workflow.",
        "owner-architecture": "The explicitly requested architecture update "
        "must accurately extend the current canonical Localization account.",
        "owner-overview": "Package docs own implemented detailed API semantics; "
        "must describe the new association separately from acquisition/readiness.",
        "development-tracking": "The requested development documentation must "
        "extend the actual current role/routing sequence, without rewriting "
        "historical research as implementation evidence.",
    },
    {
        "AGENTS.md": "Repository documentation-impact operating rules corroborate map.",
        "docs/architecture/taxonomy.md": "Terminology consistency reference.",
        "docs/architecture/decisions/ADR-0005-obligation-driven-"
        "repository-localization.md": "Accepted rationale is already required for candidate semantics; "
        "an unchanged "
        "decision need not be rewritten to record this implementation.",
        LOC + "roles/docs/overview.md": "Adjacent role documentation for cross-links.",
        LOC
        + "routing/docs/overview.md": "Adjacent view documentation for cross-links.",
    },
    "These four current surfaces are complementary for authority, "
    "architecture, "
    "package details and development tracking. A changed-file prediction alone "
    "is not the basis. The ledger is referenced but absent from the eligible "
    "archive; its contents or need for a particular ledger entry "
    "cannot be judged.",
)
decide(
    "validation",
    [["validation-contract", "static-configuration"]],
    {
        "validation-contract": "Must locate the canonical protected invocation "
        "and know experiment exclusion, coverage gate and separate static checks "
        "without opening confirmation outcomes.",
        "static-configuration": "Passing the applicable static gates requires "
        "their actual configured Ruff and strict mypy scope/options, not just "
        "knowing the tool names. Test coverage/profile semantics are already in "
        "the canonical validation contract.",
    },
    {
        "scripts/validate_development.py": "Implementation confirms documented "
        "selection/exit semantics; canonical contract is sufficient to locate them.",
        "AGENTS.md": "Operating guide points to the canonical validation contract.",
    },
    "Command/profile and configured static expectations complement each other. "
    "Future successful execution is not a Localization repository witness.",
)


def serialize(value):
    return (
        json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    ).encode()


def coverage_primitive():
    name = "case_0005_frozen_coverage"
    module = types.ModuleType(name)
    sys.modules[name] = module
    resource = BY_PATH["src/devtools/evaluation/coverage.py"]
    exec(  # noqa: S102 -- only the digest-checked frozen coverage primitive
        compile(
            resource["content"], "blind:src/devtools/evaluation/coverage.py", "exec"
        ),
        module.__dict__,
    )
    return module.compare_identity_coverage


def build():
    validate_packet()
    compare = coverage_primitive()
    expected_obligations = [o["identity"] for o in MANIFEST["obligations"]]
    assert compare(expected=expected_obligations, observed=DECISIONS).is_exact
    identities = [r["resource_identity"] for r in RESOURCES]
    identity_keys = [json.dumps(i, sort_keys=True) for i in identities]
    cells = []
    summaries = []
    required_resources = set()
    for frozen in MANIFEST["obligations"]:
        oid = frozen["identity"]
        decision = DECISIONS[oid]
        by_resource = {}
        for judgment in decision["information_unit_judgments"]:
            uid = judgment["unit_identity"]
            u = UNITS[uid]
            by_resource.setdefault(u["resource_identity"]["address"], []).append(uid)
            assert judgment["inferability"] == "INFERABLE_AT_START"
            assert judgment["required_review"]["obligation"] == oid
        for group in decision["acceptable_witness_alternatives"]:
            assert group["all_members"]
            assert all(k in UNITS for k in group["all_members"])
        observed = []
        counts = dict.fromkeys(
            ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY", "UNRESOLVED"), 0
        )
        for resource in RESOURCES:
            address = resource["address"]
            members = by_resource.get(address, [])
            if members:
                label = "REQUIRED"
                reason = "Contains required information units; requirement is "
                reason += "conditional on the selected complete witness alternative. "
                reason += "Unselected file content is not implicitly required."
                required_resources.add(address)
            elif address in decision["helpful_resource_rationales"]:
                label = "HELPFUL_ONLY"
                reason = decision["helpful_resource_rationales"][address]
            else:
                label = "UNNECESSARY"
                reason = "No additional information necessary or materially helpful "
                reason += "for this bounded obligation given its witnesses, the task "
                reason += "and the other required contracts. This is an obligation-"
                reason += (
                    "relative judgment, not a claim about general repository value."
                )
            counts[label] += 1
            observed.append(json.dumps(resource["resource_identity"], sort_keys=True))
            cells.append(
                {
                    "obligation_identity": oid,
                    "resource_identity": resource["resource_identity"],
                    "judgment": label,
                    "required_units": members,
                    "rationale": reason,
                }
            )
        result = compare(expected=identity_keys, observed=observed)
        assert result.is_exact
        summaries.append(
            {
                "obligation_identity": oid,
                "applicability": decision["applicability"],
                "required_information_units": len(
                    decision["information_unit_judgments"]
                ),
                "resource_counts": counts,
                "coverage": {
                    "expected": len(identity_keys),
                    "observed": len(observed),
                    **asdict(result),
                },
            }
        )
    expected_cells = [(o, key) for o in expected_obligations for key in identity_keys]
    observed_cells = [
        (c["obligation_identity"], json.dumps(c["resource_identity"], sort_keys=True))
        for c in cells
    ]
    cell_coverage = compare(expected=expected_cells, observed=observed_cells)
    assert cell_coverage.is_exact
    assert len(cells) == 4635
    return {
        "schema": "codex-case-0005-blind-obligation-judgments-v1",
        "case": MANIFEST["case"],
        "task_identity": MANIFEST["task_identity"],
        "task_text": MANIFEST["task_text"],
        "purpose": MANIFEST["purpose"],
        "repository_id": MANIFEST["repository_id"],
        "snapshot_id": MANIFEST["snapshot_id"],
        "eligible_frame_identity": MANIFEST["eligible_frame_identity"],
        "anchors": MANIFEST["anchors"],
        "method": {
            "identity": "case-0005-independent-static-blind-adjudication",
            "version": 1,
            "description": "Human-readable independent judgments over the "
            "frozen task/frame and contents. Static path enumeration, exact "
            "text/section inspection and manual contract/import tracing only. "
            "No task-relative retriever, treatment reconstruction or Stage D.",
            "prior_case_format_access": False,
        },
        "blind_input_digests": {
            "blind_manifest.json": hashlib.sha256(MANIFEST_BYTES).hexdigest(),
            "blind_resources.json.gz": hashlib.sha256(ARCHIVE_BYTES).hexdigest(),
        },
        "semantics": {
            "REQUIRED": "Relevant unit information is necessary within its "
            "acceptable alternative. ALL members of one alternative are required; "
            "ANY one complete alternative suffices. Resource labels project unit "
            "presence and do not require unrelated whole-file content or "
            "every competitor.",
            "HELPFUL_ONLY": "Improves efficiency, orientation or confidence but "
            "correctness is reasonably achievable from required witnesses without it.",
            "UNNECESSARY": "No material additional information for this obligation "
            "given the frozen task and required contracts. Every resource "
            "cell is explicit.",
            "UNRESOLVED": "Blind evidence cannot support a defensible conclusion; "
            "never forced to unnecessary merely because evidence is missing.",
            "unit_complementarity": "Members of a single alternative are conjunctive.",
            "unit_competition": "Only listed complete alternatives independently suffice.",
            "whole_resource_remainder": "Unselected content in a required resource "
            "is unnecessary except additional directly analogous examples/operational "
            "explanation, which are helpful only; none becomes required by projection.",
        },
        "information_units": list(UNITS.values()),
        "obligations": [
            {"frozen_obligation": o, **DECISIONS[o["identity"]]}
            for o in MANIFEST["obligations"]
        ],
        "resource_obligation_judgments": cells,
        "task_interpretation_gaps": {
            "findings": [],
            "review": "no obvious mandatory task-interpretation gap found.",
            "rationale": "Native provenance, competing/complementary witnesses, "
            "unresolved hypotheses, semantic non-claims, compatibility, package "
            "integration and all requested quality requirements are represented. "
            "Excluded capabilities are boundaries within the existing obligations, "
            "not silently added implementation obligations.",
        },
        "limitations": [
            (
                "The packet references docs/implementation_ledger.md but does not contain "
                "it. No particular ledger content/update requirement is adjudicated; "
                "map, architecture, package docs and roadmap supply the available "
                "documentation witnesses. No checkout escape was used."
            ),
            (
                "Caller-assigned eligible-frame identity is verified exactly against "
                "the manifest and retained throughout. Its construction formula is "
                "not supplied; no experimental builder was read to reconstruct it."
            ),
            (
                "This judges the first bounded native lexical/role/routing integration. "
                "It does not infer universal supported channels or later implementation."
            ),
        ],
        "summary": {
            "eligible_resources": 515,
            "obligations": 9,
            "expected_resource_obligation_cells": 4635,
            "observed_resource_obligation_cells": len(cells),
            "identity_coverage": asdict(cell_coverage),
            "per_obligation": summaries,
            "required_unique_resources_overall": len(required_resources),
            "required_unique_resource_addresses": sorted(required_resources),
            "required_unit_occurrences_inferable_at_start": sum(
                len(d["information_unit_judgments"]) for d in DECISIONS.values()
            ),
            "required_distinct_unit_identities": len(UNITS),
            "inherent_discovery_count": 0,
            "inherent_discovery_prerequisites": [],
            "unresolved_judgment_count": 0,
            "unresolved_applicability_count": 0,
        },
        "blindness_attestation": {
            "other_preexisting_case_0005_artifacts_accessed": False,
            "experimental_lexical_queries_accessed": False,
            "experimental_caller_role_preferences_accessed": False,
            "experimental_derived_role_assignments_accessed": False,
            "retrieval_outputs_accessed": False,
            "routing_outputs_accessed": False,
            "current_repository_target_implementation_accessed": False,
            "stage_d_effectiveness_analysis": False,
            "confirmation_accessed": False,
            "all_515_resources_accounted_for": True,
            "all_9_obligations_adjudicated": True,
        },
        "digest_contract": "SHA-256 of exact deterministic UTF-8 JSON bytes is "
        "stored in judgments.sha256; avoiding a self-referential embedded digest.",
    }


if __name__ == "__main__":
    artifact = build()
    first = serialize(artifact)
    second = serialize(build())
    assert first == second
    assert serialize(json.loads(first)) == first
    digest = hashlib.sha256(first).hexdigest()
    (BASE / "judgments.json").write_bytes(first)
    (BASE / "judgments.sha256").write_bytes(
        (digest + "  judgments.json\n").encode("utf-8")
    )

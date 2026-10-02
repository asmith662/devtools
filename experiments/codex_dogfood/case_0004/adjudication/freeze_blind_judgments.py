"""Serialize human judgments and check only the frozen blind packet.

No acquisition or ranking is performed. Each specification below is an explicit
human information judgment, not an automatically inferred relevance label.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
import types
from collections import Counter
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode()


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def fields(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value).union(*(fields(v) for v in value.values()))
    if isinstance(value, list):
        return set().union(*(fields(v) for v in value))
    return set()


FORBIDDEN = {
    "query_id",
    "query_identity",
    "query_text",
    "obligation_query",
    "queries",
    "lane",
    "lane_id",
    "lane_identity",
    "rank",
    "ranks",
    "score",
    "scores",
    "bm25_score",
    "content_contribution",
    "filename_contribution",
    "candidate_overlap",
    "retrieved",
    "retrieved_flags",
    "retrieval_provenance",
    "acquisition_runtime",
    "retrieval_results",
}
mb = (ROOT / "blind_manifest.json").read_bytes()
ab = (ROOT / "blind_resources.json.gz").read_bytes()
m = json.loads(mb)
a = json.loads(gzip.decompress(ab))
assert not fields(m).intersection(FORBIDDEN)
assert set(a) == {
    "schema",
    "repository_id",
    "snapshot_id",
    "eligible_frame_identity",
    "resources",
}
assert sha(ab) == m["resource_archive"]["sha256"]
assert m["case_identity"] == "case_0004"
assert m["task_identity"] == "codex-dogfood-case-0004-repository-role-intelligence"
assert (
    sha(m["task_text"].encode())
    == "053e625127367c920e5e7d941e7f4c7ab086afaeeba9aa1cacf9c841b56c5bec"
)
assert m["schema"] == "codex-case-0004-blind-adjudication-v1"
assert a["schema"] == "codex-case-0004-blind-resources-v1"
assert m["repository_id"] == "d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8"
assert (
    m["snapshot_id"]
    == "3d994888fb7dc9cc1303b958acc0e6f6372f6e723a0791a6a0947a4acd5157ed"
)
assert (
    m["eligible_frame_identity"]
    == "80005a4a8b2a95a14018868bdc085d3339e86d3669a8c405b13e7857f48c7313"
)
for key in ("repository_id", "snapshot_id", "eligible_frame_identity"):
    assert a[key] == m[key]
resources = a["resources"]
assert len(resources) == m["eligible_resource_count"] == 498
assert all(
    set(r) == {"identity", "address", "path", "content_identity", "content"}
    for r in resources
)
by_path = {r["path"]: r for r in resources}
assert len(by_path) == 498
assert all(
    r["identity"] == "repository-resource-address:" + r["address"]
    and r["address"] == r["path"]
    for r in resources
)


def framed_digest(*values: str) -> str:
    """Verify the digest framing inspected in frozen observation.py."""
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()


assert all(
    framed_digest("decoded-utf8-text-sha256-v1", r["content"]) == r["content_identity"]
    for r in resources
)
assert (
    framed_digest(
        "explicit-required-text-resources-sha256-v1",
        m["repository_id"],
        *(value for r in resources for value in (r["address"], r["content_identity"])),
    )
    == m["snapshot_id"]
)
anchor_ids = [anchor["identity"] for anchor in m["anchors"]]
assert anchor_ids == [
    "roles",
    "ri",
    "paths",
    "configuration",
    "localization",
    "validation",
]
for anchor in m["anchors"]:
    assert anchor["provenance"]["source_identity"] == sha(m["task_text"].encode())
for ob in m["obligations"]:
    assert ob["requirement"] == "mandatory" and ob["applicability_condition"] is None
    assert ob["satisfaction"]["name"] and ob["satisfaction"]["statement"]
    assert set(ob["anchors"]) <= set(anchor_ids)
    assert ob["provenance"]["source_identity"] == sha(m["task_text"].encode())
    assert ob["provenance"]["task_phrase"] in m["task_text"]

# Execute the exact frozen production kernel in isolation. Never import the
# current devtools package or collect repository/experiment tests.
module = types.ModuleType("case0004_frozen_coverage")
sys.modules[module.__name__] = module
exec(  # noqa: S102 - exact digest-verified frozen Evaluation code, no current imports
    compile(
        by_path["src/devtools/evaluation/coverage.py"]["content"],
        "<blind:coverage.py>",
        "exec",
    ),
    module.__dict__,
)
compare = module.compare_identity_coverage
expected = [r["identity"] for r in resources]
assert compare(expected=expected, observed=expected).is_exact
probe = compare(expected=["a", "a", "b"], observed=["a", "a", "c"])
assert probe.duplicate_expected == ("a",) and probe.duplicate_observed == ("a",)
assert probe.missing == ("b",) and probe.unexpected == ("c",) and not probe.is_exact

R = "src/devtools/context/repository/"
C = "src/devtools/context/python/project_configuration/"
A = "docs/architecture/"
V = "docs/development/validation.md"
P = "pyproject.toml"
D = "docs/architecture.md"
M = "docs/documentation_map.md"
specs: dict[str, dict] = {}


def obligation(name: str, rationale: str) -> None:
    specs[name] = {
        "applicability": "APPLICABLE",
        "applicability_rationale": rationale,
        "information_units": [],
        "acceptable_witness_alternatives": [],
    }


def unit(
    ob: str,
    key: str,
    path: str,
    locator: str,
    information: str,
    necessity: str,
    category: str = "REQUIRED",
) -> str:
    entry = {
        "unit_identity": ob + ":" + key,
        "resource_identity": by_path[path]["identity"],
        "path": path,
        "locator": locator,
        "category": category,
        "information": information,
        "rationale": necessity,
    }
    if category == "REQUIRED":
        entry.update(
            {
                "inferability": "INFERABLE_AT_START",
                "later_observation": None,
                "inherent_discovery_prerequisite": None,
                "inferability_rationale": "The task names this responsibility; bounded static authority/API navigation in the frozen packet exposes the contract before implementation.",
                "stage_d_exploration_semantics": "AVOIDABLE_EXPLORATION if the later coding handoff lacks this information and the agent must discover it.",
                "required_review": {
                    "obligation": ob,
                    "exact_information": information,
                    "why_required": necessity,
                    "smaller_unit": locator,
                    "alternative_review": "Explicit all-of sets below; membership is conditional on the selected alternative, not universal file necessity.",
                    "blind_evidence_only": True,
                },
            }
        )
    specs[ob]["information_units"].append(entry)
    return entry["unit_identity"]


def alternatives(ob: str, *sets: list[str]) -> None:
    specs[ob]["acceptable_witness_alternatives"] = [
        {
            "identity": ob + ":alternative-" + str(i + 1),
            "all_of": members,
            "rationale": "Members establish complementary parts of the satisfaction criterion. Another complete set may substitute for this one.",
        }
        for i, members in enumerate(sets)
    ]


def helpful(
    ob: str, key: str, path: str, locator: str, information: str, rationale: str
) -> None:
    unit(ob, key, path, locator, information, rationale, "HELPFUL_ONLY")


obligation(
    "ri-ownership",
    "The task adds deterministic RI; existing context RI, retained snapshots and accepted Localization boundaries positively establish the required owner and separation.",
)
t = unit(
    "ri-ownership",
    "taxonomy",
    A + "taxonomy.md",
    "Repository intelligence definition, identity, derivation/coverage and capability subsections",
    "RI is qualified deterministic repository knowledge with explicit semantic dependencies and coverage, independent of model/task relevance.",
    "Semantic owner and proposition strength must be established before introducing facts; deterministic task-role predictions must not be mislabeled repository truth.",
)
b = unit(
    "ri-ownership",
    "architecture",
    D,
    "Accepted repository-intelligence semantics; Accepted repository Localization semantics",
    "Current/accepted extension ownership, native context substrate, provenance/coverage and downstream Localization separation.",
    "The current architecture establishes the supported extension boundary; source types alone cannot establish allowed cross-domain ownership.",
)
s = unit(
    "ri-ownership",
    "snapshot",
    R + "snapshot.py",
    "RepositorySnapshotId and RepositorySnapshot including OBSERVATION_SEMANTICS and resource_at",
    "Actual supported snapshot identity and exact retained occurrence access.",
    "Facts cannot bind to the existing snapshot API correctly without its real state contract.",
)
alternatives("ri-ownership", [t, b, s])
helpful(
    "ri-ownership",
    "adr2",
    A + "decisions/ADR-0002-repository-intelligence-identity-and-derivation.md",
    "Identity, derivation, coverage, capability and source-role sections",
    "Detailed semantic design rationale.",
    "Adds depth; taxonomy and current architecture already supply the necessary bounded extension constraints.",
)
helpful(
    "ri-ownership",
    "adr5",
    A + "decisions/ADR-0005-obligation-driven-repository-localization.md",
    "Ownership and reconciliation; Roles and safe negative evidence",
    "Exact path facts versus multi-label task-relative role interpretation.",
    "Clarifies rationale; the selected architecture witness already supplies the required distinction.",
)
helpful(
    "ri-ownership",
    "config",
    C + "docs/overview.md",
    "Ownership and dependencies; Provenance, identity and coverage",
    "Concrete supported RI family example.",
    "Useful implementation pattern, without defining every path extension.",
)

obligation(
    "resource-path",
    "Exact path characteristics are explicit task scope; canonical addresses, occurrences, snapshots and containment are implemented native contracts.",
)
b = unit(
    "resource-path",
    "address",
    R + "resource.py",
    "RepositoryResourceAddress, ContentIdentity and RepositoryResourceOccurrence",
    "Canonical relative POSIX addresses, components and invalid spelling rejection; separate content identity and retained occurrence.",
    "Characteristics must use the native address and occurrence/content distinctions instead of introducing parallel normalization or identity.",
)
s = unit(
    "resource-path",
    "snapshot",
    R + "snapshot.py",
    "RepositorySnapshot resources, OBSERVATION_SEMANTICS and resource_at",
    "Retained explicit state and exact-address lookup.",
    "Required to derive characteristics over supplied snapshot inputs rather than the current filesystem.",
)
c = unit(
    "resource-path",
    "containment",
    R + "observation.py",
    "observe_repository_resources and _observe_resource",
    "Finite explicit selection, canonical order, delegated normalization and root containment guard; no atomic/full-tree claim.",
    "The criterion explicitly includes containment and retention; this consumer locates existing containment ownership and prevents duplicated acquisition policy.",
)
n = unit(
    "resource-path",
    "normalization",
    "src/devtools/core/paths/resolution.py",
    "resolve_path",
    "Explicit absolute base, non-strict resolution and symlink component normalization.",
    "Completes the delegated normalization contract required by the criterion; a canonical address is not an absolute filesystem path.",
)
alternatives("resource-path", [b, s, c, n])
helpful(
    "resource-path",
    "filesystem-model",
    "src/devtools/core/paths/models.py",
    "ResolvedPath characteristic properties",
    "Absolute-path value and name/stem/suffix/suffixes vocabulary.",
    "Useful analogy; snapshot addresses can supply mechanical characteristics without an absolute path.",
)
helpful(
    "resource-path",
    "mirrored",
    "src/devtools/context/python/mirrored_paths.py",
    "derive_python_mirrored_path_correspondences and models",
    "Snapshot/content-supported path convention derivation.",
    "Useful example; this task need not implement source/test correspondence.",
)

obligation(
    "python-configuration",
    "Existing six-selector TOML declaration and observed-resolution APIs must be reused or extended to meet the task.",
)
b = unit(
    "python-configuration",
    "models",
    C + "models.py",
    "Selector, declaration/analysis, frame, alternative/assessment, target fact/resolution models and digest",
    "Native vocabulary, key/ordinal identity, explicit frames, qualified outcomes and versioned dependency identity.",
    "Integrating new facts correctly requires the actual typed identity/result contracts; independent replacements would duplicate the existing owner.",
)
s = unit(
    "python-configuration",
    "declarations",
    C + "declarations.py",
    "analyze_python_project_configuration, _at and _selector_declarations",
    "Retained tomllib parsing, six-key coverage, absent versus empty, malformed/dynamic/unsupported/entrypoint outcomes.",
    "The supported parser and coverage semantics must be preserved or explicitly extended; declared values alone cannot establish them.",
)
c = unit(
    "python-configuration",
    "resolution",
    C + "resolution.py",
    "resolve_python_project_configuration and validation/status/route helpers",
    "Exact dependencies, explicit frames, prefix/exact/module competition, bounded missing and deterministic results.",
    "The native consumer mechanism supplies complementary resolution semantics absent from declaration parsing.",
)
alternatives("python-configuration", [b, s, c])
helpful(
    "python-configuration",
    "docs",
    C + "docs/overview.md",
    "Syntax/routes and provenance/coverage",
    "Human-readable supported configuration contract.",
    "Improves interpretation; actual implementation witnesses supply the required integration mechanisms.",
)
helpful(
    "python-configuration",
    "actual",
    P,
    "project and Hatch/pytest/Coverage/mypy tables",
    "Real examples of all six selectors.",
    "Useful fixtures, but arbitrary retained configuration inputs can exercise the generic supported API.",
)
helpful(
    "python-configuration",
    "module-root",
    "src/devtools/context/python/modules/interpretation.py",
    "PythonModuleRoot and interpretation universe",
    "Explicit module/root dependencies.",
    "Useful deeper tracing; the configuration models/resolver expose the needed dependency contract for this bounded extension.",
)
helpful(
    "python-configuration",
    "lookup",
    "src/devtools/context/python/modules/lookup.py",
    "lookup_python_modules",
    "Shared exact module lookup without precedence.",
    "Confirms delegated behavior; task need not change lookup.",
)

obligation(
    "test-configuration",
    "Actual pyproject pytest declarations and recognized literal-array testpaths under explicit pytest roots positively establish supported semantics; full discovery/execution are outside their claims.",
)
b = unit(
    "test-configuration",
    "actual",
    P,
    "tool.pytest.ini_options",
    "Declared testpaths=[tests], strict options, marker and coverage invocation settings.",
    "Actual values establish what this repository declares, separately from generic recognized parser support.",
)
d = unit(
    "test-configuration",
    "documented",
    C + "docs/overview.md",
    "Syntax and routes; Provenance, identity and coverage",
    "Array testpaths, explicit root frame, strict component-prefix selection, unsupported/ambiguous/missing outcomes and no full-discovery/execution claim.",
    "Actual values are insufficient without their bounded recognized interpretation; this detailed contract supplies it.",
)
q = unit(
    "test-configuration",
    "models",
    C + "models.py",
    "PYTEST_TESTPATHS; Frame, Status, declaration and assessment models",
    "Native selector, pytest_root, anchor and qualified outcome vocabulary.",
    "The source alternative needs models to interpret parser and resolver outcomes.",
)
p = unit(
    "test-configuration",
    "parser",
    C + "declarations.py",
    "analyze_python_project_configuration and _selector_declarations",
    "Testpaths routing, array syntax and absent/empty/malformed distinctions.",
    "The source alternative must establish syntax/coverage, not merely declaration values.",
)
r = unit(
    "test-configuration",
    "resolver",
    C + "resolution.py",
    "pytest branch in _alternatives; _framed_path, _path, _status and _validate",
    "Explicit root selection, canonical literals, observed prefix/exact competition and dependency validation.",
    "The source alternative must establish interpretation and its supported limits.",
)
alternatives("test-configuration", [b, d], [b, q, p, r])
helpful(
    "test-configuration",
    "command",
    "scripts/validate_development.py",
    "pytest_arguments",
    "Protected invocation excludes experiments before collection.",
    "Helps separate declaration semantics from command-specific selection; not full pytest emulation.",
)
helpful(
    "test-configuration",
    "mirrored",
    "src/devtools/context/python/docs/overview.md",
    "Mirrored source/test paths",
    "Correspondence does not prove TESTS/COVERS/VALIDATES.",
    "Useful guard; configuration contract already excludes execution claims.",
)

obligation(
    "package-integration",
    "RI packages have responsibility-focused modules and explicit import/__all__ facades; preserving applicable conventions is expressly requested.",
)
b = unit(
    "package-integration",
    "rules",
    "AGENTS.md",
    "Inspect before inventing package paragraphs; Reuse canonical primitives; Framework/experiments/integrations",
    "Domain packages, mirrored test organization, native substrate reuse and experiments-to-framework direction.",
    "Explicit organization/dependency rules cannot be inferred completely from adjacent exports.",
)
p = unit(
    "package-integration",
    "repository",
    R + "__init__.py",
    "imports and __all__",
    "Supported repository state/resource APIs and explicit exports.",
    "A path capability added to this owner must preserve its actual public exposure convention.",
)
c = unit(
    "package-integration",
    "configuration",
    C + "__init__.py",
    "imports and __all__",
    "Public configuration models and analyze/resolve functions.",
    "Configuration extensions must preserve the actual native package API.",
)
alternatives("package-integration", [b, p, c])
helpful(
    "package-integration",
    "context",
    "src/devtools/context/__init__.py",
    "imports and __all__",
    "Broader historical context facade.",
    "Useful if changing this facade; the task does not require exporting every new capability at this level.",
)

obligation(
    "tests",
    "Strong regression tests are explicit task scope; existing configuration tests specify supported/unresolved outcomes, exact retention and reproducibility.",
)
b = unit(
    "tests",
    "regressions",
    "tests/context/python/project_configuration/test_configuration.py",
    "_snapshot/_resolve; selectors, frames/duplicates, unsupported/malformed/empty, competition, stale dependencies and ordering/identity tests",
    "Public fixture construction and existing regression expectations for provenance, bounded outcomes, stale inputs and deterministic order/identity.",
    "Extending behavior correctly requires existing regression expectations and fixture conventions. The complementary cases form the honest unit; an isolated happy-path test cannot substitute.",
)
alternatives("tests", [b])
helpful(
    "tests",
    "path",
    "tests/context/python/test_mirrored_paths.py",
    "Exact pairs, near matches, snapshots, order and duplicate tests",
    "Additional path fact test idioms.",
    "Helpful neighbors; configuration tests already supply sufficient retained-provenance and reproducibility conventions.",
)
helpful(
    "tests",
    "observation",
    "tests/context/repository/test_observation.py",
    "Identity/order/address/containment cases",
    "Native snapshot and path regression examples.",
    "Useful reference; native implementation establishes invariants and observation itself need not change.",
)

obligation(
    "documentation",
    "Architecture/development documentation is explicit scope; current authority/navigation and owning package claims must be extended consistently.",
)
b = unit(
    "documentation",
    "navigation",
    M,
    "Authority and ownership; Package documentation; Backlog navigation; Update workflow",
    "Authority and navigation for packages, architecture, validation, roadmap and backlog.",
    "Required to choose authoritative destinations and distinguish implementation claims from history/future pressure.",
)
a = unit(
    "documentation",
    "architecture",
    D,
    "Accepted RI and Localization semantics",
    "Current cross-domain ownership and bounded behavior claims.",
    "Consistent architecture documentation requires knowing the current claims to amend.",
)
c = unit(
    "documentation",
    "package",
    C + "docs/overview.md",
    "Ownership/dependencies; Syntax/routes; Provenance/coverage; Alternatives/future Retrieval",
    "Implemented configuration scope and unsupported/non-goal claims.",
    "Configuration behavior claims must be extended at their detailed owner, preserving existing qualified semantics.",
)
v = unit(
    "documentation",
    "development",
    V,
    "Protected profile and other quality gates",
    "Canonical validation contract and confirmation isolation.",
    "Requested development documentation must stay consistent with this current authoritative contract.",
)
alternatives("documentation", [b, a, c, v])
for key, path, locator, info in [
    (
        "roadmap",
        "docs/roadmap.md",
        "Repository-map checkpoint and next evidence gate",
        "Sequencing and unimplemented role/RI/navigation pressure.",
    ),
    (
        "backlog",
        "docs/backlog/epics/B-0002-coding-context-substrate.md",
        "Configuration capability evidence; Localization reconciliation",
        "Remaining Context/RI pressure and capability status.",
    ),
    (
        "runtime-config",
        "docs/backlog/items/B-0019-investigate-typed-configuration-ownership.md",
        "Problem/value and promotion trigger",
        "Deferred framework runtime configuration is a separate concern.",
    ),
    (
        "metadata",
        "docs/backlog/metadata.md",
        "Promotion discipline and dependency meanings",
        "Backlog maturity and hard/pressure/operational dependency meanings.",
    ),
    (
        "python",
        "src/devtools/context/python/docs/overview.md",
        "Configuration navigation and mirrored paths",
        "Adjacent Python package navigation.",
    ),
    (
        "localization",
        "src/devtools/context/localization/docs/overview.md",
        "Kernel and ownership paragraphs",
        "Downstream supplied-frame readiness contract.",
    ),
]:
    helpful(
        "documentation",
        key,
        path,
        locator,
        info,
        "Helpful impact-check context; map/current architecture and owning package/development documents suffice without changing sequencing or promoting backlog.",
    )

obligation(
    "validation",
    "Protected validation is explicit task scope and a canonical command/quality-gate contract with static project settings exists; future pass results are not localization witnesses.",
)
b = unit(
    "validation",
    "contract",
    V,
    "Protected development test profile; Other quality gates",
    "Protected script command; pre-collection exclusion; strict branch/100% gates; separate Ruff lint/format, mypy, diff/cached-diff checks and confirmation isolation.",
    "The exact canonical selection/check contract is necessary; default pytest does not establish protected isolation.",
)
p = unit(
    "validation",
    "settings",
    P,
    "tool.pytest.ini_options, tool.coverage, tool.ruff and tool.mypy",
    "Actual strict pytest, branch coverage, Ruff ALL/Python312 and strict mypy scopes/options.",
    "Static configuration completes the command-level contract including enforced settings and checked files.",
)
alternatives("validation", [b, p])
helpful(
    "validation",
    "script",
    "scripts/validate_development.py",
    "pytest_arguments and main",
    "Executable exclusion and return-status implementation.",
    "Confirms documented behavior; no script changes are required.",
)
helpful(
    "validation",
    "history",
    "docs/backlog/items/B-0047-protected-development-validation-profile.md",
    "Implemented contract; Scope/invariants",
    "Protected profile rationale/history.",
    "Confidence/history; current doc and actual settings suffice.",
)

obligation_ids = [o["identity"] for o in m["obligations"]]
assert list(specs) == obligation_ids and len(obligation_ids) == 8
matrix = []
for resource in resources:
    cells = {}
    for ob in obligation_ids:
        cats = {
            u["category"]
            for u in specs[ob]["information_units"]
            if u["resource_identity"] == resource["identity"]
        }
        cells[ob] = (
            "REQUIRED"
            if "REQUIRED" in cats
            else "HELPFUL_ONLY"
            if cats
            else "UNNECESSARY"
        )
    matrix.append(
        {
            "resource_identity": resource["identity"],
            "path": resource["path"],
            "dispositions": cells,
        }
    )
judgments = []
for frozen in m["obligations"]:
    ob = frozen["identity"]
    judgments.append(
        {
            "frozen_obligation": frozen,
            **specs[ob],
            "resource_counts": dict(Counter(row["dispositions"][ob] for row in matrix)),
            "information_unit_counts": dict(
                Counter(u["category"] for u in specs[ob]["information_units"])
            ),
        }
    )
coverage = asdict(
    compare(expected=expected, observed=[r["resource_identity"] for r in matrix])
)
artifact = {
    "schema": "codex-case-0004-blind-obligation-judgment-v1",
    **{
        k: m[k]
        for k in (
            "case_identity",
            "task_identity",
            "task_text",
            "purpose",
            "repository_id",
            "snapshot_id",
            "eligible_frame_identity",
        )
    },
    "shared_anchors": m["anchors"],
    "inspected_evidence": sorted(
        {u["path"] for spec in specs.values() for u in spec["information_units"]}
        | {
            "src/devtools/context/repository/document.py",
            "src/devtools/context/repository/identity.py",
            "src/devtools/evaluation/coverage.py",
            "docs/backlog/items/B-0008-investigate-repository-context-discovery.md",
        }
    ),
    "method": {
        "version": "independent-blind-static-adjudication-v1",
        "description": "Human exact-path archive inspection and bounded source/authority navigation; no task-relative acquisition/ranking or current source imports.",
        "source_universe": "blind_manifest.json and blind_resources.json.gz only",
        "identity_coverage": "Exact frozen production Evaluation coverage.py executed in isolated module.",
        "inventory_review": "Path inventory and bounded owner/contract inspection. No default relies on a claim of hard directory exclusion.",
        "session_limit": "No previous Case 0004 context used. Platform model/effort and session provenance are not independently attested by this script.",
    },
    "blind_packet_digests": {
        "blind_manifest.json": sha(mb),
        "blind_resources.json.gz": sha(ab),
        "task_text_utf8": sha(m["task_text"].encode()),
    },
    "packet_verification": {
        "identity_cross_checks": "passed",
        "resource_count": 498,
        "content_identity_digests_verified": 498,
        "snapshot_digest_recomputed": True,
        "metadata_structure": "allowlisted; no treatment/result fields",
        "opaque_frame_identity": "Equal between manifest/archive; producer construction is not supplied and is not independently recomputed.",
    },
    "category_semantics": {
        "REQUIRED": "Materially necessary information, possibly conditional on one acceptable alternative. Resource label means a required candidate unit is contained, not that every byte or every alternative file is jointly mandatory.",
        "HELPFUL_ONLY": "Improves understanding/confidence/efficiency; a sufficient admitted set can satisfy the obligation without it.",
        "UNNECESSARY": "No additional material information needed for this bounded obligation under admitted witness sets; not global irrelevance or elimination.",
        "UNRESOLVED": "Blind evidence insufficient for a defensible judgment.",
    },
    "witness_algebra": "OR over alternatives; AND over all_of members. Alternatives replace information rather than enumerate useful neighbors.",
    "matrix_semantics": "One explicit cell for every resource/obligation pair. Locators/rationales accompany non-default units. All remaining cells explicitly UNNECESSARY: unrelated owners, historical evidence or redundant detail outside the criterion. This is no universal file label.",
    "obligations": judgments,
    "resource_matrix": matrix,
    "task_interpretation_gaps": {
        "disposition": "NO_OBVIOUS_MANDATORY_GAP",
        "findings": [],
        "rationale": "Eight criteria cover ownership/non-goals, paths/snapshots, Python/test configuration, package/API integration, tests, documentation and validation. Determinism, provenance, ambiguity and no relevance/elimination/runtime claims are included. Soft routing itself, full pytest emulation, registration, persistence and learned ontology are not requested.",
    },
    "non_applicability_review": {
        "supported_non_applicable": [],
        "unresolved_applicability": [],
        "rationale": "All eight have positive task/implemented-contract evidence. Registration/full pytest discovery are bounded exclusions within applicable obligations, not absence-based non-applicability findings.",
    },
    "unresolved_judgments": [],
    "inherent_discovery": [],
    "limitations": [
        "Only eligible retained text resources are available; excluded filesystem/environment state is outside these claims.",
        "No implementation or validation execution selected; future failures/runtime surprises are not repository witnesses.",
        "Witness alternatives are defensible bounded sufficient sets, not proof of universal uniqueness or task success.",
        "Historical focused-validation examples do not supersede the canonical current protected development contract.",
    ],
    "frame_coverage": {
        "eligible_resources": 498,
        "observed_resources": len(matrix),
        "obligation_count": 8,
        "explicit_cells": len(matrix) * 8,
        "diagnostics": coverage,
        "is_exact": not any(coverage.values()),
    },
    "blindness_attestation": {
        "other_case_0004_inputs_accessed": False,
        "current_target_source_consulted": False,
        "treatment_or_result_artifacts_accessed": False,
        "stage_d_join_performed": False,
        "confirmation_accessed": False,
    },
    "artifact_digest": {
        "algorithm": "sha256",
        "scope": "Canonical UTF-8 JSON with artifact_digest omitted; sorted keys, indent=2, final LF",
        "value": "",
    },
}


def validate(value: dict) -> None:
    assert not fields(value).intersection(FORBIDDEN)
    assert [j["frozen_obligation"] for j in value["obligations"]] == m["obligations"]
    assert value["shared_anchors"] == m["anchors"]
    rows = value["resource_matrix"]
    assert compare(
        expected=expected, observed=[r["resource_identity"] for r in rows]
    ).is_exact
    assert len(rows) == 498
    for row in rows:
        assert set(row["dispositions"]) == set(obligation_ids)
        assert set(row["dispositions"].values()) <= {
            "REQUIRED",
            "HELPFUL_ONLY",
            "UNNECESSARY",
            "UNRESOLVED",
        }
        assert by_path[row["path"]]["identity"] == row["resource_identity"]
    for judgment in value["obligations"]:
        assert judgment["applicability"] in {
            "APPLICABLE",
            "SUPPORTED_NOT_APPLICABLE",
            "UNRESOLVED_APPLICABILITY",
        }
        units = judgment["information_units"]
        ids = [u["unit_identity"] for u in units]
        assert len(ids) == len(set(ids))
        resource_ids = [u["resource_identity"] for u in units]
        assert len(resource_ids) == len(set(resource_ids)), (
            "Only one grouped unit per resource/obligation in v1"
        )
        required = {u["unit_identity"] for u in units if u["category"] == "REQUIRED"}
        admitted = set()
        for alternative in judgment["acceptable_witness_alternatives"]:
            members = alternative["all_of"]
            assert (
                members
                and len(members) == len(set(members))
                and set(members) <= required
            )
            admitted.update(members)
        assert admitted == required
        for u in units:
            assert (
                u["resource_identity"] in expected
                and by_path[u["path"]]["identity"] == u["resource_identity"]
            )
            assert u["locator"] and u["information"] and u["rationale"]
            if u["category"] == "REQUIRED":
                assert (
                    u["inferability"] == "INFERABLE_AT_START"
                    and u["required_review"]["blind_evidence_only"]
                )
        ob = judgment["frozen_obligation"]["identity"]
        assert judgment["resource_counts"] == dict(
            Counter(row["dispositions"][ob] for row in rows)
        )
        assert judgment["information_unit_counts"] == dict(
            Counter(u["category"] for u in units)
        )
        for row in rows:
            cats = {
                u["category"]
                for u in units
                if u["resource_identity"] == row["resource_identity"]
            }
            category = (
                "REQUIRED"
                if "REQUIRED" in cats
                else "HELPFUL_ONLY"
                if cats
                else "UNNECESSARY"
            )
            assert row["dispositions"][ob] == category
    assert (
        value["frame_coverage"]["is_exact"]
        and value["frame_coverage"]["explicit_cells"] == 3984
    )
    assert (
        sha(canonical({k: v for k, v in value.items() if k != "artifact_digest"}))
        == value["artifact_digest"]["value"]
    )


artifact["artifact_digest"]["value"] = sha(
    canonical({k: v for k, v in artifact.items() if k != "artifact_digest"})
)
validate(artifact)
output = canonical(artifact)
target = ROOT / "blind_judgments.json"
if "--check" in sys.argv:
    assert target.read_bytes() == output, (
        "Retained judgment differs from deterministic specification"
    )
    validate(json.loads(target.read_bytes()))
else:
    target.write_bytes(output)
assert canonical(json.loads(output)) == output
print(
    json.dumps(
        {
            "artifact_sha256": sha(output),
            "payload_digest": artifact["artifact_digest"]["value"],
            "coverage": artifact["frame_coverage"],
            "counts": {
                j["frozen_obligation"]["identity"]: j["information_unit_counts"]
                for j in judgments
            },
        },
        indent=2,
    )
)

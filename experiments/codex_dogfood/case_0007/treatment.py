# Copyright (c) 2026
# ruff: noqa: E501, ISC004, S101
"""Caller-authored pre-execution interpretation, queries and recipe specifications.

This module constructs input values only. It never resolves a locator or executes
a projection. Native production recipes cannot be instantiated until Stage B.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from devtools.context.localization import (
    LocalizationAnchor,
    LocalizationAnchorIdentity,
    LocalizationObligation,
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
    LocalizationTaskIdentity,
    LocalizationTaskInterpretation,
    ObligationLexicalQuery,
    RequirementStatus,
    SatisfactionCriterion,
    TaskProvenance,
)
from devtools.context.localization.generation import ProjectionKind
from devtools.context.localization.grounding import (
    AnchorGroundingRequest,
    PythonDirectDeclarationKind,
    PythonDirectDeclarationLocator,
    PythonModuleLocator,
)
from devtools.context.localization.roles import RepositoryRoleKind
from devtools.context.localization.routing import ObligationRolePreference
from devtools.context.python.modules import PythonModuleKind

if TYPE_CHECKING:
    from devtools.context.repository.snapshot import RepositorySnapshot

CASE = "case_0007"
STARTING_HEAD = "61010e4dd00dd40c4bbb075ecac1714835ed4830"
STATUS = "FROZEN BEFORE RETRIEVAL, ROUTING, GROUNDING, GENERATION AND ADJUDICATION"
TASK = (
    "Implement the first bounded deterministic Python public-export and re-export "
    "Repository Intelligence capability for explicit module and package API surfaces. "
    "The capability should distinguish source declaration identity, import binding, "
    "package membership, and public API exposure; represent direct package-facade "
    "re-exports and statically explicit `__all__` declarations where they can be "
    "established soundly; preserve native repository/snapshot identity and provenance; "
    "retain ambiguity or abstention for dynamic or unsupported export behavior rather "
    "than overclaiming; integrate coherently with the existing Python module, "
    "declaration, import/member, package, and Reference Repository Intelligence "
    "contracts; expose a clean deterministic foundation for future Localization use "
    "without introducing a Localization generation operator in this increment; add "
    "rigorous tests and authoritative architecture/development documentation; preserve "
    "package/API conventions where applicable; and pass protected development "
    "validation. Do not implement runtime import execution, dynamic module "
    "`__getattr__` resolution, unrestricted star-import closure, inferred popularity "
    "or relevance, learned ranking, graph expansion, or automatic witness resolution."
)
PURPOSE = (
    "Acquire and generate repository information needed to implement the frozen "
    "explicit Python public-export/re-export RI capability while prospectively "
    "comparing global lexical, obligation lexical, role-routed and bounded structural "
    "witness-generation surfaces."
)
TASK_ID = LocalizationTaskIdentity("case-0007-python-public-export-ri")
PROVENANCE = TaskProvenance(
    "case-0007-verbatim-user-development-task",
    explanation=(
        "Stage A caller interpretation of the exact task and accepted public "
        "architecture; no retrieved candidates or historical gold."
    ),
)
REFERENCE_MAX_RESULTS = 16
REFERENCE_WORK_LIMIT = 4096

# Each row is predicate, shared anchors, named criterion, explicit query, soft roles.
ANCHORS = {
    "declarations": "Source declaration identity, independently of runtime binding",
    "bindings": "Import/member bindings and direct package-facade re-exports",
    "packages": "Explicit module interpretation and immediate package membership",
    "exposure": "Public API exposure and statically explicit __all__ declarations",
    "abstention": "Dynamic or unsupported exports retain ambiguity or abstention",
    "provenance": "Native repository/snapshot identity and derivation provenance",
    "references": "Integration with existing exact Reference RI contracts",
    "api": "Coherent package/API ownership and future Localization foundation",
    "verification": "Rigorous tests, authoritative documentation, protected validation",
}
OBLIGATIONS = {
    "declaration-identity": (
        "Understand native declaration identities and their separation from binding "
        "so export facts can retain canonical source subjects without runtime claims.",
        ("declarations", "provenance"),
        "native-source-identity-boundary",
        "Information establishes existing function/class subjects, occurrence and "
        "declaration provenance, including decoration and rebinding nonclaims.",
        "PythonFunctionDeclarationKnowledge PythonClassDeclarationKnowledge source "
        "declaration identity decorated binding provenance",
        ("PYTHON_CODE",),
    ),
    "binding-reexports": (
        "Understand existing import/member and direct facade resolution contracts "
        "to distinguish a declared re-export binding from source declaration identity.",
        ("bindings", "declarations"),
        "binding-and-facade-contract",
        "Information establishes exact import/member resolution, one-facade limits, "
        "competing bindings and retained resolution provenance.",
        "resolve_python_imported_member direct facade re-export import binding "
        "ambiguous unsupported declaration",
        ("PYTHON_CODE", "PACKAGE_SURFACE"),
    ),
    "module-membership": (
        "Understand explicit module/package identity and immediate membership "
        "without conflating containment, importability and public exposure.",
        ("packages", "exposure"),
        "module-and-membership-boundary",
        "Information establishes explicit-root module/package interpretations, "
        "bounded membership and missing/competing interpretations.",
        "PythonModuleInterpretation interpret_python_module_resources "
        "derive_python_immediate_package_memberships package membership public API",
        ("PYTHON_CODE", "PACKAGE_MEMBER"),
    ),
    "explicit-exposure": (
        "Determine sound static public-exposure semantics for direct facade "
        "re-exports and explicit __all__, separately from declaration and binding.",
        ("exposure", "bindings", "packages"),
        "explicit-export-semantic-foundation",
        "Information supplies accepted RI scope and static interpretation limits "
        "needed to design explicit exposure without dynamic or star-import closure.",
        "public API exposure explicit __all__ package-facade re-exports source "
        "declaration import binding package membership Repository Intelligence",
        ("DOCUMENTATION",),
    ),
    "unsupported-behavior": (
        "Understand ambiguity, abstention and coverage conventions for dynamic "
        "or unsupported syntax without asserting runtime absence.",
        ("abstention", "bindings", "exposure"),
        "qualified-static-outcomes",
        "Information establishes supported/unsupported outcome ownership and "
        "nonclaims needed for dynamic __all__, __getattr__ and competing exports.",
        "PythonImportedMemberResolution ambiguity unsupported abstention dynamic "
        "__all__ __getattr__ wildcard coverage runtime import",
        ("PYTHON_CODE", "DOCUMENTATION"),
    ),
    "snapshot-provenance": (
        "Understand repository/snapshot dependency identity and native provenance "
        "needed for deterministic export facts and replay/freshness validation.",
        ("provenance", "declarations", "packages"),
        "dependency-qualified-export-truth",
        "Information establishes canonical identity, dependency and provenance "
        "contracts and their bounded applicability/freshness requirements.",
        "RepositorySnapshot RepositorySubject SourceOccurrence Derivation "
        "PythonModuleInterpretation provenance dependency snapshot identity",
        ("PYTHON_CODE", "DOCUMENTATION"),
    ),
    "reference-integration": (
        "Understand Reference consumers and exact target resolution boundaries "
        "to integrate new export RI coherently without changing Reference truth.",
        ("references", "bindings", "declarations"),
        "reference-consumer-boundary",
        "Information establishes current Reference targets, routes and consumer "
        "contracts; export exposure remains distinct from Reference and Call syntax.",
        "derive_python_declaration_references PythonDeclarationReferenceKnowledge "
        "exact target facade import binding direct_call public export",
        ("PYTHON_CODE",),
    ),
    "package-api": (
        "Understand public Python RI package/API conventions and ownership for "
        "a deterministic foundation with no Localization operator in this increment.",
        ("api", "packages", "exposure"),
        "public-api-and-dependency-integration",
        "Information establishes package surfaces, dependency direction and public "
        "API conventions relevant to adding Python-owned export RI.",
        "Python Repository Intelligence package API public exports __init__ "
        "dependency direction Localization generation foundation",
        ("PACKAGE_SURFACE", "DOCUMENTATION"),
    ),
    "tests": (
        "Understand native RI test patterns for exact identity, bounded static "
        "resolution, ambiguity, unsupported forms and freshness regressions.",
        ("verification", "declarations", "bindings", "packages", "references"),
        "rigorous-native-ri-test-patterns",
        "Information supplies relevant fixture/assertion conventions for supported "
        "and rejected export forms and neighboring RI regressions.",
        "Python public export re-export __all__ import member package Reference "
        "declaration ambiguity unsupported snapshot provenance tests",
        ("TEST",),
    ),
    "documentation": (
        "Understand authoritative architecture/development documentation and "
        "taxonomy updates required by the new supported capability.",
        ("verification", "api", "exposure"),
        "authoritative-documentation-impact",
        "Information establishes documentation authority, architectural terminology "
        "and development update policy for the new static exposure capability.",
        "Repository Intelligence source declaration import binding public API "
        "exposure architecture taxonomy documentation authority development",
        ("DOCUMENTATION",),
    ),
    "validation": (
        "Understand protected development validation and package/API checks "
        "required to validate the future implementation without confirmation access.",
        ("verification", "api"),
        "protected-development-checks",
        "Information establishes canonical protected validation, coverage, typing, "
        "format/lint and confirmation exclusion requirements.",
        "protected development validation validate_development coverage mypy "
        "Ruff package API confirmation excluded",
        ("DOCUMENTATION", "TOOL_CONFIGURATION", "TEST_CONFIGURATION"),
    ),
}

# Exact locators from the recorded public surfaces, never source-result selection.
GROUNDINGS = {
    "g-function": (
        "declarations",
        "CLASS",
        "devtools.context.python.function.declarations",
        "PythonFunctionDeclarationKnowledge",
    ),
    "g-class": (
        "declarations",
        "CLASS",
        "devtools.context.python.classes.declarations",
        "PythonClassDeclarationKnowledge",
    ),
    "g-binding": (
        "bindings",
        "FUNCTION",
        "devtools.context.python.imports.members",
        "resolve_python_imported_member",
    ),
    "g-module": (
        "packages",
        "FUNCTION",
        "devtools.context.python.modules.interpretation",
        "interpret_python_module_resources",
    ),
    "g-membership": (
        "packages",
        "FUNCTION",
        "devtools.context.python.modules.membership",
        "derive_python_immediate_package_memberships",
    ),
    "g-module-identity": (
        "provenance",
        "CLASS",
        "devtools.context.python.modules.interpretation",
        "PythonModuleInterpretation",
    ),
    "g-reference": (
        "references",
        "FUNCTION",
        "devtools.context.python.references.declarations.analysis",
        "derive_python_declaration_references",
    ),
    "g-reference-fact": (
        "references",
        "CLASS",
        "devtools.context.python.references.declarations.model",
        "PythonDeclarationReferenceKnowledge",
    ),
    "g-python-api": ("api", "MODULE", "devtools.context.python", None),
}


def interpretation() -> LocalizationTaskInterpretation:
    """Construct caller interpretation without repository referents or witnesses."""
    return LocalizationTaskInterpretation(
        TASK_ID,
        PROVENANCE,
        tuple(
            LocalizationAnchor(
                LocalizationAnchorIdentity(TASK_ID, key),
                text,
                PROVENANCE,
            )
            for key, text in ANCHORS.items()
        ),
        tuple(
            LocalizationObligation(
                LocalizationObligationIdentity(TASK_ID, key),
                row[0],
                tuple(LocalizationAnchorIdentity(TASK_ID, item) for item in row[1]),
                PROVENANCE,
                RequirementStatus.MANDATORY,
                SatisfactionCriterion(row[2], row[3]),
                (),
            )
            for key, row in OBLIGATIONS.items()
        ),
    )


def lexical_inputs() -> tuple[
    tuple[ObligationLexicalQuery, ...],
    tuple[ObligationRolePreference, ...],
]:
    """Construct eleven query/preference bindings; global lane stays unrouted."""
    queries = tuple(
        ObligationLexicalQuery(
            LocalizationQueryIdentity(TASK_ID, f"q-{key}"),
            LocalizationObligationIdentity(TASK_ID, key),
            row[4],
        )
        for key, row in OBLIGATIONS.items()
    )
    preferences = tuple(
        ObligationRolePreference(
            query.identity,
            query.obligation,
            tuple(
                RepositoryRoleKind[name]
                for name in OBLIGATIONS[query.obligation.value][5]
            ),
        )
        for query in queries
    )
    return queries, preferences


def grounding_requests(
    snapshot: RepositorySnapshot,
) -> dict[str, AnchorGroundingRequest]:
    """Construct syntactically supported exact requests without resolving them."""
    return {
        key: AnchorGroundingRequest(
            TASK_ID,
            LocalizationAnchorIdentity(TASK_ID, anchor),
            snapshot.repository_id,
            snapshot.id,
            PythonModuleLocator(module, PythonModuleKind.PACKAGE)
            if kind == "MODULE"
            else PythonDirectDeclarationLocator(
                PythonModuleLocator(module),
                name,
                PythonDirectDeclarationKind[kind],
            ),
            PROVENANCE,
        )
        for key, (anchor, kind, module, name) in GROUNDINGS.items()
    }


def recipe_specs() -> list[dict[str, Any]]:
    """Freeze plausible candidate shapes, independently of projection outcomes."""
    specs = []

    def add(
        obligation: str,
        family: str,
        fixed: list[tuple[str, str, str, str]],
        branch: str | None = None,
    ) -> None:
        members = [
            {
                "key": key,
                "grounding_request": grounding,
                "operator": operator,
                "multiplicity": "fixed",
                "reason": reason,
            }
            for key, grounding, operator, reason in fixed
        ]
        if branch is not None:
            members.append(
                {
                    "key": "referencer",
                    "grounding_request": branch,
                    "operator": "REFERENCING_RESOURCE",
                    "multiplicity": "branching",
                    "max_results": REFERENCE_MAX_RESULTS,
                    "work_limit": REFERENCE_WORK_LIMIT,
                    "reason": "One exact referencer may supply a complementary consumer or integration contract; no sufficiency claim.",
                },
            )
        specs.append(
            {
                "obligation": obligation,
                "identity": family,
                "identity_kind": "family" if branch else "caller-hypothesis",
                "members": members,
                "provenance": PROVENANCE.explanation,
            },
        )

    def owner(obligation: str, seed: str) -> None:
        add(
            obligation,
            f"owner-{seed}",
            [
                (
                    "owner",
                    seed,
                    "OWNER_RESOURCE",
                    "The exact native owner's declaration/operation contract is a plausible information witness.",
                ),
            ],
        )

    for obligation, seeds in {
        "declaration-identity": ("g-function", "g-class"),
        "binding-reexports": ("g-binding",),
        "module-membership": ("g-module", "g-membership"),
        "unsupported-behavior": ("g-binding",),
        "snapshot-provenance": ("g-module-identity", "g-function"),
        "reference-integration": ("g-reference", "g-reference-fact"),
        "package-api": ("g-python-api",),
    }.items():
        for seed in seeds:
            owner(obligation, seed)

    for obligation, seed in (
        ("binding-reexports", "g-binding"),
        ("module-membership", "g-membership"),
        ("snapshot-provenance", "g-module"),
        ("reference-integration", "g-reference"),
    ):
        add(obligation, f"references-{seed}", [], seed)
        add(
            obligation,
            f"owner-plus-reference-{seed}",
            [
                (
                    "owner",
                    seed,
                    "OWNER_RESOURCE",
                    "An owner contract plus one exact consumer is a plausible complementary integration shape.",
                ),
            ],
            seed,
        )

    add(
        "package-api",
        "package-plus-module-consumer",
        [
            (
                "package",
                "g-python-api",
                "OWNER_RESOURCE",
                "The public Python package surface may complement one module-interpretation API consumer.",
            ),
        ],
        "g-module",
    )

    for seed in ("g-function", "g-class", "g-binding", "g-membership", "g-reference"):
        add(
            "tests",
            f"mirror-{seed}",
            [
                (
                    "test",
                    seed,
                    "MIRRORED_RESOURCE",
                    "An exact source/test naming counterpart may supply neighboring native RI fixture and assertion conventions; path correspondence does not prove test coverage.",
                ),
            ],
        )

    assert all(
        ProjectionKind[member["operator"]]
        for spec in specs
        for member in spec["members"]
    )
    return specs

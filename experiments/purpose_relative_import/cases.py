# Copyright (c) 2026
# ruff: noqa: E501, FBT001, FBT002, FBT003
"""Frozen manual needs and judgments for the purpose-relative oracle experiment."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.import_relationship_cases import import_relationship_cases


class UsefulnessJudgment(StrEnum):
    """A manual evaluation judgment, deliberately not a retrieval score."""

    USEFUL = "useful"
    NOT_USEFUL = "not-useful"
    UNJUDGED = "unjudged"


@dataclass(frozen=True, slots=True)
class ResourceJudgment:
    """One explicit, purpose-relative resource judgment and its rationale."""

    address: RepositoryResourceAddress
    judgment: UsefulnessJudgment
    rationale: str
    is_control: bool = False


@dataclass(frozen=True, slots=True)
class PurposeRelativeNeed:
    """Experiment-local configuration; not a production InformationNeed."""

    name: str
    information_need: str
    query_text: str
    judgments: tuple[ResourceJudgment, ...]
    categories: frozenset[str] = frozenset()


def _old_cases() -> tuple[PurposeRelativeNeed, ...]:
    """Adapt frozen Increment-20 judgments without changing their meanings."""
    values: list[PurposeRelativeNeed] = []
    for case in import_relationship_cases():
        useful = tuple(
            ResourceJudgment(address, UsefulnessJudgment.USEFUL, rationale)
            for address, rationale in zip(
                case.relevant_resource_addresses,
                case.relevant_rationales,
                strict=True,
            )
        )
        controls = tuple(
            ResourceJudgment(address, UsefulnessJudgment.NOT_USEFUL, rationale, True)
            for address, rationale in zip(
                case.negative_control_resource_addresses,
                case.negative_control_rationales,
                strict=True,
            )
        )
        values.append(PurposeRelativeNeed(case.name, case.query_text, case.query_text, (*useful, *controls), case.coverage_categories))
    return tuple(values)


def _judgment(address: str, judgment: UsefulnessJudgment, rationale: str, control: bool = False) -> ResourceJudgment:
    return ResourceJudgment(RepositoryResourceAddress(address), judgment, rationale, control)


_CASES = (
    *_old_cases(),
    PurposeRelativeNeed(
        "observation-safe-change",
        "Identify the implementation and tests needed to change bounded repository observation safely.",
        "How does bounded repository observation turn selected resource addresses into the snapshot's observed text resource occurrences?",
        (
            _judgment("src/devtools/context/repository/observation.py", UsefulnessJudgment.USEFUL, "Owns bounded observation and is the implementation being changed."),
            _judgment("src/devtools/context/repository/resource.py", UsefulnessJudgment.USEFUL, "Defines the resource occurrence representation emitted by observation."),
            _judgment("src/devtools/context/repository/snapshot.py", UsefulnessJudgment.USEFUL, "Defines the snapshot retaining observed occurrences."),
            _judgment("tests/context/repository/test_observation.py", UsefulnessJudgment.USEFUL, "Focused behavioral evidence for bounded observation."),
            _judgment("tests/context/repository/test_discovery.py", UsefulnessJudgment.NOT_USEFUL, "Plausible adjacent repository test, but discovery is metadata enumeration rather than observed-content behavior.", True),
        ),
        frozenset({"multi-resource", "relevant-test", "irrelevant-test"}),
    ),
    PurposeRelativeNeed(
        "import-resolution-safe-change",
        "Identify the implementation and tests required to change qualified repository import resolution without breaking declaration-grounded relation derivation.",
        "When does a qualified repository Python import resolution become a declaration-grounded resolved module-import relation?",
        (
            _judgment("src/devtools/context/python/imports/resolution.py", UsefulnessJudgment.USEFUL, "Owns qualified explicit-universe resolution."),
            _judgment("src/devtools/context/python/imports/relations.py", UsefulnessJudgment.USEFUL, "Consumes resolved outcomes to derive relations."),
            _judgment("tests/context/python/imports/test_resolution.py", UsefulnessJudgment.USEFUL, "Focused resolution behavior evidence."),
            _judgment("tests/context/python/imports/test_relations.py", UsefulnessJudgment.USEFUL, "Focused relation-derivation regression evidence."),
            _judgment("tests/context/python/imports/test_declarations.py", UsefulnessJudgment.NOT_USEFUL, "Plausibly adjacent import test, but covers syntax declaration facts rather than resolution or relation behavior.", True),
        ),
        frozenset({"multi-resource", "relevant-test", "irrelevant-test"}),
    ),
    PurposeRelativeNeed(
        "filesystem-translation-safe-change",
        "Identify the adapter, resource API, and tests needed to change filesystem read-error translation safely.",
        "How does the repository file-reading tool translate filesystem read failures into ToolInputError?",
        (
            _judgment("src/devtools/tools/filesystem.py", UsefulnessJudgment.USEFUL, "Owns Tool-boundary translation of filesystem read failures."),
            _judgment("src/devtools/resources/filesystem/__init__.py", UsefulnessJudgment.USEFUL, "Exports the resource API and typed errors consumed by the adapter."),
            _judgment("tests/tools/test_filesystem.py", UsefulnessJudgment.USEFUL, "Focused Tool adapter behavioral evidence."),
            _judgment("src/devtools/core/paths/__init__.py", UsefulnessJudgment.NOT_USEFUL, "Normalizes paths but does not define read-error translation.", True),
        ),
        frozenset({"multi-resource", "relevant-test", "cross-package-module"}),
    ),
    PurposeRelativeNeed(
        "context-disclosure-architecture",
        "Identify the accepted architectural rules governing purpose-relative Context disclosure.",
        "Context disclosure",
        (
            _judgment("docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md", UsefulnessJudgment.USEFUL, "Authoritative accepted decision for Context disclosure planning and assembly."),
            _judgment("docs/architecture.md", UsefulnessJudgment.USEFUL, "Authoritative current architecture links Context semantics and accepted ADR ownership."),
            _judgment("src/devtools/context/python/function/request_assembly.py", UsefulnessJudgment.NOT_USEFUL, "A plausible implementation distractor, but it does not establish accepted architectural rules.", True),
        ),
        frozenset({"same-query-different-purpose", "architecture-documentation", "multi-resource"}),
    ),
    PurposeRelativeNeed(
        "context-disclosure-implementation",
        "Locate the implemented exact-name Python function disclosure projection and its focused behavioral evidence.",
        "Context disclosure",
        (
            _judgment("src/devtools/context/python/function/disclosure.py", UsefulnessJudgment.USEFUL, "Implements the bounded exact-name disclosure projection."),
            _judgment("tests/context/python/function/test_disclosure.py", UsefulnessJudgment.USEFUL, "Focused behavioral evidence for that disclosure projection."),
            _judgment("src/devtools/context/python/function/rendering.py", UsefulnessJudgment.NOT_USEFUL, "Adjacent later rendering consumes materialized Context but does not implement the disclosure projection.", True),
        ),
        frozenset({"same-query-different-purpose", "implementation", "relevant-test"}),
    ),
)


def purpose_relative_needs() -> tuple[PurposeRelativeNeed, ...]:
    """Return frozen evaluation configuration without experimental work."""
    return _CASES

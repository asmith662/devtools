# Copyright (c) 2026
# ruff: noqa: E501 -- bounded case protocol
"""Caller-authored prospective task and queries, without witness selection."""

from __future__ import annotations

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

TASK = (
    "Add a bounded caller-directed line-range resource disclosure option to explicit repository Context Planning. "
    "The caller selects an observed text resource and inclusive one-based start/end lines; do not infer ranges from retrieval. "
    "Represent the choice alongside existing whole-resource and Python-qualified-reference options. "
    "Bind its deterministic identity to repository, snapshot, resource occurrence, exact content identity and bounds, "
    "preserving plan order, purpose and preceding-plan lineage. Materialize only from retained snapshot content, "
    "with explicit line boundaries and faithful UTF-8/newline handling, including empty lines, non-ASCII text and a final line without a newline. "
    "Retain exact source address, content identity, selected range and native provenance in the materialized item. "
    "Reject nonpositive, reversed or out-of-range bounds, unavailable text and foreign or stale snapshot/content frames. "
    "Preserve deterministic rendering and copied ModelRequest assembly without changing the caller task or other options. "
    "Follow public package and dependency conventions, add focused valid/invalid/boundary tests, update governing architecture "
    "and package documentation, and run protected development validation. Do not implement automatic range selection, "
    "token-budget optimization, retrieval ranking, semantic resolution, an option registry or agent execution."
)
OBLIGATIONS = (
    (
        "ownership",
        "Find the explicit planning and disclosure ownership contracts and dependency boundaries.",
        "context planning disclosure option representation ownership dependency boundary",
    ),
    (
        "range",
        "Find retained text and exact bounded line extraction semantics that the new option must respect.",
        "resource text line range start end UTF-8 newline boundaries snapshot content extraction",
    ),
    (
        "identity",
        "Find deterministic choice and plan identity, purpose, order and lineage semantics.",
        "disclosure option identity plan purpose order preceding plan lineage deterministic",
    ),
    (
        "frame",
        "Find repository snapshot resource occurrence and content identity validation contracts.",
        "repository snapshot resource occurrence content identity provenance stale foreign frame validation",
    ),
    (
        "materialization",
        "Find materialized item and source provenance contracts for realizing the caller range.",
        "materialize disclosure plan resource text native provenance content identities addresses representation",
    ),
    (
        "assembly",
        "Find deterministic rendering and copied ModelRequest assembly behavior.",
        "render context disclosure assemble model request copied task plan order",
    ),
    (
        "package",
        "Find public exports and package boundaries for adding the explicit choice.",
        "context planning public exports package option protocol materialization",
    ),
    (
        "tests",
        "Find tests and fixtures establishing disclosure extraction, frame rejection and assembly behavior.",
        "tests planning disclosure materialization invalid snapshot identity Unicode newline range boundaries",
    ),
    (
        "documentation",
        "Find governing architecture and package documentation that must describe the new representation.",
        "architecture context disclosure planning representation materialization documentation explicit caller",
    ),
    (
        "validation",
        "Find protected development validation and configuration constraints.",
        "protected development validation pytest branch coverage experimental exclusion ruff mypy configuration",
    ),
)


def task_inputs() -> tuple[
    LocalizationTaskInterpretation,
    tuple[ObligationLexicalQuery, ...],
]:
    """Use native caller identities; no accepted gold witness is supplied."""
    identity = LocalizationTaskIdentity("case-0010-line-range-disclosure")
    provenance = TaskProvenance("case-0010-prospective-caller-task")
    anchor = LocalizationAnchorIdentity(identity, "line-range-disclosure")
    obligations = tuple(
        LocalizationObligation(
            LocalizationObligationIdentity(identity, key),
            predicate,
            (anchor,),
            provenance,
            RequirementStatus.MANDATORY,
            SatisfactionCriterion(key + "-information", predicate),
            (),
            None,
        )
        for key, predicate, _ in OBLIGATIONS
    )
    queries = tuple(
        ObligationLexicalQuery(
            LocalizationQueryIdentity(identity, key + "-query"),
            ob.identity,
            text,
        )
        for ob, (key, _, text) in zip(obligations, OBLIGATIONS, strict=True)
    )
    return LocalizationTaskInterpretation(
        identity,
        provenance,
        (
            LocalizationAnchor(
                anchor,
                "caller-directed line-range disclosure",
                provenance,
            ),
        ),
        obligations,
    ), queries

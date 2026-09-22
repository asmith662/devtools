# Copyright (c) 2026
# ruff: noqa: D103, E501, FBT003, PLR2004
# mypy: disable-error-code="arg-type,attr-defined,call-overload"
"""Deterministic local tests for oracle-evaluation mechanics."""

from types import SimpleNamespace

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.import_relationship.comparison import RelationRecord
from experiments.import_relationship_cases import ImportRelationshipDirection
from experiments.purpose_relative_import.cases import (
    PurposeRelativeNeed,
    ResourceJudgment,
    UsefulnessJudgment,
)
from experiments.purpose_relative_import.comparison import (
    ImportRelationshipSurface,
    RankedLexicalSurface,
    blind_insert,
    build_consideration_universe,
    evaluate_universe,
    oracle_size_five,
)


def _address(value: str) -> RepositoryResourceAddress:
    return RepositoryResourceAddress(value)


def _need() -> PurposeRelativeNeed:
    return PurposeRelativeNeed(
        "fixture",
        "purpose",
        "query",
        (
            ResourceJudgment(_address("lexical.py"), UsefulnessJudgment.USEFUL, "useful lexical"),
            ResourceJudgment(_address("relation.py"), UsefulnessJudgment.USEFUL, "useful relation"),
            ResourceJudgment(_address("control.py"), UsefulnessJudgment.NOT_USEFUL, "control", True),
        ),
    )


def _relation(source: str, target: str, identity: str) -> RelationRecord:
    return RelationRecord(
        identity,
        SimpleNamespace(resource=SimpleNamespace(address=_address(source)), identity=source),
        SimpleNamespace(declaration_ordinal=1),
        SimpleNamespace(outcome=SimpleNamespace(value="resolved")),
        SimpleNamespace(resource=SimpleNamespace(address=_address(target)), identity=target),
    )


def test_multiple_typed_surfaces_group_without_erasing_direction_or_support() -> None:
    lexical = (RankedLexicalSurface(_address("lexical.py"), 1, 4.0),)
    first = _relation("seed.py", "relation.py", "one")
    second = _relation("seed.py", "relation.py", "two")
    surfaces = (
        ImportRelationshipSurface(_address("relation.py"), _address("seed.py"), 1, ImportRelationshipDirection.OUTGOING, first),
        ImportRelationshipSurface(_address("relation.py"), _address("seed.py"), 1, ImportRelationshipDirection.INCOMING, second),
    )

    grouped = build_consideration_universe(lexical=lexical, relations=surfaces)

    assert len(grouped[_address("relation.py")]["relationships"]) == 2
    assert {item.direction for item in grouped[_address("relation.py")]["relationships"]} == {ImportRelationshipDirection.OUTGOING, ImportRelationshipDirection.INCOMING}


def test_oracle_uses_frozen_judgments_only_after_universe_and_keeps_unjudged_distinct() -> None:
    need = _need()
    universe = build_consideration_universe(
        lexical=(RankedLexicalSurface(_address("lexical.py"), 1, 1.0),),
        relations=(ImportRelationshipSurface(_address("relation.py"), _address("seed.py"), 1, ImportRelationshipDirection.OUTGOING, _relation("seed.py", "relation.py", "support")),),
    )
    universe[_address("unknown.py")] = {"lexical": [], "relationships": []}

    coverage = evaluate_universe(need=need, universe=universe, canonical=(_address("lexical.py"),), lexical_top_15=(_address("lexical.py"),))
    oracle = oracle_size_five(need=need, universe=universe)

    assert coverage["candidate_recall"] == 1.0
    assert coverage["unjudged_present"] == (_address("unknown.py"),)
    assert set(oracle["useful_admitted"]) == {_address("lexical.py"), _address("relation.py")}


def test_blind_insertion_is_fixed_and_can_displace_lexical_resources() -> None:
    canonical = tuple(_address(f"l{number}.py") for number in range(1, 6))
    inserted = blind_insert(canonical=canonical, relationship_surfaces=(ImportRelationshipSurface(_address("control.py"), _address("l1.py"), 1, ImportRelationshipDirection.OUTGOING, _relation("l1.py", "control.py", "support")),))

    assert inserted == (_address("l1.py"), _address("control.py"), _address("l2.py"), _address("l3.py"), _address("l4.py"))

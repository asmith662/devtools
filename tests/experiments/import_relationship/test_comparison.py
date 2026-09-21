# Copyright (c) 2026
# ruff: noqa: D103, E501, PLR2004
# mypy: disable-error-code="arg-type,attr-defined,dict-item,index"
"""Deterministic mechanics tests for import-relationship comparison."""

from types import SimpleNamespace

import pytest

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.import_relationship.comparison import (
    Candidate,
    RelationRecord,
    expand_candidates,
    fixed_k,
)
from experiments.import_relationship_cases import ImportRelationshipDirection


def _interpretation(address: str, identity: str) -> object:
    return SimpleNamespace(resource=SimpleNamespace(address=RepositoryResourceAddress(address)), identity=identity)


def _relation(source: object, target: object, identity: str) -> RelationRecord:
    return RelationRecord(identity, source, object(), object(), target)


def test_outgoing_and_incoming_are_distinct_and_supports_are_retained() -> None:
    seed = _interpretation("seed.py", "seed")
    target = _interpretation("target.py", "target")
    other = _interpretation("other.py", "other")
    first = _relation(seed, target, "first")
    second = _relation(seed, target, "second")
    incoming = _relation(other, seed, "incoming")
    mapping = {RepositoryResourceAddress("seed.py"): (seed,)}

    participation, outgoing = expand_candidates(lexical_seeds=(RepositoryResourceAddress("seed.py"),), interpretations_by_address=mapping, relations=(first, second, incoming), direction=ImportRelationshipDirection.OUTGOING)
    _incoming_participation, incoming_candidates = expand_candidates(lexical_seeds=(RepositoryResourceAddress("seed.py"),), interpretations_by_address=mapping, relations=(first, second, incoming), direction=ImportRelationshipDirection.INCOMING)

    assert participation[0]["relation_count"] == 2
    assert outgoing == (Candidate(RepositoryResourceAddress("target.py"), (first, second)),)
    assert incoming_candidates == (Candidate(RepositoryResourceAddress("other.py"), (incoming,)),)


def test_seed_three_and_nonparticipation_preserve_candidate_evidence() -> None:
    first = _interpretation("first.py", "first")
    third = _interpretation("third.py", "third")
    target = _interpretation("target.py", "target")
    relation = _relation(third, target, "third-support")
    participation, candidates = expand_candidates(lexical_seeds=(RepositoryResourceAddress("first.py"), RepositoryResourceAddress("missing.md"), RepositoryResourceAddress("third.py")), interpretations_by_address={RepositoryResourceAddress("first.py"): (first,), RepositoryResourceAddress("third.py"): (third,)}, relations=(relation,), direction=ImportRelationshipDirection.OUTGOING)

    assert [item["status"] for item in participation] == ["available", "missing", "available"]
    assert candidates[0].address == RepositoryResourceAddress("target.py")


def test_fixed_k_preserves_rank_one_and_records_relation_insertion_shape() -> None:
    lexical = tuple(RepositoryResourceAddress(f"l{index}.py") for index in range(1, 6))
    fixed = fixed_k(lexical=lexical, additions=(RepositoryResourceAddress("new.py"), RepositoryResourceAddress("l2.py")))

    assert fixed == (RepositoryResourceAddress("l1.py"), RepositoryResourceAddress("new.py"), RepositoryResourceAddress("l2.py"), RepositoryResourceAddress("l3.py"), RepositoryResourceAddress("l4.py"))
    assert lexical == tuple(RepositoryResourceAddress(f"l{index}.py") for index in range(1, 6))


def test_candidate_projection_performs_no_parsing_resolution_or_acquisition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Expansion consumes supplied relation evidence without invoking a pipeline."""
    def fail(*_args: object, **_kwargs: object) -> None:
        message = "Candidate projection must not acquire or derive evidence."
        raise AssertionError(message)

    monkeypatch.setattr(
        "devtools.context.python.imports.declarations.derive_python_import_declarations",
        fail,
    )
    monkeypatch.setattr(
        "devtools.context.python.imports.resolution.resolve_python_import_declaration",
        fail,
    )
    monkeypatch.setattr(
        "devtools.context.repository.observation.observe_repository_resources",
        fail,
    )
    seed = _interpretation("seed.py", "seed")
    target = _interpretation("target.py", "target")
    relation = _relation(seed, target, "support")

    _participation, candidates = expand_candidates(
        lexical_seeds=(RepositoryResourceAddress("seed.py"),),
        interpretations_by_address={RepositoryResourceAddress("seed.py"): (seed,)},
        relations=(relation,),
        direction=ImportRelationshipDirection.OUTGOING,
    )

    assert candidates[0].address == RepositoryResourceAddress("target.py")

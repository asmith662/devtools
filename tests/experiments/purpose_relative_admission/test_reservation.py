# Copyright (c) 2026
# ruff: noqa: D103, E501, I001, PLC0415, PLR2004
# mypy: disable-error-code="arg-type"
"""Controlled synthetic falsification tests for directional reservation v1."""

from devtools.context.repository.resource import RepositoryResourceAddress
from types import SimpleNamespace
from experiments.import_relationship_cases import ImportRelationshipDirection
from experiments.purpose_relative_admission.design import PurposeProfile
from experiments.purpose_relative_admission.reservation import (
    AdmissionDisposition,
    AbstentionReason,
    RelationshipSurface,
    apply_directional_reservation_v1,
    retain_relationship_targets,
)
from experiments.purpose_relative_admission.surfaces import (
    canonical_lexical_top_five,
    construct_relationship_surfaces,
)


def _address(value: str) -> RepositoryResourceAddress:
    return RepositoryResourceAddress(value)


def _lexical() -> tuple[RepositoryResourceAddress, ...]:
    return tuple(_address(f"l{number}.py") for number in range(1, 6))


def _surface(target: str, relation: str, ordinal: int, *, direction: ImportRelationshipDirection = ImportRelationshipDirection.OUTGOING, seed_rank: int = 1) -> RelationshipSurface:
    return RelationshipSurface(_address(target), direction, _address(f"seed{seed_rank}.py"), seed_rank, relation, ordinal)


def test_local_profile_always_explicitly_abstains() -> None:
    result = apply_directional_reservation_v1(profile=PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE, canonical_lexical_top_five=_lexical(), surfaces=(_surface("target.py", "a", 1), _surface("target.py", "b", 2)))

    assert result.disposition is AdmissionDisposition.ABSTAINED
    assert result.abstention_reason is AbstentionReason.LOCAL_PROFILE
    assert result.addresses == _lexical()


def test_direction_profiles_never_consume_opposite_direction() -> None:
    incoming = (_surface("incoming.py", "a", 1, direction=ImportRelationshipDirection.INCOMING), _surface("incoming.py", "b", 2, direction=ImportRelationshipDirection.INCOMING))
    outgoing = (_surface("outgoing.py", "a", 1), _surface("outgoing.py", "b", 2))

    assert apply_directional_reservation_v1(profile=PurposeProfile.OUTGOING_DEPENDENCY, canonical_lexical_top_five=_lexical(), surfaces=incoming).disposition is AdmissionDisposition.ABSTAINED
    assert apply_directional_reservation_v1(profile=PurposeProfile.INCOMING_CONSUMER_OR_TEST, canonical_lexical_top_five=_lexical(), surfaces=outgoing).disposition is AdmissionDisposition.ABSTAINED


def test_support_threshold_counts_distinct_relations_not_duplicate_encounters() -> None:
    duplicate = (_surface("target.py", "one", 1), _surface("target.py", "one", 2, seed_rank=2))
    distinct = (*duplicate, _surface("target.py", "two", 3, seed_rank=3))

    retained = retain_relationship_targets(surfaces=duplicate, direction=ImportRelationshipDirection.OUTGOING)
    assert retained[0].support_count == 1
    assert len(retained[0].encounters) == 2
    assert apply_directional_reservation_v1(profile=PurposeProfile.OUTGOING_DEPENDENCY, canonical_lexical_top_five=_lexical(), surfaces=duplicate).disposition is AdmissionDisposition.ABSTAINED
    assert apply_directional_reservation_v1(profile=PurposeProfile.OUTGOING_DEPENDENCY, canonical_lexical_top_five=_lexical(), surfaces=distinct).addresses[-1] == _address("target.py")


def test_qualifier_replaces_only_rank_five_and_already_lexical_target_is_ignored() -> None:
    surfaces = (
        _surface("l3.py", "already-one", 1), _surface("l3.py", "already-two", 2),
        _surface("target.py", "target-one", 3, seed_rank=2), _surface("target.py", "target-two", 4, seed_rank=3),
    )
    result = apply_directional_reservation_v1(profile=PurposeProfile.OUTGOING_DEPENDENCY, canonical_lexical_top_five=_lexical(), surfaces=surfaces)

    assert result.addresses[:4] == _lexical()[:4]
    assert result.addresses[-1] == _address("target.py")
    assert result.admitted_target is not None
    assert result.admitted_target.support_count == 2


def test_abstention_and_deterministic_tie_order_are_explicit() -> None:
    no_target = apply_directional_reservation_v1(profile=PurposeProfile.OUTGOING_DEPENDENCY, canonical_lexical_top_five=_lexical(), surfaces=(_surface("single.py", "one", 1),))
    tied = (
        _surface("z.py", "z1", 20, seed_rank=2), _surface("z.py", "z2", 21, seed_rank=2),
        _surface("a.py", "a1", 10, seed_rank=2), _surface("a.py", "a2", 11, seed_rank=2),
    )
    chosen = apply_directional_reservation_v1(profile=PurposeProfile.OUTGOING_DEPENDENCY, canonical_lexical_top_five=_lexical(), surfaces=tied)

    assert no_target.disposition is AdmissionDisposition.ABSTAINED
    assert no_target.abstention_reason is AbstentionReason.NO_QUALIFYING_TARGET
    assert chosen.addresses[-1] == _address("a.py")


def test_more_than_one_qualifier_still_admits_only_one_and_never_uses_judgments() -> None:
    surfaces = (
        _surface("first.py", "f1", 1), _surface("first.py", "f2", 2),
        _surface("second.py", "s1", 3), _surface("second.py", "s2", 4),
    )
    result = apply_directional_reservation_v1(profile=PurposeProfile.OUTGOING_DEPENDENCY, canonical_lexical_top_five=_lexical(), surfaces=surfaces)

    assert result.disposition is AdmissionDisposition.ADMITTED
    assert result.addresses.count(_address("first.py")) == 1
    assert result.addresses.count(_address("second.py")) == 0


def test_canonical_surface_helper_retains_only_first_five_lexical_addresses() -> None:
    from experiments.purpose_relative_import.comparison import RankedLexicalSurface

    lexical = tuple(RankedLexicalSurface(_address(f"l{number}.py"), number, 1.0) for number in range(1, 7))

    assert canonical_lexical_top_five(lexical=lexical) == _lexical()


def test_surface_adapter_retains_duplicate_encounters_for_later_unique_support_count() -> None:
    from experiments.purpose_relative_import.comparison import ImportRelationshipSurface

    source = (
        ImportRelationshipSurface(_address("target.py"), _address("seed.py"), 1, ImportRelationshipDirection.OUTGOING, SimpleNamespace(identity="one")),
        ImportRelationshipSurface(_address("target.py"), _address("seed.py"), 2, ImportRelationshipDirection.OUTGOING, SimpleNamespace(identity="one")),
        ImportRelationshipSurface(_address("target.py"), _address("seed.py"), 3, ImportRelationshipDirection.OUTGOING, SimpleNamespace(identity="two")),
    )

    adapted = construct_relationship_surfaces(surfaces=source)
    retained = retain_relationship_targets(surfaces=adapted, direction=ImportRelationshipDirection.OUTGOING)

    assert len(adapted) == 3
    assert len(retained[0].encounters) == 3
    assert retained[0].support_count == 2

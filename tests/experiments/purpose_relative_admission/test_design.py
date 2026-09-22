# Copyright (c) 2026
# ruff: noqa: D103, E501, I001, PLR2004
"""Freeze the supplied Increment-22 case split and rule fingerprint."""

from experiments.purpose_relative_admission.design import (
    ExperimentPartition,
    PurposeProfile,
    directional_reservation_v1_fingerprint,
    direct_resolution_controls,
    frozen_admission_cases,
)
from experiments.purpose_relative_admission.reservation import (
    RelationshipSurface,
    apply_directional_reservation_v1,
)
from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.import_relationship_cases import ImportRelationshipDirection


def test_frozen_design_has_exact_partition_profile_and_controls() -> None:
    cases = frozen_admission_cases()

    assert [case.need.name for case in cases] == [
        "filename-field-fusion", "resolution-becomes-relation",
        "lexical-span-semantics-without-expansion", "filesystem-tool-error-translation",
        "observation-resource-snapshot-flow", "public-relation-tests",
        "relation-source-availability", "observation-safe-change",
        "import-resolution-safe-change", "filesystem-translation-safe-change",
        "context-disclosure-architecture", "context-disclosure-implementation",
    ]
    assert [case.partition for case in cases].count(ExperimentPartition.CALIBRATION) == 4
    assert [case.partition for case in cases].count(ExperimentPartition.HELD_OUT) == 8
    assert cases[-2].profile is PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE
    assert cases[-1].profile is PurposeProfile.INCOMING_CONSUMER_OR_TEST
    assert directional_reservation_v1_fingerprint() == "7e215ac2961a4329074e9a25d35d3decc554f394435aa0b73cb2251254160345"
    assert len(direct_resolution_controls()) == 2


def test_same_query_pair_has_precommitted_profiles_and_different_admission_behavior() -> None:
    architecture, implementation = frozen_admission_cases()[-2:]
    lexical = tuple(RepositoryResourceAddress(f"l{number}.py") for number in range(1, 6))
    surfaces = (
        RelationshipSurface(RepositoryResourceAddress("target.py"), ImportRelationshipDirection.INCOMING, RepositoryResourceAddress("seed.py"), 1, "one", 1),
        RelationshipSurface(RepositoryResourceAddress("target.py"), ImportRelationshipDirection.INCOMING, RepositoryResourceAddress("seed.py"), 2, "two", 2),
    )

    assert architecture.need.query_text == implementation.need.query_text
    assert apply_directional_reservation_v1(profile=architecture.profile, canonical_lexical_top_five=lexical, surfaces=surfaces).addresses == lexical
    assert apply_directional_reservation_v1(profile=implementation.profile, canonical_lexical_top_five=lexical, surfaces=surfaces).addresses[-1] == RepositoryResourceAddress("target.py")

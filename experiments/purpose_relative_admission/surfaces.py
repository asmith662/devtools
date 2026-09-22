# Copyright (c) 2026
# ruff: noqa: I001, TC001
"""Adapt existing lexical/import experiment evidence without evaluating judgments."""

from __future__ import annotations

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.purpose_relative_import.comparison import (
    ImportRelationshipSurface,
    RankedLexicalSurface,
)
from experiments.purpose_relative_admission.reservation import RelationshipSurface

_SEED_WIDTH = 3


def canonical_lexical_top_five(
    *,
    lexical: tuple[RankedLexicalSurface, ...],
) -> tuple[RepositoryResourceAddress, ...]:
    """Retain canonical lexical addresses unchanged for the reserved-slot rule."""
    return tuple(surface.address for surface in lexical[:5])


def construct_relationship_surfaces(
    *,
    surfaces: tuple[ImportRelationshipSurface, ...],
) -> tuple[RelationshipSurface, ...]:
    """Preserve one encounter per supplied relation projection from seeds one to three.

    This function has no need, judgment, control, admission, or ranking input.
    Relation identity comes from the underlying declaration-grounded qualified
    relation record; later deduplication deliberately uses that identity.
    """
    values: list[RelationshipSurface] = []
    for encounter_ordinal, surface in enumerate(surfaces, start=1):
        if surface.seed_rank > _SEED_WIDTH:
            continue
        values.append(
            RelationshipSurface(
                address=surface.address,
                direction=surface.direction,
                seed_address=surface.seed,
                seed_rank=surface.seed_rank,
                relation_identity=surface.relation.identity,
                encounter_ordinal=encounter_ordinal,
            ),
        )
    return tuple(values)

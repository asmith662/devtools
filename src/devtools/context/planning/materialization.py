# Copyright (c) 2026
"""Faithful realization of explicitly planned repository information."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.planning.plan import _digest

if TYPE_CHECKING:
    from devtools.context.planning.plan import DisclosurePlan
    from devtools.context.repository.resource import (
        ContentIdentity,
        RepositoryResourceAddress,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot


class DisclosureMaterializationError(ValueError):
    """Reject a plan or option incompatible with supplied repository state."""


@dataclass(frozen=True, slots=True)
class MaterializedDisclosureItem:
    """Keep rendered information separate from its native supporting value."""

    option_identity: str
    representation: str
    resource_addresses: tuple[RepositoryResourceAddress, ...]
    content_identities: tuple[ContentIdentity, ...]
    text: str
    native_provenance: object


@dataclass(frozen=True, slots=True)
class ContextDisclosure:
    """Retain one realized item per ordered plan choice."""

    plan: DisclosurePlan
    items: tuple[MaterializedDisclosureItem, ...]

    def __post_init__(self) -> None:
        """Keep the realized account aligned with its explicit plan."""
        if len(self.items) != len(self.plan.disclosures) or any(
            item.option_identity != option.identity
            or item.representation != option.representation
            for item, option in zip(self.items, self.plan.disclosures, strict=True)
        ):
            msg = "Context disclosure items do not match their planned choices."
            raise DisclosureMaterializationError(msg)

    @property
    def identity(self) -> str:
        """Identify exact realized text and source identities under the plan."""
        return _digest(
            "materialized-repository-context-disclosure-v1",
            self.plan.identity,
            *(
                value
                for item in self.items
                for value in (
                    item.option_identity,
                    item.representation,
                    *(str(address) for address in item.resource_addresses),
                    *(str(content) for content in item.content_identities),
                    item.text,
                )
            ),
        )


def materialize_disclosure_plan(
    *,
    plan: DisclosurePlan,
    snapshot: RepositorySnapshot,
) -> ContextDisclosure:
    """Realize every choice against retained state, without reacquisition."""
    if snapshot.id != plan.snapshot_id or snapshot.repository_id != plan.repository_id:
        msg = "Disclosure plan does not apply to the supplied repository snapshot."
        raise DisclosureMaterializationError(msg)
    items: list[MaterializedDisclosureItem] = []
    for option in plan.disclosures:
        item = option.materialize(snapshot)
        if (
            item.option_identity != option.identity
            or item.representation != option.representation
        ):
            msg = "Materialized item differs from its planned disclosure."
            raise DisclosureMaterializationError(msg)
        items.append(item)
    return ContextDisclosure(plan=plan, items=tuple(items))

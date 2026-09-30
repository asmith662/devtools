# Copyright (c) 2026
"""Adapt one qualified Python Reference disclosure to a common plan."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.planning.materialization import MaterializedDisclosureItem
from devtools.context.python.function.qualified_reference import (
    PythonQualifiedReferenceDisclosure,
    disclose_python_qualified_reference,
    materialize_python_qualified_reference_source,
    render_python_qualified_reference_context,
)

if TYPE_CHECKING:
    from devtools.context.python.references import (
        PythonFunctionReferenceAnalysis,
        PythonFunctionReferenceKnowledge,
    )
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )


@dataclass(frozen=True, slots=True)
class PythonQualifiedReferenceDisclosureOption:
    """Choose the existing relationship-plus-exact-source representation."""

    disclosure: PythonQualifiedReferenceDisclosure

    representation: ClassVar[str] = "qualified-python-reference-and-target-v1"

    @property
    def purpose(self) -> str:
        """Return the caller's explicit information purpose."""
        return self.disclosure.purpose

    @property
    def snapshot_id(self) -> RepositorySnapshotId:
        """Return the reference derivation's snapshot identity."""
        return self.disclosure.analysis.derivation.dependency.snapshot_id

    @property
    def repository_id(self) -> RepositoryId:
        """Return the reference derivation's repository identity."""
        return self.disclosure.analysis.derivation.dependency.repository_id

    @property
    def identity(self) -> str:
        """Retain the existing fact, derivation, and caller-purpose identity."""
        return self.disclosure.identity

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Use the existing fully validated Python-specific materializer."""
        materialized = materialize_python_qualified_reference_source(
            disclosure=self.disclosure,
            snapshot=snapshot,
        )
        rendered = render_python_qualified_reference_context(materialized)
        reference = self.disclosure.reference
        return MaterializedDisclosureItem(
            option_identity=self.identity,
            representation=self.representation,
            resource_addresses=(
                reference.occurrence.resource_address,
                reference.target_declaration.support.resource_address,
            ),
            content_identities=(
                materialized.source_content_identity,
                materialized.target_content_identity,
            ),
            text=rendered.text,
            native_provenance=materialized,
        )


def choose_python_qualified_reference_disclosure(
    *,
    purpose: str,
    analysis: PythonFunctionReferenceAnalysis,
    reference: PythonFunctionReferenceKnowledge,
) -> PythonQualifiedReferenceDisclosureOption:
    """Record an exact caller choice without discovering or ranking facts."""
    return PythonQualifiedReferenceDisclosureOption(
        disclose_python_qualified_reference(
            purpose=purpose,
            analysis=analysis,
            reference=reference,
        ),
    )

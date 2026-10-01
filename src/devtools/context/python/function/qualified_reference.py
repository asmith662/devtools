# Copyright (c) 2026
"""Explicit, source-faithful Context for one qualified Python reference."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, ClassVar

from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKnowledge,
    PythonModuleResourceDependency,
)
from devtools.context.python.function.materialization import _extract_source_segment
from devtools.context.python.references.declarations.model import (
    PythonDeclarationReferenceRoute,
)
from devtools.models.interaction import ModelRequest, Prompt

if TYPE_CHECKING:
    from devtools.context.python.function.declarations import PythonSourceRange
    from devtools.context.python.references import (
        PythonDeclarationReferenceAnalysis,
        PythonDeclarationReferenceKnowledge,
    )
    from devtools.context.repository.resource import (
        ContentIdentity,
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )


class PythonQualifiedReferenceDisclosureError(ValueError):
    """Reject a fact or source state that cannot be disclosed faithfully."""


@dataclass(frozen=True, slots=True)
class PythonQualifiedReferenceDisclosure:
    """Retain a caller's purpose and exact choice of one established fact."""

    purpose: str
    analysis: PythonDeclarationReferenceAnalysis
    reference: PythonDeclarationReferenceKnowledge

    SEMANTICS: ClassVar[str] = "explicit-qualified-python-reference-disclosure-v1"

    @property
    def identity(self) -> str:
        """Identify the purpose, derivation, and selected fact."""
        return _digest(
            self.SEMANTICS,
            self.purpose,
            self.analysis.derivation.identity,
            self.reference.identity,
        )


@dataclass(frozen=True, slots=True)
class MaterializedPythonQualifiedReferenceContext:
    """Retain exact observed source for a selected relationship and target."""

    disclosure: PythonQualifiedReferenceDisclosure
    snapshot_id: RepositorySnapshotId
    source_content_identity: ContentIdentity
    target_content_identity: ContentIdentity
    reference_name_text: str
    target_declaration_text: str

    @property
    def identity(self) -> str:
        """Identify the exact source realization of this disclosure."""
        return _digest(
            "materialized-qualified-python-reference-v1",
            self.disclosure.identity,
            str(self.snapshot_id),
            str(self.source_content_identity),
            str(self.target_content_identity),
            self.reference_name_text,
            self.target_declaration_text,
        )


@dataclass(frozen=True, slots=True)
class RenderedPythonQualifiedReferenceContext:
    """Retain model-facing text and the materialized information behind it."""

    materialized_context: MaterializedPythonQualifiedReferenceContext
    text: str


def disclose_python_qualified_reference(
    *,
    purpose: str,
    analysis: PythonDeclarationReferenceAnalysis,
    reference: PythonDeclarationReferenceKnowledge,
) -> PythonQualifiedReferenceDisclosure:
    """Fix one caller-chosen fact; do not search for or choose another fact."""
    if not purpose.strip():
        msg = "Qualified reference disclosure purpose must not be blank."
        raise PythonQualifiedReferenceDisclosureError(msg)
    if (
        reference.derivation_identity != analysis.derivation.identity
        or analysis.coverage.derivation_identity != analysis.derivation.identity
        or reference not in analysis.references
    ):
        msg = "Selected reference does not belong to the supplied analysis."
        raise PythonQualifiedReferenceDisclosureError(msg)
    if not isinstance(
        reference.target_declaration,
        PythonFunctionDeclarationKnowledge,
    ) or reference.route not in {
        PythonDeclarationReferenceRoute.IMPORTED_MEMBER,
        PythonDeclarationReferenceRoute.ONE_FACADE,
    }:
        msg = "Qualified function Context requires an imported function Name."
        raise PythonQualifiedReferenceDisclosureError(msg)
    return PythonQualifiedReferenceDisclosure(purpose, analysis, reference)


def materialize_python_qualified_reference_source(
    *,
    disclosure: PythonQualifiedReferenceDisclosure,
    snapshot: RepositorySnapshot,
) -> MaterializedPythonQualifiedReferenceContext:
    """Validate both dependencies and extract only the recorded source spans."""
    # Recheck membership because immutable values can still be constructed directly.
    selected = disclose_python_qualified_reference(
        purpose=disclosure.purpose,
        analysis=disclosure.analysis,
        reference=disclosure.reference,
    )
    reference = selected.reference
    dependency = selected.analysis.derivation.dependency
    target = reference.target_declaration
    if not isinstance(target, PythonFunctionDeclarationKnowledge):
        msg = "Qualified Reference target is not a supported function."
        raise PythonQualifiedReferenceDisclosureError(msg)
    if (
        dependency.snapshot_id != snapshot.id
        or dependency.repository_id != snapshot.repository_id
        or reference.occurrence.snapshot_id != snapshot.id
        or reference.occurrence.resource_address != dependency.resource.address
    ):
        msg = "Reference source dependency does not match the supplied snapshot."
        raise PythonQualifiedReferenceDisclosureError(msg)
    source_resource = _snapshot_resource(
        snapshot,
        reference.occurrence.resource_address,
        label="source",
    )
    if source_resource != dependency.resource:
        msg = "Reference source content differs from its derivation dependency."
        raise PythonQualifiedReferenceDisclosureError(msg)

    if (
        target.support.snapshot_id != snapshot.id
        or target.subject.snapshot_id != snapshot.id
    ):
        msg = "Target declaration belongs to another snapshot."
        raise PythonQualifiedReferenceDisclosureError(msg)
    target_resource = _snapshot_resource(
        snapshot,
        target.support.resource_address,
        label="target",
    )
    target_dependency = PythonModuleResourceDependency(
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=target_resource,
    )
    if target.subject.resource_dependency_identity != target_dependency.identity:
        msg = "Target declaration resource or content differs from its dependency."
        raise PythonQualifiedReferenceDisclosureError(msg)
    if target_resource != reference.target_resource:
        msg = "Target resource differs from the retained Reference support."
        raise PythonQualifiedReferenceDisclosureError(msg)
    supporting_interpretation = (
        reference.direct_member_resolution.module
        if reference.route is PythonDeclarationReferenceRoute.IMPORTED_MEMBER
        and reference.direct_member_resolution is not None
        else reference.imported_member_resolution.target
        if reference.imported_member_resolution is not None
        else None
    )
    if (
        supporting_interpretation is None
        or supporting_interpretation.snapshot_id != snapshot.id
        or supporting_interpretation.repository_id != snapshot.repository_id
        or supporting_interpretation.resource != target_resource
    ):
        msg = "Target declaration differs from its qualified resolution support."
        raise PythonQualifiedReferenceDisclosureError(msg)
    target_analysis = (
        reference.direct_member_resolution.function_analysis
        if reference.route is PythonDeclarationReferenceRoute.IMPORTED_MEMBER
        and reference.direct_member_resolution is not None
        else reference.imported_member_resolution.target_function_analysis
        if reference.imported_member_resolution is not None
        else None
    )
    if target_analysis is not None and (
        target not in target_analysis.declarations
        or target_analysis.derivation.dependency.snapshot_id != snapshot.id
        or target_analysis.derivation.dependency.repository_id != snapshot.repository_id
        or target_analysis.derivation.dependency.resource != target_resource
    ):
        msg = "Target declaration differs from its retained declaration analysis."
        raise PythonQualifiedReferenceDisclosureError(msg)

    return MaterializedPythonQualifiedReferenceContext(
        disclosure=selected,
        snapshot_id=snapshot.id,
        source_content_identity=source_resource.content_identity,
        target_content_identity=target_resource.content_identity,
        reference_name_text=_extract_source_segment(
            source_resource.content,
            reference.occurrence.source_range,
        ),
        target_declaration_text=_extract_source_segment(
            target_resource.content,
            target.support.source_range,
        ),
    )


def render_python_qualified_reference_context(
    context: MaterializedPythonQualifiedReferenceContext,
) -> RenderedPythonQualifiedReferenceContext:
    """Render the established relationship separately from exact source text."""
    reference = context.disclosure.reference
    target = reference.target_declaration
    if not isinstance(target, PythonFunctionDeclarationKnowledge):
        msg = "Qualified Reference target is not a supported function."
        raise PythonQualifiedReferenceDisclosureError(msg)
    source = reference.occurrence
    source_range = source.source_range
    target_range = target.support.source_range
    call_meaning = (
        "Yes: the qualified Name occupies ast.Call.func; "
        "no runtime invocation is asserted."
        if reference.direct_call
        else "No: this qualified Name is a Reference without the "
        "direct-call syntax tag."
    )
    text = "".join(
        (
            "Qualified Python Reference Context\n",
            f"Purpose: {context.disclosure.purpose}\n",
            f"Disclosure identity: {context.disclosure.identity}\n",
            f"Snapshot identity: {context.snapshot_id}\n",
            f"Reference fact identity: {reference.identity}\n",
            f"Reference derivation identity: {reference.derivation_identity}\n",
            f"Qualified relationship: {reference.PROPOSITION}\n",
            f"Resolution path: {reference.route.value}\n",
            f"Direct Call syntax: {call_meaning}\n",
            (
                "Coverage: qualified positive fact only; Reference analysis is "
                "non-exhaustive.\n"
            ),
            f"Source resource pointer: {source.resource_address}\n",
            f"Source content identity: {context.source_content_identity}\n",
            f"Reference Name location: {_location(source_range)}\n",
            (
                "Exact Reference Name UTF-8 bytes: "
                f"{len(context.reference_name_text.encode('utf-8'))}\n"
            ),
            "--- exact Reference Name begins ---\n",
            context.reference_name_text,
            "\n--- exact Reference Name ends ---\n",
            f"Target resource pointer: {target.support.resource_address}\n",
            f"Target content identity: {context.target_content_identity}\n",
            f"Target declared name: {target.declared_name}\n",
            f"Target declaration kind: {target.declaration_kind.value}\n",
            f"Target declaration location: {_location(target_range)}\n",
            (
                "Exact target declaration UTF-8 bytes: "
                f"{len(context.target_declaration_text.encode('utf-8'))}\n"
            ),
            "--- exact target declaration begins ---\n",
            context.target_declaration_text,
            "\n--- exact target declaration ends ---\n",
        ),
    )
    return RenderedPythonQualifiedReferenceContext(context, text)


def assemble_python_qualified_reference_model_request(
    *,
    task_request: ModelRequest,
    context: RenderedPythonQualifiedReferenceContext,
) -> ModelRequest:
    """Place realized Context after the task without changing request settings."""
    task_text = task_request.prompt.content
    prompt_content = "".join(
        (
            f"Task/instruction UTF-8 byte length: {len(task_text.encode('utf-8'))}\n",
            "--- task/instruction begins ---\n",
            task_text,
            "\n--- task/instruction ends ---\n\n",
            (
                "Supporting repository Context UTF-8 byte length: "
                f"{len(context.text.encode('utf-8'))}\n"
            ),
            "--- supporting repository Context begins ---\n",
            context.text,
            "\n--- supporting repository Context ends ---\n",
        ),
    )
    return replace(
        task_request,
        prompt=Prompt(prompt_content, role=task_request.prompt.role),
    )


def _snapshot_resource(
    snapshot: RepositorySnapshot,
    address: RepositoryResourceAddress,
    *,
    label: str,
) -> RepositoryResourceOccurrence:
    try:
        return snapshot.resource_at(address)
    except ValueError as error:
        msg = f"Qualified reference {label} resource is missing from the snapshot."
        raise PythonQualifiedReferenceDisclosureError(msg) from error


def _location(source_range: PythonSourceRange) -> str:
    return (
        f"{source_range.start_line}:{source_range.start_column_utf8}-"
        f"{source_range.end_line}:{source_range.end_column_utf8} "
        "(one-based lines; zero-based UTF-8 byte columns; exclusive end)"
    )


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()

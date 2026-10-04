# Copyright (c) 2026
"""Native structural support for unresolved resource witness members."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.localization.association.references import (
    PythonReferenceResourceSupport,
    validate_reference_support,
)
from devtools.context.localization.grounding import (
    AnchorGrounding,
    AnchorGroundingDisposition,
    ground_task_anchor,
)
from devtools.context.python.mirrored_paths import (
    PythonMirroredPathCorrespondence,
    derive_python_mirrored_path_correspondences,
)
from devtools.context.python.modules.interpretation import PythonModuleInterpretation
from devtools.context.repository.resource import RepositoryResourceOccurrence

if TYPE_CHECKING:
    from devtools.context.localization.grounding.contract import NativeGroundingReferent
    from devtools.context.localization.task import LocalizationTaskInterpretation
    from devtools.context.repository.snapshot import RepositorySnapshot


@dataclass(frozen=True, slots=True)
class OwnerResourceSupport:
    """An exact grounded native referent's observed owner resource."""

    grounding: AnchorGrounding


@dataclass(frozen=True, slots=True)
class MirroredResourceSupport:
    """An exact native source/test counterpart of a grounded owner resource."""

    grounding: AnchorGrounding
    correspondence: PythonMirroredPathCorrespondence


type StructuralMemberSupport = (
    OwnerResourceSupport | MirroredResourceSupport | PythonReferenceResourceSupport
)


def owner_resource(
    snapshot: RepositorySnapshot,
    referent: NativeGroundingReferent,
) -> RepositoryResourceOccurrence:
    """Project an already validated native referent to its observed resource."""
    if isinstance(referent, RepositoryResourceOccurrence):
        address = referent.address
    elif isinstance(referent, PythonModuleInterpretation):
        address = referent.resource.address
    else:
        address = referent.support.resource_address
    return snapshot.resource_at(address)


def validate_structural_support(
    *,
    task: LocalizationTaskInterpretation,
    snapshot: RepositorySnapshot,
    target: RepositoryResourceOccurrence,
    support: StructuralMemberSupport,
) -> None:
    """Replay the native seed and relationship; reject forged/stale support."""
    grounding = support.grounding
    replayed = ground_task_anchor(
        task=task,
        snapshot=snapshot,
        request=grounding.request,
        module_universe=grounding.module_universe,
    )
    if (
        replayed != grounding
        or grounding.disposition is not AnchorGroundingDisposition.RESOLVED
    ):
        msg = "Structural support has no current unique native grounding."
        raise ValueError(msg)
    if isinstance(support, PythonReferenceResourceSupport):
        validate_reference_support(support, snapshot, target)
        return
    source = owner_resource(snapshot, grounding.candidates[0].referent)
    if isinstance(support, OwnerResourceSupport):
        if target != source:
            msg = "Owner support target differs from the grounded native owner."
            raise ValueError(msg)
        return
    analysis = derive_python_mirrored_path_correspondences(snapshot)
    correspondence = support.correspondence
    if correspondence not in analysis.correspondences or not (
        (source == correspondence.source and target == correspondence.test)
        or (source == correspondence.test and target == correspondence.source)
    ):
        msg = "Mirrored support differs from the native snapshot correspondence."
        raise ValueError(msg)


def structural_support_key(support: StructuralMemberSupport) -> tuple[str, ...]:
    """Order provenance for replay, never by relevance or strength."""
    grounding = support.grounding
    return (
        type(support).__name__,
        grounding.request.anchor.value,
        grounding.resolver.value,
        _referent_key(grounding),
        support.correspondence.identity
        if isinstance(support, MirroredResourceSupport)
        else support.identity
        if isinstance(support, PythonReferenceResourceSupport)
        else "",
    )


def _referent_key(grounding: AnchorGrounding) -> str:
    if not grounding.candidates:
        return ""
    referent = grounding.candidates[0].referent
    if isinstance(referent, RepositoryResourceOccurrence):
        return referent.address.value
    return referent.identity

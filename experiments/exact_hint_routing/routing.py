# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- formatter owns commas; bounded experiment validation
"""Delegate admitted task hints to native grounding; never run lexical retrieval."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.localization.grounding.contract import (
    AnchorGrounding,
    AnchorGroundingDisposition,
    AnchorGroundingRequest,
    PythonDirectDeclarationKind,
    PythonDirectDeclarationLocator,
    PythonDirectMethodLocator,
    PythonModuleLocator,
    ResourceAddressLocator,
)
from devtools.context.localization.grounding.resolve import ground_task_anchor
from devtools.context.localization.identity import LocalizationAnchorIdentity
from devtools.context.localization.task import (
    LocalizationAnchor,
    LocalizationTaskInterpretation,
)
from devtools.context.python.classes.declarations import PythonClassDeclarationKnowledge
from devtools.context.python.modules.interpretation import (
    PythonModuleInterpretationUniverse,
    interpret_python_module_resources,
)
from devtools.context.repository.observation import (
    _CONTENT_IDENTITY_SEMANTICS,
    _semantic_digest,
)
from devtools.context.repository.resource import (
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
)
from experiments.exact_hint_routing.models import (
    ExactHintObservation,
    ExactHintResolution,
    ExactHintRouteRequest,
    HintAssociation,
    HintCategory,
    HintLocator,
    QualifiedMethodLocator,
    ResolutionDisposition,
)

if TYPE_CHECKING:
    from devtools.context.localization.grounding.contract import AnchorLocator
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )


@dataclass(frozen=True, slots=True)
class ExactFrame:
    """Bind only supplied native state and universes; no task-specific lookup."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    snapshot: RepositorySnapshot
    modules: PythonModuleInterpretationUniverse
    declaration_addresses: tuple[RepositoryResourceAddress, ...]

    def validate(self) -> None:  # noqa: C901 -- explicit native frame invariant checks
        """Reject foreign/stale state, malformed identities or incomplete universes."""
        if (
            self.snapshot.repository_id != self.repository_id
            or self.snapshot.id != self.snapshot_id
        ):
            raise ValueError("Foreign or stale exact frame")
        resources = self.snapshot.resources
        if len({r.address for r in resources}) != len(resources):
            raise ValueError("Exact frame repeats resources")
        for resource in resources:
            if (
                _semantic_digest(_CONTENT_IDENTITY_SEMANTICS, resource.content)
                != resource.content_identity.value
            ):
                raise ValueError("Exact frame content identity differs")
            if resource.byte_size != len(resource.content.encode("utf-8")):
                raise ValueError("Exact frame resource volume differs")
        if self.modules.repository_id != self.repository_id:
            raise ValueError("Foreign module universe")
        if len(set(self.declaration_addresses)) != len(self.declaration_addresses):
            raise ValueError("Duplicate declaration universe address")
        for address in self.declaration_addresses:
            self.snapshot.resource_at(address)
        for module in self.modules.interpretations:
            if (
                module.snapshot_id != self.snapshot_id
                or module.resource != self.snapshot.resource_at(module.resource.address)
            ):
                raise ValueError("Stale module interpretation")
            expected = interpret_python_module_resources(
                self.snapshot,
                module_root=module.module_root,
                resource_addresses=(module.resource.address,),
            )
            if expected.interpretations != (module,):
                raise ValueError("Fabricated module interpretation")
        if len({m.identity for m in self.modules.interpretations}) != len(
            self.modules.interpretations
        ):
            raise ValueError("Duplicate module interpretation")

    @property
    def identity(self) -> str:
        """Identify explicit resource/module/declaration memberships in one frame."""
        raw = repr(
            (
                str(self.repository_id),
                str(self.snapshot_id),
                self.modules.identity,
                tuple(
                    (str(r.address), str(r.content_identity))
                    for r in self.snapshot.resources
                ),
                tuple(str(a) for a in self.declaration_addresses),
            )
        )
        return hashlib.sha256(raw.encode()).hexdigest()


def admit(
    hint: ExactHintObservation, association: HintAssociation
) -> ExactHintRouteRequest:
    """Use syntax and declared native contracts only; no repository lookup."""
    parts = hint.text.split(".")
    locator: HintLocator = None
    mechanism = "UNSUPPORTED_EXACT_HINT"
    if hint.category is HintCategory.RESOURCE_ADDRESS:
        locator = ResourceAddressLocator(RepositoryResourceAddress(hint.text))
        mechanism = "repository-snapshot-resource-at"
    elif hint.category is HintCategory.PYTHON_MODULE:
        locator = PythonModuleLocator(hint.text)
        mechanism = "python-module-exact-name-lookup"
    elif (
        hint.category
        in {HintCategory.PYTHON_DIRECT_FUNCTION, HintCategory.PYTHON_DIRECT_CLASS}
        and len(parts) >= 2  # noqa: PLR2004 -- explicit module plus declaration
    ):
        locator = PythonDirectDeclarationLocator(
            PythonModuleLocator(".".join(parts[:-1])),
            parts[-1],
            PythonDirectDeclarationKind.CLASS
            if hint.category is HintCategory.PYTHON_DIRECT_CLASS
            else PythonDirectDeclarationKind.FUNCTION,
        )
        mechanism = "exact-python-module-source-declaration-selection-v1"
    elif hint.category is HintCategory.PYTHON_DIRECT_METHOD and len(parts) >= 3:  # noqa: PLR2004 -- module plus class/method
        locator = QualifiedMethodLocator(
            PythonModuleLocator(".".join(parts[:-2])), parts[-2], parts[-1]
        )
        mechanism = "exact-source-class-then-native-direct-method-containment-v1"
    return ExactHintRouteRequest(
        hint,
        association,
        locator,
        mechanism,
        "Explicit task syntax; static source locator in a frozen universe; "
        "no inferred owner"
        if locator
        else "Unqualified or unsupported hint has no sound v1 locator; "
        "retain lexical fallback",
    )


def _ground(
    frame: ExactFrame, route: ExactHintRouteRequest, locator: AnchorLocator
) -> AnchorGrounding:
    """Reuse native anchor grounding with the original task observation."""
    hint = route.hint
    anchor_id = LocalizationAnchorIdentity(hint.task, hint.identity.value)
    task = LocalizationTaskInterpretation(
        hint.task,
        hint.provenance,
        (LocalizationAnchor(anchor_id, hint.text, hint.provenance),),
        (),
    )
    request = AnchorGroundingRequest(
        hint.task,
        anchor_id,
        frame.repository_id,
        frame.snapshot_id,
        locator,
        hint.provenance,
    )
    return ground_task_anchor(
        task=task,
        snapshot=frame.snapshot,
        request=request,
        module_universe=frame.modules,
    )


def resolve(frame: ExactFrame, route: ExactHintRouteRequest) -> ExactHintResolution:
    """Execute one bounded exact route only when explicitly called; not Stage A."""
    frame.validate()
    if route != admit(route.hint, route.association):
        raise ValueError("Route differs from frozen admission policy")
    locator = route.locator
    evidence: tuple[AnchorGrounding, ...] = ()
    if locator is None:
        disposition = ResolutionDisposition.UNSUPPORTED
        reason = route.reason
    else:
        if isinstance(locator, QualifiedMethodLocator):
            parent = _ground(
                frame,
                route,
                PythonDirectDeclarationLocator(
                    locator.module,
                    locator.class_name,
                    PythonDirectDeclarationKind.CLASS,
                ),
            )
            evidence = (parent,)
            result = parent
            if parent.disposition is AnchorGroundingDisposition.RESOLVED:
                referent = parent.candidates[0].referent
                if not isinstance(referent, PythonClassDeclarationKnowledge):
                    raise TypeError("Native parent selection did not supply a class")
                result = _ground(
                    frame,
                    route,
                    PythonDirectMethodLocator(referent, locator.method_name),
                )
                evidence = (parent, result)
        else:
            result = _ground(frame, route, locator)
            evidence = (result,)
        disposition = ResolutionDisposition(result.disposition.name)
        reason = result.reason
    resources: tuple[RepositoryResourceOccurrence, ...] = ()
    if disposition is ResolutionDisposition.RESOLVED:
        referent = evidence[-1].candidates[0].referent
        if isinstance(referent, RepositoryResourceOccurrence):
            resources = (referent,)
        elif hasattr(referent, "resource"):
            resources = (referent.resource,)
        else:
            if referent.support.resource_address not in frame.declaration_addresses:
                raise ValueError("Declaration outside frozen native universe")
            resources = (frame.snapshot.resource_at(referent.support.resource_address),)
    return ExactHintResolution(
        route,
        disposition,
        resources,
        evidence,
        reason,
        frame.repository_id,
        frame.snapshot_id,
        frame.identity,
    )

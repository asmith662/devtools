# Copyright (c) 2026
"""Small deterministic task-relative view of bounded anchor groundings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.localization.grounding.contract import (
    AnchorGrounding,
    AnchorGroundingDisposition,
    AnchorGroundingRequest,
    PythonDirectDeclarationLocator,
    PythonDirectMethodLocator,
    PythonModuleLocator,
    ResourceAddressLocator,
)
from devtools.context.localization.grounding.resolve import ground_task_anchor

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.localization.grounding.contract import NativeGroundingReferent
    from devtools.context.localization.identity import LocalizationAnchorIdentity
    from devtools.context.localization.task import LocalizationTaskInterpretation
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretationUniverse,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot


@dataclass(frozen=True, slots=True)
class AnchorGroundingView:
    """Retain independent locator results without selecting or ranking referents."""

    task: LocalizationTaskInterpretation
    snapshot: RepositorySnapshot
    groundings: tuple[AnchorGrounding, ...]

    def for_anchor(
        self,
        anchor: LocalizationAnchorIdentity,
    ) -> tuple[AnchorGrounding, ...]:
        """Return all explicit requests for one known task-local anchor."""
        if anchor not in {item.identity for item in self.task.anchors}:
            msg = "Unknown task anchor."
            raise ValueError(msg)
        return tuple(item for item in self.groundings if item.request.anchor == anchor)

    def with_disposition(
        self,
        disposition: AnchorGroundingDisposition,
    ) -> tuple[AnchorGrounding, ...]:
        """Select accounts by bounded resolver outcome, not semantic status."""
        return tuple(
            item for item in self.groundings if item.disposition is disposition
        )

    @property
    def resolved(self) -> tuple[AnchorGrounding, ...]:
        """Return exact, uniquely supported locator results."""
        return self.with_disposition(AnchorGroundingDisposition.RESOLVED)

    @property
    def ambiguous(self) -> tuple[AnchorGrounding, ...]:
        """Return locator results lacking a unique bounded referent."""
        return self.with_disposition(AnchorGroundingDisposition.AMBIGUOUS)

    @property
    def unresolved(self) -> tuple[AnchorGrounding, ...]:
        """Return exact locator misses, without asserting absence of a concept."""
        return self.with_disposition(AnchorGroundingDisposition.UNRESOLVED)

    @property
    def unsupported(self) -> tuple[AnchorGrounding, ...]:
        """Return locator forms current native analysis cannot decide."""
        return self.with_disposition(AnchorGroundingDisposition.UNSUPPORTED)

    @property
    def anchors_without_resolved_locator(
        self,
    ) -> tuple[LocalizationAnchorIdentity, ...]:
        """Include unrequested anchors and anchors with only open locator results."""
        resolved = {item.request.anchor for item in self.resolved}
        return tuple(
            item.identity for item in self.task.anchors if item.identity not in resolved
        )

    def anchors_for_referent(
        self,
        referent: NativeGroundingReferent,
    ) -> tuple[LocalizationAnchorIdentity, ...]:
        """Find task anchors whose bounded result includes the same native target."""
        found = {
            grounding.request.anchor
            for grounding in self.groundings
            for candidate in grounding.candidates
            if candidate.referent == referent
        }
        return tuple(
            item.identity for item in self.task.anchors if item.identity in found
        )


def build_anchor_grounding_view(
    *,
    task: LocalizationTaskInterpretation,
    snapshot: RepositorySnapshot,
    requests: Sequence[AnchorGroundingRequest],
    module_universe: PythonModuleInterpretationUniverse | None = None,
) -> AnchorGroundingView:
    """Resolve each distinct explicit locator and retain deterministic order."""
    values = tuple(requests)
    if len({(item.anchor, item.locator) for item in values}) != len(values):
        msg = "Grounding view repeats a task-anchor locator request."
        raise ValueError(msg)
    anchor_order = {item.identity: index for index, item in enumerate(task.anchors)}
    ordered = sorted(
        values,
        key=lambda item: (
            anchor_order.get(item.anchor, len(anchor_order)),
            _locator_key(item),
        ),
    )
    groundings = tuple(
        ground_task_anchor(
            task=task,
            snapshot=snapshot,
            request=request,
            module_universe=module_universe,
        )
        for request in ordered
    )
    return AnchorGroundingView(task, snapshot, groundings)


def _locator_key(request: AnchorGroundingRequest) -> tuple[str, ...]:
    locator = request.locator
    if isinstance(locator, ResourceAddressLocator):
        return ("resource", locator.address.value)
    if isinstance(locator, PythonModuleLocator):
        return (
            "module",
            locator.dotted_name,
            locator.kind.value if locator.kind else "",
        )
    if isinstance(locator, PythonDirectDeclarationLocator):
        return (
            "declaration",
            locator.module.dotted_name,
            locator.module.kind.value if locator.module.kind else "",
            locator.declared_name,
            locator.kind.value,
        )
    if isinstance(locator, PythonDirectMethodLocator):
        return (
            "method",
            locator.containing_class.subject.identity,
            locator.declared_name,
        )
    msg = "Grounding view received an unsupported locator."
    raise ValueError(msg)
